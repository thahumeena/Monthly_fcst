# pages1_Rainfall_Outlook.py

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import box
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
from io import BytesIO

# --- AUTHENTICATION & CONFIG ---
if not st.session_state.get('authenticated', False):
    st.error("Please log in on the Home page to access this tool.")
    st.stop()

st.set_page_config(
    page_title="Rainfall Outlook",
    page_icon="🌧️",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* CUSTOM BLUE HEADER BAR */
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
    .st-emotion-cache-1629p8f { /* Hide hamburger menu icon */
        display: none !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.markdown('<div class="main-header">Forecasters\' Tools</div>', unsafe_allow_html=True)
st.title("🌧️ Rainfall Outlook Map")
# ------------------------------

# Load shapefile and clip extent
# FIX: Corrected shapefile path quotation
shp = 'data/Atoll_boundary2016.shp'

@st.cache_data
def load_data(path):
    gdf = gpd.read_file(path).to_crs(epsg=4326)
    bbox = box(71, -1, 75, 7.5)
    gdf = gdf[gdf.intersects(bbox)]
    gdf['Name'] = gdf['Name'].fillna("Unknown")
    return gdf, sorted(gdf['Name'].unique().tolist())

try:
    gdf, unique_atolls = load_data(shp)
except Exception as e:
    st.error(f"Error loading shapefile: {e}. Ensure 'data/Atoll_boundary2016.shp' exists.")
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

# Sidebar inputs for each unique atoll (Using a form to update all at once is better)
with st.sidebar.form("atoll_input_form"):
    for i, atoll in enumerate(unique_atolls):
        st.markdown(f"**{atoll}**")
        selected = st.selectbox(f"{atoll} Category", categories, index=1, key=f"{atoll}_cat_{i}")
        percent = st.slider(f"{atoll} %", min_value=0, max_value=100, value=60, step=5, key=f"{atoll}_perc_{i}")
        
        selected_categories[atoll] = selected
        selected_percentages[atoll] = percent
    
    st.form_submit_button("Update Map")


# Map category colors
cmap_below = ListedColormap([
    '#ffffff', '#ffed5c', '#ffb833', '#ff8f00', '#f15c00', '#e20000'
])
cmap_normal = ListedColormap([
    '#ffffff', '#b2df8a', '#6dc068', '#2d933e', '#006a2e', '#014723'
])
cmap_above = ListedColormap([
    '#ffffff', '#c8c8ff', '#a6b6ff', '#8798f0', '#6c7be0', '#3c4fc2'
])

# Bins and normalization
bins = [0, 35, 45, 55, 65, 75, 100]
norm = BoundaryNorm(bins, ncolors=len(bins)-1, clip=True)
tick_positions = [35, 45, 55, 65, 75]
tick_labels = ['35', '45', '55', '65', '75']

# Map selections back to gdf
gdf['category'] = gdf['Name'].map(selected_categories)
gdf['prob'] = gdf['Name'].map(selected_percentages)

# Plotting
fig, ax = plt.subplots(figsize=(12, 10))

# Plot each category with its respective color map (Structure preserved)
for cat, cmap in zip(['Below Normal', 'Normal', 'Above Normal'],
                     [cmap_below, cmap_normal, cmap_above]):
    subset = gdf[gdf['category'] == cat]
    if not subset.empty:
        # This is the correct GeoDataFrame plotting method
        subset.plot(
            column='prob', cmap=cmap, norm=norm,
            edgecolor='black', linewidth=0.5, ax=ax
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

# Colorbar display
make_cb(ax, cmap_above, "Above Normal", 2 * spacing)
make_cb(ax, cmap_normal, "Normal", spacing)
make_cb(ax, cmap_below, "Below Normal", 0)

plt.tight_layout()

# Save and display
buf = BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

st.pyplot(fig)

# Download button
st.download_button(
    label="Download Map as PNG",
    data=buf,
    file_name='rainfall_outlook_map.png',
    mime='image/png'
)
