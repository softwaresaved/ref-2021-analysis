""" Preprocess a sheet from the raw data. """
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


def preprocess_outputs(dset, sname="Outputs", replace_na=False):
    """ Preprocess the data from the Outputs sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")

    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    if replace_na:
        # replace na in selected columns with VALUE_ADDED_NO
        # --------------------------------------------------
        columns = [cb.COL_OUTPUT_CITATIONS,
                   cb.COL_OUTPUT_INTERDISCIPLINARY,
                   cb.COL_OUTPUT_NON_ENGLISH,
                   cb.COL_OUTPUT_FORENSIC_SCIENCE,
                   cb.COL_OUTPUT_CRIMINOLOGY,
                   cb.COL_OUTPUT_DOUBLE_WEIGHTING,
                   cb.COL_OUTPUT_RESERVE_OUTPUT,
                   cb.COL_OUTPUT_DELAYED]
        for column in columns:
            dset[column] = dset[column].fillna(cb.VALUE_ADDED_NO)
        lg.print_tstamp(f"- PPROC: replace NaN with '{cb.VALUE_ADDED_NO}' in '{columns}'")

        # replace missing values in object columns
        # ----------------------------------------
        columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
        dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
        lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # replace various styling characters selected columns
    # ---------------------------------------------------
    columns = [cb.COL_OUTPUT_TITLE]
    for column in columns:
        dset = pp.clean_styling(dset, column)
    lg.print_tstamp("- PPROC: replace styling characters in the following columns")
    lg.print_tstamp(f"- {columns}")

    # assign names where we only have codes
    # -------------------------------------
    dset[cb.COL_PANEL_NAME] = dset[cb.COL_PANEL_CODE].map(cb.PANEL_NAMES)
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    dset[cb.COL_OUTPUT_TYPE_NAME] = dset[cb.COL_OUTPUT_TYPE_CODE].map(cb.OUTPUT_TYPE_NAMES)
    dset = pp.move_last_column(dset, cb.COL_UOA_NAME)
    lg.print_tstamp("- PPROC: add columns for panel and output types names")

    # drop the code columns
    # ---------------------
    columns_to_drop = [cb.COL_PANEL_CODE,
                       cb.COL_UOA_NUMBER,
                       cb.COL_OUTPUT_TYPE_CODE
                       ]
    dset = dset.drop(columns_to_drop, axis=1)
    lg.print_tstamp(f"- PPROC: drop columns '{columns_to_drop}'")

    return dset


def preprocess_impacts(dset, sname="ImpactCaseStudies", replace_na=False):
    """ Preprocess the data from the ImpactCaseStudies sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    if replace_na:
        # replace missing values in object columns
        # ----------------------------------------
        columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
        dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
        lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # shift columns from title to the left
    # ------------------------------------
    columns = dset.columns.tolist()
    dset = dset.drop(cb.COL_IMPACT_TITLE, axis=1)
    dset.columns = columns[:-1]
    lg.print_tstamp("- PPROC: shift columns from title to the left to fix raw data issue ")

    # replace various styling characters selected columns
    # ---------------------------------------------------
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
    dset = pp.move_last_column(dset, cb.COL_INST_NAME)
    lg.print_tstamp("- PPROC: add column for panels names")

    # drop the code columns
    # ---------------------
    columns_to_drop = [cb.COL_PANEL_CODE,
                       cb.COL_UOA_NUMBER
                       ]
    dset = dset.drop(columns_to_drop, axis=1)
    lg.print_tstamp(f"- PPROC: drop columns '{columns_to_drop}'")

    # drop the columns not relevant for current visualisations and/or to minimize file size
    # -------------------------------------------------------------------------------------
    columns_to_drop = [cb.COL_IMPACT_ORCID,
                       cb.COL_IMPACT_GRANT_FUNDING,
                       cb.COL_IMPACT_REFERENCES_RESEARCH,
                       cb.COL_IMPACT_CORROBORATE,
                       cb.COL_IMPACT_IS_CONTINUED,
                       cb.COL_IMPACT_COUNTRIES,
                       cb.COL_IMPACT_FORMAL_PARTNERS,
                       cb.COL_IMPACT_GLOBAL_ID,
                       cb.COL_IMPACT_UNDERPIN_RESEARCH]
    for column in columns_to_drop:
        dset_stats = dset[column].value_counts().to_frame(name="count")
        dset_stats.index.name = column
        dset = dset.drop(column, axis=1)
        lg.print_tstamp(f"- PPROC: drop column '{column}'")
        print(f"{dset_stats}")

    return dset


def preprocess_degrees(dset, sname="ResearchDoctoralDegreesAwarded", replace_na=False):
    """ Preprocess the data from the ResearchDoctoralDegreesAwarded sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    if replace_na:
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

    # calculate the total number of degrees awarded
    # ---------------------------------------------
    column_to_sum = [cb.COL_DEGREES_2013, cb.COL_DEGREES_2014, cb.COL_DEGREES_2015,
                     cb.COL_DEGREES_2016, cb.COL_DEGREES_2017, cb.COL_DEGREES_2018,
                     cb.COL_DEGREES_2019]
    dset[cb.COL_DEGREES_TOTAL] = dset[column_to_sum].sum(axis=1)
    lg.print_tstamp("- PPROC: calculate total number of degrees awarded")

    return dset


def preprocess_income(dset, sname="ResearchIncome", replace_na=False):
    """ Preprocess the data from the ResearchIncome sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")
    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    if replace_na:
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

    return dset


def preprocess_incomeinkind(dset, sname="ResearchIncomeInKind", replace_na=False):
    """ Preprocess the data from the ResearchIncomeInKind sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")

    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    if replace_na:
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

    return dset


def preprocess_rgroups(dset, sname="ResearchGroups", replace_na=False):
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

    if replace_na:
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

    dset[cb.COL_MULT_SUB_LETTER] = \
        dset[cb.COL_MULT_SUB_LETTER].fillna("")

    return dset


def preprocess_results(dset, sname="Results", replace_na=False):
    """ Preprocess the data from the Results sheet
    """

    lg.print_tstamp(f"PPROC actions for '{sname}' sheet")

    # rename columns for clarity
    # ---------------------------
    dset = pp.rename_columns(dset)

    # preprocess institution name
    # ---------------------------
    dset = preprocess_inst_name(dset)

    # replace - in a list of columns with na
    # --------------------------------------
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

    if replace_na:
        # replace missing values in object columns
        # ----------------------------------------
        columns_to_fill = dset.select_dtypes(include=['object']).columns.to_list()
        dset[columns_to_fill] = dset[columns_to_fill].fillna(cb.VALUE_ADDED_NOT_SPECIFIED)
        lg.print_tstamp(f"- PPROC: replace missing values with '{cb.VALUE_ADDED_NOT_SPECIFIED}'")

    # bin percentages
    # ---------------
    # COL_RESULTS_PERC_STAFF_SUBMITTED, COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT not binned, not < 100%
    columns = [cb.COL_RESULTS_4star,
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
    columns_to_drop = [cb.COL_INST_CODE_BRACKETS,
                       cb.COL_RESULTS_SORT_ORDER]
    for column in columns_to_drop:
        dset_stats = dset[column].value_counts().to_frame(name="count")
        dset_stats.index.name = column
        dset = dset.drop(column, axis=1)
        lg.print_tstamp(f"- PPROC: drop column '{column}'")
        # print(f"{dset_stats}")

    # setup the pivoting action
    columns_index = [cb.COL_INST_NAME,
                     cb.COL_PANEL_NAME,
                     cb.COL_UOA_NAME,
                     cb.COL_MULT_SUB_LETTER,
                     cb.COL_MULT_SUB_NAME,
                     cb.COL_JOINT_SUB]
    column_pivot = cb.COL_RESULTS_PROFILE
    column_pivot_values = sorted(dset[column_pivot].unique())

    # first two are assumed to the perc staff submitted that have the same value for all profiles
    # for which duplicates are dropped and the column name is changed
    columns_values = [cb.COL_RESULTS_PERC_STAFF_SUBMITTED,
                      cb.COL_RESULTS_TOTAL_FTE_SUBMITTED_JOINT,
                      cb.COL_RESULTS_4star,
                      cb.COL_RESULTS_3star,
                      cb.COL_RESULTS_2star,
                      cb.COL_RESULTS_1star,
                      cb.COL_RESULTS_UNCLASSIFIED]
    columns_values.extend([f"{column} (binned)" for column in columns_values[2:]])
    suffix = "evaluation"

    # columns to drop from the wide format because they are duplicates
    columns_to_drop = [f"{pivot_value} {suffix} - {column_value}"
                       for pivot_value in column_pivot_values[1:]
                       for column_value in columns_values[:2]]
    # these are not binned as not < 100%
    # columns_to_drop.extend([f"{column} (binned)" for column in columns_to_drop])

    # columms to rename in the wide format after dropping the duplicates
    columns_to_rename = {}
    for column_value in columns_values[:2]:
        label = f"{column_pivot_values[0]} {suffix} - {column_value}"
        columns_to_rename[label] = f"{column_value}"
        # label = f"{column_pivot_values[0]} {suffix} - {column_value} (binned)"
        # columns_to_rename[label] = f"{column_value} (binned)"

    # pivot and drop duplcate columns
    dset = dset.pivot(index=columns_index, columns=column_pivot, values=columns_values)
    columns = [f'{column[1]} {suffix} - {column[0]}' for column in dset.columns]
    dset.columns = columns
    dset = dset[sorted(columns)]
    dset.drop(columns=columns_to_drop, inplace=True)

    # rename columns and move the re-named columns to the front
    dset.rename(columns=columns_to_rename, inplace=True)
    columns = [column for column in columns_to_rename.values()]
    columns.extend([column for column in dset.columns.tolist()
                    if column not in columns_to_rename.values()])
    dset = dset[columns]

    # flatten index
    dset.reset_index(inplace=True)

    # replace na in COL_MULT_SUB_LETTER with VALUE_ADDED_NOT_SPECIFIED to enable merge
    dset[cb.COL_MULT_SUB_LETTER] = dset[cb.COL_MULT_SUB_LETTER].fillna("")

    # prepare to merge with extra information
    # ---------------------------------------
    # columns for merging the extra information
    columns_index = [cb.COL_INST_NAME,
                     cb.COL_UOA_NAME,
                     cb.COL_MULT_SUB_LETTER]

    # read and merge information from research groups
    # -----------------------------------------------
    infname = rw.DATA_PPROC_RGROUPS
    dset_extra = pd.read_csv(infname, compression='gzip')

    # replace na in cb.COL_MULT_SUB_LETTER with "" for merging
    dset_extra[cb.COL_MULT_SUB_LETTER] = \
        dset_extra[cb.COL_MULT_SUB_LETTER].fillna("")
    column_name = "Research group submissions"
    dset_stats = dset_extra[columns_index].value_counts()\
                                          .to_frame(name=column_name)\
                                          .reset_index()
    dset = pd.merge(dset, dset_stats, how='left', on=columns_index)
    dset[column_name] = dset[column_name].fillna(0)

    lg.print_tstamp(f"- PPROC: added column '{column_name}'")
    if dset_extra.shape[0] != dset[column_name].sum():
        lg.print_tstamp(f"WARNING: {dset_extra.shape[0]} != {dset[column_name].sum()}")


    # read and merge the information from outputs
    infname = rw.DATA_PPROC_OUTPUTS
    dset_extra = pd.read_csv(infname, compression='gzip')

    # replace na in cb.COL_MULT_SUB_LETTER with "" for merging
    dset_extra[cb.COL_MULT_SUB_LETTER] = \
        dset_extra[cb.COL_MULT_SUB_LETTER].fillna("")

    column_name = "Output submissions"
    dset_stats = dset_extra[columns_index].value_counts()\
                                          .to_frame(name=column_name)\
                                          .reset_index()
    dset = pd.merge(dset, dset_stats, how='left', on=columns_index)
    dset[column_name] = dset[column_name].fillna(0)

    lg.print_tstamp(f"- PPROC: added column '{column_name}'")
    if dset_extra.shape[0] != dset[column_name].sum():
        lg.print_tstamp(f"WARNING: {dset_extra.shape[0]} != {dset[column_name].sum()}")

    column_to_count = "Output type"
    for value in dset_extra[column_to_count].unique():
        selected_indices = dset_extra[column_to_count] == value
        column_selected = f"{column_name} - {value}"
        dset_stats = dset_extra.loc[selected_indices, columns_index].value_counts()\
                                          .to_frame(name=column_selected)\
                                          .reset_index()
        dset = pd.merge(dset, dset_stats, how='left', on=columns_index)
        dset[column_selected] = dset[column_selected].fillna(0)
        lg.print_tstamp(f"- PPROC: added column '{column_selected}'")
        nrecords =  dset_extra.loc[selected_indices, column_to_count].shape[0]
        entries_count = dset[column_selected].sum()
        if nrecords != entries_count:
            lg.print_tstamp(f"WARNING: {nrecords} != {entries_count}")

    return dset


def preprocess_sheet(sname, mode="production"):
    """ Preprocess a sheet from the raw data.

    Args:
        sname (str): Name of the sheet to preprocess.
    """

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    if mode == "production":
        sys.stdout = buffer

    # read data
    # ---------
    infname = os.path.join(rw.PROCESSED_SHEETS_PATH, f"{sname}{rw.DATA_EXT}")
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
    fname = os.path.join(rw.PROCESSED_SHEETS_PATH, f"{sname}{rw.DATA_PPROCESS}{rw.DATA_EXT}")
    dset.to_csv(os.path.join(rw.PROJECT_PATH, fname),
                index=True,
                compression='gzip')
    lg.print_tstamp(f"SAVED pre-processed dataset to '{fname}'")

    # # REVERT THIS
    # if sname == "Results":
    #     lg.print_tstamp(f"PPROC merge with unit environment statements for '{sname}' sheet")
    #     # read unit environment statements, merge and save
    #     # -----------------------------------------------
    #     infname = rw.DATA_PREPARE_ENV_UNIT
    #     dset_uenv = pd.read_csv(infname, compression='gzip')
    #     lg.print_tstamp(f"- READ '{infname}': {dset_uenv.shape[0]} records")

    #     columns_index = [cb.COL_INST_NAME,
    #                      cb.COL_UOA_NAME,
    #                      cb.COL_MULT_SUB_LETTER]
    #     dset = pd.merge(dset, dset_uenv, how='left', on=columns_index)
    #     lg.print_tstamp(f"- MERGED {sname} with unit environment statements': "
    #                     f"{dset.shape[0]} records")

    #     fname = os.path.join(rw.PROCESSED_SHEETS_PATH,
    #                          f"{sname}{rw.DATA_PPROCESS}_uenv{rw.DATA_EXT}")
    #     dset.to_csv(os.path.join(rw.PROJECT_PATH, fname),
    #                 index=True,
    #                 compression='gzip')
    #     lg.print_tstamp(f"SAVED merged dataset to '{fname}'")

    # provision for saving as parquet, not used right now
    # fname = os.path.join(rw.PROCESSED_SHEETS_PATH, f"{sname}{rw.DATA_PPROCESS}.parquet")
    # dset.to_parquet(os.path.join(rw.PROJECT_PATH, fname),
    #                 index=True,
    #                 compression='gzip')
    # lg.print_tstamp(f"SAVED pre-processed dataset to '{fname}'")

    # delete infname
    # --------------
    if mode == "production":
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

    # add a mode argument with a default value
    parser.add_argument("-m", "--mode",
                        required=False,
                        default="production",
                        help="mode of operation: production, develop")

    args = parser.parse_args()
    sname = args.sheetname
    preprocess_sheet(sname, args.mode)
