from typing import Callable, Dict

def caching_fibonacci() -> Callable[[int], int]:
    """
    Повертає функцію fibonacci(n), яка обчислює n-те число Фібоначчі,
    використовуючи рекурсію та кеш (замикання).
    """
    cache: Dict[int, int] = {0: 0, 1: 1}  # базові випадки в кеші одразу

    def fibonacci(n: int) -> int:
        """
        Обчислює n-те число Фібоначчі.
        - Для n <= 0 повертає 0 (узгоджено з умовою).
        - Використовує кеш для уникнення повторних обчислень.
        """
        if not isinstance(n, int):
            raise TypeError("Аргумент n має бути цілим числом")
        if n <= 0:
            return 0
        if n in cache:
            return cache[n]
        # Рекурсивне обчислення з мемоізацією
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
