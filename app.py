import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheet Details
SHEET_URL = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/edit?usp=sharing"

# Fetch parameters from Google Sheet
def fetch_parameters(sheet_url):
    # Use gspread to connect to the Google Sheet
    gc = gspread.service_account()  # Ensure credentials are set up
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.sheet1  # Access the first sheet
    data = worksheet.get_all_records()  # Get all data as a list of dicts
    return pd.DataFrame(data)  # Convert to DataFrame for easier use

# Fetch parameters from the Google Sheet
parameters_df = fetch_parameters(SHEET_URL)
st.sidebar.header("Settings")

# Set default parameters from the database
default_width = int(parameters_df.loc[parameters_df['Parameter'] == 'Width', 'Value'].values[0])
default_height = int(parameters_df.loc[parameters_df['Parameter'] == 'Height', 'Value'].values[0])
default_max_iter = int(parameters_df.loc[parameters_df['Parameter'] == 'Max Iterations', 'Value'].values[0])

# Sidebar Inputs
width = st.sidebar.slider("Width", 400, 1600, default_width)
height = st.sidebar.slider("Height", 400, 1600, default_height)
max_iter = st.sidebar.slider("Max Iterations", 10, 500, default_max_iter)

# Generate Mandelbrot Set
x = np.linspace(-2, 1, width)
y = np.linspace(-1.5, 1.5, height)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

Z = np.zeros_like(C, dtype=complex)
mandelbrot_set = np.zeros(C.shape, dtype=int)

for i in range(max_iter):
    mask = np.abs(Z) < 2
    Z[mask] = Z[mask] * Z[mask] + C[mask]
    mandelbrot_set += mask

# Plotting
fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(
    mandelbrot_set,
    extent=(-2, 1, -1.5, 1.5),
    cmap="coolwarm",
    interpolation="bilinear",
)
plt.colorbar(im, ax=ax, label="Iterations")
ax.set_title("Mandelbrot Set")
ax.set_xlabel("Real Part")
ax.set_ylabel("Imaginary Part")

# Streamlit Display
st.pyplot(fig)
