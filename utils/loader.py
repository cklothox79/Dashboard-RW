# utils/loader.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RT_DIRS = {
    "rt1": DATA_DIR / "rt1" / "data_rt1.csv",
    "rt2": DATA_DIR / "rt2" / "data_rt2.csv",
    "rt3": DATA_DIR / "rt3" / "data_rt3.csv",
}
RAW_PATH = DATA_DIR / "raw" / "raw_combined.csv"

DEFAULT_COLUMNS = ["kk", "nama_kepala_keluarga", "alamat", "jumlah_keluarga", "tanggal_input"]

def ensure_files():
    # buat folder & file jika belum ada
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "rt1").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "rt2").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "rt3").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
    for p in RT_DIRS.values():
        if not p.exists():
            pd.DataFrame(columns=DEFAULT_COLUMNS).to_csv(p, index=False)
    if not RAW_PATH.exists():
        pd.DataFrame(columns=DEFAULT_COLUMNS + ["rt"]).to_csv(RAW_PATH, index=False)

def load_rt(rt_key: str) -> pd.DataFrame:
    ensure_files()
    path = RT_DIRS.get(rt_key)
    if not path:
        raise ValueError("RT tidak ditemukan")
    return pd.read_csv(path)

def save_rt(rt_key: str, df: pd.DataFrame):
    ensure_files()
    path = RT_DIRS.get(rt_key)
    df.to_csv(path, index=False)

def load_raw() -> pd.DataFrame:
    ensure_files()
    return pd.read_csv(RAW_PATH)

def save_raw(df):
    ensure_files()
    df.to_csv(RAW_PATH, index=False)
