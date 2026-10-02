"""Run the full Titanic pipeline: load -> clean -> analyze -> chart."""

from titanic.analysis import print_report
from titanic.charts import save_all_charts
from titanic.cleaning import clean_data, load_raw_data


def main():
    raw = load_raw_data()
    df = clean_data(raw)
    print_report(df)

    saved_paths = save_all_charts(df)
    print("\nCharts saved:")
    for path in saved_paths:
        print(f"  {path}")


# Runs only when you execute `python main.py`, not when another file imports it.
if __name__ == "__main__":
    main()
