# 🌍 GBIF Biodiversity Analysis & Interactive Dashboard

An end-to-end biodiversity analytics project built using data from the **Global Biodiversity Information Facility (GBIF)**.  
This repository demonstrates a complete data science pipeline including **data cleaning, exploratory data analysis (EDA), data optimization, and interactive dashboard deployment**.

---

## 🚀 Live Dashboard

👉 **Deploy Dashboard**  
🔗 https://gbifdashboard-i5zf8kce5lknmm6kkypnlm.streamlit.app/

The Streamlit dashboard enables interactive exploration of:
- Global biodiversity observations
- Taxonomic distributions
- Geographic patterns and country-wise contributions
- Temporal trends in biodiversity reporting
- Summary biodiversity metrics

---

## 📌 Project Objectives

- Analyze global biodiversity occurrence records from GBIF
- Study taxonomic, geographic, and temporal distributions
- Identify sampling bias and under-sampled regions
- Perform EDA on cleaned biodiversity data
- Build a scalable and interactive biodiversity dashboard

---

## 🔄 Workflow Overview

**Raw Data → Cleaning → EDA → Optimization → Dashboard**

This pipeline ensures data quality, performance optimization, and meaningful visualization.

---

## 🗂 Repository Structure

```plaintext
.
├── dataset_2.zip
│   └── Raw uncleaned biodiversity data (GBIF source)
│
├── gbif_cleaned.zip
│   └── Contains gbif_cleaned.csv (cleaned dataset)
│
├── gbif_cleaned.csv
│   └── Cleaned biodiversity dataset (used for EDA)
│
├── gbif_cleaned.parquet
│   └── Optimized binary dataset used by the dashboard
│
├── GBIF_Data_Cleaning.py
│   └── Script for cleaning raw GBIF data
│
├── GBIF_EDA.py
│   └── Performs exploratory data analysis on cleaned CSV
│
├── convert_data.py
│   └── Converts gbif_cleaned.csv → gbif_cleaned.parquet
│
├── dashboard.py
│   └── Main Streamlit dashboard application
│
└── README.md

--

🧪 Methodology
1️⃣ Data Acquisition

Raw biodiversity occurrence data downloaded from GBIF.

Dataset includes taxonomic hierarchy, geographic coordinates, and event dates.

2️⃣ Data Cleaning & Pre-processing

Script: GBIF_Data_Cleaning.py

Removed irrelevant and empty columns

Standardized text fields

Validated latitude and longitude ranges

Cleaned ISO country codes

Handled missing and inconsistent records

Output: gbif_cleaned.csv

3️⃣ Exploratory Data Analysis (EDA)

Script: GBIF_EDA.py
Data Used: gbif_cleaned.csv

EDA includes:

Taxonomic distributions (kingdom → species)

Observation frequency analysis

Geographic and country-wise summaries

Preliminary statistical insights

EDA is intentionally performed on CSV format for transparency and inspection.

4️⃣ Data Optimization

Script: convert_data.py

Converted cleaned CSV into Parquet format

Optimized data types for memory efficiency

Prepared dataset for fast dashboard queries

Output: gbif_cleaned.parquet

Why Parquet?

Faster I/O

Lower memory usage

Better performance for interactive dashboards

5️⃣ Dashboard Development

Main file: dashboard.py
Data source: gbif_cleaned.parquet

Dashboard features:

Interactive filters (country, taxonomy, year)

Taxonomic distribution plots

Geographic maps (cluster map, heatmap, point map)

Temporal trend analysis

Summary metrics:

Total records

Unique species

Genera and families count

▶️ Running the Project Locally
Install Dependencies
pip install pandas numpy matplotlib seaborn streamlit pyarrow folium

Optional: Clean Raw Data
python GBIF_Data_Cleaning.py

Perform EDA
python GBIF_EDA.py

Convert CSV to Parquet
python convert_data.py

Launch Dashboard
streamlit run dashboard.py

