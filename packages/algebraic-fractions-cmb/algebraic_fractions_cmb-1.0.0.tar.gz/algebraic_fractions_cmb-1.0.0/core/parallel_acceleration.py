"""
parallel_acceleration.py

Содержит функции для параллельного ускорения вычислений.
Например, функция polynomial_powers_parallel генерирует матрицу степенных функций с использованием Numba.
"""

import numpy as np
from numba import njit, prange


@njit(parallel=True)
def polynomial_powers_parallel(x_values: np.ndarray, degree: int) -> np.ndarray:
    """
    Генерирует матрицу A формы (N, degree + 1), где A[i, k] = (x_values[i])^k,
    с использованием параллельных циклов Numba.

    Аргументы:
        x_values: массив точек, форма (N,).
        degree: максимальная степень полинома.

    Возвращает:
        Массив A формы (N, degree + 1), содержащий значения x^k для каждой точки x.
    """
    N = x_values.shape[0]
    A = np.zeros((N, degree + 1), dtype=np.float64)

    for i in prange(N):
        xi = x_values[i]
        value = 1.0
        A[i, 0] = value
        for k in range(1, degree + 1):
            value *= xi
            A[i, k] = value

    return A
