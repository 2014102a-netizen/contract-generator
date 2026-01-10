# contract_generator.py
# Класс Contract для генерации договоров
# Все обязательные поля договора
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

# Соответствие типов договоров и шаблонов
TEMPLATE_MAP = {
    'подряд': 'templates/договор_подряда.txt',
    'услуги': 'templates/договор_услуг.txt'
}


class Contract:
    """Класс для работы с договорами"""
    
    def __init__(self, contract_type):
        """Создание договора"""
        self.contract_type = contract_type
        self.data = {}
    
    def fill_data(self, **kwargs):
        """Заполнение данных договора"""
        self.data = kwargs
    
    def validate(self):
        """Проверка заполненности всех полей"""
        for field in UNIVERSAL_FIELDS:
            if field not in self.data or not self.data[field]:
                return False, f"Поле '{field}' не заполнено"
        
        return True, "OK"
    
    def generate_txt(self):
        """Генерация текста договора из шаблона"""
        # Получаем путь к шаблону
        template_path = TEMPLATE_MAP.get(self.contract_type)
        
        if not template_path:
            raise ValueError(f"Неизвестный тип договора: {self.contract_type}")
        
        # Читаем шаблон
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Заменяем переменные на данные
        result = template
        
        for key, value in self.data.items():
            placeholder = f'{{{{{key}}}}}'
            result = result.replace(placeholder, str(value))
        
        return result
