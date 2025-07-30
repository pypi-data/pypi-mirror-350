"""
chebyshev_markov.py

Реализует класс ChebyshevMarkovFraction, описывающий алгебраическую дробь
на базе полиномов Чебышева (T или U) с опциональными полюсами.
"""

import numpy as np
from typing import Union, List, Optional, Callable
from numpy.polynomial import chebyshev as cheb
from core.approximation import iterative_chebyshev_rational_approx


class ChebyshevMarkovFraction:
    """
    Класс, описывающий дробь Чебышева–Маркова:
        R(x) = Num(x)/Den(x),
    где Num(x) и Den(x) — линейные комбинации полиномов Чебышева (T или U),
    с опциональными полюсами.
    """

    def __init__(
        self,
        num_coeffs: Union[np.ndarray, List[float]],
        den_coeffs: Union[np.ndarray, List[float]],
        poles: Optional[Union[np.ndarray, List[float]]] = None,
        kind: str = 'T'
    ) -> None:
        self.num_coeffs = np.array(num_coeffs, dtype=float)
        self.den_coeffs = np.array(den_coeffs, dtype=float)
        self.poles = np.array(poles, dtype=float) if poles is not None else np.array([])
        self.kind = kind.upper()

    def evaluate(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Вычисляет R(x) = Num(x)/Den(x) с учетом полюсов.

        Аргументы:
            x: число или np.ndarray.

        Возвращает:
            Вычисленное значение дроби.
        """
        x_arr = np.atleast_1d(np.asarray(x, dtype=float))

        if self.kind == 'T':
            num_vals = cheb.chebval(x_arr, self.num_coeffs)
            den_vals = cheb.chebval(x_arr, self.den_coeffs)
        elif self.kind == 'U':
            num_vals = cheb.chebval(x_arr, self.num_coeffs, kind='u')
            den_vals = cheb.chebval(x_arr, self.den_coeffs, kind='u')
        else:
            raise ValueError(f"Недопустимый тип полиномов Чебышева: '{self.kind}' (ожидалось 'T' или 'U')")

        for p in self.poles:
            den_vals *= (x_arr - p)

        eps = 1e-15
        den_vals = np.where(np.abs(den_vals) < eps, eps, den_vals)

        result = num_vals / den_vals
        return result if result.size > 1 else result.item()

    @staticmethod
    def approximate(
        func: Callable[[float], float],
        interval: tuple = (-1, 1),
        deg_num: int = 3,
        deg_den: int = 3,
        kind: str = 'T',
        poles: Optional[List[float]] = None,
        max_iter: int = 5,
        tol: float = 1e-12,
        parallel: bool = False
    ) -> "ChebyshevMarkovFraction":
        """
        Создаёт аппроксимирующую дробь Чебышева–Маркова с помощью iterative_chebyshev_rational_approx.

        Аргументы:
            func: аппроксимируемая функция.
            interval: интервал аппроксимации (a, b).
            deg_num: степень числителя.
            deg_den: степень знаменателя.
            kind: тип полиномов ('T' или 'U').
            poles: список полюсов (опционально).
            max_iter: максимальное число итераций.
            tol: порог сходимости.
            parallel: использовать ли параллельные вычисления.

        Возвращает:
            Экземпляр ChebyshevMarkovFraction.
        """
        num_coeffs, den_coeffs = iterative_chebyshev_rational_approx(
            func=func,
            interval=interval,
            deg_num=deg_num,
            deg_den=deg_den,
            kind=kind,
            poles=poles,
            max_iter=max_iter,
            tol=tol,
            parallel=parallel
        )
        return ChebyshevMarkovFraction(num_coeffs, den_coeffs, poles, kind)
