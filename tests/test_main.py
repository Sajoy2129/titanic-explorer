from main import parse_args


def test_chart_flag_is_off_by_default():
    assert parse_args([]).chart is False


def test_chart_flag_turns_on():
    assert parse_args(["--chart"]).chart is True
