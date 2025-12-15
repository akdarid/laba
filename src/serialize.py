import json
from src.models import Student
import argparse


def students_to_json(students: list[Student], path: str) -> None:
    data = [student.to_dict() for student in students]  # Генератор списка: преобразуем каждый объект Student в словарь

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path: str) -> list[Student]:  # Десериализация списка студентов из JSON файла
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Загрузка и парсинг JSON данных из файла в Python

        students = []
        for item in data:
            try:
                student = Student.from_dict(item)  # Создание объекта Student из словаря
                students.append(student)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании студента из данных {item}: {e}")
                continue

        return students
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из файла {path}")
        return []


if __name__ == "__main__":  # Проверка: запущен ли скрипт напрямую (
    # Пример использования
    students = [
        Student("Иванов Иван", "2000-05-15", "SE-01", 4.5),
        Student("Петрова Анна", "2001-08-22", "SE-02", 3.8),
        Student("Сидоров Алексей", "1999-12-10", "SE-01", 4.2)
    ]

    # Сериализация
    students_to_json(students, r"C:\Users\matve\PycharmProjects\laba8\data\students_output.json")

    # Десериализация
    loaded_students = students_from_json(r"C:\Users\matve\PycharmProjects\laba8\data\students_input.json")
    for student in loaded_students:
        print(student)
