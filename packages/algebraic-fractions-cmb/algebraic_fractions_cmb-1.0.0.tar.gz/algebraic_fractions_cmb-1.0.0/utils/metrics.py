"""
metrics.py

Содержит функции для расчёта метрик ошибок между истинными и аппроксимированными данными:
    - compute_basic_metrics: возвращает MSE, MAE и MAX_ERR.
"""

import numpy as np
from typing import Dict


def compute_basic_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Вычисляет базовые метрики ошибок между y_true и y_pred:
        - MSE: среднеквадратичная ошибка,
        - MAE: средняя абсолютная ошибка,
        - MAX_ERR: максимальная абсолютная ошибка.

    Аргументы:
        y_true: массив истинных значений.
        y_pred: массив предсказанных (аппроксимированных) значений.

    Возвращает:
        Словарь {"MSE": ..., "MAE": ..., "MAX_ERR": ...}
    """
    diff = y_true - y_pred
    mse = np.mean(diff ** 2)
    mae = np.mean(np.abs(diff))
    max_err = np.max(np.abs(diff))

    return {
        "MSE": mse,
        "MAE": mae,
        "MAX_ERR": max_err
    }
