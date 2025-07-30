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

import numbers

import numpy as np
import pytest
import sympy

import qubitron
from qubitron.ops.dense_pauli_string import _vectorized_pauli_mul_phase


def test_init():
    mask = np.array([0, 3, 1, 2], dtype=np.uint8)
    p = qubitron.DensePauliString(coefficient=2, pauli_mask=mask)
    m = qubitron.MutableDensePauliString(coefficient=3, pauli_mask=mask)
    assert p.coefficient == 2
    assert m.coefficient == 3
    np.testing.assert_allclose(p.pauli_mask, [0, 3, 1, 2])
    np.testing.assert_allclose(m.pauli_mask, [0, 3, 1, 2])

    # The non-mutable initializer makes a copy.
    assert m.pauli_mask is mask
    assert p.pauli_mask is not mask
    mask[:] = 0
    assert m.pauli_mask[2] == 0
    assert p.pauli_mask[2] == 1

    # Copies and converts non-uint8 arrays.
    p2 = qubitron.DensePauliString(coefficient=2, pauli_mask=[1, 2, 3])
    m2 = qubitron.DensePauliString(coefficient=2, pauli_mask=[1, 2, 3])
    assert p2.pauli_mask.dtype == m2.pauli_mask.dtype == np.uint8
    assert list(p2.pauli_mask) == list(m2.pauli_mask) == [1, 2, 3]

    # Mixed types.
    assert qubitron.DensePauliString([1, 'X', qubitron.X]) == qubitron.DensePauliString('XXX')
    assert list(qubitron.DensePauliString('XXX')) == [qubitron.X, qubitron.X, qubitron.X]
    with pytest.raises(TypeError, match='Expected a qubitron.PAULI_GATE_LIKE'):
        _ = qubitron.DensePauliString([object()])


def test_value_to_char_correspondence():
    d = qubitron.DensePauliString
    assert [d.I_VAL, d.X_VAL, d.Y_VAL, d.Z_VAL] == [0, 1, 2, 3]
    assert list(d([qubitron.I, qubitron.X, qubitron.Y, qubitron.Z]).pauli_mask) == [0, 1, 2, 3]
    assert list(d("IXYZ").pauli_mask) == [0, 1, 2, 3]
    assert list(d([d.I_VAL, d.X_VAL, d.Y_VAL, d.Z_VAL]).pauli_mask) == [0, 1, 2, 3]

    assert d('Y') * d('Z') == 1j * d('X')
    assert d('Z') * d('X') == 1j * d('Y')
    assert d('X') * d('Y') == 1j * d('Z')

    assert d('Y') * d('X') == -1j * d('Z')
    assert d('X') * d('Z') == -1j * d('Y')
    assert d('Z') * d('Y') == -1j * d('X')


def test_from_text():
    d = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    assert d('') == d(pauli_mask=[])
    assert m('') == m(pauli_mask=[])

    assert d('YYXYY') == d([2, 2, 1, 2, 2])
    assert d('XYZI') == d([1, 2, 3, 0])
    assert d('III', coefficient=-1) == d([0, 0, 0], coefficient=-1)
    assert d('XXY', coefficient=1j) == d([1, 1, 2], coefficient=1j)
    assert d('ixyz') == d([0, 1, 2, 3])
    assert d(['i', 'x', 'y', 'z']) == d([0, 1, 2, 3])
    with pytest.raises(TypeError, match='Expected a qubitron.PAULI_GATE_LIKE'):
        _ = d('2')


def test_immutable_eq():
    eq = qubitron.testing.EqualsTester()

    # Immutables
    eq.make_equality_group(lambda: qubitron.DensePauliString(coefficient=2, pauli_mask=[1]))
    eq.add_equality_group(lambda: qubitron.DensePauliString(coefficient=3, pauli_mask=[1]))
    eq.make_equality_group(lambda: qubitron.DensePauliString(coefficient=2, pauli_mask=[]))
    eq.add_equality_group(lambda: qubitron.DensePauliString(coefficient=2, pauli_mask=[0]))
    eq.make_equality_group(lambda: qubitron.DensePauliString(coefficient=2, pauli_mask=[2]))

    # Mutables
    eq.make_equality_group(lambda: qubitron.MutableDensePauliString(coefficient=2, pauli_mask=[1]))
    eq.add_equality_group(lambda: qubitron.MutableDensePauliString(coefficient=3, pauli_mask=[1]))
    eq.make_equality_group(lambda: qubitron.MutableDensePauliString(coefficient=2, pauli_mask=[]))
    eq.make_equality_group(lambda: qubitron.MutableDensePauliString(coefficient=2, pauli_mask=[2]))


def test_eye():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString
    assert qubitron.BaseDensePauliString.eye(4) == f('IIII')
    assert qubitron.DensePauliString.eye(4) == f('IIII')
    assert qubitron.MutableDensePauliString.eye(4) == m('IIII')


def test_sparse():
    a, b, c = qubitron.LineQubit.range(3)
    p = -qubitron.DensePauliString('XYZ')
    assert p.sparse() == qubitron.PauliString(-1, qubitron.X(a), qubitron.Y(b), qubitron.Z(c))
    assert p.sparse([c, b, a]) == qubitron.PauliString(-1, qubitron.X(c), qubitron.Y(b), qubitron.Z(a))
    with pytest.raises(ValueError, match='number of qubits'):
        _ = p.sparse([])
    with pytest.raises(ValueError, match='number of qubits'):
        _ = p.sparse(qubitron.GridQubit.rect(2, 2))


def test_mul_vectorized_pauli_mul_phase():
    f = _vectorized_pauli_mul_phase
    paulis = [qubitron.I, qubitron.X, qubitron.Y, qubitron.Z]
    q = qubitron.LineQubit(0)

    # Check single qubit cases.
    for i in range(4):
        for j in range(4):
            sparse1 = qubitron.PauliString(paulis[i].on(q))
            sparse2 = qubitron.PauliString(paulis[j].on(q))
            assert f(i, j) == (sparse1 * sparse2).coefficient

    # Check a vector case.
    assert (
        _vectorized_pauli_mul_phase(
            np.array([0, 1, 3, 2], dtype=np.uint8), np.array([0, 1, 2, 0], dtype=np.uint8)
        )
        == -1j
    )
    assert (
        _vectorized_pauli_mul_phase(np.array([], dtype=np.uint8), np.array([], dtype=np.uint8)) == 1
    )


def test_mul():
    f = qubitron.DensePauliString

    # Scalar.
    assert -1 * f('XXX') == -1.0 * f('XXX') == f('XXX', coefficient=-1)
    assert 2 * f('XXX') == f('XXX') * 2 == (2 + 0j) * f('XXX')
    assert 2 * f('XXX') == f('XXX', coefficient=2)

    # Pair.
    assert f('') * f('') == f('')
    assert -f('X') * (1j * f('X')) == -1j * f('I')
    assert f('IXYZ') * f('XXXX') == f('XIZY')
    assert f('IXYX') * f('XXXX') == -1j * f('XIZI')
    assert f('XXXX') * f('IXYX') == 1j * f('XIZI')

    # Pauli operations.
    assert f('IXYZ') * qubitron.X(qubitron.LineQubit(0)) == f('XXYZ')
    assert -f('IXYZ') * qubitron.X(qubitron.LineQubit(1)) == -f('IIYZ')
    assert f('IXYZ') * qubitron.X(qubitron.LineQubit(2)) == -1j * f('IXZZ')
    assert qubitron.X(qubitron.LineQubit(0)) * f('IXYZ') == f('XXYZ')
    assert qubitron.X(qubitron.LineQubit(1)) * -f('IXYZ') == -f('IIYZ')
    assert qubitron.X(qubitron.LineQubit(2)) * f('IXYZ') == 1j * f('IXZZ')
    with pytest.raises(ValueError, match='other than `qubitron.LineQubit'):
        _ = f('III') * qubitron.X(qubitron.NamedQubit('tmp'))

    # Mixed types.
    m = qubitron.MutableDensePauliString
    assert m('X') * m('Z') == -1j * m('Y')
    assert m('X') * f('Z') == -1j * m('Y')
    assert f('X') * m('Z') == -1j * m('Y')
    assert isinstance(f('') * f(''), qubitron.DensePauliString)
    assert isinstance(m('') * m(''), qubitron.MutableDensePauliString)
    assert isinstance(m('') * f(''), qubitron.MutableDensePauliString)
    assert isinstance(f('') * m(''), qubitron.MutableDensePauliString)

    # Different lengths.
    assert f('I') * f('III') == f('III')
    assert f('X') * f('XXX') == f('IXX')
    assert f('XXX') * f('X') == f('IXX')

    with pytest.raises(TypeError):
        _ = f('I') * object()
    with pytest.raises(TypeError):
        _ = object() * f('I')

    # Unknown number type
    class UnknownNumber(numbers.Number):
        pass

    with pytest.raises(TypeError):
        _ = UnknownNumber() * f('I')


def test_imul():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    # Immutable not modified by imul.
    p = f('III')
    p2 = p
    p2 *= 2
    assert p.coefficient == 1
    assert p is not p2

    # Mutable is modified by imul.
    p = m('III')
    p2 = p
    p2 *= 2
    assert p.coefficient == 2
    assert p is p2

    p *= f('X')
    assert p == m('XII', coefficient=2)

    p *= m('XY')
    assert p == m('IYI', coefficient=2)

    p *= 1j
    assert p == m('IYI', coefficient=2j)

    p *= 0.5
    assert p == m('IYI', coefficient=1j)

    p *= qubitron.X(qubitron.LineQubit(1))
    assert p == m('IZI')

    with pytest.raises(ValueError, match='smaller than'):
        p *= f('XXXXXXXXXXXX')
    with pytest.raises(TypeError):
        p *= object()

    # Unknown number type
    class UnknownNumber(numbers.Number):
        pass

    with pytest.raises(TypeError):
        p *= UnknownNumber()


def test_pos_neg():
    p = 1j * qubitron.DensePauliString('XYZ')
    assert +p == p
    assert -p == -1 * p


def test_abs():
    f = qubitron.DensePauliString
    m = qubitron.DensePauliString
    assert abs(-f('XX')) == f('XX')
    assert abs(2j * f('XX')) == 2 * f('XX')
    assert abs(2j * m('XX')) == 2 * f('XX')


def test_approx_eq():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    # Tolerance matters.
    assert qubitron.approx_eq(1.00001 * f('X'), f('X'), atol=1e-4)
    assert qubitron.approx_eq(m('X', coefficient=1.00001), m('X'), atol=1e-4)
    assert not qubitron.approx_eq(1.00001 * f('X'), f('X'), atol=1e-8)
    assert not qubitron.approx_eq(1.00001 * m('X'), m('X'), atol=1e-8)

    # Must be same type.
    assert not qubitron.approx_eq(f('X'), m('X'), atol=1e-4)

    # Differing paulis ignores tolerance.
    assert not qubitron.approx_eq(f('X'), f('YYY'), atol=1e-8)
    assert not qubitron.approx_eq(f('X'), f('Y'), atol=1e-8)
    assert not qubitron.approx_eq(f('X'), f('Y'), atol=500)


def test_pow():
    f = qubitron.DensePauliString
    m = qubitron.DensePauliString
    p = 1j * f('IXYZ')
    assert p**0 == p**4 == p**8 == qubitron.DensePauliString.eye(4)
    assert p**1 == p**5 == p**-3 == p == p**101
    assert p**2 == p**-2 == p**6 == -f('IIII')
    assert p**3 == p**-1 == p**7 == -1j * f('IXYZ')

    p = -f('IXYZ')
    assert p == p**1 == p**-1 == p**-3 == p**-303
    assert p**0 == p**2 == p**-2 == p**-4 == p**102

    p = 2 * f('XX')
    assert p**-1 == (0.5 + 0j) * f('XX')
    assert p**0 == f('II')
    assert p**1 == 2 * f('XX')
    assert p**2 == 4 * f('II')
    assert p**3 == 8 * f('XX')
    assert p**4 == 16 * f('II')

    p = -1j * f('XY')
    assert p**101 == p == p**-103

    p = 2j * f('XY')
    assert (p**-1) ** -1 == p
    assert p**-2 == f('II') / -4

    p = f('XY')
    assert p**-100 == p**0 == p**100 == f('II')
    assert p**-101 == p**1 == p**101 == f('XY')

    # Becomes an immutable copy.
    assert m('X') ** 3 == f('X')


def test_div():
    f = qubitron.DensePauliString
    t = sympy.Symbol('t')
    assert f('X') / 2 == 0.5 * f('X')
    assert f('X') / t == (1 / t) * f('X')
    with pytest.raises(TypeError):
        _ = f('X') / object()


def test_str():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    assert str(f('')) == '+'
    assert str(f('XXX')) == '+XXX'
    assert str(m('XXX')) == '+XXX (mutable)'
    assert str(2 * f('')) == '(2+0j)*'
    assert str((1 + 1j) * f('XXX')) == '(1+1j)*XXX'
    assert str(1j * f('XXX')) == '1j*XXX'
    assert str(-f('IXYZ')) == '-IXYZ'
    assert str(f('XX', coefficient=sympy.Symbol('t') + 2)) == '(t + 2)*XX'
    assert str(f('XX', coefficient=sympy.Symbol('t'))) == 't*XX'


def test_repr():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString
    qubitron.testing.assert_equivalent_repr(f(''))
    qubitron.testing.assert_equivalent_repr(-f('X'))
    qubitron.testing.assert_equivalent_repr(1j * f('XYZII'))
    qubitron.testing.assert_equivalent_repr(m(''))
    qubitron.testing.assert_equivalent_repr(-m('X'))
    qubitron.testing.assert_equivalent_repr(1j * m('XYZII'))
    qubitron.testing.assert_equivalent_repr(f(coefficient=sympy.Symbol('c'), pauli_mask=[0, 3, 2, 1]))
    qubitron.testing.assert_equivalent_repr(m(coefficient=sympy.Symbol('c'), pauli_mask=[0, 3, 2, 1]))


def test_one_hot():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    assert qubitron.DensePauliString.one_hot(index=3, length=5, pauli=qubitron.X) == f('IIIXI')
    assert qubitron.MutableDensePauliString.one_hot(index=3, length=5, pauli=qubitron.X) == m('IIIXI')

    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli='X') == f('XIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli='Y') == f('YIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli='Z') == f('ZIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli='I') == f('IIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli=qubitron.X) == f('XIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli=qubitron.Y) == f('YIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli=qubitron.Z) == f('ZIIII')
    assert qubitron.BaseDensePauliString.one_hot(index=0, length=5, pauli=qubitron.I) == f('IIIII')

    with pytest.raises(IndexError):
        _ = qubitron.BaseDensePauliString.one_hot(index=50, length=5, pauli=qubitron.X)

    with pytest.raises(IndexError):
        _ = qubitron.BaseDensePauliString.one_hot(index=0, length=0, pauli=qubitron.X)


def test_protocols():
    t = sympy.Symbol('t')
    qubitron.testing.assert_implements_consistent_protocols(qubitron.DensePauliString('Y'))
    qubitron.testing.assert_implements_consistent_protocols(-qubitron.DensePauliString('Z'))
    qubitron.testing.assert_implements_consistent_protocols(1j * qubitron.DensePauliString('X'))
    qubitron.testing.assert_implements_consistent_protocols(2 * qubitron.DensePauliString('X'))
    qubitron.testing.assert_implements_consistent_protocols(
        t * qubitron.DensePauliString('XYIZ'), ignore_decompose_to_default_gateset=True
    )
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.DensePauliString('XYIZ', coefficient=t + 2), ignore_decompose_to_default_gateset=True
    )
    qubitron.testing.assert_implements_consistent_protocols(-qubitron.DensePauliString('XYIZ'))
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.MutableDensePauliString('XYIZ', coefficient=-1)
    )

    # Unitarity and shape.
    assert qubitron.has_unitary(1j * qubitron.DensePauliString('X'))
    assert not qubitron.has_unitary(2j * qubitron.DensePauliString('X'))
    assert not qubitron.has_unitary(qubitron.DensePauliString('X') * t)
    p = -qubitron.DensePauliString('XYIZ')
    assert qubitron.num_qubits(p) == len(p) == 4


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    t = sympy.Symbol('t')
    x = qubitron.DensePauliString('X')
    xt = x * t
    x2 = x * 2
    q = qubitron.LineQubit(0)
    assert not qubitron.is_parameterized(x)
    assert not qubitron.is_parameterized(x * 2)
    assert qubitron.is_parameterized(x * t)
    assert resolve_fn(xt, {'t': 2}) == x2
    assert resolve_fn(x * 3, {'t': 2}) == x * 3
    assert resolve_fn(xt(q), {'t': 2}).gate == x2
    assert resolve_fn(xt(q).gate, {'t': 2}) == x2


def test_item_immutable():
    p = -qubitron.DensePauliString('XYIZ')
    assert p[-1] == qubitron.Z
    assert p[0] == qubitron.X
    assert p[1] == qubitron.Y
    assert p[2] == qubitron.I
    assert p[3] == qubitron.Z

    with pytest.raises(TypeError):
        _ = p["test"]
    with pytest.raises(IndexError):
        _ = p[4]
    with pytest.raises(TypeError):
        p[2] = qubitron.X
    with pytest.raises(TypeError):
        p[:] = p

    assert p[:] == abs(p)
    assert p[1:] == qubitron.DensePauliString('YIZ')
    assert p[::2] == qubitron.DensePauliString('XI')


def test_item_mutable():
    m = qubitron.MutableDensePauliString
    p = m('XYIZ', coefficient=-1)
    assert p[-1] == qubitron.Z
    assert p[0] == qubitron.X
    assert p[1] == qubitron.Y
    assert p[2] == qubitron.I
    assert p[3] == qubitron.Z
    with pytest.raises(IndexError):
        _ = p[4]
    with pytest.raises(TypeError):
        _ = p["test"]
    with pytest.raises(TypeError):
        p["test"] = 'X'

    p[2] = qubitron.X
    assert p == m('XYXZ', coefficient=-1)
    p[3] = 'X'
    p[0] = 'I'
    assert p == m('IYXX', coefficient=-1)
    p[2:] = p[:2]
    assert p == m('IYIY', coefficient=-1)
    p[2:] = 'ZZ'
    assert p == m('IYZZ', coefficient=-1)
    p[2:] = 'IY'
    assert p == m('IYIY', coefficient=-1)

    # Aliased views.
    q = p[:2]
    assert q == m('IY')
    q[0] = qubitron.Z
    assert q == m('ZY')
    assert p == m('ZYIY', coefficient=-1)

    with pytest.raises(ValueError, match='coefficient is not 1'):
        p[:] = p

    assert p[:] == m('ZYIY')
    assert p[1:] == m('YIY')
    assert p[::2] == m('ZI')

    p[2:] = 'XX'
    assert p == m('ZYXX', coefficient=-1)


def test_tensor_product():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString
    assert (2 * f('XX')).tensor_product(-f('XI')) == -2 * f('XXXI')
    assert m('XX', coefficient=2).tensor_product(-f('XI')) == -2 * m('XXXI')
    assert f('XX', coefficient=2).tensor_product(-m('XI')) == -2 * f('XXXI')
    assert m('XX', coefficient=2).tensor_product(m('XI', coefficient=-1)) == -2 * m('XXXI')


def test_commutes():
    f = qubitron.DensePauliString
    m = qubitron.MutableDensePauliString

    assert qubitron.commutes(f('XX'), m('ZZ'))
    assert qubitron.commutes(2 * f('XX'), m('ZZ', coefficient=3))
    assert qubitron.commutes(2 * f('IX'), 3 * f('IX'))
    assert not qubitron.commutes(f('IX'), f('IZ'))
    assert qubitron.commutes(f('IIIXII'), qubitron.X(qubitron.LineQubit(3)))
    assert qubitron.commutes(f('IIIXII'), qubitron.X(qubitron.LineQubit(2)))
    assert not qubitron.commutes(f('IIIXII'), qubitron.Z(qubitron.LineQubit(3)))
    assert qubitron.commutes(f('IIIXII'), qubitron.Z(qubitron.LineQubit(2)))

    assert qubitron.commutes(f('XX'), "test", default=NotImplemented) is NotImplemented


def test_copy():
    p = -qubitron.DensePauliString('XYZ')
    m = qubitron.MutableDensePauliString('XYZ', coefficient=-1)

    # Immutable copies.
    assert p.copy() is p
    assert p.frozen() is p
    assert p.mutable_copy() is not p
    assert p.mutable_copy() == m

    # Mutable copies.
    assert m.copy() is not m
    assert m.copy() == m
    assert m.frozen() == p
    assert m.mutable_copy() is not m
    assert m.mutable_copy() == m

    # Copy immutable with modifications.
    assert p.copy(coefficient=-1) is p
    assert p.copy(coefficient=-2) is not p
    assert p.copy(coefficient=-2) == -2 * qubitron.DensePauliString('XYZ')
    assert p.copy(coefficient=-2, pauli_mask=[3]) == -2 * qubitron.DensePauliString('Z')

    # Copy mutable with modifications.
    assert m.copy(coefficient=-1) is not m
    assert m.copy(coefficient=-2) is not m
    assert m.copy(coefficient=-2) == qubitron.MutableDensePauliString('XYZ', coefficient=-2)
    assert m.copy(coefficient=-2, pauli_mask=[2]) == qubitron.MutableDensePauliString(
        'Y', coefficient=-2
    )

    # Aliasing of the mask attribute when copying with modifications.
    mask = np.array([1, 2, 3], dtype=np.uint8)
    assert qubitron.MutableDensePauliString(mask).copy().pauli_mask is not mask
    assert qubitron.MutableDensePauliString(mask).copy(pauli_mask=mask).pauli_mask is mask
    assert qubitron.MutableDensePauliString('XYZ').copy(pauli_mask=mask).pauli_mask is mask


def test_gaussian_elimination():
    def table(*rows: str) -> list[qubitron.MutableDensePauliString]:
        coefs = {'i': 1j, '-': -1, '+': 1}
        return [
            qubitron.MutableDensePauliString(row[1:].replace('.', 'I'), coefficient=coefs[row[0]])
            for row in rows
        ]

    f = qubitron.MutableDensePauliString.inline_gaussian_elimination

    t = table()
    f(t)
    assert t == table()

    t = table('+X')
    f(t)
    assert t == table('+X')

    t = table("+.X.X", "+Z.Z.", "+X.XX", "+ZZ.Z")
    f(t)
    assert t == table("+X.XX", "+Z.Z.", "+.X.X", "+.ZZZ")

    t = table("+XXX", "+YYY")
    f(t)
    assert t == table("+XXX", "iZZZ")

    t = table("+XXXX", "+X...", "+..ZZ", "+.ZZ.")
    f(t)
    assert t == table("+X...", "+.XXX", "+.Z.Z", "+..ZZ")

    t = table(
        '+ZZZ.........',
        '+XX..........',
        '+X.X.........',
        '+...ZZZ......',
        '+...XX.......',
        '+...X.X......',
        '+......ZZ....',
        '+......XX....',
        '+........ZZ..',
        '+........XX..',
        '+..X....X....',
        '+..Z....Z....',
        '+.....X..X...',
        '+.....Z..Z...',
        '+.X........X.',
        '+.Z........Z.',
        '-X...X.......',
        '+Z...Z.......',
        '+...X.......X',
        '+...Z.......Z',
        '+......X..X..',
        '+......Z..Z..',
    )
    f(t)
    assert t == table(
        '-X..........X',
        '+Z........Z.Z',
        '-.X.........X',
        '+.Z.........Z',
        '-..X........X',
        '+..Z......Z..',
        '+...X.......X',
        '+...Z.......Z',
        '+....X......X',
        '+....Z....Z.Z',
        '+.....X.....X',
        '+.....Z...Z..',
        '-......X....X',
        '+......Z..Z..',
        '-.......X...X',
        '+.......Z.Z..',
        '+........X..X',
        '+........ZZ..',
        '+.........X.X',
        '-..........XX',
        '+..........ZZ',
        '-............',
    )


def test_idiv():
    p = qubitron.MutableDensePauliString('XYZ', coefficient=2)
    p /= 2
    assert p == qubitron.MutableDensePauliString('XYZ')

    with pytest.raises(TypeError):
        p /= object()


def test_symbolic():
    t = sympy.Symbol('t')
    r = sympy.Symbol('r')
    m = qubitron.MutableDensePauliString('XYZ', coefficient=t)
    f = qubitron.DensePauliString('XYZ', coefficient=t)
    assert f * r == qubitron.DensePauliString('XYZ', coefficient=t * r)
    assert m * r == qubitron.MutableDensePauliString('XYZ', coefficient=t * r)
    m *= r
    f *= r
    assert m == qubitron.MutableDensePauliString('XYZ', coefficient=t * r)
    assert f == qubitron.DensePauliString('XYZ', coefficient=t * r)
    m /= r
    f /= r
    assert m == qubitron.MutableDensePauliString('XYZ', coefficient=t)
    assert f == qubitron.DensePauliString('XYZ', coefficient=t)
