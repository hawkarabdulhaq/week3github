import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Google Sheet URL and tab
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/export?format=csv&id=1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w&gid=0"

# Function to fetch parameters from Google Sheet
def fetch_parameters():
    try:
        data = pd.read_csv(GOOGLE_SHEET_URL)
        params = {
            "width": int(data.loc[data['Parameter'] == 'Width', 'Value'].values[0]),
            "height": int(data.loc[data['Parameter'] == 'Height', 'Value'].values[0]),
            "max_iter": int(data.loc[data['Parameter'] == 'Max Iterations', 'Value'].values[0])
        }
        return params
    except Exception as e:
        st.error(f"Error fetching data from Google Sheet: {e}")
        return {"width": 800, "height": 800, "max_iter": 100}  # Defaults

# Fetch parameters
params = fetch_parameters()
width = params['width']
height = params['height']
max_iter = params['max_iter']

# Streamlit Title
st.title("Mandelbrot Set Visualization")

# Sidebar Info
st.sidebar.header("Fetched Parameters")
st.sidebar.write(f"Width: {width}")
st.sidebar.write(f"Height: {height}")
st.sidebar.write(f"Max Iterations: {max_iter}")

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
