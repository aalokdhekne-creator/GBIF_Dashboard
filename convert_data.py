import pandas as pd

def convert_csv_to_parquet():
    print("Loading CSV...")
    df = pd.read_csv("gbif_cleaned.csv")
    
    print("Processing dates...")
    df["eventDate"] = pd.to_datetime(df["eventDate"], errors="coerce")
    df["year"] = df["eventDate"].dt.year
    df["month"] = df["eventDate"].dt.month
    
    print("Optimizing data types...")
    # Convert object columns to category for massive memory savings
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("category")
        
    print("Saving to Parquet...")
    df.to_parquet("gbif_cleaned.parquet", index=False)
    print("Done! Saved as gbif_cleaned.parquet")

if __name__ == "__main__":
    convert_csv_to_parquet()
