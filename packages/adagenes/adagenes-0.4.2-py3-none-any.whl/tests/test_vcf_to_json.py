import json
import unittest
import vcfcli

class TestVCFtoJSON(unittest.TestCase):

    '''def test_vcf_to_json_line12(self):
        obj= vcfcli.vcf_clients.vcf_to_json_client.VCFtoJSONClient('hg38')

        infile_str = './test_files/somaticMutations.vcf.line_12'
        outfile_str = './test_files/somaticMutations.line_12_nw.json'

        infile= open(infile_str, 'r')
        outfile = open(outfile_str, 'w')
        vcfcli.vcf_reader.process_vcf_file(infile, outfile, obj, input_format='vcf', output_format='json')
        infile.close()
        outfile.close()

        # test to load the file
        infile = open(outfile_str, 'r')
        obj = json.load(
            infile
        )
        infile.close()
        print(obj)

    def test_vcf_to_json_line100(self):
        obj= vcfcli.vcf_clients.vcf_to_json_client.VCFtoJSONClient('hg38')

        infile_str = './test_files/somaticMutations.vcf.line_100'
        outfile_str = './test_files/somaticMutations.line_100_nw.json'

        infile= open(infile_str, 'r')
        outfile = open(outfile_str, 'w')
        vcfcli.vcf_reader.process_vcf_file(infile, outfile, obj, input_format='vcf', output_format='json')
        infile.close()
        outfile.close()

        # test to load the file
        infile = open(outfile_str, 'r')
        obj = json.load(
            infile
        )
        infile.close()
        print(obj)

    def test_vcf_to_json_line116(self):
        obj= vcfcli.vcf_clients.vcf_to_json_client.VCFtoJSONClient('hg38')

        infile_str = './test_files/somaticMutations.vcf.line_116'
        outfile_str = './test_files/somaticMutations.line_116_nw.json'

        infile= open(infile_str, 'r')
        outfile = open(outfile_str, 'w')
        vcfcli.vcf_reader.process_vcf_file(infile, outfile, obj, input_format='vcf', output_format='json')
        infile.close()
        outfile.close()

        # test to load the file
        infile = open(outfile_str, 'r')
        obj = json.load(
            infile
        )
        infile.close()
        print(obj)

    def test_vcf_to_json_line5801(self):
        obj= vcfcli.vcf_clients.vcf_to_json_client.VCFtoJSONClient('hg38')

        infile_str = './test_files/somaticMutations.vcf.line_5800'
        outfile_str = './test_files/somaticMutations.line_5800_nw.json'

        infile= open(infile_str, 'r')
        outfile = open(outfile_str, 'w')
        vcfcli.vcf_reader.process_vcf_file(infile, outfile, obj, input_format='vcf', output_format='json')
        infile.close()
        outfile.close()

        # test to load the file
        infile = open(outfile_str, 'r')
        obj = json.load(
            infile
        )
        infile.close()
        print(obj)

    def test_vcf_to_json_annotated(self):
        obj= vcfcli.vcf_clients.vcf_to_json_client.VCFtoJSONClient('hg38')

        infile_str = './test_files/variants.annotated.vcf'
        outfile_str = './test_files/variants.annotated.json'

        infile= open(infile_str, 'r')
        outfile = open(outfile_str, 'w')
        vcfcli.vcf_reader.process_vcf_file(infile, outfile, obj, input_format='vcf', output_format='json')
        infile.close()
        outfile.close()

        # test to load the file
        infile = open(outfile_str, 'r')
        obj = json.load(
            infile
        )
        infile.close()
        print(obj)
    '''
