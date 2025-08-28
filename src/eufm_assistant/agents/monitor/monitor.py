import yaml
from datetime import datetime, timezone

WBS_FILE_PATH = "src/eufm_assistant/docs/project_wbs.yaml"


def get_wbs_data():
    try:
        with open(WBS_FILE_PATH, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return None


def calculate_compliance_score(wbs_data):
    if not wbs_data or "work_packages" not in wbs_data:
        return 0
    total_possible_score, current_score = 0, 0
    now = datetime.now(timezone.utc)
    for wp in wbs_data["work_packages"]:
        total_possible_score += 3
        current_score += 1
feature/interactive-timeline
        if wp.get("leader"):
            current_score += 1
        if "tasks" in wp:
            current_score += 1
        if "tasks" in wp:
            for task in wp["tasks"]:
                total_possible_score += 1
                if "end_date" in task and task["end_date"]:
                    if (
                        datetime.fromisoformat(task["end_date"]) >= now
                        or task.get("status") == "Completed"
                    ):
=======
        if wp.get('leader'):
            current_score += 1
        if 'tasks' in wp:
            current_score += 1
        if 'tasks' in wp:
            for task in wp['tasks']:
                total_possible_score += 1
                if 'end_date' in task and task['end_date']:
                    if datetime.fromisoformat(task['end_date']) >= now or task.get('status') == 'Completed':
main
                        current_score += 1
                else:
                    current_score += 1
    if total_possible_score == 0:
        return 100
    return int((current_score / total_possible_score) * 100)
