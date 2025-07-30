import traceback, copy
import vcfcli.tools.module_requests as req
from vcfcli.tools.module_requests import generate_variant_dictionary
from vcfcli.conf import read_config as config
import vcfcli.tools.parse_genomic_data


class UTAAdapterClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines= config.uta_adapter_info_lines
        self.url_pattern = config.uta_adapter_src
        self.srv_prefix = config.uta_adapter_srv_prefix
        self.genomic_keys = config.uta_genomic_keys
        self.gene_keys = config.uta_gene_keys
        self.gene_response_keys = config.uta_gene_response_keys
        self.extract_keys = config.uta_genomic_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def generate_variant_list(self, variants, variant_list_without_alternate_alleles):
        """
        Generates a list of variants for module requests and the associated reference genome. Prioritizes hg38/GRCh38 positions if data is available.

        :param variants:
        :param variant_list_without_alternate_alleles:
        :return:
        """
        request_genome = self.genome_version
        check_for_hg38 = False
        variant_list = []
        if (self.genome_version == "hg19") or (self.genome_version=="GRCh37"):
            check_for_hg38 = True
            request_genome="hg38"
        for var in variant_list_without_alternate_alleles:
            if check_for_hg38:
                if "POS_hg38" in variants[var]["variant_data"]:
                    hg38_id = variants[var]["variant_data"]["CHROM"] + ":" + variants[var]["variant_data"]["POS_hg38"] \
                              + variants[var]["variant_data"]["REF"] + ">" + variants[var]["variant_data"]["ALT"]
                    variant_list.append(hg38_id)
                else:
                    variant_list.append("")
            else:
                variant_list.append(var)

        return variant_list, request_genome

    def process_data(self, vcf_lines):
        """
        Retrieves genomic, transcriptomic and proteomic data from the Coordinates Converter service

        :param vcf_lines:
        :return:
        """
        qid_list = copy.deepcopy(list(vcf_lines.keys()))
        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            variants_without_alternate_alleles = vcfcli.tools.filter_alternate_alleles(qids_partial)
            request_genome_version = self.genome_version
            variants = ','.join(variants_without_alternate_alleles)

            try:
                json_body = req.get_connection(variants, self.url_pattern, request_genome_version)
    
                for item in json_body:
                            qid = str(item["header"]["qid"])
    
                            if item["data"] is not None:
                                # add variant data
                                if config.variant_data_key not in vcf_lines[qid]:
                                    vcf_lines[qid][config.variant_data_key] = {}
    
                                if type(item["data"]) is dict:
    
                                    if "gene name" in item["data"]:
                                        vcf_lines[qid][config.variant_data_key]['Gene name'] = item["data"]["gene_name"]
                                        vcf_lines[qid][config.variant_data_key]['Variant exchange'] = item["data"]["variant_exchange"]
                                        vcf_lines[qid][config.variant_data_key]['Biomarker'] = item["data"]["gene_name"] + " " + item["data"][
                                            "variant_exchange"]
    
                                    chr, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(
                                        qid)
                                    vcf_lines[qid][config.variant_data_key]['CHROM'] = chr
                                    vcf_lines[qid][config.variant_data_key]['reference_sequence'] = ref_seq
                                    vcf_lines[qid][config.variant_data_key]['POS'] = pos
                                    vcf_lines[qid][config.variant_data_key]['REF'] = ref
                                    vcf_lines[qid][config.variant_data_key]['ALT'] = alt
                                    vcf_lines[qid][config.variant_data_key]['POS_' + self.genome_version] = pos
                                    vcf_lines[qid][config.variant_data_key]['ID'] = ''
                                    vcf_lines[qid][config.variant_data_key]['QUAL'] = ''
                                    vcf_lines[qid][config.variant_data_key]['FILTER'] = ''
    
                                    vcf_lines[qid][self.srv_prefix] = item["data"]
                                else:
                                    vcf_lines[qid][self.srv_prefix] = {}
                                    vcf_lines[qid][self.srv_prefix]["status"] = 400
                                    vcf_lines[qid][self.srv_prefix]["msg"] = item["data"]
            except:
                print("error: genomic to gene")
                print(traceback.format_exc())

            for i in range(0, max_length):
                del qid_list[0] #qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
