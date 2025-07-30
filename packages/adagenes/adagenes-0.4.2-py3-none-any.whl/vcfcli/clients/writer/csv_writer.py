import vcfcli.conf.read_config as conf_reader
import vcfcli.clients.writer as writer
import vcfcli
import traceback, csv, copy
import pandas as pd


def avf_to_csv(infile, outfile,mapping=None,labels=None,ranked_labels=None):
    bframe = vcfcli.read_file(infile, input_format="avf")
    vcfcli.write_file(outfile, bframe, file_type="csv",mapping=mapping,labels=labels,ranked_labels=ranked_labels )

def get_tsv_labels(mapping=None, labels=None, ranked_labels=None):
    """

    :param json_obj:
    :param mapping:
    :return:
    """
    # line = "qid,"
    line = []

    for feature in ranked_labels:
        line.append(feature)
    # get mappings
    #if (mapping is not None) and (labels is not None) and (ranked_labels is not None):
    #    for module in mapping:
    #        if type(mapping[module]) is list:
    #            keys = mapping[module]
    #            for key in keys:
    #                label = module + "_" + key
    #                if label in labels:
    #                    col = labels[label]
    #                else:
    #                    col = label
    #                line.append(col)
    #        else:
    #            line.append(module)
    return line


def get_sorted_values(cols,labels=None,ranked_labels=None):
    """

    :param cols:
    :param labels:
    :param ranked_labels:
    :return:
    """
    line = []
    if (labels is not None) and (ranked_labels is not None):
        for feature in ranked_labels:
            if feature in cols:
                line.append(cols[feature])
            elif feature in labels:
                mapped_feature = labels[feature]
                if mapped_feature in cols:
                    line.append(cols[mapped_feature])
                else:
                    line.append("")
            else:
                line.append("")
    else:
        for feature in cols.keys():
            line.append(cols[feature])
    return line


def get_row_values(json_obj,mapping=None,sep=","):
    """

    :param json_obj:
    :param mapping:
    :param labels:
    :param features:
    :param sep:
    :return:
    """
    cols = {}

    for module in mapping:
        if module in json_obj:
            if type(mapping[module]) is list:
                keys = mapping[module]
                for key in keys:
                    if module in json_obj:
                        if isinstance(json_obj[module], dict):
                            try:
                                if key in json_obj[module].keys():
                                    val = str(json_obj[module][key])
                                    val = val.replace(sep, " ")
                                    cols[module + "_" + key] = val
                                else:
                                    pass
                            except:
                                print(key)
                                print(module)
                                print(json_obj)
                                print(traceback.format_exc())
                        else:
                            pass
                    else:
                        pass
            elif isinstance(mapping[module], str):
                cols[module] = json_obj[module][mapping[module]]
            elif isinstance(mapping[module], dict):
                for sub_feature in mapping[module]:
                    if type(mapping[module][sub_feature]) is list:
                        keys = mapping[module][sub_feature]
                        for key in keys:
                            if module in json_obj:
                                if sub_feature in json_obj[module]:
                                    if key in json_obj[module][sub_feature]:
                                        val = str(json_obj[module][sub_feature][key])
                                        val = val.replace(sep, " ")
                                        cols[module + "_" + sub_feature + "_" + key] = val
                                    else:
                                        pass
                            else:
                                pass
                    elif isinstance(mapping[module], str):
                        cols[module] = json_obj[module]

    return cols


def sort_features(line, keys):
    new_line = []
    for key in conf_reader.tsv_feature_ranking:
        if key in keys:
            index = keys.index(key)
            new_line.append(line[index])
    return new_line


class CSVWriter(writer.Writer):

    def write_chunk_to_file(self, outfile, json_obj, variants_written=False, save_headers=False):
        """

        :param outfile:
        :param json_obj:
        :param variants_written:
        :param save_headers:
        :return:
        """
        self.write_to_file(outfile,json_obj)

    def write_to_file(self, outfile,
                      json_obj,
                      genome_version="hg38",
                      mapping=None,
                      labels=None,
                      ranked_labels=None,
                      sep=','):
        """
        Write a biomarker frame to an output file in CSV format

        :param outfile:
        :param json_obj:
        :param mapping:
        :param labels: Dictionary mapping feature identifiers to column labels to be exported
        :param sorted_features: Sorted list of features to export
        :return:
        """
        #print("Write data in outfile: ", outfile)

        close_file = False
        if isinstance(outfile, str):
            outfile = open(outfile, 'w', newline='')
            close_file = True

        if (mapping is not None) and (ranked_labels is not None):
            csvwriter = csv.writer(outfile, delimiter=sep,
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

            #row = ranked_labels
            #newrow=[]
            #for label in row:
            #    if label in labels:
            #        col = labels[label]
            #        newrow.append(col)
            #    else:
            #        newrow.append(label)
            #row = copy.deepcopy(newrow)
            row = ranked_labels
            csvwriter.writerow(row)

            for var in json_obj.data.keys():
                json_obj.row = json_obj.row + 1
                row = self.to_single_tsv_line(var, json_obj.data[var],mapping=mapping,labels=labels, ranked_labels=ranked_labels)
                #print(len(ranked_labels))
                #print(len(row))
                csvwriter.writerow(row)

            if close_file:
                outfile.close()
        else:
            df = None
            if isinstance(json_obj.data, dict):
                for var in json_obj.data.keys():
                    df_new = pd.json_normalize(json_obj.data[var])
                    if df is not None:
                        df = pd.concat([df,df_new],axis=0)
                    else:
                        df = copy.deepcopy(df_new)
                df["QID"] = list(json_obj.data.keys())
                df.set_index("QID")
                cols = df.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                df = df[cols]
                df.to_csv(outfile,index=False)


    def to_single_tsv_line(self, qid,json_obj,mapping=None, labels=None, ranked_labels=None,sep=',') -> list:
        """

        :param qid:
        :param json_obj:
        :param mapping:
        :return:
        """

        # get mappings
        cols = get_row_values(json_obj,mapping=mapping,sep=sep)
        #print("row values ",str(len(cols)))
        line = get_sorted_values(cols,labels=labels,ranked_labels=ranked_labels)
        #print("line ",str(len(line)))
        return line

    def get_feature_keys(self, variant_data, extract_keys):
        """

        :param variant_data:
        :param extract_keys:
        :return:
        """
        feature_labels = []
        #feature_labels.append("QID")

        tsv_features = conf_reader.tsv_columns
        if self.features is not None:
            tsv_features = self.features

        for col in tsv_features:
            # if col in variant_data.keys():
            #    for key in variant_data[var].keys():
            #        if (key not in feature_labels) and (key in config.tsv_columns):
            #                feature_labels.append(key)
            feature_labels.append(col)

        return ','.join(feature_labels)
