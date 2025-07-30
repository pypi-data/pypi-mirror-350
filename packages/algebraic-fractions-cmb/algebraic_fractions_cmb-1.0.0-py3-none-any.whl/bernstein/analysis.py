"""
analysis.py

Содержит функции для сравнения аппроксимирующей дроби с исходной функцией,
построения графиков и вычисления метрик ошибок (MSE, MAE, MAX_ERR).
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict, Tuple
from utils.metrics import compute_basic_metrics


def compare_fraction_vs_function(
    fraction,
    func: Callable[[float], float],
    interval: Tuple[float, float] = (0, 1),
    num_points: int = 200,
    plot: bool = True,
    save_fig: bool = False,
    fig_filename: str = "comparison.png"
) -> Dict[str, float]:
    """
    Строит график сравнения исходной функции и аппроксимированной дроби,
    вычисляет и возвращает метрики ошибок.

    Аргументы:
        fraction: объект дроби с методом evaluate.
        func: функция для аппроксимации.
        interval: интервал (a, b).
        num_points: количество точек для выборки.
        plot: флаг отображения графика.
        save_fig: если True, сохраняет график в файл.
        fig_filename: имя файла для сохранения графика.

    Возвращает:
        Словарь с метриками (MSE, MAE, MAX_ERR).
    """
    x = np.linspace(interval[0], interval[1], num_points)
    y_true = np.array([func(xi) for xi in x])
    y_approx = fraction.evaluate(x)

    metrics = compute_basic_metrics(y_true, y_approx)

    if plot:
        plt.figure()
        plt.plot(x, y_true, label='Исходная функция')
        plt.plot(x, y_approx, label='Аппроксимированная дробь')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"MSE={metrics.get('MSE', 0):.2e}, MAE={metrics.get('MAE', 0):.2e}")
        plt.legend()
        if save_fig:
            plt.savefig(fig_filename)
        plt.show()

    return metrics


def error_analysis(
    fraction,
    func: Callable[[float], float],
    interval: Tuple[float, float] = (0, 1),
    num_points: int = 200
) -> Dict[str, float]:
    """
    Вычисляет базовые метрики ошибок (MSE, MAE, MAX_ERR) для аппроксимации.

    Аргументы:
        fraction: объект дроби с методом evaluate.
        func: исходная функция.
        interval: интервал (a, b).
        num_points: число точек для анализа.

    Возвращает:
        Словарь с метриками ошибок.
    """
    x = np.linspace(interval[0], interval[1], num_points)
    y_true = np.array([func(xi) for xi in x])
    y_approx = fraction.evaluate(x)

    return compute_basic_metrics(y_true, y_approx)
