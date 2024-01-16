""" This module contains functions for preprocessing the data """
import pandas as pd
import logs as lg

PERCENTAGE_BINS = range(0, 101, 10)

TO_RENAME = {
    "Main panel": "Main panel code",
    # "Unit of assessment name": "Unit of assessment",
    # "Institution name": "Institution",
    # "Research group name": "Research group",
    "Output type": "Output type code",
}


def clean_styling(dset, column):

    TEXT_INSTRUCTIONS = ["(indicative maximum 100 words)",
                         "(indicative maximum 500 words)",
                         "(indicative maximum 750 words)",
                         " (indicative maximum of six references)"
                         ]
    TO_REPLACE = {
        "  ": " ",
        "‚Äò": "",  # misread left single quote
        "‚Äô": "’",  # misread right single quote or apostrophe
        "#": "",
        "*": "",
        "\(": "(",
        "\)": ")",
        "\[": "[",
        "\]": "]",
        "\-": "-",
        "<ins>": "",  # html tag for underline
        "</ins>": "",   # html tag for underline
        "<sup>": "",  # html tag for superscript
        "</sup>": "",   # html tag for superscript
        "<sub>": "",  # html tag for subscript
        "</sub>": "",   # html tag for subscript
        "\n": " ",
        "\t": " ",
    }

    for key, value in TO_REPLACE.items():
        dset[column] = dset[column].str.replace(key, value, regex=False)

    dset[column] = dset[column].str.replace(column, " ", regex=False)
    dset[column] = dset[column].str.replace(column[2:], " ", regex=False)

    for text in TEXT_INSTRUCTIONS:
        dset[column] = dset[column].str.replace(text, "", regex=False)

    return dset


def clean_fnames(fnames, template="", extension="", do_sort=True):
    """ Clean a list of filenames by removing a template and an extension.

    Args:
        fnames (list): List of filenames to clean.
        template (str): Template to remove from the filenames.
        extension (str): Extension to remove from the filenames.
        do_sort (bool): If True, sort the filenames.

    Returns:
        list: List of cleaned filenames. Filenames are sorted if do_sort is True.
    """

    cleaned_fnames = [fname.replace(template, "").replace(extension, "") for fname in fnames]
    if do_sort:
        cleaned_fnames.sort()

    return cleaned_fnames


def rename_columns(dset):
    """ Rename columns in a dataset.

    Args:
        dset (pandas.DataFrame): Dataset.

    Returns:
        pandas.DataFrame: Dataset with renamed columns.
    """
    for key, value in TO_RENAME.items():
        if key in dset.columns:
            dset = dset.rename(columns={key: value})
            lg.print_tstamp(f"- PPROC: rename '{key}' to '{value}'")

    return dset


def bin_percentages_labels():
    """ Create bin percentage labels.

        Returns:
            labels (list): list of labels
    """

    bins = PERCENTAGE_BINS
    labels = [f"{bins[i]} to {bins[i+1]} %" for i in range(len(bins)-1)]
    # labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins)-1)]
    # labels[0] = f"[{bins[0]}, {bins[1]}]"

    return labels


def bin_percentages(dset, column, column_binned):
    """ Bin percentages in a column of a dataset.

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
    dset[column_binned] = pd.cut(dset[column],
                                 bins=PERCENTAGE_BINS,
                                 right=True,
                                 include_lowest=True,
                                 labels=labels
                                 )
    return dset


def move_last_column(dset, column_before):
    """ Move a the last column to the right of specified column.

        Args:
            dset (pandas.DataFrame): dataset
            column_before (str): column name

        Returns:
            dset (pandas.DataFrame): dataset with new column
    """
    columns = dset.columns.tolist()
    index = columns.index(column_before)
    item = columns.pop()
    columns.insert(index+1, item)
    dset = dset.reindex(columns=columns)

    return dset
