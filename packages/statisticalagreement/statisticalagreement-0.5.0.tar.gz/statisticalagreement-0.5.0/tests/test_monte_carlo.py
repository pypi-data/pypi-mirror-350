# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import unittest
from unittest.util import safe_repr
import numpy as np
from scipy.stats import norm, sem

from statisticalagreement.simulation.monte_carlo import MonteCarlo

N_REPETITION = 5000

class TestMonteCarlo(unittest.TestCase):
    # using difference of ulp as a more reliable way to test equality in float/double
    # same method as used in GoogleTest C++ library
    # see https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
    def assert_almost_equal(self, first: float, second: float, max_ulps: int=4) -> None:

        # catching obvious case
        if first == second:
            return

        # catching number with difference of sign and inf/nan
        if first < 0 != second < 0:
            standard_msg = f"{safe_repr(first)} != {safe_repr(second)} \
                within {safe_repr(max_ulps)} ulp"

        else:
            first_int = np.array(first).view("int64")
            second_int = np.array(second).view("int64")

            ulps_diff = abs(first_int - second_int)

            if ulps_diff < max_ulps:
                return

            standard_msg = f"{safe_repr(first)} != {safe_repr(second)} \
                within {safe_repr(max_ulps)} ulp"

        msg = self._formatMessage(None, standard_msg)
        raise self.failureException(msg)


    def assert_almost_mc_ci(self, array: np.typing.NDArray[np.float64]) -> None:
        mc = MonteCarlo().compute(array)
        self.assert_almost_equal(mc.mean, np.mean(array, dtype=np.float64))
        self.assert_almost_equal(mc.var, np.var(array, dtype=np.float64))
        self.assert_almost_equal(mc.standard_error, float(sem(array, ddof=0)))


    def test_constant_monte_carlo(self) -> None:
        array = np.repeat(1.0, N_REPETITION).astype(np.float64)
        self.assert_almost_mc_ci(array)


    def test_normal_monte_carlo(self) -> None:
        array = norm.rvs(loc=0.0, scale=1.0, size=N_REPETITION)
        array = np.asarray(array, dtype=np.float64)
        self.assert_almost_mc_ci(array)
