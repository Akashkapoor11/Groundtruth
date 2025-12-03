
import os
from src.ingest import run as ingest_run
from src.transform import run as transform_run
from src.analyze import run as analyze_run
from src.generate_insights import run as insights_run
from src.generate_report import run as report_run

def main():
    print('--- Insight Engine pipeline starting ---')
    ingest_run()
    transform_run()
    analyze_run()
    insights_run()
    report_run()
    print('--- Pipeline finished. Outputs in data/final/ ---')

if __name__ == '__main__':
    main()
