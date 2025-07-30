# Copyright 2022 The Qubitron Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import Any

import numpy as np

import qubitron


def assert_consistent_channel(gate: Any, rtol: float = 1e-5, atol: float = 1e-8):
    """Asserts that a given gate has Kraus operators and that they are properly normalized."""
    assert qubitron.has_kraus(gate), f"Given gate {gate!r} does not return True for qubitron.has_kraus."
    kraus_ops = qubitron.kraus(gate)
    assert qubitron.is_cptp(kraus_ops=kraus_ops, rtol=rtol, atol=atol), (
        f"Kraus operators for {gate!r} did not sum to identity up to expected tolerances. "
        f"Summed to {sum(m.T.conj() @ m for m in kraus_ops)}"
    )


def assert_consistent_mixture(gate: Any, rtol: float = 1e-5, atol: float = 1e-8):
    """Asserts that a given gate is a mixture and the mixture probabilities sum to one."""
    assert qubitron.has_mixture(gate), f"Give gate {gate!r} does not return for qubitron.has_mixture."
    mixture = qubitron.mixture(gate)
    total = np.sum(np.fromiter((k for k, v in mixture), dtype=float))
    assert np.abs(1 - total) <= atol + rtol * np.abs(total), (
        f"The mixture for gate {gate!r} did not return coefficients that sum to 1. Summed to "
        f"{total}."
    )
