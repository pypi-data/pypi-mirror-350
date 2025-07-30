from vcfcli.conf import read_config as config


class VCFtoJSONClient:
    def __init__(self, genome_version, error_logfile=None):
        self.srv_prefix = 'vcf-to-json'
        self.extract_keys = []

    def process_data(self, vcf_lines):

        for variant in vcf_lines.keys():
            data = vcf_lines[variant]
            infos = data[config.variant_data_key]["INFO"].split(";")
            for info in infos:
                values = info.split("=")
                if (len(values))>1:
                    module = values[0].split("_")[0]
                    if module not in vcf_lines[variant]:
                        vcf_lines[variant][module] = {}
                    vcf_lines[variant][module][values[0]] = values[1]

        return vcf_lines
