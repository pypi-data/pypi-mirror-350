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
from typing import Any
from unittest import mock

import numpy as np
import pytest
import sympy

import qubitron


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_identity_init(num_qubits):
    assert qubitron.IdentityGate(num_qubits).num_qubits() == num_qubits
    assert qubitron.qid_shape(qubitron.IdentityGate(num_qubits)) == (2,) * num_qubits
    assert qubitron.qid_shape(qubitron.IdentityGate(3, (1, 2, 3))) == (1, 2, 3)
    assert qubitron.qid_shape(qubitron.IdentityGate(qid_shape=(1, 2, 3))) == (1, 2, 3)
    with pytest.raises(ValueError, match='len.* !='):
        qubitron.IdentityGate(5, qid_shape=(1, 2))
    with pytest.raises(ValueError, match='Specify either'):
        qubitron.IdentityGate()


def test_identity_on_each():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    assert qubitron.I.on_each(q0, q1, q2) == [qubitron.I(q0), qubitron.I(q1), qubitron.I(q2)]
    assert qubitron.I.on_each([q0, [q1], q2]) == [qubitron.I(q0), qubitron.I(q1), qubitron.I(q2)]
    assert qubitron.I.on_each(iter([q0, [q1], q2])) == [qubitron.I(q0), qubitron.I(q1), qubitron.I(q2)]
    with pytest.raises(ValueError, match='str'):
        qubitron.I.on_each('abc')


def test_identity_on_each_iter_second():
    class Q(qubitron.Qid):
        @property
        def dimension(self) -> int:
            return 2

        def _comparison_key(self) -> Any:
            return 1

        def __iter__(self):
            # Having this method makes `isinstance(x, Iterable)` return True.
            raise NotImplementedError()

    q = Q()
    assert qubitron.I.on_each(q) == [qubitron.I(q)]


def test_identity_on_each_only_single_qubit():
    q0, q1 = qubitron.LineQubit.range(2)
    q0_3, q1_3 = q0.with_dimension(3), q1.with_dimension(3)
    assert qubitron.I.on_each(q0, q1) == [qubitron.I.on(q0), qubitron.I.on(q1)]
    assert qubitron.IdentityGate(1, (3,)).on_each(q0_3, q1_3) == [
        qubitron.IdentityGate(1, (3,)).on(q0_3),
        qubitron.IdentityGate(1, (3,)).on(q1_3),
    ]


def test_identity_on_each_two_qubits():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    q0_3, q1_3 = q0.with_dimension(3), q1.with_dimension(3)
    assert qubitron.IdentityGate(2).on_each([(q0, q1)]) == [qubitron.IdentityGate(2)(q0, q1)]
    assert qubitron.IdentityGate(2).on_each([(q0, q1), (q2, q3)]) == [
        qubitron.IdentityGate(2)(q0, q1),
        qubitron.IdentityGate(2)(q2, q3),
    ]
    assert qubitron.IdentityGate(2, (3, 3)).on_each([(q0_3, q1_3)]) == [
        qubitron.IdentityGate(2, (3, 3))(q0_3, q1_3)
    ]
    assert qubitron.IdentityGate(2).on_each((q0, q1)) == [qubitron.IdentityGate(2)(q0, q1)]
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        qubitron.IdentityGate(2).on_each(q0, q1)
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        qubitron.IdentityGate(2).on_each([[(q0, q1)]])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        qubitron.IdentityGate(2).on_each([(q0,)])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        qubitron.IdentityGate(2).on_each([(q0, q1, q2)])


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_identity_unitary(num_qubits):
    i = qubitron.IdentityGate(num_qubits)
    assert np.allclose(qubitron.unitary(i), np.identity(2**num_qubits))
    i3 = qubitron.IdentityGate(num_qubits, (3,) * num_qubits)
    assert np.allclose(qubitron.unitary(i3), np.identity(3**num_qubits))


def test_identity_str():
    assert str(qubitron.IdentityGate(1)) == 'I'
    assert str(qubitron.IdentityGate(2)) == 'I(2)'
    # Qid shape is not included in str
    assert str(qubitron.IdentityGate(1, (3,))) == 'I'
    assert str(qubitron.IdentityGate(2, (1, 2))) == 'I(2)'


def test_identity_repr():
    assert repr(qubitron.I) == 'qubitron.I'
    assert repr(qubitron.IdentityGate(5)) == 'qubitron.IdentityGate(5)'
    assert repr(qubitron.IdentityGate(qid_shape=(2, 3))) == 'qubitron.IdentityGate(qid_shape=(2, 3))'


def test_identity_apply_unitary():
    v = np.array([1, 0])
    result = qubitron.apply_unitary(qubitron.I, qubitron.ApplyUnitaryArgs(v, np.array([0, 1]), (0,)))
    assert result is v

    v = np.array([1, 0, 0])
    result = qubitron.apply_unitary(
        qubitron.IdentityGate(1, (3,)), qubitron.ApplyUnitaryArgs(v, np.array([0, 1, 2]), (0,))
    )
    assert result is v


def test_identity_eq():
    equals_tester = qubitron.testing.EqualsTester()
    equals_tester.make_equality_group(
        lambda: qubitron.I, lambda: qubitron.IdentityGate(1), lambda: qubitron.IdentityGate(1, (2,))
    )
    equals_tester.add_equality_group(qubitron.IdentityGate(2), qubitron.IdentityGate(2, (2, 2)))
    equals_tester.add_equality_group(qubitron.IdentityGate(4))
    equals_tester.add_equality_group(qubitron.IdentityGate(1, (3,)))
    equals_tester.add_equality_group(qubitron.IdentityGate(4, (1, 2, 3, 4)))


def test_identity_trace_distance_bound():
    assert qubitron.I._trace_distance_bound_() == 0
    assert qubitron.IdentityGate(num_qubits=2)._trace_distance_bound_() == 0


def test_identity_pow():
    I = qubitron.I
    q = qubitron.NamedQubit('q')

    assert I(q) ** 0.5 == I(q)
    assert I(q) ** 2 == I(q)
    assert I(q) ** (1 + 1j) == I(q)
    assert I(q) ** sympy.Symbol('x') == I(q)
    with pytest.raises(TypeError):
        _ = (I**q)(q)
    with pytest.raises(TypeError):
        _ = I(q) ** q


def test_pauli_expansion_notimplemented():
    assert qubitron.IdentityGate(1, (3,))._pauli_expansion_() == NotImplemented


@pytest.mark.parametrize(
    'gate_type, num_qubits', itertools.product((qubitron.IdentityGate,), range(1, 5))
)
def test_consistent_protocols(gate_type, num_qubits):
    gate = gate_type(num_qubits=num_qubits)
    qubitron.testing.assert_implements_consistent_protocols(gate, qubit_count=num_qubits)


def test_identity_global():
    qubits = qubitron.LineQubit.range(3)
    assert qubitron.identity_each(*qubits) == qubitron.IdentityGate(3).on(*qubits)
    qids = qubitron.LineQid.for_qid_shape((1, 2, 3))
    assert qubitron.identity_each(*qids) == qubitron.IdentityGate(3, (1, 2, 3)).on(*qids)
    with pytest.raises(ValueError, match='Not a qubitron.Qid'):
        qubitron.identity_each(qubits)  # The user forgot to expand the list for example.


def test_identity_mul():
    class UnknownGate(qubitron.testing.SingleQubitGate):
        pass

    class UnknownOperation(qubitron.Operation):
        @property
        def qubits(self):
            raise NotImplementedError()

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    q = qubitron.LineQubit(0)
    g = UnknownGate().on(q)
    i = qubitron.I(q)
    p = UnknownOperation()
    assert g * i is g is i * g
    assert p * i is p is i * p
    assert i * i is i

    with pytest.raises(TypeError):
        _ = "test" * i

    assert i * 2 == qubitron.PauliString(coefficient=2)
    assert 1j * i == qubitron.PauliString(coefficient=1j)


def test_identity_short_circuits_act_on():
    args = mock.Mock(qubitron.SimulationState)
    args._act_on_fallback_.side_effect = mock.Mock(side_effect=Exception('No!'))
    qubitron.act_on(qubitron.IdentityGate(1)(qubitron.LineQubit(0)), args)


def test_identity_commutes():
    assert qubitron.commutes(qubitron.I, qubitron.X)
    with pytest.raises(TypeError):
        qubitron.commutes(qubitron.I, "Gate")


def test_identity_diagram():
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.IdentityGate(3).on_each(qubitron.LineQubit.range(3))),
        """
0: ───I───
      │
1: ───I───
      │
2: ───I───
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.IdentityGate(0)()),
        """
    I(0)""",
    )
