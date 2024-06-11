import json
from datetime import datetime
import pytest
from main import mask_card_number, mask_account_number, format_date, format_operation, get_last_operations

# Фикстура для создания временного файла с данными для тестирования
@pytest.fixture
def mock_data(tmpdir):
    # Создаем тестовые данные
    data = [
        {"date": "2024-06-10T08:30:00", "description": "Payment", "from": "Visa **** 1234", "to": "1234567890",
         "operationAmount": {"amount": 100, "currency": {"name": "USD"}}, "state": "EXECUTED"},
        {"date": "2024-06-09T12:00:00", "description": "Transfer", "from": "", "to": "0987654321",
         "operationAmount": {"amount": 200, "currency": {"name": "EUR"}}, "state": "EXECUTED"},
        {"date": "2024-06-08T15:45:00", "description": "Purchase", "from": "Maestro ** 9876", "to": "0987654321",
         "operationAmount": {"amount": 150, "currency": {"name": "GBP"}}, "state": "EXECUTED"}
    ]
    # Создаем временный файл JSON с тестовыми данными
    file_path = tmpdir.join("test_operations.json")
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path

# Тесты для функции mask_card_number
def test_mask_card_number():
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert mask_card_number("5555666677778888") == "5555 66** **** 8888"

# Тесты для функции mask_account_number
def test_mask_account_number():
    assert mask_account_number("1234567890") == "**7890"
    assert mask_account_number("9876543210") == "**3210"

# Тесты для функции format_date
def test_format_date():
    assert format_date("2024-06-10T08:30:00") == "10.06.2024"

# Тесты для функции format_operation
def test_format_operation():
    # Создаем тестовую операцию
    operation = {
        "date": "2024-06-10T08:30:00",
        "description": "Payment",
        "from": "Visa **** 1234",
        "to": "1234567890",
        "operationAmount": {"amount": 100, "currency": {"name": "USD"}}
    }
    # Проверяем форматирование операции
    assert format_operation(operation) == "10.06.2024 Payment\nVisa **** 1234 ** **** 1234 -> Счет **7890\n100 USD\n"

# Тест для функции get_last_operations
def test_get_last_operations(mock_data):
    # Получаем последние операции из временного файла
    last_operations = get_last_operations(mock_data, n=2)
    # Проверяем, что количество полученных операций соответствует ожидаемому
    assert len(last_operations) == 2
    # Проверяем, что операции отсортированы по дате в убывающем порядке
    assert last_operations[0].startswith("10.06.2024")
    assert last_operations[1].startswith("09.06.2024")

if __name__ == "__main__":
    pytest.main()
