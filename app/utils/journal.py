import datetime
import re
import os

# Construct the absolute path to the project root
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
JOURNAL_FILE = os.path.join(_PROJECT_ROOT, "PROJECT_JOURNAL.md")

def _read_journal():
    """Reads the content of the journal file."""
    try:
        with open(JOURNAL_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        # If the journal doesn't exist, we can start with a template.
        # For this implementation, we'll assume it's created and raise an error.
        raise FileNotFoundError(f"Journal file not found at {JOURNAL_FILE}")

def _write_journal(content):
    """Writes content to the journal file."""
    with open(JOURNAL_FILE, "w") as f:
        f.write(content)

def log_decision(message: str):
    """Logs a new decision in the project journal."""
    content = _read_journal()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    decision_log_line = f"- `{timestamp}`: {message}\n"

    # Use a more specific pattern to append after the header
    content, count = re.subn(
        r"(## Key Decisions Log\n)",
        r"\1" + decision_log_line,
        content
    )
    if count == 0:
        # If the header wasn't found, append it to the end of the file
        content += "\n## Key Decisions Log\n" + decision_log_line
    _write_journal(content)

def update_status(status: str):
    """Updates the project status in the journal."""
    content = _read_journal()
    new_status_line = f"* {status.lstrip('* ')}\n"

    # Replace the content under "Last Known Status"
    content, count = re.subn(
        r"(## Last Known Status\n)(?:-|\*).*",
        r"\1" + new_status_line,
        content,
        flags=re.IGNORECASE
    )
    if count == 0:
        content += "\n## Last Known Status\n" + new_status_line
    _write_journal(content)


def add_blocker(blocker: str):
    """Adds a new blocker or open question to the journal."""
    content = _read_journal()
    blocker_line = f"- {blocker}\n"

    # Append the blocker to the "Open Questions & Blockers" section
    content, count = re.subn(
        r"(## Open Questions & Blockers\n)",
        r"\1" + blocker_line,
        content
    )
    if count == 0:
        content += "\n## Open Questions & Blockers\n" + blocker_line
    _write_journal(content)
