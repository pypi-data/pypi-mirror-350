import unittest, copy
import vcfcli.onkopus_clients

class LoFToolAnnotationTestCase(unittest.TestCase):

    def test_loftool_client(self):
        genome_version = 'hg19'

        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}

        variant_data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data)
        variant_data = vcfcli.onkopus_clients.LoFToolClient(
            genome_version=genome_version).process_data(variant_data)

        print("Response ",variant_data)

    def test_loftool_client_batch(self):
        genome_version = 'hg19'
        file='../test_files/somaticMutations.l100.vcf'

        data = vcfcli.read_file(file, genome_version=genome_version)

        data.data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data.data)

        data.data = vcfcli.onkopus_clients.LoFToolClient(
            genome_version=genome_version).process_data(data.data)

        print(data.data)
