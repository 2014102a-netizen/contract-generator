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
