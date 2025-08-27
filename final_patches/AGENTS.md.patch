# Contributor Guide for Agents

This document describes the agents and automated tools in this repository.

---

## Monitor A (Legacy)

This agent provides a simple status report based on the WBS.

**Primary folder:** `/agents/monitor/`

**How to validate:**
- Run `python -m pytest agents/monitor/tests -q` (tests must pass).
- Run `ruff check . && ruff format --check .` for lint/format.
- `python agents/monitor/monitor.py --dry-run`

---

# AI Project Assistant Agents

This section documents the new, more advanced AI agents being built.

## 1. Research Agent

**File Location:** `ai_assistant/agents/research_agent.py`

### Purpose

The Research Agent is responsible for conducting online research to gather intelligence and find information relevant to the project. Its primary initial task is to identify potential collaborators for the Horizon Europe proposal.

### How to Use

The agent is run via the main controller script: `ai_assistant/main.py`.

**Command:**
```bash
python ai_assistant/main.py "Your high-level research task here"
```

**Example Task:**
`python ai_assistant/main.py "Find research institutions in Italy that have published papers on Xylella fastidiosa vectors."`

### Input

The agent takes a single string as input: `research_task`. This should be a high-level description of the research goal.

### Output

The agent returns a structured JSON list of potential collaborators. Each item in the list is an object with the following fields:
- `name` (str): The name of the person or institution.
- `role` (str): Their role or title.
- `affiliation` (str): Their affiliated university or company.
- `email` (str|null): Their contact email, if found.
- `summary_of_relevance` (str): A brief summary of why they are relevant to the input task.

**Example Output:**
```json
[
  {
    "name": "Dr. Maria Rossi",
    "role": "Lead Entomologist",
    "affiliation": "University of Bologna, Department of Agricultural Sciences",
    "email": "maria.rossi@unibo.it",
    "summary_of_relevance": "Co-authored a 2023 paper on the lifecycle of Philaenus spumarius, the primary vector for Xylella in Europe."
  }
]
```
