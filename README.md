## 🚀 GroundTruth: Automated Insight Engine

Tagline:
A fully automated ETL + AI system that converts raw CSV time-series data into weekly aggregated insights, AI-generated narratives, and a PowerPoint report — all in under 30 seconds.

1. The Problem (Real-World Scenario)
Context

Organizations generate massive amounts of raw CSV data — weather logs, sales data, performance metrics, ad spends, traffic logs, etc.
Yet, analysts still spend hours every week manually:

Cleaning the CSV

Aggregating weekly trends

Finding insights

Generating reports

Summarizing results for leadership

Pain Point

This manual workflow is:

❌ Slow
❌ Error-prone
❌ Boring
❌ Hard to scale

Teams waste time on formatting instead of real decision-making.

My Solution — GroundTruth

I built GroundTruth, a completely automated system that:

Ingests any time-series CSV

Cleans & validates data

Aggregates weekly insights

Generates AI-written summaries

Exports a ready-to-share PowerPoint report

Runs end-to-end with one command

This reduces hours of analyst work into 30 seconds.

2. Expected End Result
For the User
Input

📁 Drop a CSV file inside:

data/input/

Action

▶ Run:

python -m src.main

Output

Automatically generated inside:

data/final/


Includes:

weekly_agg.csv → Week-over-week trends

insights.json → Rule-based statistics

insights_ai.json → AI-generated narrative

report.pptx → Final presentation (charts + insights)

3. Technical Approach

GroundTruth is designed as a modular ETL pipeline, following industry best practices.

System Architecture
1. Ingestion

Reads raw CSV

Auto-detects date column

Cleans missing values

Stores sanitized data → data/staging/cleaned.csv

2. Transformation

Converts data into weekly buckets

Computes:

Average temperature / sales / KPI

Total values per week

Min-Max trends

3. Analysis

Extracts:

Latest week summary

Column-wise stats

Week-over-week changes

4. AI Insight Generation

Creates human-like summaries

Highlights anomalies

Converts numbers → stories

5. Reporting

Generates a PowerPoint report:

Title page

Weekly table

Insight summary

4. Tech Stack

Language: Python 3.x

Libraries: Pandas, Polars, Scikit-Learn

Reporting: python-pptx

AI: Local LLM summarization (or OpenAI/Gemini if plugged in)

Visualization: Matplotlib (optional)

ETL Framework: Custom pipeline

5. Challenges & Learnings
Challenge 1: Inconsistent Datasets

Some datasets lacked the required columns (date, numeric fields).

Solution:
Auto-detect date column and dynamically map numeric metrics.

Challenge 2: Weekly Aggregation Bugs

Missing weeks created reporting gaps.

Solution:
Introduced resampling + auto-fill for missing dates.

Challenge 3: AI Narrative Accuracy

AI summaries sometimes inflated numbers.

Solution:
Strict “use only provided statistics” guardrails.

6. Visual Proof
PPT Output

Generated report contains:

Latest week summary

Weekly aggregated table

Clean formatting

Auto-generated title slide

(Include screenshots here if you want)

7. Folder Structure
insight-engine-updated/
│
├── data/
│   ├── input/          # Raw CSV goes here
│   ├── staging/        # Cleaned intermediate files
│   └── final/          # Final outputs (CSV, JSON, PPTX)
│
├── src/
│   ├── ingest.py       # Data ingestion
│   ├── transform.py    # Weekly aggregation
│   ├── analyze.py      # Statistical analysis
│   ├── generate_insights.py  # AI narrative generation
│   ├── generate_report.py    # PPTX generator
│   └── main.py         # Pipeline orchestrator
│
├── assets/             # HTML / templates
├── requirements.txt
└── README.md

8. How to Run
1. Clone the Repo
git clone https://github.com/Akashkapoor11/Groundtruth.git
cd Groundtruth

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Add Your CSV

Place your file inside:

data/input/market_data.csv

5. Run Pipeline
python -m src.main

6. Check Output
data/final/report.pptx
data/final/weekly_agg.csv
data/final/insights.json
data/final/insights_ai.json
