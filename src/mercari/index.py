"""
mercari price suggestion
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

@st.cache
def load_data():
    root = os.environ['PROJECT_ROOT']
    df = pd.read_table(f'{root}/dataset/mercari/train.tsv')
    df = df.head(1000)
    return df


def save_1k_model():
    root = os.environ['PROJECT_ROOT']
    df = pd.read_table(f'{root}/dataset/mercari/train.tsv')
    df = df.head(1000)
    df.to_csv(f'{root}/dataset/mercari/train_1k.tsv', sep='\t', index=False)

    df = pd.read_table(f'{root}/dataset/mercari/test.tsv')
    df = df.head(1000)
    df.to_csv(f'{root}/dataset/mercari/test_1k.tsv', sep='\t', index=False)


if __name__ == '__main__':
    st.header('Mercari Price Suggestion')
    
    if st.button('Save 1K data'):
        save_1k_model()
    
    st.subheader('👀 Raw data')
    data = load_data()
    st.dataframe(data)