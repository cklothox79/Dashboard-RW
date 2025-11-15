import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "passwords.yaml"

def load_passwords():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("passwords", {})

def check_password(entered_password: str):
    """
    Return role key if password matches one of entries, else None.
    Roles: rt1, rt2, rt3, rw, admin
    """
    pw = load_passwords()
    for role, p in pw.items():
        if entered_password == p:
            return role
    return None
