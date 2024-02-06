""" Utilities for REF2021 processing. """
import os
import logging
import pandas as pd

import REF2021_processing.read_write as rw
import REF2021_processing.codebook as cb

COMPLETED_ICON = "\033[32m\u2713\033[0m"
FAILED_ICON = "\033[31m\u2717\033[0m"
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

PERCENTAGE_BINS = range(0, 101, 10)

TO_RENAME = {
    "Main panel": "Main panel code",
    "Output type": "Output type code",
}

TO_REPLACE = ["/", ":"]


def add_verbose_parser_argument(parser):
    """Add verbose parser argument.

    Args:
        parser (argparse.ArgumentParser): Parser.

    Returns:
        argparse.ArgumentParser: Parser with added verbose argument.
    """

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        choices=[True, False],
        help="write logging to console, default false",
    )

    return parser


def setup_logger(source, verbose=True):
    """Setup logger.

    Args:
        source (str): data source for the logged processing
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{source}{rw.LOGS['extension']}"
        fpath = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['interim_path']}{fname}")

        # make folders that do not exist and delete previous log files
        for folder in [rw.LOGS["path"], rw.LOGS["interim_path"]]:
            if not os.path.exists(folder):
                os.makedirs(folder)
            if os.path.exists(f"{folder}{fname}"):
                os.remove(f"{folder}{fname}")
    except OSError as e:
        print(f"{FAILED_ICON} failed: setup logger {e}")
        return False

    handlers = [logging.FileHandler(fpath)]

    if verbose:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, handlers=handlers)
    return True


def complete_logger(source, verbose=True):
    """Complete logger.

    Args:
        source (str): Data source for the logged processing.
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{source}{rw.LOGS['extension']}"
        fpath_interim = os.path.join(
            rw.PROJECT_PATH, f"{rw.LOGS['interim_path']}{fname}"
        )
        fpath = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['path']}{fname}")

        # move log file to the logs folder
        os.rename(fpath_interim, fpath)
        if verbose:
            print(f"{COMPLETED_ICON} moved log file to {fpath}")

        return True
    except OSError as e:
        print(f"{FAILED_ICON} failed: complete logger {e}")
        return False


def drop_specified_columns(dset, columns_to_drop, sname):
    """Drop specified columns from the dataset.

    Args:
        dset (pandas.DataFrame): Dataset.
        columns_to_drop (list): Columns to drop.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with specified columns dropped.
    """

    columns_to_drop = list(set(columns_to_drop).intersection(dset.columns))
    if len(columns_to_drop) > 0:
        dset = dset.drop(columns_to_drop, axis=1)
        logging.info("%s - drop columns '%s'", sname, columns_to_drop)

    return dset


def make_columns_categorical(dset, columns, sname):
    """Make specified columns categorical.

    Args:
        dset (pandas.DataFrame): Dataset.
        columns (list): Columns to make categorical.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with specified columns made categorical.
    """

    columns_to_category = list(set(columns).intersection(dset.columns))
    if len(columns_to_category) > 0:
        logging.info("%s - make categorical %s", sname, columns_to_category)
        for column in columns_to_category:
            dset[column] = pd.Categorical(dset[column])

    return dset


def fix_mult_sub_letter(dset, sname):
    """Fix mult sub letter column.

    Args:
        dset (pandas.DataFrame): Dataset.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with fixed mult sub letter column.
    """

    if cb.COL_MULT_SUB_LETTER in dset.columns:
        dset[cb.COL_MULT_SUB_LETTER] = dset[cb.COL_MULT_SUB_LETTER].fillna("")
        logging.info("%s - replace na with '' in %s", sname, cb.COL_MULT_SUB_LETTER)

    return dset


def get_info_from_filename(fname):
    """Get information from the filename.

    Args:
        fname (str): filename

    Returns:
        tuple: institution name, unit code, multiple submission letter
    """

    institution_name, unit_code_original = fname.split(" - ")

    # process tbe unit code and the multiple submission letter
    unit_code = "".join([i for i in unit_code_original if not i.isalpha()])
    multiple_submission_letter = ""
    if len(unit_code) != len(unit_code_original):
        multiple_submission_letter = unit_code_original[-1]

    return institution_name, unit_code, multiple_submission_letter


def clean_styling(dset, column):
    """Clean the styling in a column of a dataset.

    Args:
        dset (pandas.DataFrame): dataset to process
        column (str): column name

    Returns:
        pandas.DataFrame: Dataset with cleaned column.
    """

    text_instructions = [
        "(indicative maximum 100 words)",
        "(indicative maximum 500 words)",
        "(indicative maximum 750 words)",
        " (indicative maximum of six references)",
    ]
    text_to_replace = {
        "  ": " ",
        "‚Äò": "",  # misread left single quote
        "‚Äô": "’",  # misread right single quote or apostrophe
        "#": "",
        "*": "",
        r"\(": "(",
        r"\)": ")",
        r"\[": "[",
        r"\]": "]",
        r"\-": "-",
        "<ins>": "",  # html tag for underline
        "</ins>": "",  # html tag for underline
        "<sup>": "",  # html tag for superscript
        "</sup>": "",  # html tag for superscript
        "<sub>": "",  # html tag for subscript
        "</sub>": "",  # html tag for subscript
        "\n": " ",
        "\t": " ",
    }

    for key, value in text_to_replace.items():
        dset[column] = dset[column].str.replace(key, value, regex=False)

    dset[column] = dset[column].str.replace(column, " ", regex=False)
    dset[column] = dset[column].str.replace(column[2:], " ", regex=False)

    for text in text_instructions:
        dset[column] = dset[column].str.replace(text, "", regex=False)

    return dset


def clean_fnames(fnames, template="", extension="", do_sort=True):
    """Clean a list of filenames by removing a template and an extension.

    Args:
        fnames (list): List of filenames to clean.
        template (str): Template to remove from the filenames.
        extension (str): Extension to remove from the filenames.
        do_sort (bool): If True, sort the filenames.

    Returns:
        list: List of cleaned filenames. Filenames are sorted if do_sort is True.
    """

    cleaned_fnames = [
        fname.replace(template, "").replace(extension, "") for fname in fnames
    ]
    if do_sort:
        cleaned_fnames.sort()

    return cleaned_fnames


def rename_columns(dset, sname):
    """Rename columns in a dataset.

    Args:
        dset (pandas.DataFrame): dataset to process
        sname (str): label for the dataset

    Returns:
        pandas.DataFrame: Dataset with renamed columns.
    """

    for key, value in TO_RENAME.items():
        if key in dset.columns:
            dset = dset.rename(columns={key: value})
            logging.info("%s - rename '%s' to '%s'", sname, key, value)

    return dset


def preprocess_inst_name(dset, sname):
    """Preprocess the institution name column
        to replace characters that are not allowed in filenames.

    Args:
        dset (pd.DataFrame): Dataset to preprocess
        sname (str): label for the dataset

    Returns:
        pd.DataFrame:  Dataset with cb.COL_INST_NAME column processed.
    """

    for char_to_replace in TO_REPLACE:
        dset[cb.COL_INST_NAME] = dset[cb.COL_INST_NAME].str.replace(
            char_to_replace, "_"
        )
    logging.info(
        "%s - replace '%s' with '_' in '%s'", sname, TO_REPLACE, cb.COL_INST_NAME
    )

    return dset


def bin_percentages_labels():
    """Create bin percentage labels.

    Returns:
        labels (list): list of labels
    """

    bins = PERCENTAGE_BINS
    labels = [f"{bins[i]} to {bins[i+1]} %" for i in range(len(bins) - 1)]
    # labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins)-1)]
    # labels[0] = f"[{bins[0]}, {bins[1]}]"

    return labels


def bin_percentages(dset, column, column_binned):
    """Bin percentages in a column of a dataset.

    Args:
        dset (pandas.DataFrame): dataset
        column (str): column name
        column_binned (str): new column name for the binned column

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    labels = bin_percentages_labels()
    # labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins)-1)]
    # labels[0] = f"[{bins[0]}, {bins[1]}]"
    dset[column_binned] = pd.cut(
        dset[column],
        bins=PERCENTAGE_BINS,
        right=True,
        include_lowest=True,
        labels=labels,
    )
    dset[column_binned] = pd.Categorical(dset[column_binned])

    return dset


def move_last_column(dset, column_before):
    """Move a the last column to the right of specified column.

    Args:
        dset (pandas.DataFrame): dataset
        column_before (str): column name

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """
    columns = dset.columns.tolist()
    index = columns.index(column_before)
    item = columns.pop()
    columns.insert(index + 1, item)
    dset = dset.reindex(columns=columns)

    return dset


def pivot_results_by_profile(dset, sname):
    """Pivot the results by profile to make a wide format for analyses.

    Args:
        dset (pandas.DataFrame): dataset
        sname (str): label for the dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

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
    columns_values.extend(cb.COLUMNS_STARS)
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

    # flatten index
    dset.reset_index(inplace=True)

    return dset


def merge_results_with_groups(dset):
    """Merge results with the number of research group submissions.

    Args:
        dset (pandas.DataFrame): dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    sname = rw.SOURCES["results"]["sheet"]

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

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

    return dset


def merge_results_with_outputs(dset):
    """Merge results with the number of output submissions.

    Args:
        dset (pandas.DataFrame): dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    sname = rw.SOURCES["results"]["sheet"]

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

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

    return dset


def merge_results_with_impacts(dset):
    """Merge results with the number of impact submissions.

    Args:
        dset (pandas.DataFrame): dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    sname = rw.SOURCES["results"]["sheet"]

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

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

    return dset


def merge_results_with_degrees(dset):
    """Merge results with the number of degrees awarded.

    Args:
        dset (pandas.DataFrame): dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    sname = rw.SOURCES["results"]["sheet"]

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

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

    return dset


def merge_results_with_uenvstatements(dset):
    """Merge results with the number of environment statements.

    Args:
        dset (pandas.DataFrame): dataset

    Returns:
        dset (pandas.DataFrame): dataset with new column
    """

    sname = rw.SOURCES["results"]["sheet"]

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]

    infname = os.path.join(
        rw.PROJECT_PATH,
        f"{rw.SOURCES['environment_statements']['unit']['output_path']}"
        f"{rw.SOURCES['environment_statements']['unit']['name']}{rw.OUTPUT_EXTENSION}",
    )
    dset_extra = rw.read_dataframe(infname, sname)

    # replace na in cb.COL_MULT_SUB_LETTER with "" for merging
    dset_extra[cb.COL_MULT_SUB_LETTER] = dset_extra[cb.COL_MULT_SUB_LETTER].fillna("")

    columns_index = [cb.COL_INST_NAME, cb.COL_UOA_NAME, cb.COL_MULT_SUB_LETTER]
    dset = pd.merge(dset, dset_extra, how="left", on=columns_index)
    logging.info(
        "%s - merged with unit environment statements: %d records",
        sname,
        dset.shape[0],
    )

    # add suffix to added columns
    columns_to_rename = {}
    for column in dset.columns:
        if column not in dset.columns:
            columns_to_rename[column] = f"{column}{cb.COLUMN_NAME_ADDED_SUFFIX}"
    dset.rename(columns=columns_to_rename, inplace=True)

    return dset
