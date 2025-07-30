from adagenes.clients import client
import adagenes.conf.read_config as conf_reader


class ChromosomeFilter(client.Client):

    def process_data(self, biomarker_data, filter_chroms=None):

        biomarker_data_new = {}
        for var in biomarker_data:
            if filter_chroms is not None:
                if conf_reader.variant_data_key in biomarker_data[var]:
                    if biomarker_data[var][conf_reader.variant_data_key]["CHROM"].lower() in filter_chroms:
                        biomarker_data_new[var] = biomarker_data[var]

        return biomarker_data_new
