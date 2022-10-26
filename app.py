import streamlit as st
from module.mmm.linearMMM import mmm_model
from module.mmm.dataTransform import readData
from module.mmm.sideBar import sidebarTool
from module.mta.mtaResult import mtaModel


def run():
    st.set_page_config(
        page_title="Data Modelling",
        page_icon="📈",
        layout="wide",  # centered, wide
        initial_sidebar_state="auto",  # auto, expanded, collapsed
        menu_items={
            "Get Help": "https://www.impersuasion.com/",
            "Report a bug": "mailto:jiaminglow@impersuasion.com",
            "About": "# This is a header. This is an *extremely* cool app!"
        }
    )
    st.title('Budget Allocation')

    tool_option = sidebarTool()
    file_connection_method = st.radio('Select method:', ['Upload from local.', 'Connect to BigQuery.'], horizontal=True)

    if tool_option == 'MMM Model':
        df = readData(file_connection_method)
        mmm_model(df)

    elif tool_option == 'MTA Model':
        mtaModel(file_connection_method)

    elif tool_option == 'Markov Model':
        st.header('Developing')


if __name__ == "__main__":
    run()
