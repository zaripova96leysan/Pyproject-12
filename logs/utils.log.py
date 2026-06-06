import json
import logging
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем API ключ
API_KEY = os.getenv("EXCHANGE_API_KEY")

# Настройка логгера
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", mode='w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_transaction(file_path: str) -> list:
    logger.info(f"Загрузка транзакций из {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций")
                return data
            logger.warning("Файл не содержит списка транзакций")
            return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}", exc_info=True)
        return []


def convert_to_rub(transaction: dict) -> float:
    logger.info("Вызвана convert_to_rub")
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount")
    currency_dict = operation_amount.get("currency", {})
    currency_code = currency_dict.get("code")

    if amount_str is None or currency_code is None:
        logger.warning("Отсутствует сумма или валюта в транзакции")
        return 0.0

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        logger.error("Сумма транзакции не является числом", exc_info=True)
        return 0.0

    if currency_code == "RUB":
        logger.info(f"Сумма в рублях: {amount} RUB")
        return amount

    if currency_code not in ("USD", "EUR"):
        logger.warning(f"Валюта {currency_code} не поддерживается для конвертации")
        return 0.0

    if not API_KEY:
        logger.error("Отсутствует API_KEY для конвертации валюты")
        return 0.0

    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": API_KEY}
        params = {"base": currency_code, "symbols": "RUB"}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            logger.error(f"Ошибка API: статус {response.status_code}")
            return 0.0

        data = response.json()
        rub_rate = data.get("rates", {}).get("RUB")

        if rub_rate is None:
            logger.error("Не удалось получить курс RUB из ответа API")
            return 0.0

        result = amount * rub_rate
        logger.info(f"Конвертация {amount} {currency_code} -> {round(result, 2)} RUB")
        return round(result, 2)

    except (requests.RequestException, KeyError, ValueError, TypeError) as e:
        logger.error(f"Исключение при запросе к API: {e}", exc_info=True)
        return 0.0
