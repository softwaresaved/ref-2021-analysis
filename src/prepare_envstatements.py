""" Prepares the extracted environment statements. """
import argparse
from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import preprocess as pp
import logs as lg

TO_DELETE_HEADERS = [
    "Institutional level environment template (REF5a)",
    "Unit-level environment template (REF5b)"
]

TO_DELETE_PAGES = [
    "Page 1", "Page 2", "Page 3", "Page 4", "Page 5",
    "Page 6", "Page 7", "Page 8", "Page 9", "Page 10",
    "Page 11", "Page 12", "Page 13", "Page 14", "Page 15",
    "Page 16", "Page 17", "Page 18", "Page 19", "Page 20",
    "Page 21", "Page 22", "Page 23", "Page 24", "Page 25",
    "Page 26", "Page 27", "Page 28", "Page 29", "Page 30",
    "Page 31", "Page 32", "Page 33", "Page 34", "Page 35",
    "Page 36", "Page 37", "Page 38", "Page 39", "Page 40",
]

TO_DELETE_CHARS = ['\n', '\t']


def clean_content(content):
    """ Cleans the content of the environment statement. 
    
    Args:

        content (str): the content of the environment statement

    Returns:
    
            str: the cleaned content
    """

    # delete headers
    for item in TO_DELETE_HEADERS:
        content = '\n'.join(line for line in content.splitlines() if item not in line)

    # delete the page numbers
    for item in TO_DELETE_PAGES:
        content = '\n'.join(line for line in content.splitlines() if line.strip() != item)

    # delete the empty lines
    content = '\n'.join(line for line in content.split('\n') if line.strip())

    # specified characters to delete
    for item in TO_DELETE_CHARS:
        content = content.replace(item, " ")

    return content


def prepare_institution_statements(prefix="Institution environment statement - ", extension=".txt"):

    lg.print_tstamp("PPROC actions for organization envinroment statements")
    inputpath = os.path.join(rw.PROCESSED_ENV_EXTRACTED_PATH, "institution")
    outputpath = rw.PROCESSED_ENV_PREPARED_PATH
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, inputpath))
    lg.print_tstamp(f"- '{inputpath}' statements: {len(fnames)}")
    fnames = [fname.replace(prefix, "").replace(extension, "") for fname in fnames]

    dset = pd.DataFrame()
    for fname in fnames:
        institution_name = fname
        infname = os.path.join(inputpath, f"{prefix}{fname}{extension}")
        
        with open(infname, 'r+') as file:
            content = file.read()
            content = clean_content(content)
        dset = pd.concat([dset,
                          pd.DataFrame({cb.COL_INST_NAME: [institution_name],
                                        cb.COL_ENV_STATEMENT: [content]}
                                       )],
                         ignore_index=True)
    lg.print_tstamp(f"- aggregated {dset.shape[0]} statements")
    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         "EnvStatementsInstitutionLevel.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.to_csv(fname, index=False,
                compression='gzip')


def prepare_unit_statements(prefix="Unit environment statement - ", extension=".txt"):

    lg.print_tstamp("PPROC actions for unit envinroment statements")
    inputpath = os.path.join(rw.PROCESSED_ENV_EXTRACTED_PATH, "unit")
    outputpath = rw.PROCESSED_ENV_PREPARED_PATH
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, inputpath))
    lg.print_tstamp(f"- '{inputpath}' statements: {len(fnames)}")
    fnames = [fname.replace(prefix, "").replace(extension, "") for fname in fnames]

    dset = pd.DataFrame()
    for fname in fnames:
        institution_name, unit_code = fname.split(" - ")
        # strip any alphabetical characters from the unit code
        unit_code = ''.join([i for i in unit_code if not i.isalpha()])

        infname = os.path.join(inputpath, f"{prefix}{fname}{extension}")

        with open(infname, 'r+') as file:
            content = file.read()
            content = clean_content(content)
        dset = pd.concat([dset,
                          pd.DataFrame({cb.COL_INST_NAME: [institution_name],
                                        cb.COL_UOA_NAME: [cb.UOA_NAMES[int(unit_code)]],
                                        cb.COL_ENV_STATEMENT: [content]}
                                       )],
                         ignore_index=True)
    lg.print_tstamp(f"- aggregated {dset.shape[0]} statements")

    fname_root = "EnvStatementsUnitLevel"
    # save all the statements to a single csv file
    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         f"{fname_root}.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.to_csv(fname, index=False,
                                     compression='gzip')

    # split the DataFrame in four and save them to separate CSV files
    quarter_index = len(dset) // 4
    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         f"{fname_root}_1.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.iloc[:quarter_index].to_csv(fname, index=False,
                                     compression='gzip')

    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         f"{fname_root}_2.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.iloc[quarter_index:2*quarter_index].to_csv(fname, index=False,
                                                    compression='gzip')

    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         f"{fname_root}_3.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.iloc[2*quarter_index:3*quarter_index].to_csv(fname, index=False,
                                                      compression='gzip')

    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         f"{fname_root}_4.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.iloc[3*quarter_index:].to_csv(fname, index=False,
                                       compression='gzip')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepares the extracted environment statements and saves them as csv file."
        )

    parser.add_argument("-e", "--envname",
                        required=True,
                        help="type of statements to prepare")

    args = parser.parse_args()
    ename = args.envname

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    sys.stdout = buffer

    if ename == "institution":
        logfname = f"{rw.LOG_PREPARE_ENV_INSTITUTION}"
        prepare_institution_statements()
    elif ename == "unit":
        logfname = f"{rw.LOG_PREPARE_ENV_UNIT}"
        prepare_unit_statements()

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    print(buffer.getvalue())

    # save the log file
    # -----------------
    with open(os.path.join(rw.PROJECT_PATH, logfname), 'w') as f:
        f.write(buffer.getvalue())
