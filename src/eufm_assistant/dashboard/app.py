import pathlib
from flask import Flask, render_template, request

from eufm_assistant.agents.monitor.core import (
    calculate_compliance_score,
    gar_for_due,
    load_yaml,
)
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.ai_assistant.main import load_settings

# The project root is now 3 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]

app = Flask(__name__)

@app.route('/')
def dashboard():
    wbs_file = PROJECT_ROOT / "wbs" / "wbs.yaml"
    rules_file = PROJECT_ROOT / "src" / "eufm_assistant" / "agents" / "monitor" / "rules" / "compliance_rules.yaml"

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
        brief_path = PROJECT_ROOT / "Horizon_Xilella.md"
        document_agent.load_project_brief(brief_path)

        # Run the full workflow
        potential_collaborators = research_agent.run(research_task)

        for collaborator in potential_collaborators:
            email_draft = document_agent.draft_outreach_email(collaborator)
            collaborator['outreach_email'] = email_draft

        return render_template('research.html', task=research_task, results=potential_collaborators)

    return render_template('research.html')

if __name__ == '__main__':
    # To run this script directly for testing, you would need to be in the project root
    # and run `python -m src.eufm_assistant.dashboard.app`
    app.run(debug=True, host='0.0.0.0', port=8081)
