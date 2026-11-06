# Kenya Food Market Analysis

This project analyzes Kenya’s food-price data to understand maize and beans across wholesale and retail markets, seasonal price patterns, and the cost of food in different counties.

The repository now follows a script-based structure so the analysis can be run from a Python package rather than only in a notebook.

## Project overview

Pamoja Agri-Advisory is a fictional Kenyan NGO helping smallholder farmer groups and county food-security committees interpret market conditions. The main questions are:

- Is it better to sell maize immediately after harvest or store it and sell later?
- How do wholesale and retail prices differ?
- Which county markets are consistently the most expensive for households?
- Which months and years show the sharpest price swings?

The underlying data are real monthly market prices from the World Food Programme (WFP), and the HDX dataset is used as the public data source for this analysis.

## Data source and credit

- World Food Programme (WFP) Kenya food market prices
- Humanitarian Data Exchange (HDX)

The dataset is stored in `data/food-prices-kenya.csv` and contains monthly observations from 2006 to 2019.

## Dataset summary

- Time range: 2006-01-15 to 2019-12-15
- Rows: 2,742
- Markets: 14
- Counties: 13
- Regions: 6
- Commodities: maize, beans
- Price types: wholesale, retail
- Units: `90 KG` and `KG`

## Script-based project structure

```text
.
├── README.md
├── analysis.ipynb
├── data/
│   └── food-prices-kenya.csv
├── outputs/
│   ├── retail_maize_market_summary_2015_2019.csv
│   └── seasonal_wholesale_maize_2015_2019.csv
├── pyproject.toml
├── reports/
│   └── pamoja_note.md
├── src/
│   └── kenya_food_market/
│       ├── __init__.py
│       ├── __main__.py
│       ├── analysis.py
│       └── cli.py
├── tests/
│   └── test_analysis.py
├── .python-version
├── .venv/
├── uv.lock
└── .gitignore
```

## Setup

This project uses Python 3.13 with `uv`.

```bash
uv venv
source .venv/bin/activate
uv sync
```

To install the package in editable mode:

```bash
uv pip install -e .
```

## Run the analysis

```bash
python -m kenya_food_market
```

or:

```bash
kenya-food-market
```

This generates the CSV summaries in `outputs/` and writes the Pamoja note to `reports/pamoja_note.md`.

## Notebook and script workflow

The reusable analysis logic is in the package, while the notebook remains a working exploratory companion.

- load and clean the CSV data
- fill the missing `Hola` county and region values
- normalize prices to a common `price_per_kg` basis
- compare wholesale and retail maize flows
- summarize seasonal patterns in wholesale prices
- rank counties by average retail costs
- generate the Pamoja advisory note

## Pamoja one-page note

The advisory note is saved in [reports/pamoja_note.md](reports/pamoja_note.md).

It includes:

- three farmer recommendations backed by numbers from the notebook/data
- one county-officer recommendation backed by a market ranking number
- the required data credit to WFP and HDX

## License and usage

This project is intended for educational and analytical use. Please check the original WFP and HDX data terms before using outputs in a formal report or commercial setting.