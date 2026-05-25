Проект М

## Описание:
Проект М - это приложение для виджета банковских операций клиента.

## Установка
Клонируйте репозиторий:
```
git clone https://github.com/zaripova96leysan/pyProject6.git
```
Перейдите в директорию проекта
```
cd pyProject6
```
Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:
1. Перейдите на страницу в вашем веб-браузере.
2. Создайте модуль, который будет содержать новые функции обработки данных
3. Напишите функцию, которая принимает список словарей

## Документация
Для получения дополнительной информации, обратитесь к документации.

## Лицензия:
Этот проект лицензирован по лицензии MIT

## Тестирование

Для запуска тестов выполните команду:
```
pytest
```
Процент покрытия тестами - более 80%. Отчет о покрытии находится в папке 

## Модуль generators

Примеры использования:

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Фильтрация по валюте
transactions = [
    {"operationAmount": {"currency": {"code": "USD"}}},
    {"operationAmount": {"currency": {"code": "EUR"}}},
]
usd = list(filter_by_currency(transactions, "USD"))

# Описания транзакций
descriptions = list(transaction_descriptions(transactions))

# Номера карт
cards = list(card_number_generator(1, 5))
# ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003', '0000 0000 0000 0004']

## Модуль decorators 

Декоратор `log` для логирования работы функций.

### Использование

```python
from src.decorators import log

# Логирование в консоль
@log()
def add(a, b):
    return a + b

# Логирование в файл
@log(filename="mylog.txt")
def multiply(a, b):
    return a * b