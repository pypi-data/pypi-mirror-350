import traceback, csv, copy
import pandas as pd
import vcfcli.conf.read_config as config
import vcfcli


def to_single_tsv_line(self, qid, json_obj, mapping=None, labels=None, features=None, sep=','):
    """

    :param qid:
    :param json_obj:
    :param mapping:
    :return:
    """

    # get mappings
    # line = qid + ","#
    line = []
    cols = {}

    for module in mapping:
        if type(mapping[module]) is list:
            keys = mapping[module]
            for key in keys:
                if module in json_obj:
                    if key in json_obj[module]:
                        val = str(json_obj[module][key])
                        val = val.replace(sep, " ")
                        # line.append(val)
                        cols[module + "_" + key] = val
                    else:
                        # print("no key: ",module,",",key)
                        # line.append("")
                        pass
                else:
                    # print("no module: ",module,",",key)
                    # line.append("")
                    pass
        else:
            line.append(str(json_obj[module]))
    # line = line.rstrip(',')
    # line = sort_features(line, cols)
    for feature in features:
        if feature in cols:
            line.append(cols[feature])
        else:
            # print("feature not found ",feature,",",cols.keys())
            line.append("")

    return line


def write_csv_to_file(outfile_src, json_obj, mapping=None,labels=None,sort_features=True,
                      sorted_features=None,sep=','):
    """

    :param outfile_src:
    :param json_obj:
    :param mapping:
    :param labels:
    :param sort_features:
    :param sorted_features:
    :param sep:
    :return:
    """
    if mapping is None:
        mapping = config.tsv_mappings

    if labels is None:
        labels = config.tsv_labels

    if sorted_features is None:
        sorted_features = config.tsv_feature_ranking

    # outfile = open(outfile_src, 'w')
    print("Write data in outfile: ", outfile_src)
    with open(outfile_src, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=sep,
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # print(self.get_tsv_labels(json_obj,mapping=mapping,labels=labels),file=outfile)
        if sort_features is False:
            row = get_tsv_labels(mapping=mapping, labels=labels)
            sorted_features = row
        else:
            row = sorted_features
            newrow = []
            for label in row:
                if label in labels:
                    col = labels[label]
                    newrow.append(col)
            row = newrow
        csvwriter.writerow(row)

        for var in json_obj.data.keys():
            json_obj.row = json_obj.row + 1
            # print(self.to_single_tsv_line(var, json_obj.data[var],mapping=mapping,labels=labels),
            #      file=outfile)
            row = to_single_tsv_line(var, json_obj.data[var], mapping=mapping, labels=labels,
                                          features=sorted_features)
            csvwriter.writerow(row)


def to_single_tsv_line(qid,json_obj,mapping=None, labels=None, features=None,sep=','):
        """

        :param qid:
        :param json_obj:
        :param mapping:
        :return:
        """

        # get mappings
        #line = qid + ","#
        line = []
        cols = {}

        for module in mapping:
                if type(mapping[module]) is list:
                    keys = mapping[module]
                    for key in keys:
                        if module in json_obj:
                            if key in json_obj[module]:
                                val = str(json_obj[module][key])
                                val = val.replace(sep," ")
                                #line.append(val)
                                cols[module + "_" + key] = val
                            else:
                                #print("no key: ",module,",",key)
                                #line.append("")
                                pass
                        else:
                            #print("no module: ",module,",",key)
                            #line.append("")
                            pass
                else:
                    line.append(str(json_obj[module]))
        #line = line.rstrip(',')
        #line = sort_features(line, cols)
        for feature in features:
            if feature in cols:
                line.append(cols[feature])
            else:
                #print("feature not found ",feature,",",cols.keys())
                line.append("")

        return line


def get_tsv_labels(mapping=None, labels=None):
    """
    Returns an array of feature labels

    :param json_obj:
    :param mapping:
    :return:
    """
    # line = "qid,"
    line = []

    if mapping is None:
        mapping = config.tsv_mappings

    # get mappings
    for module in mapping:
        if type(mapping[module]) is list:
            keys = mapping[module]
            for key in keys:
                label = module + "_" + key
                if label in labels:
                    col = labels[label]
                else:
                    col = label
                line.append(col)
        else:
            line.append(module)

    # line = line.rstrip(',')
    # sort_features(line,line)

    return line


def parse_mapping(mapping):
    pass

def parse_line():
    pass

def parse_dataframe_biomarkers(df: pd.DataFrame,
                               json_obj,
                               genome_version="hg38",
                               dragen_file:bool = False,
                               mapping=None,
                               level="gene"):
    """
    Recognizes the biomarker data format of a dataframe.
    Returns the parsed variant data

    :param variant_data:
    :param json_obj:
    :param df:
    :param dragen_file:
    :param mapping:
    :return:
    """
    variant_data = {}
    columns = df.columns
    columns = [x.lower() for x in columns]
    df.columns = columns
    print("columns: ", columns)
    data_type = "vcf"

    chrom_pos = 0
    pos_pos = 1
    ref_pos = 2
    alt_pos = 3

    chrom_defined = False
    if mapping is not None:
        keys = copy.deepcopy(list(mapping.keys()))
        for key in keys:
            if isinstance(mapping[key], str):
                val = str(mapping[key]).lower()
            else:
                val = copy.deepcopy(mapping[key])

            mapping[key] = val
            mapping[key.lower()] = mapping.pop(key)

        if "<def>" in str(mapping["chrom"]):
            mapping["chrom"] = mapping["chrom"].replace("<def>","")
            chrom_pos = mapping["chrom"]
            chrom_defined = True
        else:
            if isinstance(mapping["chrom"], int):
                chrom_pos = mapping["chrom"]
            else:
                print(mapping)
                chrom_pos = columns.index(mapping["chrom"])



        if "aa_exchange" in mapping.keys():
            if isinstance(mapping["aa_exchange"], int):
                ref_pos = mapping["aa_exchange"]
            else:
                ref_pos = columns.index(mapping["aa_exchange"])
            alt_pos = None
            data_type = "ref_aa"
            if isinstance(mapping["pos"], int):
                pos_pos = mapping["pos"]
            else:
                pos_pos = columns.index(mapping["pos"])
        elif "g_description" in mapping.keys():
            if isinstance(mapping["g_description"], int):
                pos_pos = mapping["g_description"]
            else:
                pos_pos = columns.index(mapping["g_description"])
            alt_pos = None
            ref_pos = None
            data_type = "g_desc"
        else:
            if isinstance(mapping["ref"], int):
                ref_pos = mapping["ref"]
            else:
                ref_pos = columns.index(mapping["ref"])
            if isinstance(mapping["alt"], int):
                alt_pos = mapping["alt"]
            else:
                alt_pos = columns.index(mapping["alt"])
            if isinstance(mapping["pos"], int):
                pos_pos = mapping["pos"]
            else:
                pos_pos = columns.index(mapping["pos"])

    else:
        if ("chrom" in columns) and ("pos" in columns) and ("ref" in columns) and ("alt" in columns):
            chrom_pos = columns.index("chrom")
            pos_pos = columns.index("pos")
            ref_pos = columns.index("ref")
            alt_pos = columns.index("alt")
        elif ("chrom" in columns) and ("pos_hg38" in columns) and ("ref" in columns) and ("alt" in columns) and \
                (genome_version=="hg38"):
            chrom_pos = columns.index("chrom")
            pos_pos = columns.index("pos_hg38")
            ref_pos = columns.index("ref")
            alt_pos = columns.index("alt")
        elif ("chrom" in columns) and ("pos_hg19" in columns) and ("ref" in columns) and ("alt" in columns) and \
                (genome_version=="hg19"):
            chrom_pos = columns.index("chrom")
            pos_pos = columns.index("pos_hg19")
            ref_pos = columns.index("ref")
            alt_pos = columns.index("alt")
        elif ("qid" in columns):
            qid_pos = columns.index("qid")
            data_type="qid"
        elif ('gene' in columns) and ('variant' in columns):
            data_type="protein"
        elif ('gene' in columns) and ('aa_exchange' in columns):
            data_type='protein'
        else:
            print("Error: Could not find column labels for identifying SNPs (CHROM,POS,REF,ALT) and "
                  "no column mapping is specified. Please add column labels to your variant file or "
                  "define a mapping that defined the indices of the associated columns, e.g. "
                  "        mapping = {"
                  "  'chrom': 1,"
                  "  'pos': 2,"
                  "  'ref': 4,"
                  "  'alt': 5"
                  "}"
                  )
            return json_obj

    for i in range(0, df.shape[0]):
        key = ''

        if dragen_file:
            chr = df.iloc[i, :].loc["chromosome"]
            pos = df.iloc[i, :].loc["region"]
            ref = df.iloc[i, :].loc["reference"]
            alt = df.iloc[i, :].loc["allele"]
            key = 'chr' + str(chr) + ':' + str(pos) + str(ref) + '>' + str(alt)
            variant_data[key] = {}
            variant_data[key][config.variant_data_key] = {}
            if "chr" in chr:
                chr = chr.replace("chr","")
            variant_data[key][config.variant_data_key]["CHROM"] = chr
            variant_data[key][config.variant_data_key]["POS"] = pos
            variant_data[key][config.variant_data_key]["POS_"+genome_version] = pos
            variant_data[key][config.variant_data_key]["REF"] = ref
            variant_data[key][config.variant_data_key]["ALT"] = alt
            variant_data[key]["additional_columns"] = {}
            for j in range(0, (df.shape[1])):
                variant_data[key]["additional_columns"][columns[j]] = df.iloc[i, j]
        elif data_type=="qid":
            # id_index = columns.index('QID')
            #key = df.iloc[i, :].loc["qid"]
            key = df.iloc[i, qid_pos]
            chr, ref_seq, pos, ref, alt = vcfcli.parse_genome_position(key)
            data = {}
            data[config.variant_data_key] = {}
            if "chr" in chr:
                chr = chr.replace("chr","")
            data[config.variant_data_key]["CHROM"] = chr
            data[config.variant_data_key]["POS"] = pos
            data[config.variant_data_key]["POS_" + genome_version] = pos
            data[config.variant_data_key]["REF"] = ref
            data[config.variant_data_key]["ALT"] = alt
            variant_data[key] = data
            json_obj.data_type = "g"
        elif data_type=="vcf":
            if chrom_defined is not False:
                chr = chrom_pos
            else:
                chr = df.iloc[i, chrom_pos]#.loc["chrom"]

            pos = df.iloc[i, pos_pos]#.loc["pos"]
            ref = df.iloc[i, ref_pos]#.loc["ref"]
            alt = df.iloc[i, alt_pos]#.loc["alt"]
            chrom_str = str(chr)
            if "chr" not in chrom_str:
                chrom_str = "chr" + chrom_str
            key = chrom_str + ':' + str(pos) + str(ref) + '>' + str(alt)
            data = {}
            data[config.variant_data_key] = {}
            if "chr" in chrom_str:
                chr = chrom_str.replace("chr","")
            data[config.variant_data_key]["CHROM"] = chrom_str
            data[config.variant_data_key]["POS"] = pos
            data[config.variant_data_key]["POS_" + genome_version] = pos
            data[config.variant_data_key]["REF"] = ref
            data[config.variant_data_key]["ALT"] = alt
            variant_data[key] = data
            json_obj.data_type = "g"
        elif ('gene' in columns) and ('variant' in columns):
            #print("read data by gene name and amino acid exchange")
            genome_version = "hg38"
            data = {}
            # data[config.variant_data_key] = {}
            gene = df.iloc[i, :].loc["gene"]
            variant = df.iloc[i, :].loc["variant"]
            data[gene + ":" + variant] = {}
            #data[gene + ":" + variant][
            #    config.uta_adapter_genetogenomic_srv_prefix] = {}
            #data[gene + ":" + variant][
            #    config.uta_adapter_genetogenomic_srv_prefix][config.uta_genomic_keys[0]] = gene
            #data[gene + ":" + variant][
            #    config.uta_adapter_genetogenomic_srv_prefix][config.uta_genomic_keys[1]] = variant

            #client = CCSGeneToGenomicClient(genome_version)
            #data = client.process_data(data, input_format='tsv')

            genomic_locations = list(data.keys())
            for genomepos in genomic_locations:
                variant_data[genomepos] = data[genomepos]
                variant_data[genomepos]["level"] = "protein"

                # Add gene and variant data
                variant_data[genomepos]["UTA_Adapter"] = {}
                variant_data[genomepos]["UTA_Adapter"]["gene_name"] = gene
                variant_data[genomepos]["UTA_Adapter"]["variant_exchange"] = variant
            json_obj.data_type = "p"
        elif ('gene' in columns) and ('aa_exchange' in columns):
            #print("read data by gene name and amino acid exchange")
            genome_version = "hg38"
            data = {}
            # data[config.variant_data_key] = {}
            gene = df.iloc[i, :].loc["gene"]
            variant = df.iloc[i, :].loc["aa_exchange"]
            data[gene + ":" + variant] = {}

            genomic_locations = list(data.keys())
            for genomepos in genomic_locations:
                variant_data[genomepos] = data[genomepos]
                variant_data[genomepos]["level"] = "protein"

                # Add gene and variant data
                variant_data[genomepos]["UTA_Adapter"] = {}
                variant_data[genomepos]["UTA_Adapter"]["gene_name"] = gene
                variant_data[genomepos]["UTA_Adapter"]["variant_exchange"] = variant
            json_obj.data_type = "p"
        elif data_type == "ref_aa":
            try:
                if chrom_defined is not False:
                    chr = chrom_pos
                else:
                    chr = df.iloc[i, chrom_pos]  # .loc["chrom"]
                pos = df.iloc[i, pos_pos]  # .loc["pos"]

                # Split reference and alternate allele
                refalt = df.iloc[i,ref_pos]
                if "del" in refalt:
                    continue
                if "ins" in refalt:
                    continue
                else:
                    elements = refalt.split(">")
                    if len(elements) > 1:
                        ref = elements[0]
                        alt = elements[1]
                    else:
                        print("Could not parse ",refalt)
                        continue
                key = 'chr' + str(chr) + ':' + str(pos) + str(ref) + '>' + str(alt)
                data = {}
                data[config.variant_data_key] = {}
                if "chr" in chr:
                    chr = chr.replace("chr", "")
                data[config.variant_data_key]["CHROM"] = chr
                data[config.variant_data_key]["POS"] = pos
                data[config.variant_data_key]["POS_" + genome_version] = pos
                data[config.variant_data_key]["REF"] = ref
                data[config.variant_data_key]["ALT"] = alt
                variant_data[key] = data
                json_obj.data_type = "g"
            except:
                print(traceback.format_exc())
        elif data_type == "g_desc":
            try:
                if chrom_defined is not False:
                    chr = chrom_pos
                else:
                    chr = df.iloc[i, chrom_pos]  # .loc["chrom"]
                pos = df.iloc[i, pos_pos]  # .loc["pos"]

                # Split reference and alternate allele
                gdesc = df.iloc[i,pos_pos]
                key = 'chr' + str(chr) + ':' + str(gdesc)
                chrom, refseq, pos, ref, alt = vcfcli.parse_genome_position(key)
                data = {}
                data[config.variant_data_key] = {}
                if "chr" in chr:
                    chr = chr.replace("chr", "")
                data[config.variant_data_key]["CHROM"] = chr
                data[config.variant_data_key]["POS"] = pos
                data[config.variant_data_key]["POS_" + genome_version] = pos
                data[config.variant_data_key]["REF"] = ref
                data[config.variant_data_key]["ALT"] = alt
                variant_data[key] = data
                json_obj.data_type = "g"
            except:
                print(traceback.format_exc())
        else:
            print("unidentifiable columns: ", columns)
            continue

        # Read existing feature data
        for j, feature in enumerate(columns):
            if key != '':
                if feature not in variant_data[key]:
                    variant_data[key][feature] = {}
                try:
                    #if feature in config.tsv_mappings.keys():
                    #    # if len(elements) > j:
                    #    #    if elements[j]:
                    #    # print("assign ",elements,", feature ",feature,",",i,": ",elements[i])
                    #    #variant_data[key][feature][config.tsv_mappings[feature]] = df.iloc[i, j]
                    #    pass
                    #else:
                    variant_data[key][feature] = df.iloc[i, j]
                except:
                    variant_data[key][feature] = ''
                    print("error adding feature (TSV)")
                    print(traceback.format_exc())

    json_obj.data = variant_data
    return json_obj


def write_csv_to_dataframe(outfile_src, json_obj, mapping=None,labels=None,sort_features=True,
                      sorted_features=None,sep=','):
    """

    :param outfile_src:
    :param json_obj:
    :param mapping:
    :param labels:
    :param sort_features:
    :param sorted_features:
    :param sep:
    :return:
    """
    if mapping is None:
        mapping = config.tsv_mappings

    if labels is None:
        labels = config.tsv_labels

    if sorted_features is None:
        sorted_features = config.tsv_feature_ranking

    # outfile = open(outfile_src, 'w')
    print("Write data in outfile: ", outfile_src)
    data={}
    # print(self.get_tsv_labels(json_obj,mapping=mapping,labels=labels),file=outfile)
    if sort_features is False:
        row = get_tsv_labels(mapping=mapping, labels=labels)
        sorted_features = row
    else:
        row = sorted_features
        newrow = []
        for label in row:
            if label in labels:
                col = labels[label]
                newrow.append(col)
        row = newrow
    columns = row
    for col in columns:
        data[col] = []

    for var in json_obj.data.keys():
        json_obj.row = json_obj.row + 1
        # print(self.to_single_tsv_line(var, json_obj.data[var],mapping=mapping,labels=labels),
        #      file=outfile)
        row = to_single_tsv_line(var, json_obj.data[var], mapping=mapping, labels=labels,
                                          features=sorted_features)
        #csvwriter.writerow(row)
        for i,col in enumerate(columns):
            data[col].append(row[i])

    df = pd.DataFrame(data=data)
    return df


def is_dragen_file(columns):
    """
    Detects whether an Excel file is in DRAGEN format

    :param columns:
    :return:
    """
    dragen_columns = ['Chromosome', 'Region', 'Type', 'Reference', 'Allele', 'Coverage', 'Frequency', 'Exact match', 'AF',
                          'EUR_AF 1000GENOMES-phase_3_ensembl_v91_o', 'AF_EXAC clinvar_20171029_o', 'CLNSIG clinvar_20171029_o',
                          'RS clinvar_20171029_o', 'Homo_sapiens_refseq_GRCh38_p9_o_Genes', 'Coding region change',
                          'Amino acid change', 'Splice effect', 'mRNA Accession', 'Exon Number', 'dbSNP']
    if len(columns) > 6:
        #print([x for x in columns[0:5] if x in dragen_columns[0:5]])
        if len([x for x in columns[0:5] if x in dragen_columns[0:5]]) == 5:
            print("DRAGEN file detected")
            return True
    print("Could not detect DRAGEN file ",columns)
    return False

