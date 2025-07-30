import re
import vcfcli
import vcfcli.tools.hgvs_re as hgvs_re
import vcfcli.tools


def normalize_protein_identifier(protein, target="one-letter", add_refseq=True):
    """

    :param protein:
    :return:
    """
    protein_normalized = ""
    request_type, groups = vcfcli.get_variant_request_type(protein)

    refseq = ""
    if add_refseq is True:
        refseq = "p."

    if request_type == "gene_name_aa_exchange":
        if target == "one-letter":
            gene = groups[0]
            aaex = groups[1]
            protein_normalized = gene + ":" + refseq + aaex
        elif target == "3-letter":
            protein_normalized = convert_protein_to_multiple_letter_code(protein,add_refseq=add_refseq)
    elif request_type == "gene_name_aa_exchange_long":
        if target == "one-letter":
            protein_normalized = convert_protein_to_single_letter_code(protein, add_refseq=add_refseq)
        elif target == "3-letter":
            gene = groups[0]
            aaex = groups[1]
            protein_normalized = gene + ":" + refseq + aaex
    elif request_type == "gene_name_aa_exchange_refseq":
        if target == "one-letter":
            if add_refseq is True:
                protein_normalized = protein
            else:
                gene = groups[0]
                aaex = groups[2]
                protein_normalized = gene + ":" + aaex
        else:
            protein_normalized = convert_protein_to_multiple_letter_code(protein,add_refseq=add_refseq)
    elif request_type == "gene_name_aa_exchange_long_refseq":
        if target == "one-letter":
            protein_normalized = convert_protein_to_single_letter_code(protein, add_refseq=add_refseq)
        else:
            protein_normalized = protein
    else:
        protein_normalized = protein

    return protein_normalized


def normalize_transcript_identifier(transcript):
    """

    :param transcript:
    :return:
    """
    transcript_normalized = ""

    return transcript_normalized


def normalize_dna_identifier_position(var, add_refseq=True):
    """

    :param var:
    :param add_refseq:
    :return:
    """
    if re.compile(hgvs_re.exp_positions).match(var):
        aa_groups = re.compile(hgvs_re.exp_positions).match(var).groups()
        chrom = aa_groups[0]
        refseq = ""
        if add_refseq is True:
            refseq = "g."
        if len(aa_groups) == 4:
            pos = aa_groups[3]
        elif len(aa_groups) == 3:
            pos = aa_groups[2]
        return chrom + aa_groups[1] + ":" + refseq + pos

def normalize_dna_identifier(var, target="vcf", add_refseq=True):
    """

    :param dna_id:
    :param target:
    :return:
    """
    if re.compile(hgvs_re.exp_genome_positions_nc).match(var):
        aa_groups = re.compile(hgvs_re.exp_genome_positions_nc).match(var).groups()
        chrom = vcfcli.tools.get_chr(aa_groups[0])[0]
        pos = aa_groups[1]
        ref = aa_groups[2]
        alt = aa_groups[3]
    elif re.compile(hgvs_re.exp_genome_positions_nc_refseq).match(var):
        aa_groups = re.compile(hgvs_re.exp_genome_positions_nc_refseq).match(var).groups()
        chrom = vcfcli.tools.get_chr(aa_groups[0])[0]
        pos = aa_groups[2]
        ref = aa_groups[3]
        alt = aa_groups[4]
    elif re.compile(hgvs_re.exp_genome_positions).match(var):
        aa_groups = re.compile(hgvs_re.exp_genome_positions).match(var).groups()
        chrom = "chr" + aa_groups[1]
        pos = aa_groups[2]
        ref = aa_groups[3]
        alt = aa_groups[4]
    elif re.compile(hgvs_re.exp_genome_positions_refseq).match(var):
        aa_groups = re.compile(hgvs_re.exp_genome_positions_refseq).match(var).groups()
        chrom = "chr" + aa_groups[1]
        pos = aa_groups[3]
        ref = aa_groups[4]
        alt = aa_groups[5]
    else:
        return var

    refseq = "g."
    if add_refseq is False:
        refseq = ""
    var = chrom + ":" + refseq + pos + ref + ">" + alt

    return var


def convert_protein_to_single_letter_code(var, add_refseq=True):
    """
    Convert a protein identifier from 3-letter to single letter codes

    :param aa_groups: 3-letter protein identifier, e.g. 'BRAF:p.Argt600Glue'
    :return:
    """
    if re.compile(hgvs_re.exp_gene_name_variant_exchange_long).match(var):
        aa_groups = re.compile(hgvs_re.exp_gene_name_variant_exchange_long).match(var).groups()
        aa_exchange = aa_groups[1]
    elif re.compile(hgvs_re.exp_gene_name_variant_exchange_long_refseq).match(var):
        aa_groups = re.compile(hgvs_re.exp_gene_name_variant_exchange_long_refseq).match(var).groups()
        aa_exchange = aa_groups[2]
    else:
        return var

    aa_exchange_single_letter = hgvs_re.convert_aa_exchange_to_single_letter_code(aa_exchange)
    var = aa_groups[0] + ":" + aa_exchange_single_letter

    return var


def convert_protein_to_multiple_letter_code(var, add_refseq=True):
    """
    Convert a protein identifier from single letter to 3-letter codes

    :param var:
    :return:
    """
    if re.compile(hgvs_re.exp_gene_name_variant_exchange).match(var):
        aa_groups = re.compile(hgvs_re.exp_gene_name_variant_exchange).match(var).groups()
        aa_exchange = aa_groups[1]
    elif re.compile(hgvs_re.exp_gene_name_variant_exchange_refseq).match(var):
        aa_groups = re.compile(hgvs_re.exp_gene_name_variant_exchange_refseq).match(var).groups()
        aa_exchange = aa_groups[2]
    else:
        return var

    aa_exchange_single_letter = hgvs_re.convert_aa_exchange_to_multiple_letter_code(aa_exchange)
    refseq = "p."
    if add_refseq is False:
        refseq = ""
    var = aa_groups[0] + ":" + refseq + aa_exchange_single_letter
    return var
