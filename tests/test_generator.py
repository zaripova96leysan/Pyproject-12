import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


# Фикстура с тестовыми данными
@pytest.fixture
def transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод другу",
            "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
        },
        {
            "id": 2,
            "description": "Покупка в магазине",
            "operationAmount": {"amount": "200", "currency": {"code": "EUR"}},
        },
        {
            "id": 3,
            "description": "Оплата услуг",
            "operationAmount": {"amount": "300", "currency": {"code": "USD"}},
        },
    ]


# ========== ТЕСТЫ ДЛЯ filter_by_currency ==========


def test_filter_by_currency_usd(transactions):
    """Фильтрация по USD."""
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_eur(transactions):
    """Фильтрация по EUR."""
    result = list(filter_by_currency(transactions, "EUR"))
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_currency_not_found(transactions):
    """Валюта не найдена."""
    result = list(filter_by_currency(transactions, "RUB"))
    assert len(result) == 0


def test_filter_by_currency_empty_list():
    """Пустой список."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


# ========== ТЕСТЫ ДЛЯ transaction_descriptions ==========


def test_transaction_descriptions(transactions):
    """Получение описаний."""
    result = list(transaction_descriptions(transactions))
    assert result == ["Перевод другу", "Покупка в магазине", "Оплата услуг"]


def test_transaction_descriptions_empty():
    """Пустой список."""
    result = list(transaction_descriptions([]))
    assert result == []


# ========== ТЕСТЫ ДЛЯ card_number_generator ==========


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (0, 2, ["0000 0000 0000 0000", "0000 0000 0000 0001"]),
        (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
    ],
)
def test_card_number_generator(start, stop, expected):
    """Генерация номеров карт."""
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_single():
    """Один номер."""
    gen = card_number_generator(42, 43)
    assert next(gen) == "0000 0000 0000 0042"
