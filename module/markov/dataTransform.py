import streamlit as st
import numpy as np
import pandas as pd
from .markovTool import *
from .visualPlot import modelPlot


def markovModel(file_connection_method):
    if file_connection_method == 'Upload from local.':
        uploaded_file = st.file_uploader('Upload your files', accept_multiple_files=False, type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = df.astype({'conversion': 'int', 'conversion_value': 'float'})
            df = df.sort_values(['cookie', 'time'], ascending=[False, True])
            df['visit_order'] = df.groupby('cookie').cumcount() + 1
            df_paths = df.groupby('cookie')['channel'].aggregate(lambda x: x.unique().tolist()).reset_index()
    
            df_last_interaction = df.drop_duplicates('cookie', keep='last')[['cookie', 'conversion']]
            df_paths = pd.merge(df_paths, df_last_interaction, how='left', on='cookie')
            
            df_paths['path'] = transform_pathlist(df_paths)
            df_paths = df_paths[['cookie', 'path']]
            list_of_paths = df_paths['path']
            total_conversions = sum(path.count('Conversion') for path in df_paths['path'].tolist())
            base_conversion_rate = total_conversions / len(list_of_paths)
            
            trans_states = transition_states(list_of_paths)
            trans_prob = transition_prob(trans_states, list_of_paths)
            trans_matrix = transition_matrix(list_of_paths, trans_prob)
            removal_effects_dict = removal_effects(trans_matrix, base_conversion_rate)
            attributions = markov_chain_allocations(removal_effects_dict, total_conversions)
            df_plot = pd.json_normalize(attributions).T.reset_index()
            df_plot.columns = ['channel', 'conv']
            fig  = modelPlot(df_plot)
            st.plotly_chart(fig)

            
        elif file_connection_method == 'Connect to BigQuery.':
            st.header('Developing')
            