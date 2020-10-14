#!/usr/bin/env python3
import pandas as pd
import streamlit as st
import altair as alt
import colorsys
import random
from Functions.chart_configuration import set_tooltip
from Functions.option_functions import choose_time_period, choose_chart_type

@st.cache(show_spinner=False)
def get_N_HexCol(N=20):
    '''
    Generates list of colors
    '''
    HSV_tuples = [(x * 1.0 / N, 0.6, 0.6) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def format_numbers(x):
    if x >= 1000000:
        return '{:1.1f} M'.format(x*1e-6)
    elif x == 0 or x >= 1:
        return '{:,}'.format(int(x))
    return '{:.3f}'.format(x)
    

@st.cache(show_spinner=False)
def get_top_values(df, label, userdate):
    '''
    Gets top20 sorted values from given chart and adds new date and formattes columns.
        param: dataframe, label(value), userdate(timestamp)
        type: pd df object, str, datetime,  
        return: new dataframe
    '''
    top20_values = df.groupby('location').sum().reset_index()
    top20_values = top20_values.sort_values([label], ascending=False)[:20]
    top20_values['formatted'] = top20_values[label].apply(format_numbers)
    top20_values['date'] = userdate
    top20_values = top20_values[['date', 'location', 'formatted', label]]
    return top20_values

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_values_by_date(df, startdate, chart_num, label, log=False):
    '''
    Gets all the data from selected time period.
        param: dataframe, startdate, label
        type: pd df object, datetime, str
        return: new dataframe
    '''
    if chart_num == 1 and log:
        new_df = df[(df['date'] >= startdate) & (df[label] > 0)]
    elif chart_num == 1:
        new_df = df[(df['date'] >= startdate)]
    elif chart_num == 2:
        new_df = df[df['date'] <= startdate]
    return new_df

@st.cache(show_spinner=False)
def modify_data(df):
    '''
    Filter out 'World' values.
        param: dataframe
        return: new dataframe
    '''
    new_df = df[df.location != 'World']
    return new_df

@st.cache(show_spinner=False)
def get_world_data(df, label):
    '''
    Return only world data in new data frame
    '''
    new_df = df[(df['location'] == 'World')]
    new_df = new_df[['date', label]]
    return new_df

@st.cache(show_spinner=False)
def get_country_values(df, options, label):
    new_df = df.loc[df['location'].isin(options)]
    new_df = new_df[['date', 'location', label]]
    return new_df

@st.cache(show_spinner=False)
def get_continent_values(df, label):
    new_df = df.groupby(['date','continent']).sum().reset_index()
    new_df = new_df[['date', 'continent', label]]
    return new_df

def get_most_cases_chart(df, startdate, label):
    '''
    Creates labeled bar charts of 20 countries most cases and deaths
        param: pd df, startdate, label
        type: dataframe object
    '''
    new_df = modify_data(df)
    new_df = get_values_by_date(new_df, startdate, 2, label)

    top20_cases = get_top_values(new_df, label, startdate)
    margin = max(top20_cases[label]) / 10 if max(top20_cases[label]) > 2 else 1
    SCALE=alt.Scale(domain=(0, int(max(top20_cases[label])) + margin))
    label_title = 'total cases' if label == 'new_cases' or label == 'new_cases_per_million' else 'total deaths'
    bars = alt.Chart(top20_cases).mark_bar().encode(
        x= alt.X(label + ':Q', title=label_title.title(), scale=SCALE),
        y=alt.Y('location:N', sort='-x', title='Countries'),
        color=alt.Color('location:N', legend=None, scale=alt.Scale(range=get_N_HexCol())),
        tooltip=[alt.Tooltip('date:T'),
            alt.Tooltip('location', title='country'),
            alt.Tooltip(label+':Q', format=",.0f", title=label_title)],
    )

    text = bars.mark_text(
        fontSize=13,
        align='left',
        baseline='middle',
        dx=3,
    ).encode(
        text='formatted'
    )
    
    chart = (bars + text).configure_axis(
        labelFontSize=11,
        titleFontSize=13,
        titleColor='grey'
    ).configure_axisY(
        labelFontSize=12,
        labelFontWeight='bold'
    ).configure_axisX(
        labelAngle=-30
    ).properties(
        height=520
    ).interactive()

    return chart

def get_compare_countries_chart(df, label, chart_type, startdate, options, period, log, stack):
    '''
    Allows user to choose time period and countries for the graph.
    User can also choose statistics type from 1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths.
    Depending statistics type grap is bar graph (3,4) or line graph (1,2)

        param: dataframe, label, startdate, options(countries), period
        type: dataframe object, str, datetime, list(str), int 
    '''
    
    new_df = get_country_values(df, options, label)
    new_df = get_values_by_date(new_df, startdate, 1, label, log)
    scale_type = 'log' if log else 'linear'
    scale_name = ' (logarithmic scale)' if log else ' (linear scale)'
    grid = False if log else True
    if chart_type == '1':
        chart = alt.Chart(new_df).mark_line(interpolate='basis').encode(
            x = alt.X("date:T", title="Date"),
            y = alt.Y(label + ':Q', title=label.replace('_', ' ').title() + scale_name, scale=alt.Scale(type=scale_type), axis=alt.Axis(tickCount=5, grid=grid, ticks=grid)),
            color=alt.Color('location:N', legend=alt.Legend(title='countries')),
        )
        chart = set_tooltip(new_df, chart, label)
    else:
        bar_scale = {'1':15, '2':7, '3':5, '4':4, '5':3, '6':2}
        bar_size = 1 if period > 6 else bar_scale[str(period)]
        chart = alt.Chart(new_df).mark_bar(opacity=0.7, size=bar_size).encode(
            alt.X("date:T", title="Date"),
            alt.Y(label + ':Q', stack=stack, title=label.replace('_', ' ').title()),
            color='location:N',
            tooltip=[alt.Tooltip('location', title='country'),
                alt.Tooltip('date'),
                alt.Tooltip(label, format=",.0f", title=label.replace('_', ' '))]
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=13,
            titleColor='grey'
        ).configure_axisX(
            labelAngle=-30,
        ).configure_legend(
            titleFontSize=13,
            labelFontSize=12,
        ).properties(height=350).interactive()

    return chart

def show_world_scatter(df, label):
    '''
    Creates scatter plot with LOESS lines
    '''
    world_data = get_world_data(df, label)
    cases_scale = max(world_data[label])
    date_scale = max(world_data['date'])
    oldest = min(world_data['date'])
    SCALEY=alt.Scale(domain=(0, cases_scale+10000))
    SCALEX=alt.Scale(domain=(oldest, (date_scale + pd.DateOffset(days=3))))
    
    base = alt.Chart(world_data).mark_circle(size=150, opacity=0.5).transform_fold(
        fold=[label],
        as_=['cases', 'y']
    ).encode(
        x= alt.X('date:T', scale=SCALEX, title='Date'),
        y= alt.Y('y:Q', scale=SCALEY, title=label.replace('_', ' ').title()),
        fill=alt.Color(label + ':Q', legend=alt.Legend(title=label.replace('_', ' '))),
        tooltip=[alt.Tooltip('date'),
            alt.Tooltip(label, format=",.0f", title=label.replace('_', ' '))]
    )

    loess = base + base.transform_loess('date', 'y').mark_line(size=4)
    chart = (base + loess).configure_axis(
        labelFontSize=11,
        titleFontSize=13,
        titleColor='grey'
    ).configure_legend(
        titleFontSize=13,
        labelFontSize=12,
    ).configure_axisX(
        labelAngle=-30
    ).properties(height=350).interactive()

    return chart

def continent_cases(df, label):
    '''
    Creates chart of new cases of each continents
    '''
    new_df = modify_data(df)
    new_df = get_continent_values(df, label)
    chart = alt.Chart(new_df).transform_filter(
        alt.datum.location != 'World'
    ).mark_area().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y(label+':Q', title=None),
        color='continent:N',
        row=alt.Row('continent:N', title=label.replace('_', ' ').title()),
        tooltip=[alt.Tooltip('date:T'),
            alt.Tooltip('continent', title='continent'),
            alt.Tooltip(label+':Q', format=",.0f", title=label.replace('_', ' '))],
    ).configure_header(
        titleColor='grey',
        titleFontSize=13,
        labelFontSize=12,
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=13,
        titleColor='grey'
    ).configure_axisX(
        labelAngle=-30,
    ).configure_legend(
        titleFontSize=13,
        labelFontSize=12,
    ).properties(height=60).resolve_scale(y='independent').interactive()

    return chart

def show_worst_hit_chart(df, chart, youngest, oldest):
    '''
    Shows worst hit countries char depending chart type:
    '1' = Total cases
    '2' = Total deaths
    '''

    labels = {
        '1':'new_cases',
        '2':'new_deaths',
    }
    
    if (chart == '1'):
        st.markdown("""
        ## COVID-19: total confirmed cases in the worst-hit countries
        """)
    else:
        st.markdown("""
        ## COVID-19: total deaths in the worst-hit countries
        """)
    rate_m = st.checkbox('Per one million of population', value=False)
    label = '_'.join([labels[chart], "per_million"]) if rate_m else labels[chart]
    slot_for_date = st.empty()
    startdate, period = choose_time_period(youngest, oldest, 2)
    date = startdate.strftime('%Y-%m-%d')
    slot_for_date.markdown(f'***Date {date}***')

    fig = get_most_cases_chart(df, startdate, label)
    st.altair_chart(fig, use_container_width=True)

def show_compare_chart(df, chart, youngest, oldest):

    labels = {
        '1':'total_cases',
        '2':'total_deaths',
        '3':'new_cases',
        '4':'new_deaths',
    }
    chart_type = choose_chart_type()
    countries = df['location'].unique()
    log = False
    stack = False
    slot_for_checkbox = st.empty()
    # Reordering figure to show here
    slot_for_graph = st.empty()

    startdate, period = choose_time_period(youngest, oldest, 1)
    st.sidebar.markdown("# Select countries")
    options = st.sidebar.multiselect(
            'Countries:', 
            list(countries), 
            default=['World']
    )
    if chart_type == '1':
        log = slot_for_checkbox.checkbox(
            "Logarithmic scale", 
            value=False
        )
    else:
        stack = slot_for_checkbox.checkbox(
            "Stack values", 
            value=True
        ) if len(options) > 1 else False
    fig = get_compare_countries_chart(df, labels[chart], chart_type, startdate, options, period, log, stack)
    slot_for_graph.altair_chart(fig, use_container_width=True)
