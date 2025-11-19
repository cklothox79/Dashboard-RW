import yaml
import streamlit as st

# Load password config
def load_passwords(path="config/passwords.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["passwords"]

PASSWORDS = load_passwords()

# Role-based login
def authenticate():
    st.sidebar.subheader("🔐 Login Akses")

    role = st.sidebar.selectbox(
        "Pilih Role",
        ["RT 1", "RT 2", "RT 3", "RW", "Admin"]
    )

    password = st.sidebar.text_input("Masukkan Password", type="password")

    if st.sidebar.button("Login"):
        key = role.lower().replace(" ", "")
        if password == PASSWORDS.get(key):
            st.session_state["role"] = role
            st.success(f"Login berhasil sebagai **{role}**")
        else:
            st.error("Password salah!")

    return st.session_state.get("role", None)


# Authorization limit
def filter_by_role(df, role):
    if role == "Admin":
        return df
    if role == "RW":
        return df  # akses semua warga 1 RW
    if "RT" in role:
        num = role.split(" ")[1]
        return df[df["rt"] == int(num)]
    return df
