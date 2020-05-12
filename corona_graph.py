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

class Graph:
    def __init__(self, chart_name, ylabel):
        self.chart_name = chart_name
        self.ylabel = ylabel

    def set_info(self):
        ax.set_title(self.chart_name.title(), fontdict={'fontsize':22})
        ax.set_xlabel('date', fontdict={'fontsize':15})
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
chart = stats[choose_chart()]
ylabel = chart.split(sep='_')[-1]

# Creating new graph
new_graph = Graph(chart.replace('_', ' '), ylabel)
plt.style.use('ggplot')
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
        ax.bar(new_df['date'], new_df[chart], alpha=0.5, label=new_country.title())
    else:
        ax.plot(new_df.date, new_df[chart], marker='.', label=new_country.title())

# Adjust time period and show graph
stardate = choose_time_period(youngest)
new_graph.show_graph(youngest, stardate)