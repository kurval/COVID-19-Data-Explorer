#!/usr/bin/env python3
import datadotworld as dw
import pandas as pd
import numpy as np
from Functions.graph_functions import show_most_cases, compare_countries, show_world_scatter
from Functions.option_functions import choose_chart
import streamlit as st
import click
from PIL import Image

DATASET_ID = 'markmarkoh/coronavirus-data'
N_CASES = 'SELECT * FROM new_cases'
N_DEATHS = 'SELECT * FROM new_deaths'
T_CASES = 'SELECT * FROM total_cases'
T_DEATHS = 'SELECT * FROM total_deaths'

@st.cache(show_spinner=False)
def modify_data(df):
    df.fillna(0, inplace=True)
    cols = df.columns
    df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric)
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns=lambda x: x.replace('_', ' '))
    df.columns = map(str.title, df.columns)
    df = df.rename(columns={'Date': 'date'})
    return df

# Cache for 12 hours
@st.cache(ttl=3600*12, show_spinner=False)
def import_data():
    '''
    Imports data from dataworld.
    Query a dataset using the var = datadotworld.query('dataset_ID', 'query')
    '''
    res_n_cases = dw.query(
        DATASET_ID,
        N_CASES)
    new_cases = res_n_cases.dataframe

    res_n_deaths = dw.query(
        DATASET_ID, 
        N_DEATHS)
    new_deaths = res_n_deaths.dataframe

    res_t_cases = dw.query(
        DATASET_ID, 
        T_CASES)
    total_cases = res_t_cases.dataframe

    res_t_deaths = dw.query(
        DATASET_ID,
        T_DEATHS)
    total_deaths = res_t_deaths.dataframe

    new_cases = modify_data(new_cases)
    new_deaths = modify_data(new_deaths)
    total_cases = modify_data(total_cases)
    total_deaths = modify_data(total_deaths)
    return new_cases, new_deaths, total_cases, total_deaths

def main():
    with st.spinner('Please wait...'):
        new_cases, new_deaths, total_cases, total_deaths  = import_data()
    stats = {'1':total_cases, '2':total_deaths, '3':new_cases, '4':new_deaths}

    youngest = max(new_cases['date'])
    image = Image.open('./Images/header.png')
    st.image(image, use_column_width=True, caption=f"Updated: {youngest.strftime('%Y-%m-%d')}")

    chart = choose_chart()
    compare_countries(stats[chart], chart)
    st.info("ℹ️ You can select countries from the sidebar on the left corner.")

    st.sidebar.markdown("# Tips")
    st.sidebar.info("**Choose statistics from the select box and use sidebar to select or deselect countries. \
    You can compare countries by selecting multiple options. \
    Adjust time period by dragging the slider or just clicking it. \
    You can save your chart by clicking from the three dots on the right corner of the fiqure.**")

    show_most_cases(new_cases, new_deaths)

    show_world_scatter(new_cases)

    st.info("by: V.Kurkela | source: [Github](https://github.com/kurval/COVID-19-Statistics) |\
    data source: [Dataworld](https://data.world/markmarkoh/coronavirus-data) \
    (orginally: [Ourworldindata](https://ourworldindata.org/coronavirus-source-data))")

if __name__ == "__main__":
    main()
