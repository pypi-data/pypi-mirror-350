import traceback
import pandas as pd
import vcfcli.clients.reader as reader
import vcfcli.conf.read_config as config
from vcfcli.tools import parse_genome_position
import vcfcli


class PandasReader(reader.Reader):

    def get_data_from_df(self, df, sep=',', genome_version='hg19', batch_size=100):

        """
                Loads a tab or comma-separated file in a variant data object

                :param infile_src:
                :param infile:
                :return:
        """
        if genome_version is None:
            genome_version = self.genome_version

        json_obj = vcfcli.BiomarkerFrame()
        variant_data = {}
        row = 0
        columns = df.columns

        for i in range(0, df.shape[0]):
            qid = df.at[i,"qid"]

            variant_data[qid] = {}
            for col in df.columns:
                vals = col.split("_")
                if len(vals) > 1:
                    variant_data[qid][vals[0]] = { vals[1]: df.at[i,col] }
                else:
                    variant_data[qid][col] = df.at[i,col]

        # print("loaded tsv: ", variant_data)
        json_obj.data = variant_data

        return json_obj