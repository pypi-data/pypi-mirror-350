"""
iterative_approximations.py

Содержит итерационные методы аппроксимации:
 1) iterative_chebyshev_rational_approx — аппроксимация с полиномами Чебышева (T или U) с учётом полюсов.
 2) iterative_bernstein_rational_approx — аппроксимация с использованием степенного (бернштейновского) базиса и полюсов.
"""

import numpy as np
import logging
from typing import Callable, Tuple, List, Optional
from numpy.polynomial import chebyshev as cheb
from utils.helpers import generate_points
from core.calculation import solve_least_squares
from core.parallel_acceleration import polynomial_powers_parallel

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def iterative_chebyshev_rational_approx(
    func: Callable[[float], float],
    interval: Tuple[float, float],
    deg_num: int,
    deg_den: int,
    kind: str = 'T',
    poles: Optional[List[float]] = None,
    max_iter: int = 5,
    tol: float = 1e-12,
    parallel: bool = False,
    damping: float = 0.2
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Итерационная аппроксимация функции с помощью полиномов Чебышева (T или U) с учётом полюсов.

    Возвращает:
        Кортеж (num_coeffs, den_coeffs) — коэффициенты числителя и знаменателя.
    """
    if poles is None:
        poles = []

    x_points = generate_points(interval, num=200)

    if parallel:
        from joblib import Parallel, delayed
        y_points = np.array(Parallel(n_jobs=-1)(delayed(func)(xi) for xi in x_points), dtype=float)
    else:
        y_points = np.array([func(xi) for xi in x_points], dtype=float)

    num_coeffs = np.zeros(deg_num + 1, dtype=float)
    den_coeffs = np.zeros(deg_den + 1, dtype=float)
    den_coeffs[0] = 1.0

    old_num = num_coeffs.copy()
    old_den = den_coeffs.copy()

    for it in range(max_iter):
        # 1. Вычисление текущего значения знаменателя с учётом полюсов
        if kind.upper() == 'T':
            den_raw = cheb.chebval(x_points, den_coeffs)
        else:
            den_raw = cheb.chebval(x_points, den_coeffs, kind='u')

        for p in poles:
            den_raw *= (x_points - p)

        # 2. Обновление числителя: y * Den(x) ≈ Num(x)
        if parallel:
            from joblib import Parallel, delayed

            def cheb_basis(k: int) -> np.ndarray:
                return cheb.Chebyshev.basis(k)(x_points)

            columns = Parallel(n_jobs=-1)(delayed(cheb_basis)(k) for k in range(deg_num + 1))
            A_num = np.column_stack(columns)
        else:
            A_num = np.column_stack([cheb.Chebyshev.basis(k)(x_points) for k in range(deg_num + 1)])

        b_num = y_points * den_raw
        num_coeffs = solve_least_squares(A_num, b_num)

        # 3. Обновление знаменателя: Num(x) ≈ y * Den(x)
        if kind.upper() == 'T':
            num_raw = cheb.chebval(x_points, num_coeffs)
        else:
            num_raw = cheb.chebval(x_points, num_coeffs, kind='u')

        if parallel:
            def cheb_basis_den(j: int) -> np.ndarray:
                return cheb.Chebyshev.basis(j)(x_points)

            cols_den = Parallel(n_jobs=-1)(delayed(cheb_basis_den)(j) for j in range(deg_den + 1))
            A_den = np.column_stack(cols_den)
        else:
            A_den = np.column_stack([cheb.Chebyshev.basis(j)(x_points) for j in range(deg_den + 1)])

        mask = np.abs(y_points) > 1e-14
        b_den = np.zeros_like(num_raw)
        b_den[mask] = num_raw[mask] / y_points[mask]
        beta_raw = solve_least_squares(A_den[mask, :], b_den[mask])
        den_coeffs = old_den + damping * (beta_raw - old_den)

        # 4. Проверка сходимости
        diff_num = np.linalg.norm(num_coeffs - old_num)
        diff_den = np.linalg.norm(den_coeffs - old_den)
        logger.info(f"Iter {it}: ||delta num||={diff_num:.2e}, ||delta den||={diff_den:.2e}")

        if diff_num < tol and diff_den < tol:
            logger.info("Сходимость достигнута.")
            break

        old_num = num_coeffs.copy()
        old_den = den_coeffs.copy()

    return num_coeffs, den_coeffs


def iterative_bernstein_rational_approx(
    func: Callable[[float], float],
    interval: Tuple[float, float],
    deg_num: int,
    deg_den: int,
    poles: Optional[List[float]] = None,
    max_iter: int = 10,
    tol: float = 1e-12,
    parallel: bool = False,
    damping: float = 0.2
) -> np.ndarray:
    """
    Итерационная аппроксимация функции с использованием степенного (бернштейновского) базиса с учётом полюсов.

    Возвращает:
        Массив коэффициентов длины (deg_num+1 + deg_den):
        первые deg_num+1 — для числителя, затем deg_den — для знаменателя.
    """
    if poles is None:
        poles = []

    x_points = generate_points(interval, num=200)

    if parallel:
        from joblib import Parallel, delayed
        y_points = np.array(Parallel(n_jobs=-1)(delayed(func)(xi) for xi in x_points), dtype=float)
    else:
        y_points = np.array([func(x) for x in x_points], dtype=float)

    total_len = deg_num + 1 + deg_den
    coeffs = np.zeros(total_len, dtype=float)
    old_coeffs = coeffs.copy()

    for it in range(max_iter):
        half = deg_num + 1
        a = coeffs[:half]
        b = coeffs[half:]

        # 1. Знаменатель с учётом полюсов
        den_raw = np.ones_like(x_points)
        for j, bj in enumerate(b, start=1):
            den_raw += bj * (x_points ** j)
        for p in poles:
            den_raw *= (x_points - p)

        # 2. Обновление числителя: y * Den(x) ≈ Num(x)
        if parallel:
            A_num = polynomial_powers_parallel(x_points, deg_num)
        else:
            A_num = np.column_stack([x_points ** k for k in range(deg_num + 1)])

        b_num = y_points * den_raw
        a_new = solve_least_squares(A_num, b_num)

        # 3. Обновление знаменателя: Num(x) ≈ y * Den(x)
        num_raw = np.zeros_like(x_points)
        for i, ai in enumerate(a_new):
            num_raw += ai * (x_points ** i)

        mask = np.abs(y_points) > 1e-14
        b_den_vals = np.zeros_like(num_raw)
        b_den_vals[mask] = num_raw[mask] / y_points[mask]

        if parallel:
            A_den_full = polynomial_powers_parallel(x_points, deg_den)
            A_den = A_den_full[:, 1:]
        else:
            A_den = np.column_stack([x_points ** j for j in range(1, deg_den + 1)])

        b_raw = solve_least_squares(A_den[mask, :], b_den_vals[mask])
        b_new = b + damping * (b_raw - b)

        # 4. Сходимость
        new_coeffs = np.concatenate([a_new, b_new])
        diff = np.linalg.norm(new_coeffs - old_coeffs)
        logger.info(f"Iter {it}: ||delta coeffs||={diff:.2e}")

        if diff < tol:
            logger.info("Сходимость достигнута.")
            coeffs = new_coeffs
            break

        coeffs = new_coeffs
        old_coeffs = new_coeffs.copy()

    return coeffs
