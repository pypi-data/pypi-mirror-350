from adagenes.tools import open_infile


class Reader():

    infile = None
    infile_src = None

    def __init__(self, genome_version=None):
        self.genome_version=genome_version

    def open_file(self,infile_src):
        self.infile = open_infile(infile_src)

    def close_file(self):
        self.infile.close()

    def read_file(self, infile):
        pass

    def read_file_chunk(self,  infile):
        pass

    def read_header(self, line):
        pass
