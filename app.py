import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Mandelbrot Set Explorer",
    page_icon="✨",
    layout="wide"
)

# Custom Styles
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f4f4f8;
        padding: 10px;
    }
    .css-1aumxhk {
        color: #0A3D62 !important;
    }
    .css-1avcm0n {
        color: #0A3D62 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title("✨ Mandelbrot Set Explorer")
st.write("""
Discover the mesmerizing Mandelbrot Set with this interactive app! 
Zoom into the fractal by selecting a region of interest.
""")

# Sidebar Parameters
st.sidebar.title("Control Panel")
width = st.sidebar.slider(
    "Canvas Width (Pixels)",
    400, 2000,
    800,
    help="Adjust the width of the visualization canvas."
)
height = st.sidebar.slider(
    "Canvas Height (Pixels)",
    400, 2000,
    800,
    help="Adjust the height of the visualization canvas."
)
max_iter = st.sidebar.slider(
    "Max Iterations",
    10, 1000,
    500,
    help="Set the maximum number of iterations for rendering."
)

# Dynamic Viewport Settings
viewport = st.session_state.get("viewport", [-2.0, 1.0, -1.5, 1.5])

# Region Selection
st.sidebar.subheader("Region Selection")
x_min = st.sidebar.number_input("X Min", value=viewport[0], step=0.1)
x_max = st.sidebar.number_input("X Max", value=viewport[1], step=0.1)
y_min = st.sidebar.number_input("Y Min", value=viewport[2], step=0.1)
y_max = st.sidebar.number_input("Y Max", value=viewport[3], step=0.1)

# Confirm Region Button
if st.sidebar.button("🔍 Zoom Into Region"):
    if x_min < x_max and y_min < y_max:
        viewport = [x_min, x_max, y_min, y_max]
        st.session_state.viewport = viewport
    else:
        st.sidebar.error("Invalid region! Ensure X Min < X Max and Y Min < Y Max.")

# Generate Mandelbrot Set
x = np.linspace(viewport[0], viewport[1], width)
y = np.linspace(viewport[2], viewport[3], height)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

Z = np.zeros_like(C, dtype=complex)
mandelbrot_set = np.zeros(C.shape, dtype=int)

for i in range(max_iter):
    mask = np.abs(Z) < 2
    Z[mask] = Z[mask] * Z[mask] + C[mask]
    mandelbrot_set += mask

# Visualization
st.subheader("🔍 Mandelbrot Visualization")
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(
    mandelbrot_set,
    extent=(viewport[0], viewport[1], viewport[2], viewport[3]),
    cmap="inferno",
    interpolation="bilinear"
)
plt.colorbar(im, ax=ax, label="Iterations")
ax.set_title("Mandelbrot Set", fontsize=14)
ax.set_xlabel("Real Part")
ax.set_ylabel("Imaginary Part")
st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Hawkar")
