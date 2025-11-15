# utils/merge.py
import pandas as pd
from .loader import load_rt, save_raw

def merge_all():
    dfs = []
    for rt_key in ["rt1", "rt2", "rt3"]:
        df = load_rt(rt_key)
        if not df.empty:
            df["rt"] = rt_key
            dfs.append(df)
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
    else:
        combined = pd.DataFrame(columns=list(load_rt("rt1").columns) + ["rt"])
    save_raw(combined)
    return combined
