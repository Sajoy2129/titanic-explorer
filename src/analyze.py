"""Calculate survival statistics: data in, numbers out (no printing/plots)."""

import pandas as pd

CHILD_MAX_AGE = 12  # 12 and under counts as a child
CLASS_NAMES = {1: "1st class", 2: "2nd class", 3: "3rd class"}

# pd.cut bins include the right edge: (0, 12] -> "0–12", (12, 18] -> "13–18"...
AGE_GROUP_BINS = [0, 12, 18, 40, float("inf")]
AGE_GROUP_LABELS = ["0–12", "13–18", "19–40", "41+"]


def known_ages_only(df):
    """Keep only passengers whose age was recorded, not filled in by cleaning.

    Filled ages are adult group medians, so they would wrongly label
    some unknown-age children as adults.
    """
    return df[~df["age_was_missing"]]


def add_age_category(df):
    """Add an `age_category` column: 'child' (12 and under) or 'adult'."""
    df = df.copy()
    is_child = df["age"] <= CHILD_MAX_AGE
    df["age_category"] = is_child.map({True: "child", False: "adult"})
    return df


def add_age_group(df):
    """Add an `age_group` column: 0–12, 13–18, 19–40 or 41+.

    Ages between groups (e.g. 12.5) go to the higher group.
    """
    df = df.copy()
    df["age_group"] = pd.cut(df["age"], bins=AGE_GROUP_BINS,
                             labels=AGE_GROUP_LABELS, include_lowest=True)
    return df


def survival_rate(df):
    """Return the percentage of passengers who survived (0 to 100)."""
    # survived is 1 or 0, so its mean is the fraction who survived
    return df["survived"].mean() * 100


def survival_rate_by(df, column):
    """Return the survival % for each value in `column`, highest first."""
    return (
        # observed=True: skip empty categories (e.g. an age group with nobody)
        df.groupby(column, observed=True)["survived"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )


def passenger_count_by(df, column):
    """Return how many passengers have each value in `column`."""
    return df[column].value_counts()
