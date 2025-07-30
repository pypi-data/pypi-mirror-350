import datetime, traceback, copy
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config
import vcfcli.tools


class OncoKBClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.url_pattern = config.oncokb_src
        self.srv_prefix = config.oncokb_srv_prefix
        self.extract_keys = config.oncokb_keys
        self.info_lines = config.oncokb_info_lines
        self.error_logfile = error_logfile

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def get_headers(self, key):
        """
        Returns the HTTP request header for the OncoKB module

        :return:
        """
        headers = {}
        if key is not None:
            headers["oncokb-key"] = key

        return headers

    def process_data(self, vcf_lines, input_format='vcf', key=None):
        """
        Request to OncoKB module

        :param vcf_lines:
        :param input_format:
        :param key
        :return:
        """
        qid_list = copy.deepcopy(list(vcf_lines.keys()))

        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            genompos_str = ','.join(vcfcli.tools.filter_alternate_alleles(qids_partial))
            q = ""

            try:
                    q = 'genompos=' + genompos_str
                    json_body = req.get_connection(q, self.url_pattern, self.genome_version, headers=self.get_headers(key))

                    for genompos in json_body.keys():
                            json_obj = json_body[genompos]
                            qid = genompos

                            for k in self.extract_keys:
                                if k in json_obj:
                                    pass
                                    #annotations.append('{}_{}={}'.format(self.srv_prefix, k, json_body[i][k]))
                            try:
                                #json_obj.pop('q_id')
                                vcf_lines[qid][self.srv_prefix] = json_obj
                            except:
                                if self.error_logfile is not None:
                                    cur_dt = datetime.datetime.now()
                                    date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                                    print(cur_dt, ": error processing variant response: ", qid, ';', traceback.format_exc(), file=self.error_logfile+str(date_time)+'.log')
                                else:
                                    print(traceback.format_exc())
            except:
                    if self.error_logfile is not None:
                        print("error processing request: ", vcf_lines, file=self.error_logfile+str(date_time)+'.log')
                    else:
                        print(": error processing variant response: ;", traceback.format_exc())
            for i in range(0, max_length):
                del qid_list[0]
            if len(qid_list) == 0:
                break
        return vcf_lines
