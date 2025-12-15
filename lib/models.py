from dataclasses import dataclass
from datetime import datetime
from tokenize import group

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Некорректный формат {self.birthdate} - %Y-%m-%d")
        if not (0 <= self.gpa <= 5):
            raise ValueError("Среднее значение оценки должно быть от 0 до 10")

    def age(self) -> int:
        return datetime.today() - datetime.strptime(self.birthdate, "%Y-%m-%d").year

    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return Student(fio=d["fio"], birthdate=d["birthdate"], group=d["group"], gpa=float(d["gpa"]))

    def __str__(self):
        return f"ФИО: {self.fio} дата рождения: {self.birthdate} группа: {self.group} средний балл: {self.gpa}"