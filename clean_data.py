import pandas as pd
from pathlib import Path

# --- 🔹 1. Upload your file ---
# In Colab: run this cell, then select your CSV when prompted
from google.colab import files
uploaded = files.upload()

# Replace with the uploaded filename if different
INPUT_CSV = list(uploaded.keys())[0]
OUTPUT_CSV = "Monthly_Transportation_Statistics_cleaned.csv"

# --- 🔹 2. Load dataset ---
df = pd.read_csv(INPUT_CSV)
print("Original shape:", df.shape)

# --- 🔹 3. Helper to check column keywords ---
orig_cols = df.columns.tolist()
lower_map = {c: c.lower() for c in orig_cols}
def col_has_any(col: str, needles_lower):
    col_l = lower_map[col]
    return any(n in col_l for n in needles_lower)

# --- 🔹 4. Remove safety, spending, sales, and price/cost columns ---
exclude_1 = [
    "Fatalit", "Safety", "Spending", "sales", "Cost Index", "Price", "Construction"
]
exclude_1_lower = [s.lower() for s in exclude_1]
keep_cols_1 = [c for c in orig_cols if not col_has_any(c, exclude_1_lower)]
df1 = df[keep_cols_1]

# --- 🔹 5. Remove macroeconomic & employment data ---
exclude_2 = [
    "Employment", "Unemployment", "Labor Force", "GDP", "Gross Domestic Product",
    "Participation Rate", "Real", "Amtrak On-time", "Person Crossings"
]
exclude_2_lower = [s.lower() for s in exclude_2]
keep_cols_2 = [c for c in df1.columns if not col_has_any(c, exclude_2_lower)]
clean_df = df1[keep_cols_2].copy()

# --- 🔹 6. Parse dates for time series analysis ---
if "Date" in clean_df.columns:
    clean_df["Date_parsed"] = pd.to_datetime(clean_df["Date"], errors="coerce")

# Reorder columns to keep Date columns first
front = [c for c in ["Index", "Date", "Date_parsed"] if c in clean_df.columns]
other = [c for c in clean_df.columns if c not in front]
clean_df = clean_df[front + other]

# --- 🔹 7. Save cleaned dataset ---
clean_df.to_csv(OUTPUT_CSV, index=False)
print("\n✅ Cleaning complete!")
print("Original shape:", df.shape)
print("Cleaned shape:", clean_df.shape)

# --- 🔹 8. Display kept columns ---
print("\nKept columns:")
for c in clean_df.columns:
    print("-", c)

# --- 🔹 9. Download cleaned file ---
files.download(OUTPUT_CSV)
