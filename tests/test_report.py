import pandas as pd
import pytest

from src.report import build_report, save_report


@pytest.fixture
def clean_df():
    """A tiny table shaped like clean_data() output."""
    return pd.DataFrame({
        "survived": [1, 1, 0, 0],
        "sex": ["female", "female", "male", "male"],
        "pclass": [1, 2, 3, 3],
        "age": [8.0, 30.0, 40.0, 25.0],
        "age_was_missing": [False, False, False, True],
        "has_deck": [True, False, False, False],
    })


def test_build_report_contains_each_finding(clean_df):
    report = build_report(clean_df)
    assert "2 of 4 passengers survived (50.0%)" in report
    assert "female     100.0%  (n=2)" in report
    assert "1st class  100.0%  (n=1)" in report
    assert "recorded ages only: 3 passengers" in report
    assert "1 missing ages filled" in report
    assert "deck dropped (3 of 4 missing)" in report
    assert "0–12       100.0%  (n=1)" in report


def test_build_report_lists_charts_only_when_given(clean_df):
    assert "Charts" not in build_report(clean_df)
    report = build_report(clean_df, ["outputs/a.png"])
    assert "  - outputs/a.png" in report


def test_save_report_writes_text(tmp_path):
    path = save_report("hello\n", tmp_path / "out" / "report.txt")
    assert path.read_text() == "hello\n"
