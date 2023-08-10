import pandas as pd


def import_excel(path="../data/raw/REF-2021-Submissions-All-2022-07-27.xlsx",
                 verbose=False):
    """ Import the REF 2021 results Excel file.
    Args:
        path (str): path to the Excel file,
             default '../data/raw/REF-2021-Results-All-2022-05-06.xlsx'
        verbose (bool): default False
    Returns:
        dobj (pd.ExcelFile): Excel file object
    """

    dobj = pd.ExcelFile(path)

    if verbose:
        print(f"Imported {path}")
        print("Datasets")
        for sheet_name in dobj.sheet_names:
            print(f"- {sheet_name}")

    return dobj
