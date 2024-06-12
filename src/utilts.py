import json
from datetime import datetime


def mask_card_number(card_number):
    """
    Маскировка номера карты.
    """
    masked_number = card_number[:4] + " " + card_number[4:6] + "** " + "*" * 4 + " " + card_number[-4:]
    return masked_number


def mask_account_number(account_number):
    """
    Маскировка номера счета.
    """
    masked_number = "**" + account_number[-4:]
    return masked_number


def format_date(date_str):
    """
    Форматирование даты.
    """
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")


def format_operation(operation):
    """
    Форматирование операции.
    """
    date = format_date(operation["date"])
    description = operation["description"]

    from_ = operation.get("from", "")
    to = operation["to"]

    if from_ and (from_.startswith("Visa") or from_.startswith("Maestro")):
        from_name = " ".join(from_.split()[:-1])
        from_masked = mask_card_number(from_.split()[-1])
        from_formatted = f"{from_name} {from_masked}"
    elif from_:
        from_formatted = mask_account_number(from_)
    else:
        from_formatted = ""

    to_name = "Счет"
    to_masked = mask_account_number(to)

    amount = operation["operationAmount"]["amount"]
    currency_name = operation["operationAmount"]["currency"]["name"]

    if from_formatted:
        formatted_operation = f"{date} {description}\n{from_formatted} -> {to_name} {to_masked}\n{amount} {currency_name}\n"
    else:
        formatted_operation = f"{date} {description}\n{to_name} {to_masked}\n{amount} {currency_name}\n"

    return formatted_operation


def get_last_operations(file_path, n=5):
    """
    Получение последних операций.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    executed_operations = [op for op in data if op.get("state") == "EXECUTED"]
    sorted_operations = sorted(executed_operations, key=lambda x: x["date"], reverse=True)[:n]

    formatted_operations = [format_operation(op) for op in sorted_operations]
    return formatted_operations
