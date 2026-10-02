"""Load the raw Titanic data and turn it into a clean DataFrame."""

import pandas as pd
import seaborn as sns

# Columns we drop:
# - deck: ~77% of values are missing, too few to be useful
# - alive, class, embark_town: duplicates of survived, pclass, embarked
REDUNDANT_COLUMNS = ["deck", "alive", "class", "embark_town"]

AGE_BINS = [0, 12, 18, 35, 60, 120]
AGE_LABELS = ["child", "teen", "young adult", "adult", "senior"]


def load_raw_data():
    """Download (first time) or load from cache the Titanic dataset."""
    return sns.load_dataset("titanic")


def drop_redundant_columns(df):
    """Remove columns that are mostly empty or repeat other columns."""
    return df.drop(columns=REDUNDANT_COLUMNS, errors="ignore")


def fill_missing_values(df):
    """Fill missing ages with the median and missing ports with the mode."""
    df = df.copy()
    df["age"] = df["age"].fillna(df["age"].median())
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    return df


def add_features(df):
    """Add new columns built from existing ones."""
    df = df.copy()
    # +1 counts the passenger themselves
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS)
    return df


def clean_data(df):
    """Run every cleaning step in order and return a new DataFrame."""
    df = drop_redundant_columns(df)
    df = fill_missing_values(df)
    df = add_features(df)
    return df
