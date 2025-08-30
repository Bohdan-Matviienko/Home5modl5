import re
from typing import Callable, Generator

# Число має бути відокремлене пробілами з обох боків
NUMBER_TOKEN = re.compile(r" [+-]?\d+(?:\.\d+)? ")

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Генератор знаходить усі дійсні числа у тексті,
    які відокремлені пробілами з обох боків.
    """
    for m in NUMBER_TOKEN.finditer(text):
        # приберемо пробіли навколо та перетворимо в число
        yield float(m.group().strip())

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Використовує generator_numbers для підсумовування чисел.
    """
    return sum(func(text))
