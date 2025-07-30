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

import pytest

import qubitron

Q, Q2, Q3 = qubitron.LineQubit.range(3)


@pytest.mark.parametrize(
    "op,expected",
    [
        (qubitron.H(Q), False),
        (qubitron.HPowGate(exponent=0.5)(Q), False),
        (qubitron.PhasedXPowGate(exponent=0.25, phase_exponent=0.125)(Q), True),
        (qubitron.XPowGate(exponent=0.5)(Q), True),
        (qubitron.YPowGate(exponent=0.25)(Q), True),
        (qubitron.ZPowGate(exponent=0.125)(Q), True),
        (qubitron.CZPowGate(exponent=0.5)(Q, Q2), False),
        (qubitron.CZ(Q, Q2), True),
        (qubitron.CNOT(Q, Q2), True),
        (qubitron.SWAP(Q, Q2), False),
        (qubitron.ISWAP(Q, Q2), False),
        (qubitron.CCNOT(Q, Q2, Q3), True),
        (qubitron.CCZ(Q, Q2, Q3), True),
        (qubitron.ParallelGate(qubitron.X, num_copies=3)(Q, Q2, Q3), True),
        (qubitron.ParallelGate(qubitron.Y, num_copies=3)(Q, Q2, Q3), True),
        (qubitron.ParallelGate(qubitron.Z, num_copies=3)(Q, Q2, Q3), True),
        (qubitron.X(Q).controlled_by(Q2, Q3), True),
        (qubitron.Z(Q).controlled_by(Q2, Q3), True),
        (qubitron.ZPowGate(exponent=0.5)(Q).controlled_by(Q2, Q3), False),
    ],
)
def test_gateset(op: qubitron.Operation, expected: bool) -> None:
    assert qubitron.is_native_neutral_atom_op(op) == expected
    if op.gate is not None:
        assert qubitron.is_native_neutral_atom_gate(op.gate) == expected
