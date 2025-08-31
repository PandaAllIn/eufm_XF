import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.utils.journal import log_decision, update_status

def main():
    """Updates the project journal with the latest status."""
    print("--- Updating Project Journal ---")
    
    update_status("Overnight AI Task Force initiative complete. All systems refactored and new capabilities integrated.")
    log_decision("Merged all successful branches from the overnight initiative into the main branch.")
    log_decision("Implemented the failed 'Milestone Archive' task.")
    log_decision("Integrated the new journal system into the CoordinatorAgent.")
    
    print("--- Project Journal Updated ---")

if __name__ == "__main__":
    main()
