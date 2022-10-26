import streamlit as st
import numpy as np
import pandas as pd


def readData(file_connection_method):
    if file_connection_method == 'Upload from local.':
        uploaded_file = st.file_uploader('Upload your files', accept_multiple_files=False, type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)