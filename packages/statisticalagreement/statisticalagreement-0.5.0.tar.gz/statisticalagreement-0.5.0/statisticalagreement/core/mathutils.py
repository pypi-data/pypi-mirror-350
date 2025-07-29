# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import numpy as np

def almost_equal_float(first: float, second: float, max_ulps: int=4) -> bool:
    """
    Asserts if two floats are almost equal.

    Parameters
    ----------
    first : float
    second : float
    max_ulps : int, default: 4
        Maximum difference of ulp to assert equality.

    Returns
    -------
    bool

    Examples
    --------
    >>> almost_equal_float(1.0, 1.01)
    False
    """
    # using difference of ulp as a more reliable way to test equality in float/double
    # same method as used in GoogleTest C++ library
    # see https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/

    # catching number with difference of sign and inf/nan
    if first < 0 != second < 0:

        # 0 == -0 can't be catched by integer representation
        if first == second:
            return True
        return False

    first_int = np.array(first).view("int64")
    second_int = np.array(second).view("int64")

    ulps_diff = abs(first_int - second_int)

    if ulps_diff < max_ulps:
        return True

    return False
