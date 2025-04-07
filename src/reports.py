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

    result["Средняя трата"] = result["Средняя трата"].round(2)

    return result.iloc[::-1].reset_index(drop=True)
