# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

from typing import Dict, Tuple
from attr import define
import numpy as np
from scipy.stats import multivariate_normal, shapiro
import statistical_agreement as sa
from statistical_agreement.core._types import NDArrayFloat
from .monte_carlo import MonteCarlo


@define(kw_only=True)
class Models:
    mean: NDArrayFloat
    cov: NDArrayFloat

# Based on
# Lin LI.
# A concordance correlation coefficient to evaluate reproducibility.
# Biometrics. 1989 Mar;45(1):255-68. PMID: 2720055.

# and

# King TS, Chinchilli VM.
# Robust estimators of the concordance correlation coefficient.
# J Biopharm Stat. 2001;11(3):83-105. doi: 10.1081/BIP-100107651. PMID: 11725932.
# pages 90-94

MODELS = {
    "1": Models(mean=np.array([0, 0]), 
                cov=np.array([[1.0, 0.95], [0.95, 1.0]])),
    "2": Models(mean=np.array([-np.sqrt(0.1)/2, np.sqrt(0.1)/2]), 
                cov=np.array([[1.1**2, 0.95*1.1*0.9], [0.95*1.1*0.9, 0.9**2]])),
    "3": Models(mean=np.array([-np.sqrt(0.25)/2, np.sqrt(0.25)/2]), 
                cov=np.array([[(4/3)**2, 0.5*4/3*2/3], [0.5*4/3*2/3, (2/3)**2]]))}

EXPECTED_VALUES = {
    "ccc": {"1": 0.950, "2": 0.887, "3": 0.360},
    "transformed_ccc": {"1": 1.832, "2": 1.408, "3": 0.377},
    "msd": {"1": 0.100, "2": 0.239, "3": 0.1583},
    "transformed_msd": {"1": -2.303, "2": -1.431, "3": 0.640},
}


def mc_simulation(
        name_of_index: str, 
        str_criterion: str=""
    ) -> Tuple[str, Dict[Tuple[str, str], Dict[Tuple[int, str], float]]]:
    try:
        criterion = float(str_criterion)
    except ValueError:
        criterion = 0.0

    data_possibilities = [10, 20, 50]
    models_possibilities = ["1", "2", "3"]

    result: Dict[Tuple[str, str], Dict[Tuple[int, str], float]] = {}
    for m in models_possibilities:
        for d in data_possibilities:
            a = _simulation_from_model_and_ndata(
                n_iteration=5000, 
                n_data=d, 
                model=m, 
                name_of_index=name_of_index, 
                criterion=criterion
            )
            for k, v in a.items():
                if k not in result:
                    result[k] = v
                else:
                    result[k].update(v)

    return name_of_index, result


def _simulation_from_model_and_ndata(
        n_iteration: int, 
        n_data: int, 
        model: str,
        name_of_index: str, 
        criterion: float
    ) -> Dict[Tuple[str, str], Dict[Tuple[int, str], float]]:

    m = MODELS[model]
    mean, cov = m.mean, m.cov
    array_index = np.empty(n_iteration)
    array_index_std = np.empty(n_iteration)
    array_transformed_index = np.empty(n_iteration)
    array_transformed_index_std = np.empty(n_iteration)
    index_func = getattr(sa, name_of_index)

    for i in range(n_iteration):
        multidim = multivariate_normal.rvs(mean=mean, cov=cov, size=n_data)
        index = index_func(multidim[:, 0], multidim[:, 1], method="approx", alpha=0.05, transformed=True, criterion=criterion)

        array_index[i] = index.estimate
        array_transformed_index[i] = index.transformed_estimate

        try:
            array_index_std[i] = np.sqrt(index.variance)
            array_transformed_index_std[i] = np.sqrt(index.transformed_variance)
        except TypeError:
            array_index_std[i] = 0
            array_transformed_index_std[i] = 0

    mc = MonteCarlo()
    mc_index = mc.compute(array_index)
    mc_index_std = mc.compute(array_index_std)
    mc_transformed_index = mc.compute(array_transformed_index)
    mc_transformed_index_std = mc.compute(array_transformed_index_std)

    res: Dict[Tuple[str, str], Dict[Tuple[int, str], float]] = {}

    res[(model, f"{name_of_index}")] = {}
    res[(model, f"{name_of_index}")][(n_data, "mean")] = mc_index.mean
    res[(model, f"{name_of_index}")][(n_data, "std")] = np.sqrt(mc_index.var)
    res[(model, f"{name_of_index}")][(n_data, "pvalue")] = shapiro(array_index).pvalue
    res[(model, f"{name_of_index}")][(n_data, "true_value")] = EXPECTED_VALUES[f"{name_of_index}"][model]

    res[(model, f"transformed_{name_of_index}")] = {}
    res[(model, f"transformed_{name_of_index}")][(n_data, "mean")] = mc_transformed_index.mean
    res[(model, f"transformed_{name_of_index}")][(n_data, "std")] = np.sqrt(mc_transformed_index.var)
    res[(model, f"transformed_{name_of_index}")][(n_data, "pvalue")] = shapiro(array_transformed_index).pvalue
    res[(model, f"transformed_{name_of_index}")][(n_data, "true_value")] = EXPECTED_VALUES[f"transformed_{name_of_index}"][model]

    res[(model, f"s_{name_of_index}")] = {}
    res[(model, f"s_{name_of_index}")][(n_data, "mean")] = mc_index_std.mean

    res[(model, f"s_transformed_{name_of_index}")] = {}
    res[(model, f"s_transformed_{name_of_index}")][(n_data, "mean")] = mc_transformed_index_std.mean

    return res
