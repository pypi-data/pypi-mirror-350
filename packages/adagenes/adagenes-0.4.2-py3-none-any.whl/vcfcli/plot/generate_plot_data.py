import traceback

import pandas as pd
from vcfcli.conf import read_config as config

response_type_cols = {
    "Sensitivity/Response": 10,
    "Sensitive": 10,
    "Resistance": -10,
    "Resistant": -10,
    "": 0
}


def generate_clinical_significance_sunburst_data_biomarker_set(json_obj, pid, data_section="merged_match_types_data"):
    """

    :param json_obj:
    :param pid:
    :return:
    """
    biomarkers = []
    citation_urls = []
    evlevel = []
    drugs = []
    num = []
    cancer_types = []
    scores = []
    resp_types = []
    drugclasses = []

    if pid is None:
        pid = "Biomarkers"

    for qid in json_obj.keys():
        for result in json_obj[qid][config.onkopus_aggregator_srv_prefix][data_section]:

            val = True
            biomarker=""
            ev_level=""
            citation_url = ""
            drug = ""
            cancer_type = ""
            drug_clas = ""
            resp_type = ""

            #print("result ",result)

            try:
                #if "biomarker" in json_obj[qid][config.variant_data_key]
                if "gene_name" in json_obj[qid][config.uta_adapter_srv_prefix]:
                    gene = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"]
                else:
                    gene = ""
                if "variant_exchange" in json_obj[qid][config.uta_adapter_srv_prefix]:
                    variant_exchange = json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]
                else:
                    variant_exchange = ""
                biomarker = gene + ":" + variant_exchange
                #genename = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"] + ":" + \
                #       json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]
                #biomarkers.append(biomarker)

                if result["citation_id"] == '':
                    result["citation_id"] = "undefined"
                citation_url = result["citation_id"]
                #citation_url.append(result["citation_id"])

                ev_level = result["evidence_level_onkopus"]
                #evlevel.append(result["evidence_level_onkopus"])

                #if result["drugs"] == "":
                #    result["drugs"] = "_"
                drug = result["drugs"][0]["drug_name"]
                if drug == "":
                    drug = "_"
                #drugs.append(result["drugs"])

                cancer_type = result["disease"]
                #cancer_types.append(result["disease"])

                if "drug_class" in result:
                    if result["drug_class"] == '':
                        drug_class = "_"
                        #drugclasses.append("_")
                    else:
                        drug_class = result["drug_class"]
                        #drugclasses.append(result["drug_class"])
                else:
                    drug_class = "_"
                    #drugclasses.append("_")

                # print(result["response"])
                if "response" in result:
                    res =  result["response"]
                elif "response_type" in result:
                    res = result["response_type"]
                else:
                    val = False
                    continue

                if res in response_type_cols:
                    resp_type = response_type_cols[res]
                    #resp_types.append(response_type_cols[result["response"]])
                else:
                    # Append zero for unknown
                    resp_type = 0
                    #resp_types.append(0)
            except:
                #drugclasses.append("_")
                #resp_types.append(0)
                print(traceback.format_exc())
                val = False
                continue

            if val:
                biomarkers.append(biomarker)
                citation_urls.append(citation_url)
                evlevel.append(ev_level)
                drugs.append(drug)
                cancer_types.append(cancer_type)
                drugclasses.append(drug_class)
                resp_types.append(resp_type)

    count_cancer_types = {}
    for ctype in citation_urls:
        if ctype not in count_cancer_types:
            count_cancer_types[ctype] = 0
        count_cancer_types[ctype] = int(count_cancer_types[ctype]) + 1

    # num = [int(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    # num = [float(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    num = [float(resp_types[x]) + 20 for x in range(0, len(resp_types))]
    # num = resp_types
    patient_id = [pid for x in range(0, len(num))]

    data = {
        'PID': patient_id,
        'Biomarker': biomarkers,
        'Cancer Type': cancer_types,
        'PMID': citation_urls,
        'EvLevel': evlevel,
        'Drugs': drugs,
        'Response': resp_types,
        'Drug_Class': drugclasses,
        'num': num
    }

    print(data)
    print(len(data["PID"]), ", ", len(data["Biomarker"]), ", ", len(data["Cancer Type"]), ", ", len(data["PMID"]), ", ", len(data["EvLevel"]),
          ", ", len(data["Drugs"]), ", ", len(data["Response"]), ", ", len(data["Drug_Class"]), ", ", len(data["num"]))
    df = pd.DataFrame(data=data)
    return df

def generate_treatment_drugs_pmid_sunburst_data_all_match_types(json_obj, qid) -> pd.DataFrame:
    """
        Generates a sunburst plot of all match types of biomarker matches for all databases

        :param json_obj:
        :param qid:
        :return:
        """
    variant = []
    citation_url = []
    evlevel = []
    drugs = []
    num = []
    cancer_types = []
    scores = []
    resp_types = []
    drugclasses = []
    genename = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"] + ":" + \
               json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]

    for result in json_obj[qid][config.onkopus_aggregator_srv_prefix]["merged_match_types_data"]:

        if result["citation_id"] == '':
            result["citation_id"] = "undefined"
        citation_url.append(result["citation_id"])

        evlevel.append(result["evidence_level_onkopus"])

        if result["drugs"] == "":
            result["drugs"] = "_"
        drugs.append(result["drugs"])

        cancer_types.append(result["disease"])

        if "drug_class" in result:
            if result["drug_class"] == '':
                drugclasses.append("_")
            else:
                drugclasses.append(result["drug_class"])
        else:
            drugclasses.append("_")

        # print(result["response"])
        if result["response"] in response_type_cols:
            resp_types.append(response_type_cols[result["response"]])
        else:
            # Append zero for unknown
            resp_types.append(0)

    count_cancer_types = {}
    for ctype in citation_url:
        if ctype not in count_cancer_types:
            count_cancer_types[ctype] = 0
        count_cancer_types[ctype] = int(count_cancer_types[ctype]) + 1

    # num = [int(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    # num = [float(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    num = [float(resp_types[x]) + 20 for x in range(0, len(resp_types))]
    # num = resp_types
    variant = [genename for x in range(0, len(num))]

    data = {
        'Variant': variant,
        'Cancer Type': cancer_types,
        'PMID': citation_url,
        'EvLevel': evlevel,
        'Drugs': drugs,
        'Response Type': resp_types,
        'Drug_Class': drugclasses,
        'num': num
    }

    df = pd.DataFrame(data=data)
    return df

def generate_treatment_drugs_pmid_sunburst_data(json_obj, qid, section="merged_match_types_data"):
    """
    Generates a sunburst plot of all exact biomarker matches for all databases

    :param json_obj:
    :param qid:
    :return:
    """
    variant = []
    citation_url = []
    evlevel = []
    drugs = []
    num = []
    cancer_types = []
    scores = []
    resp_types = []
    drugclasses = []
    sources = []
    genename = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"] + ":" + \
               json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]

    for result in json_obj[qid][config.onkopus_aggregator_srv_prefix][section]:
        valid_res = True

        if result["citation_id"] == '':
            result["citation_id"] = "undefined"
        citation_url.append(result["citation_id"])

        if "evidence_level_onkopus" in result:
            evlevel.append(result["evidence_level_onkopus"])
        else:
            valid_res = False
            evlevel.append("X")

        drug_str = ""
        drug_class_str = ""
        #if result["drugs"] == "":
        #    result["drugs"] = "_"
        for drug in result["drugs"]:
            if isinstance(drug, dict):
                drug_str += drug["drug_name"] + ", "
                if "drug_class" in drug:
                    drug_class_str += drug["drug_class"] + ", "
        drug_str = drug_str.rstrip(", ")
        drug_class_str = drug_class_str.rstrip(", ")

        if drug_str == "":
            drug_str = "_"
        if drug_class_str == "":
            drug_class_str = "_"

        drugs.append(drug_str)
        drugclasses.append(drug_class_str)

        cancer_types.append(result["disease"])
        sources.append(result["source"])

        #if "drug_class" in result:
        #    if result["drug_class"] == '':
        #        drugclasses.append("_")
        #    else:
        #        drugclasses.append(result["drug_class"])
        #else:
        #    drugclasses.append("_")

        #print(result["response"])
        if "response" in result:
            if result["response"] in response_type_cols:
                resp_types.append(response_type_cols[result["response"]])
            else:
                # Append zero for unknown
                resp_types.append(0)
        elif "response_type" in result:
            if result["response_type"] in response_type_cols:
                resp_types.append(response_type_cols[result["response_type"]])
            else:
                # Append zero for unknown
                resp_types.append(0)
                valid_res = False
        else:
            print("Error: Could not find feature response: ", result)

    count_cancer_types = {}
    for ctype in citation_url:
        if ctype not in count_cancer_types:
            count_cancer_types[ctype] = 0
        count_cancer_types[ctype] = int(count_cancer_types[ctype]) + 1

    #num = [int(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    #num = [float(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    num = [float(resp_types[x])+20 for x in range(0, len(resp_types))]
    #num = resp_types
    variant = [genename for x in range(0, len(num))]

    data = {
        'Variant': variant,
        'Cancer Type': cancer_types,
        'PMID': citation_url,
        'EvLevel': evlevel,
        'Drugs': drugs,
        'Response Type': resp_types,
        'Drug_Class': drugclasses,
        'Source': sources,
        'num': num
    }

    df = pd.DataFrame(data=data)
    return df

def generate_treatment_drugs_sunburst_data(json_obj, qid):
    variant = []
    citation_url = []
    evlevel = []
    drugs = []
    num = []
    genename = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"] + ":" + \
               json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]

    for result in json_obj[qid][config.onkopus_aggregator_srv_prefix]["aggregated_evidence_data"]:

        if result["citation_url"] == '':
            result["citation_url"] = "undefined"
        citation_url.append(result["citation_url"])

        evlevel.append(result["evidence_level"])
        drugs.append(result["drugs"])

    count_cancer_types = {}
    for ctype in citation_url:
        if ctype not in count_cancer_types:
            count_cancer_types[ctype] = 0
        count_cancer_types[ctype] = int(count_cancer_types[ctype]) + 1

    num = [int(count_cancer_types[citation_url[x]]) for x in range(0, len(citation_url))]
    variant = [genename for x in range(0, len(num))]

    data = {
        'Variant': variant,
        'PMID': citation_url,
        'EvLevel': evlevel,
        'Drugs': drugs,
        'num': num
    }

    df = pd.DataFrame(data=data)
    return df

def generate_treatment_sunburst_data(json_obj, qid):

    variant=[]
    cancer_type=[]
    evlevel=[]
    drugs=[]
    num=[]
    genename = json_obj[qid][config.uta_adapter_srv_prefix]["gene_name"]+":"+json_obj[qid][config.uta_adapter_srv_prefix]["variant_exchange"]

    for result in json_obj[qid][config.onkopus_aggregator_srv_prefix]["aggregated_evidence_data"]:

        if result["disease"]=='':
            result["disease"] = "undefined"
        cancer_type.append(result["disease"])

        evlevel.append(result["evidence_level"])
        drugs.append(result["drugs"])


    count_cancer_types={}
    for ctype in cancer_type:
        if ctype not in count_cancer_types:
            count_cancer_types[ctype] = 0
        count_cancer_types[ctype] = int(count_cancer_types[ctype]) + 1

    num = [int(count_cancer_types[cancer_type[x]]) for x in range(0, len(cancer_type))]
    variant = [genename for x in range(0, len(num))]

    data = {
            'Variant':variant,
            'Cancer Type': cancer_type,
            'EvLevel': evlevel,
            'Drugs': drugs,
            'num': num
        }

    df = pd.DataFrame(data=data)
    return df
