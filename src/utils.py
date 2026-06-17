import json
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем API ключ
API_KEY = os.getenv("EXCHANGE_API_KEY")


def load_transaction(file_path: str) -> list:
    """Загружает транзакции из JSON-файла"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def convert_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции из USD или EUR в рубли"""
    # Получаем данные из транзакции
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount")
    currency_dict = operation_amount.get("currency", {})
    currency_code = currency_dict.get("code")

    # Проверяем наличие данных
    if amount_str is None or currency_code is None:
        return 0.0

    # Преобразуем сумму в число
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    # Если рубли - возвращаем как есть (НЕ проверяем API_KEY)
    if currency_code == "RUB":
        return amount

    # Если не USD и не EUR - не конвертируем
    if currency_code not in ("USD", "EUR"):
        return 0.0

    # Для конвертации USD/EUR нужен API_KEY
    # Если API_KEY нет, возвращаем 0.0
    if not API_KEY:
        return 0.0

    # Выполняем запрос к API
    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": API_KEY}
        params = {"base": currency_code, "symbols": "RUB"}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return 0.0

        data = response.json()
        rub_rate = data.get("rates", {}).get("RUB")

        if rub_rate is None:
            return 0.0

        result = amount * rub_rate
        return round(result, 2)

    except (requests.RequestException, KeyError, ValueError, TypeError):
        return 0.0
