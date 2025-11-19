# utils/stats.py
import pandas as pd
from datetime import date
import numpy as np

def _parse_date_series(series: pd.Series) -> pd.Series:
    # Accepts many date formats; prefer dayfirst because sample had d/m/yyyy
    return pd.to_datetime(series.fillna(""), dayfirst=True, errors="coerce")

def add_age_column(df: pd.DataFrame, dob_col: str = "tanggal_lahir", out_col: str = "age"):
    if dob_col not in df.columns:
        df[out_col] = pd.NA
        return df
    dob = _parse_date_series(df[dob_col])
    today = pd.Timestamp(date.today())
    ages = (today - dob).dt.days // 365
    df[out_col] = ages
    return df

def age_distribution(df: pd.DataFrame, bins=None, dob_col="tanggal_lahir"):
    df2 = add_age_column(df.copy(), dob_col=dob_col, out_col="age")
    ages = df2["age"].dropna().astype(int)
    if bins is None:
        bins = [0,5,12,17,30,45,60,200]
    labels = ["0-5","6-12","13-17","18-30","31-45","46-60","60+"]
    cat = pd.cut(ages, bins=bins, labels=labels, right=True)
    dist = cat.value_counts().reindex(labels, fill_value=0)
    return dist.to_dict()

def gender_counts(df: pd.DataFrame, gender_col="jenis_kelamin"):
    # normalize common values
    if gender_col not in df.columns:
        return {"L":0, "P":0, "Unknown": len(df)}
    s = df[gender_col].fillna("").astype(str).str.upper()
    male = s.str.contains("L|LAKI").sum()
    female = s.str.contains("P|PEREMPUAN").sum()
    unknown = len(df) - male - female
    return {"L": int(male), "P": int(female), "Unknown": int(unknown)}

def summary_by_rt(df: pd.DataFrame):
    if "rt" not in df.columns:
        return {}
    summary = {}
    for rt, g in df.groupby("rt"):
        summary[int(rt)] = {
            "total": int(len(g)),
            "kk": int(g["no_kk"].nunique()) if "no_kk" in g.columns else 0,
            "L": int(g[g["jenis_kelamin"].str.upper().str.contains("L|LAKI", na=False)].shape[0]) if "jenis_kelamin" in g.columns else 0,
            "P": int(g[g["jenis_kelamin"].str.upper().str.contains("P|PEREMPUAN", na=False)].shape[0]) if "jenis_kelamin" in g.columns else 0,
        }
    return summary

def top_categories(df: pd.DataFrame, column: str, top_n: int = 6):
    if column not in df.columns:
        return {}
    s = df[column].fillna("Tidak Diisi").astype(str)
    return s.value_counts().head(top_n).to_dict()
