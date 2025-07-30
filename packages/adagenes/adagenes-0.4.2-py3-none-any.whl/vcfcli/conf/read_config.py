import os, configparser
from pathlib import Path

# read in config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '', 'config.ini'))


def get_config(client_config=None):
    if client_config is None:
        return config
    else:
        # Merge client configuration and default configuration
        return config | client_config

if "LIFTOVER_DATA_DIR" in os.environ:
    __LIFTOVER_DATA_DIR__ = os.getenv('LIFTOVER_DATA_DIR')
else:
    #__LIFTOVER_DATA_DIR__ = config['DEFAULT']['LIFTOVER_DATA_DIR']
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __LIFTOVER_DATA_DIR__ = __location__ + '/data'

__LIFTOVER_FILE_HG38 = "hg38ToHg19.over.chain.gz"
__LIFTOVER_FILE_HG19 = "hg19ToHg38.over.chain.gz"

def download_liftover_files(liftover_dir):
    """
    Checks if the liftover files exist. Downloads them if the files cannot be found

    :param liftover_dir: Directory in the host file system where the liftover files are to be stored
    """
    path = Path(liftover_dir + "/hg19ToHg38.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ",path,". Downloading file...")
        os.system("wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)

    path = Path(liftover_dir + "/hg38ToHg19.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system("wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hg38/liftOver/hg38ToHg19.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)

    path = Path(liftover_dir + "/hs1ToHg38.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system("wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hs1/liftOver/hs1ToHg38.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ",path)

    path = Path(liftover_dir + "/hg38ToGCA_009914755.4.over.chain.gz")
    if not os.path.exists(path):
        print("Could not find Liftover file: ", path, ". Downloading file...")
        os.system(
            "wget -v https://hgdownload.soe.ucsc.edu/goldenPath/hg38/liftOver/hg38ToGCA_009914755.4.over.chain.gz -P " + liftover_dir)
    else:
        print("Liftover file located: ", path)

# test if liftover files can be found
download_liftover_files(__LIFTOVER_DATA_DIR__)

__VCF_COLUMNS__ = ["chr", "start", "id", "ref", "var", "qual", "filter", "info", "format", "seq"]
match_types = ["exact_match","any_mutation_in_gene","same_position","same_position_any_mutation"]
variant_data_key = 'variant_data'

extract_keys_list = config["VCF"]["EXTRACT_KEYS"].split(" ")
extract_keys = {}
extract_keys["UTA_Adapter_gene"] = ["hgnc_symbol","aminoacid_exchange"]
extract_keys["UTA_Adapter"] = ["gene_name","variant_exchange"]
extract_keys["revel"] = ["Score"]
extract_keys["dbnsfp"] = ["SIFT_pred"]
extract_keys["vus_predict"] = ["FATHMM","Missense3D","SIFT","Score"]
extract_keys["dbsnp"] = ["rsID", "total"]

__FEATURE_GENE__ = 'gene_name'
__FEATURE_VARIANT__ = 'variant_exchange'
__FEATURE_QID__ = 'q_id'

uta_adapter_srv_prefix = 'UTA_Adapter'
onkopus_aggregator_srv_prefix= "onkopus_aggregator"

gencode_srv_prefix = 'gencode'
drugclass_srv_prefix = 'drugclass'
civic_srv_prefix = 'civic'
dbnsfp_srv_prefix = 'dbnsfp'
mvp_srv_prefix = "mvp"
metakb_srv_prefix = "metakb"
oncokb_srv_prefix = "oncokb"
alphamissense_srv_prefix = "alphamissense"
primateai_srv_prefix = "primateai"
vuspredict_srv_prefix = "vus_predict"
loftool_srv_prefix = "loftool"
revel_srv_prefix = "revel"
clinvar_srv_prefix = "clinvar"
dbsnp_srv_prefix = 'dbsnp'
uta_adapter_genetogenomic_srv_prefix = "UTA_Adapter_gene"
uta_adapter_protein_sequence_srv_prefix = "UTA_Adapter_protein_sequence"




