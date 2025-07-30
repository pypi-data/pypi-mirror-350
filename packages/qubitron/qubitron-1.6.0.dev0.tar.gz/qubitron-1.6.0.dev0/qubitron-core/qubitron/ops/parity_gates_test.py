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

"""Tests for `parity_gates.py`."""

from __future__ import annotations

import numpy as np
import pytest
import sympy

import qubitron


@pytest.mark.parametrize('eigen_gate_type', [qubitron.XXPowGate, qubitron.YYPowGate, qubitron.ZZPowGate])
def test_eigen_gates_consistent_protocols(eigen_gate_type) -> None:
    qubitron.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


def test_xx_init() -> None:
    assert qubitron.XXPowGate(exponent=1).exponent == 1
    v = qubitron.XXPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_xx_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.XX,
        qubitron.XXPowGate(),
        qubitron.XXPowGate(exponent=1, global_shift=0),
        qubitron.XXPowGate(exponent=3, global_shift=0),
        qubitron.XXPowGate(global_shift=100000),
    )
    eq.add_equality_group(qubitron.XX**0.5, qubitron.XX**2.5, qubitron.XX**4.5)
    eq.add_equality_group(qubitron.XX**0.25, qubitron.XX**2.25, qubitron.XX**-1.75)

    iXX = qubitron.XXPowGate(global_shift=0.5)
    eq.add_equality_group(iXX**0.5, iXX**4.5)
    eq.add_equality_group(iXX**2.5, iXX**6.5)


def test_xx_pow() -> None:
    assert qubitron.XX**0.5 != qubitron.XX**-0.5
    assert qubitron.XX**-1 == qubitron.XX
    assert (qubitron.XX**-1) ** 0.5 == qubitron.XX**-0.5


def test_xx_str() -> None:
    assert str(qubitron.XX) == 'XX'
    assert str(qubitron.XX**0.5) == 'XX**0.5'
    assert str(qubitron.XXPowGate(global_shift=0.1)) == 'XX'


def test_xx_repr() -> None:
    assert repr(qubitron.XXPowGate()) == 'qubitron.XX'
    assert repr(qubitron.XXPowGate(exponent=0.5)) == '(qubitron.XX**0.5)'


def test_xx_matrix() -> None:
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.XX),
        np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(qubitron.unitary(qubitron.XX**2), np.eye(4), atol=1e-8)
    c = np.cos(np.pi / 6)
    s = -1j * np.sin(np.pi / 6)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.XXPowGate(exponent=1 / 3, global_shift=-0.5)),
        np.array([[c, 0, 0, s], [0, c, s, 0], [0, s, c, 0], [s, 0, 0, c]]),
        atol=1e-8,
    )


def test_xx_diagrams() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.XX(a, b), qubitron.XX(a, b) ** 3, qubitron.XX(a, b) ** 0.5)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───XX───XX───XX───────
      │    │    │
b: ───XX───XX───XX^0.5───
""",
    )


def test_yy_init() -> None:
    assert qubitron.YYPowGate(exponent=1).exponent == 1
    v = qubitron.YYPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_yy_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.YY,
        qubitron.YYPowGate(),
        qubitron.YYPowGate(exponent=1, global_shift=0),
        qubitron.YYPowGate(exponent=3, global_shift=0),
    )
    eq.add_equality_group(qubitron.YY**0.5, qubitron.YY**2.5, qubitron.YY**4.5)
    eq.add_equality_group(qubitron.YY**0.25, qubitron.YY**2.25, qubitron.YY**-1.75)

    iYY = qubitron.YYPowGate(global_shift=0.5)
    eq.add_equality_group(iYY**0.5, iYY**4.5)
    eq.add_equality_group(iYY**2.5, iYY**6.5)


def test_yy_pow() -> None:
    assert qubitron.YY**0.5 != qubitron.YY**-0.5
    assert qubitron.YY**-1 == qubitron.YY
    assert (qubitron.YY**-1) ** 0.5 == qubitron.YY**-0.5


def test_yy_str() -> None:
    assert str(qubitron.YY) == 'YY'
    assert str(qubitron.YY**0.5) == 'YY**0.5'
    assert str(qubitron.YYPowGate(global_shift=0.1)) == 'YY'

    iYY = qubitron.YYPowGate(global_shift=0.5)
    assert str(iYY) == 'YY'


def test_yy_repr() -> None:
    assert repr(qubitron.YYPowGate()) == 'qubitron.YY'
    assert repr(qubitron.YYPowGate(exponent=0.5)) == '(qubitron.YY**0.5)'


def test_yy_matrix() -> None:
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.YY),
        np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(qubitron.unitary(qubitron.YY**2), np.eye(4), atol=1e-8)
    c = np.cos(np.pi / 6)
    s = 1j * np.sin(np.pi / 6)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.YYPowGate(exponent=1 / 3, global_shift=-0.5)),
        np.array([[c, 0, 0, s], [0, c, -s, 0], [0, -s, c, 0], [s, 0, 0, c]]),
        atol=1e-8,
    )


def test_yy_diagrams() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.YY(a, b), qubitron.YY(a, b) ** 3, qubitron.YY(a, b) ** 0.5)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───YY───YY───YY───────
      │    │    │
b: ───YY───YY───YY^0.5───
""",
    )


def test_zz_init() -> None:
    assert qubitron.ZZPowGate(exponent=1).exponent == 1
    v = qubitron.ZZPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_zz_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.ZZ,
        qubitron.ZZPowGate(),
        qubitron.ZZPowGate(exponent=1, global_shift=0),
        qubitron.ZZPowGate(exponent=3, global_shift=0),
    )
    eq.add_equality_group(qubitron.ZZ**0.5, qubitron.ZZ**2.5, qubitron.ZZ**4.5)
    eq.add_equality_group(qubitron.ZZ**0.25, qubitron.ZZ**2.25, qubitron.ZZ**-1.75)

    iZZ = qubitron.ZZPowGate(global_shift=0.5)
    eq.add_equality_group(iZZ**0.5, iZZ**4.5)
    eq.add_equality_group(iZZ**2.5, iZZ**6.5)


def test_zz_pow() -> None:
    assert qubitron.ZZ**0.5 != qubitron.ZZ**-0.5
    assert qubitron.ZZ**-1 == qubitron.ZZ
    assert (qubitron.ZZ**-1) ** 0.5 == qubitron.ZZ**-0.5


def test_zz_phase_by() -> None:
    assert qubitron.phase_by(qubitron.ZZ, 0.25, 0) == qubitron.phase_by(qubitron.ZZ, 0.25, 1) == qubitron.ZZ
    assert qubitron.phase_by(qubitron.ZZ**0.5, 0.25, 0) == qubitron.ZZ**0.5
    assert qubitron.phase_by(qubitron.ZZ**-0.5, 0.25, 1) == qubitron.ZZ**-0.5


def test_zz_str() -> None:
    assert str(qubitron.ZZ) == 'ZZ'
    assert str(qubitron.ZZ**0.5) == 'ZZ**0.5'
    assert str(qubitron.ZZPowGate(global_shift=0.1)) == 'ZZ'

    iZZ = qubitron.ZZPowGate(global_shift=0.5)
    assert str(iZZ) == 'ZZ'


def test_zz_repr() -> None:
    assert repr(qubitron.ZZPowGate()) == 'qubitron.ZZ'
    assert repr(qubitron.ZZPowGate(exponent=0.5)) == '(qubitron.ZZ**0.5)'


def test_zz_matrix() -> None:
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.ZZ),
        np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(qubitron.unitary(qubitron.ZZ**2), np.eye(4), atol=1e-8)
    b = 1j**0.25
    a = np.conj(b)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.ZZPowGate(exponent=0.25, global_shift=-0.5)),
        np.array([[a, 0, 0, 0], [0, b, 0, 0], [0, 0, b, 0], [0, 0, 0, a]]),
        atol=1e-8,
    )


def test_zz_diagrams() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.ZZ(a, b), qubitron.ZZ(a, b) ** 3, qubitron.ZZ(a, b) ** 0.5)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───ZZ───ZZ───ZZ───────
      │    │    │
b: ───ZZ───ZZ───ZZ^0.5───
""",
    )


def test_trace_distance() -> None:
    foo = sympy.Symbol('foo')
    assert qubitron.trace_distance_bound(qubitron.XX**foo) == 1.0
    assert qubitron.trace_distance_bound(qubitron.YY**foo) == 1.0
    assert qubitron.trace_distance_bound(qubitron.ZZ**foo) == 1.0
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.XX), 1.0)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.YY**0), 0)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.ZZ ** (1 / 3)), np.sin(np.pi / 6))


def test_ms_arguments() -> None:
    eq_tester = qubitron.testing.EqualsTester()
    eq_tester.add_equality_group(
        qubitron.ms(np.pi / 2), qubitron.MSGate(rads=np.pi / 2), qubitron.XXPowGate(global_shift=-0.5)
    )
    eq_tester.add_equality_group(
        qubitron.ms(np.pi / 4), qubitron.XXPowGate(exponent=0.5, global_shift=-0.5)
    )
    eq_tester.add_equality_group(qubitron.XX)
    eq_tester.add_equality_group(qubitron.XX**0.5)


def test_ms_equal_up_to_global_phase() -> None:
    assert qubitron.equal_up_to_global_phase(qubitron.ms(np.pi / 2), qubitron.XX)
    assert qubitron.equal_up_to_global_phase(qubitron.ms(np.pi / 4), qubitron.XX**0.5)
    assert not qubitron.equal_up_to_global_phase(qubitron.ms(np.pi / 4), qubitron.XX)

    assert qubitron.ms(np.pi / 2) in qubitron.GateFamily(qubitron.XX)
    assert qubitron.ms(np.pi / 4) in qubitron.GateFamily(qubitron.XX**0.5)
    assert qubitron.ms(np.pi / 4) not in qubitron.GateFamily(qubitron.XX)


def test_ms_str() -> None:
    ms = qubitron.ms(np.pi / 2)
    assert str(ms) == 'MS(π/2)'
    assert str(qubitron.ms(np.pi)) == 'MS(2.0π/2)'
    assert str(ms**0.5) == 'MS(0.5π/2)'
    assert str(ms**2) == 'MS(2.0π/2)'
    assert str(ms**-1) == 'MS(-1.0π/2)'


def test_ms_matrix() -> None:
    s = np.sqrt(0.5)
    # yapf: disable
    np.testing.assert_allclose(qubitron.unitary(qubitron.ms(np.pi/4)),
                       np.array([[s, 0, 0, -1j*s],
                                 [0, s, -1j*s, 0],
                                 [0, -1j*s, s, 0],
                                 [-1j*s, 0, 0, s]]),
                                 atol=1e-8)
    # yapf: enable
    np.testing.assert_allclose(qubitron.unitary(qubitron.ms(np.pi)), np.diag([-1, -1, -1, -1]), atol=1e-8)


def test_ms_repr() -> None:
    assert repr(qubitron.ms(np.pi / 2)) == 'qubitron.ms(np.pi/2)'
    assert repr(qubitron.ms(np.pi / 4)) == 'qubitron.ms(0.5*np.pi/2)'
    qubitron.testing.assert_equivalent_repr(qubitron.ms(np.pi / 4))
    ms = qubitron.ms(np.pi / 2)
    assert repr(ms**2) == 'qubitron.ms(2.0*np.pi/2)'
    assert repr(ms**-0.5) == 'qubitron.ms(-0.5*np.pi/2)'


def test_ms_diagrams() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.SWAP(a, b), qubitron.X(a), qubitron.Y(a), qubitron.ms(np.pi).on(a, b))
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───×───X───Y───MS(π)───
      │           │
b: ───×───────────MS(π)───
""",
    )


def test_json_serialization() -> None:
    assert qubitron.read_json(json_text=qubitron.to_json(qubitron.ms(np.pi / 2))) == qubitron.ms(np.pi / 2)


@pytest.mark.parametrize('gate_cls', (qubitron.XXPowGate, qubitron.YYPowGate, qubitron.ZZPowGate))
@pytest.mark.parametrize(
    'exponent,is_clifford',
    ((0, True), (0.5, True), (0.75, False), (1, True), (1.5, True), (-1.5, True)),
)
def test_clifford_protocols(
    gate_cls: type[qubitron.EigenGate], exponent: float, is_clifford: bool
) -> None:
    gate = gate_cls(exponent=exponent)
    assert hasattr(gate, '_decompose_into_clifford_with_qubits_')
    if is_clifford:
        clifford_decomposition = qubitron.Circuit(
            gate._decompose_into_clifford_with_qubits_(qubitron.LineQubit.range(2))
        )
        assert qubitron.has_stabilizer_effect(gate)
        assert qubitron.has_stabilizer_effect(clifford_decomposition)
        if exponent == 0:
            assert clifford_decomposition == qubitron.Circuit()
        else:
            np.testing.assert_allclose(qubitron.unitary(gate), qubitron.unitary(clifford_decomposition))
    else:
        assert not qubitron.has_stabilizer_effect(gate)
        assert gate._decompose_into_clifford_with_qubits_(qubitron.LineQubit.range(2)) is NotImplemented
