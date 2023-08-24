""" Visualisations functions"""
import matplotlib.pyplot as plt


def calculate_and_visualise_counts(dset,
                                   col,
                                   do_print=True,
                                   do_plot=None,
                                   plot_xlabel="",
                                   plot_ylabel="",
                                   plot_title="",
                                   sort=True,
                                   figure_size=(10, 10)
                                   ):
    """ Calculate and visualise counts and percentages for a column.

    Args:
        dset (pandas.DataFrame): The dataset to validate.
        col (str): The column to calculate and visualise.
        do_print (bool): Whether to print the counts and percentages.
        do_plot (str): Whether to plot the counts or percentages.
        plot_xlabel (str): The x-axis label for the plot.
        plot_ylabel (str): The y-axis label for the plot.
        figure_size (tuple): The size of the figure.
    """

    col_count = "Records"
    col_perc = "Records (%)"
    # calculate counts and percentages
    dset_stats = dset[col].value_counts(sort=sort).to_frame(name=col_count)
    dset_stats[col_perc] = 100 * dset_stats[col_count] / dset.shape[0]
    dset_stats.index.name = col
    nrecords = dset_stats[col_count].sum()
    if do_print:
        print()
        print(dset_stats.to_string(float_format="{:.2f}".format))

    # plot horizontal barchart for the Records column
    if do_plot is not None:
        col_plot = col_perc if do_plot == "perc" else col_count
        if plot_title == "":
            plot_title = col_plot
        plot_title = f"{plot_title} (total: {nrecords})" if do_plot == "count" else plot_title
        dset_stats[col_plot].plot(kind="barh",
                                  legend=False,
                                  title=plot_title,
                                  xlabel=plot_xlabel,
                                  ylabel=plot_ylabel,
                                  )
        # set the figure size
        plt.gcf().set_size_inches(figure_size)
        plt.show()

    return dset_stats


def align_left(dset):
    """ Align the text in the dataframe to the left.

    Args:
        dset (pandas.DataFrame): The dataset to align.

    Returns:
        pandas.Styler: The aligned dataset.
    """

    dset = dset.style.set_properties(**{'text-align': 'left'})
    dset = dset.set_table_styles([dict(selector='th',
                                  props=[('text-align', 'left')])])

    return dset
