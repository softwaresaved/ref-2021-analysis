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
