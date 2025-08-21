import sys
import pathlib
from flask import Flask, render_template

# Add the project root to the Python path
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from agents.monitor.core import (
    calculate_compliance_score,
    gar_for_due,
    load_yaml,
)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
