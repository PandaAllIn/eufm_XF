**Assigned To:** Jules AI
**Task ID:** JULES-20250831-002
**Title:** Implement the "Milestone Archive" System

**Objective:**
As an expert in DevOps and Git, your task is to create a system for creating a versioned, rewindable history of the project on GitHub.

**Component 1: Git Strategy Design**
1.  **Design:** Propose a Git tagging strategy for archiving major project milestones. The tag format should be `v<major>.<minor>-<description>` (e.g., `v1.0-refactor-complete`, `v1.1-stage1-submitted`).
2.  **Document:** Create a new Markdown file at `eufm/docs/git_strategy.md` that documents this strategy.

**Component 2: Implementation**
1.  **Implement:** Create a new shell script at `eufm/scripts/tag_milestone.sh`. This script should take a version number and a message as arguments, create an annotated Git tag, and push the tag to the remote repository.

**Context:**
The project is a Git repository. The script should be executable and well-documented.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch. The PR should include the new `git_strategy.md` file and the `tag_milestone.sh` script.
