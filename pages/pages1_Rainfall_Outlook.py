import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import box
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import streamlit as st
from io import BytesIO

st.set_page_config(
    page_title="Rainfall Outlook",
    page_icon="🌧️",
    layout="wide"
)

# --- Configuration for Header and Hiding Icons ---
st.markdown(
    """
    <style>
    /* 1. HIDE DEVELOPER ICONS (Share, Star, Pencil, GitHub) */
    .st-emotion-cache-12fmw9a { 
        visibility: hidden;
        width: 0px;
        height: 0px;
    }
    
    /* 2. CUSTOM BLUE HEADER BAR (Copied for consistency) */
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
    /* 3. Push main content down to account for the fixed header */
    .st-emotion-cache-1g8i5u7, .st-emotion-cache-6qob1r, .st-emotion-cache-1y4pm5r {
        padding-top: 80px; 
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">Forecasters\' Tools</div>', unsafe_allow_html=True)
st.title("🌧️ Rainfall Outlook Map")
# ------------------------------

# Load shapefile and clip extent
# CRITICAL FIX: Added quotes around the file path
shp = 'data/Atoll_boundary2016.shp'
gdf = gpd.read_file(shp).to_crs(epsg=4326)
bbox = box(71, -1, 75, 7.5)
gdf = gdf[gdf.intersects(bbox)]

# ✅ Clean missing or invalid atoll names
gdf['Name'] = gdf['Name'].fillna("Unknown")

# ✅ Ensure unique atoll names
unique_atolls = sorted(gdf['Name'].unique().tolist())

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

# Sidebar inputs for each unique atoll
for i, atoll in enumerate(unique_atolls):
    selected = st.sidebar.selectbox(f"{atoll} Category", categories, index=1, key=f"{atoll}_cat_{i}")
    percent = st.sidebar.slider(f"{atoll} %", min_value=0, max_value=100, value=60, step=5, key=f"{atoll}_perc_{i}")
    
    selected_categories[atoll] = selected
    selected_percentages[atoll] = percent

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

# ✅ Map selections back to gdf (so all parts of same atoll share same values)
gdf['category'] = gdf['Name'].map(selected_categories)
gdf['prob'] = gdf['Name'].map(selected_percentages)

# Plotting
fig, ax = plt.subplots(figsize=(12, 10))

# Plot each category with its respective color map
for cat, cmap in zip(['Below Normal', 'Normal', 'Above Normal'],
                     [cmap_below, cmap_normal, cmap_above]):
    subset = gdf[gdf['category'] == cat]
    if not subset.empty:
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

# ✅ Rearranged order — Above on top, Normal middle, Below bottom
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
