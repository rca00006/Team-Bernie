import pandas as pd

# Load dataset
df = pd.read_csv("Monthly_Transportation_Statistics.csv")

# 1️⃣ Strip whitespace from column names
df.columns = df.columns.str.strip()

# 2️⃣ Drop exact duplicate rows
df = df.drop_duplicates()

# 3️⃣ Try to parse any date-like columns automatically
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            parsed = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
            if parsed.notna().sum() > 0.5 * len(parsed):  # if more than 50% valid dates
                df[col] = parsed
        except Exception:
            pass

# 4️⃣ Convert columns that look numeric to numeric
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='ignore')

# 5️⃣ Save cleaned version
df.to_csv("Monthly_Transportation_Statistics_CLEANED.csv", index=False)

print("✅ Data cleaned and saved as 'Monthly_Transportation_Statistics_CLEANED.csv'")
