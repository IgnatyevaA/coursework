import pytest


@pytest.fixture
def sample_transactions():
    return [
        {"category": "food", "amount": 100, "date": "2018-04-01 00:00:00"},
        {"category": "transport", "amount": 50, "date": "2018-04-01 00:00:00"},
    ]