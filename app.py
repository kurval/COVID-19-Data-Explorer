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
    st.markdown(f"*Updated: {youngest}*")
    image = Image.open('./Images/header.png')
    st.image(image, width=600)
    compare_countries(df)
    st.markdown('## COVID-19 cases: 20 worst-hit countries')
    show_most_cases('3', df)
    st.markdown('## COVID-19 deaths: 20 worst-hit countries')
    show_most_cases('4', df)

if __name__ == "__main__":
    main()
