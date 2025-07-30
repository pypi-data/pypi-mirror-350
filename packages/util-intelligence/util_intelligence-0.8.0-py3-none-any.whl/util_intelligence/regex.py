import re
from io import StringIO
from typing import List

import json_repair
import numpy as np
import pandas as pd


def parse_format(
    text: str, type_hint="json"
):  # Renamed 'type' to 'type_hint' to avoid conflict with built-in
    # Try to find a block like ```type\nCONTENT```
    pattern_typed_block = (
        rf"```{type_hint}\s*\n(.*?)(?:\n```|\Z)"  # Matches until \n``` or end of string
    )
    match = re.search(pattern_typed_block, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: try to find any block like ```\nCONTENT```
    pattern_any_block = r"```\s*\n(.*?)(?:\n```|\Z)"
    match = re.search(pattern_any_block, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: if text STARTS with ```type\n (e.g. from a direct LLM response with no preamble)
    pattern_starts_with_typed = rf"^\s*```{type_hint}\s*\n(.*?)(?:\n```|\Z)"
    match = re.search(pattern_starts_with_typed, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: if text STARTS with ```\n
    pattern_starts_with_any = r"^\s*```\s*\n(.*?)(?:\n```|\Z)"
    match = re.search(pattern_starts_with_any, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no ``` block is found at all, but there's a preamble ending with ```<type>
    # This is closer to your original logic if closing ``` is missing
    pattern_opening_only = rf"```{type_hint}\s*\n(.*)"
    match = re.search(pattern_opening_only, text, re.DOTALL)
    if match:
        # This might grab too much if there's trailing text after the intended CSV
        # and no closing ```. Careful with this one.
        return match.group(1).strip()

    return text.strip()  # Default to returning the stripped original text if no patterns match well


def parse_json(text: str):
    code_text = parse_format(text, type_hint="json")
    try:
        return json_repair.loads(code_text)
    except Exception:
        return None


def parse_csv2json(text: str):
    code_text = parse_format(text, type_hint="csv")
    try:
        df = pd.read_csv(StringIO(code_text), dtype=str, escapechar="\\").astype(str)
        df = df.replace("nan", "")
        return df.to_dict(orient="records")
    except Exception:
        return None


def replace_multiple_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def replace_multiple_blank_lines(text: str) -> str:
    return re.sub(r"\n+", "\n\n", text)


def create_space_insensitive_pattern(term: str) -> str:
    # Insert \s* between each character of the term
    return "".join(f"{char}\\s*" for char in term)


def exists(pattern: str, text: str):
    m = re.search(pattern, text)
    return m is not None


def exists_ignore_spaces(pattern: str, text: str) -> bool:
    """
    if pattern is '明细单', then '明 细 单' will also be matched
    """
    return bool(
        re.compile(
            create_space_insensitive_pattern(pattern),
        ).search(text)
    )


def match(pattern: str | List[str], text):
    if isinstance(pattern, str):
        m = re.match(pattern, text)
        return m is not None
    else:
        for x in pattern:
            if match(x, text):
                return True
        return False


def match_any(patterns, text):
    return np.any([match(x, text) for x in patterns])


def match_any_text(pattern, texts):
    return [x for x in texts if match(pattern, x)]


def process_quotes(text: str):
    return text.replace("“", '"').replace("”", '"')


def find_all_capital_index(lines: list, index: int, maxlines: int):
    for k in range(index, index + maxlines):
        if lines[k].upper() == lines[k]:
            return k
    return -1


def remove_leading_bullet(text: str):
    parts = text.split(" ")
    may_be_bullet = parts[0]
    if is_bullet(may_be_bullet):
        if 2 <= len(parts) and parts[1] == ".":
            return " ".join(parts[2:])
        else:
            return " ".join(parts[1:])
    else:
        return text


def is_bullet(token: str):
    if token.count("I") == len(token):
        return True
    return token.replace(".", "").isdigit()


def is_int(token: str):
    try:
        int(token)
        return True
    except ValueError:
        return False


def exists_any(pattens, text):
    return np.any([exists(x, text) for x in pattens])


def fix_breaking_sentences(lines):
    fixed_sentences = []
    sentence = ""
    for line in lines:
        sentence = sentence + " " + line
        if line[-1] in [".", "!", "?", ":", ";"] and line[-2] == " ":
            fixed_sentences.append(sentence)
            sentence = ""
    if not sentence:
        fixed_sentences.append(sentence)
    return fixed_sentences


def fix_breaking_paragraph(lines, index, maxlines=100):
    for end_index in range(index, index + maxlines):
        if lines[end_index].endswith("."):
            break
    return " ".join(lines[index : end_index + 1])


def startswith(text: str, patterns: list):
    for pattern in patterns:
        if exists("^" + pattern, text):
            return True
    return False


def retrieve(pattern: str, text: str, *args, **kwargs):
    m = re.search(pattern, text, *args, **kwargs)
    if m is None:
        return None
    start, end = m.regs[-1]
    return text[start:end]


def retrieve_groups(pattern: str, text: str, *args, **kwargs):
    m = re.search(pattern, text, *args, **kwargs)
    if m is None:
        return None
    else:
        return [g for g in m.groups() if g is not None]


def retrieve_multiple(pattern: str, text: str, *args, **kwargs):
    return re.findall(pattern, text, *args, **kwargs)


def retrieve_date(text: str):
    month_list = "|".join(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
    )
    pattern = r"(?:" + month_list + r") \d{1,2} , \d{4}"
    return retrieve(pattern, text)


def process_spaces(text: str, spaces=[" ", "\t", "\r", "\n"]):
    """
    # '你好 世界。 Hello world! '=>'你好世界。Hello world! '
    """
    result = ""
    for i, ch in enumerate(text):
        if ch in spaces:
            if i > 0 and (0x4E00 < ord(text[i - 1]) < 0x9FFF or text[i - 1] in spaces):
                continue
        result += ch
    return result


def process_duplicate_chars(text: str) -> str:
    """
    '随随附附单单证证' => '随附单证'
    """
    result = []
    i = 0
    while i < len(text):
        result.append(text[i])
        if i + 1 < len(text) and text[i] == text[i + 1]:
            i += 1
        i += 1
    return "".join(result)


def retrieve_text(json: dict):
    lines = []
    for value in json.values():
        if isinstance(value, str):
            lines.append(value)
        elif isinstance(value, dict):
            lines += retrieve_text(value)
    return lines


def is_number(text: str):
    try:
        float(text.replace(",", ""))
        return True
    except Exception:
        return False


def is_currency(text: str):
    return startswith(text.upper(), ["US$", "RMB"])


def is_percentage(text: str):
    return text.endswith("%")


def is_cjk(ch):
    cp = ord(ch)
    if (
        (cp >= 0x4E00 and cp <= 0x9FFF)
        or (cp >= 0x3400 and cp <= 0x4DBF)  #
        or (cp >= 0x20000 and cp <= 0x2A6DF)  #
        or (cp >= 0x2A700 and cp <= 0x2B73F)  #
        or (cp >= 0x2B740 and cp <= 0x2B81F)  #
        or (cp >= 0x2B820 and cp <= 0x2CEAF)  #
        or (cp >= 0xF900 and cp <= 0xFAFF)
        or (cp >= 0x2F800 and cp <= 0x2FA1F)  #
    ):  #
        return True
    return False


def join_texts(texts):
    result = ""
    for x in texts:
        if len(x) == 0:
            continue
        if result and not is_cjk(result[-1]):
            result += " "
        result += x
    return result


class MatchMachine:
    def __init__(self, name: str, matcher):
        self.name = name
        self.matcher = matcher
        self.state = "seeking"
        self.data = None

    def transfer(self, lines: list, index: int):
        if self.state != "seeking":
            return
        data = self.matcher(lines, index)
        # once data received, the machine will no longer seek for more occurrence.
        if data is not None:
            self.state = "finished"
            self.data = data


class AggregateMachine:
    def __init__(self, name: str, aggregator):
        self.name = name
        self.aggregator = aggregator
        self.data = None

    def transfer(self, lines: list, index: int):
        self.data = self.aggregator(lines, index, self.data)
