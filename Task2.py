import re
from typing import Callable, Generator

NUMBER_TOKEN = re.compile(r'(?<!\S)[+-]?\d+(?:\.\d+)?(?!\S)')
# Пояснення шаблону:
# (?<!\S)  — ліворуч або пробіл/початок рядка
# [+-]?    — необов'язковий знак
# \d+      — ціла частина
# (?:\.\d+)? — необов'язкова дробова частина
# (?!\S)   — праворуч або пробіл/кінець рядка
# Таким чином число "відокремлене пробілами з обох боків" (або на краях рядка).

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Повертає генератор дійсних чисел, відокремлених пробілами у тексті.
    Кожне знайдене число перетворюється на float і віддається через yield.
    """
    for m in NUMBER_TOKEN.finditer(text):
        yield float(m.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Використовує переданий генератор чисел (func) для підсумовування
    всіх дійсних чисел у тексті та повертає загальну суму.
    """
    return sum(func(text))
