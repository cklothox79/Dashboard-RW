# Streamlit App: Data Kependudukan RT/RW (Dark UI Modern)
# File: app.py

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Data Kependudukan Klotok", layout="wide", page_icon="📱")

# ------------------ DARK MODE CSS ------------------
dark_css = """
<style>
body { background-color: #0d1117; color: #e6edf3; }
.sidebar .sidebar-content { background-color: #161b22; }
header, .st-bw, .st-bx { background: #0d1117; }
.stButton>button { background-color:#238636; color:white; border-radius:8px; }
.stTextInput>div>div>input { background:#161b22; color:white; }
.stSelectbox>div>div>div { background:#161b22; color:white; }
.stDataFrame { background:#0d1117; }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
def load_data():
    try:
        return pd.read_csv("data_penduduk.csv")
    except:
        return pd.DataFrame(columns=["NIK", "Nama", "NoKK", "Alamat", "RT", "RW", "Jenis Kelamin", "Tanggal Lahir"])

data = load_data()

# ------------------ SAVE DATA ------------------
def save_data(df):
    df.to_csv("data_penduduk.csv", index=False)

# ------------------ UI ------------------
st.title("📱 Data Kependudukan — Dusun Klotok")
st.subheader("Aplikasi pendataan modern dengan tampilan gelap")

menu = st.sidebar.radio("Menu", ["Tambah Data", "Lihat Data", "Edit Data", "Statistik"])

# ------------------ TAMBAH DATA ------------------
if menu == "Tambah Data":
    st.header("➕ Tambah Data Penduduk")
    col1, col2 = st.columns(2)

    with col1:
        nik = st.text_input("NIK")
        nama = st.text_input("Nama Lengkap")
        nokk = st.text_input("Nomor KK")
        jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    with col2:
        alamat = st.text_input("Alamat")
        rt = st.text_input("RT")
        rw = st.text_input("RW")
        tl = st.date_input("Tanggal Lahir")

    if st.button("Simpan Data"):
        new_row = pd.DataFrame({
            "NIK": [nik], "Nama": [nama], "NoKK": [nokk], "Alamat": [alamat],
            "RT": [rt], "RW": [rw], "Jenis Kelamin": [jk], "Tanggal Lahir": [tl]
        })
        data = pd.concat([data, new_row], ignore_index=True)
        save_data(data)
        st.success("Data berhasil disimpan!")

# ------------------ LIHAT DATA ------------------
elif menu == "Lihat Data":
    st.header("📄 Lihat Data Penduduk")
    st.dataframe(data, use_container_width=True)

# ------------------ EDIT DATA ------------------
elif menu == "Edit Data":
    st.header("✏️ Edit Data Penduduk")
    pilih = st.selectbox("Pilih NIK", data["NIK"].unique())
    row = data[data["NIK"] == pilih].iloc[0]

    nama = st.text_input("Nama", row["Nama"])
    alamat = st.text_input("Alamat", row["Alamat"])
    rt = st.text_input("RT", row["RT"])
    rw = st.text_input("RW", row["RW"])

    if st.button("Simpan Perubahan"):
        data.loc[data["NIK"] == pilih, ["Nama", "Alamat", "RT", "RW"]] = [nama, alamat, rt, rw]
        save_data(data)
        st.success("Perubahan berhasil disimpan.")

# ------------------ STATISTIK ------------------
elif menu == "Statistik":
    st.header("📊 Statistik Kependudukan")
    total = len(data)
    lk = len(data[data["Jenis Kelamin"] == "Laki-laki"])
    pr = len(data[data["Jenis Kelamin"] == "Perempuan"])

    st.metric("Total Penduduk", total)
    st.metric("Laki-laki", lk)
    st.metric("Perempuan", pr)

    st.subheader("Jumlah Keluarga (berdasarkan No KK)")
    jml_kk = data["NoKK"].nunique()
    st.metric("Total KK", jml_kk)
