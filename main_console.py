# -*- coding: utf-8 -*-
"""
main_console.py
Консольная версия генератора договоров

Автор: Андрей
Дата: 04.01.2025
Демонстрирует: Урок 6 (функции), Урок 3 (условия), Урок 4 (циклы)
"""

from file_handler import save_contract, append_to_history
from data_validator import validate_inn, validate_sum, validate_date, validate_contract_number
from contract_generator import Contract

UNIVERSAL_FIELDS = [
    'contract_number',
    'contract_date',
    'customer_name',
    'customer_director',
    'customer_inn',
    'customer_kpp',
    'customer_ogrn',
    'customer_address',
    'customer_account',
    'work_description',
    'object_address',
    'duration_days',
    'price_digits',
    'price_words',
    'vat_digits',
    'vat_words'
]

FIELD_NAMES_RU = {
    'contract_number': 'Номер договора',
    'contract_date': 'Дата договора (ДД.ММ.ГГГГ)',
    'customer_name': 'Название заказчика',
    'customer_director': 'ФИО директора',
    'customer_inn': 'ИНН заказчика',
    'customer_kpp': 'КПП заказчика',
    'customer_ogrn': 'ОГРН заказчика',
    'customer_address': 'Адрес заказчика',
    'customer_account': 'Расчётный счёт',
    'work_description': 'Описание работ/услуг',
    'object_address': 'Адрес объекта',
    'duration_days': 'Срок выполнения (дней)',
    'price_digits': 'Сумма цифрами (руб)',
    'price_words': 'Сумма прописью',
    'vat_digits': 'НДС цифрами (руб)',
    'vat_words': 'НДС прописью'
}


def show_menu():
    """Показывает главное меню"""
    print("\n" + "=" * 50)
    print("    ГЕНЕРАТОР ДОГОВОРОВ")
    print("=" * 50)
    print("\n1. Создать договор подряда")
    print("2. Создать договор услуг")
    print("3. Выход")
    print()


def get_contract_data():
    """Собирает данные для договора"""
    data = {}
    
    print("\n--- Ввод данных договора ---\n")
    
    for field in UNIVERSAL_FIELDS:
        field_name_ru = FIELD_NAMES_RU[field]
        
        while True:
            value = input(f"{field_name_ru}: ").strip()
            
            if not value:
                print(" Поле не может быть пустым. Попробуйте снова.")
                continue
            
            # Валидация по типу поля
            if field == 'contract_number':
                is_valid, msg = validate_contract_number(value)
                if not is_valid:
                    print(f" Ошибка: {msg}")
                    continue
            
            elif field == 'contract_date':
                is_valid, msg = validate_date(value)
                if not is_valid:
                    print(f"⚠ Ошибка: {msg}")
                    continue
            
            elif field == 'customer_inn':
                is_valid, msg = validate_inn(value)
                if not is_valid:
                    print(f" Ошибка: {msg}")
                    continue
            
            elif field in ['price_digits', 'vat_digits']:
                is_valid, msg = validate_sum(value)
                if not is_valid:
                    print(f" Ошибка: {msg}")
                    continue
            
            data[field] = value
            break
    
    return data


def show_summary(data):
    """Показывает введённые данные для проверки"""
    print("\n" + "=" * 50)
    print("    ПРОВЕРЬТЕ ДАННЫЕ")
    print("=" * 50 + "\n")
    
    for field, value in data.items():
        field_name_ru = FIELD_NAMES_RU.get(field, field)
        print(f"{field_name_ru}: {value}")


def main():
    """Главная функция программы"""
    print("\n Добро пожаловать в Генератор Договоров!")
    
    while True:
        show_menu()
        
        choice = input("Выберите действие (1-3): ").strip()
        
        if choice == '3':
            print("\n До свидания!")
            break
        
        elif choice == '1':
            contract_type = 'подряд'
            print("\n Создание договора ПОДРЯДА")
        
        elif choice == '2':
            contract_type = 'услуги'
            print("\n Создание договора УСЛУГ")
        
        else:
            print("\n Неправильный выбор. Попробуйте снова.")
            continue
        
        # Сбор данных
        data = get_contract_data()
        
        # Показываем для проверки
        show_summary(data)
        
        # Подтверждение
        while True:
            confirm = input("\n✓ Всё правильно? (да/нет): ").strip().lower()
            
            if confirm == 'да':
                break
            elif confirm == 'нет':
                print(" Отменено. Возврат в главное меню.")
                break
            else:
                print(" Введите 'да' или 'нет'")
        
        if confirm == 'нет':
            continue
        
        print("\n Генерирую договор...")
        
        try:
            # Создаём договор через класс Contract
            contract = Contract(contract_type)
            contract.fill_data(**data)
            
            # Проверяем данные
            is_valid, msg = contract.validate()
            if not is_valid:
                print(f" Ошибка валидации: {msg}")
                continue
            
            # Генерируем текст
            text = contract.generate_txt()
            
            # Сохраняем
            filename = f"договор_{data['contract_number']}.txt"
            filepath = save_contract(text, filename)
            
            print(f"\n Договор сохранён: {filepath}")
            
            # Записываем в историю
            append_to_history(data)
            print(" Запись добавлена в историю")
            
            print("\n Готово!\n")
            
        except FileNotFoundError:
            print("\n Ошибка: Не найден файл шаблона!")
            print("Проверьте что папка templates/ существует и содержит:")
            print("  - договор_подряда.txt")
            print("  - договор_услуг.txt\n")
            
        except Exception as e:
            print(f"\n Ошибка при создании договора: {e}\n")


if __name__ == "__main__":
    main()
