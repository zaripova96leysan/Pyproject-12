import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY", "")
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
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB').upper()

    if currency == 'RUB':
        return float(amount)

    if currency not in ['USD', 'EUR']:
        return 0.0

    try:
        url = f"{API_URL}/{currency}"
        params = {'apikey': API_KEY} if API_KEY else {}

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        rates = response.json().get('rates', {})
        rub_rate = rates.get('RUB')

        if rub_rate:
            return round(float(amount) * rub_rate, 2)
        return 0.0
    except Exception:
        return 0.0
