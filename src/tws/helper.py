import csv
import os.path


def convert_to_dict(value):
    """Convert API string to csv"""
    # TODO: remove eval
    return eval(
        "dict("
        + value.replace(";;", ";")
        .replace(";", ", ")
        .replace("=", '="')
        .replace(",", '",')
        + '")'
    )


def save_dict_to_file(file_name, my_dict):
    """Saving dic to file"""
    file_exists = os.path.isfile(file_name)
    with open(file_name, "a") as f:
        w = csv.DictWriter(f, my_dict.keys())
        if not file_exists:
            w.writeheader()
        w.writerow(my_dict)


def read_csv_to_dict(file_name):
    """Read a csv file and convert to dict"""
    reader = csv.DictReader(open(file_name))
    return reader
