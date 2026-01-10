# -*- coding: utf-8 -*-
# main_gui.py
# Графический интерфейс генератора договоров
import tkinter as tk
from tkinter import messagebox, ttk
from contract_generator import Contract
from file_handler import save_contract, append_to_history
from data_validator import validate_inn, validate_date, validate_sum, validate_contract_number


class ContractApp:
    """Главный класс приложения с GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор Договоров - ООО Альянс")
        self.root.geometry("600x500")
        
        # Данные договора
        self.contract_data = {}
        self.contract_type = None
        
        # Создаём главное меню
        self.create_main_menu()
    
    def create_main_menu(self):
        """Главное меню программы"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title = tk.Label(
            self.root,
            text="ГЕНЕРАТОР ДОГОВОРОВ",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=30)
        
        subtitle = tk.Label(
            self.root,
            text="ООО «Альянс»",
            font=("Arial", 12)
        )
        subtitle.pack(pady=10)
        
        # Кнопки выбора типа договора
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=40)
        
        btn_podryad = tk.Button(
            btn_frame,
            text="Договор ПОДРЯДА",
            font=("Arial", 12),
            width=20,
            height=2,
            command=lambda: self.start_contract('подряд')
        )
        btn_podryad.pack(pady=10)
        
        btn_uslugi = tk.Button(
            btn_frame,
            text="Договор УСЛУГ",
            font=("Arial", 12),
            width=20,
            height=2,
            command=lambda: self.start_contract('услуги')
        )
        btn_uslugi.pack(pady=10)
        
        # Кнопка выхода
        btn_exit = tk.Button(
            self.root,
            text="Выход",
            font=("Arial", 10),
            command=self.root.quit
        )
        btn_exit.pack(pady=20)
    
    def start_contract(self, contract_type):
        """Начало создания договора"""
        self.contract_type = contract_type
        self.contract_data = {}
        self.open_step1()
    
    def open_step1(self):
        """Шаг 1: Основные данные договора"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title_text = f"Договор {self.contract_type.upper()}"
        title = tk.Label(
            self.root,
            text=title_text,
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)
        
        step_label = tk.Label(
            self.root,
            text="Шаг 1 из 3: Основные данные",
            font=("Arial", 10)
        )
        step_label.pack(pady=5)
        
        # Форма
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Поля ввода
        fields = [
            ('Номер договора:', 'contract_number'),
            ('Дата договора (ДД.ММ.ГГГГ):', 'contract_date'),
        ]
        
        self.step1_entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 10))
            label.grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            
            self.step1_entries[field_name] = entry
        
        # Кнопки навигации
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        btn_back = tk.Button(
            btn_frame,
            text="← Назад",
            font=("Arial", 10),
            command=self.create_main_menu
        )
        btn_back.pack(side=tk.LEFT, padx=10)
        
        btn_next = tk.Button(
            btn_frame,
            text="Далее →",
            font=("Arial", 10),
            command=self.save_step1_and_continue
        )
        btn_next.pack(side=tk.LEFT, padx=10)
    
    def save_step1_and_continue(self):
        """Сохранение данных шага 1 и переход к шагу 2"""
        # Собираем данные
        for field_name, entry in self.step1_entries.items():
            value = entry.get().strip()
            
            if not value:
                messagebox.showerror("Ошибка", f"Поле '{field_name}' не заполнено!")
                return
            
            # Валидация номера
            if field_name == 'contract_number':
                is_valid, msg = validate_contract_number(value)
                if not is_valid:
                    messagebox.showerror("Ошибка", f"Номер договора: {msg}")
                    return
            
            # Валидация даты
            if field_name == 'contract_date':
                is_valid, msg = validate_date(value)
                if not is_valid:
                    messagebox.showerror("Ошибка", f"Дата: {msg}")
                    return
            
            self.contract_data[field_name] = value
        
        self.open_step2()
    
    def open_step2(self):
        """Шаг 2: Данные заказчика"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title = tk.Label(
            self.root,
            text=f"Договор {self.contract_type.upper()}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)
        
        step_label = tk.Label(
            self.root,
            text="Шаг 2 из 3: Данные заказчика",
            font=("Arial", 10)
        )
        step_label.pack(pady=5)
        
        # Создаём canvas для прокрутки
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Поля ввода
        fields = [
            ('Название заказчика:', 'customer_name'),
            ('ФИО директора:', 'customer_director'),
            ('ИНН:', 'customer_inn'),
            ('КПП:', 'customer_kpp'),
            ('ОГРН:', 'customer_ogrn'),
            ('Адрес:', 'customer_address'),
            ('Расчётный счёт:', 'customer_account'),
        ]
        
        self.step2_entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(scrollable_frame, text=label_text, font=("Arial", 10))
            label.grid(row=i, column=0, sticky='w', pady=5, padx=20)
            
            entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=35)
            entry.grid(row=i, column=1, pady=5, padx=10)
            
            self.step2_entries[field_name] = entry
        
        canvas.pack(side="left", fill="both", expand=True, padx=40, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки навигации
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        btn_back = tk.Button(
            btn_frame,
            text="← Назад",
            font=("Arial", 10),
            command=self.open_step1
        )
        btn_back.pack(side=tk.LEFT, padx=10)
        
        btn_next = tk.Button(
            btn_frame,
            text="Далее →",
            font=("Arial", 10),
            command=self.save_step2_and_continue
        )
        btn_next.pack(side=tk.LEFT, padx=10)
    
    def save_step2_and_continue(self):
        """Сохранение данных шага 2 и переход к шагу 3"""
        # Собираем данные
        for field_name, entry in self.step2_entries.items():
            value = entry.get().strip()
            
            if not value:
                messagebox.showerror("Ошибка", f"Поле '{field_name}' не заполнено!")
                return
            
            # Валидация ИНН
            if field_name == 'customer_inn':
                is_valid, msg = validate_inn(value)
                if not is_valid:
                    messagebox.showerror("Ошибка", f"ИНН: {msg}")
                    return
            
            self.contract_data[field_name] = value
        
        self.open_step3()
    
    def open_step3(self):
        """Шаг 3: Данные о работах и стоимости"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title = tk.Label(
            self.root,
            text=f"Договор {self.contract_type.upper()}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)
        
        step_label = tk.Label(
            self.root,
            text="Шаг 3 из 3: Работы и стоимость",
            font=("Arial", 10)
        )
        step_label.pack(pady=5)
        
        # Создаём canvas для прокрутки
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Поля ввода
        fields = [
            ('Описание работ/услуг:', 'work_description'),
            ('Адрес объекта:', 'object_address'),
            ('Срок выполнения (дней):', 'duration_days'),
            ('Сумма цифрами (руб):', 'price_digits'),
            ('Сумма прописью:', 'price_words'),
            ('НДС цифрами (руб):', 'vat_digits'),
            ('НДС прописью:', 'vat_words'),
        ]
        
        self.step3_entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(scrollable_frame, text=label_text, font=("Arial", 10))
            label.grid(row=i, column=0, sticky='w', pady=5, padx=20)
            
            entry = tk.Entry(scrollable_frame, font=("Arial", 10), width=35)
            entry.grid(row=i, column=1, pady=5, padx=10)
            
            self.step3_entries[field_name] = entry
        
        canvas.pack(side="left", fill="both", expand=True, padx=40, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки навигации
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        btn_back = tk.Button(
            btn_frame,
            text="← Назад",
            font=("Arial", 10),
            command=self.open_step2
        )
        btn_back.pack(side=tk.LEFT, padx=10)
        
        btn_create = tk.Button(
            btn_frame,
            text="✓ Создать договор",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.create_contract
        )
        btn_create.pack(side=tk.LEFT, padx=10)
    
    def create_contract(self):
        """Создание договора - финальный шаг"""
        # Собираем данные шага 3
        for field_name, entry in self.step3_entries.items():
            value = entry.get().strip()
            
            if not value:
                messagebox.showerror("Ошибка", f"Поле '{field_name}' не заполнено!")
                return
            
            # Валидация сумм
            if field_name in ['price_digits', 'vat_digits']:
                is_valid, msg = validate_sum(value)
                if not is_valid:
                    messagebox.showerror("Ошибка", f"Сумма: {msg}")
                    return
            
            self.contract_data[field_name] = value
        
        try:
            # Создаём договор через класс Contract
            contract = Contract(self.contract_type)
            contract.fill_data(**self.contract_data)
            
            # Валидация
            is_valid, msg = contract.validate()
            if not is_valid:
                messagebox.showerror("Ошибка валидации", msg)
                return
            
            # Генерация текста
            text = contract.generate_txt()
            
            # Сохранение
            filename = f"договор_{self.contract_data['contract_number']}.txt"
            filepath = save_contract(text, filename)
            
            # История
            append_to_history(self.contract_data)
            
            # Готово
            messagebox.showinfo(
                "Готово!",
                f"Договор успешно создан!\n\nСохранён: {filepath}"
            )
            
            # Возврат в главное меню
            self.create_main_menu()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать договор:\n{e}")


def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = ContractApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
