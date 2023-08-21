import argparse
from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import preprocess as pp


def preprocess_outputs(dset, sname="Outputs"):
    """ Preprocess the data from the Outputs sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(cb.OUTPUT_TYPE_NAMES)
    rw.print_tstamp("- PPROC: add columns for panel and output types names")

    # select and save software outputs
    target_output_type = "Software"
    fsuffix = f"{target_output_type.lower()}"
    fname = os.path.join(rw.PROCESSSED_SUBSETS_PATH, f"{sname}_{fsuffix}.csv.gz")
    fpath = os.path.join(rw.PROJECT_PATH, fname)
    dset[dset[cb.COL_OUTPUT_TYPE_NAME] == target_output_type].to_csv(fpath,
                                                                     index=False,
                                                                     compression='gzip')

    rw.print_tstamp(f"SAVED '{fsuffix}' subset to '{fname}'")

    return dset


def preprocess_impacts(dset, sname="ImpactCaseStudies"):
    """ Preprocess the data from the ImpactCaseStudies sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

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
    rw.print_tstamp("- PPROC: shift columns from title to the left to fix raw data issue ")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- PPROC: add column for panels names")

    return dset


def preprocess_degrees(dset, sname="ResearchDoctoralDegreesAwarded"):
    """ Preprocess the data from the ResearchDoctoralDegreesAwarded sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_income(dset, sname="ResearchIncome"):
    """ Preprocess the data from the ResearchIncome sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_incomeinkind(dset, sname="ResearchIncomeInKind"):
    """ Preprocess the data from the ResearchIncomeInKind sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_rgroups(dset, sname="ResearchGroups"):
    """ Preprocess the data from the ResearchGroups sheet
    """

    # pre-processing
    # --------------
    rw.print_tstamp(f"PPROC actions for '{sname}' sheet")
    dset = dset.fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    rw.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    rw.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_sheet(sname):
    """ Preprocess a sheet from the raw data.

    Args:
        sname (str): Name of the sheet to preprocess.
    """

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    sys.stdout = buffer

    # read data
    # ---------
    fname = os.path.join(rw.PROCESSED_EXTRACTED_PATH, f"{sname}.csv.gz")
    dset = pd.read_csv(os.path.join(rw.PROJECT_PATH, fname),
                       index_col=None,
                       dtype={0: str},
                       compression='gzip'
                       )
    rw.print_tstamp(f"READ '{fname}': {dset.shape[0]} records")

    # run specific pre-processing
    # ---------------------------
    if sname == "Outputs":
        preprocess_outputs(dset)
    elif sname == "ImpactCaseStudies":
        preprocess_impacts(dset)
    elif sname == "ResearchDoctoralDegreesAwarded":
        preprocess_degrees(dset)
    elif sname == "ResearchIncome":
        preprocess_income(dset)
    elif sname == "ResearchIncomeInKind":
        preprocess_incomeinkind(dset)
    elif sname == "ResearchGroups":
        preprocess_rgroups(dset)
    else:
        raise ValueError(f"Unknown sheet name: {sname}")

    # save the pre-processed data
    # ---------------------------
    fname = os.path.join(rw.PROCESSED_EXTRACTED_PATH, f"{sname}_pprocessed.csv.gz")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fname),
                index=False,
                compression='gzip')
    rw.print_tstamp(f"SAVED pre-processed dataset to '{fname}'")

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    # save the log file
    # -----------------
    fname = os.path.join(rw.LOGS_PATH, f"preprocess_{sname}.log")
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts a sheet from an excel file and saves it as csv file."
        )

    parser.add_argument("-s", "--sheetname",
                        required=True,
                        help="name of the sheet to preprocess")

    args = parser.parse_args()
    sname = args.sheetname
    preprocess_sheet(sname)
