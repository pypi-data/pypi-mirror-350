"""
bernstein.py

Реализует класс BernsteinFraction, описывающий алгебраическую дробь
в степенном (аналог бернштейновского) базисе:
  R(x) = Num(x) / Den(x),
где:
  Num(x) = a0 + a1*x + ... + a_deg_num*x^deg_num,
  Den(x) = 1 + b1*x + ... + b_deg_den*x^deg_den,
с опциональными полюсами (учитываются через умножение на ∏ (x - p_i)).

Для аппроксимации используется функция iterative_bernstein_rational_approx из core.approximation,
возвращающая массив коэффициентов длины (deg_num+1 + deg_den).
"""

import numpy as np
from typing import Callable, List, Union, Optional
from core.approximation import iterative_bernstein_rational_approx


class BernsteinFraction:
    """
    Класс, описывающий аппроксимирующую дробь:
        R(x) = Num(x)/Den(x),
    где числитель и знаменатель заданы в степенном базисе и могут модифицироваться полюсами.
    """

    def __init__(
        self,
        coeffs: Union[np.ndarray, List[float]],
        deg_num: int,
        deg_den: int,
        poles: Optional[Union[np.ndarray, List[float]]] = None
    ) -> None:
        expected_length = deg_num + 1 + deg_den
        coeffs_arr = np.asarray(coeffs, dtype=float)
        if coeffs_arr.size != expected_length:
            raise ValueError(
                f"Неверное число коэффициентов: ожидалось {expected_length}, получено {coeffs_arr.size}."
            )
        self.deg_num = deg_num
        self.deg_den = deg_den
        self.num_coeffs = coeffs_arr[:deg_num + 1]
        self.den_coeffs = coeffs_arr[deg_num + 1:]
        self.poles = np.array(poles, dtype=float) if poles is not None else np.array([])

    def evaluate(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Вычисляет значение дроби R(x) = Num(x)/Den(x).

        Аргументы:
            x: число или массив чисел.

        Возвращает:
            Вычисленное значение (скаляр или np.ndarray).
        """
        x_arr = np.atleast_1d(np.asarray(x, dtype=float))

        # Вычисление числителя
        A_num = np.vander(x_arr, N=self.num_coeffs.size, increasing=True)
        num_vals = A_num @ self.num_coeffs

        # Вычисление знаменателя: 1 + sum(b_j * x^j)
        A_den = np.vander(x_arr, N=self.den_coeffs.size + 1, increasing=True)
        den_vals = A_den[:, 0] + (A_den[:, 1:] @ self.den_coeffs)

        # Учёт полюсов
        for p in self.poles:
            den_vals *= (x_arr - p)

        # Защита от деления на значение, близкое к нулю
        eps = 1e-15
        den_vals = np.where(np.abs(den_vals) < eps, eps, den_vals)

        result = num_vals / den_vals
        return result if result.size > 1 else result.item()

    @staticmethod
    def approximate(
        func: Callable[[float], float],
        interval: tuple = (0, 1),
        deg_num: int = 3,
        deg_den: int = 3,
        poles: Optional[Union[List[float], np.ndarray]] = None,
        max_iter: int = 5,
        tol: float = 1e-12,
        parallel: bool = False
    ) -> "BernsteinFraction":
        """
        Аппроксимирует функцию func рациональной дробью в бернштейновском базисе.

        Аргументы:
            func: аппроксимируемая функция (float -> float).
            interval: интервал аппроксимации (a, b).
            deg_num: степень числителя.
            deg_den: степень знаменателя.
            poles: список полюсов (опционально).
            max_iter: максимум итераций.
            tol: порог сходимости.
            parallel: использовать параллельные вычисления.

        Возвращает:
            BernsteinFraction с рассчитанными коэффициентами.
        """
        coeffs = iterative_bernstein_rational_approx(
            func=func,
            interval=interval,
            deg_num=deg_num,
            deg_den=deg_den,
            poles=poles,
            max_iter=max_iter,
            tol=tol,
            parallel=parallel
        )
        return BernsteinFraction(coeffs, deg_num, deg_den, poles=poles)
