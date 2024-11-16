import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

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
Customize parameters, zoom into specific regions, and download your favorite visuals.
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

# Zoom Controls
st.sidebar.markdown("### Zoom Controls")
x_min = st.sidebar.number_input("X Min", value=-2.0, step=0.1)
x_max = st.sidebar.number_input("X Max", value=1.0, step=0.1)
y_min = st.sidebar.number_input("Y Min", value=-1.5, step=0.1)
y_max = st.sidebar.number_input("Y Max", value=1.5, step=0.1)

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
    mandelbrot_set += mask

# Visualization
st.subheader("🔍 Mandelbrot Visualization")
col1, col2 = st.columns([3, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(
        mandelbrot_set,
        extent=(x_min, x_max, y_min, y_max),
        cmap="inferno",
        interpolation="bilinear"
    )
    plt.colorbar(im, ax=ax, label="Iterations")
    ax.set_title("Mandelbrot Set", fontsize=14)
    ax.set_xlabel("Real Part")
    ax.set_ylabel("Imaginary Part")

    st.pyplot(fig)

    # Downloadable Image
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    st.download_button(
        label="Download Mandelbrot Image",
        data=buffer,
        file_name="mandelbrot_set.png",
        mime="image/png"
    )

with col2:
    st.info("""
    **Tips:**
    - Use the zoom controls to focus on specific regions.
    - Adjust iterations for more detailed visuals.
    - Download your creations and share with friends!
    """, icon="ℹ️")

    st.markdown("**Performance Note:** Increasing width, height, or iterations may slow rendering.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Hawkar")
