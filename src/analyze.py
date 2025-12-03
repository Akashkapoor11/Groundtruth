
import os, json
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

FINAL = os.path.join(os.path.dirname(__file__), "..", "data", "final", "weekly_agg.csv")
OUT_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "final", "insights.json")

def detect_anomalies(df):
    # use visitors + revenue for anomaly detection (simple)
    X = df[['visitors','revenue']].fillna(0).values
    if len(X) < 3:
        return []
    iso = IsolationForest(contamination=0.1, random_state=42)
    labels = iso.fit_predict(X)
    df['anomaly'] = (labels==-1)
    anomalies = []
    for _, row in df[df['anomaly']].iterrows():
        anomalies.append({'week': str(row['week']), 'description': f"Visitors={int(row['visitors'])}, Revenue={row['revenue']} (flagged as anomaly)"})
    return anomalies

def run():
    df = pd.read_csv(FINAL, parse_dates=['week'])
    anomalies = detect_anomalies(df)
    # produce some simple metrics
    metrics = []
    df_sorted = df.sort_values('week')
    prev = None
    for _, r in df_sorted.iterrows():
        week = str(r['week']) if not pd.isna(r['week']) else ''
        visitors = int(r['visitors'])
        sales = int(r['sales'])
        revenue = float(r['revenue'])
        change = None
        if prev is not None:
            change = {'visitors_pct': round((visitors - prev['visitors'])/max(prev['visitors'],1)*100,2)}
        else:
            change = {'visitors_pct': None}
        metrics.append({'week': week, 'visitors': visitors, 'sales': sales, 'revenue': revenue, 'change': change})
        prev = {'visitors': visitors}
    out = {'metrics': metrics, 'anomalies': anomalies}
    with open(OUT_JSON, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print('Saved analysis to', OUT_JSON)
    return OUT_JSON

if __name__ == '__main__':
    run()
