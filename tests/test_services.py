import pytest

from src.services import search_to_str



@pytest.fixture
def valid_data():
    return [{"category": "еда", "amount": 100}, {"category": "транспорт", "amount": 50}]


def test_search_to_str(valid_data):
    result = search_to_str(valid_data, "еда")
    assert isinstance(
        result, list
    ), f"Функция должна возвращать строку, но получен {type(result)}"






