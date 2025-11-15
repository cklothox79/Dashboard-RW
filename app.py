import streamlit as st
import pandas as pd
from utils.loader import load_rt, save_rt
from utils.auth import check_password
from utils.ui import inject_css, header
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Bank Data RW 02", layout="wide", page_icon="🏘️")

# Inject custom CSS
inject_css()

# Header
header()

# Login untuk proteksi password
def password_page():
    st.subheader("Masukkan Password untuk Akses Data")
    password = st.text_input("Password", type="password")
    if password:
        role = check_password(password)
        if role:
            st.session_state["role"] = role
            st.success(f"Akses diberikan untuk {role}")
        else:
            st.error("Password salah!")

if "role" not in st.session_state:
    password_page()

else:
    # Sidebar navigasi
    st.sidebar.header("Navigasi")
    page = st.sidebar.radio("Pilih Halaman", ["Dashboard", "Input Data KK", "Input Anggota Keluarga", "Lihat Data"])

    rt_key = st.sidebar.radio("Pilih RT", ["rt1", "rt2", "rt3"])

    if page == "Dashboard":
        st.title("Dashboard Data")
        st.write("Menampilkan statistik umum atau data terkait lainnya.")
        df = load_rt(rt_key)
        st.dataframe(df)

    elif page == "Input Data KK":
        input_kk(rt_key)

    elif page == "Input Anggota Keluarga":
        input_anggota(rt_key)

    elif page == "Lihat Data":
        df = load_rt(rt_key)
        st.subheader(f"Data KK dan Anggota Keluarga RT {rt_key}")
        st.dataframe(df)

# Input data KK
def input_kk(rt_key: str):
    st.subheader(f"Input Data KK untuk RT {rt_key}")

    with st.form(key=f"kk_form", clear_on_submit=True):
        no_kk = st.text_input("Nomor KK")
        nama_kepala_keluarga = st.text_input("Nama Kepala Keluarga")
        alamat = st.text_input("Alamat")
        rt = st.text_input("RT")
        rw = st.text_input("RW")
        kode_pos = st.text_input("Kode Pos")
        desa_kelurahan = st.text_input("Desa/Kelurahan")
        kecamatan = st.text_input("Kecamatan")
        kabupaten_kota = st.text_input("Kabupaten/Kota")
        provinsi = st.text_input("Provinsi")
        tanggal_dikeluarkan = st.date_input("Tanggal Dikeluarkan")

        submit_button = st.form_submit_button("Simpan Kartu Keluarga")

        if submit_button:
            kk_data = {
                "no_kk": no_kk,
                "nama_kepala_keluarga": nama_kepala_keluarga,
                "alamat": alamat,
                "rt": rt,
                "rw": rw,
                "kode_pos": kode_pos,
                "desa_kelurahan": desa_kelurahan,
                "kecamatan": kecamatan,
                "kabupaten_kota": kabupaten_kota,
                "provinsi": provinsi,
                "tanggal_dikeluarkan": tanggal_dikeluarkan.strftime("%Y-%m-%d")
            }
            df_kk = pd.DataFrame([kk_data])
            df = load_rt(rt_key)
            df = pd.concat([df, df_kk], ignore_index=True)
            save_rt(rt_key, df)
            st.success("Data Kartu Keluarga berhasil disimpan!")

# Input data anggota keluarga
def input_anggota(rt_key: str):
    st.subheader(f"Input Anggota Keluarga untuk RT {rt_key}")

    with st.form(key=f"anggota_form", clear_on_submit=True):
        no_urut = st.number_input("No. Urut Anggota", min_value=1)
        nama_lengkap = st.text_input("Nama Lengkap")
        nik = st.text_input("NIK")
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        tempat_lahir = st.text_input("Tempat Lahir")
        tanggal_lahir = st.date_input("Tanggal Lahir")
        agama = st.selectbox("Agama", ["Islam", "Kristen", "Katolik", "Hindu", "Budha", "Konghucu"])
        pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah", "SD", "SMP", "SMA", "D1", "D2", "D3", "S1", "S2", "S3"])
        jenis_pekerjaan = st.text_input("Jenis Pekerjaan")
        status_perkawinan = st.selectbox("Status Perkawinan", ["Kawin", "Belum Kawin", "Cerai"])
        status_hubungan_dalam_keluarga = st.selectbox("Status Hubungan dalam Keluarga", ["Kepala Keluarga", "Istri", "Anak"])
        kewarganegaraan = st.selectbox("Kewarganegaraan", ["WNI", "WNA"])
        no_paspor = st.text_input("No. Paspor")
        no_kitap = st.text_input("No. KITAP")
        ayah = st.text_input("Nama Ayah")
        ibu = st.text_input("Nama Ibu")

        submit_button = st.form_submit_button("Simpan Anggota Keluarga")

        if submit_button:
            anggota_data = {
                "no_urut": no_urut,
                "nama_lengkap": nama_lengkap,
                "nik": nik,
                "jenis_kelamin": jenis_kelamin,
                "tempat_lahir": tempat_lahir,
                "tanggal_lahir": tanggal_lahir.strftime("%Y-%m-%d"),
                "agama": agama,
                "pendidikan": pendidikan,
                "jenis_pekerjaan": jenis_pekerjaan,
                "status_perkawinan": status_perkawinan,
                "status_hubungan_dalam_keluarga": status_hubungan_dalam_keluarga,
                "kewarganegaraan": kewarganegaraan,
                "no_paspor": no_paspor,
                "no_kitap": no_kitap,
                "ayah": ayah,
                "ibu": ibu
            }
            df_anggota = pd.DataFrame([anggota_data])
            df = load_rt(rt_key)
            df = pd.concat([df, df_anggota], ignore_index=True)
            save_rt(rt_key, df)
            st.success("Data Anggota Keluarga berhasil disimpan!")
