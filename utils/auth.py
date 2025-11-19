# utils/auth.py
import yaml
from pathlib import Path
import streamlit as st
from typing import Optional, Tuple

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "passwords.yaml"

def load_passwords() -> dict:
    """
    Load passwords.yaml.
    Accepts two styles:
      1) simple: { "rt1": "rt1pass", "rw": "rwpass", "admin": "adminpass" }
      2) multi-user: { "users": { "riaji": {"role":"rt1","password":"pw1"}, ... } }
    Returns a normalized dict:
      {
        "users": {
           username: {"role": role, "password": pw}
        },
        "roles": { role: [password1, password2, ...] }  # legacy compatibility
      }
    """
    data = {}
    if not CONFIG_PATH.exists():
        return {"users": {}, "roles": {}}

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data_raw = yaml.safe_load(f) or {}

    users = {}
    roles = {}

    # If file is simple mapping of role -> password string
    simple_roles = {k: v for k, v in (data_raw.items()) if isinstance(v, str)}
    for role, pw in simple_roles.items():
        # Make a synthetic username for backwards compatibility
        synthetic_user = f"{role}_user"
        users[synthetic_user] = {"role": role, "password": str(pw)}
        roles.setdefault(role, []).append(str(pw))

    # If file contains 'users' block with explicit usernames
    if "users" in data_raw and isinstance(data_raw["users"], dict):
        for uname, info in data_raw["users"].items():
            role = info.get("role")
            pw = info.get("password")
            if role and pw is not None:
                users[uname] = {"role": role, "password": str(pw)}
                roles.setdefault(role, []).append(str(pw))

    return {"users": users, "roles": roles}

_PASSWORD_STORE = load_passwords()

def check_credentials(username: str, password: str) -> Optional[str]:
    """
    Returns role if credentials valid, else None.
    Checks:
      - explicit users in passwords.yaml
      - synthetic users created from simple role->pw mapping
    """
    for uname, info in _PASSWORD_STORE.get("users", {}).items():
        if uname == username and info.get("password") == password:
            return info.get("role")
    # fallback: allow login by password only (legacy behavior)
    for role, pws in _PASSWORD_STORE.get("roles", {}).items():
        if password in pws:
            # return role (first match)
            return role
    return None

def login_widget():
    """
    Streamlit-side login widget for username+password.
    Stores 'user' and 'role' in st.session_state on success.
    """
    st.sidebar.subheader("🔐 Login RT / RW / Admin")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        role = check_credentials(username.strip(), password.strip())
        if role:
            st.session_state["user"] = username.strip()
            st.session_state["role"] = role
            st.sidebar.success(f"Login berhasil: {username} ({role})")
            return True
        else:
            st.sidebar.error("Login gagal — username/password salah.")
            return False
    return False

def logout():
    """Clear session keys for login."""
    for k in ("user", "role"):
        if k in st.session_state:
            del st.session_state[k]

def current_user() -> Tuple[Optional[str], Optional[str]]:
    """Return (username, role) from session state."""
    return (st.session_state.get("user"), st.session_state.get("role"))
