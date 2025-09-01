**Assigned To:** OpenAI Codex
**Task ID:** CODEX-DIRECTOR-20250901-FINAL
**Title:** Act as AI Tech Lead: Finalize System Refactoring and Initiate "Mission Control" UI Development

**Objective:**
You are the AI Tech Lead for the EUFM project. Your mission is to direct our AI development team to first complete the foundational backend refactoring and then begin development of our new "Mission Control" web interface.

**Your Foundational Documents:**
You must read and understand these documents before you begin:
1.  **The Blueprint (`docs/MISSION_CONTROL_BLUEPRINT.md`):** The master plan for the new UI.
2.  **The Raw Research (`docs/sonar_research_mission_control.md`):** The deep research that informed the blueprint.
3.  **The Project Journal (`PROJECT_JOURNAL.md`):** The log of our current status and decisions.

**Your Mission Roadmap (Execute in Order):**

**Phase 1: Clear the Existing Backlog**
Your first priority is to complete the core system refactoring tasks that have already been defined. You will find these tasks in the `eufm/tasks/` directory. Assign them to Codex one by one, in numerical order.

1.  **Task File:** `eufm/tasks/jules_task_autogen_01.md` - Implement the Database Models.
2.  **Task File:** `eufm/tasks/jules_task_autogen_02.md` - Implement the Asynchronous TaskQueue.
3.  **Task File:** `eufm/tasks/jules_task_autogen_03.md` - Implement the Agent Orchestrator Service.
4.  **Task File:** `eufm/tasks/jules_task_autogen_04.md` - Implement the API Endpoints for the Orchestrator.

**Phase 2: Operation "Mission Control"**
Once all tasks in Phase 1 are complete and their Pull Requests have been created, you will begin directing the implementation of the new UI, as defined in the `MISSION_CONTROL_BLUEPRINT.md`.

You will work through the "Implementation Roadmap" section of the blueprint, creating a detailed prompt for Codex for each task.

**Your Continuous Workflow:**
1.  **Select Task:** Choose the next task from the roadmap.
2.  **Read Spec:** Open and read the corresponding task file (for Phase 1) or the blueprint (for Phase 2).
3.  **Instruct Codex:** Formulate a detailed prompt and assign it to Codex via its web interface. Instruct it to submit its work as a Pull Request.
4.  **Log Action:** After assigning a task, open `PROJECT_JOURNAL.md` on GitHub and log the action.
5.  **Repeat.**

**Your first action is to connect to the `PandaAllIn/eufm` GitHub repository, navigate to the `eufm/tasks/` directory, and begin executing Phase 1 of the Mission Roadmap.**
