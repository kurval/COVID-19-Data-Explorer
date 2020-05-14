#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
from classes import Graph

def show_most_cases(chart, df):
    '''
    Shows 20 countries statistic of most cases/deats
    '''
    stats= chart.split(sep='_')[-1]
    graph2 = Graph('COVID-19 ' + stats + 'rate per country', 'countries', stats)
    graph2.set_info()
    top20 = df.groupby('location')[[chart]].sum().sort_values([chart])[-20:-1].reset_index()
    top20.plot(kind='barh', color='#336600', width=0.85, y=chart, x='location', ax=graph2.ax)
    plt.show()