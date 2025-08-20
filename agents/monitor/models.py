from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    title: str
    type: str
    due: date
    owner: str
    depends: List[str] = Field(default_factory=list)
    acceptance: Optional[List[str]] = None


class WorkBreakdown(BaseModel):
    wbs: Dict[str, List[Task]]


class Milestone(BaseModel):
    id: str
    title: str
    date: date
    gate_rules: List[str]


class Milestones(BaseModel):
    milestones: List[Milestone]
