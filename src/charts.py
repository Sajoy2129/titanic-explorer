"""Draw one chart per finding and save each as a PNG. No calculations here.

The numbers come from src/analyze.py, so charts always match the printed report.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save to files only; never open a window

import matplotlib.pyplot as plt  # noqa: E402 (must come after matplotlib.use)

from src.analyze import (  # noqa: E402
    CLASS_NAMES,
    add_age_category,
    add_age_group,
    known_ages_only,
    passenger_count_by,
    survival_rate,
    survival_rate_by,
)

DEFAULT_OUT_DIR = Path("outputs")


def _save(fig, out_dir, filename):
    """Save a figure to out_dir/filename, free its memory, return the path."""
    path = Path(out_dir) / filename
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return path


def _bar_chart(rates, title, xlabel, out_dir, filename, bar_labels=None):
    """Draw survival percentages as labelled bars (shared by every chart).

    bar_labels: optional text under each bar; defaults to the index values.
    """
    if bar_labels is None:
        bar_labels = [str(label) for label in rates.index]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(bar_labels, rates.values)
    ax.bar_label(bars, fmt="%.1f%%")  # write the number on top of each bar
    ax.set(title=title, xlabel=xlabel, ylabel="Survived (%)", ylim=(0, 100))
    return _save(fig, out_dir, filename)


def plot_overall_survival(df, out_dir=DEFAULT_OUT_DIR):
    """Finding 1: what share of all passengers survived."""
    survived = survival_rate(df)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([survived, 100 - survived], labels=["Survived", "Died"],
           autopct="%.1f%%", startangle=90)
    ax.set(title=f"Overall survival ({len(df)} passengers)")
    return _save(fig, out_dir, "1_overall_survival.png")


def plot_survival_by_sex(df, out_dir=DEFAULT_OUT_DIR):
    """Finding 2: women survived far more often than men."""
    return _bar_chart(survival_rate_by(df, "sex"), "Survival rate by sex",
                      "Sex", out_dir, "2_survival_by_sex.png")


def plot_survival_by_class(df, out_dir=DEFAULT_OUT_DIR):
    """Finding 3: survival falls from 1st to 3rd class."""
    rates = survival_rate_by(df, "pclass").sort_index()  # keep 1, 2, 3 order
    counts = passenger_count_by(df, "pclass")
    # e.g. "1st class\n(n=216)" — \n puts the count on a second line
    bar_labels = [f"{CLASS_NAMES[pclass]}\n(n={counts[pclass]})"
                  for pclass in rates.index]
    return _bar_chart(rates, "Survival rate by ticket class", "Ticket class",
                      out_dir, "3_survival_by_class.png", bar_labels)


def plot_survival_by_age(df, out_dir=DEFAULT_OUT_DIR):
    """Finding 4: children (12 and under) survived more than adults.

    Uses recorded ages only (filled-in ages are all adult medians).
    """
    known = add_age_category(known_ages_only(df))
    return _bar_chart(survival_rate_by(known, "age_category"),
                      f"Children vs adults ({len(known)} recorded ages)",
                      "Age group", out_dir, "4_survival_by_age.png")


def plot_survival_by_age_group(df, out_dir=DEFAULT_OUT_DIR):
    """Finding 5: survival rate for each age group (recorded ages only)."""
    known = add_age_group(known_ages_only(df))
    rates = survival_rate_by(known, "age_group").sort_index()  # youngest first
    counts = passenger_count_by(known, "age_group")
    bar_labels = [f"{group}\n(n={counts[group]})" for group in rates.index]
    return _bar_chart(rates, "Survival rate by age group (recorded ages)",
                      "Age (years)", out_dir, "5_survival_by_age_group.png",
                      bar_labels)


def save_all_charts(df, out_dir=DEFAULT_OUT_DIR):
    """Create every chart and return the list of saved file paths."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    chart_functions = [
        plot_overall_survival,
        plot_survival_by_sex,
        plot_survival_by_class,
        plot_survival_by_age,
        plot_survival_by_age_group,
    ]
    return [make_chart(df, out_dir) for make_chart in chart_functions]
