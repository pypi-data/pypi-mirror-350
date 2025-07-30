import copy, traceback, os, gzip
import pandas as pd
from vcfcli.tools import parse_genome_position
from vcfcli.conf import read_config as config
import vcfcli.clients.reader as reader
import vcfcli
from vcfcli.tools.parse_dataframes import parse_dataframe_biomarkers, is_dragen_file


class TSVReader(reader.Reader):

    def __init__(self, genome_version=None):
        super(TSVReader, self).__init__(genome_version=genome_version)

    def read_file(self, infile, columns=None, genome_version=None,sep=None, mapping=None) -> vcfcli.BiomarkerFrame:
        if isinstance(infile,str):
            file_name, file_extension = os.path.splitext(infile)
            input_format_recognized = file_extension.lstrip(".")
            if input_format_recognized == "gz":
                infile = gzip.open(infile, 'rt')
            else:
                infile = open(infile, 'r')

        biomarker_data = self.load_table_file(infile, columns=columns,mapping=mapping)
        #for i, key in enumerate(biomarker_data.keys()):
        #    self.variants[i] = key

        infile.close()
        return biomarker_data

    def load_table_file(self, infile, sep='\t', genome_version=None, columns=None,mapping=None):
        """
        Loads a tab or comma-separated file in a variant data object

        :param infile:
        :return:
        """
        if genome_version is None:
            genome_version = self.genome_version

        json_obj = vcfcli.BiomarkerFrame()
        json_obj.data = {}
        json_obj.genome_version = genome_version

        variant_data = {}
        row = 0

        df = pd.read_csv(infile, sep="\t")
        print(df.shape)
        dragen_file = is_dragen_file(df.columns)
        if dragen_file:
            json_obj.data_type = "g"

        json_obj = parse_dataframe_biomarkers(df,json_obj,dragen_file=dragen_file,mapping=mapping)
        return json_obj
