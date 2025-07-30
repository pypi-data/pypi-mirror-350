import unittest
import vcfcli.onkopus_clients


class TestOnkopusModules(unittest.TestCase):

    def test_all_modules_client(self):
        genome_version = 'hg38'
        data = {"chr7:140753336A>T": {}, "chr12:25245350C>T": {}}

        variant_data = vcfcli.onkopus_clients.AllModulesClient(
            genome_version=genome_version).process_data(data)

        print(variant_data)
