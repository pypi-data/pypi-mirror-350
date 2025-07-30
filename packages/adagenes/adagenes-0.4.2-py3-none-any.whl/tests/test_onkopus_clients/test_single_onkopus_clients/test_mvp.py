import unittest, copy
import vcfcli.onkopus_clients

class MVPAnnotationTestCase(unittest.TestCase):

    def test_mvp_client(self):
        genome_version = 'hg19'

        #infile = "../test_files/somaticMutations.vcf"
        infile = "../test_files/somaticMutations.ln_12.vcf"
        outfile = "../test_files/somaticMutations.ln_12.tsv.mvp"
        #data = vcfcli.VCFReader(genome_version).read_file(infile)

        #data.data = vcfcli.onkopus_clients.MVPClient(
        #    genome_version=genome_version).process_data(data.data)

        #print("Response ",data.data)
        #mapping = { "variant_data": ["POS_hg19","POS_hg38"]
        #         }
        #vcfcli.TSVWriter().write_to_file(outfile,data,mapping=mapping)

    def test_mvp_client_hg38(self):
        genome_version = 'hg38'
        data = {"chr7:140753336A>T": {}, "chr10:8073950C>T": {}}
        #for var in data:
        #    data[var] = vcfcli.generate_variant_data_section(data[var])
        #print(data)

        #data = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version).process_data(data)
        data = vcfcli.LiftoverClient(genome_version=genome_version).process_data(data)

        print(data)
        data = vcfcli.onkopus_clients.MVPClient(
            genome_version=genome_version).process_data(data)

        print("Response ",data)


