"""
helpers.py

Содержит утилитарные функции:
 - generate_points — генерация равномерной сетки точек.
 - measure_time — замер времени выполнения произвольной функции.
"""

import time
import numpy as np
from typing import Tuple, Any, Callable


def generate_points(
    interval: Tuple[float, float],
    num: int = 100
) -> np.ndarray:
    """
    Генерирует num равномерно распределённых точек на интервале [xmin, xmax].

    Аргументы:
        interval: кортеж (xmin, xmax).
        num: количество точек.

    Возвращает:
        Массив точек np.ndarray.
    """
    xmin, xmax = interval
    return np.linspace(xmin, xmax, num)


def measure_time(
    func: Callable,
    *args,
    **kwargs
) -> Tuple[Any, float]:
    """
    Замеряет время выполнения функции func(*args, **kwargs).

    Аргументы:
        func: вызываемая функция.
        *args: позиционные аргументы.
        **kwargs: именованные аргументы.

    Возвращает:
        Кортеж (результат выполнения, время в секундах).
    """
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed
