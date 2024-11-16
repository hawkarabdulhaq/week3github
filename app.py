import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Fetch parameters from Google Sheets
def fetch_sheet_data(sheet_url, sheet_name):
    # Load credentials from Streamlit secrets
    credentials = Credentials.from_service_account_info(st.secrets["google_service_account"])
    
    # Authorize and connect to the Google Sheets API
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    
    # Get all records and convert to DataFrame
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Main app
def main():
    st.title("Dynamic App with Google Sheets Integration")

    # Google Sheet URL and sheet name
    sheet_url = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/edit?usp=sharing"
    sheet_name = "Sheet1"  # Replace with the correct sheet name

    # Fetch data from Google Sheets
    st.write("Fetching data from Google Sheets...")
    parameters_df = fetch_sheet_data(sheet_url, sheet_name)
    st.write(parameters_df)  # Debugging: Display the fetched data

    # Dynamically create sliders or inputs based on parameters
    for index, row in parameters_df.iterrows():
        param_name = row["Parameter"]
        min_val = int(row["Min"])
        max_val = int(row["Max"])
        default_val = int(row["Default"])

        st.sidebar.slider(param_name, min_val, max_val, default_val)

    st.write("Interact with the sliders to modify app behavior dynamically!")

if __name__ == "__main__":
    main()
