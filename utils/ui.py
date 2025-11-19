import streamlit as st
import pandas as pd
import plotly.express as px
from utils.stats import statistik_rw, statistik_rt
from utils.merge import group_by_family
from utils.loader import save_rt_data
from utils.logger import write_log

def metric_card(label, value, color):
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:15px;
            border-radius:8px;
            color:white;
            text-align:center;
            margin-bottom:10px">
            <h3>{value}</h3>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True
    )

def dashboard_rw(df, config):
    st.title("🏠 Dashboard Kependudukan RW 02 – Dusun Klotok")

    stats = statistik_rw(df)

    col1, col2, col3, col4 = st.columns(4)
    metric_card("Total Penduduk", stats["total"], "#333")
    metric_card("Laki-laki", stats["laki"], "#004080")
    metric_card("Perempuan", stats["perempuan"], "#800040")
    metric_card("Usia Produktif", stats["produktif"], "#226622")

    st.subheader("📊 Penduduk per RT")
    df["RT"] = df["RT"].astype(str)
    fig = px.bar(df.groupby("RT").size().reset_index(name="Jumlah"),
                 x="RT", y="Jumlah", title="Jumlah Penduduk per RT",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def tampil_rt(df, rt):
    st.title(f"👪 Data RT {rt}")

    df_rt = df[df["RT"].astype(str) == str(rt)]
    stats = statistik_rt(df, rt)

    col1, col2, col3 = st.columns(3)
    metric_card("Total Penduduk", stats["total"], "#444")
    metric_card("Laki-laki", stats["laki"], "#004080")
    metric_card("Perempuan", stats["perempuan"], "#800040")

    st.subheader("📦 Data Keluarga")
    families = group_by_family(df_rt)

    for fam in families:
        with st.expander(f"KK: {fam['no_kk']} – Kepala: {fam['kepala']} ({fam['jumlah_anggota']} anggota)"):
            st.table(pd.DataFrame(fam["detail"]))

def form_tambah(df):
    st.subheader("➕ Tambah Data Warga")

    with st.form("form_warga"):
        no_kk = st.text_input("Nomor KK")
        nik = st.text_input("NIK")
        nama = st.text_input("Nama Kepala Keluarga / Warga")
        rt = st.selectbox("RT", ["1", "2", "3"])
        jk = st.selectbox("Jenis Kelamin", ["LAKI-LAKI", "PEREMPUAN"])
        tgl = st.date_input("Tanggal Lahir")
        pekerjaan = st.text_input("Pekerjaan")

        submit = st.form_submit_button("Simpan Data")

    if submit:
        new = {
            "no_kk": no_kk,
            "nik": nik,
            "nama_kepala_keluarga": nama,
            "RT": rt,
            "jenis_kelamin": jk,
            "tanggal_lahir": str(tgl),
            "pekerjaan": pekerjaan
        }

        df_new = pd.concat([df, pd.DataFrame([new])], ignore_index=True)

        save_rt_data(f"rt{rt}", df_new[df_new["RT"] == rt])

        write_log(st.session_state["role"], "TAMBAH", nik)
        st.success("Data berhasil ditambahkan!")
        st.rerun()
