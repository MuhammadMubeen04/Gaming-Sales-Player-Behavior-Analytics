"""
visualization.py
----------------
Create and save charts for the gaming analytics project.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CHARTS_DIR = BASE_DIR / "outputs" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)


def save_fig(name: str) -> None:
    path = CHARTS_DIR / name
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[visualization] Saved {path.name}")


def plot_sales_by_platform(df: pd.DataFrame) -> None:
    data = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots()
    data.plot(kind="barh", color="#4e79a7", ax=ax)
    ax.set_title("Total Global Sales by Platform (Million Units)")
    ax.set_xlabel("Sales (Millions)")
    save_fig("01_sales_by_platform.png")


def plot_sales_by_genre(df: pd.DataFrame) -> None:
    data = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots()
    data.plot(kind="barh", color="#59a14f", ax=ax)
    ax.set_title("Total Global Sales by Genre (Million Units)")
    ax.set_xlabel("Sales (Millions)")
    save_fig("02_sales_by_genre.png")


def plot_yearly_trend(df: pd.DataFrame) -> None:
    yearly = df.groupby("Year").agg(Sales=("Global_Sales", "sum"), Games=("GameID", "count"))
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.bar(yearly.index, yearly["Sales"], color="#4e79a7", alpha=0.8, label="Sales")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Sales (Millions)", color="#4e79a7")
    ax2 = ax1.twinx()
    ax2.plot(yearly.index, yearly["Games"], color="#e15759", marker="o", label="Games Released")
    ax2.set_ylabel("Games Released", color="#e15759")
    ax1.set_title("Yearly Sales & Number of Games Released")
    save_fig("03_yearly_trend.png")


def plot_score_distribution(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df["Critic_Score"], bins=20, kde=True, ax=axes[0], color="#4e79a7")
    axes[0].set_title("Critic Score Distribution")
    sns.histplot(df["User_Score"], bins=20, kde=True, ax=axes[1], color="#59a14f")
    axes[1].set_title("User Score Distribution")
    save_fig("04_score_distribution.png")


def plot_critic_vs_user(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="Critic_Score", y="User_Score", hue="Genre", alpha=0.6, ax=ax)
    ax.set_title("Critic Score vs User Score by Genre")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    save_fig("05_critic_vs_user.png")


def plot_top_games(df: pd.DataFrame, n: int = 10) -> None:
    top = df.nlargest(n, "Global_Sales")[["Name", "Global_Sales"]].sort_values("Global_Sales")
    fig, ax = plt.subplots()
    ax.barh(top["Name"], top["Global_Sales"], color="#f28e2b")
    ax.set_title(f"Top {n} Games by Global Sales")
    ax.set_xlabel("Sales (Millions)")
    save_fig("06_top_games_by_sales.png")


def plot_playtime_by_genre(df: pd.DataFrame) -> None:
    order = df.groupby("Genre")["Avg_Playtime_Hours"].mean().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.boxplot(data=df, x="Genre", y="Avg_Playtime_Hours", order=order, ax=ax, palette="Set2")
    ax.set_title("Average Playtime by Genre")
    ax.tick_params(axis="x", rotation=30)
    save_fig("07_playtime_by_genre.png")


def plot_publisher_sales(df: pd.DataFrame, top_n: int = 10) -> None:
    data = (
        df.groupby("Publisher")["Global_Sales"]
        .sum()
        .nlargest(top_n)
        .sort_values()
    )
    fig, ax = plt.subplots()
    data.plot(kind="barh", color="#76b7b2", ax=ax)
    ax.set_title(f"Top {top_n} Publishers by Global Sales")
    ax.set_xlabel("Sales (Millions)")
    save_fig("08_top_publishers.png")


def generate_all_charts(df: pd.DataFrame) -> None:
    """Run all visualization functions."""
    print("[visualization] Generating charts...")
    plot_sales_by_platform(df)
    plot_sales_by_genre(df)
    plot_yearly_trend(df)
    plot_score_distribution(df)
    plot_critic_vs_user(df)
    plot_top_games(df)
    plot_playtime_by_genre(df)
    plot_publisher_sales(df)
    print(f"[visualization] All charts saved to {CHARTS_DIR}")


if __name__ == "__main__":
    from data_loading import load_raw_data
    from data_cleaning import clean_data

    df = clean_data(load_raw_data())
    generate_all_charts(df)
