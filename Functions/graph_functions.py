import pandas as pd
import streamlit as st
import altair as alt
from Functions.chart_configuration import set_tooltip
from Functions.choose_functions import choose_time_period, choose_chart_type, choose_data_type
from Functions.helper\
import get_continent_values,\
        get_country_values, get_colors,\
        get_top_values, get_values_by_date,\
        get_world_data, modify_data

def get_most_cases_chart(df, startdate, label):
    '''
    Creates labeled bar charts of 20 countries most cases and deaths
        param: pd df, startdate, label
        type: dataframe object
    '''
    new_df = modify_data(df)
    new_df = get_values_by_date(new_df, startdate, 2, label)

    top20_cases = get_top_values(new_df, label, startdate)
    if max(top20_cases[label]) > 2:
        margin = max(top20_cases[label]) / 10
    else:
        margin = 1
    scale = alt.Scale(domain=(0, int(max(top20_cases[label])) + margin))
    if label in ('new_cases', 'new_cases_per_million'):
        label_title = 'total cases'
    else:
        label_title = 'total deaths'
    bars = alt.Chart(top20_cases).mark_bar().encode(
        x=alt.X(label + ':Q', title=label_title.title(), scale=scale),
        y=alt.Y('location:N', sort='-x', title='Countries'),
        color=alt.Color('location:N', legend=None, scale=alt.Scale(range=get_colors())),
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

def show_world_scatter(df, label):
    '''
    Creates scatter plot with LOESS lines
    '''
    world_data = get_world_data(df, label)
    cases_scale = max(world_data[label])
    date_scale = max(world_data['date'])
    oldest = min(world_data['date'])
    scale_y = alt.Scale(domain=(0, cases_scale+10000))
    scale_x = alt.Scale(domain=(oldest, (date_scale + pd.DateOffset(days=3))))

    base = alt.Chart(world_data).mark_circle(size=150, opacity=0.5).transform_fold(
        fold=[label],
        as_=['cases', 'y']
    ).encode(
        x=alt.X('date:T', scale=scale_x, title='Date'),
        y=alt.Y('y:Q', scale=scale_y, title=label.replace('_', ' ').title()),
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

    st.altair_chart(chart, use_container_width=True)

def show_continent_cases(df, label):
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

    st.altair_chart(chart, use_container_width=True)

def show_worst_hit_chart(df, youngest, oldest):
    '''
    Shows worst hit countries char depending chart type:
    '1' = Total cases
    '2' = Total deaths
    '''

    labels = {
        '1':'new_cases',
        '2':'new_deaths',
    }
    slot_for_header = st.empty()
    chart = choose_data_type(2)
    if chart == '1':
        slot_for_header.markdown("""
        ## COVID-19: total confirmed cases in the worst-hit countries
        """)
    else:
        slot_for_header.markdown("""
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

def get_compare_countries_chart(df, label, chart_type, startdate, options, period, log, stack):
    '''
    Allows user to choose time period and countries for the graph.
    User can also choose statistics type from
    1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths.
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
            x=alt.X("date:T", title="Date"),
            y=alt.Y(label + ':Q', title=label.replace('_', ' ').title()
                    + scale_name, scale=alt.Scale(type=scale_type),
                    axis=alt.Axis(tickCount=5, grid=grid, ticks=grid)),
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
    fig = get_compare_countries_chart(
        df, labels[chart], chart_type, startdate,
        options, period, log, stack)
    slot_for_graph.altair_chart(fig, use_container_width=True)
