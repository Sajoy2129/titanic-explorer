import pandas as pd
import pytest

from src.clean import (
    add_missing_flags,
    clean_data,
    drop_deck,
    fill_age_by_group,
)


@pytest.fixture
def sample_df():
    """A tiny fake passenger table with gaps in age, deck and embarked."""
    return pd.DataFrame({
        "pclass": [1, 1, 1, 3, 3, 3],
        "sex": ["male", "male", "male", "female", "female", "female"],
        "age": [40.0, 50.0, None, 20.0, 30.0, None],
        "deck": ["C", None, "B", None, None, None],
        "embarked": ["S", "S", None, "C", "S", "S"],
        "embark_town": ["Southampton", "Southampton", None,
                        "Cherbourg", "Southampton", "Southampton"],
    })


def test_add_missing_flags_marks_gaps(sample_df):
    result = add_missing_flags(sample_df)
    assert result["age_was_missing"].tolist() == [False, False, True,
                                                  False, False, True]
    assert result["has_deck"].tolist() == [True, False, True,
                                           False, False, False]


def test_fill_age_uses_own_group_median(sample_df):
    result = fill_age_by_group(sample_df)
    assert result.loc[2, "age"] == 45.0  # 1st-class male: median(40, 50)
    assert result.loc[5, "age"] == 25.0  # 3rd-class female: median(20, 30)


def test_drop_deck_removes_column(sample_df):
    assert "deck" not in drop_deck(sample_df).columns


def test_clean_data_leaves_no_missing_values(sample_df):
    result = clean_data(sample_df)
    assert result.isna().sum().sum() == 0
    assert "has_deck" in result.columns


def test_clean_data_does_not_change_input(sample_df):
    original = sample_df.copy()
    clean_data(sample_df)
    pd.testing.assert_frame_equal(sample_df, original)
