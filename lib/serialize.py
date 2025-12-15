from os import write
from pathlib import Path
from lib.models import Student
import json
from src.lib.io_helper import check_path_in, read_text

def students_to_json(students:list[Student], path: Path):
    data = [s.to_dict() for s in students]
    res = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(res)

def students_from_json(path: Path) -> list[Student]:
    if not path.exists():
        raise FileNotFoundError("Файл не существует")
    with open(path) as f:
        d = json.load(f)
    return [Student.from_dict(s) for s in d]