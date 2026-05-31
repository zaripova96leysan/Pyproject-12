import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


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
    # 1. Извлечение данных из словаря
    amount = transaction.get('amount')
    currency = transaction.get('currency')

    if amount is None or currency is None:
        return 0.0

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return 0.0

    currency = str(currency).upper()

    # 2. Возврат значения для RUB
    if currency == 'RUB':
        return amount

    # Конвертируем только USD и EUR
    if currency not in ['USD', 'EUR']:
        return 0.0

    # 3. Получаем API ключ
    API_KEY = os.getenv('EXCHANGE_API_KEY')

    # 4. Правильный URL запроса
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    # 5. Передача API-ключа в заголовках
    headers = {
        'api-key': API_KEY if API_KEY else '',
        'Authorization': f'Bearer {API_KEY}' if API_KEY else ''
    }

    # 6. Обращение к внешнему API
    try:
        response = requests.get(url, headers=headers, timeout=10)

        # 7. Извлечение значения из ответа API
        data = response.json()
        rub_rate = data.get('rates', {}).get('RUB')

        if rub_rate is None:
            return 0.0

        rub_rate = float(rub_rate)

        # 8. Возврат float значения
        result = amount * rub_rate
        return round(result, 2)

    except Exception:
        return 0.0
