import datetime, traceback, copy

import vcfcli.tools
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config
from vcfcli.tools import generate_variant_dictionary


class DBSNPClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.url_pattern = config.dbsnp_src
        self.srv_prefix = config.dbsnp_srv_prefix
        self.extract_keys = config.dbsnp_keys
        self.info_lines = config.dbsnp_info_lines
        self.error_logfile = error_logfile

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines):
        """
        Annotates biomarker data with data from the dbSNP database

        :param vcf_lines:
        :return:
        """

        qid_list = copy.deepcopy(list(vcf_lines.keys()))
        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            q = ','.join(vcfcli.tools.filter_alternate_alleles(qids_partial))

            vcf_lines = vcfcli.processing.parse_http_responses.parse_module_response(q, vcf_lines, self.url_pattern,
                                                                                     self.genome_version,
                                                                                     self.srv_prefix)

            for i in range(0, max_length):
                del qid_list[0] #qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
