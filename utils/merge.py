def group_by_kk(df):
    """
    Mengelompokkan warga berdasarkan nomor KK.
    Output: dict {no_kk: list anggota}
    """
    return {
        kk: group.to_dict(orient="records")
        for kk, group in df.groupby("no_kk")
    }


def get_kepala_keluarga(anggota):
    for orang in anggota:
        if orang.get("hubungan_keluarga", "").lower() in ["kepala keluarga", "kepala"]:
            return orang["nama"]
    return "(Tidak ada kepala keluarga)"
