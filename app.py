#!/usr/bin/env python3
import datadotworld as dw
import pandas as pd
import numpy as np
from Functions.graph_functions import show_most_cases, compare_countries, show_world_scatter
from Functions.option_functions import choose_chart, choose_time_period
import streamlit as st
import altair as alt
import click
from PIL import Image

DATASET_ID = 'markmarkoh/coronavirus-data'
N_CASES = 'SELECT * FROM new_cases'
N_DEATHS = 'SELECT * FROM new_deaths'
T_CASES = 'SELECT * FROM total_cases'
T_DEATHS = 'SELECT * FROM total_deaths'

labels = {'1':'total cases', '2':'total deaths', '3':'new cases', '4':'new deaths'}

@st.cache(show_spinner=False)
def format_data(df, label):
    '''
    Reformat column names and set date column to datetime type.
    Also converts all the other columns to numeric type(float).
    '''
    df.fillna(0, inplace=True)
    cols = df.columns
    df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric)
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns=lambda x: x.replace('_', ' '))
    df.columns = map(str.title, df.columns)
    df = df.rename(columns={'Date': 'date'})
    long_format = df.melt('date', var_name='countries', value_name=label)
    return long_format

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

    new_cases = format_data(new_cases, labels['3'])
    new_deaths = format_data(new_deaths, labels['4'])
    total_cases = format_data(total_cases, labels['1'])
    total_deaths = format_data(total_deaths, labels['2'])
    return new_cases, new_deaths, total_cases, total_deaths

def main():
    with st.spinner('Please wait...'):
        new_cases, new_deaths, total_cases, total_deaths  = import_data()
    stats = {'1':total_cases, '2':total_deaths, '3':new_cases, '4':new_deaths}

    # Header image with timestamp
    youngest = max(new_cases['date'])
    image = Image.open('./Images/header.png')
    st.image(image, use_column_width=True, caption=f"Updated: {youngest.strftime('%Y-%m-%d')}")

    # Compare countries chart
    chart = choose_chart()
    df = stats[chart]
    countries = df['countries'].unique()
    youngest = max(df['date'])
    # Reordering figure to show here
    slot_for_graph = st.empty()
    slot_for_checkbox = st.empty()

    startdate, period = choose_time_period(youngest, 1)
    st.sidebar.markdown("# Select countries")
    options = st.sidebar.multiselect('Countries:', list(countries), default=['Finland'])
    fig = compare_countries(df, labels[chart], startdate, options, period)
    slot_for_graph.altair_chart(fig, use_container_width=True)

    st.info("ℹ️ You can select countries from the sidebar on the left corner.")

    # Sidebar info
    st.sidebar.markdown("# Tips")
    st.sidebar.info("**Choose statistics from the select box and use sidebar to select or deselect countries. \
    You can compare countries by selecting multiple options. \
    Adjust time period by dragging the slider or just clicking it.\
    Hover over each line/block to see the values.**")

    # Worst-hit countries charts
    st.markdown('## COVID-19: total confirmed cases and deaths in the worst-hit countries')
    slot_for_date = st.empty()
    startdate, period = choose_time_period(max(new_cases['date']), 2, min(new_cases['date']))
    date = startdate.strftime('%Y-%m-%d')
    slot_for_date.markdown(f'***Date {date}***')

    fig1 = show_most_cases(new_cases, startdate, labels['3'])
    st.altair_chart(fig1, use_container_width=True)
    fig2 = show_most_cases(new_deaths, startdate, labels['4'])
    st.altair_chart(fig2, use_container_width=True)

    # World scatter plot
    st.markdown('## COVID-19: new confirmed cases worldwide 🌐')
    st.markdown("Hover over each circle to see the values")
    fig = show_world_scatter(new_cases, labels['3'])
    st.altair_chart(fig, use_container_width=True)

    # Footer info
    st.info("by: V.Kurkela | source: [Github](https://github.com/kurval/COVID-19-Statistics) |\
    data source: [Dataworld](https://data.world/markmarkoh/coronavirus-data) \
    (orginally: [Ourworldindata](https://ourworldindata.org/coronavirus-source-data))")

if __name__ == "__main__":
    main()
