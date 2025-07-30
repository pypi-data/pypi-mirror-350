import unittest, copy
import vcfcli.onkopus_clients

class LiftoverAnnotationTestCase(unittest.TestCase):

    def test_liftover_client(self):
        genome_version = 'hg19'

        #infile = "../test_files/somaticMutations.vcf"
        infile = "../test_files/somaticMutations.l280.vcf"
        outfile = "../test_files/somaticMutations.l280.tsv.liftover"
        data = vcfcli.VCFReader(genome_version).read_file(infile)

        data.data = vcfcli.onkopus_clients.LiftOverClient(
            genome_version=genome_version).process_data(data.data)

        #print("Response ",data.data)
        mapping = { "variant_data": ["POS_hg19","POS_hg38"]
                 }
        vcfcli.TSVWriter().write_to_file(outfile,data,mapping=mapping)


