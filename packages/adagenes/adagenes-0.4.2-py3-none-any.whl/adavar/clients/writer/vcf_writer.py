import adagenes.clients.writer as writer
import adagenes.conf.vcf_config
from adagenes.conf import read_config as conf_reader
from adagenes.conf import vcf_config
from adagenes.tools.parse_vcf import generate_variant_data_section,generate_vcf_columns
import traceback
import pandas as pd


def generate_annotations(vcf_obj,mapping,labels,sorted_features):
    """

    :param vcf_obj:
    :param mapping:
    :param labels:
    :param sorted_features:
    :return:
    """
    base_list=["CHROM","POS","REF","ALT","ID","QUAL","FILTER","INFO","OPTIONAL","GENOME_VERSION"]
    if (mapping is not None) and (labels is not None) and (sorted_features is not None):
        annotations = []
        cols = {}
        for module in mapping:
            if type(mapping[module]) is list:
                keys = mapping[module]
                for key in keys:
                    if module in vcf_obj:
                        if key in vcf_obj[module]:
                            val = str(vcf_obj[module][key])
                            val = val.replace(",", " ")
                            # line.append(val)
                            cols[module + "_" + key] = val
                        else:
                            # print("no key: ",module,",",key)
                            # line.append("")
                            pass
                    else:
                        # print("no module: ",module,",",key)
                        # line.append("")
                        pass
            else:
                # line.append(str(vcf_obj[module]))
                pass
        # line = line.rstrip(',')
        # line = sort_features(line, cols)
        for feature in sorted_features:
            if feature in cols:
                # line.append(cols[feature])
                label = labels[feature]
                annotations.append(label + '=' + cols[feature])
            else:
                # print("feature not found ",feature,",",cols.keys())
                # line.append("")
                pass
    else:
        annotations = []
        if "variant_data" in vcf_obj:
            for feature in vcf_obj["variant_data"]:
                if feature == "info_features":
                    for info_feature in vcf_obj["variant_data"]["info_features"]:
                        annotations.append(feature+ "=" + vcf_obj["variant_data"]["info_features"][info_feature])
                elif isinstance(vcf_obj["variant_data"][feature],str):
                    if feature not in base_list:
                        annotations.append(feature+"="+vcf_obj["variant_data"][feature])
    return annotations


class VCFWriter(writer.Writer):

    def write_to_file(self, outfile, json_obj, genome_version="hg38",
                      mapping=None, labels=None, ranked_labels=None,
                      sort_features=False, save_headers=True):
        """
        Writes a biomarker JSON representation into a Variant Call Format (VCF) file

        :param outfile: Output file where to save the new file. May either be a file object or a string
        :param json_obj: Biomarker JSON representation
        :param genome_version: Reference genome of the source data which is saved as an additional header line. Possible values are 'hg19', 'GRCh37, 'hg38' and 'GRCh38'
        :param save_headers: Defines whether header lines should be included in the VCF file
        :return:
        """
        close_file = False
        if isinstance(outfile, str):
            outfile = open(outfile, 'w')
            close_file = True

        if save_headers:
            # print preexisting header lines
            if len(json_obj.header_lines) > 0:
                for line in json_obj.header_lines:
                    print(line, file=outfile)
            else:
                if genome_version is not None:
                    print(adagenes.conf.vcf_config.genome_version_line.format(genome_version), file=outfile)
                print(adagenes.conf.vcf_config.base_info_line, file=outfile)

        for var in json_obj.data.keys():
            json_obj.row = json_obj.row + 1
            row = self.to_single_vcf_line(json_obj.data[var], mapping=mapping,labels=labels,
                                              sort_features=sort_features, sorted_features = ranked_labels)
            if row != '':
                print(row,file=outfile)

        if close_file is True:
            outfile.close()


    def write_chunk_to_file(self, outfile, json_obj, save_headers=False, variants_written=False):
        """
        Writes a defined number of lines in an output file

        :param outfile:
        :param json_obj:
        :param save_headers:
        :param variants_written:
        :return:
        """

        if save_headers:
            for line in json_obj.header_lines:
                print(line, file=outfile)

        for var in json_obj.data.keys():
            json_obj.row = json_obj.row + 1
            print(self.to_single_vcf_line(json_obj.data[var]), file=outfile)

    def to_single_vcf_line(self, vcf_obj,mapping=None, labels=None, sort_features=True, sorted_features=None):
        """
        Receives data of a single variant in JSON format and converts it to a line in Variant Call Format (VCF)

        :param vcf_obj:
        :param srv_prefix:
        :param extract_keys:
        :return:
        """

        try:
            vcf_obj = generate_variant_data_section(vcf_obj)
            vcf_obj = generate_vcf_columns(vcf_obj)

            # generate annotated INFO column
            #print(self.get_tsv_labels(json_obj,mapping=mapping,labels=labels),file=outfile)
            #if sort_features is False:
            #    columns = adagenes.tools.parse_dataframes.get_tsv_labels(mapping=mapping,labels=labels)
            #    sorted_features = columns
            #else:
            #row = sorted_features
            #newrow=[]
            #for label in row:
            #    if label in labels:
            #        col = labels[label]
            #        newrow.append(col)
            #columns = newrow

            annotations = generate_annotations(vcf_obj,mapping,labels,sorted_features)

            #for srv_prefix in extract_modules:
            #    if srv_prefix in vcf_obj:
            #        service_output = vcf_obj[srv_prefix]
            #        for k in extract_keys[srv_prefix]:
            #            if k in service_output:
            #                annotations.append('{}_{}={}'.format(srv_prefix, k, service_output[k]))

            annotations = ';'.join(annotations)
            vcf_obj[conf_reader.variant_data_key]["INFO"] = vcf_obj[conf_reader.variant_data_key]["INFO"] + ";" + annotations
            vcf_obj[conf_reader.variant_data_key]["INFO"] = vcf_obj[conf_reader.variant_data_key]["INFO"].lstrip(";.")

            if (conf_reader.variant_data_key in vcf_obj) and ('OPTIONAL' in vcf_obj[conf_reader.variant_data_key]):
                optional_columns = '\t'.join(vcf_obj[conf_reader.variant_data_key]['OPTIONAL'])
            else:
                optional_columns = ''

            if "variant_data" in vcf_obj:
                if "CHROM" in vcf_obj["variant_data"]:
                    qual = vcf_obj[conf_reader.variant_data_key]['QUAL']
                    if qual == "":
                        qual = "."
                    filter_vcf = vcf_obj[conf_reader.variant_data_key]['FILTER']
                    if filter_vcf == "":
                        filter_vcf = "."
                    id_vcf = vcf_obj[conf_reader.variant_data_key]['ID']
                    if id_vcf == "":
                        id_vcf = "."
                    info_vcf = vcf_obj[conf_reader.variant_data_key]['INFO']
                    if info_vcf == "":
                        info_vcf = "."

                    vcfline = f"{vcf_obj[conf_reader.variant_data_key]['CHROM']}\t{vcf_obj[conf_reader.variant_data_key]['POS']}\t{id_vcf}\t{vcf_obj[conf_reader.variant_data_key]['REF']}" \
                              f"\t{vcf_obj[conf_reader.variant_data_key]['ALT']}\t{qual}\t{filter_vcf}\t{info_vcf}" \
                              f"{optional_columns}"
                    vcfline = vcfline.rstrip("\t")
                    return vcfline
                else:
                    print("Could not identify: ",vcf_obj)
                    return ""
        except:
            print(traceback.format_exc())
            return ''

    def to_vcf(self):
        """
        Writes data of multiple variants in JSON format into a file in Variant Call Format (VCF)

        :param vcf_obj:
        :param srv_prefix:
        :param extract_keys:
        :param outfile:
        :return:
        """
        for json_obj in self.vcf_obj:
            print(self.to_single_vcf_line(json_obj, self.srv_prefix, self.extract_keys), file=self.outfile)
