# --- Code cell ---
import pandas as pd
import numpy as np
import re

# ===============================
# Load dataset
# ===============================
file_path = r"D:\APP_project\dataset_2.csv"
df = pd.read_csv(file_path)

print("\n==============================")
print("BASIC INFO")
print("==============================")
print("Shape (rows, columns):", df.shape)

# ===============================
# 1. Missing & Empty Checks
# ===============================
print("\n==============================")
print("MISSING VALUES (COUNT)")
print("==============================")
missing_count = df.isna().sum()
print(missing_count)

print("\n==============================")
print("MISSING VALUES (%)")
print("==============================")
missing_percent = (df.isna().mean() * 100).round(2)
print(missing_percent)

print("\n==============================")
print("COMPLETELY EMPTY COLUMNS")
print("==============================")
empty_cols = missing_count[missing_count == len(df)].index.tolist()
print(empty_cols)

# ===============================
# 2. Inconsistency Checks
# ===============================
print("\n==============================")
print("INCONSISTENCY CHECKS")
print("==============================")

# ---- Coordinate checks (fixed for old pandas) ----
df["decimalLatitude"] = pd.to_numeric(df["decimalLatitude"], errors="coerce")
df["decimalLongitude"] = pd.to_numeric(df["decimalLongitude"], errors="coerce")

invalid_lat = df[
    (df["decimalLatitude"].notna()) &
    ((df["decimalLatitude"] < -90) | (df["decimalLatitude"] > 90))
]

invalid_lon = df[
    (df["decimalLongitude"].notna()) &
    ((df["decimalLongitude"] < -180) | (df["decimalLongitude"] > 180))
]

print("Invalid latitudes:", len(invalid_lat))
print("Invalid longitudes:", len(invalid_lon))

# ---- Year validation ----
if "year" in df.columns:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    invalid_year = df[(df["year"].notna()) & ((df["year"] < 1700) | (df["year"] > 2025))]
    print("Invalid years:", len(invalid_year))

# ---- Negative individualCount ----
if "individualCount" in df.columns:
    df["individualCount"] = pd.to_numeric(df["individualCount"], errors="coerce")
    neg_individuals = df[df["individualCount"] < 0]
    print("Negative individualCount:", len(neg_individuals))

# ---- Coordinate uncertainty consistency ----
if "coordinateUncertaintyInMeters" in df.columns:
    df["coordinateUncertaintyInMeters"] = pd.to_numeric(df["coordinateUncertaintyInMeters"], errors="coerce")
    bad_uncertainty = df[df["coordinateUncertaintyInMeters"] < 0]
    print("Negative coordinateUncertaintyInMeters:", len(bad_uncertainty))

# ---- Country code checks ----
if "countryCode" in df.columns:
    invalid_country = df[
        df["countryCode"].notna() &
        ~df["countryCode"].astype(str).str.match(r"^[A-Z]{2}$")
    ]
    print("Invalid country codes:", len(invalid_country))

# ---- Messy blank text fields ----
text_cols = ["stateProvince", "locality", "habitat"]
for col in text_cols:
    if col in df.columns:
        blank_like = df[
            df[col].astype(str).str.strip().isin(["", "nan", "None"])
        ]
        print(f"Blank-like values in {col}:", len(blank_like))


# --- Code cell ---
import pandas as pd

# ===============================
# Load dataset
# ===============================
file_path = r"D:\APP_project\dataset_2.csv"
df = pd.read_csv(file_path)

print("Original shape:", df.shape)

# ===============================
# 1. Drop completely empty columns
# ===============================
empty_cols = [
    'verbatimScientificNameAuthorship',
    'locality',
    'individualCount',
    'coordinatePrecision',
    'elevation', 'elevationAccuracy',
    'depth', 'depthAccuracy',
    'recordNumber',
    'typeStatus',
    'establishmentMeans'
]

df = df.drop(columns=empty_cols, errors="ignore")
print("After dropping empty columns:", df.shape)

# ===============================
# 2. Clean text-like columns
# ===============================
text_cols = ["stateProvince", "mediaType"]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

# ===============================
# 3. Handle partial missing values
# ===============================
# Fill countryCode missing
df["countryCode"] = df["countryCode"].fillna("Unknown")

# Flag missing speciesKey
df["speciesKey_missing"] = df["speciesKey"].isna()

# ===============================
# 4. Date Parsing
# ===============================
df["eventDate"] = pd.to_datetime(df["eventDate"], errors="coerce")

df["year"] = df["eventDate"].dt.year
df["month"] = df["eventDate"].dt.month
df["day"] = df["eventDate"].dt.day

# Keep only reasonable year range
df = df[df["year"].between(1800, 2025)]

# ===============================
# 5. Coordinate Cleaning
# ===============================
df["decimalLatitude"] = pd.to_numeric(df["decimalLatitude"], errors="coerce")
df["decimalLongitude"] = pd.to_numeric(df["decimalLongitude"], errors="coerce")

df = df[
    df["decimalLatitude"].between(-90, 90) &
    df["decimalLongitude"].between(-180, 180)
]

# Clean coordinate uncertainty
df["coordinateUncertaintyInMeters"] = pd.to_numeric(
    df["coordinateUncertaintyInMeters"],
    errors="coerce"
)

MAX_UNCERTAINTY = 10000  # 10 km threshold

df = df[
    df["coordinateUncertaintyInMeters"].isna() |
    (df["coordinateUncertaintyInMeters"] <= MAX_UNCERTAINTY)
]

# ===============================
# 6. Final checks
# ===============================
print("Final shape:", df.shape)

print("\nRemaining missing values (%):")
print((df.isna().mean() * 100).round(2).sort_values(ascending=False))

# ===============================
# 7. Save cleaned dataset
# ===============================
clean_path = r"D:\APP_project\gbif_cleaned.csv"
df.to_csv(clean_path, index=False)

print("\n✅ Cleaned dataset saved at:")
print(clean_path)


# --- Code cell ---


