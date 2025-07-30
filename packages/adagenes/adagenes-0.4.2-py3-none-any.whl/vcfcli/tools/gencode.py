import re
import vcfcli


def convert_aa_exchange_to_single_letter_code(aa_exchange):
    """
    Converts a multiple letter variant exchange into single letter codes

    :param aa_exchange:
    :return:
    """
    if re.compile(variant_exchange_long_pt_ext).match(aa_exchange):
        groups = re.compile(variant_exchange_long_pt_ext).match(aa_exchange).groups()
        #print(groups)
        try:
            aa_1 = groups[0].lower()
            aa_2 = groups[2].lower()
            aa1_single = protein_dc_lower[aa_1]
            aa2_single = protein_dc_lower[aa_2]
        except:
            print("error converting multiple letter code into single letter code: ", aa_1, ",", aa_2)
            return aa_exchange
        return aa1_single + groups[1] + aa2_single
    else:
        return None


def convert_to_single_letter_code(aa):
    """

    :param aa:
    :return:
    """
    if aa in vcfcli.tools.gencode.protein_dc:
        return vcfcli.tools.gencode.protein_dc[aa]
    else:
        return None


# genomic location patterns
gene_symbol_pt = '([A-Z|a-z|0-9]+)'
variant_exchange_pt = '([a-z|A-Z][0-9]+[a-z|A-Z])'
variant_exchange_long_pt = '([a-z|A-Z]+[0-9]+[a-z|A-Z]+)'
variant_exchange_long_pt_ext = '([a-z|A-Z]+)([0-9]+)([a-z|A-Z]+)'

variant_exchange_pt_refseq = '([p|P]\\.)' + variant_exchange_pt
variant_exchange_long_pt_refseq = '([p|P]\\.)' + variant_exchange_long_pt

exp_gene_name = '(^[A-Za-z0-9]+)$'

exp_gene_name_variant_exchange = gene_symbol_pt + ":" + variant_exchange_pt
exp_gene_name_variant_exchange_long = gene_symbol_pt + ":" + variant_exchange_long_pt

exp_gene_name_variant_exchange_refseq = gene_symbol_pt + ":" + variant_exchange_pt_refseq
exp_gene_name_variant_exchange_long_refseq = gene_symbol_pt + ":" + variant_exchange_long_pt_refseq

chr_pt = '([c|C][h|H][r|R])([X|Y|N|M|x|y|n|m|0-9]+)'
refseq_chromosome_pt = '(NC_[0-9]+\.[0-9]+)'
refseq_transcript = '(NM_[0-9]+\\.[0-9]+)'

ref_seq_pt = '([p|P|c|C|o|O|r|R][\\.])'
ref_seq_gt = '([g|G]\\.)'
pos_pt = '([0-9]+)'
ref_pt = '([A|C|G|T]+)'
alt_pt = '([A|C|G|T]+)'

refseq_transcript_aaexchange_snv = '([c|C]\\.[0-9]+[A|C|G|T|N]+>[A|C|G|T|N]+)'
# e.g. c.4375_4376insACCT
refseq_transcript_aaexchange_ins = '([g|G]?[\\.]?[0-9]+_[0-9]+[i|I][n|N][s|S][C|G|A|T|N]+)'
# e.g. c.4375_4379del or c.4375_4379delCGATT
refseq_transcript_aaexchange_del = '([g|G]?[\\.]?[0-9]+[d|D][e|E][l|L])'
refseq_transcript_aaexchange_del_long = '([g|G]?[\\.]?[0-9]+_[0-9]+[d|D][e|E][l|L])'
# e.g. c.4375_4385dup
# or c.4375_4385dupCGATTATTCCA
refseq_transcript_aaexchange_dup = '(c\\.[0-9]+_[0-9]+dup[C|G|A|T]?)'
# e.g. c.4375_4376delinsACTT
# or c.4375_4376delCGinsAGTT
# delins e.g. NC_000001.11:g.123delinsAC
refseq_transcript_aaexchange_delins = '([g|G]?[\\.]?[0-9]+[d|D][e|E][l|L][i|I][n|N][s|S][A|C|G|T|N]?)'
refseq_transcript_aaexchange_delins_long = '([g|G]?[\\.]?[0-9]+_[0-9]+[d|D][e|E][l|L][i|I][n|N][s|S][A|C|G|T|N]?)'
#refseq_transcript_aaexchange_insdel = '(c\\.[0-9]+_[0-9]delins[C|G|A|T]?)'

# SNV: Genomic location
exp_genome_positions = chr_pt + ":" + pos_pt + ref_pt + ">" + alt_pt
exp_genome_positions_nc = refseq_chromosome_pt + ":" + pos_pt + ref_pt + ">" + alt_pt
exp_genome_positions_refseq = chr_pt + ":" + ref_seq_gt + pos_pt + ref_pt + ">" + alt_pt
exp_genome_positions_nc_refseq = refseq_chromosome_pt + ":" + ref_seq_gt + pos_pt + ref_pt + ">" + alt_pt

# InDel
exp_insertion = chr_pt + ":" + refseq_transcript_aaexchange_ins
exp_insertion_ncbichrom = refseq_chromosome_pt + ":" + refseq_transcript_aaexchange_ins
exp_deletion = chr_pt + ":" + refseq_transcript_aaexchange_del
exp_deletion_ncbichrom = refseq_chromosome_pt + ":" + refseq_transcript_aaexchange_del
exp_deletion_long = chr_pt + ":" + refseq_transcript_aaexchange_del_long
exp_deletion_ncbichrom_long = refseq_chromosome_pt + ":" + refseq_transcript_aaexchange_del_long
exp_indel = chr_pt + ":" + refseq_transcript_aaexchange_delins
exp_indel_ncbichrom = refseq_chromosome_pt + ":" + refseq_transcript_aaexchange_delins
exp_indel_long = chr_pt + ":" + refseq_transcript_aaexchange_delins_long
exp_indel_ncbichrom_long = refseq_chromosome_pt + ":" + refseq_transcript_aaexchange_delins_long

# Transcript
exp_refseq_transcript_pt = refseq_transcript + ":" + refseq_transcript_aaexchange_snv

exp_fusions = '(CHR[0-9|X|Y]+:[0-9]+)-(CHR[0-9|X|Y]+:[0-9]+)'

aalist = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V","U","O","B","Z","X"]

protein_dc_lower = {
    "ala": "A",
    "arg": "R",
    "asn": "N",
    "asp": "D",
    "cys": "C",
    "gln": "Q",
    "glu": "E",
    "gly": "G",
    "his": "H",
    "ile": "I",
    "leu": "L",
    "lys": "K",
    "met": "M",
    "phe": "F",
    "pro": "P",
    "ser": "S",
    "thr": "T",
    "trp": "W",
    "tyr": "Y",
    "val": "V",
    "sec": "U",
    "pyl": "O",
    "asx": "B",
    "glx": "Z",
    "xaa": "X"
}

protein_dc_upper = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "SEC": "U",
    "PYL": "O",
    "ASX": "B",
    "GLX": "Z",
    "XAA": "X"
}

protein_dc = {
    "Ala": "A",
    "Arg": "R",
    "Asn": "N",
    "Asp": "D",
    "Cys": "C",
    "Gln": "Q",
    "Glu": "E",
    "Gly": "G",
    "His": "H",
    "Ile": "I",
    "Leu": "L",
    "Lys": "K",
    "Met": "M",
    "Phe": "F",
    "Pro": "P",
    "Ser": "S",
    "Thr": "T",
    "Trp": "W",
    "Tyr": "Y",
    "Val": "V",
    "Sec": "U",
    "Pyl": "O",
    "Asx": "B",
    "Glx": "Z",
    "Xaa": "X"
}
