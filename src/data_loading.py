"""
data_loading.py
---------------
Load raw gaming dataset.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "games_data.csv"


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw games dataset from CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    print(f"[data_loading] Loaded {len(df):,} records from {path.name}")
    return df


if __name__ == "__main__":
    df = load_raw_data()
    print(df.head())
    print(df.info())
