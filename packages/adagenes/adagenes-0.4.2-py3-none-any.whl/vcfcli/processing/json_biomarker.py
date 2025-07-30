
class BiomarkerFrame:
    """
    Main class for storing biomarker information

    Attributes
    ----------
    data_type: str
        Data type of the source biomarker data. May be "g" (genomic), "t" (transcriptomic) or "p" (proteomic).
        "g" describes data where biomarker data is defined a genomic locations (e.g. VCF format),
        "t" describes transcriptomic identifiers (e.g. "NM_006015.4:c.5336A>G" in CSV-format),
        and "p" describes proteomic identifiers (e.g. "BRAF:V600E" in CSV-format)

    Methods
    -------

    """

    infile = ''
    outfile = ''
    generic_obj = None
    variants_written = False
    variant_batch_size = 5000
    line_batch_size = 100
    genome_version = None
    error_logfile = None
    input_type = ''
    output_type = ''
    save_headers = True
    output_format = 'file'
    input_format = 'file'
    features = None
    variants = {}
    row = 0
    columns = []
    header_lines = []
    orig_features = []
    biomarker_pos = {}
    data_type = ""

    data = {}

    def __init__(self, data=None, genome_version="hg38", src=None,
                 header_lines=[], src_format=None,columns=[], data_type=""):
        """

        :param data:
        :param genome_version: Reference genome ("hg38","hg19")
        :param src: Source biomarker file. Stores the file path if variant data has been loaded from a file
        :param src_format: Source data format. Stores the data type if variant has been loaded from a file
        """
        if data is not None:
            self.data = data
        self.genome_version = genome_version
        self.src = src
        self.header_lines = header_lines
        self.src_format = src_format
        self.columns = columns
        self.data_type = data_type

    def __str__(self):
        tostr = "{data type: " + str(self.data_type) + ",data:" + str(self.data) + "}"
        return tostr

    def get_ids(self):
        """
        Returns a list of all biomarker IDs stored in the biomarker frame

        :return:
        """
        return list(self.data.keys())
