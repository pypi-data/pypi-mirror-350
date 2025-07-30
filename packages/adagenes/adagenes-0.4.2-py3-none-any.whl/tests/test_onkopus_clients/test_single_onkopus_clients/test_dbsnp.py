import unittest, copy
import vcfcli.onkopus_clients

class DBSNPAnnotationTestCase(unittest.TestCase):

    def test_dbsnp_client(self):
        genome_version = 'hg19'

        data = {"chr17:7681744T>C": {}, "chr10:8115913C>T": {}}

        variant_data = vcfcli.onkopus_clients.DBSNPClient(
            genome_version=genome_version).process_data(data)

        print("Response ",variant_data)

    def test_dbsnp_client_reader_writer(self):
        genome_version = 'hg19'
        infile_src = "../../test_files/somaticMutations_ln25.vcf"
        outfile_src = "../../test_files/somaticMutations_ln25.vcf.dbsnp"

        genompos_list = [
        ]
        data = {}
        for el in genompos_list:
            data[el] = {}

        reader = vcfcli.VCFReader(genome_version)
        writer = vcfcli.VCFWriter()

        variant_data = reader.read_file(infile_src)
        print(variant_data.data)
        variant_data.data = vcfcli.onkopus_clients.DBSNPClient(
            genome_version=genome_version).process_data(variant_data.data)

        writer.write_to_file(outfile_src, variant_data)

        print("Response ",variant_data)
