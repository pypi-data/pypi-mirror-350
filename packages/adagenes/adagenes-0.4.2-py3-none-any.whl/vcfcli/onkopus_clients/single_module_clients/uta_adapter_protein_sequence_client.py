import traceback, copy
import vcfcli.tools.module_requests as req
from vcfcli.conf import read_config as config
import vcfcli.tools.parse_genomic_data


class UTAAdapterProteinSequenceClient:

    def __init__(self, genome_version, error_logfile=None):
        self.genome_version = genome_version
        self.info_lines = config.uta_adapter_protein_sequence_info_lines
        self.url_pattern = config.uta_adapter_protein_sequence_src
        self.srv_prefix = config.uta_adapter_protein_sequence_srv_prefix
        self.genomic_keys = config.uta_genomic_keys
        self.gene_keys = config.uta_gene_keys
        self.gene_response_keys = config.uta_gene_response_keys
        self.extract_keys = config.uta_genomic_keys

        self.qid_key = "q_id"
        if (self.genome_version == "hg19") or (self.genome_version == "GRCh37"):
            self.qid_key = "q_id_hg19"

    def process_data(self, vcf_lines):
        keys = [config.uta_genomic_keys[0],
                    config.uta_genomic_keys[1]]
        annotations = vcfcli.tools.parse_vcf.extract_annotations_json(vcf_lines, config.uta_adapter_srv_prefix, keys)
        gene_names = copy.deepcopy(annotations[keys[0]])
        variant_exchange = copy.deepcopy(annotations[keys[1]])

        qid_list = copy.deepcopy(annotations['q_id'])

        while True:

            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            #qids_partial = qid_list[0:max_length]
            #qids_partial = vcfcli.tools.filter_alternate_alleles(qids_partial)

            gene_names_partial = gene_names[0:max_length]
            variant_exchange_partial = variant_exchange[0:max_length]
            gene_request = False

            for gene_name in gene_names_partial:
                if gene_name == '':
                    gene_request=True

            max_length = int(config.config["DEFAULT"]["MODULE_BATCH_SIZE"])
            if max_length > len(qid_list):
                max_length = len(qid_list)
            qids_partial = qid_list[0:max_length]

            if gene_request:
                q = ','.join(qids_partial)
            else:
                variants = []
                for gene,variant in zip(gene_names_partial,variant_exchange_partial):
                    variants.append(gene + ":" + variant)
                q = ','.join(variants)

            try:
                json_body = req.get_connection(q, self.url_pattern, self.genome_version)

                for key in json_body[0].keys():
                        if gene_request:
                            qid = str(json_body[0][key]["header"]["qid"])
                        else:
                            qid_index = variants.index(str(json_body[0][key]["header"]["qid"]))
                            qid = qids_partial[qid_index]
                            #print("genompos for ",str(json_body[0][key]["header"]["qid"]),": ",qid)

                        if json_body[0][key]["data"] is not None:
                            if type(json_body[0][key]["data"]) is dict:
                                #print("available qids: ",list(vcf_lines.keys()))
                                vcf_lines[qid][self.srv_prefix] = json_body[0][key]["data"]
                            else:
                                vcf_lines[qid][self.srv_prefix] = {}
                                vcf_lines[qid][self.srv_prefix]["status"] = 400
                                vcf_lines[qid][self.srv_prefix]["msg"] = json_body[0][key]["data"]
            except:
                print("error: genomic to gene")
                print(traceback.format_exc())

            for i in range(0, max_length):
                del qid_list[0]  # qid_list.remove(qid)
            if len(qid_list) == 0:
                break

        return vcf_lines
