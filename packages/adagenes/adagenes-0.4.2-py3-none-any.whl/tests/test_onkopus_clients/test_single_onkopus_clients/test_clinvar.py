import unittest, copy
import vcfcli.onkopus_clients

class ClinVarAnnotationTestCase(unittest.TestCase):

    def test_clinvar_client(self):
        genome_version = 'hg19'

        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}

        variant_data = vcfcli.onkopus_clients.ClinVarClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)

    def test_clinvar_client_batch(self):
        genome_version = 'hg19'

        file='../../test_files/somaticMutations.l100.vcf'
        #vcfcli.annotate_file(file, file+'.clinvar', 'clinvar', genome_version=genome_version)

        data = vcfcli.read_file(file, genome_version=genome_version)

        data.data = vcfcli.onkopus_clients.ClinVarClient(
            genome_version=genome_version).process_data(data.data)

        print(data.data)
