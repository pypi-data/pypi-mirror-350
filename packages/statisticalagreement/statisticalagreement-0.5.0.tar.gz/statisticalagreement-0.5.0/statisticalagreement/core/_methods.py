# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import warnings
import numpy as np

from statisticalagreement.core import _categorical_agreement, _continuous_agreement
from statisticalagreement.core.classutils import Indices, TransformedEstimator
from statisticalagreement.core._types import NDArrayFloat, NDArrayInt


def _ccc_methods(
        x: NDArrayFloat,
        y: NDArrayFloat,
        method: str,
        alpha: float,
        allowance: float
    ) -> TransformedEstimator:

    if method == "approx":
        # Lin LI. A concordance correlation coefficient to evaluate reproducibility.
        # Biometrics. 1989 Mar;45(1):255-68. PMID: 2720055.
        rho = _continuous_agreement.precision(x, y, alpha)
        acc = _continuous_agreement.accuracy(x, y, rho, alpha)
        return _continuous_agreement.ccc_lin(x, y, rho, acc, alpha, allowance)

    if method == "ustat":
        # King TS, Chinchilli VM.
        # Robust estimators of the concordance correlation coefficient.
        # J Biopharm Stat. 2001;11(3):83-105. doi: 10.1081/BIP-100107651. PMID: 11725932.
        warnings.warn("The current implementation of the variance of the estimator is invalid.")
        return _continuous_agreement.ccc_ustat(x, y, alpha, allowance)

    raise ValueError("Wrong method called for ccc computation, \
                     current possible methods are approx or ustat.")


def _cp_methods(
        x: NDArrayFloat,
        y: NDArrayFloat,
        method: str,
        alpha: float,
        criterion: float,
        allowance: float
    ) -> TransformedEstimator:

    if method == "approx":
        _msd = _continuous_agreement.msd_exact(x, y, alpha)
        return _continuous_agreement.cp_approx(x, y, _msd, alpha, criterion, allowance)

    if method == "exact":
        return _continuous_agreement.cp_exact(x, y, alpha, criterion, allowance)

    raise ValueError("Wrong method called for cp computation, \
                     current possible methods are approx or exact.")


def _tdi_methods(
        x: NDArrayFloat,
        y: NDArrayFloat,
        method: str,
        alpha: float,
        criterion: float,
        allowance: float
    ) -> TransformedEstimator:

    if method == "approx":
        _msd = _continuous_agreement.msd_exact(x, y, alpha)
        return _continuous_agreement.tdi_approx(_msd, criterion, allowance)

    raise ValueError("Wrong method called for tdi computation, \
                     current possible methods are approx.")


def _msd_methods(
        x: NDArrayFloat,
        y: NDArrayFloat,
        method: str,
        alpha: float
    ) -> TransformedEstimator:

    if method == "approx":
        return _continuous_agreement.msd_exact(x, y, alpha)

    raise ValueError("Wrong method called for msd computation, \
                     current possible methods are approx.")


def _kappa_methods(
        x: NDArrayInt,
        y: NDArrayInt,
        method: str,
        alpha: float
    ) -> TransformedEstimator:

    c = max(len(np.unique(x)), len(np.unique(y)))
    if method == "cohen":
        return _categorical_agreement.cohen_kappa(x, y, c, alpha)

    if method in {"ciccetti", "abs"}:
        return _categorical_agreement.abs_kappa(x, y, c, alpha)

    if method in {"fleiss", "squared"}:
        return _categorical_agreement.squared_kappa(x, y, c, alpha)

    raise ValueError("Wrong method called for kappa computation, \
                     current possible methods are cohen, abs or squared.")


def continuous_methods(
        index_name: Indices,
        x: NDArrayFloat,
        y: NDArrayFloat,
        method: str,
        alpha: float,
        criterion: float,
        allowance: float
    ) -> TransformedEstimator:

    if x.ndim == 0 or y.ndim == 0:
        raise ValueError("Input must be at least 1-dimensional")

    if len(x) <= 3 or len(y) <= 3:
        raise ValueError("Not enough data to compute indices, \
                            need at least four elements on each array_like input.")
    
    if index_name == Indices.CCC:
        return _ccc_methods(x, y, method, alpha, allowance)

    elif index_name == Indices.CP:
        return _cp_methods(x, y, method, alpha, criterion, allowance)

    elif index_name == Indices.TDI:
        return _tdi_methods(x, y, method, alpha, criterion, allowance)

    elif index_name == Indices.MSD:
        return _msd_methods(x, y, method, alpha)
    
    raise ValueError("Unknown index")


def categorical_methods(
        index_name: Indices,
        x: NDArrayInt,
        y: NDArrayInt,
        method: str,
        alpha: float,
        criterion: float,
        allowance: float
    ) -> TransformedEstimator:

    if x.ndim == 0 or y.ndim == 0:
        raise ValueError("Input must be at least 1-dimensional")

    if len(x) <= 3 or len(y) <= 3:
        raise ValueError("Not enough data to compute indices, \
                            need at least four elements on each array_like input.")
    
    if index_name == Indices.KAPPA:
        return _kappa_methods(x, y, method, alpha)
    
    raise ValueError("Unknown index")
