import streamlit as st

source_url = "https://results2021.ref.ac.uk/"

page_title = "REF 2021 Data Explorer"
page_sidebar = "Home"
st.set_page_config(page_title=page_title,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )

st.title(page_title)
st.sidebar.markdown(f"# {page_sidebar}")

st.sidebar.success("Select a visualisation from the sidebar to start exploring the data.")

# page content
st.markdown("## Data source")
st.markdown(f"The data used in this app is from the [REF 2021 website]({source_url})"
            ", accessed 2023/08/10.")
