#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from Classes.classes import Graph, format_numbers
from Functions.option_functions import choose_chart, choose_time_period
import colorsys
import streamlit as st
from matplotlib.ticker import FuncFormatter

stats = {'1':"total_cases", '2':"total_deaths", '3':"new_cases", '4':"new_deaths"}

# Generates list of colors
@st.cache(show_spinner=False)
def get_N_HexCol(N=20):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

@st.cache(show_spinner=False)
def get_top_values(df, chart):
    top20_values = df.groupby('location')[[chart]].sum().sort_values([chart])[-21:-1].reset_index()
    return top20_values

@st.cache(show_spinner=False)
def get_countries(df):
    countries = np.sort(df['location'].unique())
    return countries

@st.cache(show_spinner=False)
def get_location_values(df, new_country, startdate):
    new_df = df.loc[(df['location'].str.lower() == new_country.lower()) & (df['date'] >= startdate)].reset_index()
    return new_df

def show_most_cases(chart_num, df):
    '''
    Shows 20 countries statistic of most cases/deaths
    Chart nums: '3':"new_cases", '4':"new_deaths"

        param: chart name, dataframe
        type: str, dataframe object
    '''
    formatter = FuncFormatter(format_numbers)
    chart = stats[chart_num]
    stats_name = chart.split(sep='_')[-1]
    graph = Graph('COVID-19 ' + stats_name[:-1] + ' rate per country', 'countries', stats_name, (13,5))
    top20 = get_top_values(df, chart)
    values = top20[chart].apply(formatter).to_numpy()
    top20.plot(kind='barh', color=get_N_HexCol(), width=0.85, y=chart, x='location', ax=graph.ax)
    graph.set_info()
    for i, country in enumerate(top20[chart]):
        graph.ax.text(country, i, " "+values[i], va='center', fontsize=15)
    graph.ax.legend().set_visible(False)
    plt.yticks(fontsize=15, fontweight='bold', color='black')
    plt.xticks(fontsize=15)
    graph.ax.xaxis.set_major_formatter(formatter)
    plt.tight_layout()
    st.pyplot()

def compare_countries(df):
    '''
    Allows user to choose time period of the graph 1 ,3 ,5 months.
    User can choose countries to graph from 210 countries.
    User can also choose statistics type from 1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths.
    Depending statistics type grap is bar graph (3,4) or line graph (1,2)

        param: dataframe
        type: dataframe object
    '''
    countries = get_countries(df)
    youngest = max(df['date'])
    chart = stats[choose_chart()]
    # Reordering figure to show here
    slot_for_graph = st.empty()
    startdate = choose_time_period(youngest)
    ylabel = chart.split(sep='_')[-1]
    new_graph = Graph(chart.replace('_', ' ').title(), ylabel, 'date', (15,7))
    new_graph.set_info()
    st.sidebar.markdown("## Select countries")
    options = st.sidebar.multiselect('', list(countries), default=['Finland'])
    for new_country in options:
        new_df = get_location_values(df, new_country, startdate)
        if chart == 'new_cases' or chart == 'new_deaths':
            new_graph.ax.bar(new_df['date'], new_df[chart], align='edge', alpha=0.5, label=new_country.title())
        else:
            new_graph.ax.plot(new_df['date'], new_df[chart], marker='.', label=new_country.title(), linewidth=2, markersize=12)
    new_graph.ajust_graph()
    slot_for_graph.pyplot()