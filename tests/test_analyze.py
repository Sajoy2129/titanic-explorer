import pandas as pd

from src.analyze import (
    add_age_category,
    add_age_group,
    known_ages_only,
    passenger_count_by,
    survival_rate,
    survival_rate_by,
)


def test_survival_rate_is_percentage():
    df = pd.DataFrame({"survived": [1, 0, 0, 1]})
    assert survival_rate(df) == 50.0


def test_survival_rate_when_nobody_survived():
    df = pd.DataFrame({"survived": [0, 0, 0]})
    assert survival_rate(df) == 0.0


def test_survival_rate_by_sex_highest_first():
    df = pd.DataFrame({
        "sex": ["male", "male", "female", "female"],
        "survived": [0, 1, 1, 1],
    })
    result = survival_rate_by(df, "sex")
    assert result.to_dict() == {"female": 100.0, "male": 50.0}
    assert result.index[0] == "female"


def test_add_age_category_boundary_at_12():
    df = pd.DataFrame({"age": [0.5, 12.0, 12.5, 60.0]})
    result = add_age_category(df)
    assert result["age_category"].tolist() == ["child", "child",
                                               "adult", "adult"]


def test_known_ages_only_drops_filled_ages():
    df = pd.DataFrame({"age": [5.0, 30.0], "age_was_missing": [False, True]})
    result = known_ages_only(df)
    assert result["age"].tolist() == [5.0]


def test_passenger_count_by_counts_each_value():
    df = pd.DataFrame({"pclass": [1, 3, 3, 3]})
    assert passenger_count_by(df, "pclass").to_dict() == {3: 3, 1: 1}


def test_add_age_group_boundaries():
    df = pd.DataFrame({"age": [0.4, 12.0, 12.5, 18.0, 19.0, 40.0, 40.5, 80.0]})
    result = add_age_group(df)
    assert result["age_group"].tolist() == [
        "0–12", "0–12", "13–18", "13–18", "19–40", "19–40", "41+", "41+",
    ]
