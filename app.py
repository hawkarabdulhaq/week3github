import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets Integration Function
def fetch_parameters(sheet_url: str, sheet_name: str):
    try:
        # Authenticate and fetch data
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.sidebar.error(f"Error fetching parameters: {e}")
        return None

# Streamlit Title
st.title("Mandelbrot Set Visualization with Google Sheets Parameters")

# Google Sheet details
SHEET_URL = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/edit?usp=sharing"
SHEET_NAME = "Sheet1"

# Fetch parameters from Google Sheets
params_df = fetch_parameters(SHEET_URL, SHEET_NAME)

# Sidebar Parameters
if params_df is not None:
    st.sidebar.header("Parameters from Database")
    
    # Debugging: Display fetched data in sidebar
    st.sidebar.write("Fetched Parameters:")
    st.sidebar.dataframe(params_df)
    
    # Extract parameter values
    try:
        width = st.sidebar.slider("Width", 400, 1600, int(params_df.loc[params_df['Parameter'] == 'width', 'Value'].values[0]))
        height = st.sidebar.slider("Height", 400, 1600, int(params_df.loc[params_df['Parameter'] == 'height', 'Value'].values[0]))
        max_iter = st.sidebar.slider("Max Iterations", 10, 500, int(params_df.loc[params_df['Parameter'] == 'max_iter', 'Value'].values[0]))
    except Exception as e:
        st.sidebar.error(f"Error parsing parameters: {e}")
        width, height, max_iter = 800, 800, 100
else:
    st.sidebar.error("Failed to fetch parameters. Using default values.")
    width, height, max_iter = 800, 800, 100

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
