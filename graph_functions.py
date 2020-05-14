#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from classes import Graph
from option_functions import choose_chart, choose_country, choose_time_period
import colorsys

stats = {'1':"total_cases", '2':"total_deaths", '3':"new_cases", '4':"new_deaths"}

# Generates list of colors
def get_N_HexCol(N=20):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def show_most_cases(chart_num, df):
    '''
    Shows 20 countries statistic of most cases/deaths
    Chart nums: '3':"new_cases", '4':"new_deaths"

        param: chart name, dataframe
        type: str, dataframe object
    '''
    chart = stats[chart_num]
    stats_name = chart.split(sep='_')[-1]
    graph = Graph('COVID-19 ' + stats_name[:-1] + ' rate per country', 'countries', stats_name)
    top20 = df.groupby('location')[[chart]].sum().sort_values([chart])[-21:-1].reset_index()
    top20.plot(kind='barh', color=get_N_HexCol(), width=0.85, y=chart, x='location', ax=graph.ax)
    graph.set_info()
    for i, country in enumerate(top20[chart]):
        graph.ax.text(country, i, " "+str(country), va='center')
    graph.ax.legend().set_visible(False)
    plt.show()

def compare_countries(dataframe, youngest):
    '''
    Allows user to choose time period of the graph 1 ,3 ,5 months.
    User can choose countries to graph from 210 countries.
    User can also choose statistics type from 1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths.
    Depending statistics type grap is bar graph (3,4) or line graph (1,2)

        param: dataframe, youngest date
        type: dataframe object, datetime.date
    '''
    df = dataframe.drop(dataframe.loc[dataframe['location'] == "Cote d'Ivoire"].index)
    countries = np.sort(df['location'].unique())
    df['location'] = df['location'].str.lower()
    stardate = choose_time_period(youngest)
    chart = stats[choose_chart()]
    ylabel = chart.split(sep='_')[-1]
    new_graph = Graph(chart.replace('_', ' ').title(), ylabel, 'date')

    new_graph.set_info()
    print("\nOptions:\n\n".upper(), np.array2string(countries, max_line_width=150, separator=', ').replace("'", ''))
    countries = np.char.lower(countries.astype(str))
    new_country = []
    while True:
        new_country.append(choose_country(countries, new_country))
        if new_country[-1] == '0':
            break
        new_df = df.loc[(df['location'] == new_country[-1]) & (df['date'] > stardate)].reset_index()
        if chart == 'new_cases' or chart == 'new_deaths':
            new_graph.ax.bar(new_df['date'], new_df[chart], alpha=0.5, label=new_country[-1].title())
        else:
            new_graph.ax.plot(new_df['date'], new_df[chart], marker='.', label=new_country[-1].title(), linewidth=2, markersize=12)
    new_graph.ajust_graph(youngest, stardate)
    plt.show()