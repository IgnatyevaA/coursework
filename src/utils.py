import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional


load_dotenv()
API_KEY_CUR_USD = os.getenv("API_KEY_CUR_USD")
API_KEY_POS = os.getenv("API_KEY_STOCK")


df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def get_date_range(date: str) -> tuple[str, str]:
    """Возвращает даты первый день месяца до введеной даты в формате DD-MM-YYYY"""
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_month = date_obj.replace(day=1)
    return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")


def filtered_operations(time: str) -> list[dict]:
    """Сортирует транзакции в зависимости от функции get_date_range"""
    start_date, end_date = get_date_range(time)
    start_date = pd.to_datetime(start_date, dayfirst=True)
    end_date = pd.to_datetime(end_date, dayfirst=True)
    filtered_op = [
        op
        for op in operations_df
        if start_date <= pd.to_datetime(op["Дата операции"], dayfirst=True) <= end_date
    ]
    return filtered_op


def greetings() -> str:
    """Возвращает привествие в зависимости от времени"""
    time_now = datetime.now().hour
    if 5 <= time_now < 12:
        greeting = "Доброе утро"
    elif 12 <= time_now < 18:
        greeting = "Добрый день"
    elif 18 <= time_now < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting


def info_about_operations(operations: list[dict]) -> tuple[list, list, list]:
    """Возвращает кортеж с информацией о карте"""
    information_cards = []
    information_amount = []
    information_cashback = []

    for op in operations:
        card_number = op.get("Номер карты", "Неизвестно")
        amount = op.get("Сумма операции с округлением", 0)
        cashback = op.get("Кэшбэк", 0)

        information_cards.append(card_number)
        information_amount.append(amount)
        information_cashback.append(cashback)

    return (
        information_cards,
        information_amount,
        information_cashback,
    )


def top5_tran(operations: list[dict]) -> list[dict]:
    """Возвращает топ 5 транзакций по сумме платежа"""
    top_transactions = sorted(
        operations, key=lambda x: x["Сумма операции с округлением"], reverse=True
    )
    return top_transactions[:5]


def currency_rates(user_settings: str) -> tuple[list, list]:
    """Возвращает информацию о курсах валют и акций использую API"""
    currency_info = []
    stocks_info = []
    with open(user_settings, encoding="utf-8") as file:
        settings = json.load(file)

    currencies = ",".join(settings["user_currencies"])
    url_currency = f"http://api.currencylayer.com/live?access_key={API_KEY_CUR_USD}&currencies={currencies}"

    response_currency = requests.get(url_currency)
    data_currency = response_currency.json()
    if "quotes" in data_currency:
        for currency in settings["user_currencies"]:
            key = f"{currency}RUB"  # USDRUB
            if key in data_currency["quotes"]:
                currency_info.append(
                    {
                        "currency": currency,
                        "rate": round(data_currency["quotes"][key], 2),
                    }
                )

    stocks = ",".join(settings["user_stocks"])
    url_stocks = f"http://api.marketstack.com/v1/eod/latest?access_key={API_KEY_POS}&symbols={stocks}"
    response_stocks = requests.get(url_stocks)
    data_stocks = response_stocks.json()

    if "data" in data_stocks:
        for stock in data_stocks["data"]:
            stocks_info.append(
                {"stock": stock["symbol"], "price": float(stock["close"])}
            )

    return currency_info, stocks_info


def sorted_by_month(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    """Сортирует датафрейм от введенной даты и до трех месяцев до нее"""
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_date = end_date - timedelta(days=90)
    transactions.loc[:, "Дата платежа"] = pd.to_datetime(
        transactions["Дата платежа"], errors="coerce", dayfirst=True
    )

    filtered_data = transactions[
        (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= end_date)
    ]

    return filtered_data