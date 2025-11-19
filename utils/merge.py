# utils/merge.py
import pandas as pd

def group_by_kk(df: pd.DataFrame) -> dict:
    """
    Group dataframe by 'no_kk'.
    Returns { no_kk: [record_dicts] }
    """
    if df.empty:
        return {}
    if "no_kk" not in df.columns:
        raise KeyError("DataFrame harus memiliki kolom 'no_kk'.")
    grouped = {kk: group.to_dict(orient="records") for kk, group in df.groupby("no_kk")}
    return grouped

def get_family_members(df: pd.DataFrame, no_kk: str):
    if df.empty:
        return []
    return df[df["no_kk"] == no_kk].to_dict(orient="records")
