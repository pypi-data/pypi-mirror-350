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


class GoodGateDecompose(qubitron.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return qubitron.X(qubits[0])

    def _unitary_(self):
        return np.array([[0, 1], [1, 0]])


class BadGateDecompose(qubitron.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return qubitron.Y(qubits[0])

    def _unitary_(self):
        return np.array([[0, 1], [1, 0]])


def test_assert_decompose_is_consistent_with_unitary() -> None:
    qubitron.testing.assert_decompose_is_consistent_with_unitary(GoodGateDecompose())

    qubitron.testing.assert_decompose_is_consistent_with_unitary(
        GoodGateDecompose().on(qubitron.NamedQubit('q'))
    )

    qubitron.testing.assert_decompose_is_consistent_with_unitary(
        qubitron.testing.PhaseUsingCleanAncilla(theta=0.1, ancilla_bitsize=3)
    )

    qubitron.testing.assert_decompose_is_consistent_with_unitary(
        qubitron.testing.PhaseUsingDirtyAncilla(phase_state=1, ancilla_bitsize=4)
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_is_consistent_with_unitary(BadGateDecompose())

    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_is_consistent_with_unitary(
            BadGateDecompose().on(qubitron.NamedQubit('q'))
        )


class GateDecomposesToDefaultGateset(qubitron.Gate):
    def _num_qubits_(self):
        return 2

    def _decompose_(self, qubits):
        return [GoodGateDecompose().on(qubits[0]), BadGateDecompose().on(qubits[1])]


class GateDecomposeDoesNotEndInDefaultGateset(qubitron.Gate):
    def _num_qubits_(self):
        return 4

    def _decompose_(self, qubits):
        yield GateDecomposeNotImplemented().on_each(*qubits)


class GateDecomposeNotImplemented(qubitron.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return NotImplemented


class ParameterizedGate(qubitron.Gate):
    def _num_qubits_(self):
        return 2

    def _decompose_(self, qubits):
        yield qubitron.X(qubits[0]) ** sympy.Symbol("x")
        yield qubitron.Y(qubits[1]) ** sympy.Symbol("y")


def test_assert_decompose_ends_at_default_gateset() -> None:
    qubitron.testing.assert_decompose_ends_at_default_gateset(GateDecomposesToDefaultGateset())
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        GateDecomposesToDefaultGateset().on(*qubitron.LineQubit.range(2))
    )

    qubitron.testing.assert_decompose_ends_at_default_gateset(ParameterizedGate())
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        ParameterizedGate().on(*qubitron.LineQubit.range(2))
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_ends_at_default_gateset(GateDecomposeNotImplemented())

    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeNotImplemented().on(qubitron.NamedQubit('q'))
        )
    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeDoesNotEndInDefaultGateset()
        )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeDoesNotEndInDefaultGateset().on(*qubitron.LineQubit.range(4))
        )
