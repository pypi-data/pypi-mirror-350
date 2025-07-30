import copy
import traceback
import time
import pymongo
import uuid
import adagenes
import adagenes.conf.read_config as conf_reader
import adagenes.app.app_tools

def apply_filter(raw_data, data, filter_model, filter_key, val):
    for i, dc in enumerate(raw_data):
        #print(dc)
        dc_keys = {str(item).lower(): item for item in list(dc.keys())}

        count = i
        if filter_key in dc_keys:
            key_orig = dc_keys[filter_key]
            # text filters
            if filter_model[filter_key]["type"] == "contains":
                if val in dc[key_orig]:
                    data.append(dc)
            if filter_model[filter_key]["type"] == "notContains":
                if val not in dc[key_orig]:
                    data.append(dc)
            if filter_model[filter_key]["type"] == "startsWith":
                if dc[key_orig].startswith(val):
                    data.append(dc)
            if filter_model[filter_key]["type"] == "endsWith":
                if dc[key_orig].endswith(val):
                    data.append(dc)
            if filter_model[filter_key]["type"] == "blank":
                if dc[key_orig] == "" or dc[key_orig] == ".":
                    data.append(dc)
            if filter_model[filter_key]["type"] == "notBlank":
                if dc[key_orig] != "" and dc[key_orig] != ".":
                    data.append(dc)
            # numeric filters
            elif filter_model[filter_key]["type"] == "equals":
                try:
                    if str(val) == str(dc[key_orig]):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "notEqual":
                if str(val) != str(dc[key_orig]):
                    data.append(dc)
            elif filter_model[filter_key]["type"] == "greaterThan":
                try:
                    if float(dc[key_orig]) > float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "lessThan":
                try:
                    if float(dc[key_orig]) < float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "greaterThanOrEqual":
                try:
                    if float(dc[key_orig]) >= float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "lessThanOrEqual":
                try:
                    if float(dc[key_orig]) <= float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
            elif filter_model[filter_key]["type"] == "inRange":
                try:
                    val2 = filter_model[filter_key]["filterTo"]
                    if float(val2) > float(dc[key_orig]) < float(val):
                        data.append(dc)
                except:
                    print(traceback.format_exc())
    return data

class DBConn:

    def __init__(self, file_id):
        db_name = conf_reader.__ADAGENES_DB_NAME__
        host = conf_reader.__ADAGENES_DB_SERVER__
        port = conf_reader.__ADAGENES_DB_PORT__
        self.client = self.connect_to_mongodb(host, port, db_name)
        self.db = self.client[db_name]
        self.collection = self.db[file_id]

    def close_connection(self):
        self.client.close()

    def connect_to_mongodb(self,host, port, db_name):
        print("Connect to MongoDB... ",host,": ",port)
        client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        #db = client[db_name]
        print("connected")
        return client

    def clear_collection(self,file_id):
        self.collection.drop()

    def insert_vcf(self,bframe, file_id, genome_version):

        collection = self.db[file_id]
        collection_header = self.db[file_id + '_' + 'headers']
        collection_add_cols = self.db[file_id + '_' + 'additional_columns']

        #print("add header lines ",bframe.header_lines)
        header_lines = bframe.header_lines
        collection_header.insert_one({'headers': header_lines, 'genome_version': genome_version, 'annotations': []})
        variants = []

        for i, var in enumerate(bframe.data.keys()):
            variant = bframe.data[var]

            row_number = i+1
            chrom = variant["variant_data"]["CHROM"]
            pos = variant["variant_data"]["POS"]
            ref = variant["variant_data"]["REF"]
            alt = variant["variant_data"]["ALT"]

            if "ID" in variant["variant_data"]:
                q_id = variant["variant_data"]["ID"]
            else:
                q_id = '.'

            if "QUAL" in variant["variant_data"]:
                qual = variant["variant_data"]["QUAL"]
            else:
                qual = '.'

            if "FILTER" in variant["variant_data"]:
                filter = variant["variant_data"]["FILTER"]
            else:
                filter = '.'

            #print("add variant ",variant)

            if "additional_columns" in variant:
                additional_columns = variant["additional_columns"]
                for add_col in additional_columns:
                    collection_add_cols.insert_one({add_col})

            variant_dc = {
                "row_number": row_number,
                "qid": var,
                "chrom": chrom,
                "pos": pos,
                "id": q_id,
                "ref": ref,
                "alt": alt,
                "qual": qual,
                "filter": filter
            }

            #default_columns = ["CHROM","POS","REF","ALT","ID","FILTER","QUAL",""]
            if "info_features" in variant.keys():
                for key in variant["info_features"]:
                    variant_dc[key] = variant["info_features"][key]

            # TODO: add additional columns

            #print("insert db data ",variant_dc)
            #collection.insert_one(variant)
            variants.append(variant_dc)

        if variants:
            collection.insert_many(variants)

        collection.create_index([("row_number", pymongo.ASCENDING), ("chrom", pymongo.ASCENDING)])
        #print("db data ",file_id,": ",collection[file_id])

    def update_annotations(self,file_id, annotations):
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        if "annotations" in header_lines.keys():
            lines = header_lines["annotations"] + annotations
        else:
            lines = annotations
        genome_version = header_lines["genome_version"]
        info_lines = header_lines["headers"]
        header_lines = {"headers": info_lines, 'genome_version': genome_version, 'annotations': lines}
        #print("Add new header ",header_lines)
        collection_header.drop()
        collection_header.insert_one(header_lines)

    def update_header_lines(self, file_id, info_lines):
        # update header lines
        collection_header = self.db[file_id + "_headers"]
        header_lines = collection_header.find_one()
        #print("Header lines ", header_lines)
        lines = header_lines["headers"] + info_lines
        genome_version = header_lines["genome_version"]
        header_lines = {"headers": lines, 'genome_version': genome_version}
        collection_header.drop()
        collection_header.insert_one(header_lines)

    def update_vcf(self,vcf_lines, genome_version, magic_obj):
            """

            :param bframe:
            :param file_id:
            :param annotations:
            :return:
            """
            bulk_operations = []
            for i, var in enumerate(vcf_lines.keys()):

                if hasattr(magic_obj, 'labels'):
                    labels = magic_obj.labels
                else:
                    labels = None

                annotations = adagenes.app.app_tools.generate_annotations_db(magic_obj.srv_prefix, vcf_lines[var], magic_obj.extract_keys, labels)
                #print("generated annotations ",annotations)

                #variant_raw = self.collection[var]
                filter = {"qid": var}

                # Retrieve the document
                variant_raw = self.collection.find_one(filter)

                if variant_raw:
                    #print("var data ",variant)
                    variant=variant_raw

                    # for i, dc in enumerate(variant_raw):
                    #    #print(dc)
                    #    count = i
                    #    variant = dc

                    #print("add new annotations ",annotations)
                    #print("add to dc ",variant)
                    for annotation in annotations.keys():
                        variant[annotation] = annotations[annotation]
                    #print("update db data ",variant)

                    if genome_version == "hg19":
                        if "POS_t2t" in variant.keys():
                            variant["pos"] = variant["POS_hg19"]
                    elif genome_version == "t2t":
                        if "POS_t2t" in variant.keys():
                            variant["pos"] = variant["POS_t2t"]

                    #collection.update_one(filter_criteria,variant)
                    #print("update filter criteria ",filter_criteria)
                    #result = self.collection.update_one(filter_criteria, {'$set': variant})
                else:
                    print("Variant not found ",var)

                #print("var data ",variant)
                bulk_operations.append(pymongo.UpdateOne(filter, {'$set': variant}))

            start_time = time.time()
            if bulk_operations:
                self.collection.bulk_write(bulk_operations)
            end_time = time.time()
            print("Time for updates: ",end_time - start_time)
            self.collection.create_index([("row_number", pymongo.ASCENDING), ("chrom", pymongo.ASCENDING)])

    def import_vcf(self,bframe, file_id, genome_version):
        self.collection.drop()

        self.insert_vcf(bframe, file_id, genome_version)

    def parse_info_field(self,info_str):
        info = {}
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info[key] = value
            else:
                info[item] = True
        return info

    def generate_random_file_id(self):
        return str(uuid.uuid4())

    def get_header(self,db, file_id):
        collection_header = db[file_id + "_headers"]
        header_data = collection_header.find()

        genome_version = None
        header_lines = None
        for dc_header in header_data:
            if "genome_version" in dc_header.keys():
                genome_version = dc_header["genome_version"]
            if "headers" in dc_header.keys():
                header_lines = dc_header["headers"]

        return genome_version, header_lines

    def query_vcf(
            self,
            file_id,
            filter_model=None,
            sort_model=None,
            start_row=None,
            end_row=None,
            genome_version=None) -> (list, int, list):
        collection_header = self.db[file_id + '_' + 'headers']
        header_data = collection_header.find()

        for dc_header in header_data:
            #print("HEADER LINES ",dc_header)
            if "headers" in dc_header.keys():
                header_lines = dc_header["headers"]

        raw_data = self.collection.find()

        #print("return data for ", file_id, ": ", raw_data)
        data = []
        count=0
        print("apply filter ", filter_model)

        # filter
        if not filter_model:
            for i, dc in enumerate(raw_data):
                data.append(dc)
        else:
            for filter_key in filter_model.keys():
                if "filter" in filter_model[filter_key]:
                    val = filter_model[filter_key]["filter"]
                    data = []

                    data = apply_filter(raw_data, data, filter_model, filter_key, val)
                    raw_data = copy.deepcopy(data)
                elif "conditions" in filter_model[filter_key]:
                    if filter_model[filter_key]["operator"] == "AND":
                        print("Apply and filter")
                        for condition in filter_model[filter_key]["conditions"]:
                            val = condition["filter"]
                            data = apply_filter(raw_data, data, {filter_key : condition}, filter_key, val)
                            raw_data = copy.deepcopy(data)
                            data = []
                            print("after filter ",len(raw_data)," ",len(data))
                        data = copy.deepcopy(raw_data)
                    elif filter_model[filter_key]["operator"] == "OR":
                        datasets = []
                        for condition in filter_model[filter_key]["conditions"]:
                            val = condition["filter"]
                            datasets.append(apply_filter(raw_data, data, {filter_key: condition}, filter_key, val))
                        data = []
                        for sublist in datasets:
                            data.extend(sublist)
                        raw_data = copy.deepcopy(data)

                #data_new = copy.deepcopy(data)
                #raw_data = copy.deepcopy(data)
            #data = copy.deepcopy(data_new)


        #print("Unsorted ",data)
        # sort
        if sort_model is not None:
            for sort_option in sort_model:
                if sort_option["sortable"] is True:
                    #print("sort option ",sort_option)
                    field = sort_option["field"]
                    if sort_option["sort"] is not None:
                        asc = sort_option["sort"]
                        field_orig = sort_option["headerName"]

                        if sort_option["filter"] == 'agNumberColumnFilter':
                            sorting_func = lambda x: sort_mixed_keys(x, field, field_orig)
                        else:
                            sorting_func = lambda x: sort_text(x, field, field_orig)

                        if asc == "desc":
                            reverse = True
                        elif asc == "asc":
                            reverse = False
                        data = sorted(data, reverse=reverse, key=sorting_func)

        count = len(data)
        # start and end row
        # TODO
        data_page = []
        for dc in data:
            if start_row is not None and end_row is not None:
                row = dc["row_number"]

                if genome_version is not None:
                    print("check for genome version ",genome_version,": ",dc)
                    if genome_version=="hg19" and "POS_hg19" in dc:
                        dc["pos"] = dc["POS_hg19"]
                    elif genome_version=="hg38" and "POS_hg38" in dc:
                        dc["pos"] = dc["POS_hg38"]
                    elif genome_version=="t2t" and "POS_t2t" in dc:
                        dc["pos"] = dc["POS_t2t"]

                if start_row <= row <= end_row:
                    data_page.append(dc)

            else:
                data_page.append(dc)

        #print("data page ",data_page)
        return data_page, count, header_lines

def load_bframe_from_db_data(raw_data, genome_version):
        data = {}
        orig_ids = {}
        print("load bframe from data ",genome_version)
        for i, dc in enumerate(raw_data):
            #print("dc ",dc)

            if genome_version == "hg19":
                if "POS_hg19" in dc.keys():
                    dc["pos"] = dc["POS_hg19"]
            elif genome_version == "t2t":
                if "POS_t2t" in dc.keys():
                    dc["pos"] = dc["POS_t2t"]
            elif genome_version == "hg38":
                if "POS_hg38" in dc.keys():
                    dc["pos"] = dc["POS_hg38"]

            qid_orig = dc["qid"]
            qid = "chr" + str(dc["chrom"]) + ":" + str(dc["pos"]) + str(dc["ref"]) + ">" + str(dc["alt"])
            data[qid_orig] = dc
            data[qid_orig].pop("_id")
            data[qid_orig].pop("row_number")
            data[qid_orig].pop("qid")

            orig_ids[qid_orig] = qid

        #bframe = adagenes.BiomarkerFrame(data)
        return data, orig_ids

    #data_dir = os.getenv("DATA_DIR")
    #filepath= data_dir + "/sample.vcf"
    #bframe = ag.read_file(filepath)
    #file_id = generate_random_file_id()
    #import_vcf(bframe, file_id)

    #data = query_vcf(file_id)
    #print("data ",data)

    #for dc in data:
    #    print(dc)

def sort_mixed_keys(x, field, field_orig):
    if field in x:
        key = x[field]
        if isinstance(key, int):
            return (0, key)  # Numeric values come first, sorted by their value
        else:
            return (1, key)  # Non-numeric values come after numeric values, sorted alphabetically
    elif field_orig in x:
        key = x[field_orig]
        if isinstance(key, int):
            return (0, key)  # Numeric values come first, sorted by their value
        else:
            return (1, key)  # Non-numeric values come after numeric values, sorted alphabetically
    else:
        return (2,)  # Field not present, these come last


def sort_text(x, field, field_orig):
    if field in x:
        return x[field]
    elif field_orig in x:
        return x[field_orig]
