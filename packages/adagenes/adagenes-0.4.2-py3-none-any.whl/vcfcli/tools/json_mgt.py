import vcfcli
from vcfcli.conf import read_config as config
import traceback


def generate_variant_data_sections(json_obj):
    for qid in json_obj.keys():
        chrom, ref_seq, pos, ref, alt = vcfcli.tools.parse_genomic_data.parse_genome_position(qid)
        if "variant_data" not in json_obj[qid]:
            json_obj[qid]["variant_data"] = {}

        json_obj[qid]["variant_data"]["CHROM"] = chrom
        json_obj[qid]["variant_data"]["POS"] = pos
        json_obj[qid]["variant_data"]["REF"] = ref
        json_obj[qid]["variant_data"]["ALT"] = alt

    return json_obj


def generate_variant_data(json_obj, variant, chromosome, pos, fields, ref_base, alt_base):
    """
    Adds an additional biomarker to a biomarker frame

    :param json_obj:
    :param variant:
    :param chromosome:
    :param pos:
    :param fields:
    :param ref_base:
    :param alt_base:
    :return:
    """
    json_obj.data[variant] = {}

    json_obj.data[variant][config.variant_data_key] = {
        "CHROM": chromosome,
        "POS": pos,
        "ID": fields[2],
        "REF": ref_base,
        "ALT": alt_base,
        "QUAL": fields[5],
        "FILTER": fields[6],
        "INFO": fields[7],
        "OPTIONAL": fields[8:]
    }

    try:
        info_features = fields[7].split(";")
        if "info_features" not in json_obj.data[variant][config.variant_data_key]:
            json_obj.data[variant][config.variant_data_key]["info_features"] = {}
        for feature in info_features:
            if len(feature.split("=")) > 1:
                key, val = feature.split("=")
                json_obj.data[variant][config.variant_data_key]["info_features"][key] = val
    except:
        print("error extracting INFO features")
        print(traceback.format_exc())

    return json_obj


def generate_keys(json_obj, modules):
    """
    Generates keys with empty dictionaries for all Onkopus modules to avoid missing keys

    Parameters
    ----------
    json_obj

    Returns
    -------

    """
    for variant in json_obj.keys():
        if variant != 'vcf_header':
            for k in modules.keys():
                if k not in json_obj[variant]:
                    json_obj[variant][k] = {}
                if type(modules[k]) is dict:
                    for sk in modules[k].keys():
                        if sk not in json_obj[variant][k].keys():
                            if type(modules[k][sk]) is dict:
                                json_obj[variant][k][sk] = {}
                                for skk in modules[k][sk].keys():
                                    if skk not in json_obj[variant][k][sk].keys():
                                        if type(json_obj[variant][k][sk]) is dict:
                                            json_obj[variant][k][sk][skk] = {}
                                        else:
                                            json_obj[variant][k][sk][skk] = ""
                            else:
                                json_obj[variant][k][sk] = ""

    return json_obj
