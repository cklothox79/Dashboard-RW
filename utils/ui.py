# utils/ui.py
import streamlit as st
import plotly.express as px
from typing import Dict
from utils.merge import group_by_kk, get_family_members
from utils.stats import (
    age_distribution,
    gender_counts,
    summary_by_rt,
    top_categories,
    add_age_column,
)
from utils.logger import write_log
from utils.auth import current_user

# ---------- CSS (dark theme + cards) ----------
def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --bg: #0f1724;
            --card: #0b1220;
            --muted: #9aa4a6;
            --accent: #1f8ef1;
            --glass: rgba(255,255,255,0.03);
        }
        .main > .block-container{
            padding: 1.25rem 1.5rem;
            background: linear-gradient(180deg, var(--bg), #07101a);
            color: #e6eef3;
        }
        .card {
            background: var(--card);
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.03);
        }
        .metric-title { color: #cfe9ff; font-weight:600; }
        .small-muted { color: var(--muted); font-size:13px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def top_metrics(df):
    add_age_column(df, dob_col="tanggal_lahir", out_col="age")
    total = len(df)
    kk = int(df["no_kk"].nunique()) if "no_kk" in df.columns else 0
    gender = gender_counts(df)
    ages = df["age"].dropna().astype(int) if "age" in df.columns else []
    cols = st.columns(4)
    cols[0].metric("Total Penduduk", total)
    cols[1].metric("Jumlah KK", kk)
    cols[2].metric("Laki-laki", gender.get("L",0))
    cols[3].metric("Perempuan", gender.get("P",0))

def show_dashboard(df, info):
    inject_css()
    st.title("🏡 Dashboard Kependudukan — RW 02 Dusun Klotok")
    st.caption(f"{info.get('desa','')} — {info.get('dusun','')} — Kepala Dusun: {info.get('kepala_dusun','')}")
    st.divider()
    top_metrics(df)

    st.subheader("Distribusi Umur")
    age_dist = age_distribution(df)
    fig = px.bar(x=list(age_dist.keys()), y=list(age_dist.values()), labels={"x":"Rentang usia", "y":"Jumlah"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Jenis Kelamin")
    g = gender_counts(df)
    fig2 = px.pie(names=list(g.keys()), values=list(g.values()), hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Pendidikan Teratas")
    edu = top_categories(df, "pendidikan")
    if edu:
        fig3 = px.bar(x=list(edu.keys()), y=list(edu.values()))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Tidak ada data pendidikan yang tersedia.")

    st.divider()
    # Add button to open form modal (using st.form area)
    st.button("Tambah Data Penduduk", key="open_add")

def show_rt_overview(summary_rt: dict):
    st.subheader("Ringkasan per RT")
    cols = st.columns(len(summary_rt) if summary_rt else 1)
    i = 0
    for rt, s in sorted(summary_rt.items()):
        with cols[i % len(cols)]:
            st.markdown(f"**RT {rt}**")
            st.markdown(f"- Total: {s['total']}")
            st.markdown(f"- KK: {s['kk']}")
            st.markdown(f"- L: {s['L']}")
            st.markdown(f"- P: {s['P']}")
        i += 1

def show_data_kk(grouped_kk: Dict[str, list]):
    st.title("📂 Data Kartu Keluarga (Per KK)")
    for kk, anggota in grouped_kk.items():
        kepala = next((a.get("nama_kepala_keluarga") or a.get("nama") for a in anggota if a.get("nama_kepala_keluarga") or a.get("hubungan_keluarga","").lower().startswith("kepala")), "(Tidak terdeteksi)")
        with st.expander(f"KK {kk} — Kepala: {kepala} — {len(anggota)} anggota"):
            for a in anggota:
                st.markdown(f"**{a.get('nama') or a.get('nama_kepala_keluarga') or a.get('nik','-')}**  \nNIK: `{a.get('nik','-')}`  \nHubungan: {a.get('status_hubungan_dalam_keluarga', a.get('hubungan_keluarga','-'))}")
            st.divider()

def show_rt_detail(df_rt):
    st.title("🔎 Detail Data RT")
    user, role = current_user()
    if not role:
        st.warning("Harap login RT untuk melihat detail ini.")
        st.stop()
    st.caption(f"Diakses oleh {user} ({role})")
    st.dataframe(df_rt, use_container_width=True)

def show_add_form(default_rt=None):
    st.subheader("Tambah Data Penduduk Baru")
    with st.form("add_warga_form", clear_on_submit=True):
        no_kk = st.text_input("No. KK")
        nama_kepala_keluarga = st.text_input("Nama Kepala Keluarga")
        nama = st.text_input("Nama Lengkap")
        nik = st.text_input("NIK")
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["LAKI-LAKI", "PEREMPUAN"])
        tempat_lahir = st.text_input("Tempat Lahir")
        tanggal_lahir = st.text_input("Tanggal Lahir (contoh: 5/7/1967 atau 1967-07-05)")
        status_perkawinan = st.selectbox("Status Perkawinan", ["KAWIN TERCATAT", "BELUM KAWIN", "CERAI"])
        agama = st.text_input("Agama")
        pendidikan = st.text_input("Pendidikan")
        pekerjaan = st.text_input("Pekerjaan")
        golongan_darah = st.text_input("Golongan Darah")
        nama_ayah = st.text_input("Nama Ayah")
        nama_ibu = st.text_input("Nama Ibu")
        no_hp = st.text_input("No. HP")
        rt = st.number_input("RT", min_value=1, max_value=99, value=default_rt or 1)
        rw = st.number_input("RW", min_value=1, max_value=99, value=2)
        submit = st.form_submit_button("Simpan Data")
        if submit:
            row = {
                "no_kk": no_kk, "nama_kepala_keluarga": nama_kepala_keluarga, "nama": nama,
                "nik": nik, "jenis_kelamin": jenis_kelamin, "tempat_lahir": tempat_lahir,
                "tanggal_lahir": tanggal_lahir, "status_perkawinan": status_perkawinan,
                "agama": agama, "pendidikan": pendidikan, "pekerjaan": pekerjaan,
                "golongan_darah": golongan_darah, "nama_ayah": nama_ayah, "nama_ibu": nama_ibu,
                "no_hp": no_hp, "rt": int(rt), "rw": int(rw)
            }
            return row
    return None
