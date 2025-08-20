import sys
from types import SimpleNamespace
from unittest.mock import Mock
import pathlib

# Ensure the scripts directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import seed_backlog


def sample_item():
    return {"id": "WPX-T1", "title": "Title", "acceptance": []}


def test_dry_run_returns_actions_without_api_calls():
    item = sample_item()
    gh = Mock()
    repo = Mock()
    # No existing issue -> create(dry)
    gh.search_issues_and_pull_requests.return_value = []
    result = seed_backlog.create_or_update_issue(
        gh=gh,
        repo=repo,
        repo_full="org/repo",
        wp="WPX",
        item=item,
        assignee_username=None,
        dry_run=True,
    )
    assert result == {
        "action": "create(dry)",
        "title": seed_backlog.ISSUE_TITLE_FMT.format(
            wp="WPX", id=item["id"], title=item["title"]
        ),
    }
    assert repo.method_calls == []

    # Existing issue -> update(dry)
    existing = SimpleNamespace(number=5)
    gh.search_issues_and_pull_requests.return_value = [existing]
    repo = Mock()
    result = seed_backlog.create_or_update_issue(
        gh=gh,
        repo=repo,
        repo_full="org/repo",
        wp="WPX",
        item=item,
        assignee_username=None,
        dry_run=True,
    )
    assert result == {
        "action": "update(dry)",
        "number": 5,
        "title": seed_backlog.ISSUE_TITLE_FMT.format(
            wp="WPX", id=item["id"], title=item["title"]
        ),
    }
    assert repo.method_calls == []


def test_apply_mode_creates_issue_and_label():
    item = sample_item()
    gh = Mock()
    gh.search_issues_and_pull_requests.return_value = []
    repo = Mock()
    issue = Mock(number=101)
    repo.create_issue.return_value = issue
    repo.get_label.side_effect = Exception
    result = seed_backlog.create_or_update_issue(
        gh=gh,
        repo=repo,
        repo_full="org/repo",
        wp="WPX",
        item=item,
        assignee_username=None,
        dry_run=False,
    )
    assert result == {
        "action": "create",
        "number": 101,
        "title": seed_backlog.ISSUE_TITLE_FMT.format(
            wp="WPX", id=item["id"], title=item["title"]
        ),
    }
    repo.create_issue.assert_called_once()
    repo.create_label.assert_called_once_with(
        name="WPX", color=seed_backlog.LABEL_COLOR, description="Work Package WPX"
    )
    issue.add_to_labels.assert_called_once_with("WPX")


def test_apply_mode_updates_issue_and_label():
    item = sample_item()
    existing = SimpleNamespace(number=55)
    gh = Mock()
    gh.search_issues_and_pull_requests.return_value = [existing]
    repo = Mock()
    issue = Mock(number=55)
    repo.get_issue.return_value = issue
    repo.get_label.side_effect = Exception
    result = seed_backlog.create_or_update_issue(
        gh=gh,
        repo=repo,
        repo_full="org/repo",
        wp="WPX",
        item=item,
        assignee_username="user",
        dry_run=False,
    )
    expected_title = seed_backlog.ISSUE_TITLE_FMT.format(
        wp="WPX", id=item["id"], title=item["title"]
    )
    assert result == {"action": "update", "number": 55, "title": expected_title}
    repo.get_issue.assert_called_once_with(number=55)
    issue.edit.assert_called_once_with(
        title=expected_title, body=seed_backlog.build_body(item)
    )
    issue.add_to_assignees.assert_called_once_with("user")
    repo.create_label.assert_called_once_with(
        name="WPX", color=seed_backlog.LABEL_COLOR, description="Work Package WPX"
    )
    issue.add_to_labels.assert_called_once_with("WPX")
