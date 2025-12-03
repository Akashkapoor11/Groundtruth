
# Insight Engine (H-001) - Automated Insight Engine (Hackathon-ready)

This repository is a complete end-to-end prototype for **H-001 — The Automated Insight Engine**.
It ingests a CSV dataset, transforms and aggregates metrics, detects anomalies, produces AI-written
insights (via OpenAI / fallback template), and generates a PDF + PPTX report.

## Structure
```
insight-engine/
├── data/
│   ├── input/          # put market_data.csv here (already included if you uploaded)
│   ├── staging/
│   └── final/
├── src/
│   ├── ingest.py
│   ├── transform.py
│   ├── analyze.py
│   ├── generate_insights.py
│   ├── generate_report.py
│   └── main.py
├── assets/
│   ├── template.html
│   └── template.pptx
├── requirements.txt
└── README.md
```

## How to run (locally)
1. Create and activate a Python venv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Place your CSV into `data/input/market_data.csv` (the repo includes the uploaded CSV if provided).

3. (Optional) Set `OPENAI_API_KEY` to enable AI-generated narrative (or the code will use template text).
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

4. Run the pipeline:
   ```bash
   python src/main.py
   ```

5. Outputs:
   - `data/staging/cleaned.csv`
   - `data/final/weekly_agg.csv`
   - `data/final/insights.json`
   - `data/final/report.pdf`
   - `data/final/report.pptx`

## Notes
- The AI integration uses `openai` by default. Replace with Google Gemini calls if you prefer.
- The HTML -> PDF conversion uses WeasyPrint. If you cannot install WeasyPrint on your environment,
  the repository still generates the PPTX output using `python-pptx`.
- Templates and prompts are in `src/generate_insights.py` and `assets/template.html`.
