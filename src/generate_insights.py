
import os, json, os, textwrap
from jinja2 import Template
OPENAI_KEY = os.environ.get('OPENAI_API_KEY', None)

INSIGHTS_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "final", "insights.json")
REPORT_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "final", "insights_ai.json")

DEFAULT_PROMPT = textwrap.dedent("""
You are an analytics assistant. Given weekly metrics and anomalies, write:
1) A concise 2-line executive summary.
2) 3 bullet key findings.
3) 2 action-oriented recommendations.
Do not hallucinate beyond the data.
""")

def local_generate(analysis):
    # Build a human-readable insight using the analysis JSON as input
    metrics = analysis.get('metrics', [])
    anomalies = analysis.get('anomalies', [])
    latest = metrics[-1] if metrics else {}
    summary = f"Latest week ({latest.get('week','N/A')}): visitors={latest.get('visitors',0)}, revenue={latest.get('revenue',0)}."
    bullets = []
    bullets.append(f"Total weeks analyzed: {len(metrics)}.")
    if anomalies:
        bullets.append(f"Detected {len(anomalies)} anomalous weeks; most recent: {anomalies[-1].get('week')}")
    else:
        bullets.append('No anomalies detected.')
    bullets.append(f"Recent week visitors change: {latest.get('change',{}).get('visitors_pct')}%")
    recs = ["Investigate high-impact anomalous weeks (check campaigns, local events, outages).", "If revenue dropped, consider shifting budget to top performing regions / weeks."]
    out = {'summary': summary, 'bullets': bullets, 'recommendations': recs}
    return out

def run():
    with open(INSIGHTS_JSON) as f:
        analysis = json.load(f)
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            prompt = DEFAULT_PROMPT + "\n\nAnalysis JSON:\n" + json.dumps(analysis)
            resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], max_tokens=400)
            text = resp['choices'][0]['message']['content']
            ai_out = {'ai_text': text}
        except Exception as e:
            print('OpenAI call failed, falling back to local generator:', e)
            ai_out = local_generate(analysis)
    else:
        ai_out = local_generate(analysis)
    with open(REPORT_JSON, 'w') as f:
        json.dump({'analysis': analysis, 'insights': ai_out}, f, indent=2, default=str)
    print('Saved AI insights to', REPORT_JSON)
    return REPORT_JSON

if __name__ == '__main__':
    run()
