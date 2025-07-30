"""
plotting.py

Содержит функции для построения графиков и визуализации данных:
 - plot_signal_and_approx — сравнение 1D-сигнала и его аппроксимации.
 - plot_2d_data — визуализация исходных и восстановленных 2D-данных.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_signal_and_approx(
    x: np.ndarray,
    signal: np.ndarray,
    approx_signal: np.ndarray,
    title: str = "Сравнение сигнала и аппроксимации"
) -> None:
    """
    Строит график сравнения исходного 1D-сигнала и его аппроксимации.

    Аргументы:
        x: координаты точек (1D массив).
        signal: оригинальный сигнал.
        approx_signal: восстановленный (аппроксимированный) сигнал.
        title: заголовок графика.
    """
    plt.figure()
    plt.plot(x, signal, 'o-', label='Оригинальный сигнал')
    plt.plot(x, approx_signal, 'x--', label='Аппроксимация')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_2d_data(
    original_2d: np.ndarray,
    restored_2d: np.ndarray,
    title: str = "Сравнение 2D-данных"
) -> None:
    """
    Визуализирует сравнение оригинальных и восстановленных 2D-данных (например, изображений).

    Аргументы:
        original_2d: оригинальный двумерный массив.
        restored_2d: восстановленный двумерный массив.
        title: заголовок окна.
    """
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(original_2d, cmap='gray')
    plt.title("Оригинал")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(restored_2d, cmap='gray')
    plt.title("Восстановлено")
    plt.axis("off")

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()
