from pathlib import Path

from kenya_food_market.analysis import (
    compute_retail_market_summary,
    compute_seasonal_wholesale_summary,
    prepare_data,
)


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food-prices-kenya.csv"


def test_prepare_data_adds_expected_columns():
    df = prepare_data(DATA_PATH)

    assert {"date", "year", "month", "price_per_kg"}.issubset(df.columns)
    assert df["date"].dtype.kind in {"M"}
    assert df["market"].isin(["Hola"]).any()


def test_seasonal_wholesale_summary_has_expected_rows():
    df = prepare_data(DATA_PATH)
    summary = compute_seasonal_wholesale_summary(df)

    assert set(summary.columns) == {"month", "avg_price_kes"}
    assert len(summary) == 12
    assert summary["avg_price_kes"].notna().all()


def test_retail_market_summary_ranks_markets():
    df = prepare_data(DATA_PATH)
    summary = compute_retail_market_summary(df, start_year=2015, end_year=2019)

    assert "market" in summary.columns
    assert "average_price_kes_per_kg" in summary.columns
    assert len(summary) >= 1
    assert summary["average_price_kes_per_kg"].notna().all()
