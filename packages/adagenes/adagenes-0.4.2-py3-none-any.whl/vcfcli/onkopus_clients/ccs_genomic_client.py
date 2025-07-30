import pandas as pd, traceback
import vcfcli.tools.module_requests as req
import vcfcli.tools.parse_genomic_data
from vcfcli.conf import read_config as config
from vcfcli.tools import split_gene_name


def filter_empty_variants(q):
    """
    Filters all variants without a gene name and protein change from the query string

    :param q:
    :return:
    """
    q_new = ""
    q_elements = q.split(",")
    for el in q_elements:
        if (el == "") or (el == ":"):
            pass
        else:
            q_new += el + ","
    q_new = q_new.rstrip(",")
    return q_new


def generate_variant_str_from_gene_names_prot_change(vcf_lines):
    """
    Generates a GeneToGenomic request to the Coordinates Converter service by extracting the protein information from the biomarker
    keys, where keys should be of the format [gene_symbol]:[aa_exchange] (e.g. BRAF:V600E)

    :param vcf_lines:
    :return:
    """
    q = ""
    for variant in vcf_lines.keys():
        resp = split_gene_name(variant)
        if resp:
            gene, variant_exchange = resp[0], resp[1]
            q += gene+":"+variant_exchange+","
    q = q.rstrip(",")
    return q


def generate_variant_str_from_data_in_json(vcf_lines):
    """
    Generates a GeneToGenomic request to the Coordinates Converter by extracting gene names and amino acid exchange from the biomarker data.
    Usable if a biomarker frame has already been annotated with the CCS GenomicToGene service and should be enriched with additional
    data by the GeneToGenomic service

    :param vcf_lines:
    :return:
    """
    q = ""
    for variant in vcf_lines.keys():
        if config.uta_adapter_srv_prefix in vcf_lines[variant]:
            gene = vcf_lines[variant][config.uta_adapter_srv_prefix]["gene_name"]
            aa_exchange = vcf_lines[variant][config.uta_adapter_srv_prefix]["variant_exchange"]
            q += gene + ":" + aa_exchange + ","
    q = q.rstrip(",")
    return q


class CCSGeneToGenomicClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.error_logfile = error_logfile
        self.srv_prefix = config.uta_adapter_genetogenomic_srv_prefix


    def generate_request_str_of_gene_names(self, vcf_lines,input_format='json'):
        """


        :param vcf_lines:
        :param input_format:
        :return:
        """

        #print("extract data: ",vcf_lines)
        variant_list=[]

        if input_format == 'vcf':
            keys = [config.uta_adapter_srv_prefix + config.concat_char + config.uta_genomic_keys[0],
                    config.uta_adapter_srv_prefix + config.concat_char + config.uta_genomic_keys[0]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_vcf(vcf_lines, keys)
        elif input_format == 'tsv':
            keys = [config.uta_genomic_keys[0], config.uta_genomic_keys[1]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines,
                                                                          config.uta_adapter_genetogenomic_srv_prefix, keys)
        else:
            keys = [config.uta_genomic_keys[0], config.uta_genomic_keys[1]]
            annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)

        gene_names = annotations[keys[0]]
        variants = annotations[keys[1]]
        for i in range(0,len(gene_names)):
            variant_list.append(gene_names[i]+":"+variants[i])

        #print(variant_list)
        variant_str = ','.join(variant_list)
        variant_str = filter_empty_variants(variant_str)
        print("req",variant_str)
        return variant_str, variant_list

    def generate_genome_locations_as_keys(self, gene_data):

        annotated_data = {}
        for gene_name, value in gene_data.items():

            # extract genomic locations
            if 'results_string' in value:
                results_string = value['results_string']
                chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(results_string)
                genompos = "chr" + chr + ":" + pos + ref + ">" + alt

                annotated_data[genompos] = {}
                annotated_data[genompos][config.uta_adapter_genetogenomic_srv_prefix] = value
                annotated_data[genompos]['variant_data'] = gene_data[gene_name]['variant_data']
            else:
                pass

        return annotated_data

    def process_data(self, vcf_lines):
        """
        Extracts gene names and protein change from biomarker data and retrieves genomic data from the Coordinates Converter service

        :param gene_data:
        :param input_format:
        :return:
        """
        # generate query string
        #variant_str, variant_list = self.generate_request_str_of_gene_names(gene_data,input_format=input_format)
        gene_names_from_structure = False
        for var in vcf_lines:
            if config.uta_adapter_srv_prefix in vcf_lines[var]:
                gene_names_from_structure = True

        if gene_names_from_structure is False:
            variant_str = generate_variant_str_from_gene_names_prot_change(vcf_lines)
        else:
            variant_str = generate_variant_str_from_data_in_json(vcf_lines)

        annotated_data = {}

        try:
            json_body = req.get_connection(variant_str,config.uta_adapter_genetogenomic_src,self.genome_version)
            for item in json_body:

                if (item["data"] is not None) and not (isinstance(item["data"],str)):
                    for res in item["data"]:
                            if res != "Error":
                                try:
                                    results_string = res['results_string']
                                    chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(
                                        results_string)
                                    qid = 'chr' + chr + ':' + pos + ref + '>' + alt

                                    annotated_data[qid] = {}
                                    annotated_data[qid][config.variant_data_key] = {}

                                    annotated_data[qid][config.variant_data_key]['CHROM'] = chr
                                    annotated_data[qid][config.variant_data_key]['reference_sequence'] = ref_seq
                                    annotated_data[qid][config.variant_data_key]['POS'] = pos
                                    annotated_data[qid][config.variant_data_key]['REF'] = ref
                                    annotated_data[qid][config.variant_data_key]['ALT'] = alt
                                    annotated_data[qid][config.variant_data_key]['POS_'+self.genome_version] = pos
                                    annotated_data[qid]["q_id"] = "chr" + chr + ":" + str(pos) + ref + ">" + alt
                                    annotated_data[qid][config.variant_data_key]['ID'] = ''
                                    annotated_data[qid][config.variant_data_key]['QUAL'] = ''
                                    annotated_data[qid][config.variant_data_key]['FILTER'] = ''

                                    annotated_data[qid][self.srv_prefix] = res
                                except:
                                    print("Error retrieving genomic UTA response ",res)
                                    print(traceback.format_exc())
                else:
                    qid = item["header"]["qid"]
                    gene,protein=qid.split(":")
                    annotated_data[qid] = {}
                    annotated_data[qid][config.variant_data_key] = {}
                    annotated_data[qid][config.variant_data_key]["gene"] = gene
                    annotated_data[qid][config.variant_data_key]["variant_exchange"] = protein
                    annotated_data[qid][config.variant_data_key]["type"] = "unidentified"
                    annotated_data[qid][config.variant_data_key]["status"] = "error"
                    annotated_data[qid][config.variant_data_key]["status_msg"] = item["data"]
        except:
            print("error: genomic to gene")
            print(traceback.format_exc())

        return annotated_data
