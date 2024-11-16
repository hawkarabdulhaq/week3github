import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Google Sheet public CSV and Sheets API link
GOOGLE_SHEET_URL_CSV = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/export?format=csv&id=1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w&gid=0"
GOOGLE_SHEET_URL_UPDATE = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/values/Sheet1!A1:append?valueInputOption=USER_ENTERED"

# Function to fetch parameters from Google Sheet
def fetch_parameters():
    try:
        data = pd.read_csv(GOOGLE_SHEET_URL_CSV)
        params = {
            "width": int(data.loc[data['Parameter'] == 'Width', 'Value'].values[0]),
            "height": int(data.loc[data['Parameter'] == 'Height', 'Value'].values[0]),
            "max_iter": int(data.loc[data['Parameter'] == 'Max Iterations', 'Value'].values[0])
        }
        return params
    except Exception as e:
        st.error(f"Error fetching data from Google Sheet: {e}")
        return {"width": 800, "height": 800, "max_iter": 100}  # Defaults

# Function to update parameters in the Google Sheet
def update_parameters(width, height, max_iter):
    try:
        # Prepare data for the update
        update_data = {
            "range": "Sheet1!A1:C3",
            "majorDimension": "ROWS",
            "values": [
                ["Parameter", "Value"],
                ["Width", width],
                ["Height", height],
                ["Max Iterations", max_iter]
            ]
        }
        response = requests.put(
            GOOGLE_SHEET_URL_UPDATE,
            json=update_data,
        )
        if response.status_code == 200:
            st.success("Parameters updated successfully!")
        else:
            st.error(f"Failed to update sheet: {response.text}")
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")

# Sidebar UI for fetching and editing parameters
st.sidebar.header("Control Panel")
if st.sidebar.button("Fetch Parameters"):
    st.session_state.params = fetch_parameters()

# Initialize session state for parameters
if "params" not in st.session_state:
    st.session_state.params = fetch_parameters()

# Display and edit parameters in the sidebar
st.sidebar.subheader("Edit Parameters")
params = st.session_state.params
width = st.sidebar.number_input("Width", min_value=100, max_value=2000, value=params["width"])
height = st.sidebar.number_input("Height", min_value=100, max_value=2000, value=params["height"])
max_iter = st.sidebar.number_input("Max Iterations", min_value=10, max_value=1000, value=params["max_iter"])

# Update button
if st.sidebar.button("Update Parameters"):
    update_parameters(width, height, max_iter)
    st.session_state.params = {"width": width, "height": height, "max_iter": max_iter}

# Get parameters for the current run
width = st.session_state.params["width"]
height = st.session_state.params["height"]
max_iter = st.session_state.params["max_iter"]

# Display current parameters in the sidebar
st.sidebar.subheader("Current Parameters")
st.sidebar.write(f"Width: {width}")
st.sidebar.write(f"Height: {height}")
st.sidebar.write(f"Max Iterations: {max_iter}")

# Streamlit Title
st.title("Mandelbrot Set Visualization")

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
