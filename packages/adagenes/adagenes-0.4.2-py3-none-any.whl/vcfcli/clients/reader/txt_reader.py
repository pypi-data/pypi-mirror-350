import os, gzip
import vcfcli.clients.reader as reader
import vcfcli.conf.read_config as conf_reader
from vcfcli.tools import parse_genome_position
import vcfcli
import pandas as pd


class TXTReader(reader.Reader):

    def read_file(self, infile,
                  genome_version='hg38',
                  batch_size=100,
                  columns=None,
                  mapping=None,
                  header=0,
                  sep=','
                  ) -> vcfcli.BiomarkerFrame:
        """
        Loads a tab or comma-separated file in a variant data object

        :param batch_size:
        :param sep:
        :param genome_version:
        :param infile:
        :return:
        """
        if genome_version is None:
            genome_version = self.genome_version

        #if isinstance(infile, str):
        #    file_name, file_extension = os.path.splitext(infile)
        #    input_format_recognized = file_extension.lstrip(".")
        #    if input_format_recognized == "gz":
        #        infile = gzip.open(infile, 'rt')
        #    else:
        #        infile = open(infile, 'r')

        if header == 0:
            header_val = 0
        else:
            header_val = None
        df = pd.read_csv(infile,sep=sep,header=header_val)

        json_obj = vcfcli.BiomarkerFrame()
        row = 0
        dragen_file = vcfcli.is_dragen_file(df.columns)
        if dragen_file:
            json_obj.data_type = "g"

        json_obj = vcfcli.parse_dataframe_biomarkers(df,json_obj, dragen_file=dragen_file,mapping=mapping,
                                                     genome_version=genome_version)
        # print("loaded tsv: ", variant_data)

        return json_obj

    def read_file2(self, infile,
                  genome_version=None,
                  columns=None,
                  mapping=None,
                  sep=","
                  ) -> vcfcli.BiomarkerFrame:
        """
        Parses a plain text file as biomarker input data.
        If no mapping is specified, the TXT reader search for columns labeled according to the VCF specification
        ("CHROM","POS","REF","ALT"). A custom mapping can be specified, which is a dictionary that specifies the
        indices of the chromosome, position, reference allele and alternate allele column, e.g.
        mapping = {
            "chrom": 1,
            "pos": 2,
            "ref": 4,
            "alt": 5
        }

        :param infile:
        :param genome_version:
        :param columns:
        :param mapping:
        :param sep:
        :return:
        """
        if genome_version is None:
            genome_version = ""

        if isinstance(infile, str):
            file_name, file_extension = os.path.splitext(infile)
            input_format_recognized = file_extension.lstrip(".")
            if input_format_recognized == "gz":
                infile = gzip.open(infile, 'rt')
            else:
                infile = open(infile, 'r')

        json_obj = vcfcli.BiomarkerFrame()
        json_obj.data = {}
        columns = []
        chrom_pos = 0
        pos_pos = 1
        ref_pos=2
        alt_pos=3
        if mapping is not None:
            chrom_pos = mapping["chrom"]
            pos_pos = mapping["pos"]
            ref_pos = mapping["ref"]
            alt_pos = mapping["alt"]

        for i,line in enumerate(infile):
            line = line.strip()
            fields = line.split(sep)

            if i == 0:
                #columns = fields.split("")
                columns = list(map(str.lower, fields))
                print(columns)
                if mapping is None:
                    if ("CHROM" in columns) and ("POS" in columns) and ("REF" in columns) and ("ALT" in columns):
                        chrom_pos = columns.index("CHROM")
                        pos_pos = columns.index("POS")
                        ref_pos = columns.index("REF")
                        alt_pos = columns.index("ALT")
                    else:
                        print("Error: Could not find column labels for identifying SNPs (CHROM,POS,REF,ALT) and "
                              "no column mapping is specified. Please add column labels to your variant file or "
                              "define a mapping that defined the indices of the associated columns, e.g. "
                              "        mapping = {"
                              "  'chrom': 1,"
                              "  'pos': 2,"
                              "  'ref': 4,"
                              "  'alt': 5"
                              "}"
                              )
                        exit(1)
                continue

            chrom = fields[chrom_pos]
            chrom = chrom.replace("chr","")
            pos = fields[pos_pos]
            ref = fields[ref_pos]
            alt = fields[alt_pos]
            qid = "chr" + str(chrom) + ":" + str(pos) + str(ref) + ">" + str(alt)
            json_obj.data[qid] = {}

            #chromosome, ref_seq, pos, ref, alt = parse_genome_position(qid)
            json_obj.data[qid][conf_reader.variant_data_key] = {
                "CHROM": chrom,
                "POS": pos,
                "ID": "",
                "REF": ref,
                "ALT": alt,
                "QUAL": "",
                "FILTER": "",
                "INFO": "",
                "OPTIONAL": "",
                "GENOME_VERSION": genome_version
            }

        infile.close()

        return json_obj
