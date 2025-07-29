# Copyright (C) 2023 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

import argparse

import pandas as pd
import statisticalagreement as sa
from examples import examples

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exampleCat", "-et", required=False, action="store_true")
    parser.add_argument("--exampleCon", "-en", required=False, action="store_true")
    parser.add_argument("--test", "-t", required=False, action="store_true")
    parser.add_argument("--simulation","-s", required=False, nargs="*")

    args = parser.parse_args()

    if args.simulation:
        name_of_index, res = sa.mc_simulation(*args.simulation)
        print(f"{name_of_index} with normal data:")
        print(pd.DataFrame(res), "\n")

    if args.exampleCat:
        examples.main(categorical=True)

    if args.exampleCon:
        examples.main(continuous=True)
