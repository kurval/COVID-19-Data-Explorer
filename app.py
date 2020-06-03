#!/usr/bin/env python3
import datadotworld as dw
import pandas as pd
import numpy as np
from Functions.graph_functions import show_most_cases, compare_countries, show_world_scatter
from Functions.option_functions import choose_chart, choose_time_period
import streamlit as st
import altair as alt
import click
from datetime import datetime
from datetime import date as dt
from PIL import Image

DATASET_ID = 'vale123/covid-19-complete-dataset'

QUERY = 'SELECT  location, \
        date, \
        total_cases, \
        total_deaths, \
        new_cases, \
        new_deaths, \
        new_cases_per_million, \
        new_deaths_per_million, \
        population \
        FROM owid_covid_data'

# Cache for 6 hours
@st.cache(ttl=3600*6, show_spinner=False)
def import_data():
    '''
    Imports data from dataworld.
    Query a dataset using the var = datadotworld.query('dataset_ID', 'query')
    '''
    result = dw.query(
        DATASET_ID,
        QUERY)
    df = result.dataframe
    df['date'] = pd.to_datetime(df['date'])
    return df

def main():
    with st.spinner('Please wait...'):
        df  = import_data()
    labels = {'1':'total_cases', '2':'total_deaths', '3':'new_cases', '4':'new_deaths', '5':'new_cases_per_million', '6':'new_deaths_per_million'}

    # Header image with timestamp
    youngest = max(df['date'])
    oldest = min(df['date'])
    current = dt.today()
    image = Image.open('./Images/header.png')
    st.image(image, use_column_width=True, caption=f"Updated: {youngest.strftime('%Y-%m-%d')}")
    if (current - datetime.date(youngest)).days > 1:
       st.warning("You can update data by clicking on the righ corner Clear cache 'C' and then Rerun 'R'")
    
    # Compare countries chart
    chart = choose_chart()
    countries = df['location'].unique()
    log = False
    stack = False
    slot_for_checkbox = st.empty()
    # Reordering figure to show here
    slot_for_graph = st.empty()

    startdate, period = choose_time_period(youngest, oldest, 1)
    st.sidebar.markdown("# Select countries")
    options = st.sidebar.multiselect('Countries:', list(countries), default=['Finland'])
    if chart == '1' or chart == '2':
        log = slot_for_checkbox.checkbox("Logarithmic scale", value=False)
    else:
        stack = slot_for_checkbox.checkbox("Stack values", value=True) if len(options) >= 2 else False
    fig = compare_countries(df, labels[chart], startdate, options, period, log, stack)
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
    rate_m = st.checkbox('Per one million of population', value=False)
    label1 = labels['5'] if rate_m else labels['3']
    label2 = labels['6'] if rate_m else labels['4']
    slot_for_date = st.empty()
    startdate, period = choose_time_period(youngest, oldest, 2)
    date = startdate.strftime('%Y-%m-%d')
    slot_for_date.markdown(f'***Date {date}***')

    fig1 = show_most_cases(df, startdate, label1)
    st.altair_chart(fig1, use_container_width=True)
    fig2 = show_most_cases(df, startdate, label2)
    st.altair_chart(fig2, use_container_width=True)

    # World scatter plot
    st.markdown('## COVID-19: new confirmed cases worldwide 🌐')
    st.markdown("Hover over each circle to see the values")
    fig = show_world_scatter(df, labels['3'])
    st.altair_chart(fig, use_container_width=True)

    # Footer info
    st.info("by: V.Kurkela | source: [Github](https://github.com/kurval/COVID-19-Statistics) |\
    data source: [Dataworld](https://data.world/vale123/covid-19-complete-dataset) \
    (orginally: [Ourworldindata](https://ourworldindata.org/coronavirus-source-data))")

if __name__ == "__main__":
    main()
