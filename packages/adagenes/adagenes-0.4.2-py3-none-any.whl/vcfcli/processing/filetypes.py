from vcfcli.clients import vcf_to_json_client
from vcfcli import FileProcessor

def vcf_to_json(infile_str, outfile_str, genome_version):
    obj = vcf_to_json_client.VCFtoJSONClient(genome_version)
    infile = open(infile_str, 'r')
    outfile = open(outfile_str, 'w')
    processor = FileProcessor()
    processor.process_file(infile, outfile, obj, input_format='vcf', output_format='json')
    infile.close()
    outfile.close()
