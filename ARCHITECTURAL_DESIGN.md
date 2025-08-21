# AI Project Assistant - Architectural Design Document

This document outlines the vision, architecture, and development roadmap for the AI Project Assistant, a system designed to manage and accelerate the 'Horizon Europe: Xylella Fastidiosa Solution' project.

## 1. High-Level Vision & Goals

### 1.1 Vision

To create a proactive, intelligent, and autonomous AI assistant that acts as a core team member for the Xylella Fastidiosa project. The assistant will manage complex information, automate key tasks, provide strategic insights, and accelerate the entire project lifecycle, from proposal submission to commercialization, ensuring a "win-win-win" outcome for the project, its partners, and European agriculture.

### 1.2 Core Goals

*   **Goal 1: Accelerate Proposal Preparation:** Dramatically reduce the time and effort required to prepare a winning Stage 1 and Stage 2 Horizon Europe proposal.
    *   *Initial Task:* Identify and vet potential consortium partners.
    *   *Initial Task:* Draft outreach emails and communication materials.
*   **Goal 2: Streamline Project Management:** Once funded, manage the project's timeline, tasks, deliverables, and reporting in accordance with EU best practices.
*   **Goal 3: Provide Strategic Intelligence:** Continuously monitor the research landscape, identify new opportunities and risks, and provide data-driven suggestions to the project team.
*   **Goal 4: Facilitate Collaboration and Communication:** Act as a central knowledge hub for the consortium and assist in drafting reports, presentations, and dissemination materials.

## 2. System Architecture

The system will be designed as a **Multi-Agent System**, where different specialized AI agents collaborate to achieve the overall goals. This architecture is modular, scalable, and allows for clear separation of concerns.

### 2.1 Core Components

1.  **Main Controller (`main.py`):** The central orchestrator. It receives high-level tasks from the user (via the command line or a future UI), selects the appropriate agent for the job, and manages the overall workflow.

2.  **Shared Context / Memory:** A mechanism for agents to share information. Initially, this will be simple file-based context (e.g., reading the `Horizon_Xilella.md` and `project_wbs.yaml` files). In the future, this could evolve into a more sophisticated vector database or knowledge graph.

3.  **Agent Toolkit:** A collection of tools that agents can use to interact with the outside world. This includes:
    *   `google_search`
    *   `view_text_website`
    *   File I/O (read/write)
    *   (Future) Email sending, Calendar integration, etc.

4.  **Agent Abstraction:** A base `Agent` class that all specialized agents will inherit from. It will define the common interface (e.g., a `run` method).

5.  **Specialized Agents:** A suite of agents, each with a specific "persona" and set of skills defined by its system prompt and internal logic.

### 2.2 Proposed Agents

*   **Research Agent (Phase 2):** Our first agent.
    *   **Persona:** A diligent research analyst.
    *   **Skills:** Online search, information extraction, data structuring.
    *   **Tasks:** Finding potential partners, literature reviews, market analysis.

*   **Document Agent (Phase 3):**
    *   **Persona:** A professional scientific and business writer.
    *   **Skills:** Reading documents, summarizing text, drafting new content (emails, proposal sections, reports).
    *   **Tasks:** Drafting outreach emails, preparing sections of the proposal, summarizing research papers.

*   **Timeline Agent (Phase 4):**
    *   **Persona:** An expert project manager (PMP certified).
    *   **Skills:** Gantt chart creation, dependency analysis, critical path identification.
    *   **Tasks:** Creating and managing the project schedule, sending deadline reminders, tracking milestones.

*   **Coordinator Agent (Future):** The master agent that can decompose complex goals and delegate tasks to the other specialized agents.

### 2.3 Technology Stack

*   **Backend:** Python
*   **LLM Interaction:** OpenAI Python Library
*   **Web Dashboard / UI:** Flask
*   **Configuration:** YAML
*   **Data Storage:** Initially file-based (Markdown, YAML, JSON). Potentially a vector database (e.g., ChromaDB, Pinecone) in the future for more advanced memory.

## 3. Development Roadmap (Phased Approach)

This section will be filled out in more detail as we complete each phase.

*   **Phase 1: Core System Setup (Complete):**
    *   [x] Directory Structure
    *   [x] Configuration File (`settings.yaml`)
    *   [x] Main Controller Entry Point (`main.py`)
    *   [x] Initial Project Documents (`Horizon_Xilella.md`, `project_wbs.yaml`)

*   **Phase 2: Research Agent Implementation (In Progress):**
    *   [x] Agent Scaffolding (`research_agent.py`)
    *   [x] Tool Integration (Mocked)
    *   [x] LLM-Powered Query Generation
    *   [x] LLM-Powered Information Extraction
    *   [x] Core Agent Logic
    *   [ ] **Next Step:** Connect Agent to a real data source (the user's API key) and tools.

*   **Phase 3: Document Agent Implementation:**
    *   [ ] Agent Scaffolding (`document_agent.py`)
    *   [ ] Implement file reading/writing tools.
    *   [ ] Implement LLM-powered drafting capabilities.
    *   [ ] Integrate with Research Agent (e.g., draft an email to a found collaborator).

*   **Phase 4: Dashboard & UI Integration:**
    *   [x] Initial Dashboard for WBS monitoring.
    *   [x] Interface for running the Research Agent.
    *   [ ] Create a unified interface for interacting with all agents.
    *   [ ] Visualize the outputs (timelines, lists of partners, drafted documents).

---
*This is a living document and will be updated as the project progresses.*
