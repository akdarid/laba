import os, csv, sys

from openpyxl import Workbook

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)

    if os.path.getsize(csv_path) == 0:
        print("ValueError")
        sys.exit(1)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    with open(csv_path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            ws.append(row)


    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = max(max_length + 2, 8)
    wb.save(xlsx_path)


import csv, json, sys, os

def json_to_csv(json_path: str, csv_path: str) -> None:
    if not os.path.exists(json_path):
        print("FileNotFoundError")
    if os.path.getsize(json_path) == 0:
        print("1ValueError")
        sys.exit(1)
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        if not all(type(x) == dict for x in json_data):
            print("ValueError")
            sys.exit(1)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)

def csv_to_json(csv_path: str, json_path: str) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)
    if os.path.getsize(csv_path) == 0:
        print("3ValueError")
        sys.exit(1)
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        if not header:
            print("4ValueError")
            sys.exit(1)
        reader = csv.DictReader(csvfile)
        data = list(reader)
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)
def table(arr: list[tuple[str, int]], isTable: bool = True) -> str:
    if not arr:
        return "(нет данных)"
    s = str()
    if isTable:
        word_col_width = max(len("слово"), max(len(a[0]) for a in arr))
        freq_col_width = max(len("частота"), max(len(str(a[1])) for a in arr))
        s += f"{'слово'.ljust(word_col_width)} | {'частота'.rjust(freq_col_width)}"
        s += "\n" + "-" * word_col_width + "-+-" + "-" * freq_col_width
        for word, freq in arr:
            s += f"\n{word.ljust(word_col_width)} | {str(freq).rjust(freq_col_width)}"
        return s
    else:
        return "\n".join(f"{a[0]}: {a[1]}" for a in arr)
def stats_text(text: str, n: int = 5):
    text = text.strip()
    tokens = normalize(text)
    tokens = tokenize(tokens)
    freqs = count_freq(tokens)
    total_words = len(tokens)
    unique_words = len(freqs)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    top_n_words = sorted(freqs.items(), key=lambda x: (-x[1], x[0]))[:n]
    print(f"Топ-{n}:")
    print(table(top_n_words, True))
import re
from collections import Counter
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    if yo2e:
        translation_table = str.maketrans({
            'ё': 'е',
            'Ё': 'Е'
        })
        text = text.translate(translation_table)
    translation_table_controls = str.maketrans({
        '\t': ' ',
        '\r': ' ',
        '\n': ' ',
        '\v': ' ',
        '\f': ' '
    })
    text = text.translate(translation_table_controls)
    text = ' '.join(text.split())

    return text
def tokenize(text: str) -> list[str]:
    word = re.findall(r"[\w-]+", text)
    words = []
    for w in word:
        w = w.strip("_-")
        w = re.sub(r"-{2,}", "-", w)
        w = re.sub(r"_{2,}", "_", w)
        w = re.sub(r"[-_]{2,}", "-", w)
        if w:
            words.append(w)
    return words
def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = Counter(tokens)
    return dict(freq)
def top_n(freqs: dict[str, int], n: int) -> list[tuple[str, int]]:
    return sorted(freqs.items(), key=lambda x: (-x[1], x[0]))[:n]

