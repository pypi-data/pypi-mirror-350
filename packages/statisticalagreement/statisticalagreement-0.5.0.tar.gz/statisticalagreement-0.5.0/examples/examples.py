# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import numpy as np
import pandas as pd
import statisticalagreement as sa

def main(categorical: bool = False, continuous: bool = False) -> None:

    if categorical:
        x_cat = np.repeat([0, 0, 0, 1, 1, 1, 2, 2, 2], [11, 2, 19, 1, 3, 3, 0, 8, 82])
        y_cat = np.repeat([0, 1, 2, 0, 1, 2, 0, 1, 2], [11, 2, 19, 1, 3, 3, 0, 8, 82])
        print(f"Of following contingency Matrix: \n{sa.get_contingency_table(x_cat, y_cat, 3)}\n")
        print(f"Estimate of Cohen's Kappa: {sa.kappa(x_cat, y_cat, method='cohen', alpha=0.05)}")
        print(f"Estimate of Abs Weighted Kappa: {sa.kappa(x_cat, y_cat, method='abs', alpha=0.05)}")
        print(f"Estimate of Sqr Weighted Kappa: {sa.kappa(x_cat, y_cat, method='squared', alpha=0.05)}")

    if continuous:
        x = np.array([12, 10, 13, 10])
        y = np.array([11, 12, 16, 9])

        print(f"Of following continuous data:\nx = {x}\ny = {y}\n")

        # Return approximate estimate of MSD
        # with a alpha risk of 5%
        print(f"Approximate estimate of MSD: {sa.msd(x, y, method='approx', alpha=0.05)}")

        # Return approximate estimate of CCC
        # with a alpha risk of 5%
        # and an allowance of whithin sample deviation of 10%.
        print(f"Approximate estimate of CCC: {sa.ccc(x, y, method='approx', alpha=0.05, allowance=0.10)}")

        # Return approximate estimate of CP with criterion of 2
        # with a alpha risk of 5%
        # and an allowance of 80%.
        print(f"Approximate estimate of CP(2): {sa.cp(x, y, method='approx', alpha=0.05, criterion=2, allowance=0.8)}")

        # Return approximate estimate of TDI with criterion of 90%
        # with a alpha risk of 5%
        # and an allowance of 100.
        print(f"Approximate estimate of TDI(0.90): {sa.tdi(x, y, method='approx', alpha=0.05, criterion=0.9, allowance=100)}")

        print("\nSummary of all indexes:\n")
        # Return estimates of CCC, CP, TDI, MSD and others
        # with a alpha risk of 5%
        # and display a summary of all estimates.
        delta_criterion_for_cp=2
        pi_criterion_for_tdi=0.9

        _, res = sa.agreement(
            x, y,
            delta_criterion_for_cp,
            pi_criterion_for_tdi,
            display=True
        )
        print(pd.DataFrame(res))
