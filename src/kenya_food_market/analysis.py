from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = ROOT_DIR / "data" / "food-prices-kenya.csv"
OUTPUTS_DIR = ROOT_DIR / "outputs"
REPORTS_DIR = ROOT_DIR / "reports"


def prepare_data(data_path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load and clean the Kenya food market dataset."""
    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    df.loc[df["market"] == "Hola", "county"] = df.loc[df["market"] == "Hola", "county"].fillna("Tana River")
    df.loc[df["market"] == "Hola", "region"] = df.loc[df["market"] == "Hola", "region"].fillna("Coast")

    df["price_per_kg"] = np.where(df["unit"] == "90 KG", df["price_kes"] / 90, df["price_kes"])
    return df


def filter_wholesale_maize(df: pd.DataFrame, start_year: int | None = None, end_year: int | None = None) -> pd.DataFrame:
    subset = df[(df["commodity"] == "Maize") & (df["price_type"] == "Wholesale")].copy()
    if start_year is not None:
        subset = subset[subset["year"] >= start_year]
    if end_year is not None:
        subset = subset[subset["year"] <= end_year]
    return subset


def compute_seasonal_wholesale_summary(
    df: pd.DataFrame,
    start_year: int | None = None,
    end_year: int | None = None,
) -> pd.DataFrame:
    wholesale = filter_wholesale_maize(df, start_year=start_year, end_year=end_year)
    summary = (
        wholesale.groupby("month", as_index=False)["price_kes"]
        .mean()
        .rename(columns={"price_kes": "avg_price_kes"})
        .sort_values("month")
        .reset_index(drop=True)
    )
    return summary


def compute_storage_gain_summary(
    df: pd.DataFrame,
    start_year: int = 2015,
    end_year: int = 2019,
) -> dict[str, Any]:
    wholesale = filter_wholesale_maize(df, start_year=start_year, end_year=end_year)

    monthly = compute_seasonal_wholesale_summary(df, start_year=start_year, end_year=end_year)
    cheapest_month = int(monthly.loc[monthly["avg_price_kes"].idxmin(), "month"])
    dearest_month = int(monthly.loc[monthly["avg_price_kes"].idxmax(), "month"])

    market_year_prices = (
        wholesale[wholesale["month"].isin([1, 6])]
        .groupby(["market", "year", "month"])["price_kes"]
        .mean()
        .unstack("month")
        .rename(columns={1: "January", 6: "June"})
        .dropna(subset=["January", "June"])
    )
    market_year_prices["gain"] = market_year_prices["June"] - market_year_prices["January"]

    return {
        "cheapest_month": cheapest_month,
        "cheapest_price_kes": float(monthly["avg_price_kes"].min()),
        "dearest_month": dearest_month,
        "dearest_price_kes": float(monthly["avg_price_kes"].max()),
        "share_higher": float((market_year_prices["gain"] > 0).mean() * 100),
        "median_gain": float(market_year_prices["gain"].median()),
    }


def compute_retail_market_summary(
    df: pd.DataFrame,
    start_year: int = 2015,
    end_year: int = 2019,
) -> pd.DataFrame:
    retail_maize = df[
        (df["commodity"] == "Maize")
        & (df["price_type"] == "Retail")
        & df["year"].between(start_year, end_year)
    ].copy()

    market_year_retail = (
        retail_maize.groupby(["market", "year"], as_index=False)["price_kes"]
        .mean()
        .rename(columns={"price_kes": "annual_avg_kes_per_kg"})
    )

    summary = (
        market_year_retail.groupby("market", as_index=False)["annual_avg_kes_per_kg"]
        .mean()
        .rename(columns={"annual_avg_kes_per_kg": "average_price_kes_per_kg"})
        .sort_values("average_price_kes_per_kg", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def compute_top_three_markets(df: pd.DataFrame, start_year: int = 2015, end_year: int = 2019) -> set[str]:
    retail_maize = df[
        (df["commodity"] == "Maize")
        & (df["price_type"] == "Retail")
        & df["year"].between(start_year, end_year)
    ].copy()

    market_year_retail = (
        retail_maize.groupby(["market", "year"], as_index=False)["price_kes"]
        .mean()
        .rename(columns={"price_kes": "annual_avg_kes_per_kg"})
    )
    market_year_retail["rank"] = market_year_retail.groupby("year")["annual_avg_kes_per_kg"].rank(
        method="min", ascending=False
    )

    top_three_by_year = {
        year: set(group.loc[group["rank"] <= 3, "market"])
        for year, group in market_year_retail.groupby("year")
    }
    return set.intersection(*top_three_by_year.values()) if top_three_by_year else set()


def build_pamoja_note(df: pd.DataFrame) -> str:
    seasonal_summary = compute_seasonal_wholesale_summary(df, start_year=2015, end_year=2019)
    storage_summary = compute_storage_gain_summary(df, start_year=2015, end_year=2019)
    retail_summary = compute_retail_market_summary(df, start_year=2015, end_year=2019)
    top_three = compute_top_three_markets(df, start_year=2015, end_year=2019)

    cheapest_month = seasonal_summary.loc[seasonal_summary["avg_price_kes"].idxmin(), "month"]
    dearest_month = seasonal_summary.loc[seasonal_summary["avg_price_kes"].idxmax(), "month"]
    retail_gap = float(retail_summary["average_price_kes_per_kg"].max() - retail_summary["average_price_kes_per_kg"].min())

    ranked_markets = sorted(top_three)
    if len(ranked_markets) == 1:
        top_markets_sentence = ranked_markets[0]
    elif len(ranked_markets) == 2:
        top_markets_sentence = f"{ranked_markets[0]} and {ranked_markets[1]}"
    else:
        top_markets_sentence = ", ".join(ranked_markets[:-1]) + f", and {ranked_markets[-1]}"

    return f"""# Pamoja Agri-Advisory: maize market note

Data source: World Food Programme (WFP) Kenya food prices and Humanitarian Data Exchange (HDX) market data.

## Advice for farmers

1. Sell early if you need cash soon after harvest. The cheapest month for wholesale maize in 2015-2019 was month {int(cheapest_month)}, when the average bag price was KES {storage_summary['cheapest_price_kes']:.2f}; the highest month was {int(dearest_month)} at KES {storage_summary['dearest_price_kes']:.2f}. This makes January a stronger cash-sale month than the late-spring peak.
2. Holding maize until June can work, but only if storage costs stay low. In {storage_summary['share_higher']:.0f}% of market-years, June prices were higher than January, and the median gain was KES {storage_summary['median_gain']:.2f} per bag. That is a real upside, but it is not guaranteed.
3. Price differences between markets matter a lot. The average retail maize price ranged from KES {retail_summary['average_price_kes_per_kg'].min():.2f}/kg to KES {retail_summary['average_price_kes_per_kg'].max():.2f}/kg, a gap of KES {retail_gap:.2f}/kg. For households, the difference between the cheapest and most expensive markets can be material.

## Advice for county officers

4. Monitor the markets that repeatedly rank as the most expensive. The top retail markets in 2015-2019 were {top_markets_sentence}; both were in the top three every year in the five-year comparison. Those repeated high-price markets are the clearest places to check for transport bottlenecks, supply shortages, or thin trading conditions.

## Bottom line

The historical pattern suggests that maize storage can sometimes pay, but only after covering storage, transport, spoilage, financing, and quality-loss costs. County officers should pay closest attention to markets that remain persistently expensive rather than assuming a single county-wide trend.
"""


def ensure_directories() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
