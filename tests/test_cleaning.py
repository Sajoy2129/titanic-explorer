"""Tests for titanic/cleaning.py.

We use a tiny hand-made DataFrame instead of downloading the real data,
so the tests are fast, work offline, and we know the exact answers.
"""

import numpy as np
import pandas as pd

from titanic.cleaning import clean_data


def make_sample_data():
    return pd.DataFrame({
        "survived": [0, 1, 1],
        "pclass": [3, 1, 3],
        "sex": ["male", "female", "female"],
        "age": [22.0, np.nan, 40.0],
        "sibsp": [1, 0, 0],
        "parch": [0, 0, 2],
        "fare": [7.25, 71.28, 7.92],
        "embarked": ["S", np.nan, "S"],
        "class": ["Third", "First", "Third"],
        "deck": [np.nan, "C", np.nan],
        "embark_town": ["Southampton", np.nan, "Southampton"],
        "alive": ["no", "yes", "yes"],
    })


def test_redundant_columns_are_dropped():
    cleaned = clean_data(make_sample_data())
    for column in ["deck", "alive", "class", "embark_town"]:
        assert column not in cleaned.columns


def test_no_missing_age_or_embarked():
    cleaned = clean_data(make_sample_data())
    assert cleaned["age"].isna().sum() == 0
    assert cleaned["embarked"].isna().sum() == 0


def test_missing_age_filled_with_median():
    cleaned = clean_data(make_sample_data())
    # median of 22 and 40 is 31
    assert cleaned.loc[1, "age"] == 31.0


def test_family_size_counts_passenger():
    cleaned = clean_data(make_sample_data())
    assert list(cleaned["family_size"]) == [2, 1, 3]


def test_original_data_is_not_changed():
    raw = make_sample_data()
    clean_data(raw)
    assert raw["age"].isna().sum() == 1
