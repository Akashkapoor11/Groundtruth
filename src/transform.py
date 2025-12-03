
import os
import pandas as pd
from datetime import datetime, timedelta

STAGING = os.path.join(os.path.dirname(__file__), "..", "data", "staging", "cleaned.csv")
FINAL = os.path.join(os.path.dirname(__file__), "..", "data", "final", "weekly_agg.csv")

def parse_date_col(df):
    # try common names
    for cand in ['date', 'Date', 'timestamp', 'datetime', 'day']:
        if cand in df.columns:
            df['date'] = pd.to_datetime(df[cand], errors='coerce')
            # if many non-nulls, return
            if df['date'].notna().sum() > 0:
                return df
    # fallback: try first column if it parses to many valid dates
    try:
        parsed = pd.to_datetime(df.iloc[:,0], errors='coerce')
        if parsed.notna().sum() > len(df) * 0.1:
            df['date'] = parsed
            return df
    except Exception:
        pass
    # If no date column, create a synthetic daily date series starting from 2023-01-01
    start = pd.to_datetime('2023-01-01')
    df = df.reset_index(drop=True)
    df['date'] = [start + timedelta(days=int(i)) for i in range(len(df))]
    return df

def run():
    print("Transform: reading staging file")
    df = pd.read_csv(STAGING)
    df = parse_date_col(df)
    # Fill simple numeric columns if present
    for col in ['visitors','visits','sales','revenue','impressions','clicks','orders','amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    # If canonical columns are missing, try mapping from dataset's numeric columns
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c not in ['index']]
    # Choose sensible defaults
    if 'visitors' not in df.columns:
        if 'Sale' in df.columns:
            df['visitors'] = df['Sale']  # treat Sale as visitors if no explicit visitors
        elif len(numeric_cols) > 0:
            df['visitors'] = df[numeric_cols[0]]
        else:
            df['visitors'] = 0
    if 'sales' not in df.columns:
        if 'Sale' in df.columns:
            df['sales'] = df['Sale']
        elif len(numeric_cols) > 1:
            df['sales'] = df[numeric_cols[1]]
        else:
            df['sales'] = 0
    if 'revenue' not in df.columns:
        if 'Price' in df.columns and 'Sale' in df.columns:
            df['revenue'] = df['Price'] * df['Sale']
        elif 'Price' in df.columns:
            df['revenue'] = df['Price']
        else:
            df['revenue'] = 0.0
    # weekly aggregation (ISO week) based on date
    df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time.date())
    agg = df.groupby('week').agg({'visitors':'sum','sales':'sum','revenue':'sum'}).reset_index()
    agg = agg.sort_values('week')
    os.makedirs(os.path.dirname(FINAL), exist_ok=True)
    agg.to_csv(FINAL, index=False)
    print("Saved weekly aggregation to", FINAL)
    return FINAL

if __name__ == '__main__':
    run()
