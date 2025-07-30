import datetime, traceback, copy
import vcfcli.tools
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config
import vcfcli.tools.parse_drug_names
from vcfcli.tools import generate_variant_dictionary


class DrugOnClient:
    """
    Client for the Onkopus drug class module
    """

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.url_pattern = config.drugclass_src
        self.srv_prefix = config.drugclass_srv_prefix
        self.extract_keys = config.drugclass_keys
        self.info_lines = config.drugclass_info_lines
        self.error_logfile = error_logfile

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def get_drug_list(self, variant_keys,variants,section="merged_evidence_data"):
        """
        Retrieves a list of all drug names found in all treatment options for all biomarkers in a biomarker set

        :param variants:
        :return:
        """
        drug_list=[]
        for qid in variant_keys:
            try:
                q_drugs = ""
                therapy_list = []
                #for section in config.clinical_evidence_match_types:
                for match_type in config.match_types:
                    if match_type in variants[qid]["onkopus_aggregator"][section]:
                        for i, treatment in enumerate(variants[qid]["onkopus_aggregator"][section][match_type]):

                                therapy = []
                                # q_drugs += treatment["drugs"] + ";"

                                if "drugs" in treatment:
                                    drugs = treatment["drugs"]
                                    for d, drug in enumerate(drugs):
                                        if isinstance(drug, dict):
                                            if "drug_name_norm" in drug:
                                                if drug['drug_name_norm'] != "":
                                                    drug_name = drug['drug_name_norm'].lower()
                                                    therapy.append(drug_name)
                                                    drug_list.append(drug_name)
                                            else:
                                                print("no drug name found ", drug)
                                        elif isinstance(drug,str):
                                            drug_name = drug.lower()
                                            therapy.append(drug_name)
                                            drug_list.append(drug_name)
                                    therapy_list.append(therapy)
                                else:
                                    print("Error: No drugs section found for ",qid," for treatment ",treatment)
            except:
                print("error getting list of drugs from variants")
                print(traceback.format_exc())

        # Remove duplicates from drug list
        drug_list = list(dict.fromkeys(drug_list))

        return drug_list

    def get_drug_classes(self, drug_list):
        """
        Retrieves drug classes from the Onkopus DrugOn adapter

        :param drug_list: List of drug names
        :return: Dictionary that contains drug names as keys and a list of drug classifications as values
        """
        drug_classifications = {}

        while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(drug_list):
                max_length = len(drug_list)
            qids_partial = drug_list[0:max_length]

            try:
                query = ""
                for drug in qids_partial:
                    if drug not in drug_classifications:
                        query += drug + ";"
                query = query.rstrip(";")
                json_body = req.get_connection(query, self.url_pattern, self.genome_version)

                for drug_name in json_body.keys():
                    drug_classes = json_body[drug_name]["manual drug class"]
                    drug_classifications[drug_name.lower()] = drug_classes
            except:
                print("Error retrieving drug classes ")
                print(traceback.format_exc())

            for i in range(0, max_length):
                del drug_list[0]
            if len(drug_list) == 0:
                break
        #print("drug classifications ",drug_classifications)
        return drug_classifications

    def process_data(self, vcf_lines, section="merged_evidence_data", match_type="exact_match"):
            """
            Retrieves drug classes for all drugs found in the aggregated, merged clinical significance data section of each biomarker

            :param vcf_lines:
            :param section:
            :param match_type:
            :return:
            """

            vcf_lines = vcfcli.tools.parse_drug_names.parse_drug_names(vcf_lines,config.match_types)

            # for each variant, extract drugs from treatment results and query drug classes


            qid_list = copy.deepcopy(list(vcf_lines.keys()))
            #while True:
            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            variant_keys = vcfcli.tools.filter_alternate_alleles(qids_partial)

            drug_list = self.get_drug_list(variant_keys,vcf_lines)
            print("drug list ",drug_list)

            drug_class_dc = self.get_drug_classes(copy.copy(drug_list))
            print("drug classes ",drug_class_dc)

            for qid in variant_keys:
                    try:
                        #for section in config.clinical_evidence_match_types:
                        for match_type in config.match_types:
                            if match_type in vcf_lines[qid]["onkopus_aggregator"][section]:
                                for i, treatment in enumerate(vcf_lines[qid]["onkopus_aggregator"][section][match_type]):
                                        for d,drug in enumerate(treatment["drugs"]):
                                            drug_class = ""
                                            if "drug_name_norm" in drug:
                                                drug_name = drug["drug_name_norm"]
                                                if drug_name.lower() in drug_class_dc:
                                                    drug_class = drug_class_dc[drug_name.lower()]
                                            try:
                                                if isinstance(vcf_lines[qid]["onkopus_aggregator"][section]
                                                                  [match_type][i]["drugs"][d],dict):
                                                    if "drug_class" not in vcf_lines[qid]["onkopus_aggregator"][section][match_type][i]["drugs"][d]:
                                                            vcf_lines[qid]["onkopus_aggregator"][section][match_type][i][
                                                                    "drugs"][d]["drug_class"] = []
                                                    #print("add drug class ",drug_class)
                                                    vcf_lines[qid]["onkopus_aggregator"][section][match_type][i][
                                                        "drugs"][d]["drug_class"]= drug_class # .append(drug_class)
                                                else:
                                                    print("No parseable result: ",print(vcf_lines[qid]["onkopus_aggregator"][section][match_type][i][
                                                        "drugs"][d]))
                                            except:
                                                print("error assigning drug class")
                                                print(traceback.format_exc())
                    except:
                        if self.error_logfile is not None:
                            print("error processing request: ", vcf_lines, file=self.error_logfile + str(datetime.datetime) + '.log')
                        else:
                            print(": error processing variant response: ;", traceback.format_exc())

            return vcf_lines
