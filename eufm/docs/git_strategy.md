# Git Tagging Strategy for Project Milestones

This document outlines the Git tagging strategy for archiving major project milestones.

## Tag Format

The tag format is designed to be descriptive and easily parseable. The format is as follows:

`v<major>.<minor>-<description>`

-   `<major>`: Major version number. Incremented for significant changes, new features, or breaking changes.
-   `<minor>`: Minor version number. Incremented for smaller changes, bug fixes, or patches.
-   `<description>`: A short, descriptive name for the milestone (e.g., `refactor-complete`, `stage1-submitted`). Use hyphens to separate words.

### Examples

-   `v1.0-refactor-complete`
-   `v1.1-stage1-submitted`
-   `v2.0-new-feature-launch`

## Creating Tags

Tags should be created using an annotated tag, which includes the author, date, and a message. This is done using the `git tag -a` command.

Example:

`git tag -a v1.0-initial-release -m "Initial release of the project"`

A helper script, `tag_milestone.sh`, is provided in the `scripts/` directory to simplify this process.
