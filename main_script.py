#!/usr/bin/env python3
import datadotworld as dw
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd
from graph_functions import show_most_cases, compare_countries
register_matplotlib_converters()

def import_data():
    '''
    Imports data from dataworld.
    '''
    results = dw.query(
        'markmarkoh/coronavirus-data', 
        'SELECT * FROM full_data')
    df = results.dataframe
    return df

def main():
    df = import_data()
    youngest = max(df['date'])
    oldest = min(df['date'])
    print(f"Updated: {youngest}")

    plt.style.use('ggplot')
    #show_most_cases('3', df)
    #show_most_cases('4', df)
    df.drop(df.loc[df['location'] == "Cote d'Ivoire"].index, inplace=True)
    countries = np.sort(df['location'].unique())
    df['location'] = df['location'].str.lower()
    compare_countries(df, countries, youngest)

if __name__ == "__main__":
    main()
