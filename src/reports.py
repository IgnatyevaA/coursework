import functools
from typing import Optional

import pandas as pd

from src.utils import sorted_by_month


def save_report(filename):
    """
    Декоратор для записи возвращений функции в файл с форматом jsonl
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_json(filename, orient="records", lines=True, force_ascii=False)

            return result

        return wrapper

    return decorator


DAYS_RU = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье'
}

@save_report("data/reports.jsonl")
def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Функция принимает Dataframe и дату(если не передается берет дату сегодня), считает
    средние траты за день за 3 месяца от введеной даты,
    возвращает Dataframe с колонами  'Дата платежа', 'Средняя трата'
    """
    filtered_data = sorted_by_month(transactions, date)
    result = (
        filtered_data.groupby("Дата платежа", as_index=False)[
    "Сумма операции с округлением"
        ]
        .mean()
        .rename(columns={"Сумма операции с округлением": "Средняя трата"})
    )
    result["Дата платежа"] = pd.to_datetime(
    result["Дата платежа"], errors="coerce", dayfirst=True)
    result["Дата платежа"] = result["Дата платежа"].dt.strftime("%Y-%m-%d")
    result["Средняя трата"] = result["Средняя трата"].round(2)
    result["День недели"] = result["Дата платежа"].apply(
        lambda x: DAYS_RU[pd.to_datetime(x).weekday()]
    )
    result = result[["Дата платежа", "День недели", "Средняя трата"]]
    return result.iloc[::-1].reset_index(drop=True)

# @save_report("data/reports.jsonl")
# def spending_by_category(
#     transactions: pd.DataFrame, category: str, date: Optional[str] = None
# ) -> pd.DataFrame:
#     """
#     Функция принимает Dataframe, категорию и дату(если не передается берет дату сегодня)
#     возвращает Dataframe с колонами 'Категория', 'Дата платежа', 'Сумма операции с округлением'
#     за 3 месяца от введенной даты
#     """
#     filtered_data = sorted_by_month(transactions, date)
#     filtered_data = filtered_data[(filtered_data["Категория"] == category)]
#     filtered_data["Дата платежа"] = pd.to_datetime(
#         filtered_data["Дата платежа"], errors="coerce", dayfirst=True
#     )
#     filtered_data["Дата платежа"] = filtered_data["Дата платежа"].dt.strftime(
#         "%Y-%m-%d"
#     )
#     return filtered_data[
#         ["Категория", "Дата платежа", "Сумма операции с округлением"]
#     ].reset_index(drop=True)
