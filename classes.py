#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

title_font = {'fontweight':'bold', 'fontsize':22}
label_font = {'weight':'bold', 'fontsize': 15}

class Graph:
    def __init__(self, chart_name, ylabel, xlabel):
        self.chart_name = chart_name
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.fig, self.ax = plt.subplots(num='COVID-19', figsize=(15,7))

    def set_info(self):
        self.ax.set_title(self.chart_name, fontdict=title_font)
        self.ax.set_xlabel(self.xlabel.title(), fontdict=label_font)
        self.ax.set_ylabel(self.ylabel.title(), fontdict=label_font)

    def ajust_graph(self, youngest, stardate):
        plt.xticks(fontsize=8, rotation=50, ha="right")
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.legend(loc=2)
        plt.tight_layout()
        plt.xlim([stardate, youngest + timedelta(days=1)])