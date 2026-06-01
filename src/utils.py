import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список
    """
    try:
        if not Path(file_path).exists():
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return []
            data = json.loads(content)

        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции из USD или EUR в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции

    Returns:
        float: Сумма в рублях или 0.0 при ошибке
    """
    # Правильное извлечение данных из вложенной структуры
    operation_amount = transaction.get('operationAmount')

    if operation_amount is None:
        return 0.0

    amount_str = operation_amount.get('amount')
    currency_info = operation_amount.get('currency', {})
    currency_code = currency_info.get('code')

    if amount_str is None or currency_code is None:
        return 0.0

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    currency = str(currency_code).upper()

    if currency == 'RUB':
        return amount

    if currency not in ['USD', 'EUR']:
        return 0.0

    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    headers = {'api-key': API_KEY} if API_KEY else {}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return 0.0

        data = response.json()
        rub_rate = data.get('rates', {}).get('RUB')

        if rub_rate is None:
            return 0.0

        result = amount * float(rub_rate)
        return round(result, 2)

    except Exception:
        return 0.0