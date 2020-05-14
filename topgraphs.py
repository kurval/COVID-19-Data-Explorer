#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
from classes import Graph
import colorsys

# Generates list of colors
def get_N_HexCol(N=20):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def show_most_cases(chart, df):
    '''
    Shows 20 countries statistic of most cases/deaths

        param: chart name, dataframe
    '''
    stats= chart.split(sep='_')[-1]
    graph = Graph('COVID-19 ' + stats[:-1] + ' rate per country', 'countries', stats)
    top20 = df.groupby('location')[[chart]].sum().sort_values([chart])[-21:-1].reset_index()
    top20.plot(kind='barh', color=get_N_HexCol(), width=0.85, y=chart, x='location', ax=graph.ax)
    graph.set_info()
    for i, country in enumerate(top20[chart]):
        graph.ax.text(country, i, " "+str(country), va='center')
    graph.ax.legend().set_visible(False)
    plt.show()