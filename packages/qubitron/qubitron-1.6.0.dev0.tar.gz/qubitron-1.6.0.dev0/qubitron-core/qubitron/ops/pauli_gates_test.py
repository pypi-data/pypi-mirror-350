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

import qubitron


def test_equals() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.X, qubitron.ops.pauli_gates.X, qubitron.XPowGate())
    eq.add_equality_group(qubitron.Y, qubitron.ops.pauli_gates.Y, qubitron.YPowGate())
    eq.add_equality_group(qubitron.Z, qubitron.ops.pauli_gates.Z, qubitron.ZPowGate())


def test_phased_pauli_product() -> None:
    assert qubitron.X.phased_pauli_product(qubitron.I) == (1, qubitron.X)
    assert qubitron.X.phased_pauli_product(qubitron.X) == (1, qubitron.I)
    assert qubitron.X.phased_pauli_product(qubitron.Y) == (1j, qubitron.Z)
    assert qubitron.X.phased_pauli_product(qubitron.Z) == (-1j, qubitron.Y)

    assert qubitron.Y.phased_pauli_product(qubitron.I) == (1, qubitron.Y)
    assert qubitron.Y.phased_pauli_product(qubitron.X) == (-1j, qubitron.Z)
    assert qubitron.Y.phased_pauli_product(qubitron.Y) == (1, qubitron.I)
    assert qubitron.Y.phased_pauli_product(qubitron.Z) == (1j, qubitron.X)

    assert qubitron.Z.phased_pauli_product(qubitron.I) == (1, qubitron.Z)
    assert qubitron.Z.phased_pauli_product(qubitron.X) == (1j, qubitron.Y)
    assert qubitron.Z.phased_pauli_product(qubitron.Y) == (-1j, qubitron.X)
    assert qubitron.Z.phased_pauli_product(qubitron.Z) == (1, qubitron.I)


def test_isinstance() -> None:
    assert isinstance(qubitron.X, qubitron.XPowGate)
    assert isinstance(qubitron.Y, qubitron.YPowGate)
    assert isinstance(qubitron.Z, qubitron.ZPowGate)

    assert not isinstance(qubitron.X, qubitron.YPowGate)
    assert not isinstance(qubitron.X, qubitron.ZPowGate)

    assert not isinstance(qubitron.Y, qubitron.XPowGate)
    assert not isinstance(qubitron.Y, qubitron.ZPowGate)

    assert not isinstance(qubitron.Z, qubitron.XPowGate)
    assert not isinstance(qubitron.Z, qubitron.YPowGate)


def test_by_index() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.X, *[qubitron.Pauli.by_index(i) for i in (-3, 0, 3, 6)])
    eq.add_equality_group(qubitron.Y, *[qubitron.Pauli.by_index(i) for i in (-2, 1, 4, 7)])
    eq.add_equality_group(qubitron.Z, *[qubitron.Pauli.by_index(i) for i in (-1, 2, 5, 8)])


def test_relative_index() -> None:
    assert qubitron.X.relative_index(qubitron.X) == 0
    assert qubitron.X.relative_index(qubitron.Y) == -1
    assert qubitron.X.relative_index(qubitron.Z) == 1
    assert qubitron.Y.relative_index(qubitron.X) == 1
    assert qubitron.Y.relative_index(qubitron.Y) == 0
    assert qubitron.Y.relative_index(qubitron.Z) == -1
    assert qubitron.Z.relative_index(qubitron.X) == -1
    assert qubitron.Z.relative_index(qubitron.Y) == 1
    assert qubitron.Z.relative_index(qubitron.Z) == 0


def test_by_relative_index() -> None:
    assert qubitron.Pauli.by_relative_index(qubitron.X, -1) == qubitron.Z
    assert qubitron.Pauli.by_relative_index(qubitron.X, 0) == qubitron.X
    assert qubitron.Pauli.by_relative_index(qubitron.X, 1) == qubitron.Y
    assert qubitron.Pauli.by_relative_index(qubitron.X, 2) == qubitron.Z
    assert qubitron.Pauli.by_relative_index(qubitron.X, 3) == qubitron.X
    assert qubitron.Pauli.by_relative_index(qubitron.Y, -1) == qubitron.X
    assert qubitron.Pauli.by_relative_index(qubitron.Y, 0) == qubitron.Y
    assert qubitron.Pauli.by_relative_index(qubitron.Y, 1) == qubitron.Z
    assert qubitron.Pauli.by_relative_index(qubitron.Y, 2) == qubitron.X
    assert qubitron.Pauli.by_relative_index(qubitron.Y, 3) == qubitron.Y
    assert qubitron.Pauli.by_relative_index(qubitron.Z, -1) == qubitron.Y
    assert qubitron.Pauli.by_relative_index(qubitron.Z, 0) == qubitron.Z
    assert qubitron.Pauli.by_relative_index(qubitron.Z, 1) == qubitron.X
    assert qubitron.Pauli.by_relative_index(qubitron.Z, 2) == qubitron.Y
    assert qubitron.Pauli.by_relative_index(qubitron.Z, 3) == qubitron.Z


def test_too_many_qubits() -> None:
    a, b = qubitron.LineQubit.range(2)
    with pytest.raises(ValueError, match='single qubit'):
        _ = qubitron.X.on(a, b)

    x = qubitron.X(a)
    with pytest.raises(ValueError, match=r'len\(new_qubits\)'):
        _ = x.with_qubits(a, b)


def test_relative_index_consistency() -> None:
    for pauli_1 in (qubitron.X, qubitron.Y, qubitron.Z):
        for pauli_2 in (qubitron.X, qubitron.Y, qubitron.Z):
            shift = pauli_2.relative_index(pauli_1)
            assert qubitron.Pauli.by_relative_index(pauli_1, shift) == pauli_2


def test_gt() -> None:
    assert not qubitron.X > qubitron.X
    assert not qubitron.X > qubitron.Y
    assert qubitron.X > qubitron.Z
    assert qubitron.Y > qubitron.X
    assert not qubitron.Y > qubitron.Y
    assert not qubitron.Y > qubitron.Z
    assert not qubitron.Z > qubitron.X
    assert qubitron.Z > qubitron.Y
    assert not qubitron.Z > qubitron.Z


def test_gt_other_type() -> None:
    with pytest.raises(TypeError):
        _ = qubitron.X > object()


def test_lt() -> None:
    assert not qubitron.X < qubitron.X
    assert qubitron.X < qubitron.Y
    assert not qubitron.X < qubitron.Z
    assert not qubitron.Y < qubitron.X
    assert not qubitron.Y < qubitron.Y
    assert qubitron.Y < qubitron.Z
    assert qubitron.Z < qubitron.X
    assert not qubitron.Z < qubitron.Y
    assert not qubitron.Z < qubitron.Z


def test_lt_other_type() -> None:
    with pytest.raises(TypeError):
        _ = qubitron.X < object()


def test_str() -> None:
    assert str(qubitron.X) == 'X'
    assert str(qubitron.Y) == 'Y'
    assert str(qubitron.Z) == 'Z'


def test_repr() -> None:
    assert repr(qubitron.X) == 'qubitron.X'
    assert repr(qubitron.Y) == 'qubitron.Y'
    assert repr(qubitron.Z) == 'qubitron.Z'


def test_third() -> None:
    assert qubitron.X.third(qubitron.Y) == qubitron.Z
    assert qubitron.Y.third(qubitron.X) == qubitron.Z
    assert qubitron.Y.third(qubitron.Z) == qubitron.X
    assert qubitron.Z.third(qubitron.Y) == qubitron.X
    assert qubitron.Z.third(qubitron.X) == qubitron.Y
    assert qubitron.X.third(qubitron.Z) == qubitron.Y

    assert qubitron.X.third(qubitron.X) == qubitron.X
    assert qubitron.Y.third(qubitron.Y) == qubitron.Y
    assert qubitron.Z.third(qubitron.Z) == qubitron.Z


def test_commutes() -> None:
    for A, B in itertools.product([qubitron.X, qubitron.Y, qubitron.Z], repeat=2):
        assert qubitron.commutes(A, B) == (A == B)
    with pytest.raises(TypeError):
        assert qubitron.commutes(qubitron.X, 'X')
    assert qubitron.commutes(qubitron.X, 'X', default='default') == 'default'
    assert qubitron.commutes(qubitron.Z, qubitron.read_json(json_text=qubitron.to_json(qubitron.Z)))


def test_unitary() -> None:
    np.testing.assert_equal(qubitron.unitary(qubitron.X), qubitron.unitary(qubitron.X))
    np.testing.assert_equal(qubitron.unitary(qubitron.Y), qubitron.unitary(qubitron.Y))
    np.testing.assert_equal(qubitron.unitary(qubitron.Z), qubitron.unitary(qubitron.Z))


def test_apply_unitary() -> None:
    qubitron.testing.assert_has_consistent_apply_unitary(qubitron.X)
    qubitron.testing.assert_has_consistent_apply_unitary(qubitron.Y)
    qubitron.testing.assert_has_consistent_apply_unitary(qubitron.Z)


def test_identity_multiplication() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    assert qubitron.X(a) * qubitron.I(a) == qubitron.X(a)
    assert qubitron.X(a) * qubitron.I(b) == qubitron.X(a)
    assert qubitron.X(a) * qubitron.Y(b) * qubitron.I(c) == qubitron.X(a) * qubitron.Y(b)
    assert qubitron.I(c) * qubitron.X(a) * qubitron.Y(b) == qubitron.X(a) * qubitron.Y(b)
    with pytest.raises(TypeError):
        _ = qubitron.H(c) * qubitron.X(a) * qubitron.Y(b)
    with pytest.raises(TypeError):
        _ = qubitron.X(a) * qubitron.Y(b) * qubitron.H(c)
    with pytest.raises(TypeError):
        _ = qubitron.I(a) * str(qubitron.Y(b))


def test_powers() -> None:
    assert isinstance(qubitron.X, qubitron.Pauli)
    assert isinstance(qubitron.Y, qubitron.Pauli)
    assert isinstance(qubitron.Z, qubitron.Pauli)
    assert not isinstance(qubitron.X**-0.5, qubitron.Pauli)
    assert not isinstance(qubitron.Y**0.2, qubitron.Pauli)
    assert not isinstance(qubitron.Z**0.5, qubitron.Pauli)
    assert isinstance(qubitron.X**-0.5, qubitron.XPowGate)
    assert isinstance(qubitron.Y**0.2, qubitron.YPowGate)
    assert isinstance(qubitron.Z**0.5, qubitron.ZPowGate)

    assert isinstance(qubitron.X**1, qubitron.Pauli)
    assert isinstance(qubitron.Y**1, qubitron.Pauli)
    assert isinstance(qubitron.Z**1, qubitron.Pauli)
