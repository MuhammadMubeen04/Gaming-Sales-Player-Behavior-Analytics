"""
main.py
-------
Entry point for the Gaming Analytics project.
Runs the full pipeline: Load → Clean → Analyze → Visualize
"""

from pathlib import Path
import sys

# Ensure src is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.data_loading import load_raw_data
from src.data_cleaning import clean_data, save_processed
from src.analysis import overall_summary, sales_by_platform, sales_by_genre, top_games, print_insights
from src.visualization import generate_all_charts


def main():
    print("=" * 60)
    print("GAMING SALES & PLAYER BEHAVIOR ANALYTICS")
    print("=" * 60)

    # 1. Load
    raw_df = load_raw_data()

    # 2. Clean
    df = clean_data(raw_df)
    save_processed(df)

    # 3. Analysis
    print_insights(df)

    print("\n--- Sales by Platform ---")
    print(sales_by_platform(df))

    print("\n--- Sales by Genre ---")
    print(sales_by_genre(df))

    print("\n--- Top 10 Games by Sales ---")
    print(top_games(df, n=10)[["Name", "Platform", "Genre", "Global_Sales", "Critic_Score"]])

    # 4. Visualizations
    generate_all_charts(df)

    print("\n" + "=" * 60)
    print("✅ Pipeline complete!")
    print("   Charts → outputs/charts/")
    print("   Cleaned data → data/processed/games_cleaned.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()
