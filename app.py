#!/usr/bin/env python3
import datadotworld as dw
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import numpy as np
from Functions.graph_functions import show_most_cases, compare_countries
import timeit
import streamlit as st
import click
from PIL import Image
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
    image = Image.open('./Images/header.png')
    st.image(image, use_column_width=True, caption=f"Updated: {youngest}")
    compare_countries(df)
    st.sidebar.markdown("**Choose statistics from the select box and use sidebar to select countries. \
    You can compare countries by selecting multiple options. \
    Adjust time period one to six months by dragging a slider or just clicking it. \
    Click on the right corner of the fiqure to view fullscreen.**")
    st.markdown('## COVID-19 cases: 20 worst-hit countries')
    show_most_cases('3', df)
    st.markdown('## COVID-19 deaths: 20 worst-hit countries')
    show_most_cases('4', df)

if __name__ == "__main__":
    main()
