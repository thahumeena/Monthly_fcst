# pages/1_🌧️_Rainfall_Map.py

import streamlit as st

# --- AUTHENTICATION CHECK ---
if not st.session_state.get('authenticated', False):
    st.error("Please log in on the Home page to access this tool.")
    st.stop()
# ---------------------------

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import box
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from io import BytesIO
# import warnings # Removed unused import

# Set up page config and custom CSS for the header
st.set_page_config(
    page_title="Rainfall Map",
    page_icon="🌧️",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* CUSTOM BLUE HEADER BAR (repeated for consistency) */
    .main-header {
        background-color: #1E90FF;
        color: white;
        padding: 10px 0;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Push main content down to account for the fixed header */
    .st-emotion-cache-1g8i5u7, .st-emotion-cache-6qob1r, .st-emotion-cache-1y4pm5r {
        padding-top: 80px;
    }
    /* Hide the default Streamlit footer and hamburger menu */
    .st-emotion-cache-1629p8f {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="main-header">Forecasters\' Tools</div>', unsafe_allow_html=True)
st.title("🌧️ Rainfall Outlook Map")

# --- START OF USER'S ORIGINAL MAP SCRIPT LOGIC ---

# Load shapefile and clip extent
shp = 'data/Atoll_boundary2016.shp'
# Use st.cache_data to speed up file loading on reruns
@st.cache_data
def load_data(path):
    gdf = gpd.read_file(path).to_crs(epsg=4326)
    bbox = box(71, -1, 75, 7.5)
    gdf = gdf[gdf.intersects(bbox)]
    # Clean missing or invalid atoll names
    gdf['Name'] = gdf['Name'].fillna("Unknown")
    # Ensure unique atoll names
    return gdf, sorted(gdf['Name'].unique().tolist())

try:
    gdf, unique_atolls = load_data(shp)
except Exception as e:
    st.error(f"Error loading shapefile: {e}. Please ensure 'data/Atoll_boundary2016.shp' exists.")
    st.stop()


# Editable map title (sidebar)
map_title = st.sidebar.text_input("Edit Map Title:", "Maximum Rainfall Outlook for OND 2025")

# Categories for each atoll
categories = ['Below Normal', 'Normal', 'Above Normal']

# Sidebar instructions
st.sidebar.write("### Adjust Atoll Categories & Percentages")
st.sidebar.write("Select category and percentage for each atoll:")

# Dictionaries to store selections
selected_categories = {}
selected_percentages = {}

# Sidebar inputs for each atoll
for atoll in unique_atolls:
    with st.sidebar.expander(atoll):
        selected_categories[atoll] = st.selectbox(
            f"Category for {atoll}:",
            categories,
            key=f"cat_{atoll}"
        )
        selected_percentages[atoll] = st.slider(
            f"Percentage for {selected_categories[atoll]} (%):",
            min_value=33, max_value=100, value=35, step=1,
            key=f"perc_{atoll}"
        )

# Map Plotting Logic
# Colormaps: Below Normal (Red), Normal (Gray/White), Above Normal (Blue)
category_colors = {
    'Below Normal': ['#FEE0D2', '#FC9272', '#DE2D26'],  # Reds
    'Normal': ['#ECECEC', '#BDBDBD', '#737373'],        # Grays
    'Above Normal': ['#DEEBF7', '#9ECAE1', '#4292C6']   # Blues
}

# Combine data for plotting
gdf['fill_color'] = 'lightgray' # Default color
for atoll in unique_atolls:
    category = selected_categories[atoll]
    percentage = selected_percentages[atoll]
    # Simple color assignment based on percentage and category
    if percentage >= 66:
        color_index = 2
    elif percentage >= 33:
        color_index = 1
    else:
        color_index = 0
    gdf.loc[gdf['Name'] == atoll, 'fill_color'] = category_colors[category][color_index]


# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(10, 15))
ax.set_aspect('equal')

# Bounds for the colorbar
min_val, max_val = 0, 3
bins = np.linspace(min_val, max_val, 4)
norm = BoundaryNorm(bins, len(bins) - 1)
tick_positions = bins[:-1] + (bins[1] - bins[0]) / 2
tick_labels = ['< 33%', '33%-66%', '> 66%']

# Plot the shapefile
for idx, row in gdf.iterrows():
    # Determine the outline color based on the category for visual distinction
    outline_color = 'black'
    if selected_categories.get(row['Name']) == 'Above Normal':
        outline_color = '#4292C6' # Dark Blue
    elif selected_categories.get(row['Name']) == 'Below Normal':
        outline_color = '#DE2D26' # Dark Red
    
    # Plot the atoll
    row['geometry'].plot(
        ax=ax, 
        color=row['fill_color'], 
        edgecolor=outline_color, # Use the determined outline color
        linewidth=0.5
    )

# Axis and title
ax.set_xlim(71, 75)
ax.set_ylim(-1, 7.5)
ax.set_title(map_title, fontsize=18)
ax.set_xlabel("Longitude (°E)", fontsize=14)
ax.set_ylabel("Latitude (°N)", fontsize=14)
ax.set_xticks([71, 72, 73, 74, 75])
ax.set_xticklabels(['71', '72', '73', '74', '75'])
ax.tick_params(labelsize=12)

# Function for colorbars
width = "40%"
height = "2.5%"
start_x = 0.05
start_y = 0.1
spacing = 0.09

def make_cb(ax, cmap, title, offset):
    cax = inset_axes(ax, width=width, height=height, loc='lower left',
                     bbox_to_anchor=(start_x, start_y + offset, 1, 1),
                     bbox_transform=ax.transAxes, borderpad=0)
    cb = colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=bins,
                               ticks=tick_positions, spacing='uniform', orientation='horizontal')
    cb.set_ticklabels(tick_labels)
    cax.set_title(title, fontsize=10, pad=6)
    cb.ax.tick_params(labelsize=9, pad=2)

# Create colorbars for each category
make_cb(ax, ListedColormap(category_colors["Above Normal"]), "Above Normal", 2 * spacing)
make_cb(ax, ListedColormap(category_colors["Normal"]), "Normal", spacing)
make_cb(ax, ListedColormap(category_colors["Below Normal"]), "Below Normal", 0)

plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# --- Display map ---
st.pyplot(fig)

# --- Download button ---
buf = BytesIO()
fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
st.download_button(
    label="Download Map as PNG",
    data=buf.getvalue(),
    file_name=f"{map_title.replace(' ', '_')}.png",
    mime="image/png"
)

# --- END OF USER'S ORIGINAL MAP SCRIPT LOGIC ---
