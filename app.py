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

# Initialize session state variables
if "viewport" not in st.session_state:
    st.session_state.viewport = [-2.0, 1.0, -1.5, 1.5]

if "selected_region" not in st.session_state:
    st.session_state.selected_region = st.session_state.viewport.copy()

# Read current viewport
viewport = st.session_state.viewport

# Sidebar Section for Selected Region and Zoom Controls
st.sidebar.header("Zoom Controls")

# Use selected_region for x_min, x_max, y_min, y_max
x_min, x_max, y_min, y_max = st.session_state.selected_region

# Update sidebar inputs dynamically with keys to maintain state
x_min = st.sidebar.number_input("X Min", value=x_min, key='x_min')
x_max = st.sidebar.number_input("X Max", value=x_max, key='x_max')
y_min = st.sidebar.number_input("Y Min", value=y_min, key='y_min')
y_max = st.sidebar.number_input("Y Max", value=y_max, key='y_max')

# Function to handle zoom in
def zoom_in():
    st.session_state.viewport = [
        st.sidebar.session_state.x_min,
        st.sidebar.session_state.x_max,
        st.sidebar.session_state.y_min,
        st.sidebar.session_state.y_max
    ]
    st.session_state.selected_region = st.session_state.viewport.copy()

# Function to reset view
def reset_view():
    st.session_state.viewport = [-2.0, 1.0, -1.5, 1.5]
    st.session_state.selected_region = st.session_state.viewport.copy()
    # Reset the number inputs
    st.sidebar.session_state.x_min = -2.0
    st.sidebar.session_state.x_max = 1.0
    st.sidebar.session_state.y_min = -1.5
    st.sidebar.session_state.y_max = 1.5

# Apply Zoom When Button Clicked
if st.sidebar.button("Zoom In"):
    zoom_in()

# Reset Viewport
if st.sidebar.button("Reset View"):
    reset_view()

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
mandelbrot_set, x_vals, y_vals = generate_mandelbrot(
    st.session_state.viewport, width, height, max_iter
)

# Create Plotly Interactive Plot
fig = px.imshow(
    mandelbrot_set,
    labels=dict(color="Iterations"),
    x=x_vals,
    y=y_vals,
    color_continuous_scale="inferno",
    origin="lower",
    aspect='auto',
)
fig.update_layout(
    xaxis_title="Real Part",
    yaxis_title="Imaginary Part",
    dragmode="select",
    width=width,
    height=height,
)

# Display the Plotly chart
chart = st.plotly_chart(fig, use_container_width=True, key='mandelbrot_chart')

# Capture relayout data from the chart
relayout_data = st.session_state.get('mandelbrot_chart_relayout_data')

# Process selection events
if relayout_data:
    if (
        'xaxis.range[0]' in relayout_data and
        'xaxis.range[1]' in relayout_data and
        'yaxis.range[0]' in relayout_data and
        'yaxis.range[1]' in relayout_data
    ):
        # Update selected region based on the selection
        st.session_state.selected_region = [
            relayout_data['xaxis.range[0]'],
            relayout_data['xaxis.range[1]'],
            relayout_data['yaxis.range[0]'],
            relayout_data['yaxis.range[1]']
        ]
        # Update the sidebar inputs
        st.sidebar.session_state.x_min = st.session_state.selected_region[0]
        st.sidebar.session_state.x_max = st.session_state.selected_region[1]
        st.sidebar.session_state.y_min = st.session_state.selected_region[2]
        st.sidebar.session_state.y_max = st.session_state.selected_region[3]
