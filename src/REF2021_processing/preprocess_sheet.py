""" Preprocess a sheet from the raw data. """
import argparse
import os
import logging
import pandas as pd

from REF2021_processing import utils
import REF2021_processing.read_write as rw
import REF2021_processing.codebook as cb
import REF2021_processing.preprocess as pp


def preprocess_results(dset):
    """Preprocess the data from the Results sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    sname = rw.SOURCES["results"]["sheet"]

    # replace - in a list of columns with na
    # --------------------------------------
    text_to_replace = "-"
    for column in cb.COLUMNS_STARS:
        dset[column] = dset[column].apply(
            lambda x: float("NaN") if x == text_to_replace else float(x)
        )
    logging.info(
        f"%s - replace '%s' with na in {cb.COLUMNS_STARS}", sname, text_to_replace
    )

    # bin percentages
    # ---------------
    # COL_RESULTS_PERC_STAFF_SUBMITTED, COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT not binned, not < 100%
    for column in cb.COLUMNS_STARS:
        dset = pp.bin_percentages(
            dset, column, f"{column}{cb.COLUMN_NAME_BINNED_SUFFIX}"
        )
    logging.info("%s - bin percentages for %s", sname, cb.COLUMNS_STARS)

    # drop the columns not relevant for current visualisations
    # --------------------------------------------------------
    dset = utils.drop_specified_columns(
        dset, [cb.COL_INST_CODE_BRACKETS, cb.COL_RESULTS_SORT_ORDER], sname
    )

    dset = pp.pivot_results_by_profile(dset, sname)

    # make all binned columns categorical
    dset = utils.make_columns_categorical(
        dset,
        [column for column in dset.columns if cb.COLUMN_NAME_BINNED_SUFFIX in column],
        sname,
    )

    # read and merge information from research groups
    # -----------------------------------------------
    dset = pp.merge_resuts_with_groups(dset)

    # read and merge the information from outputs
    # --------------------------------------------
    dset = pp.merge_resuts_with_outputs(dset)

    # read and merge the information from impacts
    # -------------------------------------------
    dset = pp.merge_resuts_with_impacts(dset)

    # read and merge the information from degrees
    # -------------------------------------------
    dset = pp.merge_resuts_with_degrees(dset)

    # read and merge the unit environment statements
    # ---------------------------------------------
    dset = pp.merge_resuts_with_uenvstatements(dset)

    return dset


def preprocess_groups(dset):
    """Preprocess the data from the ResearchGroups sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    sname = rw.SOURCES["submissions"]["sheets"]["groups"]

    # make group code categorical
    dset[cb.COL_RG_CODE] = pd.Categorical(dset[cb.COL_RG_CODE])
    logging.info("%s - make group code categorical", sname)

    return dset


def preprocess_income(dset):
    """Preprocess the data from the ResearchIncome sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    sname = rw.SOURCES["submissions"]["sheets"]["income"]

    # make group code categorical
    dset[cb.COL_INCOME_SOURCE] = pd.Categorical(dset[cb.COL_INCOME_SOURCE])
    logging.info("%s - make income source categorical", sname)

    return dset


def preprocess_income_in_kind(dset):
    """Preprocess the data from the ResearchIncomeInKind sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    sname = rw.SOURCES["submissions"]["sheets"]["income_in_kind"]

    # make group code categorical
    dset[cb.COL_INCOME_SOURCE] = pd.Categorical(dset[cb.COL_INCOME_SOURCE])
    logging.info("%s - make income source categorical", sname)

    return dset


def preprocess_degrees(dset):
    """Preprocess the data from the ResearchDoctoralDegreesAwarded sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    sname = rw.SOURCES["submissions"]["sheets"]["degrees"]

    # calculate the total number of degrees awarded
    column_to_sum = [
        cb.COL_DEGREES_2013,
        cb.COL_DEGREES_2014,
        cb.COL_DEGREES_2015,
        cb.COL_DEGREES_2016,
        cb.COL_DEGREES_2017,
        cb.COL_DEGREES_2018,
        cb.COL_DEGREES_2019,
    ]
    dset[cb.COL_DEGREES_TOTAL] = dset[column_to_sum].sum(axis=1)
    logging.info("%s - calculate total number of degrees awarded", sname)

    return dset


def preprocess_outputs(dset):
    """Preprocess the data from the Outputs sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    sname = rw.SOURCES["submissions"]["sheets"]["outputs"]

    # replace various styling characters selected columns
    columns = [cb.COL_OUTPUT_TITLE]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    logging.info("%s - replace styling characters in %s", sname, columns)

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(
        cb.OUTPUT_TYPE_NAMES
    )
    dset = pp.move_last_column(dset, cb.COL_UOA_NAME)
    logging.info("%s - add columns for output types names", sname)

    # make output year categorical
    dset[cb.COL_OUTPUT_YEAR] = pd.Categorical(dset[cb.COL_OUTPUT_YEAR])
    logging.info("%s - make output year categorical", sname)

    return dset


def preprocess_impacts(dset):
    """Preprocess the data from the ImpactCaseStudies sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    sname = rw.SOURCES["submissions"]["sheets"]["impacts"]

    # shift columns from title to the left
    # ------------------------------------
    columns = dset.columns.tolist()
    dset = dset.drop(cb.COL_IMPACT_TITLE, axis=1)
    dset.columns = columns[:-1]
    logging.info(
        "%s - shift columns from title to the left to fix raw data issue ", sname
    )

    # replace various styling characters selected columns
    # ---------------------------------------------------
    columns = [
        cb.COL_IMPACT_SUMMARY,
        cb.COL_IMPACT_UNDERPIN_RESEARCH,
        cb.COL_IMPACT_REFERENCES_RESEARCH,
        cb.COL_IMPACT_DETAILS,
        cb.COL_IMPACT_CORROBORATE,
    ]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    logging.info("%s - replace styling characters in %s", sname, columns)

    return dset


def preprocess_sheet(source):
    """Preprocess a sheet from the raw data.

    Args:
        sname (str): Name of the sheet to preprocess.
    """

    # set the input excel file name and index
    if source == "results":
        sname = rw.SOURCES["results"]["sheet"]
        infname = os.path.join(
            rw.SOURCES["results"]["raw_path"], rw.SOURCES["results"]["filename"]
        )
        header_index = rw.SOURCES["results"]["header_index"]
    else:
        sname = rw.SOURCES["submissions"]["sheets"][source]

        infname = os.path.join(
            rw.SOURCES["submissions"]["raw_path"], rw.SOURCES["submissions"]["filename"]
        )
        header_index = rw.SOURCES["submissions"]["header_index"]

    # extract sheet
    dset = rw.extract_sheet(infname, sname, header_index)
    # rename columns for clarity
    dset = pp.rename_columns(dset, sname)

    # preprocess institution name
    dset = pp.preprocess_inst_name(dset, sname)

    # assign names where we only have codes and make categorical
    dset[cb.COL_PANEL_NAME] = pd.Categorical(
        dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    )
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    logging.info("%s - add columns for panel names", sname)

    # replace na in COL_MULT_SUB_LETTER with empty string
    if cb.COL_MULT_SUB_LETTER in dset.columns:
        dset[cb.COL_MULT_SUB_LETTER] = dset[cb.COL_MULT_SUB_LETTER].fillna("")

    # runs specific pre-processing if needed
    if source == "groups":
        dset = preprocess_groups(dset)
    if source == "degrees":
        dset = preprocess_degrees(dset)
    if source == "outputs":
        dset = preprocess_outputs(dset)
    if source == "impacts":
        dset = preprocess_impacts(dset)
    if source == "income":
        dset = preprocess_income(dset)
    if source == "income_in_kind":
        dset = preprocess_income_in_kind(dset)
    if source == "results":
        dset = preprocess_results(dset)

    # drop the code columns
    dset = utils.drop_specified_columns(dset, cb.COLUMNS_TO_DROP, sname)

    # make categorical
    dset = utils.make_columns_categorical(dset, cb.COLUMNS_TO_CATEGORY, sname)

    # set the index name and save the pre-processed data
    dset.index.name = "Record"
    rw.export_dataframe(
        dset, os.path.join(rw.SOURCES["submissions"]["output_path"], sname), sname
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts a sheet from an excel file and saves it as csv and parquet files."
    )

    parser.add_argument(
        "-s", "--source", required=True, help="source of data to process"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        help="write logging to console, default false",
    )

    args = parser.parse_args()
    source_name = args.source

    if source_name == "results":
        SHEET_NAME = rw.SOURCES["results"]["sheet"]
    else:
        SHEET_NAME = rw.SOURCES["submissions"]["sheets"][source_name]

    STATUS = utils.setup_logger(SHEET_NAME, verbose=args.verbose)

    # run pre-processing
    if STATUS:
        preprocess_sheet(source_name)
    else:
        print(f"{utils.FAILED_ICON} failed: setup logger")

    utils.complete_logger(SHEET_NAME, verbose=args.verbose)
