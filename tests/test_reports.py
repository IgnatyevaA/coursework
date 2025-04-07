import pandas as pd
import pytest

from src.reports import spending_by_weekday

df = pd.read_excel("data/operations.xlsx")


@pytest.fixture
def valid_datetime():
    return "2018-04-04 12:00:00"


def test_spending_by_weekday(valid_datetime):
    result = spending_by_weekday(df, valid_datetime)
    assert isinstance(
        result, pd.DataFrame
    ), f"Функция должна возвращать DataFrame, но получен {type(result)}"
    assert not result.empty, "DataFrame не должен быть пустым"