import datetime, requests, traceback, copy
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config
import vcfcli.tools

qid_key = "q_id"
error_logfile=None

class DBNSFPClient:
    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.dbnsfp_info_lines
        self.url_pattern = config.dbnsfp_src
        self.srv_prefix = config.dbnsfp_srv_prefix
        self.extract_keys = config.dbnsfp_keys

        self.qid_key = "q_id"
        self.error_logfile = error_logfile
        #if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
        #    self.qid_key = "q_id_hg19"

    def get_connection(self, variants, url_pattern, genome_version):
        url = url_pattern.format(genome_version) + variants
        print(url)
        r = requests.get(url)
        return r.json()

    def process_data(self, vcf_lines):
        #variant_dc = generate_variant_dictionary(vcf_lines)
        #variants = ','.join(variant_dc.values())

        #TODO Liftover hg19
        qid_list = copy.deepcopy(list(vcf_lines.keys()))
        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            variants = ','.join(vcfcli.tools.filter_alternate_alleles(qids_partial))

            try:
                json_body = req.get_connection(variants, self.url_pattern, self.genome_version)

                for qid, json_obj in json_body.items():
                    json_obj = json_obj["dbnsfp"]
                    if json_obj:

                        # calculate percentage
                        scores = ["SIFT_score","Polyphen2_HDIV_rankscore","Polyphen2_HVAR_rankscore",
                                  "fathmm-MKL_coding_rankscore",
                                  "fathmm-XF_coding_rankscore",
                                  "phastCons17way_primate_rankscore",
                                  "phyloP17way_primate_rankscore",
                                  "MetaLR_rankscore",
                                  "MPC_rankscore",
                                  "M-CAP_rankscore",
                                  "HUVEC_fitCons_rankscore",
                                  "Eigen-raw_coding_rankscore",
                                  "ClinPred_rankscore",
                                  "PROVEAN_converted_rankscore",
                                  "MutationTaster_converted_rankscore",
                                  "VEST4_rankscore"
                                  ]
                        for score in scores:
                            try:
                                if score in json_obj:
                                    score_percent = score + '_percent'
                                    json_obj[score_percent] = int(float(json_obj[score]) * 100)
                                else:
                                    print("Could not find score in response: ",score,": ",json_obj)
                            except:
                                print("error ",score,": ", traceback.format_exc())

                        # format multiple semicolon-separated scores
                        scores = [
                                    "MutationTaster_score",
                                    "MPC_score",
                                    "VEST4_score",
                                    "Polyphen2_HDIV_score",
                                    "Polyphen2_HVAR_score"
                                  ]
                        min_scores = ["PROVEAN_score"]

                        # format semicolon-separated scores, max values as pathogenic
                        for score in scores:
                            try:
                                if score in json_obj:
                                    score_percent = score + '_aggregated_value'
                                    values = json_obj[score].split(";")
                                    score_max = 0.0
                                    #score_max = ""
                                    for val in values:
                                        if (val != "") and (val != "."):
                                            if float(val) > score_max:
                                                score_max = float(val)
                                    json_obj[score_percent] = score_max
                                else:
                                    print("Could not find score in response: ",score,": ",json_obj)
                            except:
                                print("error ",score,": ", traceback.format_exc())

                        # format semicolon-separated scores, min values as pathogenic
                        for score in min_scores:
                            try:
                                if score in json_obj:
                                    score_percent = score + '_aggregated_value'
                                    values = json_obj[score].split(";")
                                    score_max = 0.0
                                    #score_max = ""
                                    for val in values:
                                        if (val != "") and (val != "."):
                                            if float(val) < score_max:
                                                score_max = float(val)
                                    json_obj[score_percent] = score_max
                                else:
                                    print("Could not find score in response: ",score,": ",json_obj)
                            except:
                                print("error ",score,": ", traceback.format_exc())

                        # format multiple semicolon-separated predictions (select highest value)
                        predictions = ["SIFT_pred",
                                       "Polyphen2_HDIV_pred",
                                       "Polyphen2_HVAR_pred"
                                        ]
                        for pred in predictions:
                            if pred in json_obj:
                                try:
                                    pred_formatted= pred+"_formatted"
                                    values = json_obj[pred].split(";")
                                    #score_max = 0.0
                                    score_max=""
                                    for val in values:
                                        if (val!="") and (val!="."):
                                    #        if float(val) > score_max:
                                    #            score_max = float(val)
                                            score_max = val
                                            if val == "D":
                                                score_max += " (probably damaging)"
                                            elif val == "P":
                                                score_max += " (possibly damaging)"
                                            elif val == "B":
                                                score_max += " (benign)"
                                    json_obj[pred_formatted] = score_max
                                except:
                                    print("error formatting scores: ",traceback.format_exc())
                            else:
                                print("Could not find score in response: ",pred,": ",json_obj)

                        # normalize CADD
                        try:
                            cadd_score = float(json_obj["CADD_raw_rankscore"])
                            cadd_max = 18.301497
                            cadd_min = -6.458163
                            cadd_normalized =  (cadd_score - cadd_min) / (cadd_max - cadd_min)
                            json_obj["CADD_raw_rankscore_normalized"] = cadd_normalized
                            json_obj["CADD_raw_rankscore_percentage"] = int(float(cadd_normalized) * 100)
                        except:
                            print("Could not normalized CADD rankscore: ", traceback.format_exc())

                        # normalize GERP++
                        try:
                            gerp_score = float(json_obj["CADD_raw_rankscore"])
                            gerp_max = 6.17
                            gerp_min = -12.3
                            gerp_normalized =  (gerp_score - gerp_min) / (gerp_max - gerp_min)
                            json_obj["GERP_raw_rankscore_normalized"] = gerp_normalized
                            json_obj["GERP_raw_rankscore_percentage"] = int(float(gerp_normalized) * 100)
                        except:
                            print("Could not normalized CADD rankscore: ", traceback.format_exc())

                        try:
                            #json_obj.pop('q_id')
                            vcf_lines[qid][self.srv_prefix] = json_obj#[self.srv_prefix]
                        except:
                            print("error ",traceback.format_exc())

            except:
                print(traceback.format_exc())

            for i in range(0, max_length):
                del qid_list[0]
            if len(qid_list) == 0:
                break

        return vcf_lines
