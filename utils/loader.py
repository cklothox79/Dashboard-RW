import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RT_DIRS = {
    "rt1": DATA_DIR / "rt1" / "data_rt1.csv",
    "rt2": DATA_DIR / "rt2" / "data_rt2.csv",
    "rt3": DATA_DIR / "rt3" / "data_rt3.csv",
}

def load_rt(rt_key: str) -> pd.DataFrame:
    """
    Memuat data dari CSV untuk RT yang ditentukan.
    """
    path = RT_DIRS.get(rt_key)
    if not path.exists():
        return pd.DataFrame(columns=["no_kk", "nama_kepala_keluarga", "alamat", "rt", "rw", "kode_pos", 
                                     "desa_kelurahan", "kecamatan", "kabupaten_kota", "provinsi", "tanggal_dikeluarkan"])
    return pd.read_csv(path)

def save_rt(rt_key: str, df: pd.DataFrame):
    """
    Menyimpan data ke CSV untuk RT yang ditentukan.
    """
    path = RT_DIRS.get(rt_key)
    df.to_csv(path, index=False)
