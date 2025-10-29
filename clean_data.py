# --- 🧭 SETUP ---
# Cleans Monthly_Transportation_Statistics.csv
# Keeps only transportation activity metrics and removes data before 1975.

import pandas as pd
import os
from pathlib import Path
from IPython.display import HTML, display

# --- 🔹 1. Upload your file ---
try:
    from google.colab import files
    uploaded = files.upload()
    INPUT_CSV = list(uploaded.keys())[0]
except Exception:
    print("Not running in Colab. Set INPUT_CSV manually.")
    INPUT_CSV = "Monthly_Transportation_Statistics.csv"

OUTPUT_CSV = "Monthly_Transportation_Statistics_cleaned.csv"

# --- 🔹 2. Load dataset ---
df = pd.read_csv(INPUT_CSV)
print("Original shape:", df.shape)

# --- 🔹 3. Helper function ---
orig_cols = df.columns.tolist()
lower_map = {c: c.lower() for c in orig_cols}
def col_has_any(col: str, needles_lower):
    col_l = lower_map[col]
    return any(n in col_l for n in needles_lower)

# --- 🔹 4. Remove irrelevant columns ---
exclude_1 = ["Fatalit", "Safety", "Spending", "sales", "Cost Index", "Price", "Construction"]
exclude_1_lower = [s.lower() for s in exclude_1]
keep_cols_1 = [c for c in orig_cols if not col_has_any(c, exclude_1_lower)]
df1 = df[keep_cols_1]

exclude_2 = [
    "Employment","Unemployment","Labor Force","GDP","Gross Domestic Product",
    "Participation Rate","Real","Amtrak On-time","Person Crossings"
]
exclude_2_lower = [s.lower() for s in exclude_2]
keep_cols_2 = [c for c in df1.columns if not col_has_any(c, exclude_2_lower)]
clean_df = df1[keep_cols_2].copy()

# --- 🔹 5. Parse date column ---
if "Date" in clean_df.columns:
    clean_df["Date_parsed"] = pd.to_datetime(clean_df["Date"], errors="coerce", infer_datetime_format=True)

# Try extracting year if parsing fails
if clean_df["Date_parsed"].isna().all():
    clean_df["Year"] = clean_df["Date"].astype(str).str.extract(r"(\d{4})")
    clean_df["Year"] = pd.to_numeric(clean_df["Year"], errors="coerce")
else:
    clean_df["Year"] = clean_df["Date_parsed"].dt.year

# --- 🔹 6. Remove data before 1975 ---
before_filter = clean_df.shape[0]
clean_df = clean_df[clean_df["Year"] >= 1975].reset_index(drop=True)
after_filter = clean_df.shape[0]
print(f"\n📅 Removed {before_filter - after_filter} rows before 1975.")
print("Years remaining:", sorted(clean_df["Year"].dropna().unique())[:5], "... →", sorted(clean_df["Year"].dropna().unique())[-5:])

# --- 🔹 7. Reorder columns ---
front = [c for c in ["Index", "Date", "Date_parsed", "Year"] if c in clean_df.columns]
other = [c for c in clean_df.columns if c not in front]
clean_df = clean_df[front + other]

# --- 🔹 8. Save intermediate file ---
clean_df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Saved cleaned file: {OUTPUT_CSV}")

# --- 🔹 9. Drop rows with no data ---
value_cols = [c for c in clean_df.columns if "Date" not in c and "Index" not in c and c not in ["Year"]]
lean_df = clean_df.dropna(subset=value_cols, how="all").reset_index(drop=True)
if "Date_parsed" in lean_df.columns:
    lean_df = lean_df.dropna(subset=["Date_parsed"]).reset_index(drop=True)

OUTPUT_CSV_FINAL = "Monthly_Transportation_Statistics_CLEAN_FINAL.csv"
lean_df.to_csv(OUTPUT_CSV_FINAL, index=False)
print(f"✅ Final cleaned dataset saved as: {OUTPUT_CSV_FINAL}")

# --- 🔹 10. Download section (3 methods) ---
try:
    from google.colab import files
    print("\n⬇️ Attempting Colab download...")
    files.download(OUTPUT_CSV_FINAL)
    print("✅ If nothing happens, enable pop-ups for Colab.")
except Exception as e:
    print("⚠️ Automatic download failed:", e)

# --- 🔹 Fallback: Manual link ---
abs_path = Path(OUTPUT_CSV_FINAL).resolve()
display(HTML(f"""
<h4>📎 Manual download options:</h4>
<ol>
<li>Open the <b>Files</b> sidebar on the left in Colab (folder icon).</li>
<li>Right-click <b>{OUTPUT_CSV_FINAL}</b> → <b>Download</b></li>
<li>Or click below:</li>
</ol>
<a href="{abs_path}" download><b>⬇️ Click here to download {OUTPUT_CSV_FINAL}</b></a>
"""))
