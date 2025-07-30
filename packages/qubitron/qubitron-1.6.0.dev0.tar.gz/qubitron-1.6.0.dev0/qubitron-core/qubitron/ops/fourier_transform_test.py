# Copyright 2019 The Qubitron Developers
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


def test_phase_gradient():
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhaseGradientGate(num_qubits=2, exponent=1)), np.diag([1, 1j, -1, -1j])
    )

    for k in range(4):
        qubitron.testing.assert_implements_consistent_protocols(
            qubitron.PhaseGradientGate(num_qubits=k, exponent=1)
        )


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_phase_gradient_symbolic(resolve_fn):
    a = qubitron.PhaseGradientGate(num_qubits=2, exponent=0.5)
    b = qubitron.PhaseGradientGate(num_qubits=2, exponent=sympy.Symbol('t'))
    assert not qubitron.is_parameterized(a)
    assert qubitron.is_parameterized(b)
    assert qubitron.has_unitary(a)
    assert not qubitron.has_unitary(b)
    assert resolve_fn(a, {'t': 0.25}) is a
    assert resolve_fn(b, {'t': 0.5}) == a
    assert resolve_fn(b, {'t': 0.25}) == qubitron.PhaseGradientGate(num_qubits=2, exponent=0.25)


def test_str():
    assert str(qubitron.PhaseGradientGate(num_qubits=2, exponent=0.5)) == 'Grad[2]^0.5'
    assert str(qubitron.PhaseGradientGate(num_qubits=2, exponent=1)) == 'Grad[2]'


def test_phase_gradient_gate_repr():
    a = qubitron.PhaseGradientGate(num_qubits=2, exponent=0.5)
    qubitron.testing.assert_equivalent_repr(a)


def test_quantum_fourier_transform_gate_repr():
    b = qubitron.QuantumFourierTransformGate(num_qubits=2, without_reverse=False)
    qubitron.testing.assert_equivalent_repr(b)


def test_pow():
    a = qubitron.PhaseGradientGate(num_qubits=2, exponent=0.5)
    assert a**0.5 == qubitron.PhaseGradientGate(num_qubits=2, exponent=0.25)
    assert a ** sympy.Symbol('t') == qubitron.PhaseGradientGate(
        num_qubits=2, exponent=0.5 * sympy.Symbol('t')
    )


def test_qft():
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.qft(*qubitron.LineQubit.range(2))),
        np.array(
            [
                [1, 1, 1, 1],
                [1, 1j, -1, -1j],
                [1, -1, 1, -1],
                [1, -1j, -1, 1j],
            ]
        )
        / 2,
        atol=1e-8,
    )

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.qft(*qubitron.LineQubit.range(2), without_reverse=True)),
        np.array(
            [
                [1, 1, 1, 1],
                [1, -1, 1, -1],
                [1, 1j, -1, -1j],
                [1, -1j, -1, 1j],
            ]
        )
        / 2,
        atol=1e-8,
    )
    # fmt: on

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.qft(*qubitron.LineQubit.range(4))),
        np.array([[np.exp(2j * np.pi * i * j / 16) for i in range(16)] for j in range(16)]) / 4,
        atol=1e-8,
    )

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.qft(*qubitron.LineQubit.range(2)) ** -1),
        np.array([[1, 1, 1, 1], [1, -1j, -1, 1j], [1, -1, 1, -1], [1, 1j, -1, -1j]]) / 2,
        atol=1e-8,
    )

    for k in range(4):
        for b in [False, True]:
            qubitron.testing.assert_implements_consistent_protocols(
                qubitron.QuantumFourierTransformGate(num_qubits=k, without_reverse=b)
            )


def test_inverse():
    a, b, c = qubitron.LineQubit.range(3)
    assert qubitron.qft(a, b, c, inverse=True) == qubitron.qft(a, b, c) ** -1
    assert qubitron.qft(a, b, c, inverse=True, without_reverse=True) == qubitron.inverse(
        qubitron.qft(a, b, c, without_reverse=True)
    )


def test_circuit_diagram():
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.decompose_once(qubitron.qft(*qubitron.LineQubit.range(4)))),
        """
0: ───H───Grad^0.5───────#2─────────────#3─────────────×───
          │              │              │              │
1: ───────@──────────H───Grad^0.5───────#2─────────×───┼───
                         │              │          │   │
2: ──────────────────────@──────────H───Grad^0.5───×───┼───
                                        │              │
3: ─────────────────────────────────────@──────────H───×───
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.decompose_once(qubitron.qft(*qubitron.LineQubit.range(4), without_reverse=True))),
        """
0: ───H───Grad^0.5───────#2─────────────#3─────────────
          │              │              │
1: ───────@──────────H───Grad^0.5───────#2─────────────
                         │              │
2: ──────────────────────@──────────H───Grad^0.5───────
                                        │
3: ─────────────────────────────────────@──────────H───
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.qft(*qubitron.LineQubit.range(4)), qubitron.inverse(qubitron.qft(*qubitron.LineQubit.range(4)))
        ),
        """
0: ───qft───qft^-1───
      │     │
1: ───#2────#2───────
      │     │
2: ───#3────#3───────
      │     │
3: ───#4────#4───────
        """,
    )
