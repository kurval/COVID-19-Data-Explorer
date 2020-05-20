#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

title_font = {'fontweight':'bold', 'fontsize':22}
label_font = {'weight':'bold', 'fontsize': 15}

def format_numbers(x, pos):
    if x >= 1000000:
        return '{:1.1f} M'.format(x*1e-6)
    return '{:,}'.format(int(x), ',')

class Graph:
    '''
    Class for plots
        param: chart_name, ylabel, xlabel, size
        type: str, str, str, (float, float)
        
        methods:
        set_info()
            sets plot title, ylabel and xlabel

        ajust_graph():
            sets yticks, xticks, legend and tight layout
    '''
    plt.style.use('ggplot')
    
    def __init__(self, chart_name, ylabel, xlabel, size):
        self.chart_name = chart_name
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.fig, self.ax = plt.subplots(num='COVID-19', figsize=(size))

    def set_info(self):
        self.ax.set_title(self.chart_name, fontdict=title_font)
        self.ax.set_xlabel(self.xlabel.title(), fontdict=label_font)
        self.ax.set_ylabel(self.ylabel.title(), fontdict=label_font)

    def ajust_graph(self):
        formatter = FuncFormatter(format_numbers)
        plt.xticks(fontsize=15, rotation=40, ha="right")
        plt.yticks(fontsize=15)
        self.ax.yaxis.set_major_formatter(formatter)
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.legend(loc=2, fontsize=15)
        plt.tight_layout()
        plt.margins(x=0)