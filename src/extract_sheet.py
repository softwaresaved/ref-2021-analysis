import argparse
import os
import pandas as pd
from io import StringIO
import sys
import read_write as rw


def extract_sheet(fname, sname, header=4, index_col=None):
    """ Extract a sheet from an excel file and save it as csv file.

    Args:
        fname (str): Filename of the Excel file.
        sname (str): Name of the sheet to extract from the Excel file.
        header (int): Row number to use as the column names.
        index_col (int): Column number to use as the row labels.
    """

    # redirect stdout to a buffer
    buffer = StringIO()
    sys.stdout = buffer

    # read file, extract sheet and save as csv
    rw.print_tstamp(f"Started extracting {sname} from {fname}")
    fpath = fname
    dobj = pd.ExcelFile(os.path.join(rw.PROJECT_PATH, fpath))
    rw.print_tstamp(f"Imported {fpath}")
    dset = dobj.parse(sname,
                      header=header,
                      index_col=index_col,
                      na_values=['NA'])
    rw.print_tstamp(f"Extracted {sname} sheet")
    fpath = os.path.join(rw.PROCESSED_EXTRACTED_PATH, f"{sname}.csv")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fpath),
                index=False)
    rw.print_tstamp(f"Saved {sname} sheet to {fpath}")

    # restore stdout
    sys.stdout = sys.__stdout__

    fname = os.path.join(rw.LOGS_PATH, f"extract_{sname}.log")
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts a sheet from an excel file and saves it as csv file."
        )

    parser.add_argument("-f", "--filename",
                        required=True,
                        help="name of the excel file")

    parser.add_argument("-s", "--sheetname",
                        required=True,
                        help="name of the sheet to extract from the excel file")

    args = parser.parse_args()

    extract_sheet(args.filename, args.sheetname)
