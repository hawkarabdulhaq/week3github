import streamlit as st
import pandas as pd

# Fetch data from Google Sheets
def get_parameters():
    sheet_url = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/edit?usp=sharing"
    sheet_name = "Sheet1"  # Replace with your actual sheet name
    data = fetch_sheet_data(sheet_url, sheet_name)
    return data

# Fetch the parameter data
parameters_df = get_parameters()

# Streamlit interface
st.title("Dynamic App with Google Sheet Parameters")

# Dynamically create sliders and inputs
for index, row in parameters_df.iterrows():
    param_name = row["Parameter"]
    min_val = row["Min"]
    max_val = row["Max"]
    default_val = row["Default"]

    st.sidebar.slider(param_name, min_val, max_val, default_val)

# Add functionality based on parameters (custom logic)
st.write("Use the sliders to interact with the preset values!")
