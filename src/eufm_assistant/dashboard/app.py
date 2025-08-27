from flask import Flask, render_template, request, jsonify
import os
import yaml

from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.monitor.monitor import get_wbs_data, calculate_compliance_score

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    wbs_data = get_wbs_data()
    compliance_score = calculate_compliance_score(wbs_data)
    return render_template('index.html', wbs_data=wbs_data, compliance_score=compliance_score)

@app.route('/research', methods=['GET', 'POST'])
def research():
    if request.method == 'POST':
        query = request.form['query']

        research_agent = ResearchAgent()
        partner_data = research_agent.run(query)

        if partner_data:
            document_agent = DocumentAgent()
            emails = document_agent.draft_outreach_emails(partner_data)

            # Combine partner data and emails
            results = []
            for i, partner in enumerate(partner_data):
                results.append({
                    "partner": partner,
                    "email": emails[i]
                })

            return render_template('research.html', results=results)
        else:
            return render_template('research.html', message="No partners found for the given query.")

    return render_template('research.html')

@app.route('/strategy')
def strategy():
    try:
        with open('src/eufm_assistant/docs/Horizon_Xilella.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "Strategy document not found."
    return render_template('strategy.html', strategy_content=content)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
