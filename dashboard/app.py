import sys
import pathlib
from flask import Flask, render_template

# Add the project root to the Python path
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from flask import request
from agents.monitor.core import (
    calculate_compliance_score,
    gar_for_due,
    load_yaml,
)
from ai_assistant.agents.research_agent import ResearchAgent
from ai_assistant.agents.document_agent import DocumentAgent
from ai_assistant.main import load_settings

app = Flask(__name__)

@app.route('/')
def dashboard():
    wbs_file = ROOT_DIR / "wbs" / "wbs.yaml"
    rules_file = ROOT_DIR / "agents" / "monitor" / "rules" / "compliance_rules.yaml"

    wbs_data = load_yaml(wbs_file) or {}
    rules_data = load_yaml(rules_file) or {}

    compliance_score = calculate_compliance_score(wbs_data, rules_data)

    work_items = []
    for wp, items in (wbs_data.get("wbs") or {}).items():
        for item in items:
            item['gar'] = gar_for_due(item.get('due'))
            item['wp'] = wp
            work_items.append(item)

    return render_template('index.html', compliance_score=compliance_score, work_items=work_items)

@app.route('/research', methods=['GET', 'POST'])
def research():
    if request.method == 'POST':
        research_task = request.form.get('task')
        if not research_task:
            return render_template('research.html', error="Research task cannot be empty.")

        print(f"Received research task: {research_task}")

        settings = load_settings()
        if not settings:
            return render_template('research.html', error="Could not load AI assistant settings.")

        # Initialize both agents
        research_agent = ResearchAgent(settings)
        document_agent = DocumentAgent(settings)

        # Load context for the document agent
        brief_path = ROOT_DIR / "Horizon_Xilella.md"
        document_agent.load_project_brief(brief_path)

        # Run the full workflow
        potential_collaborators = research_agent.run(research_task)

        for collaborator in potential_collaborators:
            email_draft = document_agent.draft_outreach_email(collaborator)
            collaborator['outreach_email'] = email_draft

        return render_template('research.html', task=research_task, results=potential_collaborators)

    return render_template('research.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
