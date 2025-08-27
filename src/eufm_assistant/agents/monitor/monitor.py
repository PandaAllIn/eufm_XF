import yaml
from datetime import datetime, timezone

WBS_FILE_PATH = 'src/eufm_assistant/docs/project_wbs.yaml'

def get_wbs_data():
    """
    Loads the Work Breakdown Structure data from the YAML file.
    The path is relative to the project root.
    """
    try:
        with open(WBS_FILE_PATH, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: WBS file not found at {WBS_FILE_PATH}")
        return None

def calculate_compliance_score(wbs_data):
    """
    Calculates a compliance score based on the WBS data.
    A simple scoring mechanism:
    - 1 point for each work package.
    - 1 extra point if a work package has a 'leader' defined.
    - 1 extra point if a work package has tasks.
    - Compares dates to check for overdue tasks.
    """
    if not wbs_data or 'work_packages' not in wbs_data:
        return 0

    total_possible_score = 0
    current_score = 0
    now = datetime.now(timezone.utc)

    for wp in wbs_data['work_packages']:
        total_possible_score += 3 # Base score for existence, leader, and tasks
        current_score += 1

        if wp.get('leader'):
            current_score += 1

        if 'tasks' in wp:
            current_score += 1

        # Date checks for tasks (assuming tasks have start/end dates)
        if 'tasks' in wp:
            for task in wp['tasks']:
                total_possible_score += 1
                if 'end_date' in task and task['end_date']:
                    end_date = datetime.fromisoformat(task['end_date'])
                    if end_date < now and task.get('status') != 'Completed':
                        # Penalty for overdue tasks, no points awarded
                        pass
                    else:
                        current_score +=1
                else:
                    # No end date, still give the point
                    current_score += 1


    if total_possible_score == 0:
        return 100 # Or 0, depending on desired behavior for empty WBS

    compliance_percentage = (current_score / total_possible_score) * 100
    return int(compliance_percentage)
