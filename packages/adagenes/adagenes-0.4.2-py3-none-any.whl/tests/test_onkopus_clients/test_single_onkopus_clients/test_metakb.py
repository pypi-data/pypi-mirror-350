import unittest
import vcfcli.onkopus_clients

class MetaKBAnnotationTestCase(unittest.TestCase):

    def test_metakb_client(self):
        genome_version = 'hg19'

        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}
        data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data)
        variant_data = vcfcli.onkopus_clients.MetaKBClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)

    def test_metakb_client_batch(self):
        genome_version = 'hg38'
        file='../../test_files/variants_2023-5-9.json'

        data = vcfcli.read_file(file, genome_version=genome_version)
        data.data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data.data)
        data.data = vcfcli.onkopus_clients.MetaKBClient(
            genome_version=genome_version).process_data(data.data)

        print(data.data)
