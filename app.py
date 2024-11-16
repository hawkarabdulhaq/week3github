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
Customize parameters or choose from predefined settings to visualize this mathematical masterpiece.
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
width = st.sidebar.slider(
    "Canvas Width (Pixels)",
    400, 2000,
    int(selected_params["Width"]),
    help="Adjust the width of the visualization canvas."
)
height = st.sidebar.slider(
    "Canvas Height (Pixels)",
    400, 2000,
    int(selected_params["Height"]),
    help="Adjust the height of the visualization canvas."
)
max_iter = st.sidebar.slider(
    "Max Iterations",
    10, 1000,
    int(selected_params["Max Iterations"]),
    help="Set the maximum number of iterations for rendering."
)

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

# Visualization
st.subheader("🔍 Mandelbrot Visualization")
col1, col2 = st.columns([3, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(
        mandelbrot_set,
        extent=(-2, 1, -1.5, 1.5),
        cmap="inferno",
        interpolation="bilinear"
    )
    plt.colorbar(im, ax=ax, label="Iterations")
    ax.set_title("Mandelbrot Set", fontsize=14)
    ax.set_xlabel("Real Part")
    ax.set_ylabel("Imaginary Part")

    st.pyplot(fig)

with col2:
    st.info("""
    **Tips:**
    - Adjust the sliders to fine-tune your visualization.
    - Higher iterations reveal more detail but take longer to compute.
    - Switch between presets for quick exploration!
    """, icon="ℹ️")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Hawkar")
