# Kenya Food Market Analysis

This project analyzes monthly food-price data for Kenya to understand how maize and beans are priced across wholesale and retail markets, how seasonal patterns affect farmer decisions, and which markets are consistently more expensive for households.

The repo is designed around an exploratory analysis workflow using Python, pandas, and matplotlib, with the main work captured in a Jupyter notebook.

## Project overview

Pamoja Agri-Advisory is a fictional Kenyan NGO that helps smallholder farmer groups and county food-security committees interpret market signals. The central questions are:

- Is it better to sell maize immediately after harvest or store it and sell later?
- How do wholesale and retail prices differ in practice?
- Which county markets are consistently the most expensive for households?
- Which years and months show the sharpest price changes?

The underlying dataset contains real monthly prices published by the World Food Programme (WFP), while the NGO context is fictional.

## Dataset

The data file is located at `data/food-prices-kenya.csv`.

### Coverage
- Time range: 2006-01-15 to 2019-12-15
- Rows: 2,742
- Markets: 14
- Counties: 13
- Regions: 6
- Commodities: maize, beans
- Price types: wholesale, retail
- Units: `90 KG` and `KG`

### Data fields
- `date`
- `region`
- `county`
- `market`
- `commodity`
- `price_type`
- `unit`
- `price_kes`
- `price_usd`

## Repository structure

```text
.
├── README.md
├── analysis.ipynb
├── data/
│   └── food-prices-kenya.csv
├── pyproject.toml
├── src/
│   └── kenya_food_market/
│       └── __init__.py
├── .python-version
├── .venv/
├── uv.lock
└── .gitignore
```

## Analysis goals

The analysis focuses on a few practical questions:

1. Compare maize and beans across price types and markets.
2. Convert prices to a common per-kilogram basis for fair comparison.
3. Measure year-to-year and month-to-month changes in wholesale maize prices.
4. Assess whether storing maize from January to June is usually profitable.
5. Rank retail markets by average price and identify high-cost counties.

## Setup

This project uses Python 3.13 and the `uv` dependency manager.

```bash
uv venv
source .venv/bin/activate
uv sync
```

If you prefer a direct install from the local project:

```bash
uv pip install -e .
```

## Running the analysis

Open the notebook in the project root:

```bash
jupyter notebook analysis.ipynb
```

or open it directly in VS Code/Jupyter support.

## Key analysis workflow

The notebook covers the following steps:

- loading the CSV and checking data quality
- fixing missing county/region values for the `Hola` market
- standardizing prices to a comparable per-kilogram view
- separating wholesale and retail series for fair comparisons
- plotting yearly maize trends and seasonal patterns
- comparing January and June prices to evaluate storage decisions
- ranking county markets by average retail cost

## Notes

- This project is primarily an exploratory data analysis rather than a production package.
- The NGO description is fictional, but the price data is based on real WFP market observations.
- The project is intentionally structured to keep the analytical workflow transparent and easy to extend.

<!-- ## Suggested next improvements

- add reusable Python scripts for ETL and analysis steps
- convert the notebook into a more maintainable package structure
- add summary charts and exported CSV/PNG outputs
- add tests for data-cleaning logic and price normalization -->

## License

This project is intended for educational and analytical use. Check the repository and data source terms before using the outputs in a formal or commercial context.