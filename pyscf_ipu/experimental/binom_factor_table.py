# Copyright (c) 2023 Graphcore Ltd. All rights reserved.
# AUTOGENERATED from notebooks/binom_factor_table.ipynb

# fmt: off
# flake8: noqa
# isort: skip_file

import jax.numpy as jnp
import numpy as np
array = np.array

LMAX = 8
def get_monomials(a,b):
    a_pows = a ** jnp.arange(LMAX)
    b_pows = b ** jnp.arange(LMAX)
    ans = a_pows.reshape(LMAX,1) @ b_pows.reshape(1,LMAX)
    return ans.reshape(LMAX*LMAX)


def build_binom_factor_table(sparse=False):
    inds,values = ((array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7]), array([0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6,
       6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 1, 1, 1, 1, 2, 2,
       2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0,
       1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 1, 1, 1, 1, 1,
       1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 1, 1,
       1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0,
       0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
       2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 7, 7, 7, 7]), array([0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 0,
       1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 0, 1, 1, 2, 0, 1,
       1, 2, 2, 3, 0, 1, 1, 2, 2, 3, 3, 4, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5,
       0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5,
       5, 6, 6, 7, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 0, 1, 2,
       0, 1, 1, 2, 2, 3, 0, 1, 1, 2, 2, 2, 3, 3, 4, 0, 1, 1, 2, 2, 2, 3,
       3, 3, 4, 4, 5, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6, 0, 1,
       1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 0, 1, 1, 2, 2, 2,
       3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3,
       3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 0, 1, 2, 3, 0, 1, 1, 2, 2,
       3, 3, 4, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 0, 1, 1, 2, 2, 2, 3,
       3, 3, 3, 4, 4, 4, 5, 5, 6, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4,
       4, 5, 5, 5, 6, 6, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5,
       5, 5, 5, 6, 6, 6, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
       5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
       4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 0, 1, 2, 3, 4, 0, 1,
       1, 2, 2, 3, 3, 4, 4, 5, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5,
       6, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 0,
       1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7,
       7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6,
       6, 6, 6, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5,
       5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3,
       3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 0,
       1, 2, 3, 4, 5, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 0, 1, 1, 2, 2,
       2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3,
       3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3,
       3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 0, 1, 1,
       2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6,
       6, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5,
       5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3,
       3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7,
       7, 7, 7, 7, 0, 1, 2, 3, 4, 5, 6, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,
       6, 6, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7,
       7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6,
       6, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
       5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
       4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 0,
       1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6,
       6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4,
       4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7,
       7, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6,
       6, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7,
       7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6,
       6, 6, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5,
       5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3,
       3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7,
       7, 7, 7, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5,
       5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 0, 1, 1, 2, 2, 2,
       3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6,
       7, 7, 7, 7, 7, 7, 7, 7]), array([ 0,  1,  0,  2,  1,  0,  3,  2,  1,  0,  4,  3,  2,  1,  0,  5,  4,
        3,  2,  1,  0,  6,  5,  4,  3,  2,  1,  0,  7,  6,  5,  4,  3,  2,
        1,  0,  8,  0,  9,  1,  8,  0, 10,  2,  9,  1,  8,  0, 11,  3, 10,
        2,  9,  1,  8,  0, 12,  4, 11,  3, 10,  2,  9,  1,  8,  0, 13,  5,
       12,  4, 11,  3, 10,  2,  9,  1,  8,  0, 14,  6, 13,  5, 12,  4, 11,
        3, 10,  2,  9,  1,  8,  0, 15,  7, 14,  6, 13,  5, 12,  4, 11,  3,
       10,  2,  9,  1,  8, 16,  8,  0, 17,  9, 16,  1,  8,  0, 18, 10, 17,
        2,  9, 16,  1,  8,  0, 19, 11, 18,  3, 10, 17,  2,  9, 16,  1,  8,
        0, 20, 12, 19,  4, 11, 18,  3, 10, 17,  2,  9, 16,  1,  8,  0, 21,
       13, 20,  5, 12, 19,  4, 11, 18,  3, 10, 17,  2,  9, 16,  1,  8,  0,
       22, 14, 21,  6, 13, 20,  5, 12, 19,  4, 11, 18,  3, 10, 17,  2,  9,
       16,  1,  8, 23, 15, 22,  7, 14, 21,  6, 13, 20,  5, 12, 19,  4, 11,
       18,  3, 10, 17,  2,  9, 16, 24, 16,  8,  0, 25, 17, 24,  9, 16,  1,
        8,  0, 26, 18, 25, 10, 17, 24,  2,  9, 16,  1,  8,  0, 27, 19, 26,
       11, 18, 25,  3, 10, 17, 24,  2,  9, 16,  1,  8,  0, 28, 20, 27, 12,
       19, 26,  4, 11, 18, 25,  3, 10, 17, 24,  2,  9, 16,  1,  8,  0, 29,
       21, 28, 13, 20, 27,  5, 12, 19, 26,  4, 11, 18, 25,  3, 10, 17, 24,
        2,  9, 16,  1,  8, 30, 22, 29, 14, 21, 28,  6, 13, 20, 27,  5, 12,
       19, 26,  4, 11, 18, 25,  3, 10, 17, 24,  2,  9, 16, 31, 23, 30, 15,
       22, 29,  7, 14, 21, 28,  6, 13, 20, 27,  5, 12, 19, 26,  4, 11, 18,
       25,  3, 10, 17, 24, 32, 24, 16,  8,  0, 33, 25, 32, 17, 24,  9, 16,
        1,  8,  0, 34, 26, 33, 18, 25, 32, 10, 17, 24,  2,  9, 16,  1,  8,
        0, 35, 27, 34, 19, 26, 33, 11, 18, 25, 32,  3, 10, 17, 24,  2,  9,
       16,  1,  8,  0, 36, 28, 35, 20, 27, 34, 12, 19, 26, 33,  4, 11, 18,
       25, 32,  3, 10, 17, 24,  2,  9, 16,  1,  8, 37, 29, 36, 21, 28, 35,
       13, 20, 27, 34,  5, 12, 19, 26, 33,  4, 11, 18, 25, 32,  3, 10, 17,
       24,  2,  9, 16, 38, 30, 37, 22, 29, 36, 14, 21, 28, 35,  6, 13, 20,
       27, 34,  5, 12, 19, 26, 33,  4, 11, 18, 25, 32,  3, 10, 17, 24, 39,
       31, 38, 23, 30, 37, 15, 22, 29, 36,  7, 14, 21, 28, 35,  6, 13, 20,
       27, 34,  5, 12, 19, 26, 33,  4, 11, 18, 25, 32, 40, 32, 24, 16,  8,
        0, 41, 33, 40, 25, 32, 17, 24,  9, 16,  1,  8,  0, 42, 34, 41, 26,
       33, 40, 18, 25, 32, 10, 17, 24,  2,  9, 16,  1,  8,  0, 43, 35, 42,
       27, 34, 41, 19, 26, 33, 40, 11, 18, 25, 32,  3, 10, 17, 24,  2,  9,
       16,  1,  8, 44, 36, 43, 28, 35, 42, 20, 27, 34, 41, 12, 19, 26, 33,
       40,  4, 11, 18, 25, 32,  3, 10, 17, 24,  2,  9, 16, 45, 37, 44, 29,
       36, 43, 21, 28, 35, 42, 13, 20, 27, 34, 41,  5, 12, 19, 26, 33, 40,
        4, 11, 18, 25, 32,  3, 10, 17, 24, 46, 38, 45, 30, 37, 44, 22, 29,
       36, 43, 14, 21, 28, 35, 42,  6, 13, 20, 27, 34, 41,  5, 12, 19, 26,
       33, 40,  4, 11, 18, 25, 32, 47, 39, 46, 31, 38, 45, 23, 30, 37, 44,
       15, 22, 29, 36, 43,  7, 14, 21, 28, 35, 42,  6, 13, 20, 27, 34, 41,
        5, 12, 19, 26, 33, 40, 48, 40, 32, 24, 16,  8,  0, 49, 41, 48, 33,
       40, 25, 32, 17, 24,  9, 16,  1,  8,  0, 50, 42, 49, 34, 41, 48, 26,
       33, 40, 18, 25, 32, 10, 17, 24,  2,  9, 16,  1,  8, 51, 43, 50, 35,
       42, 49, 27, 34, 41, 48, 19, 26, 33, 40, 11, 18, 25, 32,  3, 10, 17,
       24,  2,  9, 16, 52, 44, 51, 36, 43, 50, 28, 35, 42, 49, 20, 27, 34,
       41, 48, 12, 19, 26, 33, 40,  4, 11, 18, 25, 32,  3, 10, 17, 24, 53,
       45, 52, 37, 44, 51, 29, 36, 43, 50, 21, 28, 35, 42, 49, 13, 20, 27,
       34, 41, 48,  5, 12, 19, 26, 33, 40,  4, 11, 18, 25, 32, 54, 46, 53,
       38, 45, 52, 30, 37, 44, 51, 22, 29, 36, 43, 50, 14, 21, 28, 35, 42,
       49,  6, 13, 20, 27, 34, 41, 48,  5, 12, 19, 26, 33, 40, 55, 47, 54,
       39, 46, 53, 31, 38, 45, 52, 23, 30, 37, 44, 51, 15, 22, 29, 36, 43,
       50,  7, 14, 21, 28, 35, 42, 49,  6, 13, 20, 27, 34, 41, 48, 56, 48,
       40, 32, 24, 16,  8,  0, 57, 49, 56, 41, 48, 33, 40, 25, 32, 17, 24,
        9, 16,  1,  8, 58, 50, 57, 42, 49, 56, 34, 41, 48, 26, 33, 40, 18,
       25, 32, 10, 17, 24,  2,  9, 16, 59, 51, 58, 43, 50, 57, 35, 42, 49,
       56, 27, 34, 41, 48, 19, 26, 33, 40, 11, 18, 25, 32,  3, 10, 17, 24,
       60, 52, 59, 44, 51, 58, 36, 43, 50, 57, 28, 35, 42, 49, 56, 20, 27,
       34, 41, 48, 12, 19, 26, 33, 40,  4, 11, 18, 25, 32, 61, 53, 60, 45,
       52, 59, 37, 44, 51, 58, 29, 36, 43, 50, 57, 21, 28, 35, 42, 49, 56,
       13, 20, 27, 34, 41, 48,  5, 12, 19, 26, 33, 40, 62, 54, 61, 46, 53,
       60, 38, 45, 52, 59, 30, 37, 44, 51, 58, 22, 29, 36, 43, 50, 57, 14,
       21, 28, 35, 42, 49, 56,  6, 13, 20, 27, 34, 41, 48, 63, 55, 62, 47,
       54, 61, 39, 46, 53, 60, 31, 38, 45, 52, 59, 23, 30, 37, 44, 51, 58,
       15, 22, 29, 36, 43, 50, 57,  7, 14, 21, 28, 35, 42, 49, 56])), array([1, 1, 1, 1, 2, 1, 1, 3, 3, 1, 1, 4, 6, 4, 1, 1, 5, 10, 10, 5, 1, 1,
       6, 15, 20, 15, 6, 1, 1, 7, 21, 35, 35, 21, 7, 1, 1, 1, 1, 1, 1, 1,
       1, 1, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 4, 4, 6, 6, 4, 4,
       1, 1, 1, 1, 5, 5, 10, 10, 10, 10, 5, 5, 1, 1, 1, 1, 6, 6, 15, 15,
       20, 20, 15, 15, 6, 6, 1, 1, 1, 1, 7, 7, 21, 21, 35, 35, 35, 35, 21,
       21, 7, 7, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 4, 1, 2, 2, 1,
       1, 2, 3, 1, 6, 3, 3, 6, 1, 3, 2, 1, 1, 2, 4, 1, 8, 6, 4, 12, 4, 6,
       8, 1, 4, 2, 1, 1, 2, 5, 1, 10, 10, 5, 20, 10, 10, 20, 5, 10, 10, 1,
       5, 2, 1, 1, 2, 6, 1, 12, 15, 6, 30, 20, 15, 40, 15, 20, 30, 6, 15,
       12, 1, 6, 2, 1, 2, 7, 1, 14, 21, 7, 42, 35, 21, 70, 35, 35, 70, 21,
       35, 42, 7, 21, 14, 1, 1, 3, 3, 1, 1, 3, 1, 3, 3, 1, 3, 1, 1, 3, 2,
       3, 6, 1, 1, 6, 3, 2, 3, 1, 1, 3, 3, 3, 9, 3, 1, 9, 9, 1, 3, 9, 3,
       3, 3, 1, 1, 3, 4, 3, 12, 6, 1, 12, 18, 4, 4, 18, 12, 1, 6, 12, 3,
       4, 3, 1, 1, 3, 5, 3, 15, 10, 1, 15, 30, 10, 5, 30, 30, 5, 10, 30,
       15, 1, 10, 15, 3, 5, 3, 1, 3, 6, 3, 18, 15, 1, 18, 45, 20, 6, 45,
       60, 15, 15, 60, 45, 6, 20, 45, 18, 1, 15, 18, 3, 1, 3, 7, 3, 21,
       21, 1, 21, 63, 35, 7, 63, 105, 35, 21, 105, 105, 21, 35, 105, 63,
       7, 35, 63, 21, 1, 1, 4, 6, 4, 1, 1, 4, 1, 6, 4, 4, 6, 1, 4, 1, 1,
       4, 2, 6, 8, 1, 4, 12, 4, 1, 8, 6, 2, 4, 1, 1, 4, 3, 6, 12, 3, 4,
       18, 12, 1, 1, 12, 18, 4, 3, 12, 6, 3, 4, 1, 1, 4, 4, 6, 16, 6, 4,
       24, 24, 4, 1, 16, 36, 16, 1, 4, 24, 24, 4, 6, 16, 6, 4, 4, 1, 4, 5,
       6, 20, 10, 4, 30, 40, 10, 1, 20, 60, 40, 5, 5, 40, 60, 20, 1, 10,
       40, 30, 4, 10, 20, 6, 1, 4, 6, 6, 24, 15, 4, 36, 60, 20, 1, 24, 90,
       80, 15, 6, 60, 120, 60, 6, 15, 80, 90, 24, 1, 20, 60, 36, 4, 1, 4,
       7, 6, 28, 21, 4, 42, 84, 35, 1, 28, 126, 140, 35, 7, 84, 210, 140,
       21, 21, 140, 210, 84, 7, 35, 140, 126, 28, 1, 1, 5, 10, 10, 5, 1,
       1, 5, 1, 10, 5, 10, 10, 5, 10, 1, 5, 1, 1, 5, 2, 10, 10, 1, 10, 20,
       5, 5, 20, 10, 1, 10, 10, 2, 5, 1, 1, 5, 3, 10, 15, 3, 10, 30, 15,
       1, 5, 30, 30, 5, 1, 15, 30, 10, 3, 15, 10, 3, 5, 1, 5, 4, 10, 20,
       6, 10, 40, 30, 4, 5, 40, 60, 20, 1, 1, 20, 60, 40, 5, 4, 30, 40,
       10, 6, 20, 10, 1, 5, 5, 10, 25, 10, 10, 50, 50, 10, 5, 50, 100, 50,
       5, 1, 25, 100, 100, 25, 1, 5, 50, 100, 50, 5, 10, 50, 50, 10, 1, 5,
       6, 10, 30, 15, 10, 60, 75, 20, 5, 60, 150, 100, 15, 1, 30, 150,
       200, 75, 6, 6, 75, 200, 150, 30, 1, 15, 100, 150, 60, 5, 1, 5, 7,
       10, 35, 21, 10, 70, 105, 35, 5, 70, 210, 175, 35, 1, 35, 210, 350,
       175, 21, 7, 105, 350, 350, 105, 7, 21, 175, 350, 210, 35, 1, 1, 6,
       15, 20, 15, 6, 1, 1, 6, 1, 15, 6, 20, 15, 15, 20, 6, 15, 1, 6, 1,
       1, 6, 2, 15, 12, 1, 20, 30, 6, 15, 40, 15, 6, 30, 20, 1, 12, 15, 2,
       6, 1, 6, 3, 15, 18, 3, 20, 45, 18, 1, 15, 60, 45, 6, 6, 45, 60, 15,
       1, 18, 45, 20, 3, 18, 15, 1, 6, 4, 15, 24, 6, 20, 60, 36, 4, 15,
       80, 90, 24, 1, 6, 60, 120, 60, 6, 1, 24, 90, 80, 15, 4, 36, 60, 20,
       1, 6, 5, 15, 30, 10, 20, 75, 60, 10, 15, 100, 150, 60, 5, 6, 75,
       200, 150, 30, 1, 1, 30, 150, 200, 75, 6, 5, 60, 150, 100, 15, 1, 6,
       6, 15, 36, 15, 20, 90, 90, 20, 15, 120, 225, 120, 15, 6, 90, 300,
       300, 90, 6, 1, 36, 225, 400, 225, 36, 1, 6, 90, 300, 300, 90, 6, 1,
       6, 7, 15, 42, 21, 20, 105, 126, 35, 15, 140, 315, 210, 35, 6, 105,
       420, 525, 210, 21, 1, 42, 315, 700, 525, 126, 7, 7, 126, 525, 700,
       315, 42, 1, 1, 7, 21, 35, 35, 21, 7, 1, 1, 7, 1, 21, 7, 35, 21, 35,
       35, 21, 35, 7, 21, 1, 7, 1, 7, 2, 21, 14, 1, 35, 42, 7, 35, 70, 21,
       21, 70, 35, 7, 42, 35, 1, 14, 21, 1, 7, 3, 21, 21, 3, 35, 63, 21,
       1, 35, 105, 63, 7, 21, 105, 105, 21, 7, 63, 105, 35, 1, 21, 63, 35,
       1, 7, 4, 21, 28, 6, 35, 84, 42, 4, 35, 140, 126, 28, 1, 21, 140,
       210, 84, 7, 7, 84, 210, 140, 21, 1, 28, 126, 140, 35, 1, 7, 5, 21,
       35, 10, 35, 105, 70, 10, 35, 175, 210, 70, 5, 21, 175, 350, 210,
       35, 1, 7, 105, 350, 350, 105, 7, 1, 35, 210, 350, 175, 21, 1, 7, 6,
       21, 42, 15, 35, 126, 105, 20, 35, 210, 315, 140, 15, 21, 210, 525,
       420, 105, 6, 7, 126, 525, 700, 315, 42, 1, 1, 42, 315, 700, 525,
       126, 7, 1, 7, 7, 21, 49, 21, 35, 147, 147, 35, 35, 245, 441, 245,
       35, 21, 245, 735, 735, 245, 21, 7, 147, 735, 1225, 735, 147, 7, 1,
       49, 441, 1225, 1225, 441, 49, 1]))
    if sparse:
      return inds,values
    else:
      W = np.zeros((LMAX,LMAX,LMAX,LMAX*LMAX))
      W[inds] = values
      return W