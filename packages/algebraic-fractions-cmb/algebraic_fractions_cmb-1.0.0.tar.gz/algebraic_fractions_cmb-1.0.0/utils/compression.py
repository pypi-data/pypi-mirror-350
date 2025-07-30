"""
compression.py

Модуль для сжатия 1D и 2D данных (например, сигналов, изображений) посредством аппроксимации
с использованием ChebyshevMarkovFraction или BernsteinFraction.
Все аппроксимации осуществляются в масштабе [-1, 1] для обеспечения стабильности.
"""

import numpy as np
from typing import Tuple, Any, List

from chebyshev_markov.chebyshev_markov import ChebyshevMarkovFraction
from bernstein.bernstein import BernsteinFraction


def compress_signal_1d(
    signal: np.ndarray,
    x: np.ndarray = None,
    method: str = 'chebyshev',
    deg_num: int = 3,
    deg_den: int = 3
) -> Tuple[Any, Tuple[float, float]]:
    """
    Сжимает 1D-сигнал, используя рациональную аппроксимацию выбранного типа.

    Функция масштабирует координаты сигнала в интервал [-1, 1] и использует
    линейную интерполяцию значений, устраняя резкие скачки.

    Аргументы:
        signal: одномерный массив значений сигнала.
        x: координаты сигнала (если None, используется np.arange).
        method: 'chebyshev' или 'bernstein'.
        deg_num: степень числителя.
        deg_den: степень знаменателя.

    Возвращает:
        (fraction, interval) — аппроксимирующая дробь и интервал [-1, 1].
    """
    N = len(signal)
    if x is None:
        x = np.arange(N)
    xmin, xmax = x[0], x[-1]

    def scaled_to_original(u: float) -> float:
        return (u + 1) * 0.5 * (xmax - xmin) + xmin

    def func(u: float) -> float:
        real_coord = scaled_to_original(u)
        return np.interp(real_coord, x, signal)

    interval_scaled = (-1.0, 1.0)

    if method.lower() == 'chebyshev':
        frac = ChebyshevMarkovFraction.approximate(
            func=func,
            interval=interval_scaled,
            deg_num=deg_num,
            deg_den=deg_den,
            kind='T'
        )
    else:
        frac = BernsteinFraction.approximate(
            func=func,
            interval=interval_scaled,
            deg_num=deg_num,
            deg_den=deg_den
        )

    return frac, interval_scaled


def decompress_signal_1d(
    fraction: Any,
    interval: Tuple[float, float],
    length: int
) -> np.ndarray:
    """
    Восстанавливает 1D-сигнал из аппроксимирующей дроби на интервале [-1, 1].

    Аргументы:
        fraction: объект с методом evaluate.
        interval: интервал восстановления (обычно [-1, 1]).
        length: длина выходного сигнала.

    Возвращает:
        Восстановленный 1D-сигнал.
    """
    u_new = np.linspace(interval[0], interval[1], length)
    return fraction.evaluate(u_new)


def compress_image_2d(
    image: np.ndarray,
    method: str = 'chebyshev',
    deg_num: int = 3,
    deg_den: int = 3
) -> Tuple[List[Tuple[Any, Tuple[float, float]]], Tuple[int, int]]:
    """
    Сжимает 2D-данные (изображение) построчно, применяя аппроксимацию к каждой строке.

    Аргументы:
        image: массив формы (H, W).
        method: метод аппроксимации ('chebyshev' или 'bernstein').
        deg_num: степень числителя.
        deg_den: степень знаменателя.

    Возвращает:
        (fractions, size), где fractions — список (fraction, interval) по строкам,
        а size — кортеж (H, W) исходного изображения.
    """
    H, W = image.shape
    fractions = []

    for h in range(H):
        row = image[h, :]
        frac, inter = compress_signal_1d(
            row,
            x=np.arange(W),
            method=method,
            deg_num=deg_num,
            deg_den=deg_den
        )
        fractions.append((frac, inter))

    return fractions, (H, W)


def decompress_image_2d(
    fractions: List[Tuple[Any, Tuple[float, float]]],
    size: Tuple[int, int]
) -> np.ndarray:
    """
    Восстанавливает 2D-изображение из списка аппроксимирующих дробей по строкам.

    Аргументы:
        fractions: список (fraction, interval) по строкам.
        size: размер изображения (H, W).

    Возвращает:
        Восстановленное изображение (np.ndarray формы (H, W)).
    """
    H, W = size
    restored = np.zeros((H, W), dtype=float)

    for h in range(H):
        frac, inter = fractions[h]
        restored[h, :] = decompress_signal_1d(frac, inter, W)

    return restored
