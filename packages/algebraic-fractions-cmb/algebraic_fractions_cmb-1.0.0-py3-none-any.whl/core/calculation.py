"""
approximation.py

Содержит базовые численные методы:
 - solve_least_squares — решение задачи МНК.
 - numerical_integration — численное интегрирование (метод трапеций).
 - numerical_derivative — приближённое вычисление производной (метод центральной разности).
"""

import numpy as np
from typing import Callable


def solve_least_squares(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Решает задачу МНК A * x = b, минимизируя ||A * x - b||^2.

    Аргументы:
        A: матрица формы (m, n).
        b: вектор правой части формы (m,).

    Возвращает:
        Решение x в виде np.ndarray формы (n,).
    """
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    return x


def numerical_integration(
    func: Callable[[np.ndarray], np.ndarray],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """
    Численное интегрирование методом трапеций.

    Аргументы:
        func: функция, принимающая np.ndarray и возвращающая np.ndarray.
        a: нижняя граница интегрирования.
        b: верхняя граница интегрирования.
        n: число разбиений (чем больше, тем точнее).

    Возвращает:
        Приближённое значение интеграла ∫ₐᵇ func(x) dx.
    """
    x = np.linspace(a, b, n + 1)
    y = func(x)
    h = (b - a) / n
    return (h / 2) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1])


def numerical_derivative(
    func: Callable[[float], float],
    x: float,
    h: float = 1e-5
) -> float:
    """
    Вычисляет приближённую производную функции в точке x методом центральной разности:
        f'(x) ≈ (f(x + h) - f(x - h)) / (2 * h)

    Аргументы:
        func: функция f(x).
        x: точка вычисления производной.
        h: малый шаг (по умолчанию 1e-5).

    Возвращает:
        Приближённое значение производной в точке x.
    """
    return (func(x + h) - func(x - h)) / (2.0 * h)
