import re
import vcfcli
from vcfcli.conf import read_config as config
import vcfcli.tools.hgvs_re as gencode
from vcfcli.tools.preprocessing import get_variant_request_type, get_genome_location, get_chr


def normalize_variant_request(request, target):
    """
    Normalizes a text-based request according to the HGVS notation into a target notation on DNA, transcript or protein
    level.
    Example: A request on protein level, characterized by HUGO gene symbol and amino acid exchange "BRAF:V600E",
    can be converted

    :param request:
    :param target:
    :return:
    """
    normalized_request = ""

    variant_type = get_variant_request_type(request)

    return normalized_request


def identify_biomarkers(bframe):
    """
    Identify requested variants in a search query and retrieve them either as gene names or as genome positions.
    Identifies whether a text query contains a gene name and variant exchange or a genome position
    Retrieves comma-separated lists of text input, gene names and variant exchange in the format GENE_NAME:VAR_EXCHANGE, and genome positions.
    Returns a list of gene names and variant exchange, a list of genome positions and a list of identified gene fusions

    :param bframe
    :return: Dictionaries for biomarkers separated by gene_names, snvs, indels, genome_positions and gene fusions
    :vartype query: str | list
    """

    for var in bframe.data.keys():

            biomarker_type = get_variant_request_type(var)
            #print("biomarker type(" + var + "): ",biomarker_type)

            # gene fusion
            if biomarker_type == "fusion":
                #print("gene fusion match ",var)
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "fusion"
            elif biomarker_type == "gene_name_aa_exchange":
                # gene name, variant exchange
                #print("Request match: Gene name, variant exchange ", var)
                bframe.data[var]["type"] = "p"
                bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_long":
                # gene name, variant exchange
                #print("Request match: Gene name, variant exchange (long)", var)
                var = vcfcli.tools.convert_protein_to_single_letter_code(var)
                bframe.data[var]["type"] = "p"
                bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_refseq":
                #print("Request type: Gene name:(Reference sequence) protein change")
                aa_groups = re.compile(gencode.exp_gene_name_variant_exchange_refseq).match(var).groups()
                var = aa_groups[0] + ":" + aa_groups[2]
                #print("new identifier: ",var)

                bframe.data[var]["type"] = "p"
                bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_long_refseq":
                #print("Request type: Gene name:(Reference sequence) protein change (long)")
                var = vcfcli.tools.convert_protein_to_single_letter_code(var)
                #print("new identifier: ",var)
                bframe.data[var]["type"] = "p"
                bframe.data[var]["mutation_type"] = "snv"

            elif biomarker_type == "genomic_location":
                # genomic location
                aa_groups = re.compile(gencode.exp_genome_positions).match(var).groups()
                ref = aa_groups[3]
                alt = aa_groups[4]
                if len(ref) != len(alt):
                    var = var.replace("CHR", "chr")

                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "indel"
                else:
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_refseq":
                aa_groups = re.compile(gencode.exp_genome_positions_refseq).match(var).groups()
                genpos = 'chr' + aa_groups[1] + ":" + aa_groups[3] + aa_groups[4] + ">" + aa_groups[5]
                if len(aa_groups[4]) != len(aa_groups[5]):
                    var = var.replace("CHR", "chr")
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "indel"
                else:
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_nc":
                aa_groups = re.compile(gencode.exp_genome_positions_nc).match(var).groups()
                var = vcfcli.normalize_dna_identifier(var, add_refseq=False)
                if len(aa_groups[2]) != len(aa_groups[3]):
                    var = var.replace("CHR", "chr")
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "indel"
                else:
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_nc_refseq":
                aa_groups = re.compile(gencode.exp_genome_positions_nc_refseq).match(var).groups()
                chrom = get_chr(aa_groups[0])
                var = chrom[0] + ":" + aa_groups[2] + aa_groups[3] + ">" + aa_groups[4]
                if len(aa_groups[3]) != len(aa_groups[4]):
                    var = var.replace("CHR","chr")
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "indel"
                else:
                    bframe.data[var]["type"] = "g"
                    bframe.data[var]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name":
                # gene name
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "gene"
            elif biomarker_type == "deletion":
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "deletion_nc":
                aa_groups = re.compile(gencode.exp_deletion_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "deletion_nc_long":
                aa_groups = re.compile(gencode.exp_deletion_ncbichrom_long).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "insertion":
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "insertion_nc":
                aa_groups = re.compile(gencode.exp_insertion_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "indel":
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "indel_nc":
                aa_groups = re.compile(gencode.exp_indel_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            elif biomarker_type == "indel_nc_long":
                aa_groups = re.compile(gencode.exp_indel_ncbichrom_long).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "indel"
            else:
                print("Could not match query: ",var)
                bframe.data[var]["type"] = "g"
                bframe.data[var]["mutation_type"] = "unidentified"

    return bframe
