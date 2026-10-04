"""Load the Titanic dataset, save a local copy, and describe it."""

from pathlib import Path

import seaborn as sns

DEFAULT_CSV_PATH = Path("data") / "titanic.csv"


def load_titanic():
    """Return the Titanic dataset as a DataFrame (seaborn caches it after the first download)."""
    return sns.load_dataset("titanic")


def save_csv(df, path=DEFAULT_CSV_PATH):
    """Save df to a CSV file, creating the folder if needed. Returns the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)  # index=False: don't write the 0, 1, 2... row numbers
    return path


def describe_data(df):
    """Print the shape, column names, and missing-value count per column."""
    rows, columns = df.shape
    print(f"Shape: {rows} rows x {columns} columns\n")

    print("Columns:")
    for name in df.columns:
        print(f"  {name}")

    print("\nMissing values per column:")
    print(df.isna().sum().to_string())
