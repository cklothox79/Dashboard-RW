import pandas as pd
from datetime import datetime

def hitung_usia(tgl):
    try:
        return datetime.now().year - pd.to_datetime(tgl).year
    except:
        return None

def statistik_rw(df):
    df["usia"] = df["tanggal_lahir"].apply(hitung_usia)

    total = len(df)
    laki = len(df[df["jenis_kelamin"] == "LAKI-LAKI"])
    perempuan = len(df[df["jenis_kelamin"] == "PEREMPUAN"])

    anak = len(df[df["usia"].between(0, 14, inclusive="both")])
    produktif = len(df[df["usia"].between(15, 64, inclusive="both")])
    lansia = len(df[df["usia"] >= 65])

    return {
        "total": total,
        "laki": laki,
        "perempuan": perempuan,
        "anak": anak,
        "produktif": produktif,
        "lansia": lansia
    }

def statistik_rt(df, rt):
    return statistik_rw(df[df["RT"].astype(str) == str(rt)])
