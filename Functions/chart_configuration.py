import altair as alt
import pandas as pd

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