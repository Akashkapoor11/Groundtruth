import pandas as pd
import os

INPUT = os.path.join(os.path.dirname(__file__), "..", "data", "input", "market_data.csv")
STAGING = os.path.join(os.path.dirname(__file__), "..", "data", "staging", "cleaned.csv")

def clean_numeric(col):
    return (
        col.astype(str)
        .str.replace(",", "", regex=True)
        .str.replace(" ", "", regex=True)
        .str.replace("$", "", regex=True)
        .str.replace("₹", "", regex=True)
        .str.replace("-", "0", regex=True)
        .astype(float)
    )

def detect_date_column(cols):
    possible = ["date", "week", "timestamp", "day", "time"]
    for name in possible:
        if name in cols:
            return name
    return None

def run():
    print(f"Ingesting {INPUT}")

    df = pd.read_csv(INPUT)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    cols = df.columns.tolist()
    print("Detected columns:", cols)

    # detect date column
    date_col = detect_date_column(cols)
    if not date_col:
        raise Exception(f"No date-like column found. Columns = {cols}")

    print(f"Using '{date_col}' as date column")

    # convert date column
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # numeric columns
    num_cols = [c for c in df.columns if c not in [date_col] and df[c].dtype != "datetime64[ns]"]

    for col in num_cols:
        df[col] = clean_numeric(df[col])

    df = df.dropna()

    os.makedirs(os.path.dirname(STAGING), exist_ok=True)
    df.to_csv(STAGING, index=False)

    print(f"Saved cleaned staging file to {STAGING}")
    return True

if __name__ == "__main__":
    run()
