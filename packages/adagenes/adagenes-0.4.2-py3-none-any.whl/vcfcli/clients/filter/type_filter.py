from vcfcli.clients import client
import vcfcli
import vcfcli.conf.read_config as conf_reader


class TypeFilterClient(client.Client):
    """
    Mutation type filter that selects mutations of a specific mutation type

    """

    def process_data(self, biomarker_data, get_types=None):

        biomarker_data_new = {}

        for var in biomarker_data:
            if get_types is not None:
                if conf_reader.variant_data_key in biomarker_data[var]:
                    if "type" in biomarker_data[var][conf_reader.variant_data_key]:
                        if biomarker_data[var][conf_reader.variant_data_key]["type"].lower() in get_types:
                            biomarker_data_new[var] = biomarker_data[var]

        return biomarker_data_new
