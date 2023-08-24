""" Functions for processing the data. """


def calculate_counts(dset, col, sort=True):
    """ Calculate counts and percentages for a column.

    Args:
        dset (pandas.DataFrame): The dataset to use.
        col (str): The column to use
        sort (bool): Whether to sort the counts.
    """

    col_count = "Records"
    col_perc = "Records (%)"
    dset_stats = dset[col].value_counts(sort=sort).to_frame(name=col_count)
    dset_stats[col_perc] = 100 * dset_stats[col_count] / dset.shape[0]
    dset_stats.index.name = col

    return dset_stats
