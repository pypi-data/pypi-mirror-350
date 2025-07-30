
def transform_hg19_in_hg38_bframe(bframe, genome_version):
    """
    Converts a biomarker frame from hg19/GRCh37 IDs in hg38/GRCh38

    :param bframe:
    :return:
    """
    t_possible = False
    bframe_hg38 = {}

    if genome_version == "hg19":
        for var in bframe.keys():
            if ("POS_hg38" in bframe[var]["variant_data"]) and \
                ("REF" in bframe[var]["variant_data"] and \
                 ("ALT" in bframe[var]["variant_data"])):
                hg38_id = "chr" + str(bframe[var]["variant_data"]["CHROM"]) + ":" + str(bframe[var]["variant_data"]["POS_hg38"]) \
                                  + str(bframe[var]["variant_data"]["REF"]) + ">" + str(bframe[var]["variant_data"]["ALT"])
                bframe_hg38[hg38_id] = bframe[var]

        return bframe_hg38
    else:
        return bframe


def add_hg38_positions(bframe):
    """
    Generates the hg38/GRCh38 position as the default variant position

    :param bframe:
    :return:
    """
    for var in bframe.keys():
        if "POS_hg38" in bframe[var]["variant_data"]:
            bframe[var]["variant_data"]["POS_hg38"] = bframe[var]["variant_data"]["POS"]
    return bframe
