# data_validator.py
# Проверка введённых данных

import re
from datetime import datetime


def validate_inn(inn):
    """Проверка ИНН (10 или 12 цифр)"""
    if not inn:
        return False, "ИНН не может быть пустым"
    
    inn = inn.strip()
    
    if not inn.isdigit():
        return False, "ИНН должен содержать только цифры"
    
    if len(inn) not in [10, 12]:
        return False, "ИНН должен быть 10 или 12 цифр"
    
    return True, "OK"


def validate_sum(sum_str):
    """Проверка суммы (должна быть числом > 0)"""
    if not sum_str:
        return False, "Сумма не может быть пустой"
    
    try:
        amount = float(sum_str.replace(',', '.').replace(' ', ''))
        
        if amount <= 0:
            return False, "Сумма должна быть больше нуля"
        
        return True, "OK"
    except ValueError:
        return False, "Некорректный формат суммы"


def validate_date(date_str):
    """Проверка даты (формат ДД.ММ.ГГГГ)"""
    if not date_str:
        return False, "Дата не может быть пустой"
    
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    
    if not re.match(pattern, date_str):
        return False, "Формат даты должен быть ДД.ММ.ГГГГ"
    
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True, "OK"
    except ValueError:
        return False, "Некорректная дата"


def validate_contract_number(number):
    """Проверка номера договора (не пустой)"""
    if not number or not number.strip():
        return False, "Номер договора не может быть пустым"
    
    return True, "OK"
