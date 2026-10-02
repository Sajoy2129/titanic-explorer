"""Tests for titanic/analysis.py."""

import pandas as pd
import pytest

from titanic.analysis import overall_survival_rate, survival_rate_by


def make_sample_data():
    return pd.DataFrame({
        "survived": [0, 1, 1, 0],
        "sex": ["male", "female", "female", "male"],
        "pclass": [3, 1, 1, 3],
    })


def test_overall_survival_rate():
    assert overall_survival_rate(make_sample_data()) == 0.5


def test_survival_rate_is_between_0_and_1():
    rate = overall_survival_rate(make_sample_data())
    assert 0 <= rate <= 1


def test_survival_rate_by_sex():
    rates = survival_rate_by(make_sample_data(), "sex")
    assert len(rates) == 2
    assert rates["female"] == 1.0
    assert rates["male"] == 0.0


def test_survival_rate_by_sorted_highest_first():
    rates = survival_rate_by(make_sample_data(), "pclass")
    assert list(rates.index) == [1, 3]


def test_unknown_column_raises_error():
    with pytest.raises(KeyError):
        survival_rate_by(make_sample_data(), "not_a_column")
