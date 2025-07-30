import requests, datetime, copy, re
import adagenes.tools.hgvs_re


def get_connection(variants, url_pattern, genome_version, headers=None):
    """
        Requests a module over a HTTP GET request

        :param variants:
        :param url_pattern:
        :param genome_version:
        :param headers: HTTP request header
        :return:
    """
    url = url_pattern.format(genome_version) + variants
    try:
        if headers is None:
            r = requests.get(url, timeout=60)
            print(r.elapsed," , ",url)
        else:
            r = requests.get(url, headers=headers, timeout=60)
            print(r.elapsed," , ",url)
    except:
        print("Error ",url)
        return {}
    return r.json()


def post_connection(biomarker_data, url, genome_version):
    """
    Requests a module over a HTTP POST request

    :param biomarker_data:
    :param url:
    :param genome_version:
    :return:
    """
    print(url)
    r = requests.post(url, json = biomarker_data)
    print(r.elapsed, " , ", url)
    return r.text


def query_service(vcf_lines, variant_dc, outfile, extract_keys, srv_prefix, url_pattern, genome_version, qid_key="q_id", error_logfile=None):
    variants = ','.join(variant_dc.values())

    try:
        json_body = get_connection(variants, url_pattern, genome_version)

        # for i, l in enumerate(variant_dc.keys()):
        for i, l in enumerate(json_body):
            if json_body[i]:
                annotations = []

                if qid_key not in json_body[i]:
                    continue
                qid = json_body[i][qid_key]

                for k in extract_keys:
                    if k in json_body[i]:
                        annotations.append('{}-{}={}'.format(srv_prefix, k, json_body[i][k]))

                try:
                    splits = vcf_lines[qid].split("\t")
                    splits[7] = splits[7] + ";" + ';'.join(annotations)
                    vcf_lines[qid] = "\t".join(splits)
                except:
                # print("error in query response ",qid,'  ,',variant_dc)
                    if error_logfile is not None:
                        cur_dt = datetime.datetime.now()
                        date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                        print(cur_dt, ": error processing variant response: ", qid, file=error_logfile)

    except:
        # print("error in whole service query ",variant_dc)
        if error_logfile is not None:
            print("error processing request: ", variants, file=error_logfile)

    for line in vcf_lines:
        print(vcf_lines[line], file=outfile)


def generate_variant_dictionary(variant_data):
    variant_dc = {}
    for i,genompos in enumerate(variant_data.keys()):
        variant_dc[i] = genompos

    return variant_dc


def filter_alternate_alleles(variant_data_keys):
    """
    Filters variants with multiple alternate alleles

    :param variant_data_keys:
    :return:
    """
    var_list = []
    for var in variant_data_keys:
        if '>' in var:
            alt = var.split(">")[1]
            if "," not in alt:
                var_list.append(copy.deepcopy(var))
            else:
                print("alt allele: ",alt)
        if '%3E' in var:
            alt = var.split("%3E")[1]
            if "," not in alt:
                var_list.append(copy.deepcopy(var))
            else:
                print("alt allele: ",alt)
    return var_list


def filter_unparseable_variants(variant_data_keys):
    """
    Filters out genomic locations that are not parseable by the Onkopus clients

    :param variant_data_keys:
    :return:
    """
    var_list = []
    pattern = re.compile(adagenes.tools.gencode.exp_genome_positions)
    for var in variant_data_keys:
        if pattern.match(var):
            var_list.append(var)
        else:
            print("No parseable variant: ",var)
    return var_list
