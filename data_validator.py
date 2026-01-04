"""
data_validator.py
Модуль валидации данных договоров
Демонстрирует: Урок 6 (функции), Урок 3 (условия), Урок 8 (регулярки)
"""

import re
from datetime import datetime


def validate_inn(inn):
    """
    Проверка ИНН (10 или 12 цифр)
    
    Демонстрирует:
    - Урок 6: Функции
    - Урок 3: Условия (if-else)
    - Урок 2: Строки (методы isdigit, strip)
    
    Args:
        inn (str): ИНН для проверки
    
    Returns:
        tuple: (bool, str) — (валиден ли ИНН, сообщение об ошибке)
    
    Examples:
        >>> validate_inn("7701234567")
        (True, "OK")
        >>> validate_inn("123")
        (False, "ИНН должен быть 10 или 12 цифр")
    """
    # Урок 3: Условие — проверка на пустоту
    if not inn:
        return False, "ИНН не может быть пустым"
    
    # Урок 2: Метод strip() удаляет пробелы
    inn = inn.strip()
    
    # Урок 3: Условие — только цифры
    if not inn.isdigit():
        return False, "ИНН должен содержать только цифры"
    
    # Урок 3: Условие — проверка длины
    if len(inn) not in [10, 12]:
        return False, "ИНН должен быть 10 или 12 цифр"
    
    return True, "OK"


def validate_sum(sum_str):
    """
    Проверка суммы (должна быть числом > 0)
    
    Демонстрирует:
    - Урок 6: Функции
    - Урок 3: Условия
    - Урок 2: Преобразование типов (float)
    
    Args:
        sum_str (str): Сумма в виде строки
    
    Returns:
        tuple: (bool, str) — (валидна ли сумма, сообщение)
    """
    # Урок 3: Проверка на пустоту
    if not sum_str:
        return False, "Сумма не может быть пустой"
    
    try:
        # Урок 2: Преобразование строки в число
        # Заменяем запятую на точку, убираем пробелы
        amount = float(sum_str.replace(',', '.').replace(' ', ''))
        
        # Урок 3: Условие — сумма должна быть положительной
        if amount <= 0:
            return False, "Сумма должна быть больше нуля"
        
        return True, "OK"
    
    except ValueError:
        # Урок 3: Обработка ошибки — если не число
        return False, "Некорректный формат суммы (должно быть число)"


def validate_date(date_str):
    """
    Проверка даты (формат ДД.ММ.ГГГГ)
    
    Демонстрирует:
    - Урок 6: Функции
    - Урок 3: Условия
    - Урок 8: Регулярные выражения
    
    Args:
        date_str (str): Дата в виде строки
    
    Returns:
        tuple: (bool, str) — (валидна ли дата, сообщение)
    """
    # Урок 3: Проверка на пустоту
    if not date_str:
        return False, "Дата не может быть пустой"
    
    # Урок 8: Регулярное выражение — проверка формата
    # ^ — начало строки
    # \d{2} — ровно 2 цифры
    # \. — точка (экранирована)
    # $ — конец строки
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    
    # Урок 3: Условие — соответствие паттерну
    if not re.match(pattern, date_str):
        return False, "Формат даты должен быть ДД.ММ.ГГГГ (например, 03.01.2025)"
    
    # Проверка валидности даты (31.02.2025 — невалидна)
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True, "OK"
    except ValueError:
        return False, "Некорректная дата (например, 31.02 не существует)"


def validate_contract_number(number):
    """
    Проверка номера договора (не пустой)
    
    Демонстрирует:
    - Урок 6: Функции
    - Урок 3: Условия
    - Урок 2: Методы строк
    
    Args:
        number (str): Номер договора
    
    Returns:
        tuple: (bool, str) — (валиден ли номер, сообщение)
    """
    # Урок 3: Условие с методом strip()
    if not number or not number.strip():
        return False, "Номер договора не может быть пустым"
    
    return True, "OK"


# ===== ТЕСТИРОВАНИЕ =====

if __name__ == "__main__":
    print("=== Тестирование data_validator.py ===\n")
    
    # Тест 1: Валидация ИНН
    print("--- Тест 1: ИНН ---")
    test_inn_cases = [
        ("7701234567", True, "10 цифр"),
        ("770123456789", True, "12 цифр"),
        ("123", False, "слишком короткий"),
        ("abc123", False, "не цифры"),
        ("", False, "пустой"),
        ("  7701234567  ", True, "с пробелами"),
    ]
    
    for inn, expected, description in test_inn_cases:
        result, msg = validate_inn(inn)
        status = "✅" if result == expected else "❌"
        print(f"{status} ИНН '{inn}' ({description}): {msg}")
    
    # Тест 2: Валидация суммы
    print("\n--- Тест 2: Суммы ---")
    test_sum_cases = [
        ("100000", True, "целое число"),
        ("100000.50", True, "с копейками"),
        ("100,000.50", True, "с запятой"),
        ("100 000", True, "с пробелами"),
        ("0", False, "ноль"),
        ("-100", False, "отрицательное"),
        ("abc", False, "не число"),
        ("", False, "пустое"),
    ]
    
    for sum_str, expected, description in test_sum_cases:
        result, msg = validate_sum(sum_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} Сумма '{sum_str}' ({description}): {msg}")
    
    # Тест 3: Валидация даты
    print("\n--- Тест 3: Даты ---")
    test_date_cases = [
        ("03.01.2025", True, "корректная дата"),
        ("31.12.2024", True, "конец года"),
        ("29.02.2024", True, "високосный год"),
        ("31.02.2025", False, "несуществующая дата"),
        ("32.01.2025", False, "невалидный день"),
        ("01.13.2025", False, "невалидный месяц"),
        ("1.1.2025", False, "неправильный формат"),
        ("01-01-2025", False, "дефисы вместо точек"),
        ("", False, "пустая"),
    ]
    
    for date_str, expected, description in test_date_cases:
        result, msg = validate_date(date_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} Дата '{date_str}' ({description}): {msg}")
    
    # Тест 4: Номер договора
    print("\n--- Тест 4: Номер договора ---")
    test_number_cases = [
        ("123/2025", True, "нормальный номер"),
        ("TEST-001", True, "с буквами"),
        ("", False, "пустой"),
        ("   ", False, "только пробелы"),
    ]
    
    for number, expected, description in test_number_cases:
        result, msg = validate_contract_number(number)
        status = "✅" if result == expected else "❌"
        print(f"{status} Номер '{number}' ({description}): {msg}")
    
    print("\n=== Все тесты завершены ===")
