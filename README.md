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
