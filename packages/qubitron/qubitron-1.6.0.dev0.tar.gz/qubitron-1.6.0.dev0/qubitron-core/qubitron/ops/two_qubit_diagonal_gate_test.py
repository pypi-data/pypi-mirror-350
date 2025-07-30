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
import sympy

import qubitron


@pytest.mark.parametrize(
    'gate',
    (
        (
            qubitron.TwoQubitDiagonalGate([2, 3, 5, 7]),
            qubitron.TwoQubitDiagonalGate([0, 0, 0, 0]),
            qubitron.TwoQubitDiagonalGate([2, 3, 5, sympy.Symbol('a')]),
            qubitron.TwoQubitDiagonalGate([0.34, 0.12, 0, 0.96]),
        )
    ),
)
def test_consistent_protocols(gate) -> None:
    qubitron.testing.assert_implements_consistent_protocols(gate)


def test_property() -> None:
    assert qubitron.TwoQubitDiagonalGate([2, 3, 5, 7]).diag_angles_radians == (2, 3, 5, 7)


def test_parameterized_decompose() -> None:
    angles = sympy.symbols('x0, x1, x2, x3')
    parameterized_op = qubitron.TwoQubitDiagonalGate(angles).on(*qubitron.LineQubit.range(2))
    decomposed_circuit = qubitron.Circuit(qubitron.decompose(parameterized_op))
    for resolver in (
        qubitron.Linspace('x0', -2, 2, 3)
        * qubitron.Linspace('x1', -2, 2, 3)
        * qubitron.Linspace('x2', -2, 2, 3)
        * qubitron.Linspace('x3', -2, 2, 3)
    ):
        np.testing.assert_allclose(
            qubitron.unitary(qubitron.resolve_parameters(parameterized_op, resolver)),
            qubitron.unitary(qubitron.resolve_parameters(decomposed_circuit, resolver)),
        )


def test_unitary() -> None:
    diagonal_angles = [2, 3, 5, 7]
    assert qubitron.has_unitary(qubitron.TwoQubitDiagonalGate(diagonal_angles))
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.TwoQubitDiagonalGate(diagonal_angles)),
        np.diag([np.exp(1j * angle) for angle in diagonal_angles]),
        atol=1e-8,
    )


def test_diagram() -> None:
    a, b = qubitron.LineQubit.range(2)

    diagonal_circuit = qubitron.Circuit(qubitron.TwoQubitDiagonalGate([2, 3, 5, 7])(a, b))
    qubitron.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, 5, 7)───
      │
1: ───#2─────────────────
""",
    )
    qubitron.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ---diag(2, 3, 5, 7)---
      |
1: ---#2-----------------
""",
        use_unicode_characters=False,
    )


def test_diagonal_exponent() -> None:
    diagonal_angles = [2, 3, 5, 7]
    diagonal_gate = qubitron.TwoQubitDiagonalGate(diagonal_angles)

    sqrt_diagonal_gate = diagonal_gate**0.5

    expected_angles = [prime / 2 for prime in diagonal_angles]
    assert qubitron.approx_eq(sqrt_diagonal_gate, qubitron.TwoQubitDiagonalGate(expected_angles))

    assert qubitron.pow(qubitron.TwoQubitDiagonalGate(diagonal_angles), "test", None) is None


def test_protocols_mul_not_implemented() -> None:
    diagonal_angles = [2, 3, None, 7]
    diagonal_gate = qubitron.TwoQubitDiagonalGate(diagonal_angles)
    with pytest.raises(TypeError):
        qubitron.protocols.pow(diagonal_gate, 3)


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve(resolve_fn) -> None:
    diagonal_angles = [2, 3, 5, 7]
    diagonal_gate = qubitron.TwoQubitDiagonalGate(
        diagonal_angles[:2] + [sympy.Symbol('a'), sympy.Symbol('b')]
    )
    assert qubitron.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'a': 5})
    assert diagonal_gate == qubitron.TwoQubitDiagonalGate(diagonal_angles[:3] + [sympy.Symbol('b')])
    assert qubitron.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'b': 7})
    assert diagonal_gate == qubitron.TwoQubitDiagonalGate(diagonal_angles)
    assert not qubitron.is_parameterized(diagonal_gate)
