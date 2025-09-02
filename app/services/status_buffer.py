from collections import deque
from typing import Deque, Dict, List

# Maximum number of status updates to retain in memory.
_MAX_SIZE = 1000

# Internal ring buffer storing status update dictionaries.
_status_buffer: Deque[Dict] = deque(maxlen=_MAX_SIZE)


def add_status_update(update: Dict) -> None:
    """Append a new status update to the ring buffer."""
    _status_buffer.append(update)


def get_status_updates(limit: int) -> List[Dict]:
    """Return the most recent ``limit`` status updates."""
    if limit <= 0:
        return []
    return list(_status_buffer)[-limit:]


def clear_status_updates() -> None:
    """Remove all entries from the ring buffer.

    This is primarily intended for test cleanup.
    """
    _status_buffer.clear()
