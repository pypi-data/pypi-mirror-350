# Copyright 2018 The Qubitron Developers
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

import numpy as np
import pytest
import sympy

import qubitron


def test_canonicalize_half_turns() -> None:
    assert qubitron.canonicalize_half_turns(0) == 0
    assert qubitron.canonicalize_half_turns(1) == +1
    assert qubitron.canonicalize_half_turns(-1) == +1
    assert qubitron.canonicalize_half_turns(0.5) == 0.5
    assert qubitron.canonicalize_half_turns(1.5) == -0.5
    assert qubitron.canonicalize_half_turns(-0.5) == -0.5
    assert qubitron.canonicalize_half_turns(101.5) == -0.5
    # Variable sympy expression
    assert qubitron.canonicalize_half_turns(sympy.Symbol('a')) == sympy.Symbol('a')
    assert qubitron.canonicalize_half_turns(sympy.Symbol('a') + 1) == sympy.Symbol('a') + 1
    # Constant sympy expression
    assert qubitron.canonicalize_half_turns(sympy.Symbol('a') * 0 + 3) == 1


def test_chosen_angle_to_half_turns() -> None:
    assert qubitron.chosen_angle_to_half_turns() == 1
    assert qubitron.chosen_angle_to_half_turns(default=0.5) == 0.5
    assert qubitron.chosen_angle_to_half_turns(half_turns=0.25, default=0.75) == 0.25
    np.testing.assert_allclose(qubitron.chosen_angle_to_half_turns(rads=np.pi / 2), 0.5, atol=1e-8)
    np.testing.assert_allclose(qubitron.chosen_angle_to_half_turns(rads=-np.pi / 4), -0.25, atol=1e-8)
    assert qubitron.chosen_angle_to_half_turns(degs=90) == 0.5
    assert qubitron.chosen_angle_to_half_turns(degs=1080) == 6.0
    assert qubitron.chosen_angle_to_half_turns(degs=990) == 5.5

    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_half_turns(half_turns=0, rads=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_half_turns(half_turns=0, degs=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_half_turns(degs=0, rads=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_half_turns(half_turns=0, rads=0, degs=0)


def test_chosen_angle_to_canonical_half_turns() -> None:
    assert qubitron.chosen_angle_to_canonical_half_turns() == 1
    assert qubitron.chosen_angle_to_canonical_half_turns(default=0.5) == 0.5
    assert qubitron.chosen_angle_to_canonical_half_turns(half_turns=0.25, default=0.75) == 0.25
    np.testing.assert_allclose(
        qubitron.chosen_angle_to_canonical_half_turns(rads=np.pi / 2), 0.5, atol=1e-8
    )
    np.testing.assert_allclose(
        qubitron.chosen_angle_to_canonical_half_turns(rads=-np.pi / 4), -0.25, atol=1e-8
    )
    assert qubitron.chosen_angle_to_canonical_half_turns(degs=90) == 0.5
    assert qubitron.chosen_angle_to_canonical_half_turns(degs=1080) == 0
    assert qubitron.chosen_angle_to_canonical_half_turns(degs=990) == -0.5

    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_canonical_half_turns(half_turns=0, rads=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_canonical_half_turns(half_turns=0, degs=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_canonical_half_turns(degs=0, rads=0)
    with pytest.raises(ValueError):
        _ = qubitron.chosen_angle_to_canonical_half_turns(half_turns=0, rads=0, degs=0)
