import pandas as pd
from datetime import datetime
import streamlit as st

def choose_chart():
    '''
    Allowing user to choose data type

        return: chart number ('1':total_cases, '2':total_deaths, '3':new_cases, '4':new_deaths,)
    '''
    stats = {'Total cases':'1', 'Total deaths':'2', 'New cases':'3', 'New deaths':'4'}
    charts = ['Total cases', 'Total deaths', 'New cases', 'New deaths']
    chart = st.selectbox('', charts)
    return stats[chart]

def choose_time_period(youngest):
    '''
    Allowing user to choose time period

        param: youngest (newest date)
        type: datetime.date object
        return: startdate (youngest - time period)
        returntype: datetime object
    '''
    period = st.slider('Choose time period (months)', 1, 6, 3)
    startdate = youngest - pd.DateOffset(months=period)
    return startdate