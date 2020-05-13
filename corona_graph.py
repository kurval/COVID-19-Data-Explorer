#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
from option_functions import choose_chart, choose_country, choose_time_period
from datetime import datetime, timedelta
import matplotlib.dates as mdates
register_matplotlib_converters()

# Import data
results = dw.query(
	'markmarkoh/coronavirus-data', 
    'SELECT * FROM full_data')
df = results.dataframe

stats = {'1':"total_cases", '2':"total_deaths", '3':"new_cases", '4':"new_deaths"}
title_font = {'fontweight':'bold', 'fontsize':22}
label_font = {'weight':'bold', 'fontsize': 15}

class Graph:
    def __init__(self, chart_name, ylabel, xlabel):
        self.chart_name = chart_name
        self.ylabel = ylabel
        self.xlabel = xlabel

    def set_info(self):
        ax.set_title(self.chart_name.title(), fontdict=title_font)
        ax.set_xlabel(self.xlabel, fontdict=label_font)
        ax.set_ylabel(self.ylabel, fontdict=label_font)

    def ajust_graph(self, youngest, stardate):
        plt.xticks(fontsize=8, rotation=50, ha="right")
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.legend(loc=2)
        plt.tight_layout()
        plt.xlim([stardate, youngest + timedelta(days=1)])

youngest = max(df['date'])
oldest = min(df['date'])

#Set style for graph
plt.style.use('ggplot')

#Additional graph
graph2 = Graph('Total cases', 'countries', 'cases')
fig, ax = plt.subplots(figsize=(15,7))
top20 = df.groupby('location')[['new_cases']].sum().sort_values(['new_cases'])[-20:-1].reset_index()
top20.plot(kind='barh', color='#336600', width=0.85, y="new_cases", x="location", ax=ax)
graph2.set_info()
plt.show()

# Choose time prediod
stardate = choose_time_period(youngest)

# Sort country names
df.drop(df.loc[df['location'] == "Cote d'Ivoire"].index, inplace=True)
countries = np.sort(df.location.unique())
df['location'] = df['location'].str.lower()

# Choose stats
chart = stats[choose_chart()]
ylabel = chart.split(sep='_')[-1]

# Creating new graph
new_graph = Graph(chart.replace('_', ' '), ylabel, 'date')
fig, ax = plt.subplots(figsize=(15,7), num='COVID-19')
new_graph.set_info()

# Adding countries to graph
print("\nOptions:\n\n".upper(), np.array2string(countries, max_line_width=150, separator=', ').replace("'", ''))
countries = np.char.lower(countries.astype(str))
while True:
    new_country = choose_country(countries)
    if not new_country:
        break
    new_df = df.loc[(df['location'] == new_country) & (df['date'] > stardate)].reset_index()
    if chart == 'new_cases' or chart == 'new_deaths':
        ax.bar(new_df['date'], new_df[chart], alpha=0.5, label=new_country.title())
    else:
        ax.plot(new_df['date'], new_df[chart], marker='.', label=new_country.title(), linewidth=2, markersize=12)

# Adjust and show graph
new_graph.ajust_graph(youngest, stardate)
plt.show()