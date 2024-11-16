import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_service_account.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1okyZW0Y20lOq7iVKdyTKdztUmpwGu1ARmhzsOH4vR5w/edit?usp=sharing')
worksheet = sheet.sheet1

# Fetch parameters from the sheet
data = worksheet.get_all_records()
params = {item['Parameter']: int(item['Value']) for item in data}

# Streamlit Title
st.title("Mandelbrot Set Visualization")

# Sidebar Parameters
st.sidebar.header("Settings")
width = st.sidebar.slider("Width", 400, 1600, params.get('Width', 800))
height = st.sidebar.slider("Height", 400, 1600, params.get('Height', 800))
max_iter = st.sidebar.slider("Max Iterations", 10, 500, params.get('Max Iterations', 100))

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
