""" Preprocess a sheet from the raw data. """
import argparse
import os
import pandas as pd
import logging

import utils
import read_write as rw
import codebook as cb
import preprocess as pp


def preprocess_results(dset, sname):
    """Preprocess the data from the Results sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    # replace - in a list of columns with na
    # --------------------------------------
    text_to_replace = "-"
    columns = [
        cb.COL_RESULTS_4star,
        cb.COL_RESULTS_3star,
        cb.COL_RESULTS_2star,
        cb.COL_RESULTS_1star,
        cb.COL_RESULTS_UNCLASSIFIED,
    ]
    for column in columns:
        dset[column] = dset[column].replace(text_to_replace, float("NaN"))
        dset[column] = dset[column].astype(float)

    # bin percentages
    # ---------------
    # COL_RESULTS_PERC_STAFF_SUBMITTED, COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT not binned, not < 100%
    columns = [
        cb.COL_RESULTS_4star,
        cb.COL_RESULTS_3star,
        cb.COL_RESULTS_2star,
        cb.COL_RESULTS_1star,
        cb.COL_RESULTS_UNCLASSIFIED,
    ]
    for column in columns:
        dset = pp.bin_percentages(
            dset, column, f"{column}{cb.COLUMN_NAME_BINNED_SUFFIX}"
        )
    logging.info(f"{sname} - bin percentages in the {columns}")

    # drop the columns not relevant for current visualisations
    # --------------------------------------------------------
    columns_to_drop = [cb.COL_INST_CODE_BRACKETS, cb.COL_RESULTS_SORT_ORDER]
    for column in columns_to_drop:
        dset_stats = dset[column].value_counts().to_frame(name="count")
        dset_stats.index.name = column
        dset = dset.drop(column, axis=1)
    logging.info(f"{sname} - drop columns {columns_to_drop}")

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
        cb.COL_RESULTS_4star,
        cb.COL_RESULTS_3star,
        cb.COL_RESULTS_2star,
        cb.COL_RESULTS_1star,
        cb.COL_RESULTS_UNCLASSIFIED,
    ]
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

    # pivot and drop duplcate columns
    dset = dset.pivot(index=columns_index, columns=column_pivot, values=columns_values)
    columns = [f"{column[1]} {suffix} - {column[0]}" for column in dset.columns]
    dset.columns = columns
    dset = dset[sorted(columns)]
    dset.drop(columns=columns_to_drop, inplace=True)

    # rename columns and move the re-named columns to the front
    dset.rename(columns=columns_to_rename, inplace=True)
    columns = [column for column in columns_to_rename.values()]
    columns.extend(
        [
            column
            for column in dset.columns.tolist()
            if column not in columns_to_rename.values()
        ]
    )
    dset = dset[columns]

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
        rw.PROCESSED_SHEETS_PATH, f"{rw.SHEET_RGROUPS}{rw.PPROCESS}{rw.DATA_EXTS[0]}"
    )
    dset_extra = rw.read_dataframe(infname, sname)

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
    logging.info(f"{sname} - added column '{column_name}'")
    
    nrecords = dset_extra.shape[0]
    entries_count = dset[column_name].sum()
    if nrecords != entries_count:
        logging.info(f"WARNING: {nrecords} != {entries_count}")

    # read and merge the information from outputs
    # --------------------------------------------
    infname = os.path.join(
        rw.PROCESSED_SHEETS_PATH, f"{rw.SHEET_OUTPUTS}{rw.PPROCESS}{rw.DATA_EXTS[0]}"
    )
    dset_extra = rw.read_dataframe(infname, sname)

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

    logging.info(f"{sname} - added column '{column_name}'")
    nrecords = dset_extra.shape[0]
    entries_count = dset[column_name].sum()
    if nrecords != entries_count:
        logging.info(f"WARNING: {nrecords} != {entries_count}")

    column_to_count = "Output type"
    for value in dset_extra[column_to_count].unique():
        selected_indices = dset_extra[column_to_count] == value
        column_selected = f"{column_name} - {value}{cb.COLUMN_NAME_ADDED_SUFFIX}"
        dset_stats = (
            dset_extra.loc[selected_indices, columns_index]
            .value_counts()
            .to_frame(name=column_selected)
            .reset_index()
        )
        dset = pd.merge(dset, dset_stats, how="left", on=columns_index)
        dset[column_selected] = dset[column_selected].fillna(0)
        logging.info(f"{sname} - added column '{column_selected}'")
        nrecords = dset_extra.loc[selected_indices, column_to_count].shape[0]
        entries_count = dset[column_selected].sum()
        if nrecords != entries_count:
            logging.info(f"WARNING: {nrecords} != {entries_count}")

    # read and merge the information from impacts
    infname = os.path.join(
        rw.PROCESSED_SHEETS_PATH, f"{rw.SHEET_IMPACTS}{rw.PPROCESS}{rw.DATA_EXTS[0]}"
    )
    dset_extra = rw.read_dataframe(infname, sname)

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

    logging.info(f"{sname} - added column '{column_name}'")
    if dset_extra.shape[0] != dset[column_name].sum():
        logging.info(f"WARNING: {dset_extra.shape[0]} != {dset[column_name].sum()}")

    # read and merge the information from degrees
    infname = os.path.join(
        rw.PROCESSED_SHEETS_PATH, f"{rw.SHEET_DEGREES}{rw.PPROCESS}{rw.DATA_EXTS[0]}"
    )
    dset_extra = rw.read_dataframe(infname, sname)

    columns_to_merge = [cb.COL_DEGREES_TOTAL]
    columns_all = columns_index.copy()
    columns_all.extend(columns_to_merge)
    dset = pd.merge(dset, dset_extra[columns_all], how="left", on=columns_index)

    logging.info(f"{sname} - added columns '{columns_to_merge}'")
    extra_sum = dset_extra[columns_to_merge[0]].sum()
    dset_sum = dset[columns_to_merge[0]].sum()
    if extra_sum != dset_sum:
        logging.info(f"WARNING: {extra_sum} != {dset_sum}")

    # read and merge the unit environment statements
    infname = os.path.join(
        rw.PROCESSED_ENV_PREPARED_PATH, f"{rw.ENV_UNIT}{rw.PPROCESS}{rw.DATA_EXTS[0]}"
    )
    dset_uenv = rw.read_dataframe(infname, sname)

    # replace na in cb.COL_MULT_SUB_LETTER with "" for merging
    dset_uenv[cb.COL_MULT_SUB_LETTER] = dset_uenv[cb.COL_MULT_SUB_LETTER].fillna("")

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]
    dset_extra = pd.merge(dset, dset_uenv, how="left", on=columns_index)
    logging.info(
        f"{sname} - merged with unit environment statements: {dset_extra.shape[0]} records"
    )

    return (dset, dset_extra)


def preprocess_rgroups(dset, sname):
    """Preprocess the data from the ResearchGroups sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    # make group code categorical
    dset[cb.COL_RG_CODE] = pd.Categorical(dset[cb.COL_RG_CODE])
    logging.info(f"{sname} - make group code categorical")

    return dset


def preprocess_income(dset, sname):
    """Preprocess the data from the ResearchIncome sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    # make group code categorical
    dset[cb.COL_INCOME_SOURCE] = pd.Categorical(dset[cb.COL_INCOME_SOURCE])
    logging.info(f"{sname} - make income source categorical")

    return dset


def preprocess_incomeinkind(dset, sname):
    """Preprocess the data from the ResearchIncomeInKind sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.

    """

    # make group code categorical
    dset[cb.COL_INCOME_SOURCE] = pd.Categorical(dset[cb.COL_INCOME_SOURCE])
    logging.info(f"{sname} - make income source categorical")

    return dset


def preprocess_degrees(dset, sname):
    """Preprocess the data from the ResearchDoctoralDegreesAwarded sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

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
    logging.info(f"{sname} - calculate total number of degrees awarded")

    return dset


def preprocess_outputs(dset, sname):
    """Preprocess the data from the Outputs sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    # replace various styling characters selected columns
    columns = [cb.COL_OUTPUT_TITLE]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    logging.info(f"{sname} - replace styling characters in {columns}")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(
        cb.OUTPUT_TYPE_NAMES
    )
    dset = pp.move_last_column(dset, cb.COL_UOA_NAME)
    logging.info(f"{sname} - add columns for output types names")

    # make output year categorical
    dset[cb.COL_OUTPUT_YEAR] = pd.Categorical(dset[cb.COL_OUTPUT_YEAR])
    logging.info(f"{sname} - make output year categorical")

    return dset


def preprocess_impacts(dset, sname):
    """Preprocess the data from the ImpactCaseStudies sheet

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with data pre-processed.
    """

    # shift columns from title to the left
    # ------------------------------------
    columns = dset.columns.tolist()
    dset = dset.drop(cb.COL_IMPACT_TITLE, axis=1)
    dset.columns = columns[:-1]
    logging.info(
        f"{sname} - shift columns from title to the left to fix raw data issue "
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
    logging.info(f"{sname} - replace styling characters in {columns}")

    return dset


def preprocess_sheet(sname):
    """Preprocess a sheet from the raw data.

    Args:
        sname (str): Name of the sheet to preprocess.
    """

    # set the input excel file name and index
    if sname == "Results":
        infname = rw.RAW_RESULTS_FNAME
        header_index = rw.RAW_RESULTS_HEADER_INDEX
    else:
        infname = rw.RAW_SUBMISSIONS_FNAME
        header_index = rw.RAW_SUBMISSIONS_HEADER_INDEX

    # extract sheet
    dset = rw.extract_sheet(infname, sname, header_index)

    # rename columns for clarity
    dset = pp.rename_columns(dset, sname)

    # preprocess institution name
    dset = pp.preprocess_inst_name(dset, sname)

    # assign names where we only have codes and make categorical
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset[cb.COL_PANEL_NAME] = pd.Categorical(dset[cb.COL_PANEL_NAME])
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    logging.info(f"{sname} - add columns for panel names")

    # replace na in COL_MULT_SUB_LETTER with empty string
    if cb.COL_MULT_SUB_LETTER in dset.columns:
        dset[cb.COL_MULT_SUB_LETTER] = dset[cb.COL_MULT_SUB_LETTER].fillna("")

    # runs specific pre-processing if needed
    dset_extra = None
    if sname == rw.SHEET_RGROUPS:
        dset = preprocess_rgroups(dset, sname)
    elif sname == rw.SHEET_DEGREES:
        dset = preprocess_degrees(dset, sname)
    elif sname == rw.SHEET_OUTPUTS:
        dset = preprocess_outputs(dset, sname)
    elif sname == rw.SHEET_IMPACTS:
        dset = preprocess_impacts(dset, sname)
    elif sname == rw.SHEET_INCOME:
        dset = preprocess_income(dset, sname)
    elif sname == rw.SHEET_INCOMEINKIND:
        dset = preprocess_incomeinkind(dset, sname)
    elif sname == rw.SHEET_RESULTS:
        dset, dset_extra = preprocess_results(dset, sname)

    # drop the code columns
    columns_to_drop = list(set(cb.COLUMNS_TO_DROP).intersection(dset.columns))
    dset = dset.drop(columns_to_drop, axis=1)
    logging.info(f"{sname} - drop columns '{columns_to_drop}'")

    # make categorical
    columns_to_category = list(set(cb.COLUMNS_TO_CATEGORY).intersection(dset.columns))
    if len(columns_to_category) > 0:
        logging.info(f"{sname} - make categorical {columns_to_category}")
        for column in columns_to_category:
            dset[column] = pd.Categorical(dset[column])

    # set the index name
    dset.index.name = "Record"

    # save the pre-processed data
    rw.export_dataframe(
        dset, os.path.join(rw.PROCESSED_SHEETS_PATH, f"{sname}{rw.PPROCESS}"), sname
    )

    # save the extra pre-processed data
    if dset_extra is not None:
        rw.export_dataframe(
            dset_extra,
            os.path.join(rw.PROCESSED_SHEETS_PATH, f"{sname}{rw.PPROCESS}_extra"),
            sname,
        )

    # move the interim logfile in the log folder
    fname = f"{sname}{rw.PPROCESS}{rw.LOG_EXT}"
    os.rename(
        os.path.join(rw.LOG_INTERIM_PATH, fname), os.path.join(rw.LOG_PATH, fname)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts a sheet from an excel file and saves it as csv file."
    )

    parser.add_argument(
        "-s", "--sheetname", required=True, help="name of the sheet to preprocess"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        help="write logging to console, default false",
    )

    args = parser.parse_args()
    sname = args.sheetname

    # setup logger
    status = utils.setup_logger(f"{sname}{rw.PPROCESS}", verbose=args.verbose)

    # run pre-processing
    if status:
        preprocess_sheet(sname)
    else:
        print(f"{utils.FAILED_ICON} failed: setup logger")
