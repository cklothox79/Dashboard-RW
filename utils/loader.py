import pandas as pd
import os
import yaml

def load_config():
    with open("config/info_wilayah.yaml", "r") as f:
        return yaml.safe_load(f)

def ensure_directories():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

def load_rt_data():
    data_all = []
    for rt in ["rt1", "rt2", "rt3"]:
        path = f"data/{rt}/data_{rt}.csv"
        if os.path.exists(path):
            df = pd.read_csv(path, dtype=str)
            df["RT_Folder"] = rt
            data_all.append(df)
    if data_all:
        merged = pd.concat(data_all, ignore_index=True)
        merged.to_csv("data/warga_merged.csv", index=False)
        return merged
    else:
        return pd.DataFrame()

def save_rt_data(rt, df):
    df.to_csv(f"data/{rt}/data_{rt}.csv", index=False)
