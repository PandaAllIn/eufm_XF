from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import yaml
import pathlib
from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.monitor.monitor import (
    get_wbs_data,
    calculate_compliance_score,
)

# The project root is 3 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]

def load_settings():
    """Loads settings from the YAML file."""
    settings_path = (
        PROJECT_ROOT
        / "src"
        / "eufm_assistant"
        / "ai_assistant"
        / "config"
        / "settings.yaml"
    )
    try:
        with open(settings_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Settings file not found at {settings_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing settings YAML file: {e}")
        return None

app = Flask(__name__, template_folder="templates", static_folder="static")
UPLOAD_FOLDER = "src/eufm_assistant/dashboard/storage"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    wbs_data = get_wbs_data()
    compliance_score = calculate_compliance_score(wbs_data)
    return render_template(
        "index.html", wbs_data=wbs_data, compliance_score=compliance_score
    )


@app.route("/research", methods=["GET", "POST"])
def research():
    if request.method == "POST":
        query = request.form["query"]
        settings = load_settings()
        if not settings:
            return render_template(
                "research.html", message="Error: Could not load application settings."
            )

        research_agent = ResearchAgent(settings)
        # Since the research agent is mocked, this will return mock data.
        # In a real scenario, this would perform a search.
        partner_data = research_agent.run(query)

        if partner_data:
            document_agent = DocumentAgent(settings)
            # This will make a real call to OpenAI if the API key is valid.
            emails = document_agent.draft_outreach_emails(partner_data)
            results = [
                {"partner": p, "email": e} for p, e in zip(partner_data, emails)
            ]
            return render_template("research.html", results=results)
        else:
            return render_template(
                "research.html", message="No partners found for the given query."
            )
    return render_template("research.html")


@app.route("/strategy")
def strategy():
    try:
        with open("src/eufm_assistant/docs/Horizon_Xilella.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "Strategy document not found."
    return render_template("strategy.html", strategy_content=content)


@app.route("/documents", methods=["GET", "POST"])
def documents():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("documents"))

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    docs = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("documents.html", documents=docs)


@app.route("/api/timeline")
def api_timeline():
    """
    API endpoint to provide timeline data to the frontend.
    Currently returns a static empty list as a placeholder.
    """
    # In a real application, you would fetch this data from a database
    # or by parsing the WBS files.
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, port=8080)
