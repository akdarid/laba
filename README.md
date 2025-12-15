
# Лабораторная работа №9
## ```group.pyw```
### Конструктор
В конструкторе делаем все проверки.
### ```list()```
В методе list() с помощью next() пропускаем заголовок и из остальных строк делаем массив.
### ```add()```
В методе add() сначала создаем словарь из студента, затем просто записываем его в файл.
### ```find()```
В методе find() сначала открываем файл на чтение затем по подстроке находим нужного и выводим его данные.
### ```remove()```
В методе remove() считываем все данные затем делаем делаем массив с обновленными данными, потом открываем файл на перезапись и по новой записываем уже новые данные.
### ```update()```
В методе update() первым делаем создаем студента через метод from_dict(), таким образом мы провалидируем данные которые нам передали, после этого сразу конвертируем экземпляр в словарь и удаляем из него fio, после чего открываем файл на чтение и ищем нужного студента по фио, затем обновляем его данные и сохраняем для записи, после этого открываем файл на запись и перезаписываем обновленные данные

```python
import csv
from pathlib import Path
from lab_08.models import student 

class Group():
    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        if not self.path.exists():
            self.path.write_text("", encoding='utf-8')
        if not self.path.read_text(encoding='utf-8').split('\n')[0] == 'fio,birthdate,group,gpa':
            raise ValueError('Не корректный заголовок')
        with open(self.path, 'r', encoding='utf-8') as f:
            rd = list(csv.DictReader(f))
            [student.from_dict(st) for st in rd]

    
    def _read_all(self):
        data_text = self.path.read_text(encoding='utf-8')
        return data_text
    
    def list(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            rd = csv.reader(f)
            next(rd)
            students = list(rd)
        return students
        
    def add(self, student: student):
        with open(self.path, 'a', newline='\n', encoding='utf-8') as f:
            data_append = student.to_dict()
            wr = csv.DictWriter(f, fieldnames=list(data_append.keys()))
            wr.writerow(data_append)

    def find(self, substr: str):
        with open(self.path, 'r', encoding='utf-8') as f:
            rd = list(csv.DictReader(f))
        return [student.from_dict(r) for r in rd if substr in r['fio']]
    
    def remove(self, fio: str):
        with open(self.path, 'r', encoding='utf-8') as f:
            rd = csv.DictReader(f)
            data_new = [r for r in rd if fio not in r['fio']]
        with open(self.path, 'w', newline='', encoding='utf-8') as f:
            wr = csv.DictWriter(f, fieldnames=list(data_new[0].keys()))
            wr.writeheader()
            wr.writerows(data_new)

    def update(self, fio: str, **fields):
        data = student.from_dict({'fio': fio, **fields}).to_dict()
        data.pop('fio')
        with open(self.path, 'r', encoding='utf-8') as f:
            rd = list(csv.DictReader(f))
            for r in rd:
                if fio in r['fio']:
                    r.update(data)
                    break 
        with open(self.path, 'w', newline='', encoding='utf-8') as f:
            wr = csv.DictWriter(f, fieldnames=list(rd[0].keys()))
            wr.writeheader()
            wr.writerows(rd)
```

Тестовый csv:

```csv
fio,birthdate,group,gpa
Иванов Иван Иванович,2007-05-15,БИВТ-25-1,4.8
Петрова Мария Сергеевна,2007-03-22,БИВТ-25-2,5.0
Сидоров Алексей Петрович,2007-11-30,БИВТ-25-3,3.9
Козлова Анна Дмитриевна,2007-08-14,БИВТ-25-1,4.5
Васильев Дмитрий Андреевич,2007-01-10,БИВТ-25-2,4.2
```

### Результат
Для ```list()```

<img width="1448" height="67" alt="reslt_list" src="https://github.com/user-attachments/assets/90f2e663-396c-4f9b-8f85-2e8e42fee8ed" />

Для ```add()```
```python
print(gr.add(student('Данилов Иван Иванович', '2007-08-17', 'БИВТ-25-2', 3.8)))
```

<img width="582" height="210" alt="reslt_add" src="https://github.com/user-attachments/assets/bcb07c0a-5924-425a-a85f-66250880447c" />

Для ```find()```

```python
print(gr.find('Иванов Иван Иванович'))
```

<img width="828" height="52" alt="reslt_find" src="https://github.com/user-attachments/assets/5473e485-47ca-4689-81b8-8bddd7a50435" />

Для ```remove()```

<img width="532" height="368" alt="reslt_remove" src="https://github.com/user-attachments/assets/26e39bad-2c3f-42ed-bf3b-266a5a8aef56" />

Для ```update()```

```python
print(gr.update('Васильев Дмитрий Андреевич', **{'birthdate': '2007.06/25', 'group': 'БИВТ-25-4', 'gpa': 4.2}))
```

<img width="603" height="190" alt="reslt_updata_csv" src="https://github.com/user-attachments/assets/6ba0f374-5058-48c8-8846-59cc0f7e8345" />
