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
Customize parameters, zoom in/out, or pan across the image for a complete exploration.
""")

# Sidebar
st.sidebar.title("Control Panel")
parameters_file = "parameters.csv"
parameters = pd.read_csv(parameters_file)
selected_set = st.sidebar.selectbox(
    "Select Parameter Preset",
    parameters["Parameter Set"],
    help="Choose a predefined parameter set for the Mandelbrot visualization."
)
selected_params = parameters[parameters["Parameter Set"] == selected_set].iloc[0]

# Sidebar Parameters
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

# Dynamic Viewport Settings
viewport = st.session_state.get("viewport", [-2.0, 1.0, -1.5, 1.5])

# Pan and Zoom Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 Zoom In"):
        x_mid = (viewport[0] + viewport[1]) / 2
        y_mid = (viewport[2] + viewport[3]) / 2
        x_range = (viewport[1] - viewport[0]) / 2
        y_range = (viewport[3] - viewport[2]) / 2
        viewport = [
            x_mid - x_range / 2, x_mid + x_range / 2,
            y_mid - y_range / 2, y_mid + y_range / 2
        ]
        st.session_state.viewport = viewport
with col2:
    if st.button("🔄 Reset View"):
        viewport = [-2.0, 1.0, -1.5, 1.5]
        st.session_state.viewport = viewport
with col3:
    if st.button("🔍 Zoom Out"):
        x_mid = (viewport[0] + viewport[1]) / 2
        y_mid = (viewport[2] + viewport[3]) / 2
        x_range = (viewport[1] - viewport[0])
        y_range = (viewport[3] - viewport[2])
        viewport = [
            x_mid - x_range, x_mid + x_range,
            y_mid - y_range, y_mid + y_range
        ]
        st.session_state.viewport = viewport

# Pan Controls
col4, col5, col6 = st.columns([1, 2, 1])
with col4:
    if st.button("⬅️ Left"):
        x_shift = (viewport[1] - viewport[0]) * 0.1
        viewport = [viewport[0] - x_shift, viewport[1] - x_shift, viewport[2], viewport[3]]
        st.session_state.viewport = viewport
with col5:
    up_down = st.columns([1, 1])
    with up_down[0]:
        if st.button("⬆️ Up"):
            y_shift = (viewport[3] - viewport[2]) * 0.1
            viewport = [viewport[0], viewport[1], viewport[2] - y_shift, viewport[3] - y_shift]
            st.session_state.viewport = viewport
    with up_down[1]:
        if st.button("⬇️ Down"):
            y_shift = (viewport[3] - viewport[2]) * 0.1
            viewport = [viewport[0], viewport[1], viewport[2] + y_shift, viewport[3] + y_shift]
            st.session_state.viewport = viewport
with col6:
    if st.button("➡️ Right"):
        x_shift = (viewport[1] - viewport[0]) * 0.1
        viewport = [viewport[0] + x_shift, viewport[1] + x_shift, viewport[2], viewport[3]]
        st.session_state.viewport = viewport

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
