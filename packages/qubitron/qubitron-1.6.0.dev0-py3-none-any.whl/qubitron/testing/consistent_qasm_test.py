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

import warnings

import numpy as np
import pytest

import qubitron


class Fixed(qubitron.Operation):
    def __init__(self, unitary: np.ndarray, qasm: str) -> None:
        self.unitary = unitary
        self.qasm = qasm

    def _unitary_(self):
        return self.unitary

    @property
    def qubits(self):
        return qubitron.LineQubit.range(self.unitary.shape[0].bit_length() - 1)

    def with_qubits(self, *new_qubits):
        raise NotImplementedError()

    def _qasm_(self, args: qubitron.QasmArgs):
        return args.format(self.qasm, *self.qubits)


class QuditGate(qubitron.Gate):
    def _qid_shape_(self) -> tuple[int, ...]:
        return (3, 3)

    def _unitary_(self):
        return np.eye(9)

    def _qasm_(self, args: qubitron.QasmArgs, qubits: tuple[qubitron.Qid, ...]):
        return NotImplemented


def test_assert_qasm_is_consistent_with_unitary() -> None:
    try:
        import qiskit as _
    except ImportError:  # pragma: no cover
        warnings.warn(
            "Skipped test_assert_qasm_is_consistent_with_unitary "
            "because qiskit isn't installed to verify against."
        )
        return

    # Checks matrix.
    qubitron.testing.assert_qasm_is_consistent_with_unitary(
        Fixed(np.array([[1, 0], [0, 1]]), 'z {0}; z {0};')
    )
    qubitron.testing.assert_qasm_is_consistent_with_unitary(
        Fixed(np.array([[1, 0], [0, -1]]), 'z {0};')
    )
    with pytest.raises(AssertionError, match='Not equal'):
        qubitron.testing.assert_qasm_is_consistent_with_unitary(
            Fixed(np.array([[1, 0], [0, -1]]), 'x {0};')
        )

    # Checks qubit ordering.
    qubitron.testing.assert_qasm_is_consistent_with_unitary(qubitron.CNOT)
    qubitron.testing.assert_qasm_is_consistent_with_unitary(
        qubitron.CNOT.on(qubitron.NamedQubit('a'), qubitron.NamedQubit('b'))
    )
    qubitron.testing.assert_qasm_is_consistent_with_unitary(
        qubitron.CNOT.on(qubitron.NamedQubit('b'), qubitron.NamedQubit('a'))
    )

    # Checks that code is valid.
    with pytest.raises(AssertionError, match='QASM not consistent'):
        qubitron.testing.assert_qasm_is_consistent_with_unitary(
            Fixed(np.array([[1, 0], [0, -1]]), 'JUNK$&*@($#::=[];')
        )

    # Checks that the test handles qudits
    qubitron.testing.assert_qasm_is_consistent_with_unitary(QuditGate())
