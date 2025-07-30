import unittest, copy
import vcfcli.onkopus_clients


class UTAAdapterGeneAnnotationTestCase(unittest.TestCase):

    def test_uta_adapter_genetogenomic_client(self):
        genome_version = 'hg38'
        data = {"NRAS:Q61L": {}, "TP53:R282W": {}, "MUTYH:L420M": {}}
        variant_data = vcfcli.onkopus_clients.CCSGeneToGenomicClient(
            genome_version=genome_version).process_data(data)
        print("Response ",variant_data)

    def test_uta_adapter_client_batch(self):
        genome_version = 'hg38'

        #infile='../../test_files/somaticMutations.l100.vcf'
        infile = '../../test_files/somaticMutations.vcf'
        #vcfcli.annotate_file(file, file+'.clinvar', 'clinvar', genome_version=genome_version)

        #data = vcfcli.read_file(file, genome_version=genome_version)

        #infile="../../test_files/somaticMutations.ln_12.vcf"
        #infile="../../test_files/medium_input.vcf"
        #infile="../../test_files/99_input.vcf"
        #data = vcfcli.VCFReader(genome_version).read_file(infile=infile)
        #data = vcfcli.read_file(infile)
        #data.data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data.data)
        #variant_data = vcfcli.onkopus_clients.CCSGeneToGenomicClient(
        #    genome_version=genome_version).process_data(data.data)
        #print("Response ",variant_data)
