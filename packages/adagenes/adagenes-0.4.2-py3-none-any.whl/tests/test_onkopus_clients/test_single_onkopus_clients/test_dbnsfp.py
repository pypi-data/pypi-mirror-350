import unittest
import vcfcli.onkopus_clients

class DBNSFPAnnotationTestCase(unittest.TestCase):

    def test_dbnsfp_client(self):
        genome_version = 'hg38'
        data = {"chr7:140753336A>T": {}}

        data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data)
        data = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version).process_data(data)
        variant_data = vcfcli.onkopus_clients.DBNSFPClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)

    def test_dbnsfp_client_batch(self):
        genome_version = 'hg19'
        file='../test_files/somaticMutations.l100.vcf'

        #data = vcfcli.read_file(file, genome_version=genome_version)
        #data.data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data.data)
        #data.data = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version).process_data(data.data)
        #data.data = vcfcli.onkopus_clients.DBNSFPClient(
        #    genome_version=genome_version).process_data(data.data)

        #print(data.data)
