#!/usr/bin/env python3
import pandas as pd
import numpy as np
from Functions.option_functions import choose_time_period
from Functions.chart_configuration import set_tooltip, configure_label_bar_chart
import streamlit as st
import altair as alt

stats = {'1':"total_cases", '2':"total_deaths", '3':"new_cases", '4':"new_deaths"}

def format_numbers(x):
    if x >= 1000000:
        return '{:1.1f} M'.format(x*1e-6)
    return '{:,}'.format(int(x), ',')

@st.cache(show_spinner=False)
def get_top_values(df, label, date):
    '''
    Gets top20 sorted values from given chart and adds new date and formattes columns.
        param: dataframe, label(value), date(timestamp)
        type: pd df object, str, datetime,  
        return: new dataframe
    '''
    top20_values = df.groupby('countries')[[label]].sum().sort_values([label], ascending=False)[:20].reset_index()
    top20_values['formatted'] = top20_values[label].apply(format_numbers)
    top20_values['date'] = date
    return top20_values

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_values(df, startdate, chart_num, label):
    '''
    Gets all the date from selected time period.
        param: dataframe, startdate, chart_num
        type: pd df object, datetime, int
        return: new dataframe
    '''
    if chart_num == 1:
        new_df = df.loc[df['date'] >= startdate]
    elif chart_num == 2:
        new_df = df.loc[df['date'] <= startdate]
    long_format = new_df.melt('date', var_name='countries', value_name=label)
    return long_format

@st.cache(show_spinner=False)
def modify_data(df):
    '''
    Drops 'International' and 'World' columns.
        param: dataframe
        return: new dataframe
    '''
    new_df = df.drop('International', 1)
    new_df = df.drop('World', 1)
    return new_df

@st.cache(show_spinner=False)
def get_world_data(df):
    new_df = df[['date', 'World']]
    return new_df

def show_most_cases(df1, df2):
    '''
    Creates labeled bar chart of 20 countries most cases and deaths
        param: pd df, pd df
        type: dataframe object
    '''
    df1 = modify_data(df1)
    df2 = modify_data(df2)
    youngest = max(df1['date'])
    oldest = min(df1['date'])
    slot_for_header = st.empty()
    slot_for_date = st.empty()
    startdate, period = choose_time_period(youngest, 2, oldest)
    date = startdate.strftime('%Y-%m-%d')
    slot_for_header.markdown('## COVID-19: total cases and deaths in the worst-hit countries')
    slot_for_date.markdown(f'***Date {date}***')

    chart1 = stats['3']
    label1 = chart1.split(sep='_')[-1]

    chart2 = stats['4']
    label2 = chart2.split(sep='_')[-1]

    long_format1 = get_values(df1, startdate, 2, label1)
    long_format2 = get_values(df2, startdate, 2, label2)

    top20_cases = get_top_values(long_format1, label1, date)
    top20_deaths = get_top_values(long_format2, label2, date)

    fig1 = configure_label_bar_chart(top20_cases, label1, 1)
    fig2 = configure_label_bar_chart(top20_deaths, label2, 2)
    
    st.altair_chart(fig1, use_container_width=True)
    st.altair_chart(fig2, use_container_width=True)

def compare_countries(df, chart_num):
    '''
    Allows user to choose time period and countries for the graph.
    User can also choose statistics type from 1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths.
    Depending statistics type grap is bar graph (3,4) or line graph (1,2)

        param: dataframe, chart num
        type: dataframe object, str
    '''
    countries = df.columns[1:]
    youngest = max(df['date'])
    # Reordering figure to show here
    slot_for_graph = st.empty()
    slot_for_checkbox = st.empty()

    startdate, period = choose_time_period(youngest, 1)
    st.sidebar.markdown("# Select countries")
    options = st.sidebar.multiselect('Countries:', list(countries), default=['Finland'])
    options.insert(0, 'date')
    new_df = df[options]
    label = stats[chart_num].split(sep='_')[-1]
    long_format = get_values(new_df, startdate, 1, label)

    if chart_num == '1' or chart_num == '2':
        chart = alt.Chart(long_format).mark_line(interpolate='basis').encode(
            x = alt.X("date:T", title="Date"),
            y = alt.Y(label + ':Q', title=label.title()),
            color='countries:N',
        ).properties(height=350)
        chart = set_tooltip(long_format, chart, label)
    else:
        stack = slot_for_checkbox.checkbox("Stack values", value=True) if len(options) > 2 else False
        bar_size = {'1':15, '2':7, '3':5, '4':4, '5':3, '6':2}
        chart = alt.Chart(long_format).mark_bar(opacity=0.7, size=bar_size[str(period)]).encode(
            alt.X("date:T", title="Date"),
            alt.Y(label + ':Q', stack=stack, title=label.title()),
            color='countries:N',
            tooltip=[alt.Tooltip('countries', title='country'),
                alt.Tooltip('date'),
                alt.Tooltip(label, format=",.0f")]
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=15,
        ).configure_axisX(
            labelAngle=-30
        ).configure_legend(
            titleFontSize=13,
            labelFontSize=12,
        ).properties(height=350).interactive()

    slot_for_graph.altair_chart(chart, use_container_width=True)

def show_world_scatter(df):
    st.markdown('## COVID-19: new cases worldwide 🌐')
    st.write('')
    world_data = get_world_data(df)

    cases_scale = max(world_data['World'])
    date_scale = max(world_data['date'])
    oldest = min(world_data['date'])
    label = 'cases'
    
    SCALEY=alt.Scale(domain=(0, cases_scale+10000))
    SCALEX=alt.Scale(domain=(oldest, (date_scale + pd.DateOffset(days=3))))
    
    base = alt.Chart(world_data).mark_circle(size=150, opacity=0.5, color='orange').transform_fold(
        fold=['World'],
        as_=['cases', 'y']
    ).encode(
        x= alt.X('date:T', scale=SCALEX, title='Date'),
        y= alt.Y('y:Q', scale=SCALEY, title=label.title()),
        tooltip=[alt.Tooltip('date'),
            alt.Tooltip('World', format=",.0f", title=label)]
    )

    loess = base + base.transform_loess('date', 'y').mark_line(size=4)
    chart = (base + loess).configure_axis(
        labelFontSize=11,
        titleFontSize=15,
    ).configure_legend(
        titleFontSize=13,
        labelFontSize=12,
    ).configure_axisX(
        labelAngle=-30
    ).properties(height=350).interactive()

    st.altair_chart(chart, use_container_width=True)