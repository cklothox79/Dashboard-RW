# utils/ui.py
import streamlit as st
from pathlib import Path
import yaml

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

def load_info_wilayah():
    cfg = Path(__file__).resolve().parent.parent / "config" / "info_wilayah.yaml"
    import yaml
    with open(cfg, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def header():
    info = load_info_wilayah()
    desa = info.get("desa")
    dusun = info.get("dusun")
    rw = info.get("rw", {})
    st.markdown(f"### 🏘️ Bank Data RW {rw.get('nomor', '')} — {desa}, {dusun}")
    st.caption(f"Kepala Dusun: {info.get('kepala_dusun')} · Ketua RW: {rw.get('ketua_rw')}")
