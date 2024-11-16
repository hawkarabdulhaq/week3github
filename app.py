import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Mandelbrot Set Explorer",
    page_icon="✨",
    layout="wide"
)

# Title and Description
st.title("✨ Mandelbrot Set Explorer")
st.write("""
Explore the mesmerizing Mandelbrot Set interactively! 
Drag to select a region on the plot, and zoom into the fractal in real-time.
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
if "viewport" not in st.session_state:
    st.session_state.viewport = [-2.0, 1.0, -1.5, 1.5]

# Generate Mandelbrot Set Function
def generate_mandelbrot(viewport, width, height, max_iter):
    x = np.linspace(viewport[0], viewport[1], width)
    y = np.linspace(viewport[2], viewport[3], height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C, dtype=complex)
    mandelbrot_set = np.zeros(C.shape, dtype=int)

    for i in range(max_iter):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        mandelbrot_set[mask] += 1

    return mandelbrot_set, x, y

# Generate Data
viewport = st.session_state.viewport
mandelbrot_set, x, y = generate_mandelbrot(viewport, width, height, max_iter)

# Create Plotly Interactive Plot
fig = px.imshow(
    mandelbrot_set,
    labels=dict(color="Iterations"),
    x=x,
    y=y,
    color_continuous_scale="inferno",
    origin="lower"
)
fig.update_layout(
    xaxis_title="Real Part",
    yaxis_title="Imaginary Part",
    dragmode="select",
    width=800,
    height=800
)

# Streamlit Plotly Component
st.plotly_chart(fig, use_container_width=True)

# Get Selected Region
st.sidebar.header("Zoom Controls")
selected_region = st.session_state.get("selected_region", None)

if st.session_state.get("plotly_click"):
    selection = st.session_state.plotly_click
    viewport = [
        selection["range"]["x"][0],
        selection["range"]["x"][1],
        selection["range"]["y"][0],
        selection["range"]["y"][1]
    ]
    st.session_state.viewport = viewport

# Reset Viewport Button
if st.sidebar.button("Reset View"):
    st.session_state.viewport = [-2.0, 1.0, -1.5, 1.5]
