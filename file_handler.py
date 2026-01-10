# file_handler.py
# Сохранение договоров и истории

import os
import csv


def save_contract(text, filename):
    """Сохранение договора в папку output/"""
    output_dir = 'output'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = f'{output_dir}/{filename}'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return filepath


def append_to_history(contract_data):
    """Добавление записи в историю (history.csv)"""
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
