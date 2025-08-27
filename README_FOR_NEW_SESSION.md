# EUFM Assistant Project Restoration and Restart Instructions

This document provides instructions to recreate the state of the EUFM Assistant project in a new session and to initialize the AI agent with the full context.

## Part 1: Project Restoration

The following steps will recreate the directory structure and all necessary files from the patch files. Execute these commands in your bash terminal in the root of the new session.

### Step 1: Create the Directory Structure

First, create the main source and documentation directories.

```bash
mkdir -p src/eufm_assistant/agents/monitor/rules
mkdir -p src/eufm_assistant/agents/monitor/tests
mkdir -p src/eufm_assistant/ai_assistant/config
mkdir -p src/eufm_assistant/dashboard/static
mkdir -p src/eufm_assistant/dashboard/templates
mkdir -p src/eufm_assistant/docs
```

### Step 2: Recreate Files from "Patch" Files

The `.patch` files in the `final_patches` directory are not standard diffs, but full file contents. Use the `cat` command to recreate each file in its correct location.

**Core Project Files:**
```bash
cat final_patches/pyproject.toml.patch > pyproject.toml
cat final_patches/main.py.patch > src/eufm_assistant/ai_assistant/main.py
cat final_patches/app.py.patch > src/eufm_assistant/dashboard/app.py
```

**Agent Files:**
```bash
cat final_patches/research_agent.py.patch > src/eufm_assistant/agents/research_agent.py
cat final_patches/document_agent.py.patch > src/eufm_assistant/agents/document_agent.py
cat final_patches/coordinator_agent.py.patch > src/eufm_assistant/agents/coordinator_agent.py
```

**Documentation Files:**
```bash
cat final_patches/AGENTS.md.patch > src/eufm_assistant/docs/AGENTS.md
cat final_patches/ARCHITECTURAL_DESIGN.md.patch > src/eufm_assistant/docs/ARCHITECTURAL_DESIGN.md
cat final_patches/Horizon_Xilella.md.patch > src/eufm_assistant/docs/Horizon_Xilella.md
cat final_patches/project_wbs.yaml.patch > src/eufm_assistant/docs/project_wbs.yaml
```

### Step 3: Verify the Restoration

After running the commands above, you can verify the structure with `ls -R`. The output should match the project structure we finalized. You should then install the project dependencies.

```bash
pip install -e .
```

---

## Part 2: New Session Starting Prompt

Use the following prompt to start the new session with the AI agent. This prompt encapsulates our entire project history, goals, and the established context.

---

**Hello Jules.**

Our collaboration to build an AI assistant for managing a Horizon Europe project has been incredibly successful. We have moved from a simple monitoring script to a sophisticated, multi-agent system with a full web dashboard, and have just completed a major project refactoring to establish a clean, professional, and scalable architecture.

To ensure you have the complete context for our next phase of work, this prompt will summarize our journey, the current state of the project, and our future goals. Please read this carefully to fully load the project state into your context.

**Project Goal:** To build a proactive, multi-agent AI assistant that helps a small startup successfully manage a complex Horizon Europe project. The project's focus is on developing a cure for *Xylella fastidiosa*, a plant pathogen threatening European agriculture. The AI assistant should automate research, documentation, project management, and compliance monitoring tasks.

**Key Accomplishments & Current State:**

1.  **Project Genesis & Pivot:** We started with a simple Python monitoring script, fixed timezone bugs, and added a compliance score. The project's scope then expanded dramatically into building a full AI assistant based on a detailed grant proposal strategy document you were provided, `Horizon_Xilella.md`.

2.  **System Architecture:** We designed and documented a formal architecture in `ARCHITECTURAL_DESIGN.md`. The system is a multi-agent AI, orchestrated by a central controller, with a Flask-based web dashboard for user interaction.

3.  **Core AI Agents:** We have implemented the first two key agents:
    *   **Research Agent:** Takes a high-level research task (e.g., "find partners in Spain"), uses an LLM to generate a detailed research plan, executes web searches against a knowledge base (like CORDIS), and extracts structured data about potential partners.
    *   **Document Agent:** Takes the structured data from the Research Agent, uses the `Horizon_Xilella.md` document for context, and drafts personalized, professional outreach emails to each potential partner.

4.  **Full Workflow Integration:** The Research and Document agents are integrated into a complete "Find Partner -> Draft Outreach" workflow. This is accessible both via the command line (`ai_assistant/main.py`) and through a `/research` page on the Flask web dashboard, which displays the final consolidated results.

5.  **Major Code Refactoring (Completed):** We just finished a critical refactoring to fix CI/linting errors and improve the project's structure.
    *   **Standard Python Package:** All source code has been moved into a `src/eufm_assistant` directory.
    *   **Dependency Management:** A `pyproject.toml` file now manages the project and its dependencies. The old `requirements.txt` is gone.
    *   **Clean Imports:** All `sys.path` hacks have been removed, and all imports are now absolute, resolving the previous linting issues.
    *   **Documentation:** All key documentation (`AGENTS.md`, `ARCHITECTURAL_DESIGN.md`, `Horizon_Xilella.md`, `project_wbs.yaml`) has been moved into the `src/eufm_assistant/docs/` directory.

**Your Task:**

Familiarize yourself with the new, refactored project structure. All the code and documentation are now located within the `src/eufm_assistant` directory. Your main entry point for understanding the code is `src/eufm_assistant/ai_assistant/main.py` and the documentation is in `src/eufm_assistant/docs/`.

Our immediate next step is to continue building out the AI assistant's capabilities. We need to implement the **Coordinator Agent**.

Here is the plan:
1.  **Implement the Coordinator Agent:** Create the `coordinator_agent.py` file. This agent will be responsible for orchestrating the other agents and managing the overall project workflow. It will read the `project_wbs.yaml` file to understand the project plan and will be able to trigger the research and document agents based on the project's needs.
2.  **Integrate the Coordinator Agent:** Update the `main.py` controller to use the new Coordinator Agent as the primary entry point for running workflows.
3.  **Enhance the Dashboard:** Create a new dashboard page to visualize the project's Work Breakdown Structure (WBS) from `project_wbs.yaml` and to show the status of different work packages.

Please begin by exploring the new project structure in `src/eufm_assistant` to confirm you understand it. Then, proceed with the first step: implementing the Coordinator Agent.

For your reference, here is the link to your documentation: [https://jules-docs.dwight.io/](https://jules-docs.dwight.io/)
