import os
import datetime
import pandas as pd
import codebook as cb

# data paths
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOGS_PATH = "logs/"
DATA_PATH = "data/"
RAW_PATH = os.path.join(DATA_PATH, "raw/")
PROCESSED_PATH = os.path.join(DATA_PATH, "processed/")
RAW_EXTRACTED_PATH = os.path.join(RAW_PATH, "extracted/")
PROCESSSED_EXTRACTED_PATH = os.path.join(PROCESSED_PATH, "extracted/")
PROCESSSED_SUBSETS_PATH = os.path.join(PROCESSED_PATH, "subsets/")


def print_tstamp(text):
    """ Print a timestamped message.

    Args:
        text (str): The message to print.
    """

    now = datetime.datetime.now()
    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} {text}")


def create_folders():
    """ Create the data folders if they do not exist.
    """

    for path in [LOGS_PATH, RAW_EXTRACTED_PATH,
                 PROCESSSED_EXTRACTED_PATH, PROCESSSED_SUBSETS_PATH]:
        if not os.path.exists(path):
            print_tstamp(f"Creating folder {path}")
            os.makedirs(os.path.join(PROJECT_PATH, path))


def import_excel(fname="REF-2021-Submissions-All-2022-07-27.xlsx",
                 path=RAW_PATH,
                 verbose=False):
    """ Import the REF 2021 results Excel file.

    Args:
        fname (str): Filename of the Excel file.
        path (str): Path to the Excel file.
        verbose (bool): Whether to print additional information.

    Returns:
        dobj (pandas.ExcelFile): The Excel file object.
    """

    filepath = f"{path}{fname}"
    dobj = None
    dobj = pd.ExcelFile(os.path.join(PROJECT_PATH, filepath))
    if verbose:
        print_tstamp(f"Imported {filepath}")

        print("\nAvailable datasets")
        for sheet_name in dobj.sheet_names:
            print(f"- {sheet_name}")
        print()

    return dobj


def extract_sheets(fname="REF-2021-Submissions-All-2022-07-27.xlsx",
                   inpath=RAW_PATH,
                   outpath=RAW_EXTRACTED_PATH,
                   header=4,
                   index_col=None,
                   verbose=False):
    """ Extract the sheets from the REF 2021 results Excel file.

    Args:
        fname (str): Filename of the Excel file.
        path (str): Path to the Excel file.
        verbose (bool): Whether to print additional information.
    """
    dobj = import_excel(fname, inpath, verbose=verbose)

    for sname in dobj.sheet_names:

        df = dobj.parse(sname,
                        header=header,
                        index_col=index_col,
                        na_values=['NA'])

        fpath = f"{outpath}{sname}.csv"
        df.to_csv(os.path.join(PROJECT_PATH, fpath),
                  index=False)
        if verbose:
            print_tstamp(f"Extracted {sname} and saved to {fpath}")


def validate_table(dset, verbose=False):
    """ Validate a table using panel against the panel and uoa names.

    Args:
        dset (pandas.DataFrame): The dataset to validate.
        verbose (bool): Whether to print additional information.

    Returns:
        validated (bool): Whether the dataset is validated.
        errors (list): List of errors.
    """

    # get counts of unique values
    n_uoa_numbers = dset[cb.COL_UOA_NUMBER].nunique()
    n_uoa_names = dset[cb.COL_UOA_NAME].nunique()
    n_inst_codes = dset[cb.COL_INST_CODE].nunique()
    n_inst_names = dset[cb.COL_INST_NAME].nunique()

    # simple validation
    validated = True
    errors = []
    if n_inst_codes != n_inst_names:
        errors.append(
            f"number of institution codes ({n_inst_codes}) "
            f"does not match number of institution names ({n_inst_names})"
        )
        validated = False
    if n_uoa_numbers != n_uoa_names:
        errors.append(
            f"number of UOA codes ({n_uoa_numbers}) "
            f"does not match number of UOA names ({n_uoa_names})"
        )
        validated = False

    print(f"Data validated : {validated}")
    if not validated:
        print("ERRORS:")
        for error in errors:
            print(f"- {error}")

    return (validated, errors)
