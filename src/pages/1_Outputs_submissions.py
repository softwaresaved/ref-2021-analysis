# import sys
import streamlit as st
import matplotlib.pyplot as plt

# sys.path.append('../')
import codebook as cb
import read_write as rw
import process as proc


page_title = "Outputs submissions"
page_sidebar = page_title

st.title(page_title)
st.sidebar.markdown(f"# {page_sidebar}")

(dset, _) = rw.get_data(rw.DATA_PPROC_OUTPUTS)

st.write(f"Number of submitted outputs: {dset.shape[0]}")

for column in [cb.COL_OUTPUT_TYPE_NAME, cb.COL_OPEN_ACCESS]:
    dset_stats = proc.calculate_counts(dset, column, sort=False)
    st.write(dset_stats)
    column_to_plot = "Records (%)"
    fig, ax = plt.subplots()
    dset_stats[column_to_plot].plot.barh(legend=False,
                                         xlabel="",
                                         ylabel=column_to_plot,
                                         ax=ax,
                                         )
    ax.set_xlim([0, 100])
    st.pyplot(fig)
