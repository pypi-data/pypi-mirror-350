import unittest
import vcfcli
import vcfcli.onkopus_clients


class TestOnkopusAnnotation(unittest.TestCase):

    def test_single_module_annotation(self):

        infile="../test_files/somaticMutations.l8.vcf"
        outfile="../test_files/somaticMutations.l8.vcf.onkopus.dbsnp"
        module="dbsnp"

        #vcfcli.annotate(infile, outfile, module=module)

    def test_full_module_annotation(self):
        infile = "../test_files/somaticMutations.ln_12.vcf"
        outfile = infile + ".annotated"
        genome_version='hg19'

        #vcfcli.annotate_file_all_modules(infile, outfile, genome_version=genome_version, writer_output_format="json")

    def test_process_file_with_generic_transformer_vcf(self):
        infile = "../test_files/somaticMutations_ln25.vcf"
        outfile = infile + ".generic.vcf"
        genome_version = 'hg19'

        transformer = vcfcli.onkopus_clients.DBSNPClient(genome_version)
        vcfcli.process_file(infile, outfile, transformer, genome_version=genome_version)

    def test_process_file_with_generic_transformer_json(self):
        infile = "../test_files/somaticMutations_ln25.vcf"
        outfile = infile + ".generic.json"
        genome_version = 'hg19'

        transformer = vcfcli.onkopus_clients.DBSNPClient(genome_version)
        vcfcli.process_file(infile, outfile, transformer, genome_version=genome_version)
