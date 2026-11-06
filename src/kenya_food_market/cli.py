from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from .analysis import (
        DEFAULT_DATA_PATH,
        OUTPUTS_DIR,
        REPORTS_DIR,
        build_pamoja_note,
        compute_retail_market_summary,
        compute_seasonal_wholesale_summary,
        compute_storage_gain_summary,
        ensure_directories,
        prepare_data,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from kenya_food_market.analysis import (
        DEFAULT_DATA_PATH,
        OUTPUTS_DIR,
        REPORTS_DIR,
        build_pamoja_note,
        compute_retail_market_summary,
        compute_seasonal_wholesale_summary,
        compute_storage_gain_summary,
        ensure_directories,
        prepare_data,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Kenya food market prices.")
    parser.add_argument("--data-path", type=Path, default=DEFAULT_DATA_PATH, help="Path to the CSV dataset.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUTS_DIR, help="Directory for generated CSV outputs.")
    parser.add_argument("--report-path", type=Path, default=REPORTS_DIR / "pamoja_note.md", help="Path for the Pamoja advisory note.")
    args = parser.parse_args()

    ensure_directories()
    df = prepare_data(args.data_path)

    seasonal_summary = compute_seasonal_wholesale_summary(df, start_year=2015, end_year=2019)
    storage_summary = compute_storage_gain_summary(df, start_year=2015, end_year=2019)
    retail_summary = compute_retail_market_summary(df, start_year=2015, end_year=2019)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    seasonal_summary.to_csv(args.output_dir / "seasonal_wholesale_maize_2015_2019.csv", index=False)
    retail_summary.to_csv(args.output_dir / "retail_maize_market_summary_2015_2019.csv", index=False)

    note = build_pamoja_note(df)
    args.report_path.parent.mkdir(parents=True, exist_ok=True)
    args.report_path.write_text(note, encoding="utf-8")

    print(f"Data rows analyzed: {len(df)}")
    print(f"Cheapest wholesale month: {storage_summary['cheapest_month']} at KES {storage_summary['cheapest_price_kes']:.2f}")
    print(f"June vs January: {storage_summary['share_higher']:.0f}% of market-years higher; median gain KES {storage_summary['median_gain']:.2f}")
    print(f"Most expensive retail market: {retail_summary.iloc[0]['market']} at KES {retail_summary.iloc[0]['average_price_kes_per_kg']:.2f}/kg")
    print(f"Report written to: {args.report_path}")


if __name__ == "__main__":
    main()
