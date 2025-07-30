import unittest, copy
import vcfcli.onkopus_clients

class GencodeMANESelectTestCase(unittest.TestCase):

    def test_gencode_client(self):
        genome_version = 'hg38'
        data = {"chr7:140753336A>T": {}, "chr10:8115913C>T": {}}

        variant_data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data)
        variant_data = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version).process_data(variant_data)
        variant_data = vcfcli.onkopus_clients.GENCODEMANESelectClient(
            genome_version=genome_version).process_data(variant_data)

        print("Response ",variant_data)


