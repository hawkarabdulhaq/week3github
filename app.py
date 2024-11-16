import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit Title
st.title("Mandelbrot Set Visualization")

# Load Parameters from CSV
parameters_file = "parameters.csv"
parameters = pd.read_csv(parameters_file)

# Sidebar
st.sidebar.header("Settings")
selected_set = st.sidebar.selectbox("Choose Parameter Set", parameters["Parameter Set"])
selected_params = parameters[parameters["Parameter Set"] == selected_set].iloc[0]

# Fetch Parameters
width = st.sidebar.slider("Width", 400, 1600, int(selected_params["Width"]))
height = st.sidebar.slider("Height", 400, 1600, int(selected_params["Height"]))
max_iter = st.sidebar.slider("Max Iterations", 10, 500, int(selected_params["Max Iterations"]))

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
