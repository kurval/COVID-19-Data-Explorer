#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
from option_functions import choose_chart, choose_country, choose_time_period
from topgraphs import show_most_cases
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from classes import Graph
register_matplotlib_converters()

# Import data
results = dw.query(
	'markmarkoh/coronavirus-data', 
    'SELECT * FROM full_data')
df = results.dataframe

stats = {'1':"total_cases", '2':"total_deaths", '3':"new_cases", '4':"new_deaths"}

youngest = max(df['date'])
oldest = min(df['date'])

#Set style for graph
plt.style.use('ggplot')

#Additional graph
show_most_cases(stats['3'], df)
show_most_cases(stats['4'], df)

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
new_graph = Graph(chart.replace('_', ' ').title(), ylabel, 'date')
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
        new_graph.ax.bar(new_df['date'], new_df[chart], alpha=0.5, label=new_country.title())
    else:
        new_graph.ax.plot(new_df['date'], new_df[chart], marker='.', label=new_country.title(), linewidth=2, markersize=12)

# Adjust and show graph
new_graph.ajust_graph(youngest, stardate)
plt.show()