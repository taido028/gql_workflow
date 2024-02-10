import json
from utils.DBFeeder import get_demodata
from unittest.mock import mock_open, patch


def test_datetime_parser_with_none_value():
    mock_json_data = json.dumps({
        "startdate": None,
        "enddate": None,
        "lastchange": None,
        "created": None
    })

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        data = get_demodata()
        assert data["startdate"] is None
        assert data["enddate"] is None
        assert data["lastchange"] is None
        assert data["created"] is None


def test_datetime_parser_with_invalid_datetime_format():
    mock_json_data = json.dumps({
        "startdate": "invalid-date-format",
        "enddate": "invalid-date-format",
        "lastchange": "invalid-date-format",
        "created": "invalid-date-format"
    })

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        data = get_demodata()
        assert data["startdate"] is None
        assert data["enddate"] is None
        assert data["lastchange"] is None
        assert data["created"] is None


