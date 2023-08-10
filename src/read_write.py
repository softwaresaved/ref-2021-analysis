import pandas as pd

DATA_PATH = "../data/"
RAW_PATH = f"{DATA_PATH}raw/"
RAW_EXTRACTED_PATH = f"{RAW_PATH}extracted/"
PROCESSED_PATH = "{DATA_PATH}processed/"


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
