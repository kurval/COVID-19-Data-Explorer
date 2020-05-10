#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
from option_functions import choose_chart, choose_country, choose_time_period
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
        self.scale = 0
    
    def set_info(self):
        plt.figure(num='COVID-19', figsize=(8,5))
        plt.title(self.chart_name.title(), fontdict={'fontsize':22})
        plt.xlabel('Date', fontdict={'fontsize':15})
        plt.ylabel(self.ylabel, fontdict={'fontsize':15})
    
    def set_range(self, oldest, youngest):
        self.scale = np.arange(oldest, youngest)

    def show_graph(self, youngest, stardate):
        plt.xticks([stardate]+new_graph.scale[::5].tolist()+[youngest], fontsize=8, rotation=70, ha="right")
        plt.legend()
        plt.xlim([stardate, youngest])
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
if chart == 1:
    chart = 'total_cases'
    ylabel = 'Cases'
else:
    chart = 'total_deaths'
    ylabel = 'Deaths'

# Creating new line graph
new_graph = Graph(chart, ylabel)
new_graph.set_info()
new_graph.set_range(oldest, youngest)

# Adding countries to graph
print("\nOptions:\n\n".upper(), np.array2string(countries, max_line_width=150, separator=', ').replace("'", ''))
countries = np.char.lower(countries.astype(str))
new_country = 'default'
while new_country:
    new_country = choose_country(countries)
    for country in countries:
        if country == new_country:
            new_df = df.loc[df['location'] == country]
            plt.plot(new_df.date, new_df[chart], marker='.', label=new_country.title())

# Adjust time period and show graph
stardate = choose_time_period(youngest)
new_graph.show_graph(youngest, stardate)