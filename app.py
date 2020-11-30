#!/usr/bin/python3
"""Streamlit Covid-19 app"""
import datadotworld as dw
import pandas as pd
import streamlit as st
from PIL import Image
from Functions.graph_functions\
import show_world_scatter, show_continent_cases,\
       show_worst_hit_chart, show_compare_chart
from Functions.choose_functions import choose_data_type
from Functions.ui_elements import world_cases

DATASET_ID = 'vale123/covid-19-complete-dataset'

QUERY = """
        SELECT continent,
        location,
        date,
        total_cases,
        total_deaths,
        new_cases,
        new_deaths,
        new_cases_per_million,
        new_deaths_per_million
        FROM owid_covid_data
        WHERE location != 'International'
        """

# Cache for 6 hours
@st.cache(ttl=3600*6, show_spinner=False)
def import_data():
    '''
    Imports data from dataworld.
    Query a dataset using the var = datadotworld.query('dataset_ID', 'query')
    '''
    result = dw.query(DATASET_ID, QUERY)
    df = result.dataframe
    df['date'] = pd.to_datetime(df['date'])
    df[['total_cases', 'total_deaths']] = df[['total_cases', 'total_deaths']].apply(pd.to_numeric)
    floats = df.select_dtypes(include=['float64']).columns.tolist()
    df[floats] = df[floats].astype('float32')
    return df

def main():
    st.set_page_config(
        page_title="COVID-19 STATISTICS",
        page_icon=":globe_with_meridians:")

    with st.spinner('Please wait...'):
        df = import_data()

    youngest = max(df['date'])
    oldest = min(df['date'])

    image = Image.open('./Images/covid_logo.png')
    st.sidebar.image(
        image,
        use_column_width=True,
        caption=f"Updated: {youngest.strftime('%Y-%m-%d')}")

    st.sidebar.markdown("# Choose statistics")
    graph = st.sidebar.radio("Chart:",
                             ("Country compare",
                              "Worst-hit countries",
                              "Cases by continent",
                              "Cases worldwide"))

    # Compare countries chart
    if graph == "Country compare":
        num_cases = df[(df['date'] == youngest) & (df['location'] == 'World')]
        #world_cases(num_cases)
        chart = choose_data_type(1)
        show_compare_chart(df, chart, youngest, oldest)

    # Worst-hit countries charts
    if graph == "Worst-hit countries":
        show_worst_hit_chart(df, youngest, oldest)

    # Cases by continent
    if graph == "Cases by continent":
        st.markdown("""
        ## COVID-19: new confirmed cases by continent\n
        Hover over each area to see the values
        """)
        show_continent_cases(df, 'new_cases')

    # World scatter plot
    if graph == "Cases worldwide":
        st.markdown("""
        ## COVID-19: new confirmed cases worldwide 🌐\n
        Hover over each circle to see the values
        """)
        show_world_scatter(df, 'new_cases')

    ##Tips info text
    st.sidebar.markdown("# Tips")
    if graph == "Country compare":
        info_text = """
        **Use the sidebar** to select or deselect countries.\n
        **Compare countries** by selecting multiple options.\n
        **Choose the type of the statistics** from the select box.\n
        **Adjust time period** by dragging the slider or just clicking it.\n
        **Hover over** each line/block to see the values.
        """
    elif graph == "Worst-hit countries":
        info_text = """
        **Adjust time period** by dragging the slider or just clicking it.\n
        **By clicking the checkbox** you can see the values per one million of population.\n
        **Hover over** each line/block to see the values.
        """
    elif graph == "Cases by continent":
        info_text = """
        **Hover over** each line/block to see the values.
        """
    elif graph == "Cases worldwide":
        info_text = """
        **Hover over** each area to see the values.
        """
    st.sidebar.info(info_text)

    #About info text
    st.sidebar.markdown("# About")
    st.sidebar.info("""
    **This project's mission** is to transform COVID-19 data into understandable and shareable visuals.
    Data also needs to be reliable and up-to-date throughout the duration of the COVID-19 pandemic.\n
    This app is maintained by [*Valtteri Kurkela*](https://github.com/kurval) and 
    data is sourced from [**Our World in Data**](https://ourworldindata.org/coronavirus).
    """)

    st.info("""
    ℹ️ You can select different statistics from the sidebar on the left corner.
    """)

    # Footer info
    st.markdown("""
    by: *V.Kurkela* | source: [Github](https://github.com/kurval/COVID-19-Statistics) |
    data source: [Dataworld](https://data.world/vale123/covid-19-complete-dataset)
    (orginally: [Ourworldindata](https://ourworldindata.org/coronavirus-source-data))
    """)

if __name__ == "__main__":
    main()
