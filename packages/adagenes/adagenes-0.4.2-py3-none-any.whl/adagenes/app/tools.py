import re, datetime, os

def delete_files_with_higher_number(directory, infile):
    # Regular expression to match the number at the beginning of the filename
    pattern = re.compile(r'^(\d+)_')

    # Extract the number from the reference file path
    reference_filename = os.path.basename(infile)
    match = pattern.match(reference_filename)
    if not match:
        print(f"Error: The reference file '{infile}' does not match the expected pattern.")
        return

    threshold_number = int(match.group(1))

    if threshold_number >= 2:

        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                # Extract the number from the filename
                file_number = int(match.group(1))
                if file_number > threshold_number:
                    # Construct the full file path
                    file_path = os.path.join(directory, filename)
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                elif file_number == threshold_number:
                    if "processed" not in filename:
                        file_path = os.path.join(directory, filename)
                        # Delete the file
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")

def increment_file_number(file_path, increase_count=True):
    # Split the file path into directory and filename
    directory, filename = os.path.split(file_path)

    # Define the regular expression pattern to match the number at the beginning of the filename
    pattern = r'^(\d+)_'

    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    print("increase file number ", filename)

    if match:
        # Extract the number and the rest of the filename
        number = int(match.group(1))
        rest_of_filename = filename[match.end():]

        # Increment the number
        if increase_count is True:
            new_number = number + 1
        else:
            new_number = number

        # Construct the new filename
        new_filename = f"{new_number}_{rest_of_filename}"

        # Reconstruct the full file path with the new filename
        new_file_path = os.path.join(directory, new_filename)
        return new_file_path
    else:
        # If no number is found, return the original file path
        print("Could not find file number")
        return file_path



def update_filename_with_current_datetime(file_name, action="sort", datetime_str=None, increase_count=True):
    print("Update file name ",file_name)

    if (file_name.endswith("_processed.vcf")) and (action != "processed"):
        file_name = file_name.replace("_processed.vcf", ".vcf")

    # Regular expression to match the timestamp in the filename
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})')
    #pattern = re.compile("[0-9]+-[0-9]+-[0-9]_[0-9]+-[0-9]+")
    match = pattern.search(file_name)

    if datetime_str is None:
        current_datetime = datetime.datetime.now()
        #datetime_str = str(datetime.datetime.now())
        #datetime_str = datetime.datetime.now()
        #datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
        datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')#[:-3]

    datetime_found = False
    if match:
        # Get the current datetime and format it
        current_datetime = datetime.datetime.now()
        #current_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
        current_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        # Replace the old timestamp with the current datetime
        new_file_name = pattern.sub(current_datetime, file_name)
        datetime_found = True
    else:
        new_file_name = file_name

    # outfile = infile_name.strip() + ".sort." + datetime_str + "." + output_format
    new_file_name = new_file_name.replace(" ", "_")
    new_file_name = new_file_name.replace(":", "-")

    if datetime_found is False:
        new_file_name = new_file_name.replace(".vcf","")
        new_file_name += '_' + datetime_str
        new_file_name += ".vcf"

    if action == "sort":
        new_file_name = new_file_name.replace("_processed", "_sort")
        new_file_name = new_file_name.replace("_filter", "_sort")
        if "_sort" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "sort"
            new_file_name += ".vcf"
    elif action == "filter":
        new_file_name = new_file_name.replace("_processed", "_sort")
        new_file_name = new_file_name.replace("_sort", "_filter")
        if "_filter" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "filter"
            new_file_name += ".vcf"
    elif action == "processed":
        new_file_name = new_file_name.replace("_filter", "_processed")
        new_file_name = new_file_name.replace("_sort", "_processed")
        if "_processed" not in new_file_name:
            new_file_name = new_file_name.replace(".vcf", "")
            new_file_name += '_' + "processed"
            new_file_name += ".vcf"

    #elif action == "processed":
    #    new_file_name = new_file_name.replace("_processed", "_sort")
    #    new_file_name = new_file_name.replace("_processed", "_sort")

    # increase file count
    new_file_name = increment_file_number(new_file_name, increase_count=increase_count)
    print("increased file name ",new_file_name)

    return new_file_name