import re, os, gzip
import traceback
import vcfcli.clients.reader as reader
import vcfcli.conf.read_config as config
from vcfcli.tools import parse_vcf
from vcfcli.processing.json_biomarker import BiomarkerFrame
import vcfcli.conf.vcf_config
from vcfcli.tools.json_mgt import generate_variant_data


class VCFReader(reader.Reader):
    """
    Reader for Variant Call Format (VCF)
    """

    def read_file(self, infile, genome_version=None, columns=None,sep="\t",mapping=None) -> BiomarkerFrame:
        """
        Reads in a VCF file and returns a biomarker frame

        :param infile:
        :param genome_version:
        :param columns:
        :return:
        """
        if isinstance(infile, str):
            file_name, file_extension = os.path.splitext(infile)
            input_format_recognized = file_extension.lstrip(".")
            if input_format_recognized == "gz":
                infile = gzip.open(infile, 'rt')
            else:
                infile = open(infile, 'r')

        json_obj = BiomarkerFrame(src_format='vcf')
        json_obj.header_lines = []
        json_obj.data = {}
        json_obj.info_lines = {}
        json_obj.genome_version = genome_version
        variant_count = 0
        line_count = 0
        json_obj.variants = {}

        for line in infile:
            try:
                if line.startswith('##'):
                    json_obj.header_lines.append(line.strip())
                    if genome_version is None:
                        json_obj.genome_version = self.read_genomeversion(line)
                    continue
                elif line.startswith('#CHROM'):
                    json_obj.header_lines.append(line.strip())
                    features = line.split("\t")
                    for feature in features:
                        json_obj.orig_features.append(feature)
                    # if genome version is not set yet, use hg38 as default
                    if genome_version is None:
                        json_obj.genome_version = 'hg38'

                    json_obj.info_lines, json_obj.genome_version = parse_vcf.process_vcf_headers(json_obj.header_lines,
                                                                               genome_version)
                    continue
                else:
                    variant_count += 1
                    line_count += 1

                fields = line.strip().split('\t')
                chromosome, pos, ref_base, alt_base = fields[0], fields[1], fields[3], fields[4]
                info = fields[7]
                chr_prefix = ""
                if not chromosome.startswith("chr"):
                    chr_prefix = "chr"
                variant = chr_prefix + '{}:{}{}>{}'.format(chromosome, pos, ref_base, alt_base)
                chromosome = chromosome.replace("chr", "")
                if alt_base != '.':
                    json_obj.variants[variant_count] = variant

                json_obj = generate_variant_data(json_obj, variant, chromosome, pos, fields, ref_base, alt_base)
                json_obj.info_lines = info.strip()
            except:
                print("VCF reader: Error parsing line ")
                print(traceback.format_exc())
        infile.close()

        return json_obj

    def read_file_chunk(self, infile, json_obj: BiomarkerFrame) -> BiomarkerFrame:
        """
        Reads a defined number of lines from a file object, adds them to the given biomarker set and returns the extended biomarker list

        :param infile:
        :type infile:
        :param json_obj:
        :type json_obj: BiomarkerSet
        :return: json_obj
        """

        json_obj.variant_count = 0
        json_obj.line_count = 0
        json_obj.data = {}
        json_obj.info_lines = {}
        json_obj.header_lines = []
        json_obj.c = 0

        for line in json_obj.infile:
            if line.startswith('##'):
                #if json_obj.output_format == 'vcf':
                #    print(line.strip(), file=json_obj.outfile)
                json_obj.header_lines.append(line.strip())
                if json_obj.genome_version is None:
                    json_obj.genome_version = self.read_genomeversion(line)
                continue
            elif line.startswith('#CHROM'):
                json_obj.header_lines.append(line.strip())
                # if genome version is not set yet, use hg38 as default
                if json_obj.genome_version is None:
                    json_obj.genome_version = 'hg38'

                json_obj.info_lines, json_obj.genome_version = parse_vcf.process_vcf_headers(json_obj.header_lines, json_obj.genome_version, json_obj.info_lines)
                continue
            else:
                json_obj.variant_count += 1
                json_obj.line_count += 1

            fields = line.strip().split('\t')
            chromosome, pos, ref_base, alt_base = fields[0], fields[1], fields[3], fields[4]
            info = fields[7]
            chr_prefix = ""
            if not chromosome.startswith("chr"):
                chr_prefix = "chr"
            variant = chr_prefix + '{}:{}{}>{}'.format(chromosome, pos, ref_base, alt_base)
            chromosome = chromosome.replace("chr", "")
            if alt_base != '.':
                json_obj.variants[json_obj.variant_count] = variant
            json_obj.data[variant] = {}
            json_obj.data[variant][config.variant_data_key] = {
                                  "CHROM": chromosome,
                                  "POS": pos,
                                  "ID": fields[2],
                                  "REF": ref_base,
                                  "ALT": alt_base,
                                  "QUAL": fields[5],
                                  "FILTER": fields[6],
                                  "INFO": fields[7],
                                  "OPTIONAL": fields[8:]
                                  }
            #json_obj.info_lines[variant] = info.strip()

        return json_obj

    def read_genomeversion(self, line):
        if not line.startswith('##reference'):
            return None
        p = re.compile('(##reference=).*GRCh([0-9]+).*')
        m = p.match(line)

        if m and len(m.groups()) > 1:
            genome_version = 'hg' + m.group(2)
            if genome_version == 'hg37':
                genome_version = 'hg19'
            return genome_version

        p = re.compile('(##reference=).*(hg[0-9]+).*')
        m = p.match(line)
        if m and len(m.groups()) > 1:
            return m.group(2)
        return None
