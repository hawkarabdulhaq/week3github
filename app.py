import sqlite3
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch parameters from the database
def get_parameters():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Fetch the latest parameters (you could add logic to fetch specific ones)
    cursor.execute("SELECT width, height, max_iter FROM parameters ORDER BY id DESC LIMIT 1")
    parameters = cursor.fetchone()  # Fetch the first row (latest parameters)
    
    conn.close()
    
    # Return the parameters if found, otherwise default values
    if parameters:
        return parameters
    else:
        return (800, 800, 100)  # Default values

# Streamlit Title
st.title("Mandelbrot Set Visualization")

# Fetch parameters from the database
width, height, max_iter = get_parameters()

# Sidebar for adjusting parameters
st.sidebar.header("Settings")
width = st.sidebar.slider("Width", 400, 1600, width)
height = st.sidebar.slider("Height", 400, 1600, height)
max_iter = st.sidebar.slider("Max Iterations", 10, 500, max_iter)

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
