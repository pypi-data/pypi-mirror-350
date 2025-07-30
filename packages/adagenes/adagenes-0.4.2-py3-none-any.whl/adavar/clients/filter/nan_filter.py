from adagenes.clients import client
import adagenes.conf.read_config as conf_reader


class NaNFilter(client.Client):
    """
    Filters biomarker data according to a defined feature value, filters only exact matches
    """

    def process_data(self, biomarker_data, module=None, feature=None, inv=False):

        biomarker_data_new = {}

        for var in biomarker_data:
            if feature is not None:
                if module is not None:
                    if module in biomarker_data[var]:
                        if feature in biomarker_data[var][module]:
                            if not inv:
                                if biomarker_data[var][module][feature] == biomarker_data[var][module][feature]:
                                    biomarker_data_new[var] = biomarker_data[var]
                            else:
                                if biomarker_data[var][module][feature] != biomarker_data[var][module][feature]:
                                    biomarker_data_new[var] = biomarker_data[var]

        return biomarker_data_new
