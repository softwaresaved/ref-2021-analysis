""" This module contains functions for preprocessing the data """


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
