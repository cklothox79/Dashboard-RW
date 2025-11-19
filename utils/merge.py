import pandas as pd

def group_by_family(df):
    grouped = df.groupby("no_kk")
    families = []

    for kk, group in grouped:
        data = {
            "no_kk": kk,
            "kepala": group.iloc[0]["nama_kepala_keluarga"],
            "jumlah_anggota": len(group),
            "detail": group.to_dict(orient="records")
        }
        families.append(data)

    return families
