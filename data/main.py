import re
from utils import load_transaction
from file_reader import read_csv_transactions, read_excel_transactions
from process_bank import search_transactions, count_categories


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    if choice == '1':
        file_path = "data/transactions.json"  # измените путь, если файлы в другой папке
        try:
            transactions = load_transaction(file_path)
            print("Для обработки выбран JSON-файл.")
        except Exception as e:
            print(f"Ошибка чтения JSON: {e}")
            return
    elif choice == '2':
        file_path = "data/transactions.csv"
        try:
            transactions = read_csv_transactions(file_path)
            print("Для обработки выбран CSV-файл.")
        except Exception as e:
            print(f"Ошибка чтения CSV: {e}")
            return
    elif choice == '3':
        file_path = "data/transactions_excel.xlsx"
        try:
            transactions = read_excel_transactions(file_path)
            print("Для обработки выбран XLSX-файл.")
        except Exception as e:
            print(f"Ошибка чтения Excel: {e}")
            return
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Файл не содержит транзакций или данные повреждены.")
        return

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Ваш выбор: ").strip().upper()
        if status_input in valid_statuses:
            filtered_by_status = [t for t in transactions if t.get('state', '').upper() == status_input]
            print(f"Операции отфильтрованы по статусу \"{status_input}\"")
            break
        else:
            print(f"Статус операции \"{status_input}\" недоступен. Повторите ввод.")

    if not filtered_by_status:
        print("Не найдено ни одной транзакции с таким статусом.")
        return

    sort_choice = input("\nОтсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice in ['да', 'yes', 'д', 'y']:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = order in ['убыванию', 'desc', 'убыв']
        filtered_by_status.sort(key=lambda x: x.get('date', ''), reverse=reverse)

    rub_choice = input("\nВыводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if rub_choice in ['да', 'yes', 'д', 'y']:
        filtered_by_status = [t for t in filtered_by_status if
                              t.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB']

    search_choice = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if search_choice in ['да', 'yes', 'д', 'y']:
        search_word = input("Введите слово для поиска: ").strip()
        filtered_by_status = search_transactions(filtered_by_status, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_by_status:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_by_status)}")
        for t in filtered_by_status:
            date = t.get('date', 'Дата не указана')
            desc = t.get('description', 'Без описания')
            amount = t.get('operationAmount', {}).get('amount', '0')
            currency = t.get('operationAmount', {}).get('currency', {}).get('code', '')
            print(f"{date} {desc} Сумма: {amount} {currency}")

if __name__ == "__main__":
    main()
