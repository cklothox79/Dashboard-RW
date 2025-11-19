import streamlit as st
from utils.merge import get_kepala_keluarga

# ---------- UI KK ----------
def show_data_kk(grouped_kk):
    st.title("📂 Data Keluarga (KK)")

    for kk, anggota in grouped_kk.items():
        kepala = get_kepala_keluarga(anggota)

        with st.expander(f"🧩 KK {kk} — Kepala: {kepala} — {len(anggota)} anggota"):
            for orang in anggota:
                st.markdown(f"""
                    **{orang['nama']}**
                    - NIK: `{orang['nik']}`
                    - Hubungan: {orang['hubungan_keluarga']}
                    - Jenis Kelamin: {orang['jenis_kelamin']}
                    - Tempat/Tanggal Lahir: {orang['tempat_lahir']}, {orang['tgl_lahir']}
                """)
            st.divider()


# ---------- UI WARGA ----------
def show_data_warga(df):
    st.title("👥 Data Warga")

    # Filter
    rt_filter = st.selectbox("Filter RT", [0] + sorted(df["rt"].unique()), index=0)
    gender_filter = st.selectbox("Filter Jenis Kelamin", ["Semua", "L", "P"])

    df_filtered = df.copy()
    if rt_filter != 0:
        df_filtered = df_filtered[df_filtered["rt"] == rt_filter]
    if gender_filter != "Semua":
        df_filtered = df_filtered[df_filtered["jenis_kelamin"] == gender_filter]

    st.dataframe(df_filtered, use_container_width=True)


# ---------- DASHBOARD ----------
def show_dashboard(df, info):
    st.title("🏡 Dashboard Kependudukan RT/RW")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Warga", len(df))
    col2.metric("Jumlah KK", df["no_kk"].nunique())
    col3.metric("RT Aktif", df["rt"].nunique())

    st.subheader("Info Wilayah")
    st.json(info)
