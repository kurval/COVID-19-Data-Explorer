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

class Graph:
    def __init__(self, chart_name, ylabel):
        self.chart_name = chart_name
        self.ylabel = ylabel

    def set_info(self):
        ax.set_title(self.chart_name.title(), fontdict={'fontsize':22})
        ax.set_xlabel('Date', fontdict={'fontsize':15})
        ax.set_ylabel(self.ylabel, fontdict={'fontsize':15})

    def show_graph(self, youngest, stardate):
        plt.xticks(fontsize=8, rotation=70, ha="right")
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.legend()
        plt.xlim([stardate, youngest + timedelta(days=1)])
        plt.tight_layout()
        plt.show()

youngest = max(df['date'])
oldest = min(df['date'])

# Sort country names
df.drop(df.loc[df['location'] == "Cote d'Ivoire"].index, inplace=True)
countries = np.sort(df.location.unique())
df['location'] = df['location'].str.lower()

# Choose stats
chart = choose_chart()
if chart == 1 or chart == 2:
    chart, ylabel = ('total_cases', 'Cases') if chart == 1 else ('total_deaths', 'Deaths')
else:
    chart, ylabel = ('new_cases', 'Cases') if chart == 3 else ('new_deaths', 'Deaths')

# Creating new line graph
new_graph = Graph(chart, ylabel)
fig, ax = plt.subplots(figsize=(15,7))
new_graph.set_info()

# Adding countries to graph
print("\nOptions:\n\n".upper(), np.array2string(countries, max_line_width=150, separator=', ').replace("'", ''))
countries = np.char.lower(countries.astype(str))
while True:
    new_country = choose_country(countries)
    if not new_country:
        break
    new_df = df.loc[df['location'] == new_country]
    if chart == 'new_cases' or chart == 'new_deaths':
        new_df.set_index('date',inplace=True)
        ax.bar(new_df.index, new_df[chart])
        break
    plt.plot(new_df.date, new_df[chart], marker='.', label=new_country.title())

# Adjust time period and show graph
stardate = choose_time_period(youngest)
new_graph.show_graph(youngest, stardate)