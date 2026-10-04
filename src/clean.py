"""Fill or remove missing values in the Titanic data.

Every function returns a new DataFrame and leaves the input unchanged.
"""

AGE_GROUP_COLUMNS = ["pclass", "sex"]


def add_missing_flags(df):
    """Add True/False columns recording where age and deck were missing.

    Run this BEFORE filling: missing age/deck is linked to lower survival,
    so we keep that signal as its own column.
    """
    df = df.copy()
    df["age_was_missing"] = df["age"].isna()
    df["has_deck"] = df["deck"].notna()
    return df


def fill_age_by_group(df):
    """Fill missing ages with the median age of the same class and sex."""
    df = df.copy()
    # transform("median") returns one value per row: that row's group median
    group_medians = df.groupby(AGE_GROUP_COLUMNS)["age"].transform("median")
    df["age"] = df["age"].fillna(group_medians)
    return df


def drop_deck(df):
    """Drop the deck column (77% empty; has_deck keeps the useful part)."""
    return df.drop(columns=["deck"])


def fill_embarked(df):
    """Fill the few missing ports with the most common one (the mode)."""
    df = df.copy()
    for column in ["embarked", "embark_town"]:
        df[column] = df[column].fillna(df[column].mode()[0])
    return df


def clean_data(df):
    """Run every cleaning step in order."""
    df = add_missing_flags(df)
    df = fill_age_by_group(df)
    df = drop_deck(df)
    df = fill_embarked(df)
    return df
