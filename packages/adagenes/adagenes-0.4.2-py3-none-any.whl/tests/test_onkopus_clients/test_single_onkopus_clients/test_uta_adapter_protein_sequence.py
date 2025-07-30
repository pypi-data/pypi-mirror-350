import unittest, copy
import vcfcli.onkopus_clients


class UTAAdapterProteinSequenceAnnotationTestCase(unittest.TestCase):

    def test_uta_adapter_protein_sequence_client_variant(self):
        genome_version = 'hg19'
        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}
        variant_data = vcfcli.onkopus_clients.UTAAdapterClient(
            genome_version=genome_version).process_data(data)
        variant_data = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(
            genome_version=genome_version).process_data(variant_data)
        print("Response ",variant_data)

    def test_uta_adapter_protein_sequence_client_gene(self):
        genome_version = 'hg19'
        data = {"BRAF": {}, "NRAS": {}}
        variant_data = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(
            genome_version=genome_version).process_data(data)
        print("Response ",variant_data)

