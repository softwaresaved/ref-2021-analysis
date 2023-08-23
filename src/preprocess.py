""" This module contains functions for preprocessing the data """
import pandas as pd


def clean_styling(dset, column):

    TEXT_INSTRUCTIONS = ["\(indicative maximum 100 words\)",
                         "\(indicative maximum 500 words\)",
                         "\(indicative maximum 750 words\)",
                         " \(indicative maximum of six references\)"
                         ]

    dset[column] = dset[column].str.replace("  ", " ", regex=False)
    dset[column] = dset[column].str.replace("‚Äò", "", regex=False)
    dset[column] = dset[column].str.replace("‚Äô", "", regex=False)
    dset[column] = dset[column].str.replace(column, " ", regex=False)
    dset[column] = dset[column].str.replace(column[2:], " ", regex=False)
    dset[column] = dset[column].str.replace("#", "", regex=False)
    dset[column] = dset[column].str.replace("*", "", regex=False)
    dset[column] = dset[column].str.replace("\n", " ", regex=False)
    dset[column] = dset[column].str.replace("\t", " ", regex=False)

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


def bin_percentages(dset, column, column_binned):
    """ Bin percentages in a column of a dataset.

        Args:
            dset (pandas.DataFrame): dataset
            column (str): column name
            column_binned (str): new column name for the binned column

        Returns:
            dset (pandas.DataFrame): dataset with new column
    """

    bins = range(0, 101, 10)
    labels = [f"({bins[i]}, {bins[i+1]}]" for i in range(len(bins)-1)]
    labels[0] = f"[{bins[0]}, {bins[1]}]"
    dset[column_binned] = pd.cut(dset[column],
                                 bins=bins,
                                 right=True,
                                 include_lowest=True,
                                 labels=labels
                                 )
    return dset
