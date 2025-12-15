import re
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class student():
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        try:
            self.birthdate = re.sub(r'[\D_]', '-', self.birthdate)
            date_brth = datetime.fromisoformat(self.birthdate).date() #strptime(self.birthdate, '%Y/%m/%d').date()
        except ValueError:
            raise ValueError('Введенная дата некорректна')
        
        if date_brth > date.today():
            raise ValueError('Введенная дата еще не наступила')

        if not(0 <= self.gpa <= 5):
            raise ValueError('Введенный средний бал некорректен')
    
    def age(self) -> int:
        today = date.today()
        date_birth = datetime.fromisoformat(self.birthdate).date() #strptime(self.birthdate, '%Y/%m/%d')
        if today.month > date_birth.month:
            return today.year - date_birth.year
        elif today.month < date_birth.month:
            return today.year - date_birth.year - 1
        else:
            return today.year - date_birth.year if today.day > date_birth.day else today.year - date_birth.year - 1
                
    
    def to_dict(self) -> dict:
        student_info_dict = {
            'fio': self.fio,
            'birthdate': self.birthdate,
            'group': self.group,
            'gpa': self.gpa
        }
        return student_info_dict
    
    @classmethod
    def from_dict(cls, d: dict):
        fields = list(d.keys())
        st = cls(d[fields[0]], d[fields[1]], d[fields[2]], float(d[fields[3]]))
        return st

    def __str__(self):
        return f'ФИО: {self.fio}, группа: {self.group}, средний балл: {self.gpa}'