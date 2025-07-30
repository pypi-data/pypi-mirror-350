from numpy import bool_

import adagenes.conf.read_config as conf_reader
import adagenes.clients.writer as writer
import adagenes
import traceback, csv, copy, json
import numpy as np


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, bool):
            return str(obj)
        if isinstance(obj, bool_):
            return str(obj)
        return super(NpEncoder, self).default(obj)

class AVFWriter(writer.Writer):

    def write_to_file(self, outfile,
                      json_obj: adagenes.BiomarkerFrame,
                      genome_version="hg38",
                      mapping=None,
                      labels=None,
                      ranked_labels=None,
                      sep=','):
        close_file = False
        if isinstance(outfile, str):
            outfile = open(outfile, 'w')
            close_file = True

        # Write header lines
        print("# GENOME_VERSION=" + str(json_obj.genome_version), file=outfile)

        # Write main data
        print(json.dumps(json_obj.data, cls=NpEncoder), file=outfile)

        if close_file is True:
            outfile.close()



