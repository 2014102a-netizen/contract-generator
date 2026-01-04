"""
file_handler.py
Модуль для работы с файлами договоров

Автор: Андрей
Дата: 03.01.2025
Демонстрирует: Урок 8 (работа с файлами), Урок 6 (функции)
"""

import csv
from pathlib import Path


def read_template(filename):
    """
    Чтение шаблона договора из папки templates/
    
    Args:
        filename (str): Имя файла шаблона
    
    Returns:
        str: Содержимое шаблона
    
    Raises:
        FileNotFoundError: Если шаблон не найден
    """
    filepath = Path('templates') / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Шаблон не найден: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_contract(text, filename):
    """
    Сохранение готового договора в папку output/
    
    Args:
        text (str): Текст договора
        filename (str): Имя файла для сохранения
    
    Returns:
        str: Полный путь к сохранённому файлу
    """
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return str(filepath)


def append_to_history(contract_data):
    """
    Добавление записи в файл истории (history.csv)
    
    Args:
        contract_data (dict): Словарь с данными договора
    """
    filepath = Path('history.csv')
    
    if not filepath.exists():
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Номер', 'Дата', 'Заказчик', 'Сумма'])
    
    with open(filepath, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            contract_data.get('contract_number', ''),
            contract_data.get('contract_date', ''),
            contract_data.get('customer_name', ''),
            contract_data.get('price_digits', '')
        ])


if __name__ == "__main__":
    print("=== Тестирование file_handler.py ===\n")
    
    print("Тест 1: Сохранение договора")
    test_text = """ДОГОВОР ПОДРЯДА № TEST-001

г. Санкт-Петербург                    03.01.2025

ТЕСТОВЫЙ договор для проверки работы модуля file_handler.
"""
    
    try:
        path = save_contract(test_text, 'test_договор.txt')
        print(f"Успешно сохранено: {path}\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    
    print("Тест 2: Запись в историю")
    test_data = {
        'contract_number': 'TEST-001',
        'contract_date': '03.01.2025',
        'customer_name': 'ООО "Тестовая компания"',
        'price_digits': '100000.00'
    }
    
    try:
        append_to_history(test_data)
        print("Запись добавлена в history.csv\n")
        
        if Path('history.csv').exists():
            print("Файл history.csv существует\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    
    print("Тест 3: Чтение шаблона")
    try:
        template = read_template('договор_подряда.txt')
        print(f"Шаблон прочитан, длина: {len(template)} символов\n")
    except FileNotFoundError as e:
        print(f" {e}")
        print("   Это нормально — ещё не созданы шаблоны\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    
    print("=== Тесты завершены ===")
    print("\nСозданные файлы:")
    print("  - output/test_договор.txt")
    print("  - history.csv")