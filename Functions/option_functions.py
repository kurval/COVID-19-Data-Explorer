import pandas as pd
import streamlit as st

def choose_chart():
    '''
    Allowing user to choose data type

        return: chart number ('1':total_cases, '2':total_deaths, '3':new_cases, '4':new_deaths)
    '''
    stats = {'Total cases':'1', 'Total deaths':'2', 'New cases':'3', 'New deaths':'4'}
    charts = ['Total cases', 'Total deaths', 'New cases', 'New deaths']
    chart = st.selectbox('Choose data type:', charts)
    return stats[chart]

def choose_chart_type():
    '''
    Allowing user to choose chart

        return: chart type number ('1':line_chart, '2':bar_chart)
    '''
    chart_types = {'Line chart':'1', 'Bar chart':'2', }
    charts = ['Line chart', 'Bar chart']
    chart = st.selectbox('Choose chart type:', charts)
    return chart_types[chart]

def choose_time_period(youngest, oldest, key):
    '''
    Allowing user to choose time period

        param: youngest (newest date), oldest (oldest date), slider key
        type: datetime.date object, int
        return: startdate (youngest - time period), time period
        returntype: datetime object, int
    '''
    if key == 1:
        end_date = youngest
        start_date = oldest
        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        period = st.slider('Choose time period (months)', 1, num_months, num_months)
        startdate = youngest - pd.DateOffset(months=period)
    elif key == 2:
        days = (oldest - youngest).days
        period = abs(st.slider('Choose date (days) *default is the most recent date', days, 0, 0))
        startdate = youngest - pd.DateOffset(days=period)
    return startdate, period