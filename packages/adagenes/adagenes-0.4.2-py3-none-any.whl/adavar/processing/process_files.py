import re, traceback, copy, json, gzip
import adagenes.conf.read_config as config
from adagenes.processing.json_biomarker import BiomarkerFrame
from adagenes.tools.client_mgt import get_reader, get_writer


def process_file(
                 infile_src,
                 outfile_src,
                 generic_obj,
                 input_format=None,
                 output_format=None,
                 variant_batch_size=100,
                 line_batch_size=5000,
                 genome_version=None,
                 error_logfile=None,
                 input_type='file',
                 output_type='file',
                 save_headers=True,
                 features=None,
                 lo_hg19=None,
                 lo_hg38=None
                 ):
    reader = get_reader(infile_src, file_type=input_format)
    reader.infile_src = infile_src
    reader.open_file(infile_src)
    writer = get_writer(outfile_src, file_type=output_format)
    writer.outfile_src = outfile_src
    writer.open_file(outfile_src)

    process(
        reader,
        writer,
        generic_obj,
        input_format='vcf',
        output_format='vcf',
        variant_batch_size=100,
        line_batch_size=5000,
        genome_version=None,
        error_logfile=None,
        input_type='file',
        output_type='file',
        save_headers=True,
        features=None,
        lo_hg19=lo_hg19,
        lo_hg38=lo_hg38
    )

    reader.close_file()
    writer.close_file()


def process(
            reader,
            writer,
            module,
            input_format='vcf',
            output_format='vcf',
            variant_batch_size=100,
            line_batch_size=5000,
            genome_version=None,
            error_logfile=None,
            input_type='file',
            output_type='file',
            save_headers=True,
            features=None,
            lo_hg19=None,
            lo_hg38=None
            ):
    """
        Reads a file of genetic mutations in multiple formats (VCF, JSON), calls a specific processing function that edits the contents of the input file and saves the results in an output file

        :param infile:
        :param outfile:
        :param generic_obj:
        :param input_format:
        :param output_format:
        :param variant_batch_size:
        :param line_batch_size:
        :param genome_version:
        :param output_type:
        :param save_headers
        :return:
        """

    json_obj = BiomarkerFrame()
    json_obj.infile = reader.infile
    json_obj.outfile = writer.outfile
    json_obj.module = module
    json_obj.variants_written = False
    json_obj.variant_batch_size = variant_batch_size
    json_obj.line_batch_size = line_batch_size
    json_obj.genome_version = genome_version
    json_obj.error_logfile = error_logfile
    json_obj.input_type = input_type
    json_obj.output_type = output_type
    json_obj.save_headers = save_headers
    json_obj.output_format = output_format
    json_obj.input_format = input_format
    json_obj.features = features
    json_obj.variants = {}
    json_obj.row = 0
    json_obj.data = {}
    print_headers = True

    writer.write_to_file_start(json_obj.outfile)


    # process
    #if (len(json_obj.variants) >= json_obj.variant_batch_size) or (len(json_obj.data) >= json_obj.line_batch_size):
    json_obj = reader.read_file_chunk(json_obj.infile,json_obj)

    if module=="liftover":
        json_obj.data = module.process_data(json_obj.data,lo_hg19=lo_hg19,lo_hg38=lo_hg38)
    else:
        json_obj.data = module.process_data(json_obj.data)

    writer.write_chunk_to_file(json_obj.outfile, json_obj,variants_written=json_obj.variants_written, save_headers=print_headers)
    print_headers = False

    json_obj.variants = {}
    json_obj.data = {}
    json_obj.variant_count = 0
    json_obj.line_count = 0
    json_obj.info_lines = {}
    json_obj.variants_written = True


    writer.write_to_file_finish(json_obj.outfile)

    # if input_format == 'vcf':
    #    self._read_vcf_file_chunk()
    # elif input_format == 'json':
    #    self.data = json.load(infile)
    #    if 'vcf_header' in self.data.keys():
    #        self.data.pop('vcf_header')
    #    for i, key in enumerate(self.data.keys()):
    #        self.variants[i] = key
    # elif input_format == 'tsv':
    #     self.data = self.load_table_file(infile)
    #     for i, key in enumerate(self.data.keys()):
    #        self.variants[i] = key

    # query the service with the remaining lines
    # self._module_requests()
    # self._vcf_to_json()

    # if output_type == 'obj':
    #    return self.data

def _write_chunk_to_file(self):
    #if self.output_format == 'json' and self.variants_written:
    #    print(',', file=self.outfile, end='')
    # elif output_format == 'tsv':
    #    print("f ",'\t'.join(get_feature_keys(data, generic_obj.extract_keys)))
    #    print('\t'.join(get_feature_keys(data, generic_obj.extract_keys)),file=outfile)

    try:
        self.data = self.generic_obj.process_data(self.data, self.variants, self.outfile,
                                                       input_format=self.input_format)
    except:
        print("error calling object-specific function")
        print(traceback.format_exc())

    if self.output_type == 'file':
        c = 1

        for var in self.data.keys():
            self.row = self.row + 1
            if self.output_format == 'vcf':
                print(self.to_single_vcf_line(self.data[var], self.generic_obj.srv_prefix,
                                              self.generic_obj.extract_keys),
                      file=self.outfile)
            elif self.output_format == 'json':
                json_str = json.dumps(self.data[var])
                json_str = "\"" + var + "\"" + ":" + json_str
                if c < len(self.data):
                    json_str = json_str + ','
                c += 1
                print(json_str, file=self.outfile)
            elif self.output_format == 'tsv':
                if self.row == 1:
                    # add column labels in 1st row
                    print(self.get_feature_keys(self.data, self.generic_obj.extract_keys), file=self.outfile)
                tsv_str = self.to_single_tsv_line(self.data[var], self.generic_obj.srv_prefix,
                                                  self.generic_obj.extract_keys)
                print(tsv_str, file=self.outfile)

        self.variants = {}
        self.data = {}
        self.variant_count = 0
        self.line_count = 0
        self.info_lines = {}
        self.variants_written = True


def _module_requests(self):
    c = 1
    if len(self.data) > 0:
        try:
            self.data = self.generic_obj.process_data(self.data, self.variants, self.outfile,
                                                           input_format=self.input_format)
        except:
            print("error calling object-specific function")
            print(traceback.format_exc())
        if self.output_format == 'json' and self.variants_written:
            print(',', file=self.outfile, end='')
        for var in self.data.keys():
            self.row = self.row + 1
            if self.output_type == 'file':
                if self.output_format == 'vcf':
                    # print("write to file ",self.data)
                    print(self._to_single_vcf_line(self.data[var], self.generic_obj.srv_prefix,
                                                   self.generic_obj.extract_keys),
                          file=self.outfile)
                elif self.output_format == 'json':
                    json_str = json.dumps(self.data[var])
                    json_str = "\"" + var + "\"" + ":" + json_str
                    if c < len(self.data):
                        json_str = json_str + ','
                    print(json_str, file=self.outfile)
                    c += 1
                elif self.output_format == 'tsv':
                    # add column labels in 1st row
                    if self.row == 1:
                        print(self.get_feature_keys(self.data, self.generic_obj.extract_keys),
                              file=self.outfile)
                    tsv_str = self.to_single_tsv_line(self.data[var], self.generic_obj.srv_prefix,
                                                      self.generic_obj.extract_keys)
                    print(tsv_str, file=self.outfile)

def transform_file_format(input_file, input_format=None, output_format=None):

    pass
