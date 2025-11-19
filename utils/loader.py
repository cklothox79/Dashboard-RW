import pandas as pd
import yaml

def load_info(path="config/info_wilayah.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_warga(path="data/warga.csv"):
    df = pd.read_csv(path, dtype=str)

    # convert numerik
    df["rt"] = df["rt"].astype(int)
    df["rw"] = df["rw"].astype(int)

    return df
