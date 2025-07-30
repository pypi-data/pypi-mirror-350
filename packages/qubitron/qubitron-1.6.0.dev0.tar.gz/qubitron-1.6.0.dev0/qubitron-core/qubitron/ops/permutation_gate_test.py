# Copyright 2020 The Qubitron Developers
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

import qubitron
from qubitron.ops import QubitPermutationGate


def test_permutation_gate_equality() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(
        lambda: QubitPermutationGate([0, 1]), lambda: QubitPermutationGate((0, 1))
    )
    eq.add_equality_group(QubitPermutationGate([1, 0]), QubitPermutationGate((1, 0)))


def test_permutation_gate_repr() -> None:
    qubitron.testing.assert_equivalent_repr(QubitPermutationGate([0, 1]))


rs = np.random.RandomState(seed=1234)


@pytest.mark.parametrize('permutation', [rs.permutation(i) for i in range(3, 7)])
def test_permutation_gate_consistent_protocols(permutation) -> None:
    gate = QubitPermutationGate(list(permutation))
    qubitron.testing.assert_implements_consistent_protocols(gate)


def test_permutation_gate_invalid_indices() -> None:
    with pytest.raises(ValueError, match="Invalid indices"):
        QubitPermutationGate([1, 0, 2, 4])
    with pytest.raises(ValueError, match="Invalid indices"):
        QubitPermutationGate([-1])


def test_permutation_gate_invalid_permutation() -> None:
    with pytest.raises(ValueError, match="Invalid permutation"):
        QubitPermutationGate([1, 1])
    with pytest.raises(ValueError, match="Invalid permutation"):
        QubitPermutationGate([])


def test_permutation_gate_diagram() -> None:
    q = qubitron.LineQubit.range(6)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.X(q[0]), qubitron.X(q[5]), QubitPermutationGate([3, 2, 1, 0]).on(*q[1:5])),
        """
0: ───X───────

1: ───[0>3]───
      │
2: ───[1>2]───
      │
3: ───[2>1]───
      │
4: ───[3>0]───

5: ───X───────
""",
    )


def test_permutation_gate_json_dict() -> None:
    assert qubitron.QubitPermutationGate([0, 1, 2])._json_dict_() == {'permutation': (0, 1, 2)}


@pytest.mark.parametrize(
    'maps, permutation',
    [
        [{0b0: 0b0}, [0]],
        [{0b00: 0b00, 0b01: 0b01, 0b10: 0b10}, [0, 1, 2]],
        [
            {
                0b_000: 0b_000,
                0b_001: 0b_100,
                0b_010: 0b_010,
                0b_100: 0b_001,
                0b_111: 0b_111,
                0b_101: 0b_101,
            },
            [2, 1, 0],
        ],
    ],
)
def test_permutation_gate_maps(maps, permutation) -> None:
    qs = qubitron.LineQubit.range(len(permutation))
    permutationOp = qubitron.QubitPermutationGate(permutation).on(*qs)
    circuit = qubitron.Circuit(permutationOp)
    qubitron.testing.assert_equivalent_computational_basis_map(maps, circuit)
    circuit = qubitron.Circuit(qubitron.I.on_each(*qs), qubitron.decompose(permutationOp))
    qubitron.testing.assert_equivalent_computational_basis_map(maps, circuit)
