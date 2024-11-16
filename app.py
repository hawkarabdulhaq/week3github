import streamlit as st
import numpy as np
import pandas as pd
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
Explore the Mandelbrot Set interactively with infinite zoom capabilities. Use your mouse to zoom in and pan around the visualization in real time.
""")

# Load Parameters
parameters_file = "parameters.csv"
parameters = pd.read_csv(parameters_file)

# Sidebar
st.sidebar.title("Control Panel")
selected_set = st.sidebar.selectbox(
    "Select Parameter Preset",
    parameters["Parameter Set"],
    help="Choose a predefined parameter set for the Mandelbrot visualization."
)

selected_params = parameters[parameters["Parameter Set"] == selected_set].iloc[0]

# Fetch Parameters
width = int(selected_params["Width"])
height = int(selected_params["Height"])
max_iter = int(selected_params["Max Iterations"])

# Initial Bounds
x_min, x_max = st.sidebar.slider("Real Part Range", -2.0, 2.0, (-2.0, 1.0))
y_min, y_max = st.sidebar.slider("Imaginary Part Range", -2.0, 2.0, (-1.5, 1.5))

# Generate Mandelbrot Set
x = np.linspace(x_min, x_max, width)
y = np.linspace(y_min, y_max, height)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

Z = np.zeros_like(C, dtype=complex)
mandelbrot_set = np.zeros(C.shape, dtype=int)

for i in range(max_iter):
    mask = np.abs(Z) < 2
    Z[mask] = Z[mask] * Z[mask] + C[mask]
    mandelbrot_set[mask] = i

# Create a Plotly Figure
fig = go.Figure(
    data=go.Heatmap(
        z=mandelbrot_set,
        x=x,
        y=y,
        colorscale="Inferno",
        showscale=True,
        colorbar=dict(title="Iterations")
    )
)

fig.update_layout(
    title="Interactive Mandelbrot Set",
    xaxis_title="Real Part",
    yaxis_title="Imaginary Part",
    autosize=True,
    dragmode="pan",
)

# Display the Plotly Figure
st.plotly_chart(fig, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Hawkar")
