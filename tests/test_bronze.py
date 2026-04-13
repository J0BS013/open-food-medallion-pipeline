from unittest.mock import MagicMock, patch

import pytest
import requests

from pipeline.bronze import fetch_product


@patch("pipeline.bronze.requests.get")
def test_fetch_product_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 1, "product": {"product_name": "Nutella"}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product("3017620429484")

    assert result["status"] == 1
    assert result["product"]["product_name"] == "Nutella"


@patch("pipeline.bronze.requests.get")
def test_fetch_product_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Product not found"):
        fetch_product("0000000000000")


@patch("pipeline.bronze.requests.get")
def test_fetch_product_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Forbidden")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_product("3017620429484")
