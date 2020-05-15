#!/usr/bin/env python3
import datadotworld as dw
from pandas.plotting import register_matplotlib_converters
import pandas as pd
from Functions.graph_functions import show_most_cases, compare_countries
register_matplotlib_converters()

def import_data():
    '''
    Imports data from dataworld.

        return: dataframe object
    '''
    results = dw.query(
        'markmarkoh/coronavirus-data', 
        'SELECT * FROM full_data')
    df = results.dataframe
    return df

def main():
    df = import_data()
    youngest = max(df['date'])
    print(f"Updated: {youngest}")
    show_most_cases('3', df)
    show_most_cases('4', df)
    compare_countries(df, youngest)

if __name__ == "__main__":
    main()
