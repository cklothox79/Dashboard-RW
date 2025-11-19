# utils/loader.py
import pandas as pd
from pathlib import Path
import yaml
from typing import Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = DATA_DIR / "log"

# ensure log dir exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

INFO_PATH = CONFIG_DIR / "info_wilayah.yaml"

def load_info() -> dict:
    if not INFO_PATH.exists():
        return {}
    with open(INFO_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def list_rt_files() -> dict:
    """
    Return mapping of rt_key -> file path
    Looks for data/rt*/data_rt*.csv
    """
    mapping = {}
    for rt_dir in sorted(DATA_DIR.glob("rt*")):
        if rt_dir.is_dir():
            # find first csv with prefix data_rt
            csvs = list(rt_dir.glob("data_rt*.csv"))
            if csvs:
                key = rt_dir.name  # e.g., 'rt1'
                mapping[key] = csvs[0]
    return mapping

def load_all_warga() -> pd.DataFrame:
    """
    Load and concat all RT CSVs (if exist).
    Normalize column names to lowercase.
    """
    rt_files = list_rt_files()
    dfs = []
    for rt_key, path in rt_files.items():
        try:
            df = pd.read_csv(path, dtype=str)
            # normalize column names to lowercase
            df.columns = [c.strip().lower() for c in df.columns]
            # ensure rt column exists and as int if convertible
            if "rt" not in df.columns:
                # infer from folder name
                try:
                    df["rt"] = int(rt_key.replace("rt", ""))
                except:
                    df["rt"] = None
            else:
                # clean whitespace and convert to int when possible
                df["rt"] = df["rt"].str.extract(r"(\d+)").astype(float).astype("Int64")
            dfs.append(df)
        except Exception as e:
            print(f"Warning loading {path}: {e}")
    if dfs:
        combined = pd.concat(dfs, ignore_index=True, sort=False)
    else:
        combined = pd.DataFrame()
    return combined

def save_row_to_rt(row: dict):
    """
    Save a single row (dictionary) into the proper RT csv file based on row['rt'].
    Creates the RT folder and file if not exists (with header inferred from row keys).
    """
    rt_val = row.get("rt")
    if rt_val is None:
        raise ValueError("Field 'rt' harus diisi.")
    rt_key = f"rt{int(rt_val)}"
    rt_dir = DATA_DIR / rt_key
    rt_dir.mkdir(parents=True, exist_ok=True)
    csv_path = rt_dir / f"data_{rt_key}.csv"

    # normalize keys and order
    row_norm = {k.strip().lower(): v for k, v in row.items()}

    if csv_path.exists():
        df = pd.read_csv(csv_path, dtype=str)
        df.columns = [c.strip().lower() for c in df.columns]
        df = pd.concat([df, pd.DataFrame([row_norm])], ignore_index=True, sort=False)
    else:
        df = pd.DataFrame([row_norm])
    df.to_csv(csv_path, index=False)
    return csv_path

def save_full_dataframe_to_rt(df: pd.DataFrame, rt_key: str):
    """
    Overwrite RT file with df (useful for edits/deletes).
    rt_key like 'rt1'
    """
    rt_dir = DATA_DIR / rt_key
    rt_dir.mkdir(parents=True, exist_ok=True)
    csv_path = rt_dir / f"data_{rt_key}.csv"
    # ensure lowercase columns
    df.columns = [c.strip().lower() for c in df.columns]
    df.to_csv(csv_path, index=False)
    return csv_path
