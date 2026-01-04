# Модуль 2 - Генератор договоров

from pathlib import Path


# Список всех полей договора
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

# Соответствие типов договоров и файлов шаблонов
TEMPLATE_MAP = {
    'подряд': 'договор_подряда.txt',
    'услуги': 'договор_услуг.txt'
}


class Contract:
    """
    Класс для работы с договорами
    
    ООП - класс
    """
    
    def __init__(self, contract_type):
        """
        Создание экземпляра договора
        
        Args:
            contract_type (str): Тип договора ('подряд' или 'услуги')
        """
        self.contract_type = contract_type
        self.data = {}
        self.template = None
    
    def fill_data(self, **kwargs):
        """
        Заполнение данных договора
        
        Args:
            **kwargs: Данные в виде именованных параметров
        
        словари
        """
        self.data = kwargs
    
    def validate(self):
        """
        Проверка заполненности всех полей
        
        Returns:
            tuple: (bool, str) - (валиден ли, сообщение об ошибке)
        
        условия и циклы
        """
        for field in UNIVERSAL_FIELDS:
            if field not in self.data or not self.data[field]:
                return False, f"Поле {field} не заполнено"
        
        return True, "OK"
    
    def generate_txt(self):
        """
        Генерация текста договора
        
        Returns:
            str: Готовый текст договора
        
        файлы и циклы
        """
        # Получаем имя файла шаблона
        template_file = TEMPLATE_MAP.get(self.contract_type)
        
        if not template_file:
            raise ValueError(f"Неизвестный тип договора: {self.contract_type}")
        
        # Читаем шаблон
        template_path = Path('templates') / template_file
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Заменяем переменные на данные
        result = template
        
        for key, value in self.data.items():
            placeholder = f'{{{{{key}}}}}'
            result = result.replace(placeholder, value)
        
        return result


# Тестирование модуля
if __name__ == "__main__":
    print("=== Тестирование contract_generator.py ===\n")
    
    # Тестовые данные
    test_data = {
        'contract_number': 'TEST-001',
        'contract_date': '04.01.2025',
        'customer_name': 'ООО "Тестовая Компания"',
        'customer_director': 'Иванов Иван Иванович',
        'customer_inn': '7701234567',
        'customer_kpp': '770101001',
        'customer_ogrn': '1234567890123',
        'customer_address': 'г. Спб, ул. Итмошная, д. 1',
        'customer_account': '40702810100000000001',
        'work_description': 'Тестовые работы',
        'object_address': 'г. Спб, ул. Объектная, д. 2',
        'duration_days': '30',
        'price_digits': '100000',
        'price_words': 'Сто тысяч',
        'vat_digits': '20000',
        'vat_words': 'Двадцать тысяч'
    }
    
    print("Тест 1: Создание договора подряда")
    contract = Contract('подряд')
    contract.fill_data(**test_data)
    
    is_valid, msg = contract.validate()
    if is_valid:
        print("Валидация пройдена")
    else:
        print(f"Ошибка валидации: {msg}")
    
    try:
        text = contract.generate_txt()
        print(f"Договор сгенерирован, длина: {len(text)} символов")
        print(f"\nПервые 200 символов:\n{text[:200]}...")
    except Exception as e:
        print(f"Ошибка генерации: {e}")
    
    print("\n=== Тест завершён ===")