import streamlit as st

def world_cases(num_cases):
    _border_color = "light-gray"
    _number_format = "font-size:30px; color:black;"
    _cell_style = f" border: 2px solid {_border_color}; border-bottom:2px solid white; margin:10px;"
    _text_style = "font-size:13px; margin:0px;"
    st.markdown(
        f"<table style='width: 100%; color:white; font-size:20px; border: 0px solid gray; border-spacing: 10px;  border-collapse: collapse;'> "
        f"<tr> "
        f"<td id=cases style='{_cell_style} + background-color:blue;'> Confirmed Cases 🌐<p style='{_text_style}'>Worldwide</p></td> "
        f"<td id=deaths style='{_cell_style} + background-color:red;'> Total Deaths 🌐<p style='{_text_style}'>Worldwide</p></td>"
        "</tr>"
        f"<tr style='border: 2px solid {_border_color}'> "
        f"<td style='border-right: 2px solid {_border_color}; border-spacing: 10px; {_number_format}' > {float(num_cases['total_cases']):,.0f}</td> "
        f"<td style='{_number_format}'> {float(num_cases['total_deaths']):,.0f} </td>"
        "</tr>"
        "</table>"
        "<br>",
        unsafe_allow_html=True,
    )
