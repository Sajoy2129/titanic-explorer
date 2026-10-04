"""Build a plain-text summary report and save it. No calculations here.

The numbers come from src/analyze.py, so the report always matches the charts.
"""

from pathlib import Path

from src.analyze import (
    CHILD_MAX_AGE,
    CLASS_NAMES,
    add_age_category,
    add_age_group,
    known_ages_only,
    passenger_count_by,
    survival_rate,
    survival_rate_by,
)

DEFAULT_REPORT_PATH = Path("outputs") / "report.txt"


def _group_lines(df, column, names=None, sort_by_label=False):
    """Return one line per group: name, survival %, and passenger count."""
    rates = survival_rate_by(df, column)
    if sort_by_label:
        rates = rates.sort_index()
    counts = passenger_count_by(df, column)
    names = names or {}
    lines = []
    for value, rate in rates.items():
        name = names.get(value, str(value))
        lines.append(f"  {name:<10} {rate:5.1f}%  (n={counts[value]})")
    return lines


def build_report(df, chart_paths=()):
    """Return the full report as one string. `df` must be cleaned data."""
    survived = df["survived"].sum()
    filled_ages = df["age_was_missing"].sum()
    missing_decks = (~df["has_deck"]).sum()
    known_ages = add_age_group(add_age_category(known_ages_only(df)))

    lines = [
        "TITANIC SURVIVAL REPORT",
        "=======================",
        f"Passengers: {len(df)}",
        "",
        "Data cleaning",
        f"  - {filled_ages} missing ages filled with the median for the "
        "passenger's class and sex",
        f"  - deck dropped ({missing_decks} of {len(df)} missing); "
        "kept as a has_deck flag",
        "",
        "1. Overall survival",
        f"  {survived} of {len(df)} passengers survived "
        f"({survival_rate(df):.1f}%)",
        "",
        "2. By sex: women survived far more often than men",
        *_group_lines(df, "sex"),
        "",
        "3. By class: survival fell from 1st to 3rd class",
        *_group_lines(df, "pclass", CLASS_NAMES, sort_by_label=True),
        "",
        f"4. By age: children ({CHILD_MAX_AGE} and under) survived more "
        "than adults",
        f"   (recorded ages only: {len(known_ages)} passengers)",
        *_group_lines(known_ages, "age_category"),
        "",
        "5. By age group (recorded ages only)",
        *_group_lines(known_ages, "age_group", sort_by_label=True),
    ]

    if chart_paths:
        lines += ["", "Charts", *[f"  - {path}" for path in chart_paths]]

    return "\n".join(lines) + "\n"


def save_report(text, path=DEFAULT_REPORT_PATH):
    """Write the report text to a file, creating the folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")  # utf-8 handles the "–" dash
    return path
