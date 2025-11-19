import streamlit as st
import yaml
import hashlib

def load_passwords():
    with open("config/passwords.yaml", "r") as f:
        return yaml.safe_load(f)["passwords"]

PASSWORDS = load_passwords()

def hash_pass(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(role, password_input):
    if role not in PASSWORDS:
        return False
    return PASSWORDS[role] == password_input

def login_ui():
    st.title("🔐 Login Akses RT / RW / Admin")

    role = st.selectbox("Pilih Akses", ["rt1", "rt2", "rt3", "rw", "admin"])
    pwd = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if check_login(role, pwd):
            st.session_state["logged_in"] = True
            st.session_state["role"] = role
            st.success(f"Berhasil login sebagai **{role.upper()}**")
            st.rerun()
        else:
            st.error("Password salah!")

def logout():
    st.session_state["logged_in"] = False
    st.session_state["role"] = None
    st.rerun()

def require_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login untuk melanjutkan")
        login_ui()
        st.stop()

def role_is(role):
    return st.session_state.get("role") == role
