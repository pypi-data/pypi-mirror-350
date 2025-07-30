import traceback
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config


class CCSGeneFusionClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version

    def process_data(self,
                     annotated_data):
        """
        Looks up genomic data of variant calls from gene names and variant exchange data

        Parameters
        ----------
        vcf
        variant_str

        Returns
        -------
        :param annotated_data:

        """

        # generate query string
        variant_str = ",".join(annotated_data.keys())

        try:
            json_body = req.get_connection(variant_str,
                  config.uta_adapter_genefusion_src,
                  self.genome_version)

            for key, value in json_body.items():
                if value != "Error":
                    qid = value['header']['qid']
                    annotated_data[qid][config.uta_adapter_genefusion_srv_prefix] = value['data']

                    annotated_data[qid][config.variant_data_key] = {}
                    annotated_data[qid][config.variant_data_key]["type"] = "fusion"
        except:
            print("error: genomic to gene")
            print(traceback.format_exc())

        return annotated_data