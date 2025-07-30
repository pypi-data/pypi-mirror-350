import re
import adagenes
from adagenes.conf import read_config as config
import adagenes.tools.hgvs_re as gencode
from adagenes.tools.preprocessing import get_variant_request_type, get_genome_location, get_chr


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
    bframe_data_new = {}
    for var in bframe.data.keys():

            biomarker_type, groups = get_variant_request_type(var)
            print("biomarker type(" + var + "): ",biomarker_type)

            # gene fusion
            if biomarker_type == "fusion":
                #print("gene fusion match ",var)
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "g"
                bframe_data_new[var]["mutation_type"] = "fusion"
            # protein identifiers
            elif biomarker_type == "gene_name_aa_exchange":
                # gene name, variant exchange
                var_new = adagenes.normalize_protein_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var]["type"] = "p"
                bframe_data_new[var]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_long":
                # gene name, variant exchange
                var_new = adagenes.normalize_protein_identifier(var, add_refseq=False, target="one-letter")
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "p"
                bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_refseq":
                var_new = adagenes.normalize_protein_identifier(var, add_refseq=False, target="one-letter")
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "p"
                bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name_aa_exchange_long_refseq":
                var_new = adagenes.normalize_protein_identifier(var, add_refseq=False, target="one-letter")
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "p"
                bframe_data_new[var_new]["mutation_type"] = "snv"
            # genome identifiers
            elif biomarker_type == "genomic_location":
                var_new = var.replace("CHR", "chr")
                var_new = adagenes.normalize_dna_identifier(var_new, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                aa_groups = re.compile(gencode.exp_genome_positions).match(var).groups()
                ref = aa_groups[3]
                alt = aa_groups[4]
                if len(ref) != len(alt):
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "indel"
                else:
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_refseq":
                var = var.replace("CHR", "chr")
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                aa_groups = re.compile(gencode.exp_genome_positions_refseq).match(var).groups()
                if len(aa_groups[4]) != len(aa_groups[5]):
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "indel"
                else:
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_nc":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                aa_groups = re.compile(gencode.exp_genome_positions_nc).match(var).groups()
                if len(aa_groups[2]) != len(aa_groups[3]):
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "indel"
                else:
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "genomic_location_nc_refseq":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                aa_groups = re.compile(gencode.exp_genome_positions_nc_refseq).match(var).groups()
                if len(aa_groups[3]) != len(aa_groups[4]):
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "indel"
                else:
                    bframe_data_new[var_new]["type"] = "g"
                    bframe_data_new[var_new]["mutation_type"] = "snv"
            elif biomarker_type == "gene_name":
                # gene name
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "g"
                bframe_data_new[var]["mutation_type"] = "gene"
            # InDels
            elif biomarker_type == "deletion":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "deletion_nc":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                aa_groups = re.compile(gencode.exp_deletion_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var_new]["type"] = "g"
                bframe.data[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "deletion_nc_long":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                aa_groups = re.compile(gencode.exp_deletion_ncbichrom_long).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe.data[var_new]["type"] = "g"
                bframe.data[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "insertion":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "insertion_nc":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                aa_groups = re.compile(gencode.exp_insertion_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "indel":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "indel_nc":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                aa_groups = re.compile(gencode.exp_indel_ncbichrom).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "indel_nc_long":
                var_new = adagenes.normalize_dna_identifier(var, add_refseq=False)
                aa_groups = re.compile(gencode.exp_indel_ncbichrom_long).match(var).groups()
                chrom = get_chr(aa_groups[0])
                genpos = chrom[0] + ":" + aa_groups[1]
                bframe_data_new[var_new] = bframe.data[var]
                bframe_data_new[var_new]["type"] = "g"
                bframe_data_new[var_new]["mutation_type"] = "indel"
            elif biomarker_type == "refseq_transcript":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "snv"
            elif biomarker_type == "refseq_transcript_gene":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "snv"
            elif biomarker_type == "del_transcript_cdna":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "indel"
            elif biomarker_type == "del_transcript_gene_cdna":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "indel"
            elif biomarker_type == "del_transcript_cdna_long":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "indel"
            elif biomarker_type == "del_transcript_gene_cdna_long":
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "r"
                bframe_data_new[var]["mutation_type"] = "indel"

            else:
                print("Could not match query: ",var)
                bframe_data_new[var] = bframe.data[var]
                bframe_data_new[var]["type"] = "g"
                bframe_data_new[var]["mutation_type"] = "unidentified"

    bframe.data = bframe_data_new
    return bframe
