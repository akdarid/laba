import csv
import os
from pathlib import Path
from lib.models import Student
class Group:
    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def _read_all(self):
        with self.path.open("r", encoding= "utf-8") as f:
            r = csv.DictReader(f)
            if r.fieldnames != ["fio","birthdate","group","gpa"]:
                raise ValueError("Некорректный формат заголовка")
            return [row for row in r]

    def list(self) -> list[Student]:
        return [Student.from_dict(s) for s in self._read_all()]

    def find(self, substr: str):
        return [r for r in self.list() if substr in r.fio]

    def add(self, student:Student):
        emptyFile = os.path.getsize(self.path) == 0
        with self.path.open("a", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["fio","birthdate","group","gpa"])
            if emptyFile:
                w.writeheader()
            w.writerow(student.to_dict())
    def remove(self, fio: str):
        studs = self._read_all()
        if any(f for f in studs if f["fio"] == fio):
            with self.path.open('w', encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["fio","birthdate","group","gpa"])
                w.writeheader()
                w.writerows([f for f in studs if f["fio"] != fio])

    def update(self, fio: str, **fields):
        if set(fields.keys()) <= { "fio","birthdate","group","gpa" }:
            studs = self._read_all()
            if any(v := tuple(((i,f) for i,f in enumerate(studs) if f["fio"] == fio))):
                for i, k in v:
                    studs[i].update(k)
            with self.path.open("w", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["fio","birthdate","group","gpa"])
                w.writeheader()
                w.writerows(studs)

    def stats(self):
        res = {}
        studs = self.list()
        sgpa = [s.gpa for s in studs]
        sgroup = [s.group for s in studs]

        res["count"] = len(studs)
        res["min_gpa"], res["max_gpa"] = min(sgpa), max(sgpa)
        res["avg_gpa"] = round(sum(sgpa) / res["count"], 1)
        res["groups"] = { g : sgroup.count(g) for g in set(sgroup) }
        res["top_5_students"] = list(sorted(studs, key=lambda x: (-x.gpa, x.fio.split()[0])))[:5]

        return res