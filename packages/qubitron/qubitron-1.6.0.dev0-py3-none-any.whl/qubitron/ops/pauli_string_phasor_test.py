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

dps_empty = qubitron.DensePauliString('')
dps_x = qubitron.DensePauliString('X')
dps_y = qubitron.DensePauliString('Y')
dps_xy = qubitron.DensePauliString('XY')
dps_yx = qubitron.DensePauliString('YX')
dps_xyz = qubitron.DensePauliString('XYZ')
dps_zyx = qubitron.DensePauliString('ZYX')


def _make_qubits(n):
    return [qubitron.NamedQubit(f'q{i}') for i in range(n)]


def test_init():
    a = qubitron.LineQubit(0)
    with pytest.raises(ValueError, match='eigenvalues'):
        _ = qubitron.PauliStringPhasor(1j * qubitron.X(a))
    v1 = qubitron.PauliStringPhasor(-qubitron.X(a), exponent_neg=0.25, exponent_pos=-0.5)
    assert v1.pauli_string == qubitron.X(a)
    assert v1.exponent_neg == -0.5
    assert v1.exponent_pos == 0.25

    v2 = qubitron.PauliStringPhasor(qubitron.X(a), exponent_neg=0.75, exponent_pos=-0.125)
    assert v2.pauli_string == qubitron.X(a)
    assert v2.exponent_neg == 0.75
    assert v2.exponent_pos == -0.125


def test_qubit_order_mismatch():
    q0, q1 = qubitron.LineQubit.range(2)
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = qubitron.PauliStringPhasor(1j * qubitron.X(q0), qubits=[q1])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = qubitron.PauliStringPhasor(1j * qubitron.X(q0) * qubitron.X(q1), qubits=[q1])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = qubitron.PauliStringPhasor(1j * qubitron.X(q0), qubits=[])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = qubitron.PauliStringPhasor(1j * qubitron.X(q0) * qubitron.X(q1), qubits=[q1, q0])


def test_eq_ne_hash():
    q0, q1, q2, q3 = _make_qubits(4)
    eq = qubitron.testing.EqualsTester()
    ps1 = qubitron.X(q0) * qubitron.Y(q1) * qubitron.Z(q2)
    ps2 = qubitron.X(q0) * qubitron.Y(q1) * qubitron.X(q2)
    eq.make_equality_group(
        lambda: qubitron.PauliStringPhasor(qubitron.PauliString(), exponent_neg=0.5),
        lambda: qubitron.PauliStringPhasor(qubitron.PauliString(), exponent_neg=-1.5),
        lambda: qubitron.PauliStringPhasor(qubitron.PauliString(), exponent_neg=2.5),
    )
    eq.make_equality_group(lambda: qubitron.PauliStringPhasor(-qubitron.PauliString(), exponent_neg=-0.5))
    eq.add_equality_group(qubitron.PauliStringPhasor(ps1), qubitron.PauliStringPhasor(ps1, exponent_neg=1))
    eq.add_equality_group(qubitron.PauliStringPhasor(-ps1, exponent_neg=1))
    eq.add_equality_group(qubitron.PauliStringPhasor(ps2), qubitron.PauliStringPhasor(ps2, exponent_neg=1))
    eq.add_equality_group(qubitron.PauliStringPhasor(-ps2, exponent_neg=1))
    eq.add_equality_group(qubitron.PauliStringPhasor(ps2, exponent_neg=0.5))
    eq.add_equality_group(qubitron.PauliStringPhasor(-ps2, exponent_neg=-0.5))
    eq.add_equality_group(qubitron.PauliStringPhasor(ps1, exponent_neg=sympy.Symbol('a')))
    eq.add_equality_group(qubitron.PauliStringPhasor(ps1, qubits=[q0, q1, q2, q3]))


def test_equal_up_to_global_phase():
    a, b, c = qubitron.LineQubit.range(3)
    groups = [
        [
            qubitron.PauliStringPhasor(qubitron.PauliString({a: qubitron.X}), exponent_neg=0.25),
            qubitron.PauliStringPhasor(
                qubitron.PauliString({a: qubitron.X}), exponent_neg=0, exponent_pos=-0.25
            ),
            qubitron.PauliStringPhasor(
                qubitron.PauliString({a: qubitron.X}), exponent_pos=-0.125, exponent_neg=0.125
            ),
        ],
        [qubitron.PauliStringPhasor(qubitron.PauliString({a: qubitron.X}))],
        [qubitron.PauliStringPhasor(qubitron.PauliString({a: qubitron.Y}), exponent_neg=0.25)],
        [qubitron.PauliStringPhasor(qubitron.PauliString({a: qubitron.X, b: qubitron.Y}), exponent_neg=0.25)],
        [
            qubitron.PauliStringPhasor(
                qubitron.PauliString({a: qubitron.X, b: qubitron.Y}), qubits=[a, b, c], exponent_neg=0.25
            )
        ],
    ]
    for g1 in groups:
        for e1 in g1:
            assert not e1.equal_up_to_global_phase("not even close")
            for g2 in groups:
                for e2 in g2:
                    assert e1.equal_up_to_global_phase(e2) == (g1 is g2)


def test_map_qubits():
    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    qubit_map = {q1: q2, q0: q3}
    before = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y}), exponent_neg=0.1)
    after = qubitron.PauliStringPhasor(qubitron.PauliString({q3: qubitron.Z, q2: qubitron.Y}), exponent_neg=0.1)
    assert before.map_qubits(qubit_map) == after

    qubit_map = {q1: q3, q0: q4, q2: q5}
    before = qubitron.PauliStringPhasor(
        qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y}), qubits=[q0, q1, q2], exponent_neg=0.1
    )
    after = qubitron.PauliStringPhasor(
        qubitron.PauliString({q4: qubitron.Z, q3: qubitron.Y}), qubits=[q4, q3, q5], exponent_neg=0.1
    )
    assert before.map_qubits(qubit_map) == after


def test_map_qubits_missing_qubits():
    q0, q1, q2 = _make_qubits(3)
    qubit_map = {q1: q2}
    before = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y}), exponent_neg=0.1)
    with pytest.raises(ValueError, match="have a key"):
        _ = before.map_qubits(qubit_map)


def test_pow():
    a = qubitron.LineQubit(0)
    s = qubitron.PauliString({a: qubitron.X})
    p = qubitron.PauliStringPhasor(s, exponent_neg=0.25, exponent_pos=0.5)
    assert p**0.5 == qubitron.PauliStringPhasor(s, exponent_neg=0.125, exponent_pos=0.25)
    with pytest.raises(TypeError, match='unsupported operand'):
        _ = p ** object()
    assert p**1 == p
    p = qubitron.PauliStringPhasor(s, qubits=[a], exponent_neg=0.25, exponent_pos=0.5)
    assert p**0.5 == qubitron.PauliStringPhasor(s, exponent_neg=0.125, exponent_pos=0.25)


def test_consistent():
    a, b = qubitron.LineQubit.range(2)
    op = np.exp(1j * np.pi / 2 * qubitron.X(a) * qubitron.X(b))
    qubitron.testing.assert_implements_consistent_protocols(op)
    p = qubitron.PauliStringPhasor(qubitron.X(a), qubits=[a], exponent_neg=0.25, exponent_pos=0.5)
    qubitron.testing.assert_implements_consistent_protocols(p)


def test_conjugated_by():
    q0, q1 = _make_qubits(2)
    op = qubitron.SingleQubitCliffordGate.from_double_map(
        {qubitron.Z: (qubitron.X, False), qubitron.X: (qubitron.Z, False)}
    )(q0)
    ps_before = qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y}, -1)
    ps_after = qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y}, -1)
    before = qubitron.PauliStringPhasor(ps_before, exponent_neg=0.1)
    after = qubitron.PauliStringPhasor(ps_after, exponent_neg=0.1)
    assert before.conjugated_by(op).pauli_string == after.pauli_string


def test_extrapolate_effect():
    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.5)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=1.5)
    op3 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.125)
    assert op1**3 == op2
    assert op1**0.25 == op3


def test_extrapolate_effect_with_symbol():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=sympy.Symbol('a')),
        qubitron.PauliStringPhasor(qubitron.PauliString({})) ** sympy.Symbol('a'),
    )
    eq.add_equality_group(qubitron.PauliStringPhasor(qubitron.PauliString({})) ** sympy.Symbol('b'))
    eq.add_equality_group(
        qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.5) ** sympy.Symbol('b')
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=sympy.Symbol('a')) ** 0.5
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=sympy.Symbol('a'))
        ** sympy.Symbol('b')
    )


def test_inverse():
    i = qubitron.PauliString({})
    op1 = qubitron.PauliStringPhasor(i, exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(i, exponent_neg=-0.25)
    op3 = qubitron.PauliStringPhasor(i, exponent_neg=sympy.Symbol('s'))
    op4 = qubitron.PauliStringPhasor(i, exponent_neg=-sympy.Symbol('s'))
    assert qubitron.inverse(op1) == op2
    assert qubitron.inverse(op3, None) == op4


def test_can_merge_with():
    q0, q1 = _make_qubits(2)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.75)
    assert op1.can_merge_with(op2)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.75)
    assert op1.can_merge_with(op2)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Y}, -1), exponent_neg=0.75)
    assert not op1.can_merge_with(op2)

    op1 = qubitron.PauliStringPhasor(
        qubitron.PauliString({q0: qubitron.X}, +1), qubits=[q0, q1], exponent_neg=0.25
    )
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.75)
    assert not op1.can_merge_with(op2)


def test_merge_with():
    (q0,) = _make_qubits(1)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.75)
    op12 = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.75)
    op12 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.75)
    op12 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=-0.5)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.75)
    op12 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=-0.5)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=0.75)
    op12 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, -1), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), exponent_neg=0.25)
    op2 = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Y}, -1), exponent_neg=0.75)
    with pytest.raises(ValueError):
        op1.merged_with(op2)


def test_is_parameterized():
    op = qubitron.PauliStringPhasor(qubitron.PauliString({}))
    assert not qubitron.is_parameterized(op)
    assert not qubitron.is_parameterized(op**0.1)
    assert qubitron.is_parameterized(op ** sympy.Symbol('a'))


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_with_parameters_resolved_by(resolve_fn):
    op = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=sympy.Symbol('a'))
    resolver = qubitron.ParamResolver({'a': 0.1})
    actual = resolve_fn(op, resolver)
    expected = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_neg=0.1)
    assert actual == expected

    with pytest.raises(ValueError, match='complex'):
        resolve_fn(op, qubitron.ParamResolver({'a': 0.1j}))
    op = qubitron.PauliStringPhasor(qubitron.PauliString({}), exponent_pos=sympy.Symbol('a'))
    with pytest.raises(ValueError, match='complex'):
        resolve_fn(op, qubitron.ParamResolver({'a': 0.1j}))


def test_drop_negligible():
    (q0,) = _make_qubits(1)
    sym = sympy.Symbol('a')
    circuit = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** 0.25,
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** 1e-10,
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** sym,
    )
    expected = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** 0.25,
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** sym,
    )
    circuit = qubitron.drop_negligible_operations(circuit)
    circuit = qubitron.drop_empty_moments(circuit)
    assert circuit == expected


def test_manual_default_decompose():
    q0, q1, q2 = _make_qubits(3)

    mat = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})) ** 0.25, qubitron.Z(q0) ** -0.25
    ).unitary()
    qubitron.testing.assert_allclose_up_to_global_phase(mat, np.eye(2), rtol=1e-7, atol=1e-7)

    mat = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Y})) ** 0.25, qubitron.Y(q0) ** -0.25
    ).unitary()
    qubitron.testing.assert_allclose_up_to_global_phase(mat, np.eye(2), rtol=1e-7, atol=1e-7)

    mat = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Z, q2: qubitron.Z}))
    ).unitary()
    qubitron.testing.assert_allclose_up_to_global_phase(
        mat, np.diag([1, -1, -1, 1, -1, 1, 1, -1]), rtol=1e-7, atol=1e-7
    )

    mat = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y, q2: qubitron.X})) ** 0.5
    ).unitary()
    qubitron.testing.assert_allclose_up_to_global_phase(
        mat,
        np.array(
            [
                [1, 0, 0, -1, 0, 0, 0, 0],
                [0, 1, -1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, -1, 1, 0],
                [0, 0, 0, 0, -1, 0, 0, 1],
            ]
        )
        / np.sqrt(2),
        rtol=1e-7,
        atol=1e-7,
    )


@pytest.mark.parametrize(
    'paulis,phase_exponent_negative,sign',
    itertools.product(
        itertools.product((qubitron.X, qubitron.Y, qubitron.Z, None), repeat=3),
        (0, 0.1, 0.5, 1, -0.25),
        (+1, -1),
    ),
)
def test_default_decompose(paulis, phase_exponent_negative: float, sign: int):
    paulis = [pauli for pauli in paulis if pauli is not None]
    qubits = _make_qubits(len(paulis))

    # Get matrix from decomposition
    pauli_string = qubitron.PauliString(
        qubit_pauli_map={q: p for q, p in zip(qubits, paulis)}, coefficient=sign
    )
    actual = qubitron.Circuit(
        qubitron.PauliStringPhasor(pauli_string, exponent_neg=phase_exponent_negative)
    ).unitary()

    # Calculate expected matrix
    to_z_mats = {
        qubitron.X: qubitron.unitary(qubitron.Y**-0.5),
        qubitron.Y: qubitron.unitary(qubitron.X**0.5),
        qubitron.Z: np.eye(2),
    }
    expected_convert = np.eye(1)
    for pauli in paulis:
        expected_convert = np.kron(expected_convert, to_z_mats[pauli])
    t = 1j ** (phase_exponent_negative * 2 * sign)
    expected_z = np.diag([1, t, t, 1, t, 1, 1, t][: 2 ** len(paulis)])
    expected = expected_convert.T.conj().dot(expected_z).dot(expected_convert)

    qubitron.testing.assert_allclose_up_to_global_phase(actual, expected, rtol=1e-7, atol=1e-7)


def test_decompose_with_symbol():
    (q0,) = _make_qubits(1)
    ps = qubitron.PauliString({q0: qubitron.Y})
    op = qubitron.PauliStringPhasor(ps, exponent_neg=sympy.Symbol('a'))
    circuit = qubitron.Circuit(op)
    circuit = qubitron.expand_composite(circuit)
    qubitron.testing.assert_has_diagram(circuit, "q0: ───X^0.5───Z^a───X^-0.5───")

    ps = qubitron.PauliString({q0: qubitron.Y}, -1)
    op = qubitron.PauliStringPhasor(ps, exponent_neg=sympy.Symbol('a'))
    circuit = qubitron.Circuit(op)
    circuit = qubitron.expand_composite(circuit)
    qubitron.testing.assert_has_diagram(circuit, "q0: ───X^0.5───X───Z^a───X───X^-0.5───")


def test_text_diagram():
    q0, q1, q2 = _make_qubits(3)
    circuit = qubitron.Circuit(
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z})),
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Y})) ** 0.25,
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Z, q2: qubitron.Z})),
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y, q2: qubitron.X}, -1)) ** 0.5,
        qubitron.PauliStringPhasor(
            qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y, q2: qubitron.X}), exponent_neg=sympy.Symbol('a')
        ),
        qubitron.PauliStringPhasor(
            qubitron.PauliString({q0: qubitron.Z, q1: qubitron.Y, q2: qubitron.X}, -1),
            exponent_neg=sympy.Symbol('b'),
        ),
        qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.Z}), qubits=[q0, q1], exponent_neg=0.5),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
q0: ───[Z]───[Y]^0.25───[Z]───[Z]────────[Z]─────[Z]────────[Z]───────
                        │     │          │       │          │
q1: ────────────────────[Z]───[Y]────────[Y]─────[Y]────────[I]^0.5───
                        │     │          │       │
q2: ────────────────────[Z]───[X]^-0.5───[X]^a───[X]^(-b)─────────────
""",
    )


def test_empty_phasor_diagram():
    q = qubitron.LineQubit(0)
    op = qubitron.PauliSumExponential(qubitron.I(q))
    circuit = qubitron.Circuit(op)
    qubitron.testing.assert_has_diagram(circuit, '    (I)**-0.6366197723675815')


def test_repr():
    q0, q1, q2 = _make_qubits(3)
    qubitron.testing.assert_equivalent_repr(
        qubitron.PauliStringPhasor(
            qubitron.PauliString({q2: qubitron.Z, q1: qubitron.Y, q0: qubitron.X}),
            exponent_neg=0.5,
            exponent_pos=0.25,
        )
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.PauliStringPhasor(
            -qubitron.PauliString({q1: qubitron.Y, q0: qubitron.X}), exponent_neg=-0.5, exponent_pos=0.25
        )
    )


def test_str():
    q0, q1, q2 = _make_qubits(3)
    ps = qubitron.PauliStringPhasor(qubitron.PauliString({q2: qubitron.Z, q1: qubitron.Y, q0: qubitron.X}, +1)) ** 0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**0.5'

    ps = qubitron.PauliStringPhasor(qubitron.PauliString({q2: qubitron.Z, q1: qubitron.Y, q0: qubitron.X}, +1)) ** -0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**-0.5'

    ps = qubitron.PauliStringPhasor(qubitron.PauliString({q2: qubitron.Z, q1: qubitron.Y, q0: qubitron.X}, -1)) ** -0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**0.5'

    assert str(np.exp(0.5j * np.pi * qubitron.X(q0) * qubitron.Y(q1))) == 'exp(iπ0.5*X(q0)*Y(q1))'
    assert str(np.exp(-0.25j * np.pi * qubitron.X(q0) * qubitron.Y(q1))) == 'exp(-iπ0.25*X(q0)*Y(q1))'
    assert str(np.exp(0.5j * np.pi * qubitron.PauliString())) == 'exp(iπ0.5*I)'

    ps = qubitron.PauliStringPhasor(qubitron.PauliString({q0: qubitron.X}, +1), qubits=[q0, q1]) ** 0.5
    assert str(ps) == '(X(q0))**0.5'


def test_old_json():
    """Older versions of PauliStringPhasor did not have a qubit field."""
    old_json = """
    {
      "qubitron_type": "PauliStringPhasor",
      "pauli_string": {
        "qubitron_type": "PauliString",
        "qubit_pauli_map": [
          [
            {
              "qubitron_type": "LineQubit",
              "x": 0
            },
            {
              "qubitron_type": "_PauliX",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ],
          [
            {
              "qubitron_type": "LineQubit",
              "x": 1
            },
            {
              "qubitron_type": "_PauliY",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ],
          [
            {
              "qubitron_type": "LineQubit",
              "x": 2
            },
            {
              "qubitron_type": "_PauliZ",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ]
        ],
        "coefficient": {
          "qubitron_type": "complex",
          "real": 1.0,
          "imag": 0.0
        }
      },
      "exponent_neg": 0.2,
      "exponent_pos": 0.1
    }
    """
    phasor = qubitron.read_json(json_text=old_json)
    assert phasor == qubitron.PauliStringPhasor(
        (
            (1 + 0j)
            * qubitron.X(qubitron.LineQubit(0))
            * qubitron.Y(qubitron.LineQubit(1))
            * qubitron.Z(qubitron.LineQubit(2))
        ),
        qubits=(qubitron.LineQubit(0), qubitron.LineQubit(1), qubitron.LineQubit(2)),
        exponent_neg=0.2,
        exponent_pos=0.1,
    )


def test_gate_init():
    a = qubitron.LineQubit(0)
    with pytest.raises(ValueError, match='eigenvalues'):
        _ = qubitron.PauliStringPhasorGate(1j * qubitron.X(a))

    v1 = qubitron.PauliStringPhasorGate(
        qubitron.DensePauliString('X', coefficient=-1), exponent_neg=0.25, exponent_pos=-0.5
    )
    assert v1.dense_pauli_string == dps_x
    assert v1.exponent_neg == -0.5
    assert v1.exponent_pos == 0.25

    v2 = qubitron.PauliStringPhasorGate(dps_x, exponent_neg=0.75, exponent_pos=-0.125)
    assert v2.dense_pauli_string == dps_x
    assert v2.exponent_neg == 0.75
    assert v2.exponent_pos == -0.125


def test_gate_on():
    q = qubitron.LineQubit(0)
    g1 = qubitron.PauliStringPhasorGate(
        qubitron.DensePauliString('X', coefficient=-1), exponent_neg=0.25, exponent_pos=-0.5
    )

    op1 = g1.on(q)
    assert isinstance(op1, qubitron.PauliStringPhasor)
    assert op1.qubits == (q,)
    assert op1.gate == g1
    assert op1.pauli_string == dps_x.on(q)
    assert op1.exponent_neg == -0.5
    assert op1.exponent_pos == 0.25

    g2 = qubitron.PauliStringPhasorGate(dps_x, exponent_neg=0.75, exponent_pos=-0.125)
    op2 = g2.on(q)
    assert isinstance(op2, qubitron.PauliStringPhasor)
    assert op2.qubits == (q,)
    assert op2.gate == g2
    assert op2.pauli_string == dps_x.on(q)
    assert op2.exponent_neg == 0.75
    assert op2.exponent_pos == -0.125


def test_gate_eq_ne_hash():
    eq = qubitron.testing.EqualsTester()
    dps_xyx = qubitron.DensePauliString('XYX')
    eq.make_equality_group(
        lambda: qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=0.5),
        lambda: qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=-1.5),
        lambda: qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=2.5),
    )
    eq.make_equality_group(lambda: qubitron.PauliStringPhasorGate(-dps_empty, exponent_neg=-0.5))
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_xyz), qubitron.PauliStringPhasorGate(dps_xyz, exponent_neg=1)
    )
    eq.add_equality_group(qubitron.PauliStringPhasorGate(-dps_xyz, exponent_neg=1))
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_xyx), qubitron.PauliStringPhasorGate(dps_xyx, exponent_neg=1)
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_xy), qubitron.PauliStringPhasorGate(dps_xy, exponent_neg=1)
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_yx), qubitron.PauliStringPhasorGate(dps_yx, exponent_neg=1)
    )
    eq.add_equality_group(qubitron.PauliStringPhasorGate(-dps_xyx, exponent_neg=1))
    eq.add_equality_group(qubitron.PauliStringPhasorGate(dps_xyx, exponent_neg=0.5))
    eq.add_equality_group(qubitron.PauliStringPhasorGate(-dps_xyx, exponent_neg=-0.5))
    eq.add_equality_group(qubitron.PauliStringPhasorGate(dps_xyz, exponent_neg=sympy.Symbol('a')))


def test_gate_equal_up_to_global_phase():
    groups = [
        [
            qubitron.PauliStringPhasorGate(dps_x, exponent_neg=0.25),
            qubitron.PauliStringPhasorGate(dps_x, exponent_neg=0, exponent_pos=-0.25),
            qubitron.PauliStringPhasorGate(dps_x, exponent_pos=-0.125, exponent_neg=0.125),
        ],
        [qubitron.PauliStringPhasorGate(dps_x)],
        [qubitron.PauliStringPhasorGate(dps_y, exponent_neg=0.25)],
        [qubitron.PauliStringPhasorGate(dps_xy, exponent_neg=0.25)],
    ]
    for g1 in groups:
        for e1 in g1:
            assert not e1.equal_up_to_global_phase("not even close")
            for g2 in groups:
                for e2 in g2:
                    assert e1.equal_up_to_global_phase(e2) == (g1 is g2)


def test_gate_pow():
    s = dps_x
    p = qubitron.PauliStringPhasorGate(s, exponent_neg=0.25, exponent_pos=0.5)
    assert p**0.5 == qubitron.PauliStringPhasorGate(s, exponent_neg=0.125, exponent_pos=0.25)
    with pytest.raises(TypeError, match='unsupported operand'):
        _ = p ** object()
    assert p**1 == p


def test_gate_extrapolate_effect():
    gate1 = qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=0.5)
    gate2 = qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=1.5)
    gate3 = qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=0.125)
    assert gate1**3 == gate2
    assert gate1**0.25 == gate3


def test_gate_extrapolate_effect_with_symbol():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')),
        qubitron.PauliStringPhasorGate(dps_empty) ** sympy.Symbol('a'),
    )
    eq.add_equality_group(qubitron.PauliStringPhasorGate(dps_empty) ** sympy.Symbol('b'))
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=0.5) ** sympy.Symbol('b')
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')) ** 0.5
    )
    eq.add_equality_group(
        qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')) ** sympy.Symbol('b')
    )


def test_gate_inverse():
    i = dps_empty
    gate1 = qubitron.PauliStringPhasorGate(i, exponent_neg=0.25)
    gate2 = qubitron.PauliStringPhasorGate(i, exponent_neg=-0.25)
    gate3 = qubitron.PauliStringPhasorGate(i, exponent_neg=sympy.Symbol('s'))
    gate4 = qubitron.PauliStringPhasorGate(i, exponent_neg=-sympy.Symbol('s'))
    assert qubitron.inverse(gate1) == gate2
    assert qubitron.inverse(gate3, None) == gate4


def test_gate_is_parameterized():
    gate = qubitron.PauliStringPhasorGate(dps_empty)
    assert not qubitron.is_parameterized(gate)
    assert not qubitron.is_parameterized(gate**0.1)
    assert qubitron.is_parameterized(gate ** sympy.Symbol('a'))


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_gate_with_parameters_resolved_by(resolve_fn):
    gate = qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a'))
    resolver = qubitron.ParamResolver({'a': 0.1})
    actual = resolve_fn(gate, resolver)
    expected = qubitron.PauliStringPhasorGate(dps_empty, exponent_neg=0.1)
    assert actual == expected


def test_gate_repr():
    qubitron.testing.assert_equivalent_repr(
        qubitron.PauliStringPhasorGate(dps_zyx, exponent_neg=0.5, exponent_pos=0.25)
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.PauliStringPhasorGate(-dps_yx, exponent_neg=-0.5, exponent_pos=0.25)
    )


def test_gate_str():
    gate = qubitron.PauliStringPhasorGate(qubitron.DensePauliString('ZYX', coefficient=+1)) ** 0.5
    assert str(gate) == '(+ZYX)**0.5'

    gate = qubitron.PauliStringPhasorGate(qubitron.DensePauliString('ZYX', coefficient=+1)) ** -0.5
    assert str(gate) == '(+ZYX)**-0.5'

    gate = qubitron.PauliStringPhasorGate(qubitron.DensePauliString('ZYX', coefficient=-1)) ** -0.5
    assert str(gate) == '(+ZYX)**0.5'

    gate = qubitron.PauliStringPhasorGate(
        qubitron.DensePauliString('ZYX'), exponent_pos=0.5, exponent_neg=-0.5
    )
    assert str(gate) == 'exp(iπ0.5*+ZYX)'

    gate = (
        qubitron.PauliStringPhasorGate(
            qubitron.DensePauliString('ZYX'), exponent_pos=0.5, exponent_neg=-0.5
        )
        ** -0.5
    )
    assert str(gate) == 'exp(-iπ0.25*+ZYX)'
