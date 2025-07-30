import traceback


def merge_dictionaries(a, b, path=None):
    """
    Merges dictionary b into dictionary a without data loss. C

    :param a:
    :param b:
    :param path:
    :return:
    """
    if path is None:
        path = []
    try:
        if isinstance(b,str):
            print("Cannot merge data dictionary with str: ",b)
        else:
            for key in b:
                if key in a:
                    if isinstance(a[key], dict) and isinstance(b[key], dict):
                        merge_dictionaries(a[key], b[key], path + [str(key)])
                    elif a[key] == b[key]:
                        pass # same leaf value
                    else:
                        if isinstance(a[key], list) and isinstance(b[key], list):
                            a[key] = a[key] + b[key] # concatenate lists
                        else:
                            a[key] = a[key]
                            #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                else:
                    try:
                        if isinstance(b[key], dict):
                            a[key] = b[key]
                        elif isinstance(b[key], list):
                            a[key] = b[key]
                    except:
                        print("Error merge dictionaries for ",key)
    except:
        print(traceback.format_exc())
    return a


def sort_biomarker_frame_according_to_position(bframe, positions):
    """
    Sorts a biomarker frame according to the positions given in a dictionary, where the keys are the biomarker identifiers and the values the requested position

    :param bframe:
    :param positions:
    :return:
    """
    sorted_positions = dict(sorted(positions.items(), key=lambda item: item[1], reverse=False))
    bframe_new = {}
    for biomarker in sorted_positions.keys():
        bframe_new[biomarker] = bframe[biomarker]
        if "variant_data" not in bframe_new[biomarker]:
            bframe_new[biomarker]["variant_data"] = {}
        bframe_new[biomarker]["variant_data"]["file_pos"] = positions[biomarker]

    #bframe_new[biomarker] = [bframe[biomarker] for biomarker in sorted_positions.keys()]
    return bframe_new
