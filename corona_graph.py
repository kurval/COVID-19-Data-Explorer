#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
from graph_functions import show_most_cases, compare_countries
register_matplotlib_converters()

# Import data
results = dw.query(
	'markmarkoh/coronavirus-data', 
    'SELECT * FROM full_data')
df = results.dataframe

youngest = max(df['date'])
oldest = min(df['date'])

# Print timestamp
print(f"Updated: {youngest}")

# Set style for all graphs
plt.style.use('ggplot')

# Showing top 20 countries graphs
show_most_cases('3', df)
show_most_cases('4', df)

# Sort country names
df.drop(df.loc[df['location'] == "Cote d'Ivoire"].index, inplace=True)
countries = np.sort(df.location.unique())
df['location'] = df['location'].str.lower()

# Compare countries graph
compare_countries(df, countries, youngest)
