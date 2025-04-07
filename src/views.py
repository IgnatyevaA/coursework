import json
from collections import defaultdict
import pandas as pd

from src.utils import (
    filtered_operations,
    greetings,
    info_about_operations,
    top5_tran,
    currency_rates,
)

def write_json_gl(time_setting: str):
    """
    Функция возращает json, отфильтрованные транзакции от введеной даты до начала месяца
    с информацией о картах (траты, кэшбек), топ 5 транзакций и курс валют и акций
    """
    operations = filtered_operations(time_setting)
    greet = greetings()
    card_numbers, amounts, cashback = info_about_operations(operations)
    top_transactions = top5_tran(operations)
    currency_data, stock_data = currency_rates("user_settings.json")

    card_data = defaultdict(lambda: {"total_spent": 0, "cashback": 0})

    for card, amount, cash in zip(card_numbers, amounts, cashback):
        last_digits = card[-4:] if pd.notna(card) and len(str(card)) >= 4 else "----"
        card_data[last_digits]["total_spent"] += amount if pd.notna(amount) else 0
        card_data[last_digits]["cashback"] += cash if pd.notna(cash) else 0

    cards_info = [
        {
            "last_digits": card,
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2),
        }
        for card, data in card_data.items()
    ]

    top_transactions_info = [
        {
            "date": op.get("Дата платежа", ""),
            "amount": op.get("Сумма операции с округлением", 0),
            "category": op.get("Категория", ""),
            "description": op.get("Описание", ""),
        }
        for op in top_transactions
    ]

    information_json = {
        "greeting": greet,
        "cards": cards_info,
        "top_transactions": top_transactions_info,
        "currency_rates": currency_data,
        "stock_prices": stock_data,
    }

    return json.dumps(information_json, ensure_ascii=False, indent=4)