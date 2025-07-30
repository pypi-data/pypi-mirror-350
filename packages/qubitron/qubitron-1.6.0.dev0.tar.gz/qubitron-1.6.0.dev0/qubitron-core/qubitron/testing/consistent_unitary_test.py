# Copyright 2023 The Qubitron Developers
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


class InconsistentGate(qubitron.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self) -> np.ndarray:
        return np.eye(2, dtype=np.complex128)

    def _decompose_with_context_(self, qubits, *, context):
        (q,) = context.qubit_manager.qalloc(1)
        yield qubitron.X(q)
        yield qubitron.CNOT(q, qubits[0])


class FailsOnDecompostion(qubitron.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self) -> np.ndarray:
        return np.eye(2, dtype=np.complex128)

    def _has_unitary_(self) -> bool:
        return True

    def _decompose_with_context_(self, qubits, *, context):
        (q,) = context.qubit_manager.qalloc(1)
        yield qubitron.X(q)
        yield qubitron.measure(qubits[0])


class CleanCorrectButBorrowableIncorrectGate(qubitron.Gate):
    """Ancilla type determines if the decomposition is correct or not."""

    def __init__(self, use_clean_ancilla: bool) -> None:
        self.ancillas_are_clean = use_clean_ancilla

    def _num_qubits_(self):
        return 2

    def _decompose_with_context_(self, qubits, *, context):
        if self.ancillas_are_clean:
            anc = context.qubit_manager.qalloc(1)
        else:
            anc = context.qubit_manager.qborrow(1)
        yield qubitron.CCNOT(*qubits, *anc)
        yield qubitron.Z(*anc)
        yield qubitron.CCNOT(*qubits, *anc)
        context.qubit_manager.qfree(anc)


@pytest.mark.parametrize('ignore_phase', [False, True])
@pytest.mark.parametrize(
    'g,is_consistent',
    [
        (qubitron.testing.PhaseUsingCleanAncilla(theta=0.1, ancilla_bitsize=3), True),
        (qubitron.testing.PhaseUsingDirtyAncilla(phase_state=1, ancilla_bitsize=4), True),
        (InconsistentGate(), False),
        (CleanCorrectButBorrowableIncorrectGate(use_clean_ancilla=True), True),
        (CleanCorrectButBorrowableIncorrectGate(use_clean_ancilla=False), False),
    ],
)
def test_assert_unitary_is_consistent(g, ignore_phase, is_consistent) -> None:
    if is_consistent:
        qubitron.testing.assert_unitary_is_consistent(g, ignore_phase)
        qubitron.testing.assert_unitary_is_consistent(g.on(*qubitron.LineQid.for_gate(g)), ignore_phase)
    else:
        with pytest.raises(AssertionError):
            qubitron.testing.assert_unitary_is_consistent(g, ignore_phase)
        with pytest.raises(AssertionError):
            qubitron.testing.assert_unitary_is_consistent(g.on(*qubitron.LineQid.for_gate(g)), ignore_phase)


def test_failed_decomposition() -> None:
    with pytest.raises(ValueError):
        qubitron.testing.assert_unitary_is_consistent(FailsOnDecompostion())

    _ = qubitron.testing.assert_unitary_is_consistent(qubitron.Circuit())
