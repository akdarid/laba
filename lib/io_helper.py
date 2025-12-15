import csv, os.path, sys, enum, lib.constants
from lib.constants import PROJECT_DIR


def read_text(path: str, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        content = f.read()
    return content


def write_csv(
    rows: list[tuple | list], path: str, header: tuple[str, ...] | None = None
):
    with open(path, "w", encoding="utf-8") as f:
        w = csv.writer(f)
        if header:
            w.writerow(header)
        rowsl = -1 if not rows else len(rows[0])
        if rowsl == -1:
            return
        elif any(len(x) != rowsl for x in rows):
            raise ValueError()
        w.writerows(rows)


def ensure_parent_dir(path: str):
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    os.makedirs(path, exist_ok=True)


class ConvertTypes(enum.Enum):
    CSV_TO_JSON = (1,)
    JSON_TO_CSV = (2,)
    CSV_TO_XLSX = 3


def check_path(read: str, write: str, t: ConvertTypes):
    if not os.path.isfile(read) and not os.path.isfile((read := PROJECT_DIR + read)):
        raise FileNotFoundError("Файл не найден")
    if not os.path.exists(os.path.basename(write)):
        try:
            ensure_parent_dir(write)
        except PermissionError:
            write = PROJECT_DIR + write
            ensure_parent_dir(write)
    if not os.path.getsize(read):
        raise ValueError("Файл пуст")
    rT, wT = read.split(".")[-1], write.split(".")[-1]
    match t:
        case ConvertTypes.CSV_TO_JSON:
            if not (rT == "csv" and wT == "json"):
                raise ValueError("Некорректоный формат файла csv/json")
        case ConvertTypes.JSON_TO_CSV:
            if not (rT == "json" and wT == "csv"):
                raise ValueError("Некорректоный формат файла json/csv")
        case ConvertTypes.CSV_TO_XLSX:
            if not (rT == "csv" and wT == "xlsx"):
                raise ValueError("Некорректоный формат файла csv/xlsx")
    return read, write


def check_path_in(read: str):
    if not os.path.isfile(read) and not os.path.isfile((read := PROJECT_DIR + read)):
        raise FileNotFoundError()
    if not os.path.getsize(read):
        raise ValueError()
    return read