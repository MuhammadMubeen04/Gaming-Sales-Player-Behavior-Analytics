"""
data_cleaning.py
----------------
Clean and prepare the gaming dataset.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "games_cleaned.csv"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw games dataframe."""
    df = df.copy()

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"[data_cleaning] Removed {before - len(df)} duplicate rows")

    # Handle missing values (if any)
    numeric_cols = ["Global_Sales", "Critic_Score", "User_Score", "Avg_Playtime_Hours", "Price_USD", "Year"]
    for col in numeric_cols:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Ensure types
    df["Year"] = df["Year"].astype(int)
    df["Critic_Score"] = df["Critic_Score"].astype(int)
    df["Global_Sales"] = df["Global_Sales"].astype(float)
    df["User_Score"] = df["User_Score"].astype(float)

    # Derived columns
    df["Sales_Category"] = pd.cut(
        df["Global_Sales"],
        bins=[-0.01, 1, 5, 15, 100],
        labels=["Low (<1M)", "Medium (1-5M)", "High (5-15M)", "Blockbuster (15M+)"]
    )
    df["Score_Gap"] = (df["Critic_Score"] / 10 - df["User_Score"]).round(2)
    df["Decade"] = (df["Year"] // 10) * 10

    print(f"[data_cleaning] Cleaned shape: {df.shape}")
    return df


def save_processed(df: pd.DataFrame, path: Path = PROCESSED_PATH) -> None:
    """Save cleaned data to processed folder."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[data_cleaning] Saved processed data → {path}")


if __name__ == "__main__":
    from data_loading import load_raw_data
    raw = load_raw_data()
    cleaned = clean_data(raw)
    save_processed(cleaned)
    print(cleaned.head())
