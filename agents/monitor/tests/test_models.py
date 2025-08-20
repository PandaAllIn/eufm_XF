import pathlib

import pytest
import yaml
from pydantic import ValidationError

from agents.monitor.models import Milestones, WorkBreakdown

ROOT = pathlib.Path(__file__).resolve().parents[3]


def load_yaml(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_wbs_valid():
    data = load_yaml(ROOT / "wbs" / "wbs.yaml")
    model = WorkBreakdown.model_validate(data)
    assert model.wbs["WP1"][0].id == "WP1-D1.1"


def test_wbs_invalid():
    bad = {
        "wbs": {
            "WP1": [
                {
                    "title": "Missing id",
                    "type": "task",
                    "due": "2025-01-01",
                    "owner": "x",
                }
            ]
        }
    }
    with pytest.raises(ValidationError):
        WorkBreakdown.model_validate(bad)


def test_milestones_valid():
    data = load_yaml(ROOT / "wbs" / "milestones.yaml")
    model = Milestones.model_validate(data)
    assert model.milestones[0].id == "STAGE1"


def test_milestones_invalid():
    bad = {"milestones": [{"id": "M1", "title": "Missing date"}]}
    with pytest.raises(ValidationError):
        Milestones.model_validate(bad)
