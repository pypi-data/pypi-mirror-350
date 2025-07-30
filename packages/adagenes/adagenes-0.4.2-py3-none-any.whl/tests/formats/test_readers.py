import unittest
import vcfcli


class TestClientMgtFunctions(unittest.TestCase):

    def test_get_reader(self):
        input_file = "somaticMutations.ln12.vcf"
        reader = vcfcli.get_reader(input_file)
        print(type(reader))




