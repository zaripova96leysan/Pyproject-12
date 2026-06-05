import json
from unittest.mock import Mock, mock_open, patch

import pytest
import requests

from src.utils import convert_to_rub, load_transaction


def test_load_transaction_success():
    """Тест успешной загрузки транзакций"""
    fake_data = [{"id": 1, "name": "test"}]
    json_string = json.dumps(fake_data)

    with patch("builtins.open", mock_open(read_data=json_string)):
        result = load_transaction("any.json")
    # Функция должна вернуть загруженные данные
    assert result == fake_data
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_load_transaction_empty_list():
    """Тест загрузки пустого списка"""
    fake_data = []
    json_string = json.dumps(fake_data)

    with patch("builtins.open", mock_open(read_data=json_string)):
        result = load_transaction("empty.json")
    assert result == []


def test_load_transaction_not_list():
    """Тест загрузки данных не в виде списка"""
    fake_data = {"key": "value"}
    json_string = json.dumps(fake_data)

    with patch("builtins.open", mock_open(read_data=json_string)):
        result = load_transaction("not_list.json")
    assert result == []


def test_load_transaction_invalid_json():
    """Тест загрузки некорректного JSON"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = load_transaction("invalid.json")
    assert result == []


def test_convert_to_rub_rub():
    """Тест конвертации RUB (без конвертации)"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "RUB"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 100.0
    assert isinstance(result, float)


def test_convert_to_rub_usd_success():
    """Тест успешной конвертации USD в RUB"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": "success",
        "rates": {"RUB": 90.50}
    }

    with patch("src.utils.requests.get", return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        expected = 100 * 90.5
        assert result == expected
        assert isinstance(result, float)


def test_convert_to_rub_eur_success():
    """Тест успешной конвертации EUR в RUB"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": "success",
        "rates": {"RUB": 95.0}
    }

    with patch("src.utils.requests.get", return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "50",
                "currency": {"code": "EUR"}
            }
        }
        result = convert_to_rub(transaction)
        expected = 50 * 95.0
        assert result == expected
        assert isinstance(result, float)


def test_convert_to_rub_requests_exception():
    """Тест обработки исключения requests"""
    with patch("src.utils.requests.get", side_effect=requests.RequestException("Network error")):
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        assert result == 0.0
        assert isinstance(result, float)


def test_convert_to_rub_api_error_status():
    """Тест обработки ошибки API (статус не 200)"""
    mock_response = Mock()
    mock_response.status_code = 404

    with patch("src.utils.requests.get", return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        assert result == 0.0
        assert isinstance(result, float)


def test_convert_to_rub_missing_rub_key():
    """Тест отсутствия ключа RUB в ответе API"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": "success",
        "rates": {"USD": 1.0}
    }

    with patch("src.utils.requests.get", return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        assert result == 0.0
        assert isinstance(result, float)


def test_convert_to_rub_missing_operation_amount():
    """Тест отсутствия operationAmount в транзакции"""
    transaction = {"id": 1}
    result = convert_to_rub(transaction)
    assert result == 0.0
    assert isinstance(result, float)


def test_convert_to_rub_missing_amount():
    """Тест отсутствия amount в транзакции"""
    transaction = {
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 0.0
    assert isinstance(result, float)


def test_convert_to_rub_missing_currency():
    """Тест отсутствия currency в транзакции"""
    transaction = {
        "operationAmount": {
            "amount": "100"
        }
    }
    result = convert_to_rub(transaction)
    assert result == 0.0
    assert isinstance(result, float)


def test_convert_to_rub_invalid_amount():
    """Тест некорректного значения суммы"""
    transaction = {
        "operationAmount": {
            "amount": "not_a_number",
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 0.0
    assert isinstance(result, float)


def test_convert_to_rub_unsupported_currency():
    """Тест неподдерживаемой валюты"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "GBP"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 0.0
    assert isinstance(result, float)