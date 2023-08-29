import argparse
from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import preprocess as pp
import logs as lg


def preprocess_inst_name(dset):
    """ Preprocess the institution name column
        to replace characters that are not allowed in filenames.

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with cb.COL_INST_NAME column processed.
    """
    chars_to_replace = ["/", ":"]
    for char_to_replace in chars_to_replace:
        dset[cb.COL_INST_NAME] = dset[cb.COL_INST_NAME].str.replace(char_to_replace, "_")
    lg.print_tstamp(f"- PPROC: replace '{chars_to_replace}' with '_' in '{cb.COL_INST_NAME}'")

    return dset


def preprocess_outputs(dset, sname="Outputs"):
    """ Preprocess the data from the Outputs sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    dset = pp.rename_columns(dset)
    # preprocess institution name
    dset = preprocess_inst_name(dset)
    # replace na in cb.COL_OUTPUT_CITATIONS with "No"
    columns = [cb.COL_OUTPUT_CITATIONS, cb.COL_OUTPUT_INTERDISCIPLINARY]
    text_to_replace = "No"
    for column in columns:
        dset[column] = dset[column].fillna(text_to_replace)
    lg.print_tstamp(f"- PPROC: replace NaN with '{text_to_replace}' in '{columns}'")

    # replace missing values in object columns
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # replace various styling characters selected columns
    columns = [cb.COL_OUTPUT_TITLE]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    lg.print_tstamp("- PPROC: replace styling characters in the following columns")
    lg.print_tstamp(f"- {columns}")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(cb.OUTPUT_TYPE_NAMES)
    lg.print_tstamp("- PPROC: add columns for panel and output types names")

    return dset


def preprocess_impacts(dset, sname="ImpactCaseStudies"):
    """ Preprocess the data from the ImpactCaseStudies sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    dset = pp.rename_columns(dset)
    # preprocess institution name
    dset = preprocess_inst_name(dset)
    # replace missing values in object columns
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # shift columns from title to the left
    columns = dset.columns.tolist()
    dset = dset.drop(cb.COL_IMPACT_TITLE, axis=1)
    dset.columns = columns[:-1]
    lg.print_tstamp("- PPROC: shift columns from title to the left to fix raw data issue ")
    # replace various styling characters selected columns
    columns = [cb.COL_IMPACT_SUMMARY,
               cb.COL_IMPACT_UNDERPIN_RESEARCH,
               cb.COL_IMPACT_REFERENCES_RESEARCH,
               cb.COL_IMPACT_DETAILS,
               cb.COL_IMPACT_CORROBORATE
               ]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    lg.print_tstamp("- PPROC: replace styling characters in the following columns")
    lg.print_tstamp(f"- {columns}")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    lg.print_tstamp("- PPROC: add column for panels names")

    return dset


def preprocess_degrees(dset, sname="ResearchDoctoralDegreesAwarded"):
    """ Preprocess the data from the ResearchDoctoralDegreesAwarded sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    # replace missing values in object columns
    # ----------------------------------------
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    lg.print_tstamp("- PPROC: add columns for panel names")

    # drop the code columns
    # ---------------------
    columns_to_drop = [cb.COL_PANEL_CODE,
                       cb.COL_UOA_NUMBER
                       ]
    dset = dset.drop(columns_to_drop, axis=1)
    lg.print_tstamp(f"- PPROC: drop columns '{columns_to_drop}'")

    # drop the columns not relevant for current visualisations
    # --------------------------------------------------------
    columns_to_drop = [cb.COL_MULT_SUB_LETTER,
                       cb.COL_MULT_SUB_NAME,
                       cb.COL_JOINT_SUB]
    for column in columns_to_drop:
        dset_stats = dset[column].value_counts().to_frame(name="count")
        dset_stats.index.name = column
        dset = dset.drop(column, axis=1)
        lg.print_tstamp(f"- PPROC: drop column '{column}'")
        print(f"{dset_stats}")

    # calculate the total number of degrees awarded
    # ---------------------------------------------
    column_to_sum = [cb.COL_DEGREES_2013, cb.COL_DEGREES_2014, cb.COL_DEGREES_2015,
                     cb.COL_DEGREES_2016, cb.COL_DEGREES_2017, cb.COL_DEGREES_2018,
                     cb.COL_DEGREES_2019]
    dset[cb.COL_DEGREES_TOTAL] = dset[column_to_sum].sum(axis=1)
    lg.print_tstamp(f"- PPROC: calculate total number of degrees awarded")

    return dset


def preprocess_income(dset, sname="ResearchIncome"):
    """ Preprocess the data from the ResearchIncome sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    dset = pp.rename_columns(dset)
    # preprocess institution name
    dset = preprocess_inst_name(dset)
    # replace missing values in object columns
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    lg.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_incomeinkind(dset, sname="ResearchIncomeInKind"):
    """ Preprocess the data from the ResearchIncomeInKind sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    dset = pp.rename_columns(dset)
    # preprocess institution name
    dset = preprocess_inst_name(dset)
    # replace missing values in object columns
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    lg.print_tstamp("- PPROC: add columns for panel names")

    return dset


def preprocess_rgroups(dset, sname="ResearchGroups"):
    """ Preprocess the data from the ResearchGroups sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    # replace missing values in object columns
    # ----------------------------------------
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    lg.print_tstamp("- PPROC: add columns for panel names")

    # drop the code columns
    # ---------------------
    columns_to_drop = [cb.COL_PANEL_CODE,
                       cb.COL_UOA_NUMBER,
                       cb.COL_RG_CODE
                       ]
    dset = dset.drop(columns_to_drop, axis=1)
    lg.print_tstamp(f"- PPROC: drop columns '{columns_to_drop}'")

    # drop the columns not relevant for current visualisations
    # --------------------------------------------------------
    columns_to_drop = [cb.COL_MULT_SUB_LETTER,
                       cb.COL_MULT_SUB_NAME,
                       cb.COL_JOINT_SUB]
    for column in columns_to_drop:
        dset_stats = dset[column].value_counts().to_frame(name="count")
        dset_stats.index.name = column
        dset = dset.drop(column, axis=1)
        lg.print_tstamp(f"- PPROC: drop column '{column}'")
        print(f"{dset_stats}")

    return dset


def preprocess_results(dset, sname="Results"):
    """ Preprocess the data from the Results sheet
    """

    # pre-processing
    # --------------
    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    dset = pp.rename_columns(dset)
    # preprocess institution name
    dset = preprocess_inst_name(dset)
    # replace - in a list of columns with na
    text_to_replace = "-"
    columns = [cb.COL_RESULTS_4star,
               cb.COL_RESULTS_3star,
               cb.COL_RESULTS_2star,
               cb.COL_RESULTS_1star,
               cb.COL_RESULTS_UNCLASSIFIED
               ]
    for column in columns:
        dset[column] = dset[column].replace(text_to_replace, float("NaN"))
        dset[column] = dset[column].astype(float)
    lg.print_tstamp(f"- PPROC: replace '{text_to_replace}' with NaN in the following columns")
    lg.print_tstamp(f"- {columns}")

    # replace missing values in object columns
    columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
    dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
    lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # bin percentages
    columns = [cb.COL_RESULTS_PERC_STAFF_SUBMITTED,
               cb.COL_RESULTS_4star,
               cb.COL_RESULTS_3star,
               cb.COL_RESULTS_2star,
               cb.COL_RESULTS_1star,
               cb.COL_RESULTS_UNCLASSIFIED
               ]
    for column in columns:
        dset = pp.bin_percentages(dset, column, f"{column} (binned)")
    lg.print_tstamp("- PPROC: bin percentages in the following columns")
    lg.print_tstamp(f"- {columns}")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    lg.print_tstamp("- PPROC: add columns for panel names")

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
    infname = os.path.join(rw.PROCESSED_PATH, f"{sname}{rw.DATA_EXT}")
    dset = pd.read_csv(os.path.join(rw.PROJECT_PATH, infname),
                       index_col=None,
                       dtype={0: str},
                       compression='gzip'
                       )
    lg.print_tstamp(f"READ '{infname}': {dset.shape[0]} records")

    # run specific pre-processing
    # ---------------------------
    if sname == "Outputs":
        dset = preprocess_outputs(dset)
    elif sname == "ImpactCaseStudies":
        dset = preprocess_impacts(dset)
    elif sname == "ResearchDoctoralDegreesAwarded":
        dset = preprocess_degrees(dset)
    elif sname == "ResearchIncome":
        dset = preprocess_income(dset)
    elif sname == "ResearchIncomeInKind":
        dset = preprocess_incomeinkind(dset)
    elif sname == "ResearchGroups":
        dset = preprocess_rgroups(dset)
    elif sname == "Results":
        dset = preprocess_results(dset)
    else:
        raise ValueError(f"Unknown sheet name: {sname}")

    # save the pre-processed data
    # ---------------------------
    dset.index.name = "Record"
    fname = os.path.join(rw.PROCESSED_PATH, f"{sname}{rw.DATA_PPROCESS}{rw.DATA_EXT}")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fname),
                index=True,
                compression='gzip')
    lg.print_tstamp(f"SAVED pre-processed dataset to '{fname}'")

    # delete infname
    # --------------
    os.remove(os.path.join(rw.PROJECT_PATH, infname))
    lg.print_tstamp(f"DELETED '{infname}'")

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    # save the log file
    # -----------------
    fname = f"{rw.LOG_PPREPROCESS}{sname}{rw.LOG_EXT}"
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
