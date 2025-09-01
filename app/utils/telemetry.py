import json
import logging
import os
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

try:
    import fcntl  # type: ignore
except ImportError:  # pragma: no cover
    fcntl = None  # type: ignore


class TelemetryLogger:
    """Append-only JSONL telemetry logger with daily file rotation."""

    def __init__(self, log_dir: Optional[Path] = None, enabled: Optional[bool] = None):
        root_dir = Path(__file__).resolve().parent.parent.parent
        self.log_dir = log_dir or (root_dir / ".logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        if enabled is None:
            enabled = os.getenv("TELEMETRY_ENABLED", "").lower() == "true"
        self.enabled = enabled
        self._thread_lock = Lock()
        self._logger = logging.getLogger(self.__class__.__name__)

    def _current_log_path(self) -> Path:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        return self.log_dir / f"{date_str}.jsonl"

    def _write_entry(self, path: Path, entry: Dict[str, Any]) -> None:
        line = json.dumps(entry, ensure_ascii=False) + "\n"
        try:
            with self._thread_lock:
                with open(path, "a", encoding="utf-8") as f:
                    if fcntl:
                        fcntl.flock(f, fcntl.LOCK_EX)
                    f.write(line)
                    f.flush()
                    if fcntl:
                        fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as exc:  # pragma: no cover - log error
            self._logger.error("Telemetry write failed: %s", exc)

    def log(self, **data: Any) -> None:
        """Write a telemetry event if enabled."""
        if not self.enabled:
            return
        entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
        }
        entry.update(data)
        path = self._current_log_path()
        self._write_entry(path, entry)


telemetry_logger = TelemetryLogger()
