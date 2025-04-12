import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from src.utils import get_date_range, filtered_operations, greetings, info_about_operations, top5_tran, currency_rates, sorted_by_month

# Фикстуры для генерации тестовых данных
@pytest.fixture
def sample_operations():
    return [
        {"Дата операции": "01.04.2023", "Номер карты": "1234", "Сумма операции с округлением": 100, "Кэшбэк": 1},
        {"Дата операции": "15.04.2023", "Номер карты": "5678", "Сумма операции с округлением": 200, "Кэшбэк": 2},
        {"Дата операции": "20.04.2023", "Номер карты": "9101", "Сумма операции с округлением": 150, "Кэшбэк": 1.5},
    ]

@pytest.fixture
def sample_transactions():
    data = {
        "Дата платежа": ["01.04.2023", "15.04.2023", "20.04.2023"],
        "Сумма операции с округлением": [100, 200, 150],
    }
    return pd.DataFrame(data)

# Тесты для функции get_date_range
@pytest.mark.parametrize("date_input, expected_output", [
    ("2023-04-15 12:00:00", ("01.04.2023", "15.04.2023")),
    ("2023-01-01 00:00:00", ("01.01.2023", "01.01.2023")),
])
def test_get_date_range(date_input, expected_output):
    assert get_date_range(date_input) == expected_output

# Тесты для функции filtered_operations
@patch("utils.operations_df", new=[])
def test_filtered_operations_empty():
    assert filtered_operations("2023-04-15 12:00:00") == []

@patch("utils.operations_df", new=[
    {"Дата операции": "01.04.2023", "Номер карты": "1234", "Сумма операции с округлением": 100, "Кэшбэк": 1},
    {"Дата операции": "15.04.2023", "Номер карты": "5678", "Сумма операции с округлением": 200, "Кэшбэк": 2},
])
def test_filtered_operations():
    result = filtered_operations("2023-04-15 12:00:00")
    assert len(result) == 2
    assert result[0]["Номер карты"] == "1234"
    assert result[1]["Номер карты"] == "5678"

# Тесты для функции greetings
@pytest.mark.parametrize("hour, expected_greeting", [
    (6, "Доброе утро"),
    (12, "Добрый день"),
    (18, "Добрый вечер"),
    (23, "Доброй ночи"),
])
def test_greetings(hour, expected_greeting):
    with patch("utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = MagicMock(hour=hour)
        assert greetings() == expected_greeting

# Тесты для функции info_about_operations
def test_info_about_operations(sample_operations):
    cards, amounts, cashbacks = info_about_operations(sample_operations)
    assert cards == ["1234", "5678", "9101"]
    assert amounts == [100, 200, 150]
    assert cashbacks == [1, 2, 1.5]

# Тесты для функции top5_tran
def test_top5_tran(sample_operations):
    result = top5_tran(sample_operations)
    assert len(result) == 3
    assert result[0]["Сумма операции с округлением"] == 200
    assert result[1]["Сумма операции с округлением"] == 150
    assert result[2]["Сумма операции с округлением"] == 100

# Тесты для функции currency_rates
@patch("utils.requests.get")
def test_currency_rates(mock_get):
    mock_response_currency = MagicMock()
    mock_response_currency.json.return_value = {
        "quotes": {
            "USDRUB": 75.0,
            "EURRUB": 85.0,
        }
    }
    mock_response_stocks = MagicMock()
    mock_response_stocks.json.return_value = {
        "data": [
            {"symbol": "AAPL", "close": "150.0"},
            {"symbol": "GOOGL", "close": "2750.0"},
        ]
    }
    mock_get.side_effect = [mock_response_currency, mock_response_stocks]

    currency_info, stocks_info = currency_rates("path/to/settings.json")
    assert currency_info == [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 85.0}]
    assert stocks_info == [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOGL", "price": 2750.0}]

# Тесты для функции sorted_by_month
def test_sorted_by_month(sample_transactions):
    result = sorted_by_month(sample_transactions, "2023-04-20 12:00:00")
    assert len(result) == 3
    assert result["Сумма операции с округлением"].tolist() == [100, 200, 150]

def test_sorted_by_month_default_date(sample_transactions):
    with patch("utils.datetime") as mock_datetime:
        mock_datetime.today.return_value = datetime(2023, 4, 20)
        result = sorted_by_month(sample_transactions)
        assert len(result) == 3
        assert result["Сумма операции с округлением"].tolist() == [100, 200, 150]
