# ===============================================================
# GBIF BIODIVERSITY DASHBOARD — FINAL VERSION (92,142 POINTS)
# NO SAMPLING • FOLIUM CLUSTER • YEAR FILTER • SPECIES SEARCH
# ===============================================================

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="GBIF Dashboard", layout="wide")

# ---------------- BACKGROUND COLOR THEME -----------------------
st.markdown("""
    <style>
        .main {
            background-color: #f4f6fa;
        }
        .sidebar .sidebar-content {
            background-color: #eef1f6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 GBIF Biodiversity Dashboard")


# ---------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    # Load from optimized Parquet file
    try:
        df = pd.read_parquet("gbif_cleaned.parquet")
    except FileNotFoundError:
        st.error("Parquet file not found. Please run convert_data.py first.")
        return pd.DataFrame()
    return df

df = load_data()

# Metadata lists
countries = sorted(df["countryCode"].dropna().unique())
kingdoms = sorted(df["kingdom"].dropna().unique())
years = sorted(df["year"].dropna().unique())
species_list = sorted(df["species"].dropna().unique())

taxonomy_levels = {
    "Kingdom": "kingdom",
    "Phylum": "phylum",
    "Class": "class",
    "Order": "order",
    "Family": "family",
    "Genus": "genus",
    "Species": "species"
}


# ---------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------
st.sidebar.title("🔍 Filters")

selected_country = st.sidebar.selectbox("Country", ["All"] + countries)
selected_kingdoms = st.sidebar.multiselect("Kingdom", kingdoms, default=kingdoms)
selected_years = st.sidebar.multiselect("Year", years, default=years)

species_query = st.sidebar.text_input("🔎 Search Species (Exact Match):")



# ---------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------
mask = pd.Series(True, index=df.index)

if selected_country != "All":
    mask &= df["countryCode"] == selected_country

mask &= df["kingdom"].isin(selected_kingdoms)
mask &= df["year"].isin(selected_years)

if species_query:
    mask &= df["species"].astype(object).fillna("").str.lower() == species_query.lower()

filtered_df = df[mask]


# ---------------------------------------------------------------
# MAP + SUMMARY
# ---------------------------------------------------------------
st.subheader("🌍 Map & Summary")

map_col, summary_col = st.columns([2, 1])

with summary_col:
    st.write("### 📊 Summary Statistics")
    st.metric("Total Records", len(filtered_df))
    st.metric("Unique Species", filtered_df["species"].nunique())
    st.metric("Unique Genera", filtered_df["genus"].nunique())
    st.metric("Unique Families", filtered_df["family"].nunique())

    st.write("### 🗺️ Map Options")
    use_heatmap = st.checkbox("Heatmap", value=False)
    use_clusters = st.checkbox("Clusters", value=True)


# ---------------------------------------------------------------
# MAP + SUMMARY
# ---------------------------------------------------------------
with map_col:

    st.write("### Filtered Biodiversity Map")

    # -----------------------------------------------------------
    # AUTO-ZOOM LOGIC
    # -----------------------------------------------------------
    sub = filtered_df.dropna(subset=["decimalLatitude", "decimalLongitude"])

    if len(sub) > 0:
        center_lat = sub["decimalLatitude"].mean()
        center_lon = sub["decimalLongitude"].mean()
        zoom_level = 5 if selected_country != "All" else 3
    else:
        center_lat, center_lon, zoom_level = 20, 0, 2

    if species_query:
        zoom_level = 6

    # -----------------------------------------------------------
    # CREATE FOLIUM MAP
    # -----------------------------------------------------------
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)

    map_df = sub   # ALL 92k points

    # ---------------- OPTIMIZED CLUSTERING ---------------------
    if use_clusters and len(map_df) > 0:
        # FastMarkerCluster is much faster than adding individual markers
        from folium.plugins import FastMarkerCluster
        
        # Prepare data as list of [lat, lon]
        locations = map_df[["decimalLatitude", "decimalLongitude"]].values.tolist()
        
        FastMarkerCluster(data=locations).add_to(m)
    
    # ---------------- INDIVIDUAL POINTS (Fallback/Non-cluster) -
    elif not use_clusters and len(map_df) < 2000:
         # Only render individual points if count is low to prevent crash
        for _, row in map_df.iterrows():
            folium.CircleMarker(
                location=[row["decimalLatitude"], row["decimalLongitude"]],
                radius=3,
                color="blue",
                fill=True,
                fill_opacity=0.7,
                popup=f"{row['species']}"
            ).add_to(m)
    elif not use_clusters:
        st.warning("Too many points to display without clustering. Showing Heatmap instead.")
        use_heatmap = True

    # ---------------- HEATMAP OPTION ---------------------------
    if use_heatmap:
        # Generate heat_data efficiently
        heat_data = map_df[["decimalLatitude", "decimalLongitude"]].values.tolist()
        HeatMap(heat_data).add_to(m)

    # ---------------- DISPLAY MAP ------------------------------
    # ---------------- DISPLAY MAP ------------------------------
    st_folium(
        m,
        width=850,
        height=500,
        key=f"map_{selected_country}_{species_query}_{selected_years}_{use_heatmap}_{use_clusters}"
    )


# ---------------------------------------------------------------
# TABS
# ---------------------------------------------------------------
tab1, tab2 = st.tabs(["📈 Time Series", "🧬 Taxonomy"])


# ---------------------------------------------------------------
# TAB 1 — TIME SERIES
# ---------------------------------------------------------------
with tab1:

    st.write("### Yearly Observations")

    yearly = filtered_df.groupby("year").size().reset_index(name="count")
    fig_year = px.line(yearly, x="year", y="count", markers=True,
                       title="Yearly Observation Trend", template="plotly_white")
    fig_year.update_layout(height=350)
    st.plotly_chart(fig_year, use_container_width=True)

    st.write("### Monthly Observations")

    monthly = filtered_df.groupby("month").size().reset_index(name="count")
    fig_month = px.bar(monthly, x="month", y="count",
                       title="Monthly Observation Distribution", template="plotly_white")
    fig_month.update_layout(height=350)
    st.plotly_chart(fig_month, use_container_width=True)


# ---------------------------------------------------------------
# TAB 2 — TAXONOMY
# ---------------------------------------------------------------
with tab2:

    st.write("### Select Taxonomic Level")

    level_name = st.selectbox("Choose Level", list(taxonomy_levels.keys()))
    col_name = taxonomy_levels[level_name]

    values = filtered_df[col_name].astype(object).fillna("Unknown")

    top10 = values.value_counts().reset_index()
    top10.columns = [level_name, "Count"]
    top10 = top10.head(10)

    fig_tax = px.bar(top10, x=level_name, y="Count",
                     title=f"Top 10 {level_name} Observed", template="plotly_white")
    fig_tax.update_layout(height=400, xaxis_tickangle=-40)
    st.plotly_chart(fig_tax, use_container_width=True)


# ---------------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------------------
st.subheader("📥 Download Filtered Dataset")

st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_gbif.csv",
    mime="text/csv",
    use_container_width=True,
    key="download_filtered"
)
