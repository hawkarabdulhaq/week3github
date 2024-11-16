import streamlit as st
import numpy as np
import plotly.express as px

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
Drag to select a region on the plot, and then click "Zoom In" to zoom into the fractal.
""")

# Sidebar Parameters
st.sidebar.title("Control Panel")
width = st.sidebar.slider(
    "Canvas Width (Pixels)", 400, 2000, 800,
    help="Adjust the width of the visualization canvas."
)
height = st.sidebar.slider(
    "Canvas Height (Pixels)", 400, 2000, 800,
    help="Adjust the height of the visualization canvas."
)
max_iter = st.sidebar.slider(
    "Max Iterations", 10, 1000, 500,
    help="Set the maximum number of iterations for rendering."
)

# Initialize viewport in session state
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

# Generate Mandelbrot Set
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

# Display Plotly Chart
st.plotly_chart(fig, use_container_width=True)

# Manual Region Selection
st.sidebar.header("Zoom Controls")
x_min = st.sidebar.number_input("X Min", value=viewport[0])
x_max = st.sidebar.number_input("X Max", value=viewport[1])
y_min = st.sidebar.number_input("Y Min", value=viewport[2])
y_max = st.sidebar.number_input("Y Max", value=viewport[3])

# Apply Zoom When Button Clicked
if st.sidebar.button("Zoom In"):
    if x_min < x_max and y_min < y_max:
        st.session_state.viewport = [x_min, x_max, y_min, y_max]
        st.sidebar.success(f"Zooming into X: {x_min} to {x_max}, Y: {y_min} to {y_max}")
        st.experimental_set_query_params(viewport=st.session_state.viewport)

# Reset Viewport
if st.sidebar.button("Reset View"):
    st.session_state.viewport = [-2.0, 1.0, -1.5, 1.5]
    st.sidebar.info("Reset to default view.")
    st.experimental_set_query_params(viewport=st.session_state.viewport)
