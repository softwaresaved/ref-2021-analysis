import argparse
import os
import pandas as pd
from io import StringIO
import sys
import read_write as rw


def extract_sheet(fname, sname, header, index_col=None):
    """ Extract a sheet from an excel file and save it as csv file.

    Args:
        fname (str): Filename of the Excel file.
        sname (str): Name of the sheet to extract from the Excel file.
        header (int): Row number to use as the column names.
        index_col (int): Column number to use as the row labels.
    """

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    sys.stdout = buffer

    # read the excel file
    # -------------------
    fpath = fname
    dobj = pd.ExcelFile(os.path.join(rw.PROJECT_PATH, fpath))
    rw.print_tstamp(f"READ '{fpath}'")

    # parse sheet
    # -----------
    dset = dobj.parse(sname,
                      header=header,
                      index_col=index_col
                      )
    rw.print_tstamp(f"EXTRACTED '{sname}' sheet: {dset.shape[0]} records")

    # save dset to compressed csv
    # ---------------------------
    fpath = os.path.join(rw.PROCESSED_PATH, f"{sname}{rw.DATA_EXT}")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fpath),
                index=False,
                compression='gzip')
    rw.print_tstamp(f"SAVED '{sname}' sheet to '{fpath}'")

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    # save the log file
    # -----------------
    fname = f"{rw.LOG_EXTRACT}{sname}{rw.LOG_EXT}"
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

    parser.add_argument("-hr", "--headerrow",
                        required=True,
                        help="row number to use as the column names")

    args = parser.parse_args()

    extract_sheet(args.filename, args.sheetname, int(args.headerrow))
