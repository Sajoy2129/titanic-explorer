import pandas as pd

from src.load import save_csv


def test_save_csv_creates_folder_and_round_trips(tmp_path):
    # tmp_path is a temporary folder pytest creates (and cleans up) for us
    df = pd.DataFrame({"age": [22.0, None], "sex": ["male", "female"]})
    path = tmp_path / "new_folder" / "test.csv"

    returned_path = save_csv(df, path)

    assert returned_path == path
    assert path.exists()
    pd.testing.assert_frame_equal(pd.read_csv(path), df)
