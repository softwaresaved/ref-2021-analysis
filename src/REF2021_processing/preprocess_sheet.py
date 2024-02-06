""" Preprocess a sheet from the raw data. """
import argparse
import os
import logging
import pandas as pd

from REF2021_processing import utils
import REF2021_processing.read_write as rw
import REF2021_processing.codebook as cb
import REF2021_processing.preprocess as pp

COLUMNS_STARS = [
    cb.COL_RESULTS_4STAR,
    cb.COL_RESULTS_3STAR,
    cb.COL_RESULTS_2STAR,
    cb.COL_RESULTS_1STAR,
    cb.COL_RESULTS_UNCLASSIFIED,
]


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
    for column in COLUMNS_STARS:
        dset[column] = dset[column].replace(text_to_replace, float("NaN"))
        dset[column] = dset[column].astype(float)
    logging.info(
        f"%s - replace '%s' with na in {COLUMNS_STARS}", sname, text_to_replace
    )

    # bin percentages
    # ---------------
    # COL_RESULTS_PERC_STAFF_SUBMITTED, COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT not binned, not < 100%
    for column in COLUMNS_STARS:
        dset = pp.bin_percentages(
            dset, column, f"{column}{cb.COLUMN_NAME_BINNED_SUFFIX}"
        )
    logging.info("%s - bin percentages for %s", sname, COLUMNS_STARS)

    # drop the columns not relevant for current visualisations
    # --------------------------------------------------------
    dset = utils.drop_specified_columns(
        dset, [cb.COL_INST_CODE_BRACKETS, cb.COL_RESULTS_SORT_ORDER], sname
    )

    # setup the pivoting action
    columns_index = [
        cb.COL_INST_NAME,
        cb.COL_PANEL_NAME,
        cb.COL_UOA_NAME,
        cb.COL_MULT_SUB_LETTER,
        cb.COL_MULT_SUB_NAME,
        cb.COL_JOINT_SUB,
    ]
    column_pivot = cb.COL_RESULTS_PROFILE
    column_pivot_values = sorted(dset[column_pivot].unique())

    # first two are assumed to the perc staff submitted that have the same value for all profiles
    # for which duplicates are dropped and the column name is changed
    columns_values = [
        cb.COL_RESULTS_PERC_STAFF_SUBMITTED,
        cb.COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT,
    ]
    columns_values.extend(COLUMNS_STARS)
    columns_values.extend(
        [f"{column}{cb.COLUMN_NAME_BINNED_SUFFIX}" for column in columns_values[2:]]
    )
    suffix = "evaluation"

    # columns to drop from the wide format because they are duplicates
    columns_to_drop = [
        f"{pivot_value} {suffix} - {column_value}"
        for pivot_value in column_pivot_values[1:]
        for column_value in columns_values[:2]
    ]
    # these are not binned as not < 100%
    # columns_to_drop.extend(
    #     [f"{column}{cb.COLUMN_NAME_BINNED_SUFFIX}" for column in columns_to_drop]
    # )

    # columms to rename in the wide format after dropping the duplicates
    columns_to_rename = {}
    for column_value in columns_values[:2]:
        label = f"{column_pivot_values[0]} {suffix} - {column_value}"
        columns_to_rename[label] = f"{column_value}"

    # pivot and drop duplicate columns
    dset = dset.pivot(index=columns_index, columns=column_pivot, values=columns_values)
    columns = [f"{column[1]} {suffix} - {column[0]}" for column in dset.columns]
    dset.columns = columns
    dset = dset[sorted(columns)]
    dset.drop(columns=columns_to_drop, inplace=True)

    # rename columns and move the re-named columns to the front
    dset.rename(columns=columns_to_rename, inplace=True)
    columns = list(columns_to_rename.values())
    columns.extend(
        [
            column
            for column in dset.columns.tolist()
            if column not in columns_to_rename.values()
        ]
    )
    dset = dset[columns]
    logging.info(
        "%s - pivot to make wide format for ratings per profile to enable analyses",
        sname,
    )

    # make all binned columns categorical
    columns_to_category = [
        column for column in dset.columns if cb.COLUMN_NAME_BINNED_SUFFIX in column
    ]
    for column in columns_to_category:
        dset[column] = pd.Categorical(dset[column])

    # flatten index
    dset.reset_index(inplace=True)

    # prepare to merge with extra information
    # ---------------------------------------
    # columns for merging the extra information
    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

    # read and merge information from research groups
    # -----------------------------------------------
    infname = os.path.join(
        rw.SOURCES["submissions"]["output_path"],
        f"{rw.SOURCES['submissions']['sheets']['groups']}{rw.OUTPUT_EXTENSION}",
    )
    dset_extra = rw.read_dataframe(infname, sname)

    # add the column with the number of research group submissions
    column_to_count = "Research group submissions"
    column_name = f"{column_to_count}{cb.COLUMN_NAME_ADDED_SUFFIX}"
    dset_stats = (
        dset_extra[columns_index]
        .value_counts()
        .to_frame(name=column_name)
        .reset_index()
    )
    dset = pd.merge(dset, dset_stats, how="left", on=columns_index)
    dset[column_name] = dset[column_name].fillna(0)
    logging.info("%s - added column '%s'", sname, column_name)

    # report mismatch in the number of records
    nrecords = dset_extra.shape[0]
    entries_count = dset[column_name].sum()
    if nrecords != entries_count:
        logging.warning("%s - %d != %d", sname, nrecords, entries_count)

    # read and merge the information from outputs
    # --------------------------------------------
    infname = os.path.join(
        rw.SOURCES["submissions"]["output_path"],
        f"{rw.SOURCES['submissions']['sheets']['outputs']}{rw.OUTPUT_EXTENSION}",
    )
    dset_extra = rw.read_dataframe(infname, sname)

    # add the column with the number of output submissions
    column_to_count = "Output submissions"
    column_name = f"{column_to_count}{cb.COLUMN_NAME_ADDED_SUFFIX}"
    dset_stats = (
        dset_extra[columns_index]
        .value_counts()
        .to_frame(name=column_name)
        .reset_index()
    )
    dset = pd.merge(dset, dset_stats, how="left", on=columns_index)
    dset[column_name] = dset[column_name].fillna(0)
    logging.info("%s - added column '%s'", sname, column_name)

    # report mismatch in the number of records
    nrecords = dset_extra.shape[0]
    entries_count = dset[column_name].sum()
    if nrecords != entries_count:
        logging.warning("%s - %d != %d", sname, nrecords, entries_count)

    # add columns with the number of outputs by type
    column_to_count = "Output type"
    for value in dset_extra[column_to_count].unique():
        selected_indices = dset_extra[column_to_count] == value
        # delete the ADDED suffix from the output type column name so it does not appear twice
        column_selected = (
            f"{column_name.replace(cb.COLUMN_NAME_ADDED_SUFFIX, '')} - "
            f"{value}{cb.COLUMN_NAME_ADDED_SUFFIX}"
        )
        dset_stats = (
            dset_extra.loc[selected_indices, columns_index]
            .value_counts()
            .to_frame(name=column_selected)
            .reset_index()
        )
        dset = pd.merge(dset, dset_stats, how="left", on=columns_index)
        dset[column_selected] = dset[column_selected].fillna(0)
        logging.info("%s - added column '%s'", sname, column_selected)
        nrecords = dset_extra.loc[selected_indices, column_to_count].shape[0]
        # report mismatch in the number of records
        entries_count = dset[column_selected].sum()
        if nrecords != entries_count:
            logging.warning("%s - %d != %d", sname, nrecords, entries_count)

    # read and merge the information from impacts
    # -------------------------------------------
    infname = os.path.join(
        rw.SOURCES["submissions"]["output_path"],
        f"{rw.SOURCES['submissions']['sheets']['impacts']}{rw.OUTPUT_EXTENSION}",
    )
    dset_extra = rw.read_dataframe(infname, sname)

    # add the column with the number of impact case study submissions
    column_to_count = "Impact case study submissions"
    column_name = f"{column_to_count}{cb.COLUMN_NAME_ADDED_SUFFIX}"
    dset_stats = (
        dset_extra[columns_index]
        .value_counts()
        .to_frame(name=column_name)
        .reset_index()
    )
    dset = pd.merge(dset, dset_stats, how="left", on=columns_index)
    dset[column_name] = dset[column_name].fillna(0)
    logging.info("%s - added column '%s'", sname, column_name)

    # report mismatch in the number of records
    if dset_extra.shape[0] != dset[column_name].sum():
        logging.warning(
            "%s - %d != %d", sname, dset_extra.shape[0], dset[column_name].sum()
        )

    # read and merge the information from degrees
    # -------------------------------------------
    infname = os.path.join(
        rw.SOURCES["submissions"]["output_path"],
        f"{rw.SOURCES['submissions']['sheets']['degrees']}{rw.OUTPUT_EXTENSION}",
    )
    dset_extra = rw.read_dataframe(infname, sname)

    # add the column with the number of degrees awarded
    columns_to_merge = [cb.COL_DEGREES_TOTAL]
    columns_all = columns_index.copy()
    columns_all.extend(columns_to_merge)
    dset = pd.merge(dset, dset_extra[columns_all], how="left", on=columns_index)
    logging.info("%s - added columns '%s'", sname, columns_to_merge)

    # report mismatch in the number of records
    extra_sum = dset_extra[columns_to_merge[0]].sum()
    dset_sum = dset[columns_to_merge[0]].sum()
    if extra_sum != dset_sum:
        logging.warning("%s - %d != %d", sname, extra_sum, dset_sum)

    # read and merge the unit environment statements
    # ---------------------------------------------
    infname = os.path.join(
        rw.PROJECT_PATH,
        f"{rw.SOURCES['environment_statements']['unit']['output_path']}"
        f"{rw.SOURCES['environment_statements']['unit']['name']}{rw.OUTPUT_EXTENSION}",
    )
    dset_uenv = rw.read_dataframe(infname, sname)

    # replace na in cb.COL_MULT_SUB_LETTER with "" for merging
    dset_uenv[cb.COL_MULT_SUB_LETTER] = dset_uenv[cb.COL_MULT_SUB_LETTER].fillna("")

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]
    dset_extra = pd.merge(dset, dset_uenv, how="left", on=columns_index)
    logging.info(
        "%s - merged with unit environment statements: %d records",
        sname,
        dset_extra.shape[0],
    )

    # add suffix to added columns
    columns_to_rename = {}
    for column in dset_extra.columns:
        if column not in dset.columns:
            columns_to_rename[column] = f"{column}{cb.COLUMN_NAME_ADDED_SUFFIX}"
    dset_extra.rename(columns=columns_to_rename, inplace=True)

    return dset_extra


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
    else:
        sname = rw.SOURCES["submissions"]["sheets"][source]

    infname = os.path.join(
        rw.SOURCES[source]["raw_path"], rw.SOURCES[source]["filename"]
    )
    header_index = rw.SOURCES[source]["header_index"]

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
