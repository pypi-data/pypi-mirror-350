from adagenes.clients import client
import adagenes


def recognize_biomarker_types(bframe: adagenes.BiomarkerFrame) -> adagenes.BiomarkerFrame:
    """
    Recognizes biomarker type according to the biomarker identifier

    :param bframe:
    :return:
    """
    client = TypeRecognitionClient()
    return client.process_data(bframe)


class TypeRecognitionClient(client.Client):
    """
    Variant type recognition clients. Identifies the variant type from the received variant data (SNV, insertions and
    deletions, copy number variation, gene fusion) and writes the variant type in the feature 'variant_type' of the variant data section
    """

    def __init__(self, error_logfile=None):
        pass

    def process_data(self, biomarker_data):
        is_bframe = False
        if isinstance(biomarker_data, adagenes.BiomarkerFrame):
            data = biomarker_data.data
            is_bframe = True
            bframe = biomarker_data
        else:
            data = biomarker_data
            bframe = adagenes.BiomarkerFrame
            bframe.data = data

        #biomarker_data = adagenes.tools.biomarker_types.get_biomarker_type(biomarker_data)
        bframe = adagenes.tools.identify_biomarkers(bframe)


        if is_bframe:
            return bframe

        return bframe.data
