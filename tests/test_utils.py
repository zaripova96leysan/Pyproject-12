import json
from unittest.mock import Mock, mock_open, patch

from src.utils import convert_to_rub, load_transactions_from_json


class TestLoadTransactionsFromJson:
    """Тесты для функции загрузки транзакций из JSON"""

    def test_successful_load(self):
        """Тест успешной загрузки данных"""
        mock_data = [
            {"amount": 100, "currency": "USD"},
            {"amount": 200, "currency": "EUR"}
        ]

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("test.json")
                assert len(result) == 2
                assert result[0]["amount"] == 100
                assert result[0]["currency"] == "USD"

    def test_empty_file(self):
        """Тест пустого файла"""
        with patch('builtins.open', mock_open(read_data="")):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("empty.json")
                assert result == []

    def test_invalid_json(self):
        """Тест некорректного JSON"""
        with patch('builtins.open', mock_open(read_data="not json")):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("invalid.json")
                assert result == []

    def test_file_not_found(self):
        """Тест отсутствующего файла"""
        with patch('pathlib.Path.exists', return_value=False):
            result = load_transactions_from_json("missing.json")
            assert result == []

    def test_not_list_data(self):
        """Тест когда JSON не содержит список"""
        mock_data = {"key": "value"}

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('pathlib.Path.exists', return_value=True):
                result = load_transactions_from_json("object.json")
                assert result == []


class TestConvertToRub:
    """Тесты для функции конвертации валюты"""

    def test_rub_no_conversion_needed(self):
        """Тест: RUB не требует конвертации"""
        transaction = {"amount": 1000.50, "currency": "RUB"}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 1000.50

    def test_missing_amount_returns_zero(self):
        """Тест: отсутствует сумма"""
        transaction = {"currency": "USD"}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    def test_missing_currency_returns_zero(self):
        """Тест: отсутствует валюта"""
        transaction = {"amount": 100}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    def test_invalid_amount_returns_zero(self):
        """Тест: некорректная сумма"""
        transaction = {"amount": "not a number", "currency": "USD"}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0

    @patch('src.utils.requests.get')
    def test_usd_to_rub_successful(self, mock_get):
        """Тест: успешная конвертация USD в RUB"""
        # Создаем мок-ответ от API
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 92.75}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 9275.0


        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "/USD" in args[0]
        assert 'headers' in kwargs

    @patch('src.utils.requests.get')
    def test_eur_to_rub_successful(self, mock_get):
        """Тест: успешная конвертация EUR в RUB"""
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 100.30}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        transaction = {"amount": 50, "currency": "EUR"}
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 5015.0

    @patch('src.utils.requests.get')
    def test_api_error_returns_zero(self, mock_get):
        """Тест: ошибка API возвращает 0.0"""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("API connection error")

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)

        assert isinstance(result, float)
        assert result == 0.0

    def test_unsupported_currency(self):
        """Тест: неподдерживаемая валюта"""
        transaction = {"amount": 100, "currency": "GBP"}
        result = convert_to_rub(transaction)
        assert isinstance(result, float)
        assert result == 0.0
