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

import qubitron

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])


class GoodGateExplicitPauliExpansion(qubitron.testing.SingleQubitGate):
    def _unitary_(self) -> np.ndarray:
        return np.sqrt(1 / 2) * X + np.sqrt(1 / 3) * Y + np.sqrt(1 / 6) * Z

    def _pauli_expansion_(self) -> qubitron.LinearDict[str]:
        return qubitron.LinearDict({'X': np.sqrt(1 / 2), 'Y': np.sqrt(1 / 3), 'Z': np.sqrt(1 / 6)})


class GoodGateNoPauliExpansion(qubitron.Gate):
    def num_qubits(self) -> int:
        return 4  # pragma: no cover


class GoodGateNoUnitary(qubitron.testing.SingleQubitGate):
    def _pauli_expansion_(self) -> qubitron.LinearDict[str]:
        return qubitron.LinearDict({'X': np.sqrt(1 / 2), 'Y': np.sqrt(1 / 2)})


class GoodGateNoPauliExpansionNoUnitary(qubitron.testing.SingleQubitGate):
    pass


class BadGateInconsistentPauliExpansion(qubitron.testing.SingleQubitGate):
    def _unitary_(self) -> np.ndarray:
        return np.sqrt(1 / 2) * X + np.sqrt(1 / 3) * Y + np.sqrt(1 / 6) * Z

    def _pauli_expansion_(self) -> qubitron.LinearDict[str]:
        return qubitron.LinearDict({'X': np.sqrt(1 / 6), 'Y': np.sqrt(1 / 3), 'Z': np.sqrt(1 / 2)})


def test_assert_pauli_expansion_is_consistent_with_unitary() -> None:
    qubitron.testing.assert_pauli_expansion_is_consistent_with_unitary(GoodGateExplicitPauliExpansion())
    qubitron.testing.assert_pauli_expansion_is_consistent_with_unitary(GoodGateNoPauliExpansion())
    qubitron.testing.assert_pauli_expansion_is_consistent_with_unitary(GoodGateNoUnitary())
    qubitron.testing.assert_pauli_expansion_is_consistent_with_unitary(
        GoodGateNoPauliExpansionNoUnitary()
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_pauli_expansion_is_consistent_with_unitary(
            BadGateInconsistentPauliExpansion()
        )
