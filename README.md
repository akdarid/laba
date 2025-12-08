# Лабораторная работа №8
## models.py
```python
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __str__(self):
        return f'Obj Student. fio: {self.fio}, birthdate: {self.birthdate}, group: {self.group}, gpa: {self.gpa}'
    
    def __post_init__(self):
        if isinstance(self.gpa, str) or self.gpa < 0 or self.gpa > 5:
            raise ValueError('Invalid GPA-score')
        try:
            self._date_of_birth = datetime.strptime(self.birthdate, '%Y-%m-%d')
        except:
            raise ValueError('Invalid date format')
    
    @property
    def age(self) -> any:
        return date.today().year - self._date_of_birth.year
    
    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa
        }
    
    @classmethod
    def from_dict(cls, d: dict):
        return Student(d["fio"], d["birthdate"], d["group"], d["gpa"])

```
## Задание B - CSV → XLSX
```python
import os
import csv
import sys
from pathlib import Path

from openpyxl import Workbook #из библиотеки openpyx1 импортирует только класс Workbook для создаия Excel файлов

def check_file_type(file_path: str, valid_types: tuple) -> bool: #функция для проверки типа файла по расширению

    return Path(file_path).suffix.lower() in valid_types


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None: #функция конвертанции CSV в XLSX
    if not os.path.exists(csv_path): #если не существует файл по указанному пути, то
        raise FileNotFoundError #выводит сообщение об ошибке
    if not check_file_type(csv_path, ('.csv',)): #проверка расширения входящего файла (должен быть .csv)
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")

    if not check_file_type(xlsx_path, ('.xlsx',)):  #проверка расширения выходящего файла (должен быть .xlsx)
        raise ValueError(f"Выходной файл '{xlsx_path}' не является XLSX.")

    if os.path.getsize(csv_path) == 0: #получает размер в байтах и проверяет не равен ли он 0 (пустой файл)
        raise ValueError

    wb = Workbook() #создаем новую Excel книгу
    ws = wb.active #берем первый лист
    ws.title = "Sheet1" #переменовываем лист в Sheet1

    with open(csv_path, "r", encoding="utf-8") as csv_file: #безопасно открывае файл для прочтения(автомвтически закрывает после использовния #csv_path - путь к файлу
        reader = csv.reader(csv_file) #создает объект для чтения CSV файла
        for row in reader: #перебирает каждую строку в CSV файле, row - переменная, содержащая данные одной строки(как список)
            ws.append(row) #добавляет строку данных в Excel лист

#Настройка ширины колонок
    for column_cells in ws.columns: #перебирает содержания ячейки одной колонки и возвращает все колонки листа
        max_length = 0 #создает переменную для хранения максимальной длины теста в колонке
        column_letter = column_cells[0].column_letter #присваивает букву колонки
        for cell in column_cells: #перебирает все ячейки в текущей колонке
            if cell.value: #проверяет есть ли значение в ячейки(не пустая)
                max_length = max(max_length, len(str(cell.value))) #обновляет длину строкиб сравнивая прошлое значение с настоящим
        ws.column_dimensions[column_letter].width = max(max_length + 2, 8) #обращается к настройкам ширины конкретной колонки, устанавливает ширину колонки, максимальная длина + 2 символа для отступа, 8- выбирает большее значение между расчитанной шириной и минимальной шириной 8
    wb.save(xlsx_path) #сохраняет Excel книгу по указанному пути
csv_to_xlsx(r"/Users/matvejtetevin/laba/src/date/samples/cities.csv", r"/Users/matvejtetevin/laba/src/date/out/people.xlsx")
```  