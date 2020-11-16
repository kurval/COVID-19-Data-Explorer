import colorsys
import streamlit as st

@st.cache(show_spinner=False)
def get_colors(N=20):
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
    new_df = df.groupby(['date', 'continent']).sum().reset_index()
    new_df = new_df[['date', 'continent', label]]
    return new_df
