# utils/logger.py
from pathlib import Path
from datetime import datetime
import json
import os

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "log" / "activity.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def write_log(username: str, role: str, action: str, target: str = "", extra: dict = None):
    """
    Append a JSON line to the activity.log
    Fields:
      timestamp, username, role, action, target, extra
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "username": username or "",
        "role": role or "",
        "action": action,
        "target": target or "",
        "extra": extra or {}
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + os.linesep)
