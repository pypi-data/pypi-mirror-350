import os, gzip
import pandas as pd
import vcfcli.clients.reader as reader
import vcfcli
#from vcfcli.tools.parse_dataframes import parse_dataframe_biomarkers, is_dragen_file


class CSVReader(reader.Reader):

    def read_file(self, infile, sep=',',
                  genome_version='hg38',
                  batch_size=100,
                  columns=None,
                  mapping=None,
                  header=True
                  ) -> vcfcli.BiomarkerFrame:
        """
        Loads a tab or comma-separated file in a variant data object

        :param batch_size:
        :param sep:
        :param genome_version:
        :param infile:
        :return:
        """
        if genome_version is None:
            genome_version = self.genome_version

        #if isinstance(infile, str):
        #    file_name, file_extension = os.path.splitext(infile)
        #    input_format_recognized = file_extension.lstrip(".")
        #    if input_format_recognized == "gz":
        #        infile = gzip.open(infile, 'rt')
        #    else:
        #        infile = open(infile, 'r')

        if header is True:
            header_val = 0
        else:
            header_val = 1
        df = pd.read_csv(infile,sep=",",header=header_val)

        json_obj = vcfcli.BiomarkerFrame()
        row = 0
        dragen_file = vcfcli.is_dragen_file(df.columns)
        if dragen_file:
            json_obj.data_type = "g"

        json_obj = vcfcli.parse_dataframe_biomarkers(df,json_obj, dragen_file=dragen_file,mapping=mapping,
                                                     genome_version=genome_version)
        # print("loaded tsv: ", variant_data)

        return json_obj

    def read_file_chunk(self, infile, json_obj: vcfcli.BiomarkerFrame,genome_version="hg38") -> vcfcli.BiomarkerFrame:
        """
        Reads a defined number of lines from a file object, adds them to the given biomarker set and returns the extended biomarker list

        :param genome_version:
        :param infile:
        :type infile:
        :param json_obj:
        :type json_obj: BiomarkerSet
        :return: json_obj
        """

        json_obj_new = self.read_file(infile,genome_version=genome_version)
        json_obj.data = json_obj_new.data

        return json_obj
