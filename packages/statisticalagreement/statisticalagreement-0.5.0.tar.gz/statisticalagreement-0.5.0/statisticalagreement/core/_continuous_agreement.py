# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import numpy as np
from scipy.stats import norm, chi2

from statisticalagreement.core._types import NDArrayFloat

from statisticalagreement.core.classutils import TransformFunc, ConfidentLimit, TransformedEstimator
from statisticalagreement.core.mathutils import almost_equal_float


def precision(
        x: NDArrayFloat,
        y: NDArrayFloat,
        alpha: float
    ) -> TransformedEstimator:

    n = len(x)
    s_sq_hat_biased_x, s_hat_biased_xy, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()

    sqr_var = np.sqrt(s_sq_hat_biased_x * s_sq_hat_biased_y)
    rho_hat = s_hat_biased_xy / sqr_var

    var_rho_hat = (1 - rho_hat**2/2)/(n-3)
    rho = TransformedEstimator(
        estimate=rho_hat,
        variance=var_rho_hat,
        transformed_function=TransformFunc.Z,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return rho


def accuracy(
        x: NDArrayFloat,
        y: NDArrayFloat,
        t_precision: TransformedEstimator,
        alpha: float
    ) -> TransformedEstimator:

    n = len(x)
    mu_d = np.mean(x - y, dtype=np.float64)
    rho_hat = t_precision.estimate

    s_sq_hat_biased_x, _, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()
    sqr_var = np.sqrt(s_sq_hat_biased_x * s_sq_hat_biased_y)
    nu_sq_hat = mu_d**2 / sqr_var
    omega_hat = np.sqrt(s_sq_hat_biased_x / s_sq_hat_biased_y)

    acc_hat = 2 * sqr_var / (s_sq_hat_biased_x + s_sq_hat_biased_y + mu_d**2)
    var_acc_hat = (
        acc_hat**2*nu_sq_hat*(omega_hat + 1/omega_hat - 2*rho_hat) +
        0.5*acc_hat**2*(omega_hat**2+1/omega_hat**2+2*rho_hat**2) +
        (1+rho_hat**2)*(acc_hat*nu_sq_hat-1)
        ) / ((n-2)*(1-acc_hat)**2)

    acc = TransformedEstimator(
        estimate=acc_hat,
        variance=var_acc_hat,
        transformed_function=TransformFunc.LOGIT,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return acc


def ccc_lin(
        x: NDArrayFloat,
        y: NDArrayFloat,
        t_precision: TransformedEstimator,
        t_accuracy: TransformedEstimator,
        alpha: float,
        allowance_whitin_sample_deviation: float
    ) -> TransformedEstimator:

    n = len(x)
    mu_d = np.mean(x - y, dtype=np.float64)
    rho_hat = t_precision.estimate

    s_sq_hat_biased_x, _, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()
    sqr_var = np.sqrt(s_sq_hat_biased_x * s_sq_hat_biased_y)
    nu_sq_hat = mu_d**2 / sqr_var

    ccc_hat = rho_hat * t_accuracy.estimate
    var_ccc_hat = 1 / (n - 2) * ((1-rho_hat**2)*ccc_hat**2*(1-ccc_hat**2)/rho_hat**2
                                 + 2*ccc_hat**3*(1-ccc_hat)*nu_sq_hat / rho_hat
                                 - ccc_hat**4 * nu_sq_hat**2 / (2*rho_hat**2))
    var_z_hat = var_ccc_hat / (1-ccc_hat**2)**2

    ccc = TransformedEstimator(
        estimate=ccc_hat,
        variance=var_ccc_hat,
        transformed_variance=var_z_hat,
        transformed_function=TransformFunc.Z,
        allowance=1-allowance_whitin_sample_deviation**2,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return ccc


def ccc_ustat(
        x: NDArrayFloat,
        y: NDArrayFloat,
        alpha: float,
        allowance_whitin_sample_deviation: float
    ) -> TransformedEstimator:

    n = len(x)
    sx = np.sum(x)
    sy = np.sum(y)
    ssx = np.sum(x**2)
    ssy = np.sum(y**2)

    xy = x * y
    sxy = np.sum(xy)

    u1 = -4.0/n * sxy
    u2 = 2.0/n * (ssx + ssy)
    u3 = -4.0/(n*(n-1)) * (sx * sy - sxy)

    h = (n-1) * (u3 - u1)
    g = u1 + n*u2 + (n-1)*u3

    psi1 = (n-2)*xy + sxy/n
    psi2 = (n-2)*(x**2 - ssx / n + y**2 - ssy / n)
    psi3 = x * sy + y * sx - sx * sy / n + 2*xy + sxy/n

    v_u1 = 64.0*np.sum(psi1**2)/(n**2*(n-1)**2)
    v_u2 = 4.0*np.sum(psi2**2)/(n**2*(n-1)**2)
    v_u3 = 64.0*np.sum(psi3**2)/(n**2*(n-1)**2)
    cov_u1_u2 = -16.0*np.sum(psi1*psi2)/(n**2*(n-1)**2)
    cov_u1_u3 = 64.0*np.sum(psi1*psi3)/(n**2*(n-1)**2)
    cov_u2_u3 = -16.0*np.sum(psi2*psi3)/(n**2*(n-1)**2)

    v_h = (n-1)**2 * (v_u3 + v_u1 - 2 * cov_u1_u3)
    v_g = v_u1 + n**2*v_u2 + (n-1)**2*v_u3 + 2*n*cov_u1_u2 + 2.0*(n-1)*cov_u1_u3 + 2.0*n*(n-1)*cov_u2_u3
    cov_h_g = (n-1)*(-(n-2)*cov_u1_u3 + n*cov_u2_u3 + (n-1)*v_u3 - v_u1 - n*cov_u1_u2)

    ccc_hat = h/g
    var_ccc_hat = ccc_hat**2 * (v_h / h**2 - 2*cov_h_g / (h*g) + v_g / g**2)
    var_z_hat = var_ccc_hat / (1.0 - ccc_hat**2)**2

    ccc = TransformedEstimator(
        estimate=ccc_hat,
        variance=var_ccc_hat,
        transformed_variance=var_z_hat,
        transformed_function=TransformFunc.Z,
        allowance=1-allowance_whitin_sample_deviation**2,
        robust=True,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return ccc


def msd_exact(
        x: NDArrayFloat,
        y: NDArrayFloat,
        alpha: float
    ) -> TransformedEstimator:

    n = len(x)
    d = x - y
    mu_d = np.mean(d, dtype=np.float64)

    eps_sq_hat = np.sum(d**2, dtype=np.float64) / (n - 1)
    var_esp_hat = 2 / (n - 2) * ( eps_sq_hat**2 - mu_d**4 )
    var_w_hat = var_esp_hat / eps_sq_hat**2

    msd = TransformedEstimator(
        estimate=eps_sq_hat,
        variance=var_esp_hat,
        transformed_variance=var_w_hat,
        transformed_function=TransformFunc.LOG,
        alpha=alpha,
        confident_limit=ConfidentLimit.UPPER,
        n=n
    )
    return msd


def _rbs_allowance(cp_allowance: float) -> float:
    if almost_equal_float(cp_allowance, 0.75):
        return .5
    if almost_equal_float(cp_allowance, 0.8):
        return 8.0
    if almost_equal_float(cp_allowance, 0.85):
        return 2.0
    if almost_equal_float(cp_allowance, 0.9):
        return 1.0
    if almost_equal_float(cp_allowance, 0.95):
        return .5
    return np.nan


def rbs(
        x: NDArrayFloat, 
        y: NDArrayFloat, 
        cp_allowance: float
    ) -> TransformedEstimator:

    n = len(x)
    d = x - y
    s_sq_hat_biased_x, s_hat_biased_xy, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()
    s_sq_hat_d = n / (n - 3) * (s_sq_hat_biased_x + s_sq_hat_biased_y - 2 * s_hat_biased_xy)
    mu_d = np.mean(d, dtype=np.float64)

    rbs_hat = mu_d**2 / s_sq_hat_d
    _rbs = TransformedEstimator(
        estimate=rbs_hat,
        allowance=_rbs_allowance(cp_allowance)
    )
    return _rbs


def cp_approx(
        x: NDArrayFloat,
        y: NDArrayFloat,
        msd: TransformedEstimator, 
        alpha: float, 
        delta_criterion: float, 
        cp_allowance: float
    ) -> TransformedEstimator:

    n = len(x)
    d = x - y
    s_sq_hat_biased_x, s_hat_biased_xy, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()
    s_sq_hat_d = n / (n - 3) * (s_sq_hat_biased_x + s_sq_hat_biased_y - 2 * s_hat_biased_xy)
    mu_d = np.mean(d, dtype=np.float64)

    delta_plus: float = (delta_criterion + mu_d) / np.sqrt(s_sq_hat_d)
    n_delta_plus = norm.pdf(-delta_plus)
    delta_minus: float = (delta_criterion - mu_d) / np.sqrt(s_sq_hat_d)
    n_delta_minus = norm.pdf(delta_minus)

    cp_hat = chi2.cdf(delta_criterion**2 / msd.estimate, df=1)
    var_cp_hat = 1.0/(n-3) * ((n_delta_plus - n_delta_minus)**2 + 0.5*(delta_minus*n_delta_minus + delta_plus*n_delta_plus))
    var_transform_cp_hat = var_cp_hat / ((1-cp_hat)**2*cp_hat**2)

    cp = TransformedEstimator(
        estimate=cp_hat,
        variance=var_cp_hat,
        transformed_variance=var_transform_cp_hat,
        transformed_function=TransformFunc.LOGIT,
        allowance=cp_allowance,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return cp


def cp_exact(
        x: NDArrayFloat,
        y: NDArrayFloat, 
        alpha: float,
        delta_criterion: float,
        cp_allowance: float
    ) -> TransformedEstimator:

    n = len(x)
    d = x - y
    s_sq_hat_biased_x, s_hat_biased_xy, _, s_sq_hat_biased_y = np.cov(x, y, bias=True, dtype=np.float64).flatten()
    s_sq_hat_d = n / (n - 3) * (s_sq_hat_biased_x + s_sq_hat_biased_y - 2 * s_hat_biased_xy)
    mu_d = np.mean(d, dtype=np.float64)

    delta_plus: float = (delta_criterion + mu_d) / np.sqrt(s_sq_hat_d)
    n_delta_plus = norm.pdf(-delta_plus)
    delta_minus: float = (delta_criterion - mu_d) / np.sqrt(s_sq_hat_d)
    n_delta_minus = norm.pdf(delta_minus)

    cp_hat = norm.cdf(delta_minus) - norm.cdf(-delta_plus)
    var_cp_hat = 1/(n-3) * ((n_delta_plus - n_delta_minus)**2 + 0.5*(delta_minus*n_delta_minus + delta_plus*n_delta_plus))
    var_transform_cp_hat = var_cp_hat / ((1-cp_hat)**2*cp_hat**2)

    cp = TransformedEstimator(
        estimate=cp_hat,
        variance=var_cp_hat,
        transformed_variance=var_transform_cp_hat,
        transformed_function=TransformFunc.LOGIT,
        allowance=cp_allowance,
        robust=True,
        alpha=alpha,
        confident_limit=ConfidentLimit.LOWER,
        n=n
    )
    return cp


def tdi_approx(
        msd: TransformedEstimator, 
        pi_criterion: float, 
        tdi_allowance: float
    ) -> TransformedEstimator:

    coeff_tdi = norm.ppf(1 - (1 - pi_criterion) / 2)

    if np.isnan(msd.limit):
        raise ValueError("Cannot compute tdi since no limit was computed for msd.")

    tdi = TransformedEstimator(
        estimate=coeff_tdi * np.sqrt(msd.estimate),
        limit=coeff_tdi * np.sqrt(msd.limit),
        allowance=tdi_allowance,
        robust=False,
        confident_limit=ConfidentLimit.UPPER
    )
    return tdi
