import altair as alt
import pandas as pd
import streamlit as st
import colorsys
import random

# Generates list of colors
@st.cache(show_spinner=False)
def get_N_HexCol(N=20):
    HSV_tuples = [(x * 1.0 / N, 0.6, 0.6) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def set_tooltip(long_format, line, label):
    '''
    Setting interactive tooltip for line chart.
        param: dataframe, chart, label(value)
        type: pd df object, altair object, str
        return: altair chart
    '''
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    selectors = alt.Chart(long_format).mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align='right', dx=15, dy=-15, fontSize=15).encode(
        text=alt.condition(nearest, label + ':Q', alt.value(' '), format=",.0f"),
    )

    rules = alt.Chart(long_format).mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    chart = alt.layer(
        line, selectors, points, rules, text
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=15,
    ).configure_axisX(
        labelAngle=-30
    ).configure_legend(
        titleFontSize=13,
        labelFontSize=12,
    ).properties(
        width=600, height=300
    )
    return chart

def configure_label_bar_chart(data, label, key):
    '''
    Configurations for label bar chart.
        param: dataframe, label(value), key 1=most cases 2=most deaths
        type: pd df object, str, int
        return: altair chart
    '''
    margin = 100000 if key == '3' else 10000
    SCALE=alt.Scale(domain=(0, int(max(data[label])) + margin))

    label_title = 'total cases' if key == 3 else 'total deaths'
    bars = alt.Chart(data).mark_bar().encode(
        x= alt.X(label + ':Q', title=label_title.title(), scale=SCALE),
        y=alt.Y('countries:N', sort='-x', title='Countries'),
        color=alt.Color('countries:N', legend=None, scale=alt.Scale(range=get_N_HexCol())),
        tooltip=[alt.Tooltip('date:T'),
            alt.Tooltip('countries', title='country'),
            alt.Tooltip(label, format=",.0f")],
    )

    text = bars.mark_text(
        fontSize=13,
        align='left',
        baseline='middle',
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='formatted'
    )
    
    fig = (bars + text).configure_axis(
        labelFontSize=11,
        titleFontSize=15,
    ).configure_axisY(
        labelFontSize=12,
        labelFontWeight='bold'
    ).configure_axisX(
        labelAngle=-30
    ).properties(
        height=520
    ).interactive()

    return fig