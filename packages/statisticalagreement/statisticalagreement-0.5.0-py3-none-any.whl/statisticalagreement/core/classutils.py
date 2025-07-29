# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

from enum import Enum
from typing import Dict, Union

from attr import define
from scipy.stats import norm, t
import numpy as np

from statisticalagreement.core._types import NDArrayFloat

class Indices(Enum):
    CCC = 0
    CP = 1
    TDI = 2
    MSD = 3
    KAPPA = 4

class FlagData(Enum):
    OK = 0
    CONSTANT = 1
    NEGATIVE = 2

class TransformFunc(Enum):
    NONE = "none"
    ID = "identity"
    LOG = "logarithmic"
    Z = "fisher_z"
    LOGIT = "logit"


    def apply(self, x: np.typing.ArrayLike) -> NDArrayFloat:
        """
        Apply transformation to input data.

        Parameters
        ----------
        x : array_like
            Input data. Must satisfy:
            - LOG: x > 0
            - Z: |x| < 1
            - LOGIT: 0 < x < 1

        Returns
        -------
        np.ndarray
            Transformed data.
        """
        x_array = np.asarray(x, dtype=np.float64)
        if x_array.size == 0:
            return x_array
        
        match self:
            case TransformFunc.ID:
                return x_array
            case TransformFunc.LOG:
                if np.any(x_array <= 0):
                    raise ValueError("LOG transformation requires all x > 0")
                return np.log(x)
            case TransformFunc.Z:
                if np.any(np.abs(x_array) >= 1):
                    raise ValueError("Z transformation requires |x| < 1")
                return np.log((1.0 + x_array)/(1.0 - x_array)) * 0.5
            case TransformFunc.LOGIT:
                if np.any((x_array <= 0) | (x_array >= 1)):
                    raise ValueError("LOGIT transformation requires 0 < x < 1")
                return np.log(x_array / (1.0 - x_array))
            case TransformFunc.NONE:
                raise ValueError("Cannot apply a NONE transformer.")


    def apply_inv(self, x: np.typing.ArrayLike) -> NDArrayFloat:
        x_array = np.asarray(x, dtype=np.float64)
        if x_array.size == 0:
            return x_array

        match self:
            case TransformFunc.ID:
                return x_array
            case TransformFunc.LOG:
                return np.exp(x_array)
            case TransformFunc.Z:
                exp_2x = np.exp(2.0 * x_array)
                return (exp_2x - 1.0) / (exp_2x + 1.0)
            case TransformFunc.LOGIT:
                exp_x = np.exp(x_array)
                return exp_x/(exp_x + 1.0)
            case TransformFunc.NONE:
                raise ValueError("Cannot apply a NONE transformer.")


class ConfidentLimit(Enum):
    NONE = -1
    LOWER = 0
    UPPER = 1


@define
class Estimator:
    estimate: float
    limit: float
    allowance: float = np.nan

    def to_dict(self) -> Dict[str, Union[float, bool, str]]:
        return {
            "estimate": self.estimate,
            "limit": self.limit,
            "allowance": self.allowance,
        }


@define
class TransformedEstimator:
    estimate: float
    variance: float = np.nan
    transformed_function: TransformFunc = TransformFunc.NONE
    transformed_estimate: float = np.nan
    transformed_variance: float = np.nan
    limit: float = np.nan
    allowance: float = np.nan
    robust: bool = False
    alpha: float = np.nan
    confident_limit: ConfidentLimit = ConfidentLimit.NONE
    n: int = 30

    def __attrs_post_init__(self) -> None:
        if np.isnan(self.variance):
            self.transformed_estimate = np.nan
            return

        if self.n >= 30:
            coeff = norm.ppf(1 - self.alpha)
        else:
            coeff = t.ppf(1 - self.alpha, self.n - 1)

        self.transformed_estimate = float(self.transformed_function.apply(self.estimate))
        if np.isnan(self.transformed_variance):
            self.transformed_variance = self.variance

        transformed_limit = self.transformed_estimate
        if self.confident_limit == ConfidentLimit.UPPER:
            transformed_limit += coeff * np.sqrt(self.transformed_variance)
        if self.confident_limit == ConfidentLimit.LOWER:
            transformed_limit -= coeff * np.sqrt(self.transformed_variance)

        self.limit = float(self.transformed_function.apply_inv(transformed_limit))


    def to_dict(self) -> Dict[str, Union[float, bool, str]]:
        return {
            "estimate": self.estimate,
            "limit": self.limit,
            "variance": self.variance,
            "transformed_function": str(self.transformed_function),
            "transformed_estimate": self.transformed_estimate,
            "transformed_variance": self.transformed_variance,
            "allowance": self.allowance,
            "robust": self.robust,
        }


    def as_estimator(self) -> Estimator:
        return Estimator(estimate=self.estimate, limit=self.limit, allowance=self.allowance)
