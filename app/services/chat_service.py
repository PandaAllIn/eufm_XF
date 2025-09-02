from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Dict, List


class ChatService:
    """Persist and retrieve chat messages."""

    def __init__(self, path: Path, max_messages: int = 200) -> None:
        self.path = path
        self.max_messages = max_messages
        self._messages: List[Dict[str, str]] = []
        self._lock = Lock()
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    try:
                        self._messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            self._messages = self._messages[-self.max_messages :]

    def append(self, message: Dict[str, str]) -> None:
        with self._lock:
            self._messages.append(message)
            self._messages = self._messages[-self.max_messages :]
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(message) + "\n")

    def latest(self, limit: int) -> List[Dict[str, str]]:
        with self._lock:
            if limit <= 0:
                return []
            return self._messages[-limit:]
