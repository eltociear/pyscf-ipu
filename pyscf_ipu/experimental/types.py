# Copyright (c) 2023 Graphcore Ltd. All rights reserved.
from jaxtyping import Float, Int, Array


Float3 = Float[Array, "3"]
FloatNx3 = Float[Array, "N 3"]
FloatN = Float[Array, "N"]
FloatNxN = Float[Array, "N N"]
FloatNxM = Float[Array, "N M"]
Int3 = Int[Array, "3"]
IntN = Int[Array, "N"]
