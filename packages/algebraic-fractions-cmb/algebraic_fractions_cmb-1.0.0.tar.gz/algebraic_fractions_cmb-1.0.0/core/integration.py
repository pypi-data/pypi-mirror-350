"""
calculation.py

Содержит функции для интегрирования аппроксимирующих дробей с использованием метода evaluate.
"""

from typing import Any
from core.calculation import numerical_integration


def integrate_fraction(
    fraction: Any,
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """
    Интегрирует функцию, заданную методом fraction.evaluate, на отрезке [a, b].

    Аргументы:
        fraction: объект с методом evaluate (например, BernsteinFraction или ChebyshevMarkovFraction).
        a: нижняя граница интегрирования.
        b: верхняя граница интегрирования.
        n: число разбиений (по умолчанию 1000).

    Возвращает:
        Приближённую величину интеграла ∫ₐᵇ fraction(x) dx.
    """
    def local_func(x_array):
        return fraction.evaluate(x_array)

    return numerical_integration(local_func, a, b, n=n)
