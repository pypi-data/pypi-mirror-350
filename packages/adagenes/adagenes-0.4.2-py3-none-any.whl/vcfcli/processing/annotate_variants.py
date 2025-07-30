from vcfcli.conf import read_config as config
import copy, gzip, os, traceback, time
from threading import Thread
from typing import Dict
from vcfcli.conf import read_config as conf_reader
from vcfcli.onkopus_clients import CCSGeneToGenomicClient
import vcfcli.onkopus_clients
from vcfcli.tools.parse_genomic_data import parse_genome_position
from vcfcli.tools import open_infile, open_outfile
from vcfcli.tools.data_structures import merge_dictionaries


def get_onkopus_client(module, genome_version):
    """
    Returns an Onkopus module client by identifier

    :param module:
    :param genome_version:
    :return:
    """
    if module == 'ccs_liftover':
        return vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version)
    if module == 'dbsnp':
        return vcfcli.onkopus_clients.DBSNPClient(genome_version=genome_version)
    if module == 'clinvar':
        return vcfcli.onkopus_clients.ClinVarClient(genome_version=genome_version)
    if module == 'revel':
        return vcfcli.onkopus_clients.REVELClient(genome_version=genome_version)
    if module == 'loftool':
        return vcfcli.onkopus_clients.LoFToolClient(genome_version=genome_version)
    if module == 'vuspredict':
        return vcfcli.onkopus_clients.VUSPredictClient(genome_version=genome_version)
    if module == 'metakb':
        return vcfcli.onkopus_clients.MetaKBClient(genome_version=genome_version)
    if module == 'mvp':
        return vcfcli.onkopus_clients.MVPClient(genome_version=genome_version)
    if module == 'primateai':
        return vcfcli.onkopus_clients.PrimateAIClient(genome_version=genome_version)
    if module == 'alphamissense':
        return vcfcli.onkopus_clients.AlphaMissenseClient(genome_version=genome_version)
    if module == 'dbnsfp':
        return vcfcli.onkopus_clients.DBNSFPClient(genome_version=genome_version)
    if module == 'gencode':
        return vcfcli.onkopus_clients.GENCODEClient(
            genome_version=genome_version)
    if module == 'gencode_genomic':
        return vcfcli.onkopus_clients.GENCODEGenomicClient(
            genome_version=genome_version)
    if module == 'uta_adapter_protein_sequence':
        return vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version=genome_version)
    if module == 'civic':
        return vcfcli.onkopus_clients.CIViCClient(genome_version=genome_version)
    if module == 'oncokb':
        return vcfcli.onkopus_clients.OncoKBClient(genome_version=genome_version)
    if module == 'aggregator':
        return vcfcli.onkopus_clients.AggregatorClient(genome_version=genome_version)
    if module == 'biomarker_types':
        return vcfcli.onkopus_clients.BiomarkerRecognitionClient(genome_version=genome_version)
    if module == 'drug_classification':
        return vcfcli.onkopus_clients.DrugOnClient(genome_version=genome_version)
    if module == 'all':
        return vcfcli.onkopus_clients.AllModulesClient(genome_version=genome_version)

    return None


def annotate_gene_request(
        annotated_data,gene,
        genome_version=None):
    """
    Annotates a gene with available data

    :param annotated_data:
    :param gene:
    :param genome_version:
    :return:
    """
    annotated_data[gene] = {}

    # GENCODE
    annotated_data = vcfcli.onkopus_clients.GENCODEGeneNameClient(genome_version).process_data(annotated_data)

    # CIVIC Gene
    annotated_data = vcfcli.onkopus_clients.CIViCGeneClient(genome_version).process_data(annotated_data)

    # Protein sequence
    annotated_data = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version).process_data(annotated_data)

    return annotated_data


class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return



def parallel_requests(annotated_data, genome_version):
    """
    Annotates a biomarker frame with parallelized Onkopus requests

    :param annotated_data:
    :param genome_version:
    :return:
    """
    start_time = time.time()

    task1 = vcfcli.onkopus_clients.DBSNPClient(genome_version=genome_version).process_data
    task2 = vcfcli.onkopus_clients.ClinVarClient(genome_version=genome_version).process_data
    task3 = vcfcli.onkopus_clients.REVELClient(genome_version=genome_version).process_data
    task4 = vcfcli.onkopus_clients.LoFToolClient(genome_version=genome_version).process_data
    task5 = vcfcli.onkopus_clients.VUSPredictClient(genome_version=genome_version).process_data
    task6 = vcfcli.onkopus_clients.MetaKBClient(genome_version=genome_version).process_data
    task7 = vcfcli.onkopus_clients.MVPClient(genome_version=genome_version).process_data
    task8 = vcfcli.onkopus_clients.PrimateAIClient(genome_version=genome_version).process_data
    task9 = vcfcli.onkopus_clients.DBNSFPClient(genome_version=genome_version).process_data
    #task10 = vcfcli.onkopus_clients.GENCODEClient(genome_version=genome_version).process_data
    task11 = vcfcli.onkopus_clients.GENCODEGenomicClient(genome_version=genome_version).process_data
    task12 = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version=genome_version).process_data
    task13 = vcfcli.onkopus_clients.CIViCClient(genome_version=genome_version).process_data
    task14 = vcfcli.onkopus_clients.OncoKBClient(genome_version=genome_version).process_data
    task15 = vcfcli.onkopus_clients.AlphaMissenseClient(genome_version=genome_version).process_data
    task16 = vcfcli.onkopus_clients.CCSGeneToGenomicClient(genome_version=genome_version).process_data

    t1 = ThreadWithReturnValue(target=task1, args=[annotated_data])
    t2 = ThreadWithReturnValue(target=task2, args=[annotated_data])
    t3 = ThreadWithReturnValue(target=task3, args=[annotated_data])
    t4 = ThreadWithReturnValue(target=task4, args=[annotated_data])
    t5 = ThreadWithReturnValue(target=task5, args=[annotated_data])
    t6 = ThreadWithReturnValue(target=task6, args=[annotated_data])
    t7 = ThreadWithReturnValue(target=task7, args=[annotated_data])
    t8 = ThreadWithReturnValue(target=task8, args=[annotated_data])
    t9 = ThreadWithReturnValue(target=task9, args=[annotated_data])
    #t10 = ThreadWithReturnValue(target=task10, args=[annotated_data])
    t11 = ThreadWithReturnValue(target=task11, args=[annotated_data])
    t12 = ThreadWithReturnValue(target=task12, args=[annotated_data])
    t13 = ThreadWithReturnValue(target=task13, args=[annotated_data])
    t14 = ThreadWithReturnValue(target=task14, args=[annotated_data])
    t15 = ThreadWithReturnValue(target=task15, args=[annotated_data])
    t16 = ThreadWithReturnValue(target=task16, args=[annotated_data])

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    #t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()

    data1 = t1.join()
    data2 = t2.join()
    data3 = t3.join()
    data4 = t4.join()
    data5 = t5.join()
    data6 = t6.join()
    data7 = t7.join()
    data8 = t8.join()
    data9 = t9.join()
    #data10 = t10.join()
    data11 = t11.join()
    data12 = t12.join()
    data13 = t13.join()
    data14 = t14.join()
    data15 = t15.join()
    data16 = t16.join()

    annotated_data = merge_dictionaries(annotated_data, data1)
    annotated_data = merge_dictionaries(annotated_data, data2)
    annotated_data = merge_dictionaries(annotated_data, data3)
    annotated_data = merge_dictionaries(annotated_data, data4)
    annotated_data = merge_dictionaries(annotated_data, data5)
    annotated_data = merge_dictionaries(annotated_data, data6)
    annotated_data = merge_dictionaries(annotated_data, data7)
    annotated_data = merge_dictionaries(annotated_data, data8)
    annotated_data = merge_dictionaries(annotated_data, data9)
    #annotated_data = merge_dictionaries(annotated_data, data10)
    annotated_data = merge_dictionaries(annotated_data, data11)
    annotated_data = merge_dictionaries(annotated_data, data12)
    annotated_data = merge_dictionaries(annotated_data, data13)
    annotated_data = merge_dictionaries(annotated_data, data14)
    annotated_data = merge_dictionaries(annotated_data, data15)
    annotated_data = merge_dictionaries(annotated_data, data16)

    stop_time = time.time() - start_time
    print("Time for parallel requests: ",stop_time)

    return annotated_data


def annotate_variant_data(
                          annotated_data,
                          genome_version: str = 'hg38',
                          modules=None,
                          oncokb_key='',
                          lo_hg19=None,
                          lo_hg38=None,
                          ):
    """
    Retrieves all annotation modules for a list of variants and returns an annotated JSON representation of the annotated variants

    Parameters
    ----------
    vcf_data

    Returns
    -------

    """
    if modules is None:
        modules = conf_reader.__ACTIVE_MODULES__

    if annotated_data is None:
        return {}

    if 'liftover' in config.__ACTIVE_MODULES__:
        client = vcfcli.LiftoverClient(genome_version=genome_version)
        annotated_data = client.process_data(annotated_data,lo_hg19=lo_hg19,lo_hg38=lo_hg38)

    if 'ccs' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(annotated_data)

    # Parallel requests
    annotated_data = parallel_requests(annotated_data, genome_version)

    if 'aggregator' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.AggregatorClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'biomarker_types' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.BiomarkerRecognitionClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'drug_classification' in modules:
        annotated_data = vcfcli.onkopus_clients.DrugOnClient(
            genome_version=genome_version).process_data(annotated_data)

    return annotated_data


def annotate_file_all_modules(
                              infile_str,
                              outfile_str,
                              genome_version='hg38',
                              reader_input_format=None,
                              writer_output_format=None
                              ):
    """
    Annotates a specified file and writes the annotated file in the specified output path

    :param infile_str:
    :param outfile_str:
    :param genome_version:
    :param reader_input_format:
    :param writer_output_format:
    :return:
    """
    # generate reader
    reader = vcfcli.tools.get_reader(infile_str, file_type=reader_input_format)
    writer = vcfcli.tools.get_writer(outfile_str, file_type=writer_output_format)

    json_obj = reader.read_file(infile_str)
    annotated_data = json_obj.data

    #variant_dc = vcfcli.generate_variant_dictionary(annotated_data)

    if 'ccs_liftover' in config.__ACTIVE_MODULES__:
        client = vcfcli.onkopus_clients.ccs_liftover_client.LiftOverClient(genome_version=genome_version)
        annotated_data = client.process_data(annotated_data)
    if 'ccs' in config.__ACTIVE_MODULES__:
        client = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version)
        annotated_data = client.process_data(annotated_data)
    if 'dbsnp' in config.__ACTIVE_MODULES__:
        client = vcfcli.onkopus_clients.DBSNPClient(genome_version=genome_version)
        annotated_data = client.process_data(annotated_data)
    if 'clinvar' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.ClinVarClient(genome_version=genome_version).process_data(
            annotated_data)
    if 'revel' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.revel_client.REVELClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'loftool' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.LoFToolClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'vuspredict' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.VUSPredictClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'metakb' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.MetaKBClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'mvp' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.MVPClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'primateai' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.PrimateAIClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'alphamissense' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.AlphaMissenseClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'dbnsfp' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.DBNSFPClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'gencode' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.GENCODEClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'gencode_genomic' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.GENCODEGenomicClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'uta_adapter_protein_sequence' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version=genome_version).process_data(annotated_data)
    if 'civic' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.CIViCClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'oncokb' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.OncoKBClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'aggregator' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.AggregatorClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'biomarker_types' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.BiomarkerRecognitionClient(
            genome_version=genome_version).process_data(annotated_data)
    if 'drug_classification' in config.__ACTIVE_MODULES__:
        annotated_data = vcfcli.onkopus_clients.DrugOnClient(
            genome_version=genome_version).process_data(annotated_data)

    json_obj.data = annotated_data
    writer.write_to_file(outfile_str, json_obj)


def annotate_file(infile_str, outfile_str, module, genome_version, lo_hg19=None,lo_hg38=None):
    """
    Annotates a biomarker file with an Onkopus client
    
    :param infile_str:
    :param outfile_str:
    :param module:
    :param genome_version:
    :return:
    """
    infile = open_infile(infile_str)
    outfile = open_outfile(outfile_str)

    if module == "uta":
        vcf_obj = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version)
    elif module == "uta_gene":
        vcf_obj = vcfcli.onkopus_clients.vcfcli.ccs_genomic_client.CCSGeneToGenomicClient(
                genome_version=genome_version)
    elif module == 'ccs_liftover':
        vcf_obj = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version)
    elif module == 'liftover':
        vcf_obj = vcfcli.LiftoverClient(genome_version)
    elif module == 'dbsnp':
        vcf_obj = vcfcli.onkopus_clients.DBSNPClient(genome_version=genome_version)
    elif module == "clinvar":
        vcf_obj = vcfcli.onkopus_clients.ClinVarClient(genome_version=genome_version)
    elif module == "revel":
        vcf_obj = vcfcli.onkopus_clients.REVELClient(genome_version=genome_version)
    elif module == "loftool":
        vcf_obj = vcfcli.onkopus_clients.LoFToolClient(genome_version=genome_version)
    elif module == "vuspredict":
        vcf_obj = vcfcli.onkopus_clients.VUSPredictClient(genome_version=genome_version)
    elif module == 'metakb':
        vcf_obj = vcfcli.onkopus_clients.MetaKBClient(genome_version=genome_version)
    elif module == 'mvp':
        vcf_obj = vcfcli.onkopus_clients.MVPClient(genome_version=genome_version)
    elif module == 'primateai':
        vcf_obj = vcfcli.onkopus_clients.PrimateAIClient(genome_version=genome_version)
    elif module == 'alphamissense':
        vcf_obj = vcfcli.onkopus_clients.AlphaMissenseClient(genome_version=genome_version)
    elif module == 'dbnsfp':
        vcf_obj = vcfcli.onkopus_clients.DBNSFPClient(genome_version=genome_version)
    elif module == 'gencode':
        vcf_obj = vcfcli.onkopus_clients.GENCODEClient(
                genome_version=genome_version)
    elif module == 'gencode_genomic':
        vcf_obj = vcfcli.onkopus_clients.GENCODEGenomicClient(
                genome_version=genome_version)
    elif module == 'uta_adapter_protein_sequence':
        vcf_obj = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version=genome_version)
    elif module == 'civic':
        vcf_obj = vcfcli.onkopus_clients.CIViCClient(genome_version=genome_version)
    elif module == 'oncokb':
        vcf_obj = vcfcli.onkopus_clients.OncoKBClient(genome_version=genome_version)
    elif module == 'aggregator':
        vcf_obj = vcfcli.onkopus_clients.AggregatorClient(genome_version=genome_version)
    elif module == 'biomarker_types':
        vcf_obj = vcfcli.onkopus_clients.BiomarkerRecognitionClient(genome_version=genome_version)
    elif module == 'drug_classification':
        vcf_obj  = vcfcli.onkopus_clients.DrugOnClient(genome_version=genome_version)
    elif module == 'all':
        vcf_obj = vcfcli.onkopus_clients.AllModulesClient(genome_version=genome_version)

    print("perform analysis (", module, "), infile ", infile_str, " output in ", outfile_str)
    if module == 'liftover':
        vcfcli.processing.process_files.process_file(infile_str, outfile_str, vcf_obj, genome_version=genome_version,
                                                     input_format='json',
                                                     output_format='json',
                                                     lo_hg19=lo_hg19,lo_hg38=lo_hg38)
    else:
        vcfcli.processing.process_files.process_file(infile_str, outfile_str, vcf_obj, genome_version=genome_version, input_format='json',
                          output_format='json')

    infile.close()
    outfile.close()


def annotate_file_db(variant_data,module, genome_version, lo_hg19=None, lo_hg38=None):
    """
    Annotates a biomarker file with an Onkopus client

    :param module:
    :param genome_version:
    :return:
    """

    vcf_obj = None
    if module == "UTA_Adapter":
        vcf_obj = vcfcli.onkopus_clients.UTAAdapterClient(genome_version=genome_version)
    elif module == "UTA_Adapter_gene":
        vcf_obj = vcfcli.onkopus_clients.ccs_genomic_client.CCSGeneToGenomicClient(
            genome_version=genome_version)
    elif module == 'ccs_liftover':
        vcf_obj = vcfcli.onkopus_clients.LiftOverClient(genome_version=genome_version)
    elif module == 'liftover':
        vcf_obj = vcfcli.LiftoverClient(genome_version)
    elif module == 'dbsnp':
        vcf_obj = vcfcli.onkopus_clients.DBSNPClient(genome_version=genome_version)
    elif module == "clinvar":
        vcf_obj = vcfcli.onkopus_clients.ClinVarClient(genome_version=genome_version)
    elif module == "revel":
        vcf_obj = vcfcli.onkopus_clients.REVELClient(genome_version=genome_version)
    elif module == "loftool":
        vcf_obj = vcfcli.onkopus_clients.LoFToolClient(genome_version=genome_version)
    elif module == "vus_predict":
        vcf_obj = vcfcli.onkopus_clients.VUSPredictClient(genome_version=genome_version)
    elif module == "vuspredict":
        vcf_obj = vcfcli.onkopus_clients.VUSPredictClient(genome_version=genome_version)
    elif module == 'metakb':
        vcf_obj = vcfcli.onkopus_clients.MetaKBClient(genome_version=genome_version)
    elif module == 'mvp':
        vcf_obj = vcfcli.onkopus_clients.MVPClient(genome_version=genome_version)
    elif module == 'primateai':
        vcf_obj = vcfcli.onkopus_clients.PrimateAIClient(genome_version=genome_version)
    elif module == 'alphamissense':
        vcf_obj = vcfcli.onkopus_clients.AlphaMissenseClient(genome_version=genome_version)
    elif module == 'dbnsfp':
        vcf_obj = vcfcli.onkopus_clients.DBNSFPClient(genome_version=genome_version)
    elif module == 'gencode':
        vcf_obj = vcfcli.onkopus_clients.GENCODEClient(
            genome_version=genome_version)
    elif module == 'gencode_genomic':
        vcf_obj = vcfcli.onkopus_clients.GENCODEGenomicClient(
            genome_version=genome_version)
    elif module == 'UTA_Adapter_protein_sequence':
        vcf_obj = vcfcli.onkopus_clients.UTAAdapterProteinSequenceClient(genome_version=genome_version)
    elif module == 'civic':
        vcf_obj = vcfcli.onkopus_clients.CIViCClient(genome_version=genome_version)
    elif module == 'oncokb':
        vcf_obj = vcfcli.onkopus_clients.OncoKBClient(genome_version=genome_version)
    elif module == 'onkopus_aggregator':
        vcf_obj = vcfcli.onkopus_clients.AggregatorClient(genome_version=genome_version)
    elif module == 'biomarker_types':
        vcf_obj = vcfcli.onkopus_clients.BiomarkerRecognitionClient(genome_version=genome_version)
    elif module == 'drug_classification':
        vcf_obj = vcfcli.onkopus_clients.DrugOnClient(genome_version=genome_version)
    elif module == 'all':
        vcf_obj = vcfcli.onkopus_clients.AllModulesClient(genome_version=genome_version)

    if module == 'liftover':
        variant_data = vcf_obj.process_data(variant_data,lo_hg19=lo_hg19, lo_hg38=lo_hg38)
    else:
        if vcf_obj is not None:
            variant_data = vcf_obj.process_data(variant_data)
        else:
            print("Error: No client instantiated: ",module)

    return variant_data






