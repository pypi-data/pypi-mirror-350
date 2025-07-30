import re, logging
import pandas as pd
from vcfcli.conf import read_config as config


def generate_dictionary(list1, list2):
    """
    Generates a dictionary from two lists, where the first list respresents the keys and the second list represents the
    values of the dictionary

    :param list1:
    :param list2:
    :return:
    """
    dc = {}
    for i, el in enumerate(list1):
        dc[el] = list2[i]
    return dc


def generate_liftover_genompos(variant,liftover_pos):
    chrom, ref_seq, pos, ref, alt = parse_genome_position(variant)
    liftover_genompos = "chr" + str(chrom) + ":" + str(liftover_pos) + ref+ ">" + alt
    return liftover_genompos


def generate_liftover_qid_list(variant_list, liftover_position_list):
    liftover_dc = {}
    variant_dc = {}

    for i, variant in enumerate(variant_list):
        liftover_genompos = generate_liftover_genompos(variant, liftover_position_list[i])
        variant_dc[variant] = liftover_genompos
        liftover_dc[liftover_genompos] = variant

    return variant_dc, liftover_dc


def parse_variant_exchange(variant_exchange):
    rsregex = "([A-Za-z]+)([0-9]+)([A-Za-z\\?\\*=.]+)"
    if re.compile(rsregex).match(variant_exchange):
        p = re.compile(rsregex).match(variant_exchange).groups()
        aaref = p[0]
        pos = p[1]
        aaalt = p[2]
        return aaref, pos, aaalt
    else:
        return None, None, None


def parse_genome_position(genompos):
    """
    Parses and returns the components of a genomic location. Returns the chromosome, reference sequence, postion,
    reference allele and alternate allele

    :param genompos:
    :return:
    """
    rsregex = "(NC_[0]+)([1-9|X|Y][0-9|X|Y]?).([0-9]+):(g.|c.)?([0-9]+)([A|C|G|T|-]+)>([A|C|G|T|-]+)"
    if re.compile(rsregex).match(genompos):
        p = re.compile(rsregex).match(genompos).groups()
        chr = p[1]
        pos = p[4]
        ref_seq = p[3]
        ref = p[5]
        alt = p[6]
        return chr, ref_seq, pos, ref, alt
    else:
        rsregex = "(CHR|chr)([0-9|X|Y|MT]+):(g.|c.)?([0-9]+)([A|C|G|T|-]+)>([A|C|G|T|-]+)"
        if re.compile(rsregex).match(genompos):
            p = re.compile(rsregex).match(genompos).groups()
            chr = p[1]
            pos = p[3]
            ref_seq = p[2]
            ref = p[4]
            alt = p[5]
            return chr, ref_seq, pos, ref, alt
        else:
            print("no match for genomic location: ",genompos)
    print("Error: Could not parse ",genompos)
    return None, None, None, None, None


def generate_variant_data_section(variant_data):
    """
    Generates the variant data section that contains the genomic location data  for a biomarker data frame

    :param variant_data:
    :return:
    """

    for var in variant_data:
        if "variant_data" not in variant_data[var]:
            variant_data[var]["variant_data"] = {}
            try:
                chrom, ref_seq, pos, ref, alt = parse_genome_position(var)
                variant_data[var]["variant_data"]["CHROM"] = chrom
                variant_data[var]["variant_data"]["POS"] = pos
                variant_data[var]["variant_data"]["REF"] = ref
                variant_data[var]["variant_data"]["ALT"] = alt
                variant_data[var]["variant_data"]["info_features"] = ""
            except:
                print("Could not parse genomic location: ",var)
                variant_data[var]["variant_data"]["CHROM"] = ""
                variant_data[var]["variant_data"]["POS"] = ""
                variant_data[var]["variant_data"]["REF"] = ""
                variant_data[var]["variant_data"]["ALT"] = ""
                variant_data[var]["variant_data"]["info_features"] = ""

    return variant_data


def get_clinical_evidence_data(variant_data, data_section="merged_evidence_data") -> pd.DataFrame:
    """

    :param variant_data:
    :return:
    """

    chrom = []
    pos_hg19 = []
    pos_hg38 = []
    ref = []
    alt = []
    drugs = []
    drug_classes = []
    evidence_levels = []
    response_types = []
    associated_biomarkers = []
    match_types = []
    cancer_types = []
    citation_ids = []
    sources = []

    for qid in variant_data.keys():
        if config.onkopus_aggregator_srv_prefix in variant_data[qid]:
            for match_type in config.match_types:
                if match_type in variant_data[qid][config.onkopus_aggregator_srv_prefix][data_section]:
                    for result in variant_data[qid][config.onkopus_aggregator_srv_prefix][data_section][match_type]:

                        include_result = True

                        if "evidence_level_onkopus"in result:
                            evidence_level = result["evidence_level_onkopus"]
                        else:
                            evidence_level = ""

                        if include_result:
                            chrom.append(variant_data[qid]["variant_data"]["CHROM"])
                            pos_hg19.append(variant_data[qid]["variant_data"]["POS_hg19"])
                            pos_hg38.append(variant_data[qid]["variant_data"]["POS_hg38"])
                            ref.append(variant_data[qid]["variant_data"]["REF"])
                            alt.append(variant_data[qid]["variant_data"]["ALT"])

                            drugs.append(result["drugs"])
                            drug_classes.append(result["drugs"])
                            evidence_levels.append(evidence_level)
                            response_types.append(result["response"])
                            associated_biomarkers.append(result["biomarker"])
                            match_types.append(match_type)
                            cancer_types.append(result["disease"])
                            citation_ids.append(result["citation_id"])
                            sources.append(result["source"])

    treatment_data = {
        'CHROM': chrom,
        'POS_HG19': pos_hg19,
        'POS_HG38': pos_hg38,
        'REF': ref,
        'ALT': alt,
        'Drugs': drugs,
        'Drug Class': drug_classes,
        'Evidence Level': evidence_levels,
        'Response Type': response_types,
        'Associated Biomarker': associated_biomarkers,
        'Match Type': match_types,
        'Tumor Type': cancer_types,
        'Citation ID': citation_ids,
        'Source': sources
        }

    df = pd.DataFrame(data=treatment_data)
    return df