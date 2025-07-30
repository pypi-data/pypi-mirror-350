import adagenes
import adagenes.conf.read_config as conf_reader
import adagenes.clients.writer as writer
import traceback
import adagenes.tools.maf_mgt


def print_maf_columns(outfile):
    """
    Prints the MAF column labels to an output file

    :param outfile:
    :return:
    """
    line = adagenes.tools.maf_mgt.maf_columns
    print("\t".join(line), file=outfile)


def to_single_maf_line(qid,json_obj):
        """

        :param qid:
        :param json_obj:
        :param mapping:
        :return:
        """
        line = ""
        for feature in adagenes.tools.maf_mgt.maf_columns:
            if feature in json_obj["info_features"]:
                line += json_obj["info_features"][feature] + "\t"
        line = line.rstrip(',')
        return line


class MAFWriter(writer.Writer):

    def write_chunk_to_file(self, outfile, json_obj, variants_written=False, save_headers=False):
        """

        :param outfile:
        :param json_obj:
        :param variants_written:
        :param save_headers:
        :return:
        """
        self.write_to_file(outfile,json_obj)

    def write_to_file(self, outfile, json_obj, mapping=None, gz=False):
        """
        Write a biomarker frame to a MAF file

        :param outfile_src:
        :param json_obj:
        :param mapping:
        :return:
        """
        close_file = False
        if isinstance(outfile, str):
            if gz is False:
                outfile = open(outfile, 'w')
            else:
                outfile = open(outfile, 'wb')
            close_file = True

        self.print_header(outfile, json_obj)
        print_maf_columns(outfile)

        for var in json_obj.data.keys():
            json_obj.row = json_obj.row + 1
            print(to_single_maf_line(var, json_obj.data[var]), file=outfile)

        if close_file is True:
            outfile.close()

    def print_header(self, outfile, bframe: adagenes.BiomarkerFrame):
        """
        Prints the header lines of a MAF if the source format had been MAF as well

        :param outfile: Output file
        :param bframe: Annotated iomarker frame
        :return:
        """
        #headers="#version 2.3\n"
        if (bframe.src_format == "maf"):
            for line in bframe.header_lines:
                print(line, file=outfile)
