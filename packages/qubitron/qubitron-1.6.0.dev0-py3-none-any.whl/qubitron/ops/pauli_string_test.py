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
import math

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


def _make_qubits(n):
    return [qubitron.NamedQubit(f'q{i}') for i in range(n)]


def _sample_qubit_pauli_maps():
    """All combinations of having a Pauli or nothing on 3 qubits.
    Yields 64 qubit pauli maps
    """
    qubits = _make_qubits(3)
    paulis_or_none = (None, qubitron.X, qubitron.Y, qubitron.Z)
    for paulis in itertools.product(paulis_or_none, repeat=len(qubits)):
        yield {qubit: pauli for qubit, pauli in zip(qubits, paulis) if pauli is not None}


def _small_sample_qubit_pauli_maps():
    """A few representative samples of qubit maps.

    Only tests 10 combinations of Paulis to speed up testing.
    """
    qubits = _make_qubits(3)
    yield {}
    yield {qubits[0]: qubitron.X}
    yield {qubits[1]: qubitron.X}
    yield {qubits[2]: qubitron.X}
    yield {qubits[1]: qubitron.Z}

    yield {qubits[0]: qubitron.Y, qubits[1]: qubitron.Z}
    yield {qubits[1]: qubitron.Z, qubits[2]: qubitron.X}
    yield {qubits[0]: qubitron.X, qubits[1]: qubitron.X, qubits[2]: qubitron.X}
    yield {qubits[0]: qubitron.X, qubits[1]: qubitron.Y, qubits[2]: qubitron.Z}
    yield {qubits[0]: qubitron.Z, qubits[1]: qubitron.X, qubits[2]: qubitron.Y}


def assert_conjugation(
    input_ps: qubitron.PauliString,
    op: qubitron.Operation,
    expected: qubitron.PauliString | None = None,
    force_checking_unitary=True,
):
    """Verifies that conjugating `input_ps` by `op` results in `expected`.

    Also ensures that the unitary representation of the Pauli string is
    preserved under the conjugation.
    """

    def _ps_on_qubits(ps: qubitron.PauliString, qubits: tuple[qubitron.Qid, ...]):
        """Extracts a sub-PauliString from a given PauliString, restricted to
        a specified subset of qubits.
        """
        pauli_map = {}
        for q, pauli in ps.items():
            if q in qubits:
                pauli_map[q] = pauli
        return qubitron.PauliString(qubit_pauli_map=pauli_map, coefficient=ps.coefficient)

    conjugation = input_ps.conjugated_by(op)
    if expected is None or force_checking_unitary:
        # Compares the unitary of the conjugation result and the expected unitary.
        clifford = qubitron.CliffordGate.from_op_list([op], op.qubits)
        actual_unitary = qubitron.unitary(_ps_on_qubits(conjugation, op.qubits).dense(op.qubits))
        c = qubitron.unitary(clifford)
        expected_unitary = (
            np.conj(c.T) @ qubitron.unitary(_ps_on_qubits(input_ps, op.qubits).dense(op.qubits)) @ c
        )
        assert np.allclose(actual_unitary, expected_unitary, atol=1e-8)
    if expected is not None:
        assert conjugation == expected


def assert_conjugation_multi_ops(
    input_ps: qubitron.PauliString, ops: list[qubitron.Operation], expected: qubitron.PauliString | None = None
):
    conjugation = input_ps.conjugated_by(ops)
    if expected is not None:
        assert conjugation == expected
    # conj_by(op_{n-1}).conj_by(op_{n-1}).....conj_by(op_0)
    conj_in_order = input_ps
    for op in ops[::-1]:
        assert_conjugation(conj_in_order, op)
        conj_in_order = conj_in_order.conjugated_by(op)
    assert conjugation == conj_in_order


def test_eq_ne_hash():
    q0, q1, q2 = _make_qubits(3)
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(
        lambda: qubitron.PauliString(),
        lambda: qubitron.PauliString(qubit_pauli_map={}),
        lambda: qubitron.PauliString(qubit_pauli_map={}, coefficient=+1),
    )
    eq.add_equality_group(qubitron.PauliString(qubit_pauli_map={}, coefficient=-1))
    for q, pauli in itertools.product((q0, q1), (qubitron.X, qubitron.Y, qubitron.Z)):
        eq.add_equality_group(qubitron.PauliString(qubit_pauli_map={q: pauli}, coefficient=+1))
        eq.add_equality_group(qubitron.PauliString(qubit_pauli_map={q: pauli}, coefficient=-1))
    for q, p0, p1 in itertools.product(
        (q0, q1), (qubitron.X, qubitron.Y, qubitron.Z), (qubitron.X, qubitron.Y, qubitron.Z)
    ):
        eq.add_equality_group(qubitron.PauliString(qubit_pauli_map={q: p0, q2: p1}, coefficient=+1))


def test_equal_up_to_coefficient():
    (q0,) = _make_qubits(1)
    assert qubitron.PauliString({}, +1).equal_up_to_coefficient(qubitron.PauliString({}, +1))
    assert qubitron.PauliString({}, -1).equal_up_to_coefficient(qubitron.PauliString({}, -1))
    assert qubitron.PauliString({}, +1).equal_up_to_coefficient(qubitron.PauliString({}, -1))
    assert qubitron.PauliString({}, +1).equal_up_to_coefficient(qubitron.PauliString({}, 2j))

    assert qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.X}, +1)
    )
    assert qubitron.PauliString({q0: qubitron.X}, -1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.X}, -1)
    )
    assert qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.X}, -1)
    )

    assert not qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.Y}, +1)
    )
    assert not qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.Y}, 1j)
    )
    assert not qubitron.PauliString({q0: qubitron.X}, -1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.Y}, -1)
    )
    assert not qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(
        qubitron.PauliString({q0: qubitron.Y}, -1)
    )

    assert not qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(qubitron.PauliString({}, +1))
    assert not qubitron.PauliString({q0: qubitron.X}, -1).equal_up_to_coefficient(qubitron.PauliString({}, -1))
    assert not qubitron.PauliString({q0: qubitron.X}, +1).equal_up_to_coefficient(qubitron.PauliString({}, -1))


def test_exponentiation_as_exponent():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliString({a: qubitron.X, b: qubitron.Y})

    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        _ = math.e ** (math.pi * p)

    with pytest.raises(TypeError, match='unsupported'):
        _ = 'test' ** p

    assert qubitron.approx_eq(
        math.e ** (-0.5j * math.pi * p),
        qubitron.PauliStringPhasor(p, exponent_neg=0.5, exponent_pos=-0.5),
    )

    assert qubitron.approx_eq(
        math.e ** (0.25j * math.pi * p),
        qubitron.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    assert qubitron.approx_eq(
        2 ** (0.25j * math.pi * p),
        qubitron.PauliStringPhasor(
            p, exponent_neg=-0.25 * math.log(2), exponent_pos=0.25 * math.log(2)
        ),
    )

    assert qubitron.approx_eq(
        np.exp(0.25j * math.pi * p),
        qubitron.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )


def test_exponentiate_single_value_as_exponent():
    q = qubitron.LineQubit(0)

    assert qubitron.approx_eq(math.e ** (-0.125j * math.pi * qubitron.X(q)), qubitron.rx(0.25 * math.pi).on(q))

    assert qubitron.approx_eq(math.e ** (-0.125j * math.pi * qubitron.Y(q)), qubitron.ry(0.25 * math.pi).on(q))

    assert qubitron.approx_eq(math.e ** (-0.125j * math.pi * qubitron.Z(q)), qubitron.rz(0.25 * math.pi).on(q))

    assert qubitron.approx_eq(np.exp(-0.15j * math.pi * qubitron.X(q)), qubitron.rx(0.3 * math.pi).on(q))

    assert qubitron.approx_eq(qubitron.X(q) ** 0.5, qubitron.XPowGate(exponent=0.5).on(q))

    assert qubitron.approx_eq(qubitron.Y(q) ** 0.5, qubitron.YPowGate(exponent=0.5).on(q))

    assert qubitron.approx_eq(qubitron.Z(q) ** 0.5, qubitron.ZPowGate(exponent=0.5).on(q))


def test_exponentiation_as_base():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliString({a: qubitron.X, b: qubitron.Y})

    with pytest.raises(TypeError, match='unsupported'):
        _ = (2 * p) ** 5

    with pytest.raises(TypeError, match='unsupported'):
        _ = p ** 'test'

    with pytest.raises(TypeError, match='unsupported'):
        _ = p**1j

    assert p**-1 == p

    assert qubitron.approx_eq(p**0.5, qubitron.PauliStringPhasor(p, exponent_neg=0.5, exponent_pos=0))

    assert qubitron.approx_eq(p**-0.5, qubitron.PauliStringPhasor(p, exponent_neg=-0.5, exponent_pos=0))

    assert qubitron.approx_eq(
        math.e ** (0.25j * math.pi * p),
        qubitron.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    assert qubitron.approx_eq(
        2 ** (0.25j * math.pi * p),
        qubitron.PauliStringPhasor(
            p, exponent_neg=-0.25 * math.log(2), exponent_pos=0.25 * math.log(2)
        ),
    )

    assert qubitron.approx_eq(
        np.exp(0.25j * math.pi * p),
        qubitron.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    np.testing.assert_allclose(
        qubitron.unitary(np.exp(0.5j * math.pi * qubitron.Z(a))),
        np.diag([np.exp(0.5j * math.pi), np.exp(-0.5j * math.pi)]),
        atol=1e-8,
    )


@pytest.mark.parametrize('pauli', (qubitron.X, qubitron.Y, qubitron.Z))
def test_list_op_constructor_matches_mapping(pauli):
    (q0,) = _make_qubits(1)
    op = pauli.on(q0)
    assert qubitron.PauliString([op]) == qubitron.PauliString({q0: pauli})


@pytest.mark.parametrize('pauli1', (qubitron.X, qubitron.Y, qubitron.Z))
@pytest.mark.parametrize('pauli2', (qubitron.X, qubitron.Y, qubitron.Z))
def test_exponent_mul_consistency(pauli1, pauli2):
    a, b = qubitron.LineQubit.range(2)
    op_a, op_b = pauli1(a), pauli2(b)

    assert op_a * op_a * op_a == op_a
    assert op_a * op_a**2 == op_a
    assert op_a**2 * op_a == op_a
    assert op_b * op_a * op_a == op_b
    assert op_b * op_a**2 == op_b
    assert op_a**2 * op_b == op_b
    assert op_a * op_a * op_a * op_a == qubitron.PauliString()
    assert op_a * op_a**3 == qubitron.PauliString()
    assert op_b * op_a * op_a * op_a == op_b * op_a
    assert op_b * op_a**3 == op_b * op_a

    op_a, op_b = pauli1(a), pauli2(a)

    assert op_a * op_b**3 == op_a * op_b * op_b * op_b
    assert op_b**3 * op_a == op_b * op_b * op_b * op_a


def test_constructor_flexibility():
    a, b = qubitron.LineQubit.range(2)
    with pytest.raises(TypeError, match='qubitron.PAULI_STRING_LIKE'):
        _ = qubitron.PauliString(qubitron.CZ(a, b))
    with pytest.raises(TypeError, match='qubitron.PAULI_STRING_LIKE'):
        _ = qubitron.PauliString('test')
    with pytest.raises(TypeError, match='S is not a Pauli'):
        _ = qubitron.PauliString(qubit_pauli_map={a: qubitron.S})
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        _ = qubitron.PauliString(qubitron.Z(a) + qubitron.Z(b))

    assert qubitron.PauliString(qubitron.X(a)) == qubitron.PauliString(qubit_pauli_map={a: qubitron.X})
    assert qubitron.PauliString([qubitron.X(a)]) == qubitron.PauliString(qubit_pauli_map={a: qubitron.X})
    assert qubitron.PauliString([[[qubitron.X(a)]]]) == qubitron.PauliString(qubit_pauli_map={a: qubitron.X})
    assert qubitron.PauliString([[[qubitron.I(a)]]]) == qubitron.PauliString()

    assert qubitron.PauliString(1, 2, 3, qubitron.X(a), qubitron.Y(a)) == qubitron.PauliString(
        qubit_pauli_map={a: qubitron.Z}, coefficient=6j
    )

    assert qubitron.PauliString(qubitron.X(a), qubitron.X(a)) == qubitron.PauliString()
    assert qubitron.PauliString(qubitron.X(a), qubitron.X(b)) == qubitron.PauliString(
        qubit_pauli_map={a: qubitron.X, b: qubitron.X}
    )

    assert qubitron.PauliString(0) == qubitron.PauliString(coefficient=0)

    assert qubitron.PauliString(1, 2, 3, {a: qubitron.X}, qubitron.Y(a)) == qubitron.PauliString(
        qubit_pauli_map={a: qubitron.Z}, coefficient=6j
    )


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_getitem(qubit_pauli_map):
    other = qubitron.NamedQubit('other')
    pauli_string = qubitron.PauliString(qubit_pauli_map=qubit_pauli_map)
    for key in qubit_pauli_map:
        assert qubit_pauli_map[key] == pauli_string[key]
    with pytest.raises(KeyError):
        _ = qubit_pauli_map[other]
    with pytest.raises(KeyError):
        _ = pauli_string[other]


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_get(qubit_pauli_map):
    other = qubitron.NamedQubit('other')
    pauli_string = qubitron.PauliString(qubit_pauli_map)
    for key in qubit_pauli_map:
        assert qubit_pauli_map.get(key) == pauli_string.get(key)
    assert qubit_pauli_map.get(other) is None
    assert pauli_string.get(other) is None
    # pylint: disable=too-many-function-args
    assert qubit_pauli_map.get(other, 5) == pauli_string.get(other, 5) == 5
    # pylint: enable=too-many-function-args


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_contains(qubit_pauli_map):
    other = qubitron.NamedQubit('other')
    pauli_string = qubitron.PauliString(qubit_pauli_map)
    for key in qubit_pauli_map:
        assert key in pauli_string
    assert other not in pauli_string


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_basic_functionality(qubit_pauli_map):
    pauli_string = qubitron.PauliString(qubit_pauli_map)
    # Test items
    assert len(qubit_pauli_map.items()) == len(pauli_string.items())
    assert set(qubit_pauli_map.items()) == set(pauli_string.items())

    # Test values
    assert len(qubit_pauli_map.values()) == len(pauli_string.values())
    assert set(qubit_pauli_map.values()) == set(pauli_string.values())

    # Test length
    assert len(qubit_pauli_map) == len(pauli_string)

    # Test keys
    assert len(qubit_pauli_map.keys()) == len(pauli_string.keys()) == len(pauli_string.qubits)
    assert set(qubit_pauli_map.keys()) == set(pauli_string.keys()) == set(pauli_string.qubits)

    # Test iteration
    assert len(tuple(qubit_pauli_map)) == len(tuple(pauli_string))
    assert set(tuple(qubit_pauli_map)) == set(tuple(pauli_string))


def test_repr():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = qubitron.PauliString({q2: qubitron.X, q1: qubitron.Y, q0: qubitron.Z})
    qubitron.testing.assert_equivalent_repr(pauli_string)
    qubitron.testing.assert_equivalent_repr(-pauli_string)
    qubitron.testing.assert_equivalent_repr(1j * pauli_string)
    qubitron.testing.assert_equivalent_repr(2 * pauli_string)
    qubitron.testing.assert_equivalent_repr(qubitron.PauliString())


def test_repr_preserves_qubit_order():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = qubitron.PauliString({q2: qubitron.X, q1: qubitron.Y, q0: qubitron.Z})
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits

    pauli_string = qubitron.PauliString(qubitron.X(q2), qubitron.Y(q1), qubitron.Z(q0))
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits

    pauli_string = qubitron.PauliString(qubitron.Z(q0), qubitron.Y(q1), qubitron.X(q2))
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits


def test_repr_coefficient_of_one():
    pauli_string = qubitron.Z(qubitron.LineQubit(0)) * 1
    assert type(pauli_string) == type(eval(repr(pauli_string)))
    qubitron.testing.assert_equivalent_repr(pauli_string)


def test_str():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = qubitron.PauliString({q2: qubitron.X, q1: qubitron.Y, q0: qubitron.Z})
    assert str(qubitron.PauliString({})) == 'I'
    assert str(-qubitron.PauliString({})) == '-I'
    assert str(pauli_string) == 'Z(q0)*Y(q1)*X(q2)'
    assert str(-pauli_string) == '-Z(q0)*Y(q1)*X(q2)'
    assert str(1j * pauli_string) == '1j*Z(q0)*Y(q1)*X(q2)'
    assert str(pauli_string * -1j) == '-1j*Z(q0)*Y(q1)*X(q2)'


@pytest.mark.parametrize(
    'map1,map2,out',
    (
        lambda q0, q1, q2: (
            ({}, {}, {}),
            ({q0: qubitron.X}, {q0: qubitron.Y}, {q0: (qubitron.X, qubitron.Y)}),
            ({q0: qubitron.X}, {q1: qubitron.X}, {}),
            ({q0: qubitron.Y, q1: qubitron.Z}, {q1: qubitron.Y, q2: qubitron.X}, {q1: (qubitron.Z, qubitron.Y)}),
            ({q0: qubitron.X, q1: qubitron.Y, q2: qubitron.Z}, {}, {}),
            (
                {q0: qubitron.X, q1: qubitron.Y, q2: qubitron.Z},
                {q0: qubitron.Y, q1: qubitron.Z},
                {q0: (qubitron.X, qubitron.Y), q1: (qubitron.Y, qubitron.Z)},
            ),
        )
    )(*_make_qubits(3)),
)
def test_zip_items(map1, map2, out):
    ps1 = qubitron.PauliString(map1)
    ps2 = qubitron.PauliString(map2)
    out_actual = tuple(ps1.zip_items(ps2))
    assert len(out_actual) == len(out)
    assert dict(out_actual) == out


@pytest.mark.parametrize(
    'map1,map2,out',
    (
        lambda q0, q1, q2: (
            ({}, {}, ()),
            ({q0: qubitron.X}, {q0: qubitron.Y}, ((qubitron.X, qubitron.Y),)),
            ({q0: qubitron.X}, {q1: qubitron.X}, ()),
            ({q0: qubitron.Y, q1: qubitron.Z}, {q1: qubitron.Y, q2: qubitron.X}, ((qubitron.Z, qubitron.Y),)),
            ({q0: qubitron.X, q1: qubitron.Y, q2: qubitron.Z}, {}, ()),
            (
                {q0: qubitron.X, q1: qubitron.Y, q2: qubitron.Z},
                {q0: qubitron.Y, q1: qubitron.Z},
                # Order not necessary
                ((qubitron.X, qubitron.Y), (qubitron.Y, qubitron.Z)),
            ),
        )
    )(*_make_qubits(3)),
)
def test_zip_paulis(map1, map2, out):
    ps1 = qubitron.PauliString(map1)
    ps2 = qubitron.PauliString(map2)
    out_actual = tuple(ps1.zip_paulis(ps2))
    assert len(out_actual) == len(out)
    if len(out) <= 1:
        assert out_actual == out
    assert set(out_actual) == set(out)  # Ignore output order


def test_commutes():
    qubits = _make_qubits(3)

    ps1 = qubitron.PauliString([qubitron.X(qubits[0])])
    with pytest.raises(TypeError):
        qubitron.commutes(ps1, 'X')
    assert qubitron.commutes(ps1, 'X', default='default') == 'default'
    for A, commutes in [(qubitron.X, True), (qubitron.Y, False)]:
        assert qubitron.commutes(ps1, qubitron.PauliString([A(qubits[0])])) == commutes
        assert qubitron.commutes(ps1, qubitron.PauliString([A(qubits[1])]))

    ps1 = qubitron.PauliString(dict(zip(qubits, (qubitron.X, qubitron.Y))))

    for paulis, commutes in {
        (qubitron.X, qubitron.Y): True,
        (qubitron.X, qubitron.Z): False,
        (qubitron.Y, qubitron.X): True,
        (qubitron.Y, qubitron.Z): True,
        (qubitron.X, qubitron.Y, qubitron.Z): True,
        (qubitron.X, qubitron.Z, qubitron.Z): False,
        (qubitron.Y, qubitron.X, qubitron.Z): True,
        (qubitron.Y, qubitron.Z, qubitron.X): True,
    }.items():
        ps2 = qubitron.PauliString(dict(zip(qubits, paulis)))
        assert qubitron.commutes(ps1, ps2) == commutes

    for paulis, commutes in {
        (qubitron.Y, qubitron.X): True,
        (qubitron.Z, qubitron.X): False,
        (qubitron.X, qubitron.Y): False,
        (qubitron.Z, qubitron.Y): False,
    }.items():
        ps2 = qubitron.PauliString(dict(zip(qubits[1:], paulis)))
        assert qubitron.commutes(ps1, ps2) == commutes


def test_negate():
    q0, q1 = _make_qubits(2)
    qubit_pauli_map = {q0: qubitron.X, q1: qubitron.Y}
    ps1 = qubitron.PauliString(qubit_pauli_map)
    ps2 = qubitron.PauliString(qubit_pauli_map, -1)
    assert -ps1 == ps2
    assert ps1 == -ps2
    neg_ps1 = -ps1
    assert -neg_ps1 == ps1

    m = ps1.mutable_copy()
    assert -m == -1 * m
    assert -m is not m
    assert isinstance(-m, qubitron.MutablePauliString)


def test_mul_scalar():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliString({a: qubitron.X, b: qubitron.Y})
    assert -p == -1 * p == -1.0 * p == p * -1 == p * complex(-1)
    assert -p != 1j * p
    assert +p == 1 * p

    assert p * qubitron.I(a) == p
    assert qubitron.I(a) * p == p

    with pytest.raises(TypeError, match="sequence by non-int of type 'PauliString'"):
        _ = p * 'test'
    with pytest.raises(TypeError, match="sequence by non-int of type 'PauliString'"):
        _ = 'test' * p


def test_div_scalar():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliString({a: qubitron.X, b: qubitron.Y})
    assert -p == p / -1 == p / -1.0 == p / (-1 + 0j)
    assert -p != p / 1j
    assert +p == p / 1
    assert p * 2 == p / 0.5
    with pytest.raises(TypeError):
        _ = p / 'test'
    with pytest.raises(TypeError):
        # noinspection PyUnresolvedReferences
        _ = 'test' / p


def test_mul_strings():
    a, b, c, d = qubitron.LineQubit.range(4)
    p1 = qubitron.PauliString({a: qubitron.X, b: qubitron.Y, c: qubitron.Z})
    p2 = qubitron.PauliString({b: qubitron.X, c: qubitron.Y, d: qubitron.Z})
    assert p1 * p2 == -qubitron.PauliString({a: qubitron.X, b: qubitron.Z, c: qubitron.X, d: qubitron.Z})

    assert qubitron.X(a) * qubitron.PauliString({a: qubitron.X}) == qubitron.PauliString()
    assert qubitron.PauliString({a: qubitron.X}) * qubitron.X(a) == qubitron.PauliString()
    assert qubitron.X(a) * qubitron.X(a) == qubitron.PauliString()
    assert -qubitron.X(a) * -qubitron.X(a) == qubitron.PauliString()

    with pytest.raises(TypeError, match='unsupported'):
        _ = qubitron.X(a) * object()
    with pytest.raises(TypeError, match='unsupported'):
        # noinspection PyUnresolvedReferences
        _ = object() * qubitron.X(a)
    assert -qubitron.X(a) == -qubitron.PauliString({a: qubitron.X})


def test_op_equivalence():
    a, b = qubitron.LineQubit.range(2)
    various_x = [
        qubitron.X(a),
        qubitron.PauliString({a: qubitron.X}),
        qubitron.PauliString([qubitron.X.on(a)]),
        qubitron.SingleQubitPauliStringGateOperation(qubitron.X, a),
        qubitron.GateOperation(qubitron.X, [a]),
    ]

    for x in various_x:
        qubitron.testing.assert_equivalent_repr(x)

    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(*various_x)
    eq.add_equality_group(qubitron.Y(a), qubitron.PauliString({a: qubitron.Y}))
    eq.add_equality_group(-qubitron.PauliString({a: qubitron.X}))
    eq.add_equality_group(qubitron.Z(a), qubitron.PauliString({a: qubitron.Z}))
    eq.add_equality_group(qubitron.Z(b), qubitron.PauliString({b: qubitron.Z}))


def test_op_product():
    a, b = qubitron.LineQubit.range(2)

    assert qubitron.X(a) * qubitron.X(b) == qubitron.PauliString({a: qubitron.X, b: qubitron.X})
    assert qubitron.X(a) * qubitron.Y(b) == qubitron.PauliString({a: qubitron.X, b: qubitron.Y})
    assert qubitron.Z(a) * qubitron.Y(b) == qubitron.PauliString({a: qubitron.Z, b: qubitron.Y})

    assert qubitron.X(a) * qubitron.X(a) == qubitron.PauliString()
    assert qubitron.X(a) * qubitron.Y(a) == 1j * qubitron.PauliString({a: qubitron.Z})
    assert qubitron.Y(a) * qubitron.Z(b) * qubitron.X(a) == -1j * qubitron.PauliString({a: qubitron.Z, b: qubitron.Z})


def test_pos():
    q0, q1 = _make_qubits(2)
    qubit_pauli_map = {q0: qubitron.X, q1: qubitron.Y}
    ps1 = qubitron.PauliString(qubit_pauli_map)
    assert ps1 == +ps1

    m = ps1.mutable_copy()
    assert +m == m
    assert +m is not m
    assert isinstance(+m, qubitron.MutablePauliString)


def test_pow():
    a, b = qubitron.LineQubit.range(2)

    assert qubitron.PauliString({a: qubitron.X}) ** 0.25 == qubitron.X(a) ** 0.25
    assert qubitron.PauliString({a: qubitron.Y}) ** 0.25 == qubitron.Y(a) ** 0.25
    assert qubitron.PauliString({a: qubitron.Z}) ** 0.25 == qubitron.Z(a) ** 0.25

    p = qubitron.PauliString({a: qubitron.X, b: qubitron.Y})
    assert p**1 == p
    assert p**-1 == p
    assert (-p) ** 1 == -p
    assert (-p) ** -1 == -p
    assert (1j * p) ** 1 == 1j * p
    assert (1j * p) ** -1 == -1j * p


def test_rpow():
    a, b = qubitron.LineQubit.range(2)

    u = qubitron.unitary(np.exp(1j * np.pi / 2 * qubitron.Z(a) * qubitron.Z(b)))
    np.testing.assert_allclose(u, np.diag([1j, -1j, -1j, 1j]), atol=1e-8)

    u = qubitron.unitary(np.exp(-1j * np.pi / 4 * qubitron.Z(a) * qubitron.Z(b)))
    qubitron.testing.assert_allclose_up_to_global_phase(u, np.diag([1, 1j, 1j, 1]), atol=1e-8)

    u = qubitron.unitary(np.e ** (1j * np.pi * qubitron.Z(a) * qubitron.Z(b)))
    np.testing.assert_allclose(u, np.diag([-1, -1, -1, -1]), atol=1e-8)


def test_numpy_ufunc():
    with pytest.raises(TypeError, match="returned NotImplemented"):
        _ = np.sin(qubitron.PauliString())
    with pytest.raises(NotImplementedError, match="non-Hermitian"):
        _ = np.exp(qubitron.PauliString())
    x = np.exp(1j * np.pi * qubitron.PauliString())
    assert x is not None
    x = np.int64(2) * qubitron.PauliString()
    assert x == 2 * qubitron.PauliString()


def test_map_qubits():
    a, b = (qubitron.NamedQubit(name) for name in 'ab')
    q0, q1 = _make_qubits(2)
    qubit_pauli_map1 = {a: qubitron.X, b: qubitron.Y}
    qubit_pauli_map2 = {q0: qubitron.X, q1: qubitron.Y}
    qubit_map = {a: q0, b: q1}
    ps1 = qubitron.PauliString(qubit_pauli_map1)
    ps2 = qubitron.PauliString(qubit_pauli_map2)
    assert ps1.map_qubits(qubit_map) == ps2


def test_map_qubits_raises():
    q = qubitron.LineQubit.range(3)
    pauli_string = qubitron.X(q[0]) * qubitron.Y(q[1]) * qubitron.Z(q[2])
    with pytest.raises(ValueError, match='must have a key for every qubit'):
        pauli_string.map_qubits({q[0]: q[1]})


def test_to_z_basis_ops():
    x0 = np.array([1, 1]) / np.sqrt(2)
    x1 = np.array([1, -1]) / np.sqrt(2)
    y0 = np.array([1, 1j]) / np.sqrt(2)
    y1 = np.array([1, -1j]) / np.sqrt(2)
    z0 = np.array([1, 0])
    z1 = np.array([0, 1])

    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    pauli_string = qubitron.PauliString(
        {q0: qubitron.X, q1: qubitron.X, q2: qubitron.Y, q3: qubitron.Y, q4: qubitron.Z, q5: qubitron.Z}
    )
    circuit = qubitron.Circuit(pauli_string.to_z_basis_ops())

    initial_state = qubitron.kron(x0, x1, y0, y1, z0, z1, shape_len=1)
    z_basis_state = circuit.final_state_vector(
        initial_state=initial_state, ignore_terminal_measurements=False, dtype=np.complex64
    )

    expected_state = np.zeros(2**6)
    expected_state[0b010101] = 1

    qubitron.testing.assert_allclose_up_to_global_phase(
        z_basis_state, expected_state, rtol=1e-7, atol=1e-7
    )


def test_to_z_basis_ops_product_state():
    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    pauli_string = qubitron.PauliString(
        {q0: qubitron.X, q1: qubitron.X, q2: qubitron.Y, q3: qubitron.Y, q4: qubitron.Z, q5: qubitron.Z}
    )
    circuit = qubitron.Circuit(pauli_string.to_z_basis_ops())

    initial_state = (
        qubitron.KET_PLUS(q0)
        * qubitron.KET_MINUS(q1)
        * qubitron.KET_IMAG(q2)
        * qubitron.KET_MINUS_IMAG(q3)
        * qubitron.KET_ZERO(q4)
        * qubitron.KET_ONE(q5)
    )
    z_basis_state = circuit.final_state_vector(
        initial_state=initial_state, ignore_terminal_measurements=False, dtype=np.complex64
    )

    expected_state = np.zeros(2**6)
    expected_state[0b010101] = 1

    qubitron.testing.assert_allclose_up_to_global_phase(
        z_basis_state, expected_state, rtol=1e-7, atol=1e-7
    )


def test_with_qubits():
    old_qubits = qubitron.LineQubit.range(9)
    new_qubits = qubitron.LineQubit.range(9, 18)
    qubit_pauli_map = {q: qubitron.Pauli.by_index(q.x) for q in old_qubits}
    pauli_string = qubitron.PauliString(qubit_pauli_map, -1)
    new_pauli_string = pauli_string.with_qubits(*new_qubits)

    assert new_pauli_string.qubits == tuple(new_qubits)
    for q in new_qubits:
        assert new_pauli_string[q] == qubitron.Pauli.by_index(q.x)
    assert new_pauli_string.coefficient == -1


def test_with_qubits_raises():
    q = qubitron.LineQubit.range(3)
    pauli_string = qubitron.X(q[0]) * qubitron.Y(q[1]) * qubitron.Z(q[2])
    with pytest.raises(ValueError, match='does not match'):
        pauli_string.with_qubits(q[:2])


def test_with_coefficient():
    qubits = qubitron.LineQubit.range(4)
    qubit_pauli_map = {q: qubitron.Pauli.by_index(q.x) for q in qubits}
    pauli_string = qubitron.PauliString(qubit_pauli_map, 1.23)
    ps2 = pauli_string.with_coefficient(1.0)
    assert ps2.coefficient == 1.0
    assert ps2.equal_up_to_coefficient(pauli_string)
    assert pauli_string != ps2
    assert pauli_string.coefficient == 1.23


@pytest.mark.parametrize('qubit_pauli_map', _small_sample_qubit_pauli_maps())
def test_consistency(qubit_pauli_map):
    pauli_string = qubitron.PauliString(qubit_pauli_map)
    qubitron.testing.assert_implements_consistent_protocols(pauli_string)


def test_scaled_unitary_consistency():
    a, b = qubitron.LineQubit.range(2)
    qubitron.testing.assert_implements_consistent_protocols(2 * qubitron.X(a) * qubitron.Y(b))
    qubitron.testing.assert_implements_consistent_protocols(1j * qubitron.X(a) * qubitron.Y(b))


def test_bool():
    a = qubitron.LineQubit(0)
    assert not bool(qubitron.PauliString({}))
    assert bool(qubitron.PauliString({a: qubitron.X}))


def _pauli_string_matrix_cases():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    return (
        (qubitron.X(q0) * 2, None, np.array([[0, 2], [2, 0]])),
        (qubitron.X(q0) * qubitron.Y(q1), (q0,), np.array([[0, 1], [1, 0]])),
        (qubitron.X(q0) * qubitron.Y(q1), (q1,), np.array([[0, -1j], [1j, 0]])),
        (
            qubitron.X(q0) * qubitron.Y(q1),
            None,
            np.array([[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (
            qubitron.X(q0) * qubitron.Y(q1),
            (q0, q1),
            np.array([[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (
            qubitron.X(q0) * qubitron.Y(q1),
            (q1, q0),
            np.array([[0, 0, 0, -1j], [0, 0, -1j, 0], [0, 1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (qubitron.X(q0) * qubitron.Y(q1), (q2,), np.eye(2)),
        (
            qubitron.X(q0) * qubitron.Y(q1),
            (q2, q1),
            np.array([[0, -1j, 0, 0], [1j, 0, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]]),
        ),
        (
            qubitron.X(q0) * qubitron.Y(q1),
            (q2, q0, q1),
            np.array(
                [
                    [0, 0, 0, -1j, 0, 0, 0, 0],
                    [0, 0, 1j, 0, 0, 0, 0, 0],
                    [0, -1j, 0, 0, 0, 0, 0, 0],
                    [1j, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, -1j],
                    [0, 0, 0, 0, 0, 0, 1j, 0],
                    [0, 0, 0, 0, 0, -1j, 0, 0],
                    [0, 0, 0, 0, 1j, 0, 0, 0],
                ]
            ),
        ),
    )


@pytest.mark.parametrize('pauli_string, qubits, expected_matrix', _pauli_string_matrix_cases())
def test_matrix(pauli_string, qubits, expected_matrix):
    assert np.allclose(pauli_string.matrix(qubits), expected_matrix)


def test_unitary_matrix():
    a, b = qubitron.LineQubit.range(2)
    assert not qubitron.has_unitary(2 * qubitron.X(a) * qubitron.Z(b))
    assert qubitron.unitary(2 * qubitron.X(a) * qubitron.Z(b), default=None) is None
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.X(a) * qubitron.Z(b)),
        np.array(
            [
                [0, 0, 1, 0],
                [0, 0, 0, -1],
                [1, 0, 0, 0],
                [0, -1, 0, 0],
            ]
        ),
    )
    np.testing.assert_allclose(
        qubitron.unitary(1j * qubitron.X(a) * qubitron.Z(b)),
        np.array(
            [
                [0, 0, 1j, 0],
                [0, 0, 0, -1j],
                [1j, 0, 0, 0],
                [0, -1j, 0, 0],
            ]
        ),
    )
    # fmt: on


def test_decompose():
    a, b = qubitron.LineQubit.range(2)
    assert qubitron.decompose_once(2 * qubitron.X(a) * qubitron.Z(b), default=None) is None
    assert qubitron.decompose_once(1j * qubitron.X(a) * qubitron.Z(b)) == [
        qubitron.global_phase_operation(1j),
        qubitron.X(a),
        qubitron.Z(b),
    ]
    assert qubitron.decompose_once(qubitron.Y(b) * qubitron.Z(a)) == [qubitron.Y(b), qubitron.Z(a)]


def test_rejects_non_paulis():
    q = qubitron.NamedQubit('q')
    with pytest.raises(TypeError):
        _ = qubitron.PauliString({q: qubitron.S})


def test_cannot_multiply_by_non_paulis():
    q = qubitron.NamedQubit('q')
    with pytest.raises(TypeError):
        _ = qubitron.X(q) * qubitron.Z(q) ** 0.5
    with pytest.raises(TypeError):
        _ = qubitron.Z(q) ** 0.5 * qubitron.X(q)
    with pytest.raises(TypeError):
        _ = qubitron.Y(q) * qubitron.S(q)


def test_filters_identities():
    q1, q2 = qubitron.LineQubit.range(2)
    assert qubitron.PauliString({q1: qubitron.I, q2: qubitron.X}) == qubitron.PauliString({q2: qubitron.X})


def test_expectation_from_state_vector_invalid_input():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y})
    wf = np.array([1, 0, 0, 0], dtype=np.complex64)
    q_map = {q0: 0, q1: 1}

    im_ps = (1j + 1) * ps
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_ps.expectation_from_state_vector(wf, q_map)

    with pytest.raises(TypeError, match='dtype'):
        ps.expectation_from_state_vector(np.array([1, 0], dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_state_vector(wf, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_state_vector(wf, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: -1, q1: 1})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: 0, q1: 3})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: 0, q1: 0})
    # Excess keys are ignored.
    _ = ps.expectation_from_state_vector(wf, {q0: 0, q1: 1, q2: 0})

    # Incorrectly shaped state_vector input.
    with pytest.raises(ValueError, match='7'):
        ps.expectation_from_state_vector(np.arange(7, dtype=np.complex64), q_map)
    q_map_2 = {q0: 0, q1: 1, q2: 2, q3: 3}
    with pytest.raises(ValueError, match='normalized'):
        ps.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map_2)

    # The ambiguous case: Density matrices satisfying L2 normalization.
    rho_or_wf = 0.5 * np.ones((2, 2), dtype=np.complex64)
    _ = ps.expectation_from_state_vector(rho_or_wf, q_map)

    wf = np.arange(16, dtype=np.complex64) / np.linalg.norm(np.arange(16))
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_state_vector(wf.reshape((16, 1)), q_map_2)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_state_vector(wf.reshape((4, 4, 1)), q_map_2)


def test_expectation_from_state_vector_check_preconditions():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y})
    q_map = {q0: 0, q1: 1, q2: 2, q3: 3}

    with pytest.raises(ValueError, match='normalized'):
        ps.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map)

    _ = ps.expectation_from_state_vector(
        np.arange(16, dtype=np.complex64), q_map, check_preconditions=False
    )


def test_expectation_from_state_vector_basis_states():
    q0 = qubitron.LineQubit(0)
    x0 = qubitron.PauliString({q0: qubitron.X})
    q_map = {q0: 0}

    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, 0], dtype=complex), q_map), 0, atol=1e-7
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([0, 1], dtype=complex), q_map), 0, atol=1e-7
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, 1], dtype=complex) / np.sqrt(2), q_map),
        1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, -1], dtype=complex) / np.sqrt(2), q_map),
        -1,
        atol=1e-7,
    )

    y0 = qubitron.PauliString({q0: qubitron.Y})
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, 1j], dtype=complex) / np.sqrt(2), q_map),
        1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, -1j], dtype=complex) / np.sqrt(2), q_map),
        -1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, 1], dtype=complex) / np.sqrt(2), q_map),
        0,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, -1], dtype=complex) / np.sqrt(2), q_map),
        0,
        atol=1e-7,
    )


def test_expectation_from_state_vector_entangled_states():
    q0, q1 = _make_qubits(2)
    z0z1_pauli_map = {q0: qubitron.Z, q1: qubitron.Z}
    z0z1 = qubitron.PauliString(z0z1_pauli_map)
    x0x1_pauli_map = {q0: qubitron.X, q1: qubitron.X}
    x0x1 = qubitron.PauliString(x0x1_pauli_map)
    q_map = {q0: 0, q1: 1}
    wf1 = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
    for state in [wf1, wf1.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), -1)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)

    wf2 = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    for state in [wf2, wf2.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), 1)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)

    wf3 = np.array([1, 1, 1, 1], dtype=complex) / 2
    for state in [wf3, wf3.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), 0)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)


def test_expectation_from_state_vector_qubit_map():
    q0, q1, q2 = _make_qubits(3)
    z = qubitron.PauliString({q0: qubitron.Z})
    wf = np.array([0, 1, 0, 1, 0, 0, 0, 0], dtype=complex) / np.sqrt(2)
    for state in [wf, wf.reshape((2, 2, 2))]:
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 0, q1: 1, q2: 2}), 1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 0, q1: 2, q2: 1}), 1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 1, q1: 0, q2: 2}), 0, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 1, q1: 2, q2: 0}), 0, atol=1e-9
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 2, q1: 0, q2: 1}), -1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 2, q1: 1, q2: 0}), -1, atol=1e-8
        )


def test_pauli_string_expectation_from_state_vector_pure_state():
    qubits = qubitron.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qubits)}

    circuit = qubitron.Circuit(
        qubitron.X(qubits[1]), qubitron.H(qubits[2]), qubitron.X(qubits[3]), qubitron.H(qubits[3])
    )
    wf = circuit.final_state_vector(
        qubit_order=qubits, ignore_terminal_measurements=False, dtype=np.complex128
    )

    z0z1 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[1]: qubitron.Z})
    z0z2 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[2]: qubitron.Z})
    z0z3 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[3]: qubitron.Z})
    z0x1 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[1]: qubitron.X})
    z1x2 = qubitron.PauliString({qubits[1]: qubitron.Z, qubits[2]: qubitron.X})
    x0z1 = qubitron.PauliString({qubits[0]: qubitron.X, qubits[1]: qubitron.Z})
    x3 = qubitron.PauliString({qubits[3]: qubitron.X})

    for state in [wf, wf.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), -1, atol=1e-8)
        np.testing.assert_allclose(z0z2.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z0z3.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z0x1.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z1x2.expectation_from_state_vector(state, q_map), -1, atol=1e-8)
        np.testing.assert_allclose(x0z1.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(x3.expectation_from_state_vector(state, q_map), -1, atol=1e-8)


def test_pauli_string_expectation_from_state_vector_pure_state_with_coef():
    qs = qubitron.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qs)}

    circuit = qubitron.Circuit(qubitron.X(qs[1]), qubitron.H(qs[2]), qubitron.X(qs[3]), qubitron.H(qs[3]))
    wf = circuit.final_state_vector(
        qubit_order=qs, ignore_terminal_measurements=False, dtype=np.complex128
    )

    z0z1 = qubitron.Z(qs[0]) * qubitron.Z(qs[1]) * 0.123
    z0z2 = qubitron.Z(qs[0]) * qubitron.Z(qs[2]) * -1
    z1x2 = -qubitron.Z(qs[1]) * qubitron.X(qs[2])

    for state in [wf, wf.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(
            z0z1.expectation_from_state_vector(state, q_map), -0.123, atol=1e-8
        )
        np.testing.assert_allclose(z0z2.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z1x2.expectation_from_state_vector(state, q_map), 1, atol=1e-8)


def test_expectation_from_density_matrix_invalid_input():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y})
    wf = qubitron.testing.random_superposition(4)
    rho = np.kron(wf.conjugate().T, wf).reshape((4, 4))
    q_map = {q0: 0, q1: 1}

    im_ps = (1j + 1) * ps
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_ps.expectation_from_density_matrix(rho, q_map)

    with pytest.raises(TypeError, match='dtype'):
        ps.expectation_from_density_matrix(0.5 * np.eye(2, dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_density_matrix(rho, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: -1, q1: 1})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q1: 3})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q1: 0})
    # Excess keys are ignored.
    _ = ps.expectation_from_density_matrix(rho, {q0: 0, q1: 1, q2: 0})

    with pytest.raises(ValueError, match='hermitian'):
        ps.expectation_from_density_matrix(1j * np.eye(4), q_map)
    with pytest.raises(ValueError, match='trace'):
        ps.expectation_from_density_matrix(np.eye(4, dtype=np.complex64), q_map)
    with pytest.raises(ValueError, match='semidefinite'):
        ps.expectation_from_density_matrix(
            np.array(
                [[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64
            ),
            q_map,
        )

    # Incorrectly shaped density matrix input.
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(np.ones((4, 5), dtype=np.complex64), q_map)
    q_map_2 = {q0: 0, q1: 1, q2: 2, q3: 3}
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(rho.reshape((4, 4, 1)), q_map_2)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(rho.reshape((-1)), q_map_2)

    # Correctly shaped state_vectors.
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(np.array([1, 0], dtype=np.complex64), q_map)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(wf, q_map)

    # The ambiguous cases: state_vectors satisfying trace normalization.
    # This also throws an unrelated warning, which is a bug. See #2041.
    rho_or_wf = 0.25 * np.ones((4, 4), dtype=np.complex64)
    _ = ps.expectation_from_density_matrix(rho_or_wf, q_map)


def test_expectation_from_density_matrix_check_preconditions():
    q0, q1 = _make_qubits(2)
    ps = qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y})
    q_map = {q0: 0, q1: 1}

    with pytest.raises(ValueError, match='semidefinite'):
        ps.expectation_from_density_matrix(
            np.array(
                [[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64
            ),
            q_map,
        )

    _ = ps.expectation_from_density_matrix(
        np.array([[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64),
        q_map,
        check_preconditions=False,
    )


def test_expectation_from_density_matrix_basis_states():
    q0 = qubitron.LineQubit(0)
    x0_pauli_map = {q0: qubitron.X}
    x0 = qubitron.PauliString(x0_pauli_map)
    q_map = {q0: 0}
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, 0], [0, 0]], dtype=complex), q_map), 0
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[0, 0], [0, 1]], dtype=complex), q_map), 0
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, 1], [1, 1]], dtype=complex) / 2, q_map), 1
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, -1], [-1, 1]], dtype=complex) / 2, q_map),
        -1,
    )


def test_expectation_from_density_matrix_entangled_states():
    q0, q1 = _make_qubits(2)
    z0z1_pauli_map = {q0: qubitron.Z, q1: qubitron.Z}
    z0z1 = qubitron.PauliString(z0z1_pauli_map)
    x0x1_pauli_map = {q0: qubitron.X, q1: qubitron.X}
    x0x1 = qubitron.PauliString(x0x1_pauli_map)
    q_map = {q0: 0, q1: 1}

    wf1 = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
    rho1 = np.kron(wf1, wf1).reshape((4, 4))
    for state in [rho1, rho1.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)

    wf2 = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    rho2 = np.kron(wf2, wf2).reshape((4, 4))
    for state in [rho2, rho2.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), 1)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)

    wf3 = np.array([1, 1, 1, 1], dtype=complex) / 2
    rho3 = np.kron(wf3, wf3).reshape((4, 4))
    for state in [rho3, rho3.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)


def test_expectation_from_density_matrix_qubit_map():
    q0, q1, q2 = _make_qubits(3)
    z = qubitron.PauliString({q0: qubitron.Z})
    wf = np.array([0, 1, 0, 1, 0, 0, 0, 0], dtype=complex) / np.sqrt(2)
    rho = np.kron(wf, wf).reshape((8, 8))

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 0, q1: 1, q2: 2}), 1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 0, q1: 2, q2: 1}), 1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 1, q1: 0, q2: 2}), 0
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 1, q1: 2, q2: 0}), 0
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 2, q1: 0, q2: 1}), -1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 2, q1: 1, q2: 0}), -1
        )


def test_pauli_string_expectation_from_density_matrix_pure_state():
    qubits = qubitron.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qubits)}

    circuit = qubitron.Circuit(
        qubitron.X(qubits[1]), qubitron.H(qubits[2]), qubitron.X(qubits[3]), qubitron.H(qubits[3])
    )
    state_vector = circuit.final_state_vector(
        qubit_order=qubits, ignore_terminal_measurements=False, dtype=np.complex128
    )
    rho = np.outer(state_vector, np.conj(state_vector))

    z0z1 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[1]: qubitron.Z})
    z0z2 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[2]: qubitron.Z})
    z0z3 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[3]: qubitron.Z})
    z0x1 = qubitron.PauliString({qubits[0]: qubitron.Z, qubits[1]: qubitron.X})
    z1x2 = qubitron.PauliString({qubits[1]: qubitron.Z, qubits[2]: qubitron.X})
    x0z1 = qubitron.PauliString({qubits[0]: qubitron.X, qubits[1]: qubitron.Z})
    x3 = qubitron.PauliString({qubits[3]: qubitron.X})

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(z0z2.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z0z3.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z0x1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z1x2.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(x0z1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(x3.expectation_from_density_matrix(state, q_map), -1)


def test_pauli_string_expectation_from_density_matrix_pure_state_with_coef():
    qs = qubitron.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qs)}

    circuit = qubitron.Circuit(qubitron.X(qs[1]), qubitron.H(qs[2]), qubitron.X(qs[3]), qubitron.H(qs[3]))
    state_vector = circuit.final_state_vector(
        qubit_order=qs, ignore_terminal_measurements=False, dtype=np.complex128
    )
    rho = np.outer(state_vector, np.conj(state_vector))

    z0z1 = qubitron.Z(qs[0]) * qubitron.Z(qs[1]) * 0.123
    z0z2 = qubitron.Z(qs[0]) * qubitron.Z(qs[2]) * -1
    z1x2 = -qubitron.Z(qs[1]) * qubitron.X(qs[2])

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -0.123)
        np.testing.assert_allclose(z0z2.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z1x2.expectation_from_density_matrix(state, q_map), 1)


def test_pauli_string_expectation_from_state_vector_mixed_state_linearity():
    n_qubits = 6

    state_vector1 = qubitron.testing.random_superposition(2**n_qubits)
    state_vector2 = qubitron.testing.random_superposition(2**n_qubits)
    rho1 = np.outer(state_vector1, np.conj(state_vector1))
    rho2 = np.outer(state_vector2, np.conj(state_vector2))
    density_matrix = rho1 / 2 + rho2 / 2

    qubits = qubitron.LineQubit.range(n_qubits)
    q_map = {q: i for i, q in enumerate(qubits)}
    paulis = [qubitron.X, qubitron.Y, qubitron.Z]
    pauli_string = qubitron.PauliString({q: np.random.choice(paulis) for q in qubits})

    a = pauli_string.expectation_from_state_vector(state_vector1, q_map)
    b = pauli_string.expectation_from_state_vector(state_vector2, q_map)
    c = pauli_string.expectation_from_density_matrix(density_matrix, q_map)
    np.testing.assert_allclose(0.5 * (a + b), c)


def test_conjugated_by_normal_gates():
    a = qubitron.LineQubit(0)

    assert_conjugation(qubitron.X(a), qubitron.H(a), qubitron.Z(a))
    assert_conjugation(qubitron.Y(a), qubitron.H(a), -qubitron.Y(a))
    assert_conjugation(qubitron.Z(a), qubitron.H(a), qubitron.X(a))

    assert_conjugation(qubitron.X(a), qubitron.S(a), -qubitron.Y(a))
    assert_conjugation(qubitron.Y(a), qubitron.S(a), qubitron.X(a))
    assert_conjugation(qubitron.Z(a), qubitron.S(a), qubitron.Z(a))

    clifford_op = qubitron.PhasedXZGate(axis_phase_exponent=0.25, x_exponent=-1, z_exponent=0).on(a)
    assert_conjugation(qubitron.X(a), clifford_op, qubitron.Y(a))
    assert_conjugation(qubitron.Y(a), clifford_op, qubitron.X(a))
    assert_conjugation(qubitron.Z(a), clifford_op, -qubitron.Z(a))


def test_conjugated_by_op_gate_of_clifford_gate_type():
    a = qubitron.LineQubit(0)

    assert_conjugation(qubitron.X(a), qubitron.CliffordGate.from_op_list([qubitron.H(a)], [a]).on(a), qubitron.Z(a))


def test_dense():
    a, b, c, d, e = qubitron.LineQubit.range(5)
    p = qubitron.PauliString([qubitron.X(a), qubitron.Y(b), qubitron.Z(c)])
    assert p.dense([a, b, c, d]) == qubitron.DensePauliString('XYZI')
    assert p.dense([d, e, a, b, c]) == qubitron.DensePauliString('IIXYZ')
    assert -p.dense([a, b, c, d]) == -qubitron.DensePauliString('XYZI')

    with pytest.raises(ValueError, match=r'not self.keys\(\) <= set\(qubits\)'):
        _ = p.dense([a, b])
    with pytest.raises(ValueError, match=r'not self.keys\(\) <= set\(qubits\)'):
        _ = p.dense([a, b, d])


@pytest.mark.parametrize('qubits', [*itertools.permutations(qubitron.LineQubit.range(3))])
def test_gate_consistent(qubits):
    g = qubitron.DensePauliString('XYZ')
    assert g == g(*qubits).gate
    a, b, c = qubitron.GridQubit.rect(1, 3)
    ps = qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c)
    assert ps.gate == ps.with_qubits(*qubits).gate


def test_conjugated_by_incorrectly_powered_cliffords():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliString([qubitron.X(a), qubitron.Z(b)])
    cliffords = [
        qubitron.H(a),
        qubitron.X(a),
        qubitron.Y(a),
        qubitron.Z(a),
        qubitron.H(a),
        qubitron.CNOT(a, b),
        qubitron.CZ(a, b),
        qubitron.SWAP(a, b),
        qubitron.ISWAP(a, b),
        qubitron.XX(a, b),
        qubitron.YY(a, b),
        qubitron.ZZ(a, b),
    ]
    for c in cliffords:
        with pytest.raises(
            ValueError,
            match='Clifford Gate can only be constructed from the operations'
            ' that has stabilizer effect.',
        ):
            _ = p.conjugated_by(c**0.1)
        with pytest.raises(
            ValueError,
            match='Clifford Gate can only be constructed from the operations'
            ' that has stabilizer effect.',
        ):
            _ = p.conjugated_by(c ** sympy.Symbol('t'))


def test_conjugated_by_global_phase():
    """Global phase gate preserves PauliString."""
    a = qubitron.LineQubit(0)
    assert_conjugation(qubitron.X(a), qubitron.global_phase_operation(1j), qubitron.X(a))
    assert_conjugation(qubitron.X(a), qubitron.global_phase_operation(np.exp(1.1j)), qubitron.X(a))

    class DecomposeGlobal(qubitron.Gate):
        def num_qubits(self):
            return 1

        def _decompose_(self, qubits):
            yield qubitron.global_phase_operation(1j)

    assert_conjugation(qubitron.X(a), DecomposeGlobal().on(a), qubitron.X(a))


def test_conjugated_by_composite_with_disjoint_sub_gates():
    a, b = qubitron.LineQubit.range(2)

    class DecomposeDisjoint(qubitron.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            yield qubitron.H(qubits[1])

    for g1 in [qubitron.X, qubitron.Y]:
        for g2 in [qubitron.X, qubitron.Y]:
            ps = g1(a) * g2(b)
            assert ps.conjugated_by(DecomposeDisjoint().on(a, b)) == ps.conjugated_by(qubitron.H(b))


def test_conjugated_by_clifford_composite():
    class UnknownGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 4

        def _decompose_(self, qubits):
            # Involved.
            yield qubitron.SWAP(qubits[0], qubits[1])
            # Uninvolved.
            yield qubitron.SWAP(qubits[2], qubits[3])

    a, b, c, d = qubitron.LineQubit.range(4)
    ps = qubitron.X(a) * qubitron.Z(b)
    u = UnknownGate()
    assert_conjugation(ps, u(a, b, c, d), qubitron.Z(a) * qubitron.X(b))


def test_conjugated_by_move_into_uninvolved():
    a, b, c, d = qubitron.LineQubit.range(4)
    ps = qubitron.X(a) * qubitron.Z(b)
    assert_conjugation_multi_ops(ps, [qubitron.SWAP(c, d), qubitron.SWAP(b, c)], qubitron.X(a) * qubitron.Z(d))
    assert_conjugation_multi_ops(ps, [qubitron.SWAP(b, c), qubitron.SWAP(c, d)], qubitron.X(a) * qubitron.Z(c))


def test_conjugated_by_common_single_qubit_gates():
    a, b = qubitron.LineQubit.range(2)

    base_single_qubit_gates = [
        qubitron.I,
        qubitron.X,
        qubitron.Y,
        qubitron.Z,
        qubitron.X**-0.5,
        qubitron.Y**-0.5,
        qubitron.Z**-0.5,
        qubitron.X**0.5,
        qubitron.Y**0.5,
        qubitron.Z**0.5,
        qubitron.H,
    ]
    single_qubit_gates = [g**i for i in range(4) for g in base_single_qubit_gates]
    for p in [qubitron.X, qubitron.Y, qubitron.Z]:
        for g in single_qubit_gates:
            # pauli gate on a, clifford on b: pauli gate preserves.
            assert_conjugation(p(a), g(b), p(a))
            # pauli gate on a, clifford on a: check conjugation in matrices.
            assert_conjugation(p(a), g(a))


def test_conjugated_by_common_two_qubit_gates():

    a, b, c, d = qubitron.LineQubit.range(4)
    two_qubit_gates = [
        qubitron.CNOT,
        qubitron.CZ,
        qubitron.ISWAP,
        qubitron.ISWAP_INV,
        qubitron.SWAP,
        qubitron.XX**0.5,
        qubitron.YY**0.5,
        qubitron.ZZ**0.5,
        qubitron.XX,
        qubitron.YY,
        qubitron.ZZ,
        qubitron.XX**-0.5,
        qubitron.YY**-0.5,
        qubitron.ZZ**-0.5,
    ]
    for p1 in [qubitron.I, qubitron.X, qubitron.Y, qubitron.Z]:
        for p2 in [qubitron.I, qubitron.X, qubitron.Y, qubitron.Z]:
            pd = qubitron.DensePauliString([p1, p2])
            p = pd.sparse([a, b])
            for g in two_qubit_gates:
                # pauli_string on (a,b), clifford on (c,d): pauli_string preserves.
                assert_conjugation(p, g(c, d), p)
                # pauli_string on (a,b), clifford on (a,b): compare unitaries of
                # the conjugated_by and actual matrix conjugation.
                assert_conjugation(p, g.on(a, b))


def test_conjugated_by_ordering():
    """Tests .conjugated_by([op1, op2]) == .conjugated_by(op2).conjugated_by(op1)"""
    a, b = qubitron.LineQubit.range(2)
    inp = qubitron.Z(b)
    out1 = inp.conjugated_by([qubitron.H(a), qubitron.CNOT(a, b)])
    out2 = inp.conjugated_by(qubitron.CNOT(a, b)).conjugated_by(qubitron.H(a))
    assert out1 == out2 == qubitron.X(a) * qubitron.Z(b)


def test_pretty_print():
    a, b, c = qubitron.LineQubit.range(3)
    result = qubitron.PauliString({a: 'x', b: 'y', c: 'z'})

    # Test Jupyter console output from
    class FakePrinter:
        def __init__(self):
            self.text_pretty = ''

        def text(self, to_print):
            self.text_pretty += to_print

    p = FakePrinter()
    result._repr_pretty_(p, False)
    assert p.text_pretty == 'X(q(0))*Y(q(1))*Z(q(2))'

    # Test cycle handling
    p = FakePrinter()
    result._repr_pretty_(p, True)
    assert p.text_pretty == 'qubitron.PauliString(...)'


# pylint: disable=line-too-long
def test_circuit_diagram_info():
    a, b, c = qubitron.LineQubit.range(3)

    assert qubitron.circuit_diagram_info(qubitron.PauliString(), default=None) is None

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.PauliString({a: qubitron.X}),
            -qubitron.PauliString({a: qubitron.X}),
            qubitron.X(a) * qubitron.Z(c),
            1j * qubitron.X(a) * qubitron.Y(b),
            -1j * qubitron.Y(b),
            1j**0.5 * qubitron.X(a) * qubitron.Y(b),
        ),
        """
0: ───PauliString(+X)───PauliString(-X)───PauliString(+X)───PauliString(iX)──────────────────────PauliString((0.707+0.707i)*X)───
                                          │                 │                                    │
1: ───────────────────────────────────────┼─────────────────Y─────────────────PauliString(-iY)───Y───────────────────────────────
                                          │
2: ───────────────────────────────────────Z──────────────────────────────────────────────────────────────────────────────────────
        """,
    )


# pylint: enable=line-too-long


def test_mutable_pauli_string_init_raises():
    q = qubitron.LineQubit.range(3)
    with pytest.raises(ValueError, match='must be between 1 and 3'):
        _ = qubitron.MutablePauliString(pauli_int_dict={q[0]: 0, q[1]: 1, q[2]: 2})


def test_mutable_pauli_string_equality():
    eq = qubitron.testing.EqualsTester()
    a, b, c = qubitron.LineQubit.range(3)

    eq.add_equality_group(
        qubitron.MutablePauliString(),
        qubitron.MutablePauliString(),
        qubitron.MutablePauliString(1),
        qubitron.MutablePauliString(-1, -1),
        qubitron.MutablePauliString({a: 0}),
        qubitron.MutablePauliString({a: "I"}),
        qubitron.MutablePauliString({a: qubitron.I}),
        qubitron.MutablePauliString(qubitron.I(a)),
        qubitron.MutablePauliString(qubitron.I(b)),
    )

    eq.add_equality_group(
        qubitron.MutablePauliString({a: "X"}),
        qubitron.MutablePauliString({a: 1}),
        qubitron.MutablePauliString({a: qubitron.X}),
        qubitron.MutablePauliString(qubitron.X(a)),
    )

    eq.add_equality_group(
        qubitron.MutablePauliString({b: "X"}),
        qubitron.MutablePauliString({b: 1}),
        qubitron.MutablePauliString({b: qubitron.X}),
        qubitron.MutablePauliString(qubitron.X(b)),
        qubitron.MutablePauliString(-1j, qubitron.Y(b), qubitron.Z(b)),
    )

    eq.add_equality_group(
        qubitron.MutablePauliString({a: "X", b: "Y", c: "Z"}),
        qubitron.MutablePauliString({a: 1, b: 2, c: 3}),
        qubitron.MutablePauliString({a: qubitron.X, b: qubitron.Y, c: qubitron.Z}),
        qubitron.MutablePauliString(qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c)),
        qubitron.MutablePauliString(qubitron.MutablePauliString(qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c))),
        qubitron.MutablePauliString(qubitron.MutablePauliString(qubitron.X(a), qubitron.Y(b), qubitron.Z(c))),
    )

    # Cross-type equality. (Can't use tester because hashability differs.)
    p = qubitron.X(a) * qubitron.Y(b)
    assert p == qubitron.MutablePauliString(p)

    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        _ = qubitron.MutablePauliString("test")
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        # noinspection PyTypeChecker
        _ = qubitron.MutablePauliString(object())


def test_mutable_pauli_string_inplace_multiplication():
    a, b, c = qubitron.LineQubit.range(3)
    p = qubitron.MutablePauliString()
    original = p

    # Support for *=.
    p *= qubitron.X(a)
    assert p == qubitron.X(a) and p is original

    # Bad operand.
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        p.inplace_left_multiply_by([qubitron.X(a), qubitron.CZ(a, b), qubitron.Z(b)])
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        p.inplace_left_multiply_by(qubitron.CZ(a, b))
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        p.inplace_right_multiply_by([qubitron.X(a), qubitron.CZ(a, b), qubitron.Z(b)])
    with pytest.raises(TypeError, match="qubitron.PAULI_STRING_LIKE"):
        p.inplace_right_multiply_by(qubitron.CZ(a, b))
    assert p == qubitron.X(a) and p is original

    # Correct order of *=.
    p *= qubitron.Y(a)
    assert p == -1j * qubitron.Z(a) and p is original
    p *= qubitron.Y(a)
    assert p == qubitron.X(a) and p is original

    # Correct order of inplace_left_multiply_by.
    p.inplace_left_multiply_by(qubitron.Y(a))
    assert p == 1j * qubitron.Z(a) and p is original
    p.inplace_left_multiply_by(qubitron.Y(a))
    assert p == qubitron.X(a) and p is original

    # Correct order of inplace_right_multiply_by.
    p.inplace_right_multiply_by(qubitron.Y(a))
    assert p == -1j * qubitron.Z(a) and p is original
    p.inplace_right_multiply_by(qubitron.Y(a))
    assert p == qubitron.X(a) and p is original

    # Multi-qubit case.
    p *= -1 * qubitron.X(a) * qubitron.X(b)
    assert p == -qubitron.X(b) and p is original

    # Support for PAULI_STRING_LIKE
    p.inplace_left_multiply_by({c: 'Z'})
    assert p == -qubitron.X(b) * qubitron.Z(c) and p is original
    p.inplace_right_multiply_by({c: 'Z'})
    assert p == -qubitron.X(b) and p is original


def test_mutable_frozen_copy():
    a, b, c = qubitron.LineQubit.range(3)
    p = -qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c)

    pf = p.frozen()
    pm = p.mutable_copy()
    pmm = pm.mutable_copy()
    pmf = pm.frozen()

    assert isinstance(p, qubitron.PauliString)
    assert isinstance(pf, qubitron.PauliString)
    assert isinstance(pm, qubitron.MutablePauliString)
    assert isinstance(pmm, qubitron.MutablePauliString)
    assert isinstance(pmf, qubitron.PauliString)

    assert p is pf
    assert pm is not pmm
    assert p == pf == pm == pmm == pmf


def test_mutable_pauli_string_inplace_conjugate_by():
    a, b, c = qubitron.LineQubit.range(3)
    p = qubitron.MutablePauliString(qubitron.X(a))

    class NoOp(qubitron.Operation):
        def __init__(self, *qubits):
            self._qubits = qubits

        @property
        def qubits(self):  # pragma: no cover
            return self._qubits

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        def _decompose_(self):
            return []

    # No-ops
    p2 = p.inplace_after(qubitron.global_phase_operation(1j))
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(NoOp(a, b))
    assert p2 is p and p == qubitron.X(a)

    # After H and back.
    p2 = p.inplace_after(qubitron.H(a))
    assert p2 is p and p == qubitron.Z(a)
    p2 = p.inplace_before(qubitron.H(a))
    assert p2 is p and p == qubitron.X(a)

    # After S and back.
    p2 = p.inplace_after(qubitron.S(a))
    assert p2 is p and p == qubitron.Y(a)
    p2 = p.inplace_before(qubitron.S(a))
    assert p2 is p and p == qubitron.X(a)

    # Before S and back.
    p2 = p.inplace_before(qubitron.S(a))
    assert p2 is p and p == -qubitron.Y(a)
    p2 = p.inplace_after(qubitron.S(a))
    assert p2 is p and p == qubitron.X(a)

    # After sqrt-X and back.
    p2 = p.inplace_before(qubitron.X(a) ** 0.5)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.X(a) ** 0.5)
    assert p2 is p and p == qubitron.X(a)

    # After sqrt-Y and back.
    p2 = p.inplace_before(qubitron.Y(a) ** 0.5)
    assert p2 is p and p == qubitron.Z(a)
    p2 = p.inplace_after(qubitron.Y(a) ** 0.5)
    assert p2 is p and p == qubitron.X(a)

    # After inv-sqrt-Y and back.
    p2 = p.inplace_before(qubitron.Y(a) ** 1.5)
    assert p2 is p and p == -qubitron.Z(a)
    p2 = p.inplace_after(qubitron.Y(a) ** 1.5)
    assert p2 is p and p == qubitron.X(a)

    # After X**0 and back.
    p2 = p.inplace_before(qubitron.X(a) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.X(a) ** 0)
    assert p2 is p and p == qubitron.X(a)

    # After Y**0 and back.
    p2 = p.inplace_before(qubitron.Y(a) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.Y(a) ** 0)
    assert p2 is p and p == qubitron.X(a)

    # After Z**0 and back.
    p2 = p.inplace_before(qubitron.Z(a) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.Z(a) ** 0)
    assert p2 is p and p == qubitron.X(a)

    # After H**0 and back.
    p2 = p.inplace_before(qubitron.H(a) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.H(a) ** 0)
    assert p2 is p and p == qubitron.X(a)

    # After inverse S and back.
    p2 = p.inplace_after(qubitron.S(a) ** -1)
    assert p2 is p and p == -qubitron.Y(a)
    p2 = p.inplace_before(qubitron.S(a) ** -1)
    assert p2 is p and p == qubitron.X(a)

    # On other qubit.
    p2 = p.inplace_after(qubitron.S(b))
    assert p2 is p and p == qubitron.X(a)

    # Two qubit operation.
    p2 = p.inplace_after(qubitron.CX(a, b) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.CZ(a, b) ** 0)
    assert p2 is p and p == qubitron.X(a)
    p2 = p.inplace_after(qubitron.CZ(a, b))
    assert p2 is p and p == qubitron.X(a) * qubitron.Z(b)
    p2 = p.inplace_after(qubitron.CZ(a, c))
    assert p2 is p and p == qubitron.X(a) * qubitron.Z(b) * qubitron.Z(c)
    p2 = p.inplace_after(qubitron.H(b))
    assert p2 is p and p == qubitron.X(a) * qubitron.X(b) * qubitron.Z(c)
    p2 = p.inplace_after(qubitron.CNOT(b, c))
    assert p2 is p and p == -qubitron.X(a) * qubitron.Y(b) * qubitron.Y(c)

    # Inverted interactions.
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.Y, True, qubitron.Z, False).on(a, b))
    assert p2 is p and p == qubitron.X(a) * qubitron.Z(b)
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.X, False, qubitron.Z, True).on(a, b))
    assert p2 is p and p == qubitron.X(a)
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.Y, False, qubitron.Z, True).on(a, b))
    assert p2 is p and p == -qubitron.X(a) * qubitron.Z(b)
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.Z, False, qubitron.Y, True).on(a, b))
    assert p2 is p and p == -qubitron.X(a) * qubitron.Y(b)
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.Z, True, qubitron.X, False).on(a, b))
    assert p2 is p and p == qubitron.X(a) * qubitron.X(b)
    p = qubitron.MutablePauliString(qubitron.X(a))
    p2 = p.inplace_after(qubitron.PauliInteractionGate(qubitron.Z, True, qubitron.Y, False).on(a, b))
    assert p2 is p and p == qubitron.X(a) * qubitron.Y(b)


def test_after_before_vs_conjugate_by():
    a, b, c = qubitron.LineQubit.range(3)
    p = qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c)
    assert p.before(qubitron.S(b)) == p.conjugated_by(qubitron.S(b))
    assert p.after(qubitron.S(b) ** -1) == p.conjugated_by(qubitron.S(b))
    assert (
        p.before(qubitron.CNOT(a, b)) == p.conjugated_by(qubitron.CNOT(a, b)) == (p.after(qubitron.CNOT(a, b)))
    )


def test_mutable_pauli_string_dict_functionality():
    a, b, c = qubitron.LineQubit.range(3)
    p = qubitron.MutablePauliString()
    with pytest.raises(KeyError):
        _ = p[a]
    assert p.get(a) is None
    assert a not in p
    assert not bool(p)
    p[a] = qubitron.X
    assert bool(p)
    assert a in p
    assert p[a] == qubitron.X

    p[a] = "Y"
    assert p[a] == qubitron.Y
    p[a] = 3
    assert p[a] == qubitron.Z
    p[a] = "I"
    assert a not in p
    p[a] = 0
    assert a not in p

    assert len(p) == 0
    p[b] = "Y"
    p[a] = "X"
    p[c] = "Z"
    assert len(p) == 3
    assert list(iter(p)) == [b, a, c]
    assert list(p.values()) == [qubitron.Y, qubitron.X, qubitron.Z]
    assert list(p.keys()) == [b, a, c]
    assert p.keys() == {a, b, c}
    assert p.keys() ^ {c} == {a, b}

    del p[b]
    assert b not in p


@pytest.mark.parametrize(
    'pauli', (qubitron.X, qubitron.Y, qubitron.Z, qubitron.I, "I", "X", "Y", "Z", "i", "x", "y", "z", 0, 1, 2, 3)
)
def test_mutable_pauli_string_dict_pauli_like(pauli):
    p = qubitron.MutablePauliString()
    # Check that is successfully converts.
    p[0] = pauli


def test_mutable_pauli_string_dict_pauli_like_not_pauli_like():
    p = qubitron.MutablePauliString()
    # Check error string includes terms like "X" in error message.
    with pytest.raises(TypeError, match="PAULI_GATE_LIKE.*X"):
        p[0] = 1.2


def test_mutable_pauli_string_text():
    p = qubitron.MutablePauliString(qubitron.X(qubitron.LineQubit(0)) * qubitron.Y(qubitron.LineQubit(1)))
    assert str(qubitron.MutablePauliString()) == "mutable I"
    assert str(p) == "mutable X(q(0))*Y(q(1))"
    qubitron.testing.assert_equivalent_repr(p)


def test_mutable_pauli_string_mul():
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.X(a).mutable_copy()
    q = qubitron.Y(b).mutable_copy()
    pq = qubitron.X(a) * qubitron.Y(b)
    assert p * q == pq
    assert isinstance(p * q, qubitron.PauliString)
    assert 2 * p == qubitron.X(a) * 2 == p * 2
    assert isinstance(p * 2, qubitron.PauliString)
    assert isinstance(2 * p, qubitron.PauliString)


def test_mutable_can_override_mul():
    class LMul:
        def __mul__(self, other):
            return "Yay!"

    class RMul:
        def __rmul__(self, other):
            return "Yay!"

    assert qubitron.MutablePauliString() * RMul() == "Yay!"
    assert LMul() * qubitron.MutablePauliString() == "Yay!"


def test_coefficient_precision():
    qs = qubitron.LineQubit.range(4 * 10**3)
    r = qubitron.MutablePauliString({q: qubitron.X for q in qs})
    r2 = qubitron.MutablePauliString({q: qubitron.Y for q in qs})
    r2 *= r
    assert r2.coefficient == 1


def test_transform_qubits():
    a, b, c = qubitron.LineQubit.range(3)
    p = qubitron.X(a) * qubitron.Z(b)
    p2 = qubitron.X(b) * qubitron.Z(c)
    m = p.mutable_copy()
    m2 = m.transform_qubits(lambda q: q + 1)
    assert m is not m2
    assert m == p
    assert m2 == p2

    m2 = m.transform_qubits(lambda q: q + 1, inplace=False)
    assert m is not m2
    assert m == p
    assert m2 == p2

    m2 = m.transform_qubits(lambda q: q + 1, inplace=True)
    assert m is m2
    assert m == p2
    assert m2 == p2


def test_parameterization():
    t = sympy.Symbol('t')
    q = qubitron.LineQubit(0)
    pst = qubitron.PauliString({q: 'x'}, coefficient=t)
    assert qubitron.is_parameterized(pst)
    assert qubitron.parameter_names(pst) == {'t'}
    assert pst.coefficient == 1.0 * t
    assert not qubitron.has_unitary(pst)
    assert not qubitron.is_parameterized(pst.with_coefficient(2))
    with pytest.raises(TypeError):
        qubitron.decompose_once(pst)
    with pytest.raises(NotImplementedError, match='parameterized'):
        pst.expectation_from_state_vector(np.array([]), {})
    with pytest.raises(NotImplementedError, match='parameterized'):
        pst.expectation_from_density_matrix(np.array([]), {})
    with pytest.raises(NotImplementedError, match='as matrix when parameterized'):
        pst.matrix()
    assert pst**1 == pst
    assert pst**-1 == pst.with_coefficient(1.0 / t)
    assert (-pst) ** 1 == -pst
    assert (-pst) ** -1 == -pst.with_coefficient(1.0 / t)
    assert (1j * pst) ** 1 == 1j * pst
    assert (1j * pst) ** -1 == -1j * pst.with_coefficient(1.0 / t)
    with pytest.raises(TypeError):
        _ = pst**2
    with pytest.raises(TypeError):
        _ = 1**pst
    qubitron.testing.assert_has_diagram(qubitron.Circuit(pst), '0: ───PauliString((1.0*t)*X)───')


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve(resolve_fn):
    t = sympy.Symbol('t')
    q = qubitron.LineQubit(0)
    pst = qubitron.PauliString({q: 'x'}, coefficient=t)
    ps1 = qubitron.PauliString({q: 'x'}, coefficient=1j)
    assert resolve_fn(pst, {'t': 1j}) == ps1
