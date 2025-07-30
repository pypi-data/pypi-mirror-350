from vcfcli.clients import client
import vcfcli.conf.read_config as conf_reader


class ChromosomeFilter(client.Client):

    def process_data(self, biomarker_data, filter_chroms=None):

        biomarker_data_new = {}

        for var in biomarker_data:
            if filter_chroms is not None:
                if conf_reader.variant_data_key in biomarker_data[var]:
                    if "type" in biomarker_data[var][conf_reader.variant_data_key]:
                        if biomarker_data[var][conf_reader.variant_data_key]["CHROM"].lower() not in filter_chroms:
                            biomarker_data_new[var] = biomarker_data[var]

        return biomarker_data_new
