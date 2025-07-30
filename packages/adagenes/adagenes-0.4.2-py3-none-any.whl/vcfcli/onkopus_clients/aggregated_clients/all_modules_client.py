import vcfcli.onkopus_clients.clinvar_client, vcfcli.onkopus_clients.uta_adapter_client


class AllModulesClient:

    def __init__(self, genome_version):
        self.queryid = 'q_id'
        self.genome_version = genome_version

    def process_data(self, biomarker_data):

        biomarker_data = vcfcli.annotate_variant_data(biomarker_data)

        return biomarker_data
