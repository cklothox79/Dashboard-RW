import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        .main > .block-container{
            padding: 1.5rem 2rem;
        }
        .title {
            font-size:34px;
            font-weight:700;
        }
        .card {
            background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        }
        .small-muted {color: #9aa4a6; font-size: 13px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def header():
    st.markdown("# Bank Data RW 02")
    st.caption("Aplikasi untuk mengelola data KK dan Anggota Keluarga di RW 02, Desa Simogirang.")
