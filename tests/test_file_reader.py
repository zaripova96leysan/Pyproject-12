import pytest
from unittest.mock import patch
import pandas as pd
from file_reader import read_csv_transactions, read_excel_transactions


@patch('pandas.read_csv')
def test_read_csv_transactions(mock_read_csv):
    # Создаём фейковый DataFrame, который вернёт mock
    fake_df = pd.DataFrame([
        {'id': 1, 'amount': 100.5, 'date': '2023-01-01'},
        {'id': 2, 'amount': 200.0, 'date': '2023-01-02'}
    ])
    mock_read_csv.return_value = fake_df

    result = read_csv_transactions('dummy.csv')

    expected = [
        {'id': 1, 'amount': 100.5, 'date': '2023-01-01'},
        {'id': 2, 'amount': 200.0, 'date': '2023-01-02'}
    ]
    assert result == expected
    mock_read_csv.assert_called_once_with('dummy.csv')


@patch('pandas.read_excel')
def test_read_excel_transactions(mock_read_excel):
    fake_df = pd.DataFrame([
        {'id': 10, 'amount': 99.9},
        {'id': 20, 'amount': 199.9}
    ])
    mock_read_excel.return_value = fake_df

    result = read_excel_transactions('dummy.xlsx')

    expected = [{'id': 10, 'amount': 99.9}, {'id': 20, 'amount': 199.9}]
    assert result == expected
    mock_read_excel.assert_called_once_with('dummy.xlsx')