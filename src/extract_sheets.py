from io import StringIO
import sys
import os
import read_write as rw


def main():
    """ Extracts sheets from excel file and saves them as csv files.
    """

    text = "Started extracting sheets from the excel file"
    print(text)

    # redirect stdout to a buffer
    buffer = StringIO()
    sys.stdout = buffer

    # extract sheets
    rw.print_tstamp(text)
    # rw.create_folders()
    rw.extract_sheets(verbose=True)

    # restore stdout
    sys.stdout = sys.__stdout__

    fname = os.path.join(rw.LOGS_PATH, 'extract_sheets_log.txt')
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())
    print(f"Log saved in {fname}")


if __name__ == "__main__":
    main()
