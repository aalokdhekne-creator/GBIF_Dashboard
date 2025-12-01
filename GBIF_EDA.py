# --- Code cell ---
import pandas as pd

# Load cleaned data
file_path = r"D:\APP_project\gbif_cleaned.csv"
df = pd.read_csv(file_path)

print("===================================")
print("KINGDOM DISTRIBUTION")
print("===================================")
print(df["kingdom"].value_counts())

print("\n===================================")
print("PHYLUM DISTRIBUTION (Top 10)")
print("===================================")
print(df["phylum"].value_counts().head(10))

print("\n===================================")
print("ORDER DISTRIBUTION (Top 10)")
print("===================================")
print(df["order"].value_counts().head(10))


# --- Code cell ---
import pandas as pd

# Load cleaned dataset
file_path = r"D:\APP_project\gbif_cleaned.csv"
df = pd.read_csv(file_path)

# List of taxonomic columns
taxonomy_cols = [
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species"
]

# Print distributions
for col in taxonomy_cols:
    if col in df.columns:
        print("\n" + "="*50)
        print(f"{col.upper()} DISTRIBUTION")
        print("="*50)
        print(df[col].value_counts())
    else:
        print(f"\n⚠️ Column '{col}' not found in dataset")


# --- Code cell ---
import pandas as pd
import matplotlib.pyplot as plt

file_path = r"D:\APP_project\gbif_cleaned.csv"
df = pd.read_csv(file_path)

counts = df["kingdom"].value_counts()
total = counts.sum()

plt.figure(figsize=(10,6))
bars = plt.bar(counts.index, counts.values)

plt.title("Kingdom Distribution (Log Scale)", fontsize=16, fontweight="bold")
plt.xlabel("Biological Kingdom")
plt.ylabel("Number of Records (log scale)")
plt.yscale("log")

# ✅ Add labels without clipping
for bar in bars:
    height = bar.get_height()
    percent = (height / total) * 100
    
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{int(height)}\n({percent:.2f}%)",
        ha='center',
        va='bottom',
        fontsize=10,
        clip_on=False  # ✅ THIS FIXES THE CUT-OFF ISSUE
    )

# ✅ Add top margin space safely
plt.margins(y=0.2)

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# --- Code cell ---
# Top-10 Phylum Distribution Plot
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
file_path = r"D:\APP_project\gbif_cleaned.csv"
df = pd.read_csv(file_path)

# Get Top 10 Phyla
counts = df["phylum"].value_counts().head(10)
total = df["phylum"].value_counts().sum()

plt.figure(figsize=(10,6))
bars = plt.bar(counts.index, counts.values)

plt.title("Top 10 Phylum Distribution (Log Scale)", fontsize=16, fontweight="bold")
plt.xlabel("Phylum")
plt.ylabel("Number of Records (log scale)")
plt.yscale("log")

# Add count + percentage labels (2 decimals)
for bar in bars:
    height = bar.get_height()
    percent = (height / total) * 100
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{int(height)}\n({percent:.2f}%)",
        ha='center',
        va='bottom',
        fontsize=10,
        clip_on=False
    )

plt.margins(y=0.2)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# --- Code cell ---
# Top-10 Order Distribution Plot
# Get Top 10 Orders
counts = df["order"].value_counts().head(10)
total = df["order"].value_counts().sum()

plt.figure(figsize=(10,6))
bars = plt.bar(counts.index, counts.values)

plt.title("Top 10 Order Distribution (Log Scale)", fontsize=16, fontweight="bold")
plt.xlabel("Order")
plt.ylabel("Number of Records (log scale)")
plt.yscale("log")

# Add count + percentage labels (2 decimals)
for bar in bars:
    height = bar.get_height()
    percent = (height / total) * 100
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{int(height)}\n({percent:.2f}%)",
        ha='center',
        va='bottom',
        fontsize=10,
        clip_on=False
    )

plt.margins(y=0.2)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()



# --- Code cell ---
#Country Distribution (Bar Plot)
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
file_path = r"D:\APP_project\gbif_cleaned.csv"
df = pd.read_csv(file_path)

# Top 20 countries
country_counts = df["countryCode"].value_counts().head(20)

plt.figure(figsize=(12,6))
bars = plt.bar(country_counts.index, country_counts.values)

plt.title("Top 20 Countries by Number of Observations", fontsize=16, fontweight="bold")
plt.xlabel("Country Code")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# --- Code cell ---
# Top States/Provinces Plot
state_counts = df["stateProvince"].value_counts().head(20)

plt.figure(figsize=(12,6))
bars = plt.bar(state_counts.index, state_counts.values)

plt.title("Top 20 States/Provinces by Observations", fontsize=16, fontweight="bold")
plt.xlabel("State / Province")
plt.ylabel("Number of Records")

plt.xticks(rotation=60, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# --- Code cell ---
# Latitude vs Longitude Scatter Plot
plt.figure(figsize=(10,6))

plt.scatter(
    df["decimalLongitude"],
    df["decimalLatitude"],
    s=3,
    alpha=0.5
)

plt.title("Global Distribution of Observations", fontsize=16, fontweight="bold")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# --- Code cell ---
# Country Density Table
# Country density table
country_density = df["countryCode"].value_counts()

print("\nTop 20 Countries by Record Count:")
print(country_density.head(20))


# --- Code cell ---


