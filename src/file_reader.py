import pandas as pd

def read_csv_transactions(file_path: str) -> list[dict]:
    """Считывает финансовые транзакции из CSV-файла и возвращает список словарей."""
    df = pd.read_csv(file_path)
    # Заменяем NaN на None для корректного преобразования (опционально)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient='records')


def read_excel_transactions(file_path: str) -> list[dict]:
    """
       Считывает финансовые транзакции из Excel-файла и возвращает список словарей.
    """
    df = pd.read_excel(file_path)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient='records')
