#from adagenes.tools import open_outfile


class Writer():

    outfile = None
    outfile_src = None

    def __init__(self):
        pass

    def open_file(self, infile_src):
        #self.outfile = open_outfile(infile_src)
        pass

    def close_file(self):
        self.outfile.close()

    def write_to_file_start(self, outfile):
        pass

    def write_to_file_finish(self, outfile):
        pass

    def write_to_file(self, outfile, json_obj, genome_version=None,
                      sort_features=None,mapping=None, labels=None, sorted_features=None):
        pass

    def write_chunk_to_file(self, outfile, json_obj, variants_written=False, save_headers=False):
        pass

