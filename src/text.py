import re
from collections import Counter


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    if yo2e:
        translation_table = str.maketrans(
            {
                "ё": "е",
                "Ё": "Е",
            }
        )
        text = text.translate(translation_table)
    translation_table_controls = str.maketrans(
        {
            "\t": " ",
            "\r": " ",
            "\n": " ",
            "\v": " ",
            "\f": " ",
        }
    )
    text = text.translate(translation_table_controls)
    text = " ".join(text.split())

    return text


def tokenize(
    text: str,
) -> list[str]:
    word = re.findall(
        r"[\w-]+",
        text,
    )
    words = []
    for w in word:
        w = w.strip("_-")
        w = re.sub(
            r"-{2,}",
            "-",
            w,
        )
        w = re.sub(
            r"_{2,}",
            "_",
            w,
        )
        w = re.sub(
            r"[-_]{2,}",
            "-",
            w,
        )
        if w:
            words.append(w)
    return words


def count_freq(
    tokens: list[str],
) -> dict[str, int]:
    freq = Counter(tokens)
    return dict(freq)


def top_n(
    freqs: dict[
        str,
        int,
    ],
    n: int,
) -> list[tuple[str, int,]]:
    return sorted(
        freqs.items(),
        key=lambda x: (
            -x[1],
            x[0],
        ),
    )[:n]
