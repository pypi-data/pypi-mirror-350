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

import itertools

import numpy as np
import pytest
import sympy

import qubitron


@pytest.mark.parametrize('eigen_gate_type', [qubitron.CCXPowGate, qubitron.CCZPowGate])
def test_eigen_gates_consistent_protocols(eigen_gate_type) -> None:
    qubitron.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


@pytest.mark.parametrize(
    'gate',
    (
        (qubitron.CSWAP),
        (qubitron.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])),
        (qubitron.ThreeQubitDiagonalGate([0, 0, 0, 0, 0, 0, 0, 0])),
        (qubitron.CCX),
        (qubitron.CCZ),
    ),
)
def test_consistent_protocols(gate) -> None:
    qubitron.testing.assert_implements_consistent_protocols(gate)


def test_init() -> None:
    assert (qubitron.CCZ**0.5).exponent == 0.5
    assert (qubitron.CCZ**0.25).exponent == 0.25
    assert (qubitron.CCX**0.5).exponent == 0.5
    assert (qubitron.CCX**0.25).exponent == 0.25


def test_unitary() -> None:
    assert qubitron.has_unitary(qubitron.CCX)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.CCX),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0],
            ]
        ),
        atol=1e-8,
    )

    assert qubitron.has_unitary(qubitron.CCX**0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.CCX**0.5),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
                [0, 0, 0, 0, 0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
            ]
        ),
        atol=1e-8,
    )

    assert qubitron.has_unitary(qubitron.CCZ)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.CCZ), np.diag([1, 1, 1, 1, 1, 1, 1, -1]), atol=1e-8
    )

    assert qubitron.has_unitary(qubitron.CCZ**0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.CCZ**0.5), np.diag([1, 1, 1, 1, 1, 1, 1, 1j]), atol=1e-8
    )

    assert qubitron.has_unitary(qubitron.CSWAP)
    u = qubitron.unitary(qubitron.CSWAP)
    np.testing.assert_allclose(
        u,
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(u @ u, np.eye(8))

    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    assert qubitron.has_unitary(qubitron.ThreeQubitDiagonalGate(diagonal_angles))
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.ThreeQubitDiagonalGate(diagonal_angles)),
        np.diag([np.exp(1j * angle) for angle in diagonal_angles]),
        atol=1e-8,
    )


def test_str() -> None:
    assert str(qubitron.CCX) == 'TOFFOLI'
    assert str(qubitron.TOFFOLI) == 'TOFFOLI'
    assert str(qubitron.CSWAP) == 'FREDKIN'
    assert str(qubitron.FREDKIN) == 'FREDKIN'
    assert str(qubitron.CCZ) == 'CCZ'

    assert str(qubitron.CCX**0.5) == 'TOFFOLI**0.5'
    assert str(qubitron.CCZ**0.5) == 'CCZ**0.5'


def test_repr() -> None:
    assert repr(qubitron.CCX) == 'qubitron.TOFFOLI'
    assert repr(qubitron.TOFFOLI) == 'qubitron.TOFFOLI'
    assert repr(qubitron.CSWAP) == 'qubitron.FREDKIN'
    assert repr(qubitron.FREDKIN) == 'qubitron.FREDKIN'
    assert repr(qubitron.CCZ) == 'qubitron.CCZ'

    assert repr(qubitron.CCX**0.5) == '(qubitron.TOFFOLI**0.5)'
    assert repr(qubitron.CCZ**0.5) == '(qubitron.CCZ**0.5)'


def test_eq() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.CCZ(a, b, c), qubitron.CCZ(a, c, b), qubitron.CCZ(b, c, a))
    eq.add_equality_group(
        qubitron.CCZ(a, b, c) ** 0.5, qubitron.CCZ(a, c, b) ** 2.5, qubitron.CCZ(b, c, a) ** -1.5
    )
    eq.add_equality_group(
        qubitron.TOFFOLI(a, b, c) ** 0.5, qubitron.TOFFOLI(b, a, c) ** 2.5, qubitron.TOFFOLI(a, b, c) ** -1.5
    )
    eq.add_equality_group(qubitron.CCZ(a, b, d))
    eq.add_equality_group(qubitron.TOFFOLI(a, b, c), qubitron.CCX(a, b, c))
    eq.add_equality_group(qubitron.TOFFOLI(a, c, b), qubitron.TOFFOLI(c, a, b))
    eq.add_equality_group(qubitron.TOFFOLI(a, b, d))
    eq.add_equality_group(qubitron.CSWAP(a, b, c), qubitron.FREDKIN(a, b, c), qubitron.FREDKIN(a, b, c) ** -1)
    eq.add_equality_group(qubitron.CSWAP(b, a, c), qubitron.CSWAP(b, c, a))


def test_gate_equality() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.CSwapGate(), qubitron.CSwapGate())
    eq.add_equality_group(qubitron.CZPowGate(), qubitron.CZPowGate())
    eq.add_equality_group(qubitron.CCXPowGate(), qubitron.CCXPowGate(), qubitron.CCNotPowGate())
    eq.add_equality_group(qubitron.CCZPowGate(), qubitron.CCZPowGate())


def test_identity_multiplication() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    assert qubitron.CCX(a, b, c) * qubitron.I(a) == qubitron.CCX(a, b, c)
    assert qubitron.CCX(a, b, c) * qubitron.I(b) == qubitron.CCX(a, b, c)
    assert qubitron.CCX(a, b, c) ** 0.5 * qubitron.I(c) == qubitron.CCX(a, b, c) ** 0.5
    assert qubitron.I(c) * qubitron.CCZ(a, b, c) ** 0.5 == qubitron.CCZ(a, b, c) ** 0.5


@pytest.mark.parametrize(
    'op,max_two_cost',
    [
        (qubitron.CCZ(*qubitron.LineQubit.range(3)), 8),
        (qubitron.CCX(*qubitron.LineQubit.range(3)), 8),
        (qubitron.CCZ(qubitron.LineQubit(0), qubitron.LineQubit(2), qubitron.LineQubit(1)), 8),
        (qubitron.CCZ(qubitron.LineQubit(0), qubitron.LineQubit(2), qubitron.LineQubit(1)) ** sympy.Symbol("s"), 8),
        (qubitron.CSWAP(*qubitron.LineQubit.range(3)), 9),
        (qubitron.CSWAP(*reversed(qubitron.LineQubit.range(3))), 9),
        (qubitron.CSWAP(qubitron.LineQubit(1), qubitron.LineQubit(0), qubitron.LineQubit(2)), 12),
        (
            qubitron.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])(
                qubitron.LineQubit(1), qubitron.LineQubit(2), qubitron.LineQubit(3)
            ),
            8,
        ),
    ],
)
def test_decomposition_cost(op: qubitron.Operation, max_two_cost: int) -> None:
    ops = tuple(qubitron.flatten_op_tree(qubitron.decompose(op)))
    two_cost = len([e for e in ops if len(e.qubits) == 2])
    over_cost = len([e for e in ops if len(e.qubits) > 2])
    assert over_cost == 0
    assert two_cost == max_two_cost


def test_parameterized_ccz_decompose_no_global_phase() -> None:
    decomposed_ops = qubitron.decompose(qubitron.CCZ(*qubitron.LineQubit.range(3)) ** sympy.Symbol("theta"))
    assert not any(isinstance(op.gate, qubitron.GlobalPhaseGate) for op in decomposed_ops)


def test_diagonal_gate_property() -> None:
    assert qubitron.ThreeQubitDiagonalGate([2, 3, 5, 7, 0, 0, 0, 1]).diag_angles_radians == (
        (2, 3, 5, 7, 0, 0, 0, 1)
    )


@pytest.mark.parametrize(
    'gate',
    [qubitron.CCX, qubitron.CSWAP, qubitron.CCZ, qubitron.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])],
)
def test_decomposition_respects_locality(gate) -> None:
    a = qubitron.GridQubit(0, 0)
    b = qubitron.GridQubit(1, 0)
    c = qubitron.GridQubit(0, 1)
    dev = qubitron.testing.ValidatingTestDevice(qubits={a, b, c}, validate_locality=True)
    for x, y, z in itertools.permutations([a, b, c]):
        circuit = qubitron.Circuit(gate(x, y, z))
        circuit = qubitron.Circuit(qubitron.decompose(circuit))
        dev.validate_circuit(circuit)


def test_diagram() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(
        qubitron.TOFFOLI(a, b, c),
        qubitron.TOFFOLI(a, b, c) ** 0.5,
        qubitron.TOFFOLI(c, b, a) ** 0.5,
        qubitron.CCX(a, c, b),
        qubitron.CCZ(a, d, b),
        qubitron.CCZ(a, d, b) ** 0.5,
        qubitron.CSWAP(a, c, d),
        qubitron.FREDKIN(a, b, c),
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───@───@───────X^0.5───@───@───@───────@───@───
      │   │       │       │   │   │       │   │
1: ───@───@───────@───────X───@───@───────┼───×───
      │   │       │       │   │   │       │   │
2: ───X───X^0.5───@───────@───┼───┼───────×───×───
                              │   │       │
3: ───────────────────────────@───@^0.5───×───────
""",
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ---@---@-------X^0.5---@---@---@-------@------@------
      |   |       |       |   |   |       |      |
1: ---@---@-------@-------X---@---@-------|------swap---
      |   |       |       |   |   |       |      |
2: ---X---X^0.5---@-------@---|---|-------swap---swap---
                              |   |       |
3: ---------------------------@---@^0.5---swap----------
""",
        use_unicode_characters=False,
    )

    diagonal_circuit = qubitron.Circuit(
        qubitron.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])(a, b, c)
    )
    qubitron.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, 5, 7, 11, 13, 17, 19)───
      │
1: ───#2─────────────────────────────────
      │
2: ───#3─────────────────────────────────
""",
    )
    qubitron.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ---diag(2, 3, 5, 7, 11, 13, 17, 19)---
      |
1: ---#2---------------------------------
      |
2: ---#3---------------------------------
""",
        use_unicode_characters=False,
    )


def test_diagonal_exponent() -> None:
    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    diagonal_gate = qubitron.ThreeQubitDiagonalGate(diagonal_angles)

    sqrt_diagonal_gate = diagonal_gate**0.5

    expected_angles = [prime / 2 for prime in diagonal_angles]
    np.testing.assert_allclose(expected_angles, sqrt_diagonal_gate._diag_angles_radians, atol=1e-8)

    assert qubitron.pow(qubitron.ThreeQubitDiagonalGate(diagonal_angles), "test", None) is None


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve(resolve_fn) -> None:
    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    diagonal_gate = qubitron.ThreeQubitDiagonalGate(
        diagonal_angles[:6] + [sympy.Symbol('a'), sympy.Symbol('b')]
    )
    assert qubitron.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'a': 17})
    assert diagonal_gate == qubitron.ThreeQubitDiagonalGate(diagonal_angles[:7] + [sympy.Symbol('b')])
    assert qubitron.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'b': 19})
    assert diagonal_gate == qubitron.ThreeQubitDiagonalGate(diagonal_angles)
    assert not qubitron.is_parameterized(diagonal_gate)


@pytest.mark.parametrize('gate', [qubitron.CCX, qubitron.CCZ, qubitron.CSWAP])
def test_controlled_ops_consistency(gate) -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    assert gate.controlled(0) is gate
    assert gate(a, b, c).controlled_by(d) == gate(d, b, c).controlled_by(a)
