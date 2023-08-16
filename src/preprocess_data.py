from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import preprocess as pp


def preprocess_outputs():
    """ Preprocess the data from the Outputs sheet
    """
    sname = "Outputs"
    fname = os.path.join(rw.RAW_EXTRACTED_PATH, f"{sname}.csv")
    dset = pd.read_csv(os.path.join(rw.PROJECT_PATH, fname),
                       index_col=None,
                       dtype={0: str})
    rw.print_tstamp(f"Read {fname}: {dset.shape[0]} records")

    # pre-processing
    # --------------
    rw.print_tstamp("Preprocessing actions")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(cb.OUTPUT_TYPE_NAMES)
    rw.print_tstamp("- add columns for panel and output types names")

    # save pre-processed data
    # -----------------------
    fname = os.path.join(rw.PROCESSSED_EXTRACTED_PATH, f"{sname}_pprocessed.csv")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fname))
    rw.print_tstamp(f"Saved pre-processed dataset to {fname}")

    # select and save software outputs
    target_output_type = "Software"
    fsuffix = f"{target_output_type.lower()}"
    fname = os.path.join(rw.PROCESSSED_SUBSETS_PATH, f"{sname}_{fsuffix}.csv")
    dset[dset[cb.COL_OUTPUT_TYPE_NAME] == target_output_type].to_csv(os.path.join(rw.PROJECT_PATH,
                                                                     fname))
    rw.print_tstamp(f"Saved '{fsuffix}' subset to {fname}")


def preprocess_impacts():
    """ Preprocess the data from the ImpactCaseStudies sheet
    """
    sname = "ImpactCaseStudies"
    fname = os.path.join(rw.RAW_EXTRACTED_PATH, f"{sname}.csv")
    dset = pd.read_csv(os.path.join(rw.PROJECT_PATH, fname),
                       index_col=None,
                       dtype={0: str})
    rw.print_tstamp(f"Read {fname}: {dset.shape[0]} records")

    # pre-processing
    # --------------
    rw.print_tstamp("Preprocessing actions")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # shift columns from title to the left
    columns = dset.columns.tolist()
    dset = dset.drop(cb.COL_IMPACT_TITLE, axis=1)
    dset.columns = columns[:-1]
    # replace markdown in summary column
    for column in [cb.COL_IMPACT_SUMMARY,
                   cb.COL_IMPACT_UNDERPIN_RESEARCH,
                   cb.COL_IMPACT_REFERENCES_RESEARCH,
                   cb.COL_IMPACT_DETAILS,
                   cb.COL_IMPACT_CORROBORATE
                   ]:
        dset = pp.clean_markdown(dset, column)
    rw.print_tstamp("- shift columns from title to the left to fix raw data issue ")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- add column for panels names")

    # save pre-processed data
    # -----------------------
    fname = os.path.join(rw.PROCESSSED_EXTRACTED_PATH, f"{sname}_pprocessed.csv")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fname))
    rw.print_tstamp(f"Saved pre-processed dataset to {fname}")


def main():

    text = "Started preprocessing the data"
    print(text)

    # redirect stdout to a buffer
    buffer = StringIO()
    sys.stdout = buffer

    # process sheets
    # rw.create_folders()
    rw.print_tstamp(text)
    preprocess_outputs()
    preprocess_impacts()

    # restore stdout
    sys.stdout = sys.__stdout__

    fname = os.path.join(rw.LOGS_PATH, 'preprocess_data_log.txt')
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())
    print(f"Log saved in {fname}")


if __name__ == "__main__":
    main()
