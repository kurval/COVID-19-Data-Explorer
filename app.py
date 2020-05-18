#!/usr/bin/env python3
import datadotworld as dw
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import numpy as np
from Functions.graph_functions import show_most_cases, compare_countries
import timeit
import streamlit as st
import click
register_matplotlib_converters()

@st.cache
def import_data():
    '''
    Imports data from dataworld.

        return: dataframe object
    '''
    results = dw.query(
        'markmarkoh/coronavirus-data', 
        'SELECT * FROM full_data')
    df = results.dataframe
    return df

def main():
    df = import_data()
    youngest = max(df['date'])
    st.markdown(f"*Updated: {youngest}*")
    st.title("COVID-19 Statistics")
    compare_countries(df)
    st.markdown('## Most cases')
    show_most_cases('3', df)
    st.markdown('## Most deaths')
    show_most_cases('4', df)

if __name__ == "__main__":
    main()
