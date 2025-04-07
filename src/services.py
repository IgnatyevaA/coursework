import re


def search_to_str(list_tran: list[dict], str_search: str) -> list[dict]:
    """
    Функция для поиска всех транзакций с введенной категорией
    """
    pattern = re.compile(str_search, re.IGNORECASE)
    operations = [
        op
        for op in list_tran
        if pattern.search(str(op.get("Категория", "")))
        or pattern.search(str(op.get("Описание", "")))
    ]
    return operations
