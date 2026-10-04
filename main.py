"""Entry point: load -> save copy -> describe -> clean -> (charts) -> report.

Usage:
    python3 main.py            # report only
    python3 main.py --chart    # report + PNG charts in outputs/
"""

import argparse

from src.charts import save_all_charts
from src.clean import clean_data
from src.load import describe_data, load_titanic, save_csv
from src.report import build_report, save_report


def parse_args(argv=None):
    """Read command-line options. argv=None means use the real command line."""
    parser = argparse.ArgumentParser(
        description="Explore the Titanic dataset and write a survival report."
    )
    parser.add_argument(
        "--chart",
        action="store_true",  # flag: True if given, False if not
        help="also save charts as PNG files in outputs/",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    df = load_titanic()

    saved_path = save_csv(df)
    print(f"Saved a copy to {saved_path}\n")

    print("===== Raw data =====")
    describe_data(df)

    clean_df = clean_data(df)
    print("\n===== After cleaning =====")
    describe_data(clean_df)

    chart_paths = save_all_charts(clean_df) if args.chart else []

    report = build_report(clean_df, chart_paths)
    report_path = save_report(report)
    print()
    print(report)
    print(f"Report saved to {report_path}")
    if not args.chart:
        print("Charts skipped (run with --chart to save them)")


# Runs only when you execute `python main.py`, not when another file imports it.
if __name__ == "__main__":
    main()
