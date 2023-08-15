import pandas as pd
import codebook as cb

# data paths
DATA_PATH = "../data/"
RAW_PATH = f"{DATA_PATH}raw/"
PROCESSED_PATH = f"{DATA_PATH}processed/"
RAW_EXTRACTED_PATH = f"{RAW_PATH}extracted/"
PROCESSSED_EXTRACTED_PATH = f"{PROCESSED_PATH}extracted/"
PROCESSSED_SUBSETS_PATH = f"{PROCESSED_PATH}subsets/"


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
    if verbose:
        print(f"Importing {filepath} ... ", end="")
    dobj = pd.ExcelFile(filepath)
    if verbose:
        print("done")

    if verbose:
        print("Datasets")
        for sheet_name in dobj.sheet_names:
            print(f"- {sheet_name}")

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

    for sheet_name in dobj.sheet_names:

        if verbose:
            print(f"Extracting {sheet_name} ... ", end="")
        df = dobj.parse(sheet_name,
                        header=header,
                        index_col=index_col,
                        na_values=['NA'])
        if verbose:
            print("done")

        filepath = f"{outpath}{sheet_name}.csv"
        if verbose:
            print(f"Writing {filepath} ... ", end="")
        df.to_csv(filepath, index=False)
        if verbose:
            print("done")


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
