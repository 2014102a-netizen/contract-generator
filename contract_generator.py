# contract_generator.py
# Автор: Дмитрий Сокол
# Дата: 04.01.2025
#
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
    """
    Класс для работы с договорами
    
    Демонстрирует: Урок 7 (ООП - классы, self, __init__)
    """
    
    def __init__(self, contract_type):
        """
        Создание договора
        
        Демонстрирует: Урок 7 (метод __init__)
        
        Args:
            contract_type (str): Тип договора ('подряд' или 'услуги')
        """
        self.contract_type = contract_type
        self.data = {}
    
    def fill_data(self, **kwargs):
        """
        Заполнение данных договора
        
        Демонстрирует: Урок 5 (словари), Урок 6 (**kwargs)
        
        Args:
            **kwargs: Данные в виде именованных параметров
        """
        self.data = kwargs
    
    def validate(self):
        """
        Проверка заполненности всех полей
        
        Демонстрирует: Урок 4 (циклы), Урок 3 (условия)
        
        Returns:
            tuple: (bool, str) - (валиден ли, сообщение)
        """
        for field in UNIVERSAL_FIELDS:
            if field not in self.data or not self.data[field]:
                return False, f"Поле '{field}' не заполнено"
        
        return True, "OK"
    
    def generate_txt(self):
        """
        Генерация текста договора из шаблона
        
        Демонстрирует: Урок 8 (файлы), Урок 4 (циклы), Урок 1 (строки)
        
        Returns:
            str: Готовый текст договора
        """
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
            placeholder = f'{{{{{key}}}}}'  # {{contract_number}}
            result = result.replace(placeholder, str(value))
        
        return result


# ============================================================
# Мои объяснения что и ка5к 
# ============================================================

"""
 Зачем класс?

 Класс объединяет данные и методы. Вместо разных функций 
       у меня один объект contract который хранит данные и умеет 
       генерировать договор.


 Что такое self?

 self - ссылка на конкретный объект. Когда я создаю 
       contract = Contract('подряд'), внутри методов self указывает 
       на этот contract.


 Что такое **kwargs?

 **kwargs упаковывает именованные аргументы в словарь.
       fill_data(name="ООО", inn="123") → kwargs = {'name': 'ООО', 'inn': '123'}


 Как работает замена переменных?

 В шаблоне переменные обозначены {{contract_number}}.
       Я циклом прохожу по данным и заменяю каждую переменную 
       на реальное значение: {{contract_number}} → "001"


 Зачем validate?

 Проверяет что все поля заполнены ПЕРЕД генерацией.
       Без этого можем создать неполный договор с {{переменными}}.
"""

