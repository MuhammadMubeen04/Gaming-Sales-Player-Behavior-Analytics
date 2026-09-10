"""
analysis.py
-----------
Core analysis and key insights for the gaming dataset.
"""

import pandas as pd


def overall_summary(df: pd.DataFrame) -> dict:
    """Return overall KPIs."""
    summary = {
        "total_games": len(df),
        "total_sales_millions": round(df["Global_Sales"].sum(), 2),
        "avg_critic_score": round(df["Critic_Score"].mean(), 1),
        "avg_user_score": round(df["User_Score"].mean(), 2),
        "avg_playtime_hours": round(df["Avg_Playtime_Hours"].mean(), 1),
        "avg_price_usd": round(df["Price_USD"].mean(), 2),
        "year_range": f"{df['Year'].min()} – {df['Year'].max()}",
    }
    return summary


def sales_by_platform(df: pd.DataFrame) -> pd.DataFrame:
    """Sales and counts by platform."""
    return (
        df.groupby("Platform")
        .agg(
            Games=("GameID", "count"),
            Total_Sales=("Global_Sales", "sum"),
            Avg_Sales=("Global_Sales", "mean"),
            Avg_Critic=("Critic_Score", "mean"),
            Avg_User=("User_Score", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
    )


def sales_by_genre(df: pd.DataFrame) -> pd.DataFrame:
    """Sales and scores by genre."""
    return (
        df.groupby("Genre")
        .agg(
            Games=("GameID", "count"),
            Total_Sales=("Global_Sales", "sum"),
            Avg_Sales=("Global_Sales", "mean"),
            Avg_Critic=("Critic_Score", "mean"),
            Avg_User=("User_Score", "mean"),
            Avg_Playtime=("Avg_Playtime_Hours", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
    )


def top_games(df: pd.DataFrame, n: int = 15, by: str = "Global_Sales") -> pd.DataFrame:
    """Top N games by a given metric."""
    cols = ["Name", "Platform", "Genre", "Year", "Global_Sales", "Critic_Score", "User_Score", "Publisher"]
    return df.nlargest(n, by)[cols]


def yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Games released and sales per year."""
    return (
        df.groupby("Year")
        .agg(
            Games=("GameID", "count"),
            Total_Sales=("Global_Sales", "sum"),
            Avg_Critic=("Critic_Score", "mean"),
        )
        .round(2)
    )


def publisher_performance(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top publishers by total sales."""
    return (
        df.groupby("Publisher")
        .agg(
            Games=("GameID", "count"),
            Total_Sales=("Global_Sales", "sum"),
            Avg_Critic=("Critic_Score", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .head(top_n)
    )


def print_insights(df: pd.DataFrame) -> None:
    """Print key insights to console."""
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)

    summary = overall_summary(df)
    print(f"Total Games          : {summary['total_games']}")
    print(f"Total Global Sales   : {summary['total_sales_millions']} million units")
    print(f"Avg Critic Score     : {summary['avg_critic_score']}")
    print(f"Avg User Score       : {summary['avg_user_score']}")
    print(f"Year Range           : {summary['year_range']}")

    print("\n--- Top Platform by Sales ---")
    print(sales_by_platform(df).head(3))

    print("\n--- Top Genre by Sales ---")
    print(sales_by_genre(df).head(3))

    print("\n--- Top 5 Games by Sales ---")
    print(top_games(df, n=5)[["Name", "Platform", "Global_Sales", "Critic_Score"]])


if __name__ == "__main__":
    from data_loading import load_raw_data
    from data_cleaning import clean_data

    df = clean_data(load_raw_data())
    print_insights(df)
