import pandas as pd

from src.charts import save_all_charts


def test_save_all_charts_writes_one_png_per_finding(tmp_path):
    df = pd.DataFrame({
        "survived": [1, 0, 1, 0],
        "sex": ["female", "male", "female", "male"],
        "pclass": [1, 3, 2, 3],
        "age": [8.0, 40.0, 30.0, 25.0],
        "age_was_missing": [False, False, False, True],
    })
    out_dir = tmp_path / "charts"

    paths = save_all_charts(df, out_dir)

    assert len(paths) == 5
    for path in paths:
        assert path.exists()
        assert path.suffix == ".png"
        assert path.stat().st_size > 0  # file isn't empty
