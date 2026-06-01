import json
from unittest.mock import Mock, mock_open, patch

from src.utils import convert_to_rub, load_transactions_from_json


class TestLoadTransactionsFromJson:
    """Тесты для функции загрузки транзакций из JSON"""

    def test_successful_load(self):
        """Тест успешной загрузки данных"""
        mock_data = [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100.50",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200.00",
                    "currency": {"code": "EUR"}
                }
            }
        ]

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("test.json")
                assert len(result) == 2

    def test_empty_file(self):
        """Тест пустого файла"""
        with patch('builtins.open', mock_open(read_data="")):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("empty.json")
                assert result == []

    def test_file_not_found(self):
        """Тест отсутствующего файла"""
        with patch('pathlib.Path.exists', return_value=False):
            result = load_transactions_from_json("missing.json")
            assert result == []


class TestConvertToRub:
    """Тесты для функции конвертации валюты"""

    def test_rub_no_conversion_needed(self):
        """Тест: RUB не требует конвертации"""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"}
            }
        }
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 1000.50

    def test_missing_amount_returns_zero(self):
        """Тест: отсутствует сумма"""
        transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    def test_missing_currency_returns_zero(self):
        """Тест: отсутствует валюта"""
        transaction = {
            "operationAmount": {
                "amount": "100"
            }
        }
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    def test_missing_operation_amount_returns_zero(self):
        """Тест: отсутствует operationAmount"""
        transaction = {"id": 1}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    def test_invalid_amount_returns_zero(self):
        """Тест: некорректная сумма"""
        transaction = {
            "operationAmount": {
                "amount": "not a number",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    @patch('src.utils.requests.get')
    def test_usd_to_rub_successful(self, mock_get):
        """Тест: успешная конвертация USD в RUB"""
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 92.75}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 9275.0

    @patch('src.utils.requests.get')
    def test_eur_to_rub_successful(self, mock_get):
        """Тест: успешная конвертация EUR в RUB"""
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 100.30}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "50",
                "currency": {"code": "EUR"}
            }
        }
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 5015.0

    @patch('src.utils.requests.get')
    def test_api_error_returns_zero(self, mock_get):
        """Тест: ошибка API возвращает 0.0"""
        mock_get.side_effect = Exception("API connection error")

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 0.0

    def test_unsupported_currency(self):
        """Тест: неподдерживаемая валюта"""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "GBP"}
            }
        }
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0