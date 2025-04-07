import pytest
import json
from unittest.mock import patch

from src.views import write_json_gl

@pytest.fixture
def mock_dependencies():
    with patch("src.views.filtered_operations") as mock_filtered, \
            patch("src.views.greetings") as mock_greet, \
            patch("src.views.info_about_operations") as mock_info, \
            patch("src.views.top5_tran") as mock_top5, \
            patch("src.views.currency_rates") as mock_rates:

        mock_filtered.return_value = [
            {
                "Номер карты": "1234567890123456",
                "Сумма операции с округлением": 150.75,
                "Кэшбэк": 5.25,
                "Дата платежа": "2023-05-15",
                "Категория": "Рестораны",
                "Описание": "Поход в кафе"
            }
        ]
        mock_greet.return_value = "Доброе утро"
        mock_info.return_value = (
            ["1234567890123456"],
            [150.75],
            [5.25]
        )
        mock_top5.return_value = mock_filtered.return_value
        mock_rates.return_value = (
            [{"currency": "USD", "rate": 95.5}],
            [{"stock": "AAPL", "price": 172.5}]
        )

        yield

def test_write_json_gl(mock_dependencies):
    result = write_json_gl("2023-05-20 10:00:00")
    result_dict = json.loads(result)

    assert result_dict["greeting"] == "Доброе утро"
    assert len(result_dict["cards"]) == 1
    assert result_dict["cards"][0]["last_digits"] == "3456"
    assert result_dict["cards"][0]["total_spent"] == 150.75
    assert result_dict["cards"][0]["cashback"] == 5.25

    assert len(result_dict["top_transactions"]) == 1
    assert result_dict["top_transactions"][0]["category"] == "Рестораны"

    assert result_dict["currency_rates"][0]["currency"] == "USD"
    assert result_dict["stock_prices"][0]["stock"] == "AAPL"
