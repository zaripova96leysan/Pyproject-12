import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = os.getenv("EXCHANGE_API_URL", "https://api.exchangerate-api.com/v4/latest")


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из JSON-файла."""
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
    """Конвертирует сумму транзакции из USD или EUR в рубли."""

    amount = transaction.get('amount')
    currency = transaction.get('currency')


    if amount is None or currency is None:
        return 0.0


    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return 0.0


    currency = str(currency).upper()


    if currency == 'RUB':
        return amount


    if currency not in ['USD', 'EUR']:
        return 0.0


    try:
        url = f"{API_URL}/{currency}"
        headers = {}
        if API_KEY:
            headers['apikey'] = API_KEY


        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()


        data = response.json()


        rub_rate = None


        if 'rates' in data and 'RUB' in data['rates']:
            rub_rate = data['rates']['RUB']

        elif 'data' in data and 'RUB' in data['data']:
            rub_rate = data['data']['RUB']

        elif 'RUB' in data:
            rub_rate = data['RUB']


        if rub_rate is None:
            return 0.0


        try:
            rub_rate = float(rub_rate)
        except (ValueError, TypeError):
            return 0.0


        result = amount * rub_rate
        return round(result, 2)

    except (requests.RequestException, KeyError, ValueError, TypeError) as e:
        print(f"Ошибка конвертации: {e}")
        return 0.0