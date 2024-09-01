import re


def clean_number(value: str) -> float:
    return float(''.join(filter(lambda x: x.isdigit() or x == '.', value)))


def extract_neighborhood(text: str) -> str:
    match = re.search(r"in (.+)$", text)
    return match.group(1) if match else text


def extract_property_type(text: str) -> str:
    match = re.search(r"(.+?) in", text)
    return match.group(1) if match else text

