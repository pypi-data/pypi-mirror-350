import traceback
import pandas as pd
import vcfcli.clients.reader as reader
import vcfcli.conf.read_config as config
from vcfcli.tools import parse_genome_position
import vcfcli
from vcfcli.tools.parse_dataframes import parse_dataframe_biomarkers, is_dragen_file


class XLSXReader(reader.Reader):

    def store_additional_columns_in_bframe(self, biomarker, lines,columns):
        """

        :param biomarker:
        :param lines:
        :param columns:
        :return:
        """
        biomarker["additional_columns"] = {}

        for i,feature in enumerate(columns):
            biomarker["additional_columns"][feature] = lines[i]

        return biomarker

    def read_file(self, infile_src, sep='\t', genome_version=None, batch_size=100, columns=None, mapping=None) \
            -> vcfcli.BiomarkerFrame:
        """
            Loads a tab or comma-separated file in a variant data object

            :param mapping:
            :param columns:
            :param batch_size:
            :param genome_version:
            :param sep:
            :param infile_src:
            :param infile:
            :return:
        """

        if genome_version is None:
            genome_version = self.genome_version

        df = pd.read_excel(infile_src)

        import vcfcli
        json_obj = vcfcli.BiomarkerFrame()
        row = 0
        columns = df.columns
        dragen_file = is_dragen_file(columns)
        json_obj = parse_dataframe_biomarkers(df, json_obj, dragen_file=dragen_file)

        #if dragen_file:
        #    import vcfcli.clients.transform.dragen_to_vcf_client
        #    dragen_client = vcfcli.clients.transform.dragen_to_vcf_client.DragenToVCFClient(self.genome_version)
        #    variant_data = dragen_client.process_data(variant_data.data)

        # print("loaded tsv: ", variant_data)
        #json_obj.data = variant_data

        return json_obj
