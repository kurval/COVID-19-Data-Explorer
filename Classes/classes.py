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
        plt.xticks(fontsize=10, rotation=50, ha="right")
        plt.yticks(fontsize=10)
        self.ax.yaxis.set_major_formatter(formatter)
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.legend(loc=2)
        plt.tight_layout()
        plt.margins(x=0)