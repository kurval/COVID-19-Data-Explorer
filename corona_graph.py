#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
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
        plt.figure(num='COVID-19', figsize=(8,5))
        plt.title(self.chart_name.title(), fontdict={'fontsize':22})
        plt.xlabel('Date', fontdict={'fontsize':15})
        plt.ylabel(self.ylabel, fontdict={'fontsize':15})

# Sort country names
df.drop(df.loc[df['location'] == "Cote d'Ivoire"].index, inplace=True)
countries = np.sort(df.location.unique())
df['location'] = df['location'].str.lower()

# Choose stats
print("Options:\n\n1: Total cases\n2: Total deaths\n")
while True:
    try:
        chart = int(input("Choose statistics number: "))
    except ValueError:
        print("\nERROR: Input not number. Try again.")
        continue
    if chart != 1 and chart !=2:
        print("\nERROR: Invalid number. Try again.")
        continue
    else:
        break

if chart == 1:
    chart = 'total_cases'
    ylabel = 'Cases'
else:
    chart = 'total_deaths'
    ylabel = 'Deaths'

# Creating new line graph
new_graph = Graph(chart, ylabel)
new_graph.set_info()

# Set range
youngest = max(df['date'])
oldest = min(df['date'])
scale = np.arange(oldest, youngest)

# User input
print("\nOptions:\n\n".upper(), np.array2string(countries, max_line_width=150, separator=', ').replace("'", ''))
countries = np.char.lower(countries.astype(str))
while True:
    new_country = input("\nEnter country name or hit Enter to continue: ").lower()
    if not new_country:
        break
    elif new_country in countries:
        for country in countries:
            if country == new_country:
                new_df = df.loc[df['location'] == country]
                plt.plot(new_df.date, new_df[chart], marker='.', label=new_country.title())
        print("\nAdded ", new_country.title())
    else:
        print(f"\nERROR: Country '{new_country}' doesn't exist. Try again.")
        continue

# Adjust and show graph
stardate = '2020-03-01'
plt.xticks([stardate]+scale[::5].tolist()+[youngest], fontsize=8, rotation=70, ha="right")
plt.legend()
plt.xlim([stardate, youngest])
plt.tight_layout()
plt.show()