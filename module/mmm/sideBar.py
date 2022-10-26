import streamlit as st


def sidebarTool():
    with st.sidebar:
        tool_options = st.radio('Select the tool:', ['MMM Model', 'MTA Model', 'Markov Model'])

    return tool_options
