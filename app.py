import streamlit as st
import matplotlib.pyplot as plt
import json
from compute_mandelbrot import compute_mandelbrot
from datetime import datetime

# Database setup
DATABASE = "parameters.json"

def initialize_database():
    """Initialize JSON file storage."""
    try:
        with open(DATABASE, "x") as f:
            json.dump({"parameters": []}, f)
    except FileExistsError:
        pass

def update_database(params):
    """Update the JSON file with the latest parameters."""
    with open(DATABASE, "r+") as f:
        data = json.load(f)
        params["updated_at"] = datetime.now().isoformat()  # Add timestamp
        params["id"] = len(data["parameters"]) + 1  # Assign an ID
        data["parameters"].append(params)
        f.seek(0)
        json.dump(data, f, indent=4)

def read_database():
    """Read parameters from the JSON file."""
    with open(DATABASE, "r") as f:
        data = json.load(f)
    return data["parameters"]

def get_latest_parameters():
    """Fetch the latest parameters from the database."""
    parameters = read_database()
    if parameters:
        return parameters[-1]
    return None

# Initialize database
initialize_database()

# App title
st.title("Mandelbrot Set Visualization with JSON Database Logging")

# Sidebar for user inputs
st.sidebar.header("Visualization Parameters")
width = st.sidebar.slider("Image Width", 400, 1600, 800, key="width")
height = st.sidebar.slider("Image Height", 400, 1600, 800, key="height")
max_iter = st.sidebar.slider("Max Iterations", 50, 500, 100, key="max_iter")
center_real = st.sidebar.number_input("Center Real Part", -2.0, 2.0, -0.5, key="center_real")
center_imag = st.sidebar.number_input("Center Imaginary Part", -2.0, 2.0, 0.0, key="center_imag")
x_range = st.sidebar.slider("X Range", 0.5, 3.0, 1.5, key="x_range")
y_range = st.sidebar.slider("Y Range", 0.5, 3.0, 1.5, key="y_range")
zoom = st.sidebar.slider("Zoom", 0.5, 5.0, 1.0, key="zoom")

# Button to log parameters and update database
if st.sidebar.button("Save Parameters"):
    params = {
        "width": width,
        "height": height,
        "max_iter": max_iter,
        "center_real": center_real,
        "center_imag": center_imag,
        "x_range": x_range,
        "y_range": y_range,
        "zoom": zoom
    }
    update_database(params)
    st.sidebar.success("Parameters saved to database!")

# Fetch the latest parameters
latest_params = None
if st.sidebar.button("Fetch Latest Parameters"):
    latest_params = get_latest_parameters()
    if latest_params:
        st.sidebar.info("Fetched the latest parameters from the database.")
    else:
        st.sidebar.warning("No parameters found in the database.")

# Determine parameters to use for computation
if latest_params:
    st.sidebar.write(f"Using fetched parameters: {latest_params}")
    computation_params = latest_params
else:
    computation_params = {
        "width": width,
        "height": height,
        "max_iter": max_iter,
        "center_real": center_real,
        "center_imag": center_imag,
        "x_range": x_range,
        "y_range": y_range,
        "zoom": zoom
    }

# Compute Mandelbrot set
mandelbrot_set, bounds = compute_mandelbrot(
    width=computation_params["width"],
    height=computation_params["height"],
    max_iter=computation_params["max_iter"],
    center_real=computation_params["center_real"],
    center_imag=computation_params["center_imag"],
    x_range=computation_params["x_range"],
    y_range=computation_params["y_range"],
    zoom=computation_params["zoom"]
)

# Plotting the Mandelbrot set
x_min, x_max, y_min, y_max = bounds

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(mandelbrot_set, extent=[x_min, x_max, y_min, y_max], cmap="hot", origin="lower")
ax.set_title(f"Mandelbrot Set\nCenter: ({computation_params['center_real']}, {computation_params['center_imag']}), Zoom: {computation_params['zoom']}")
ax.set_xlabel("Real Part")
ax.set_ylabel("Imaginary Part")
st.pyplot(fig)

# Display database contents for debugging
st.sidebar.header("Database Contents")
if st.sidebar.button("Show Parameter Log"):
    parameters = read_database()
    st.sidebar.write(parameters)
