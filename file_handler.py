"""
file_handler.py
Модуль для сохранения договоров

Автор: Андрей
Дата: 03.01.2025
Демонстрирует: Урок 8 (работа с файлами)
"""

import os
import csv


def save_contract(text, filename):
    """
    Сохранение договора в папку output/
    
    Args:
        text (str): Текст договора
        filename (str): Имя файла
    
    Returns:
        str: Путь к сохранённому файлу
    """
    # Создаём папку output если её нет
    output_dir = 'output'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Полный путь к файлу
    filepath = f'{output_dir}/{filename}'
    
    # Сохраняем
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return filepath


def append_to_history(contract_data):
    """
    Добавление записи в историю (history.csv)
    
    Args:
        contract_data (dict): Данные договора
    """
    filepath = 'history.csv'
    
    # Если файла нет - создаём с заголовками
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Номер', 'Дата', 'Заказчик', 'Сумма'])
    
    # Добавляем данные
    with open(filepath, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            contract_data.get('contract_number', ''),
            contract_data.get('contract_date', ''),
            contract_data.get('customer_name', ''),
            contract_data.get('price_digits', '')
        ])
