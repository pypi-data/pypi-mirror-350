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

import re

import numpy as np
import pytest
import sympy

import qubitron

H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
HH = qubitron.kron(H, H)
QFT2 = np.array([[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]]) * 0.5
PLUS_ONE = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def test_single_qubit_init():
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    x2 = qubitron.MatrixGate(m)
    assert qubitron.has_unitary(x2)
    assert np.all(qubitron.unitary(x2) == m)
    assert qubitron.qid_shape(x2) == (2,)

    x2 = qubitron.MatrixGate(PLUS_ONE, qid_shape=(3,))
    assert qubitron.has_unitary(x2)
    assert np.all(qubitron.unitary(x2) == PLUS_ONE)
    assert qubitron.qid_shape(x2) == (3,)

    with pytest.raises(ValueError, match='Not a .*unitary matrix'):
        qubitron.MatrixGate(np.zeros((2, 2)))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        qubitron.MatrixGate(qubitron.eye_tensor((2, 2), dtype=float))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        qubitron.MatrixGate(np.ones((3, 4)))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        qubitron.MatrixGate(np.ones((2, 2, 2)))


def test_single_qubit_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(lambda: qubitron.MatrixGate(np.eye(2)))
    eq.make_equality_group(lambda: qubitron.MatrixGate(np.array([[0, 1], [1, 0]])))
    x2 = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    eq.make_equality_group(lambda: qubitron.MatrixGate(x2))
    eq.add_equality_group(qubitron.MatrixGate(PLUS_ONE, qid_shape=(3,)))


def test_single_qubit_trace_distance_bound():
    x = qubitron.MatrixGate(np.array([[0, 1], [1, 0]]))
    x2 = qubitron.MatrixGate(np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5))
    assert qubitron.trace_distance_bound(x) >= 1
    assert qubitron.trace_distance_bound(x2) >= 0.5


def test_single_qubit_approx_eq():
    x = qubitron.MatrixGate(np.array([[0, 1], [1, 0]]))
    i = qubitron.MatrixGate(np.array([[1, 0], [0, 1]]))
    i_ish = qubitron.MatrixGate(np.array([[1, 0.000000000000001], [0, 1]]))
    assert qubitron.approx_eq(i, i_ish, atol=1e-9)
    assert qubitron.approx_eq(i, i, atol=1e-9)
    assert not qubitron.approx_eq(i, x, atol=1e-9)
    assert not qubitron.approx_eq(i, '', atol=1e-9)


def test_single_qubit_extrapolate():
    i = qubitron.MatrixGate(np.eye(2))
    x = qubitron.MatrixGate(np.array([[0, 1], [1, 0]]))
    x2 = qubitron.MatrixGate(np.array([[1, 1j], [1j, 1]]) * (1 - 1j) / 2)
    assert qubitron.has_unitary(x2)
    x2i = qubitron.MatrixGate(np.conj(qubitron.unitary(x2).T))

    assert qubitron.approx_eq(x**0, i, atol=1e-9)
    assert qubitron.approx_eq(x2**0, i, atol=1e-9)
    assert qubitron.approx_eq(x2**2, x, atol=1e-9)
    assert qubitron.approx_eq(x2**-1, x2i, atol=1e-9)
    assert qubitron.approx_eq(x2**3, x2i, atol=1e-9)
    assert qubitron.approx_eq(x**-1, x, atol=1e-9)

    z2 = qubitron.MatrixGate(np.array([[1, 0], [0, 1j]]))
    z4 = qubitron.MatrixGate(np.array([[1, 0], [0, (1 + 1j) * np.sqrt(0.5)]]))
    assert qubitron.approx_eq(z2**0.5, z4, atol=1e-9)
    with pytest.raises(TypeError):
        _ = x ** sympy.Symbol('a')


def test_two_qubit_init():
    x2 = qubitron.MatrixGate(QFT2)
    assert qubitron.has_unitary(x2)
    assert np.all(qubitron.unitary(x2) == QFT2)


def test_two_qubit_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(lambda: qubitron.MatrixGate(np.eye(4)))
    eq.make_equality_group(lambda: qubitron.MatrixGate(QFT2))
    eq.make_equality_group(lambda: qubitron.MatrixGate(HH))


def test_two_qubit_approx_eq():
    f = qubitron.MatrixGate(QFT2)
    perturb = np.zeros(shape=QFT2.shape, dtype=np.float64)
    perturb[1, 2] = 1e-8

    assert qubitron.approx_eq(f, qubitron.MatrixGate(QFT2), atol=1e-9)

    assert not qubitron.approx_eq(f, qubitron.MatrixGate(QFT2 + perturb), atol=1e-9)
    assert qubitron.approx_eq(f, qubitron.MatrixGate(QFT2 + perturb), atol=1e-7)

    assert not qubitron.approx_eq(f, qubitron.MatrixGate(HH), atol=1e-9)


def test_two_qubit_extrapolate():
    cz2 = qubitron.MatrixGate(np.diag([1, 1, 1, 1j]))
    cz4 = qubitron.MatrixGate(np.diag([1, 1, 1, (1 + 1j) * np.sqrt(0.5)]))
    i = qubitron.MatrixGate(np.eye(4))

    assert qubitron.approx_eq(cz2**0, i, atol=1e-9)
    assert qubitron.approx_eq(cz4**0, i, atol=1e-9)
    assert qubitron.approx_eq(cz2**0.5, cz4, atol=1e-9)
    with pytest.raises(TypeError):
        _ = cz2 ** sympy.Symbol('a')


def test_single_qubit_diagram():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    c = qubitron.Circuit(qubitron.MatrixGate(m).on(a), qubitron.CZ(a, b))

    assert re.match(
        r"""
      ┌[          ]+┐
a: ───│[0-9\.+\-j ]+│───@───
      │[0-9\.+\-j ]+│   │
      └[          ]+┘   │
       [          ]+    │
b: ────[──────────]+────@───
    """.strip(),
        c.to_text_diagram().strip(),
    )

    assert re.match(
        r"""
a[          ]+  b
│[          ]+  │
┌[          ]+┐ │
│[0-9\.+\-j ]+│ │
│[0-9\.+\-j ]+│ │
└[          ]+┘ │
│[          ]+  │
@[──────────]+──@
│[          ]+  │
    """.strip(),
        c.to_text_diagram(transpose=True).strip(),
    )


def test_two_qubit_diagram():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    c = qubitron.Circuit(
        qubitron.MatrixGate(qubitron.unitary(qubitron.CZ)).on(a, b),
        qubitron.MatrixGate(qubitron.unitary(qubitron.CZ)).on(c, a),
    )
    assert re.match(
        r"""
      ┌[          ]+┐
      │[0-9\.+\-j ]+│
a: ───│[0-9\.+\-j ]+│───#2─+
      │[0-9\.+\-j ]+│   │
      │[0-9\.+\-j ]+│   │
      └[          ]+┘   │
      │[          ]+    │
b: ───#2[─────────]+────┼──+
       [          ]+    │
       [          ]+    ┌[          ]+┐
       [          ]+    │[0-9\.+\-j ]+│
c: ────[──────────]+────│[0-9\.+\-j ]+│──+
       [          ]+    │[0-9\.+\-j ]+│
       [          ]+    │[0-9\.+\-j ]+│
       [          ]+    └[          ]+┘
    """.strip(),
        c.to_text_diagram().strip(),
    )

    assert re.match(
        r"""
a[          ]+  b  c
│[          ]+  │  │
┌[          ]+┐ │  │
│[0-9\.+\-j ]+│ │  │
│[0-9\.+\-j ]+│─#2 │
│[0-9\.+\-j ]+│ │  │
│[0-9\.+\-j ]+│ │  │
└[          ]+┘ │  │
│[          ]+  │  │
│[          ]+  │  ┌[          ]+┐
│[          ]+  │  │[0-9\.+\-j ]+│
#2[─────────]+──┼──│[0-9\.+\-j ]+│
│[          ]+  │  │[0-9\.+\-j ]+│
│[          ]+  │  │[0-9\.+\-j ]+│
│[          ]+  │  └[          ]+┘
│[          ]+  │  │
    """.strip(),
        c.to_text_diagram(transpose=True).strip(),
    )


def test_named_single_qubit_diagram():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    c = qubitron.Circuit(qubitron.MatrixGate(m, name='Foo').on(a), qubitron.CZ(a, b))

    expected_horizontal = """
a: ───Foo───@───
            │
b: ─────────@───
    """.strip()
    assert expected_horizontal == c.to_text_diagram().strip()

    expected_vertical = """
a   b
│   │
Foo │
│   │
@───@
│   │
    """.strip()
    assert expected_vertical == c.to_text_diagram(transpose=True).strip()


def test_named_two_qubit_diagram():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    c = qubitron.Circuit(
        qubitron.MatrixGate(qubitron.unitary(qubitron.CZ), name='Foo').on(a, b),
        qubitron.MatrixGate(qubitron.unitary(qubitron.CZ), name='Bar').on(c, a),
    )

    expected_horizontal = """
a: ───Foo[1]───Bar[2]───
      │        │
b: ───Foo[2]───┼────────
               │
c: ────────────Bar[1]───
    """.strip()
    assert expected_horizontal == c.to_text_diagram().strip()

    expected_vertical = """
a      b      c
│      │      │
Foo[1]─Foo[2] │
│      │      │
Bar[2]─┼──────Bar[1]
│      │      │
    """.strip()
    assert expected_vertical == c.to_text_diagram(transpose=True).strip()


def test_with_name():
    gate = qubitron.MatrixGate(qubitron.unitary(qubitron.Z**0.25))
    T = gate.with_name('T')
    S = (T**2).with_name('S')
    assert T._name == 'T'
    np.testing.assert_allclose(qubitron.unitary(T), qubitron.unitary(gate))
    assert S._name == 'S'
    np.testing.assert_allclose(qubitron.unitary(S), qubitron.unitary(T**2))


def test_str_executes():
    assert '1' in str(qubitron.MatrixGate(np.eye(2)))
    assert '0' in str(qubitron.MatrixGate(np.eye(4)))


@pytest.mark.parametrize('n', [1, 2, 3, 4, 5])
def test_implements_consistent_protocols(n):
    u = qubitron.testing.random_unitary(2**n)
    g1 = qubitron.MatrixGate(u)
    qubitron.testing.assert_implements_consistent_protocols(g1, ignoring_global_phase=True)
    qubitron.testing.assert_decompose_ends_at_default_gateset(g1)

    if n == 1:
        return

    g2 = qubitron.MatrixGate(u, qid_shape=(4,) + (2,) * (n - 2))
    qubitron.testing.assert_implements_consistent_protocols(g2, ignoring_global_phase=True)
    qubitron.testing.assert_decompose_ends_at_default_gateset(g2)


def test_repr():
    qubitron.testing.assert_equivalent_repr(qubitron.MatrixGate(qubitron.testing.random_unitary(2)))
    qubitron.testing.assert_equivalent_repr(qubitron.MatrixGate(qubitron.testing.random_unitary(4)))


def test_matrix_gate_init_validation():
    with pytest.raises(ValueError, match='square 2d numpy array'):
        _ = qubitron.MatrixGate(np.ones(shape=(1, 1, 1)))
    with pytest.raises(ValueError, match='square 2d numpy array'):
        _ = qubitron.MatrixGate(np.ones(shape=(2, 1)))
    with pytest.raises(ValueError, match='not a power of 2'):
        _ = qubitron.MatrixGate(np.ones(shape=(0, 0)))
    with pytest.raises(ValueError, match='not a power of 2'):
        _ = qubitron.MatrixGate(np.eye(3))
    with pytest.raises(ValueError, match='matrix shape for qid_shape'):
        _ = qubitron.MatrixGate(np.eye(3), qid_shape=(4,))


def test_matrix_gate_eq():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.MatrixGate(np.eye(1)))
    eq.add_equality_group(qubitron.MatrixGate(-np.eye(1)))
    eq.add_equality_group(qubitron.MatrixGate(np.diag([1, 1, 1, 1, 1, -1]), qid_shape=(2, 3)))
    eq.add_equality_group(qubitron.MatrixGate(np.diag([1, 1, 1, 1, 1, -1]), qid_shape=(3, 2)))


def test_matrix_gate_pow():
    t = sympy.Symbol('t')
    assert qubitron.pow(qubitron.MatrixGate(1j * np.eye(1)), t, default=None) is None
    assert qubitron.pow(qubitron.MatrixGate(1j * np.eye(1)), 2) == qubitron.MatrixGate(-np.eye(1))

    m = qubitron.MatrixGate(np.diag([1, 1j, -1]), qid_shape=(3,))
    assert m**3 == qubitron.MatrixGate(np.diag([1, -1j, -1]), qid_shape=(3,))


def test_phase_by():
    # Single qubit case.
    x = qubitron.MatrixGate(qubitron.unitary(qubitron.X))
    y = qubitron.phase_by(x, 0.25, 0)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(y), qubitron.unitary(qubitron.Y), atol=1e-8
    )

    # Two qubit case. Commutes with control.
    cx = qubitron.MatrixGate(qubitron.unitary(qubitron.X.controlled(1)))
    cx2 = qubitron.phase_by(cx, 0.25, 0)
    qubitron.testing.assert_allclose_up_to_global_phase(qubitron.unitary(cx2), qubitron.unitary(cx), atol=1e-8)

    # Two qubit case. Doesn't commute with target.
    cy = qubitron.phase_by(cx, 0.25, 1)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(cy), qubitron.unitary(qubitron.Y.controlled(1)), atol=1e-8
    )

    m = qubitron.MatrixGate(np.eye(3), qid_shape=[3])
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = qubitron.phase_by(m, 0.25, 0)


def test_protocols_and_repr():
    qubitron.testing.assert_implements_consistent_protocols(qubitron.MatrixGate(np.diag([1, 1j, 1, -1])))
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.MatrixGate(np.diag([1, 1j, -1]), qid_shape=(3,))
    )


def test_matrixgate_unitary_tolerance():
    ## non-unitary matrix
    with pytest.raises(ValueError):
        _ = qubitron.MatrixGate(np.array([[1, 0], [0, -0.6]]), unitary_check_atol=0.5)

    # very high atol -> check converges quickly
    _ = qubitron.MatrixGate(np.array([[1, 0], [0, 1]]), unitary_check_atol=1)

    # very high rtol -> check converges quickly
    _ = qubitron.MatrixGate(np.array([[1, 0], [0, -0.6]]), unitary_check_rtol=1)

    ## unitary matrix
    _ = qubitron.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_atol=0.5)

    # very low atol -> the check never converges
    with pytest.raises(ValueError):
        _ = qubitron.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_atol=1e-10)

    # very low atol -> the check never converges
    with pytest.raises(ValueError):
        _ = qubitron.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_rtol=1e-10)


def test_matrixgate_name_serialization():
    # https://github.com/amyssnippet/Qubitron/issues/5999

    # Test name serialization
    gate1 = qubitron.MatrixGate(np.eye(2), name='test_name')
    gate_after_serialization1 = qubitron.read_json(json_text=qubitron.to_json(gate1))
    assert gate1._name == 'test_name'
    assert gate_after_serialization1._name == 'test_name'

    # Test name backwards compatibility
    gate2 = qubitron.MatrixGate(np.eye(2))
    gate_after_serialization2 = qubitron.read_json(json_text=qubitron.to_json(gate2))
    assert gate2._name is None
    assert gate_after_serialization2._name is None

    # Test empty name
    gate3 = qubitron.MatrixGate(np.eye(2), name='')
    gate_after_serialization3 = qubitron.read_json(json_text=qubitron.to_json(gate3))
    assert gate3._name == ''
    assert gate_after_serialization3._name == ''
