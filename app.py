# app.py
import streamlit as st
from utils.auth import login_widget, logout, current_user, check_credentials
from utils.loader import load_all_warga, load_info, save_row_to_rt, save_full_dataframe_to_rt
from utils.merge import group_by_kk
from utils.stats import summary_by_rt
from utils.ui import (
    inject_css,
    show_dashboard,
    show_rt_overview,
    show_data_kk,
    show_rt_detail,
    show_add_form,
)
from utils.logger import write_log
import pandas as pd

st.set_page_config(page_title="Bank Data RW 02 - Dusun Klotok", layout="wide", page_icon="🏘️")

# --- Authentication widget in sidebar ---
_ = login_widget()
user, role = current_user()

# Sidebar navigation
inject_css()
st.sidebar.title("🏷 Navigasi")
menu = st.sidebar.radio("Menu", ("Dashboard", "Data Keluarga (KK)", "Data Warga", "RT Detail", "Admin Panel"))

# logout button
if st.sidebar.button("Logout"):
    logout()
    st.experimental_rerun()

# Load data & config
df_all = load_all_warga()
info = load_info()
grouped = group_by_kk(df_all)
summary_rt = summary_by_rt(df_all)

# ROUTING
if menu == "Dashboard":
    # show dashboard metrics & charts
    show_dashboard(df_all, info)
    st.divider()
    show_rt_overview(summary_rt)
    st.divider()
    # Add data button on dashboard
    if st.session_state.get("open_add"):
        # nothing: button toggles state only
        pass
    # show add form inline
    new_row = show_add_form()
    if new_row:
        # Save and log
        save_row_to_rt(new_row)
        write_log(user or "anonymous", role or "unknown", "tambah", target=new_row.get("nik") or new_row.get("no_kk"), extra={"rt": new_row.get("rt")})
        st.success("Data berhasil disimpan.")
        st.experimental_rerun()

elif menu == "Data Keluarga (KK)":
    show_data_kk(grouped)

elif menu == "Data Warga":
    st.title("📋 Data Warga Seluruh RW")
    st.dataframe(df_all, use_container_width=True)

elif menu == "RT Detail":
    st.title("📍 RT Detail")
    # Choose RT to view
    rt_choice = st.sidebar.selectbox("Pilih RT", sorted(df_all["rt"].dropna().unique().tolist()) if not df_all.empty else [1])
    # Access control: if user is RT, only allow that RT; RW/Admin allow all
    if user is None:
        st.info("Silakan login untuk membuka detail RT (hanya user RT/RW/Admin dapat membuka).")
    else:
        # if role like 'rt1' or 'rt2' or 'rt3'
        if role.startswith("rt"):
            allowed_rt = int(role.replace("rt",""))
            if allowed_rt != int(rt_choice):
                st.error("Anda hanya dapat mengakses RT Anda sendiri.")
            else:
                df_rt = df_all[df_all["rt"] == int(rt_choice)]
                show_rt_detail(df_rt)
                write_log(user, role, "buka_rt_detail", target=f"rt{rt_choice}")
        else:
            # RW or Admin
            df_rt = df_all[df_all["rt"] == int(rt_choice)]
            show_rt_detail(df_rt)
            write_log(user or "anonymous", role or "unknown", "buka_rt_detail", target=f"rt{rt_choice}")

elif menu == "Admin Panel":
    # Only admin allowed
    if role != "admin":
        st.error("Hanya admin yang dapat mengakses panel ini.")
    else:
        st.title("⚙️ Admin Panel")
        st.write("Fitur admin: lihat log, export, dan manajemen pengguna.")
        # show logs
        log_path = "data/log/activity.log"
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.read().strip().splitlines()
            st.subheader("Activity Log (terbaru paling bawah)")
            for ln in lines[-200:]:
                st.text(ln)
        except FileNotFoundError:
            st.info("Belum ada log aktivitas.")
