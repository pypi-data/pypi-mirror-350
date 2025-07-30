import subprocess
import datetime
import onkopus as op
import adagenes as ag
from adagenes.app.io import find_newest_file, load_log_actions, append_to_file, split_filename
import adagenes.conf
import os
import json # for parsing the dict data
import multiprocessing
import adagenes.app.tools

expected_n_files_dict = {} # global variable

def modify_global_expected_n_files_dict(key, value):
    '''
    modify the global variable expected_n_files_dict- add a key key with value value in the expected_n_files_dict
    '''
    global expected_n_files_dict  # Declare that we are using the global variable
    expected_n_files_dict[key] = value  # Modify the global variable

def update_file(key, value):
    data_dir = adagenes.conf.read_config.__DATA_DIR__
    file_path = data_dir + "/dict.json"
    with open(file_path, "r") as data:
        dictionary = json.load(data)
    dictionary[key]= value
    print(dictionary)
    with open(file_path, "w") as file:
        json.dump(dictionary, file, indent=4)



def get_magic_obj(key, genome_version, transform_model = None):
    if key == "clinvar":
        return op.ClinVarClient(genome_version=genome_version)
    elif key == 'protein':
        return op.UTAAdapterClient(genome_version=genome_version)
    elif key == 'protein-to-gene':
        return op.CCSGeneToGenomicClient(genome_version=genome_version)
    elif key == 'transcripts':
        return op.GENCODEGenomicClient(genome_version=genome_version)
    elif key == 'dbsnp':
        return op.DBSNPClient(genome_version=genome_version)
    elif key == 'patho':
        return op.DBNSFPClient(genome_version=genome_version)
    elif key == 'molecular':
        return op.MolecularFeaturesClient(genome_version=genome_version)
    elif key == 'proteinfeatures':
        return op.ProteinFeatureClient(genome_version=genome_version)
    elif key == 'geneexpression':
        return op.GeneExpressionClient()
    elif key == 'proteinseq':
        return op.UTAAdapterProteinSequenceClient(genome_version=genome_version)
    elif key == 'functionalregions':
        return op.GENCODEGenomicClient(genome_version=genome_version)
    elif key == 'drug-gene-interactions':
        return op.DGIdbClient(genome_version=genome_version)
    elif key == 'clinical-evidence':
        return op.ClinSigClient(genome_version=genome_version)
    elif key == 'filter_text':
        return ag.TextFilter()
    elif key == 'filter_number':
        return ag.NumberFilter()
    elif key == 'hgvs':
        return ag.HGVSClient(genome_version=genome_version)
    elif key == 'transform-vcf':
        return ag.VCFTransformator(transform_model)
    else:
        return None


def annotate_qid(qid: str, annotations: dict, genome_version=None, data_dir=None,
                 output_format='vcf',
                 mapping=None):
    """
    Annotate variant data with selected filters, and stores the annotated data in a new file

    :param qid:
    :param annotations: Dictionary containing annotations as keys and true if the annotation should be performed, e.g. { 'clinvar' true, 'protein': true }
    :param genome_version:
    :param data_dir:
    :param output_format:
    :return:
    """

    annotation_requirements = {
        "transcripts": ["protein"]
    }

    print("Annotations ",annotations)
    print(qid)
    print(data_dir)
    if data_dir is None:
        data_dir = adagenes.conf.read_config.__DATA_DIR__
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    for key in annotations.keys():
        if annotations[key]:
            print("Annotate: ", key, " ", qid)


            infile = find_newest_file(data_dir)
            if qid == "sample-vcf": # TO DO : this should not work - with multiple annotations there should be problems?
                infile= data_dir + ag.conf_reader.sample_file
            if qid == "sample-protein":
                infile= data_dir + ag.conf_reader.sample_protein_file

            #infile = split_filename(infile)
            infile_name = split_filename(infile)

            previous_actions = load_log_actions(logfile)
            print("loaded logfile ",logfile)
            print("previous actions: ",previous_actions)

            annotation_key = 'Annotation:'+key
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            if contains_substring is False:
                datetime_str = str(datetime.datetime.now())
                print("infile ",infile)
                output_format = output_format.lstrip(".")
                outfile = infile_name + ".ann."  + datetime_str + "." + output_format
                outfile = outfile.replace(" ", "_")
                outfile = outfile.replace(":", "-")

                magic_obj = get_magic_obj(key, genome_version)
                print("annotate with magic obj ",magic_obj, " mapping ",mapping)
                ag.process_file(infile, outfile, magic_obj, mapping=mapping)

                append_to_file(logfile, annotation_key + "(" + datetime_str + ")::" + outfile + '\n')

                print("File annotated: ",outfile)
            else:
                print("Annotation already found: ",annotation_key)


    # Generate new column definitions:
    #, cellClass: "rag-blue"


def build_file_name(base_name, annotation, file_count):
    return f"{base_name}_{annotation}_{file_count}.vcf"

def split_large_file(input_file, base_name, stage_name, lines_per_file=2500):
    """
    Splits a large file into multiple smaller files, each containing a specified number of lines - less than lines_per_file

    :param input_file: Path to the input file.
    :param base_name: Base name base don the input_file name
    :param stage_name: Name of the stage, ususally "start"
    :param lines_per_file: Number of lines per output file (default is 2500).

    return the names of the small files
    """
    output_files = []
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            file_count = 1
            lines = []

            for line in infile:
                lines.append(line)
                if len(lines) >= lines_per_file:
                    output_file = build_file_name(base_name, stage_name, file_count)
                    with open(output_file, 'w', encoding='utf-8') as outfile:
                        outfile.writelines(lines)
                    print(f"Created {output_file}")
                    file_count += 1
                    lines = []
                    output_files.append(output_file)

            # Write remaining lines if any
            if len(lines) > 0:
                output_file = build_file_name(base_name, stage_name, file_count)
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(lines)
                print(f"Created {output_file}")
                output_files.append(output_file)
            else:
                # reduce the number of files for 1, so that the file_count is how many new files were made
                file_count = file_count -1
        return output_files, file_count
    except Exception as e:
        print(f"Error: {e}")

def needed_annotations(annotations, logfile):
    '''
    For a annotation dictionary: remove the annotation keys of the annotations that were already done
    TO DO: this function could be probably cleaned? When is false in dict?
    '''

    previous_actions = load_log_actions(logfile)
    print("loaded logfile ", logfile)
    print("previous actions: ", previous_actions)

    new_annotations = {}
    for key in annotations.keys():
        if annotations[key]:
            annotation_key = 'Annotation:' + key
            contains_substring = any(annotation_key in entry for entry in previous_actions)
            if contains_substring is False:
                new_annotations[key] = True
            else:
                print("Annotation already found: ", annotation_key)
    return new_annotations

def merge_files(outfile, n_chunks, last_step, base_name):
    """
    Merges multiple small files back into a single file.

    :param outfile: Path to the merged file at the ned
    :param n_chunks: Number of chunks, which were processed with all annotations
    :param last_step: the name of the last step - which word is used in the naming of the  output files
    :param base_name: the base name of the original file
    """
    print(outfile, n_chunks, last_step, base_name)
    try:
        with open(outfile, 'w', encoding='utf-8') as outfile:
            for n in range(1, n_chunks+1):
                file_name = build_file_name(base_name, last_step, n)
                with open(file_name, 'r', encoding='utf-8') as infile:
                    outfile.writelines(infile.readlines())
        print(f"Merged files into {outfile}")
    except Exception as e:
        print(f"Error while merging files: {e}")

def get_base_file_name(infile):
    if ".vcf" in infile:
        original_name = "".join(infile.split(".")[:-1])
    else:
        original_name = infile
    return original_name

def get_annotation_steps(annotations, start = "start"):
    '''
    Order the annotation keys  the first should be start, then protein (SeqCAT) - if it is inside
    TO DO: SeqCAt should be added in some cases?
    Args:
        annotations: dictionary with annotation names as keys
        start: the name of the starting phase - how the chunks of input file are named

    Returns:

    '''
    annotation_stages = [start]
    if "protein" in annotations:
        annotation_stages.append("protein")
        del annotations["protein"]
    annotation_stages = annotation_stages+ list(annotations.keys())
    print("Ordered annotation stages", annotation_stages)
    return annotation_stages

def annotate_one_file(annotation_key, genome_version, mapping, original_name, number, prev_step):
    '''
    Calculate the name of the input file and then process it with the service named "annotation_key" and save the result in the calculated outfiel
    Args:
        annotation_key: annotation key - which annotation should be done
        genome_version:
        mapping:
        original_name: original name of the input file - without .vcf at the end
        number: the "chunk" number - which ofthe chunks should be used?
        prev_step: which step was beforehand? it should be "start" or the name of the previous annotation
    '''

    input_file = build_file_name(original_name, prev_step, number)
    outfile = build_file_name(original_name, annotation_key, number) # original_name + "_" + annotation_key + "_" + number + ".vcf"

    magic_obj = get_magic_obj(annotation_key, genome_version)
    #print("annotate with magic obj ", magic_obj, " mapping ", mapping)
    ag.process_file(input_file, outfile, magic_obj, mapping=mapping)

    print("file_number", number, "with annotation", annotation_key, "File annotated: ", outfile)

def execute_annotations_for_file(number, steps, genome_version, mapping, original_name):
    '''
    Args:
        pool:
        number: number of the file chunk - identifier for input and output file
        steps:
        genome_version:
        mapping:
        n_step:
        original_name:

    Returns:

    '''
    for n_step in range(1, len(steps)):
          annotate_one_file(steps[n_step], genome_version, mapping, original_name, number, steps[n_step-1])


def generate_outfile_name(infile_name):
    infile_name = infile_name.replace("_processed", "")
    outfile_name = infile_name + "_processed.vcf"
    new_file_name = adagenes.app.tools.increment_file_number(outfile_name, increase_count=True)
    return new_file_name

def annotate_qid_chunks_parallel(qid: str, annotations: dict, genome_version=None, data_dir=None,
                 output_format='vcf',
                 mapping=None, lines_per_file = 2500):
    """
    Annotate variant data with selected filters, and stores the annotated data in a new file
        - with splitting the file in smaller files
    :param qid:
    :param annotations: Dictionary containing annotations as keys and true if the annotation should be performed, e.g. { 'clinvar' true, 'protein': true }
    :param genome_version:
    :param data_dir:
    :param output_format:
    :return:
    """

    annotation_requirements = {
        "transcripts": ["protein"]
    }

    print("Annotations ",annotations)
    print(qid)
    print(data_dir)
    if data_dir is None:
        data_dir = adagenes.conf.read_config.__DATA_DIR__
    data_dir = data_dir + "/" + qid
    logfile = data_dir + '/log.txt'

    # input_file is the file that was changed the last in the data_dir
    infile = find_newest_file(data_dir)
    print("Newest file ",infile)
    if qid == "sample-vcf": # TO DO check if it can be deleted
        infile = data_dir + ag.conf_reader.sample_file
    if qid == "sample-protein":
        infile = data_dir + ag.conf_reader.sample_protein_file

    # get the current number of files in the directory
    starting_n_of_files = len([name for name in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, name))])

    # take care of the naming of temp files
    original_name= get_base_file_name(infile)

    # split file in chunks
    # the files will be kept in chunks and processed in every chunk, then afterwards the files will be combined
    # the files are named like: [original_name_might_have_underscores]_[start/annotation_key]_[chunk_part].vcf
    files_names, file_count = split_large_file(infile, original_name, "start", lines_per_file=lines_per_file)

    # clean the annotations - delete the entries that have the value false
    new_annotations = needed_annotations(annotations, logfile)
    print("Needed annotations: ", new_annotations)

    # prepare the dictionary: to get the name of the outputfile for the input file

    # calculate the expected number of files
    expected_n_files = file_count * (len(new_annotations.keys())+1) + starting_n_of_files + 1  # +1: output file
    modify_global_expected_n_files_dict(qid, expected_n_files)
    update_file(qid, expected_n_files)
    print(expected_n_files_dict)

    # organise annotations in the ordered list, first is "start", then annotations follow
    steps = get_annotation_steps(new_annotations, start = "start")

    # process the files with annotations with parellel executions across different files, but sequential executing for annotations for one file
    with multiprocessing.Pool() as pool:
        pool.starmap(execute_annotations_for_file, [(n, steps, genome_version, mapping, original_name) for n in range(1, file_count +1)])

    # collect the files together again
    # TO DO: get the names of the output files! - in the correct order!
    outfile_name =  generate_outfile_name(original_name)
    merge_files(outfile_name, file_count, steps[-1], original_name)

    # add information about processing to the log file
    datetime_str = str(datetime.datetime.now())
    #append_to_file(logfile, "Annotation:" + ",Annnotation:".join(annotations.keys()) + qid + "(" + datetime_str + ")::" + outfile_name + '\n')
    append_to_file(logfile, "Annotation:" + ",Annotation:".join(
        annotations.keys()) + "(" + datetime_str + ")::" + outfile_name + '\n')

    # update annotations file
    anno_file = data_dir + "/annotations.txt"

    ## increment file number
    #most_annotated_file = adagenes.app.io.find_newest_file(data_dir, filter=False)
    #print("Update annotated file name: ", most_annotated_file)
    #symlink_file = adagenes.app.tools.update_filename_with_current_datetime(most_annotated_file, action="processed",
    #                                                                        increase_count=True)
    #cmd = ["ln", "-sv", most_annotated_file, symlink_file]
    # print(cmd)
    #subprocess.run(cmd)


