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
import os
import time
from collections import defaultdict
from random import randint, random, randrange, sample
from typing import Iterator

import numpy as np
import pytest
import sympy

import qubitron
from qubitron import circuits, ops
from qubitron.testing.devices import ValidatingTestDevice


class _Foxy(ValidatingTestDevice):
    pass


FOXY = _Foxy(
    allowed_qubit_types=(qubitron.GridQubit,),
    allowed_gates=(ops.CZPowGate, ops.XPowGate, ops.YPowGate, ops.ZPowGate),
    qubits=set(qubitron.GridQubit.rect(2, 7)),
    name=f'{__name__}.FOXY',
    auto_decompose_gates=(ops.CCXPowGate,),
    validate_locality=True,
)


BCONE = ValidatingTestDevice(
    allowed_qubit_types=(qubitron.GridQubit,),
    allowed_gates=(ops.XPowGate,),
    qubits={qubitron.GridQubit(0, 6)},
    name=f'{__name__}.BCONE',
)


q0, q1, q2, q3 = qubitron.LineQubit.range(4)


def test_from_moments():
    a, b, c, d = qubitron.LineQubit.range(4)
    moment = qubitron.Moment(qubitron.Z(a), qubitron.Z(b))
    subcircuit = qubitron.FrozenCircuit.from_moments(qubitron.X(c), qubitron.Y(d))
    circuit = qubitron.Circuit.from_moments(
        moment,
        subcircuit,
        [qubitron.X(a), qubitron.Y(b)],
        [qubitron.X(c)],
        [],
        qubitron.Z(d),
        None,
        [qubitron.measure(a, b, key='ab'), qubitron.measure(c, d, key='cd')],
    )
    assert circuit == qubitron.Circuit(
        qubitron.Moment(qubitron.Z(a), qubitron.Z(b)),
        qubitron.Moment(
            qubitron.CircuitOperation(
                qubitron.FrozenCircuit(qubitron.Moment(qubitron.X(c)), qubitron.Moment(qubitron.Y(d)))
            )
        ),
        qubitron.Moment(qubitron.X(a), qubitron.Y(b)),
        qubitron.Moment(qubitron.X(c)),
        qubitron.Moment(),
        qubitron.Moment(qubitron.Z(d)),
        qubitron.Moment(qubitron.measure(a, b, key='ab'), qubitron.measure(c, d, key='cd')),
    )
    assert circuit[0] is moment
    assert circuit[1].operations[0].circuit is subcircuit


def test_alignment():
    assert repr(qubitron.Alignment.LEFT) == 'qubitron.Alignment.LEFT'
    assert repr(qubitron.Alignment.RIGHT) == 'qubitron.Alignment.RIGHT'


def test_setitem():
    circuit = qubitron.Circuit([qubitron.Moment(), qubitron.Moment()])

    circuit[1] = qubitron.Moment([qubitron.X(qubitron.LineQubit(0))])
    assert circuit == qubitron.Circuit([qubitron.Moment(), qubitron.Moment([qubitron.X(qubitron.LineQubit(0))])])

    circuit[1:1] = (
        qubitron.Moment([qubitron.Y(qubitron.LineQubit(0))]),
        qubitron.Moment([qubitron.Z(qubitron.LineQubit(0))]),
    )
    assert circuit == qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.Y(qubitron.LineQubit(0))]),
            qubitron.Moment([qubitron.Z(qubitron.LineQubit(0))]),
            qubitron.Moment([qubitron.X(qubitron.LineQubit(0))]),
        ]
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_equality(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    eq = qubitron.testing.EqualsTester()

    # Default is empty. Iterables get listed.
    eq.add_equality_group(circuit_cls(), circuit_cls([]), circuit_cls(()))
    eq.add_equality_group(circuit_cls([qubitron.Moment()]), circuit_cls((qubitron.Moment(),)))

    # Equality depends on structure and contents.
    eq.add_equality_group(circuit_cls([qubitron.Moment([qubitron.X(a)])]))
    eq.add_equality_group(circuit_cls([qubitron.Moment([qubitron.X(b)])]))
    eq.add_equality_group(circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)])]))
    eq.add_equality_group(circuit_cls([qubitron.Moment([qubitron.X(a), qubitron.X(b)])]))

    # Big case.
    eq.add_equality_group(
        circuit_cls(
            [
                qubitron.Moment([qubitron.H(a), qubitron.H(b)]),
                qubitron.Moment([qubitron.CZ(a, b)]),
                qubitron.Moment([qubitron.H(b)]),
            ]
        )
    )
    eq.add_equality_group(circuit_cls([qubitron.Moment([qubitron.H(a)]), qubitron.Moment([qubitron.CNOT(a, b)])]))


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_approx_eq(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert not qubitron.approx_eq(circuit_cls([qubitron.Moment([qubitron.X(a)])]), qubitron.Moment([qubitron.X(a)]))

    assert qubitron.approx_eq(
        circuit_cls([qubitron.Moment([qubitron.X(a)])]), circuit_cls([qubitron.Moment([qubitron.X(a)])])
    )
    assert not qubitron.approx_eq(
        circuit_cls([qubitron.Moment([qubitron.X(a)])]), circuit_cls([qubitron.Moment([qubitron.X(b)])])
    )

    assert qubitron.approx_eq(
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=0)(a)])]),
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=1e-9)(a)])]),
    )

    assert not qubitron.approx_eq(
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=0)(a)])]),
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=1e-7)(a)])]),
    )
    assert qubitron.approx_eq(
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=0)(a)])]),
        circuit_cls([qubitron.Moment([qubitron.XPowGate(exponent=1e-7)(a)])]),
        atol=1e-6,
    )


def test_append_single():
    a = qubitron.NamedQubit('a')

    c = qubitron.Circuit()
    c.append(())
    assert c == qubitron.Circuit()

    c = qubitron.Circuit()
    c.append(qubitron.X(a))
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a)])])

    c = qubitron.Circuit()
    c.append([qubitron.X(a)])
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a)])])

    c = qubitron.Circuit(qubitron.H(a))
    c.append(c)
    assert c == qubitron.Circuit(
        [qubitron.Moment(qubitron.H(qubitron.NamedQubit('a'))), qubitron.Moment(qubitron.H(qubitron.NamedQubit('a')))]
    )


def test_append_control_key():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    c = qubitron.Circuit()
    c.append(qubitron.measure(q0, key='a'))
    c.append(qubitron.X(q1).with_classical_controls('a'))
    assert len(c) == 2

    c = qubitron.Circuit()
    c.append(qubitron.measure(q0, key='a'))
    c.append(qubitron.X(q1).with_classical_controls('b'))
    c.append(qubitron.X(q2).with_classical_controls('b'))
    assert len(c) == 1


def test_append_multiple():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = qubitron.Circuit()
    c.append([qubitron.X(a), qubitron.X(b)], qubitron.InsertStrategy.NEW)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)])])

    c = qubitron.Circuit()
    c.append([qubitron.X(a), qubitron.X(b)], qubitron.InsertStrategy.EARLIEST)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.X(b)])])

    c = qubitron.Circuit()
    c.append(qubitron.X(a), qubitron.InsertStrategy.EARLIEST)
    c.append(qubitron.X(b), qubitron.InsertStrategy.EARLIEST)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.X(b)])])


def test_append_control_key_subcircuit():
    q0, q1 = qubitron.LineQubit.range(2)

    c = qubitron.Circuit()
    c.append(qubitron.measure(q0, key='a'))
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'a'))
        )
    )
    assert len(c) == 2

    c = qubitron.Circuit()
    c.append(qubitron.measure(q0, key='a'))
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'b'))
        )
    )
    assert len(c) == 1

    c = qubitron.Circuit()
    c.append(qubitron.measure(q0, key='a'))
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 2

    c = qubitron.Circuit()
    c.append(qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.measure(q0, key='a'))))
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 2

    c = qubitron.Circuit()
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.measure(q0, key='a'))
        ).with_measurement_key_mapping({'a': 'c'})
    )
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'c'})
    )
    assert len(c) == 2

    c = qubitron.Circuit()
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.measure(q0, key='a'))
        ).with_measurement_key_mapping({'a': 'b'})
    )
    c.append(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.ClassicallyControlledOperation(qubitron.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 1


def test_measurement_key_paths():
    a = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.measure(a, key='A'))
    assert qubitron.measurement_key_names(circuit1) == {'A'}
    circuit2 = qubitron.with_key_path(circuit1, ('B',))
    assert qubitron.measurement_key_names(circuit2) == {'B:A'}
    circuit3 = qubitron.with_key_path_prefix(circuit2, ('C',))
    assert qubitron.measurement_key_names(circuit3) == {'C:B:A'}


def test_append_moments():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = qubitron.Circuit()
    c.append(qubitron.Moment([qubitron.X(a), qubitron.X(b)]), qubitron.InsertStrategy.NEW)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.X(b)])])

    c = qubitron.Circuit()
    c.append(
        [qubitron.Moment([qubitron.X(a), qubitron.X(b)]), qubitron.Moment([qubitron.X(a), qubitron.X(b)])],
        qubitron.InsertStrategy.NEW,
    )
    assert c == qubitron.Circuit(
        [qubitron.Moment([qubitron.X(a), qubitron.X(b)]), qubitron.Moment([qubitron.X(a), qubitron.X(b)])]
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_add_op_tree(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls()
    assert c + [qubitron.X(a), qubitron.Y(b)] == circuit_cls([qubitron.Moment([qubitron.X(a), qubitron.Y(b)])])

    assert c + qubitron.X(a) == circuit_cls(qubitron.X(a))
    assert c + [qubitron.X(a)] == circuit_cls(qubitron.X(a))
    assert c + [[[qubitron.X(a)], []]] == circuit_cls(qubitron.X(a))
    assert c + (qubitron.X(a),) == circuit_cls(qubitron.X(a))
    assert c + (qubitron.X(a) for _ in range(1)) == circuit_cls(qubitron.X(a))
    with pytest.raises(TypeError):
        _ = c + qubitron.X


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_radd_op_tree(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls()
    assert [qubitron.X(a), qubitron.Y(b)] + c == circuit_cls([qubitron.Moment([qubitron.X(a), qubitron.Y(b)])])

    assert qubitron.X(a) + c == circuit_cls(qubitron.X(a))
    assert [qubitron.X(a)] + c == circuit_cls(qubitron.X(a))
    assert [[[qubitron.X(a)], []]] + c == circuit_cls(qubitron.X(a))
    assert (qubitron.X(a),) + c == circuit_cls(qubitron.X(a))
    assert (qubitron.X(a) for _ in range(1)) + c == circuit_cls(qubitron.X(a))
    with pytest.raises(AttributeError):
        _ = qubitron.X + c
    with pytest.raises(TypeError):
        _ = 0 + c

    # non-empty circuit addition
    if circuit_cls == qubitron.FrozenCircuit:
        d = qubitron.FrozenCircuit(qubitron.Y(b))
    else:
        d = qubitron.Circuit()
        d.append(qubitron.Y(b))
    assert [qubitron.X(a)] + d == circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.Y(b)])])
    assert qubitron.Moment([qubitron.X(a)]) + d == circuit_cls(
        [qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.Y(b)])]
    )


def test_add_iadd_equivalence():
    q0, q1 = qubitron.LineQubit.range(2)
    iadd_circuit = qubitron.Circuit(qubitron.X(q0))
    iadd_circuit += qubitron.H(q1)

    add_circuit = qubitron.Circuit(qubitron.X(q0)) + qubitron.H(q1)
    assert iadd_circuit == add_circuit


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_bool(circuit_cls):
    assert not circuit_cls()
    assert circuit_cls(qubitron.X(qubitron.NamedQubit('a')))


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_repr(circuit_cls):
    assert repr(circuit_cls()) == f'qubitron.{circuit_cls.__name__}()'

    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls(
        [qubitron.Moment([qubitron.H(a), qubitron.H(b)]), qubitron.Moment(), qubitron.Moment([qubitron.CZ(a, b)])]
    )
    qubitron.testing.assert_equivalent_repr(c)
    assert (
        repr(c)
        == f"""qubitron.{circuit_cls.__name__}([
    qubitron.Moment(
        qubitron.H(qubitron.NamedQubit('a')),
        qubitron.H(qubitron.NamedQubit('b')),
    ),
    qubitron.Moment(),
    qubitron.Moment(
        qubitron.CZ(qubitron.NamedQubit('a'), qubitron.NamedQubit('b')),
    ),
])"""
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_empty_moments(circuit_cls):
    # 1-qubit test
    op = qubitron.X(qubitron.NamedQubit('a'))
    op_moment = qubitron.Moment([op])
    circuit = circuit_cls([op_moment, op_moment, qubitron.Moment(), op_moment])

    qubitron.testing.assert_has_diagram(circuit, "a: ───X───X───────X───", use_unicode_characters=True)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a
│
X
│
X
│
│
│
X
│
""",
        use_unicode_characters=True,
        transpose=True,
    )

    # 1-qubit ascii-only test
    qubitron.testing.assert_has_diagram(circuit, "a: ---X---X-------X---", use_unicode_characters=False)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a
|
X
|
X
|
|
|
X
|
""",
        use_unicode_characters=False,
        transpose=True,
    )

    # 2-qubit test
    op = qubitron.CNOT(qubitron.NamedQubit('a'), qubitron.NamedQubit('b'))
    op_moment = qubitron.Moment([op])
    circuit = circuit_cls([op_moment, op_moment, qubitron.Moment(), op_moment])

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───────@───
      │   │       │
b: ───X───X───────X───""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a b
│ │
@─X
│ │
@─X
│ │
│ │
│ │
@─X
│ │
""",
        use_unicode_characters=True,
        transpose=True,
    )

    # 2-qubit ascii-only test
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ---@---@-------@---
      |   |       |
b: ---X---X-------X---""",
        use_unicode_characters=False,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a b
| |
@-X
| |
@-X
| |
| |
| |
@-X
| |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_symbol_addition_in_gate_exponent(circuit_cls):
    # 1-qubit test
    qubit = qubitron.NamedQubit('a')
    circuit = circuit_cls(
        qubitron.X(qubit) ** 0.5,
        qubitron.YPowGate(exponent=sympy.Symbol('a') + sympy.Symbol('b')).on(qubit),
    )
    qubitron.testing.assert_has_diagram(
        circuit, 'a: ───X^0.5───Y^(a + b)───', use_unicode_characters=True
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a
│
X^0.5
│
Y^(a + b)
│
""",
        use_unicode_characters=True,
        transpose=True,
    )

    qubitron.testing.assert_has_diagram(
        circuit, 'a: ---X^0.5---Y^(a + b)---', use_unicode_characters=False
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a
|
X^0.5
|
Y^(a + b)
|

 """,
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_slice(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls(
        [
            qubitron.Moment([qubitron.H(a), qubitron.H(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.H(b)]),
        ]
    )
    assert c[0:1] == circuit_cls([qubitron.Moment([qubitron.H(a), qubitron.H(b)])])
    assert c[::2] == circuit_cls([qubitron.Moment([qubitron.H(a), qubitron.H(b)]), qubitron.Moment([qubitron.H(b)])])
    assert c[0:1:2] == circuit_cls([qubitron.Moment([qubitron.H(a), qubitron.H(b)])])
    assert c[1:3:] == circuit_cls([qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment([qubitron.H(b)])])
    assert c[::-1] == circuit_cls(
        [
            qubitron.Moment([qubitron.H(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.H(a), qubitron.H(b)]),
        ]
    )
    assert c[3:0:-1] == circuit_cls([qubitron.Moment([qubitron.H(b)]), qubitron.Moment([qubitron.CZ(a, b)])])
    assert c[0:2:-1] == circuit_cls()


def test_concatenate():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = qubitron.Circuit()
    d = qubitron.Circuit([qubitron.Moment([qubitron.X(b)])])
    e = qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.X(b)])])

    assert c + d == qubitron.Circuit([qubitron.Moment([qubitron.X(b)])])
    assert d + c == qubitron.Circuit([qubitron.Moment([qubitron.X(b)])])
    assert e + d == qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.X(b)]), qubitron.Moment([qubitron.X(b)])])

    d += c
    assert d == qubitron.Circuit([qubitron.Moment([qubitron.X(b)])])

    c += d
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(b)])])

    f = e + d
    f += e
    assert f == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    with pytest.raises(TypeError):
        _ = c + 'a'


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_multiply(circuit_cls):
    a = qubitron.NamedQubit('a')

    c = circuit_cls()
    d = circuit_cls([qubitron.Moment([qubitron.X(a)])])

    assert c * 0 == circuit_cls()
    assert d * 0 == circuit_cls()
    assert d * 2 == circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])])

    twice_copied_circuit = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])])
    for num in [np.int64(2), np.ushort(2), np.int8(2), np.int32(2), np.short(2)]:
        assert num * d == twice_copied_circuit
        assert d * num == twice_copied_circuit

    assert np.array([2])[0] * d == circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])])
    assert 1 * c == circuit_cls()
    assert -1 * d == circuit_cls()
    assert 1 * d == circuit_cls([qubitron.Moment([qubitron.X(a)])])

    d *= 3
    assert d == circuit_cls(
        [qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])]
    )

    with pytest.raises(TypeError):
        _ = c * 'a'
    with pytest.raises(TypeError):
        _ = 'a' * c
    with pytest.raises(TypeError):
        c *= 'a'


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_container_methods(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls(
        [
            qubitron.Moment([qubitron.H(a), qubitron.H(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.H(b)]),
        ]
    )
    assert list(c) == list(c._moments)
    # __iter__
    assert list(iter(c)) == list(c._moments)
    # __reversed__ for free.
    assert list(reversed(c)) == list(reversed(c._moments))
    # __contains__ for free.
    assert qubitron.Moment([qubitron.H(b)]) in c

    assert len(c) == 3


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_bad_index(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls([qubitron.Moment([qubitron.H(a), qubitron.H(b)])])
    with pytest.raises(TypeError):
        _ = c['string']


def test_append_strategies():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    stream = [qubitron.X(a), qubitron.CZ(a, b), qubitron.X(b), qubitron.X(b), qubitron.X(a)]

    c = qubitron.Circuit()
    c.append(stream, qubitron.InsertStrategy.NEW)
    assert c == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment([qubitron.X(a)]),
        ]
    )

    c = qubitron.Circuit()
    c.append(stream, qubitron.InsertStrategy.INLINE)
    assert c == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment([qubitron.X(b), qubitron.X(a)]),
        ]
    )

    c = qubitron.Circuit()
    c.append(stream, qubitron.InsertStrategy.EARLIEST)
    assert c == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(b), qubitron.X(a)]),
            qubitron.Moment([qubitron.X(b)]),
        ]
    )


def test_insert_op_tree_new():
    a = qubitron.NamedQubit('alice')
    b = qubitron.NamedQubit('bob')
    c = qubitron.Circuit()

    op_tree_list = [
        (-10, 0, qubitron.CZ(a, b), a),
        (-20, 0, qubitron.X(a), a),
        (20, 2, qubitron.X(b), b),
        (2, 2, qubitron.H(b), b),
        (-3, 1, qubitron.H(a), a),
    ]

    for given_index, actual_index, operation, qubit in op_tree_list:
        c.insert(given_index, operation, qubitron.InsertStrategy.NEW)
        assert c.operation_at(qubit, actual_index) == operation

    c.insert(1, (), qubitron.InsertStrategy.NEW)
    assert c == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.H(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.H(b)]),
            qubitron.Moment([qubitron.X(b)]),
        ]
    )

    BAD_INSERT = qubitron.InsertStrategy('BAD', 'Bad strategy for testing.')
    with pytest.raises(ValueError):
        c.insert(1, qubitron.X(a), BAD_INSERT)


def test_insert_op_tree_newinline():
    a = qubitron.NamedQubit('alice')
    b = qubitron.NamedQubit('bob')
    c = qubitron.Circuit()

    op_tree_list = [
        (-5, 0, [qubitron.H(a), qubitron.X(b)], [a, b]),
        (-15, 0, [qubitron.CZ(a, b)], [a]),
        (15, 2, [qubitron.H(b), qubitron.X(a)], [b, a]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, qubitron.InsertStrategy.NEW_THEN_INLINE)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index) == op_list[i]

    c2 = qubitron.Circuit()
    c2.insert(
        0,
        [qubitron.CZ(a, b), qubitron.H(a), qubitron.X(b), qubitron.H(b), qubitron.X(a)],
        qubitron.InsertStrategy.NEW_THEN_INLINE,
    )
    assert c == c2


def test_insert_op_tree_inline():
    a = qubitron.NamedQubit('alice')
    b = qubitron.NamedQubit('bob')
    c = qubitron.Circuit([qubitron.Moment([qubitron.H(a)])])

    op_tree_list = [
        (1, 1, [qubitron.H(a), qubitron.X(b)], [a, b]),
        (0, 0, [qubitron.X(b)], [b]),
        (4, 3, [qubitron.H(b)], [b]),
        (5, 3, [qubitron.H(a)], [a]),
        (-2, 0, [qubitron.X(b)], [b]),
        (-5, 0, [qubitron.CZ(a, b)], [a]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, qubitron.InsertStrategy.INLINE)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index) == op_list[i]


def test_insert_op_tree_earliest():
    a = qubitron.NamedQubit('alice')
    b = qubitron.NamedQubit('bob')
    c = qubitron.Circuit([qubitron.Moment([qubitron.H(a)])])

    op_tree_list = [
        (5, [1, 0], [qubitron.X(a), qubitron.X(b)], [a, b]),
        (1, [1], [qubitron.H(b)], [b]),
        (-4, [0], [qubitron.X(b)], [b]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, qubitron.InsertStrategy.EARLIEST)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index[i]) == op_list[i]


def test_insert_moment():
    a = qubitron.NamedQubit('alice')
    b = qubitron.NamedQubit('bob')
    c = qubitron.Circuit()

    moment_list = [
        (-10, 0, [qubitron.CZ(a, b)], a, qubitron.InsertStrategy.NEW_THEN_INLINE),
        (-20, 0, [qubitron.X(a)], a, qubitron.InsertStrategy.NEW),
        (20, 2, [qubitron.X(b)], b, qubitron.InsertStrategy.INLINE),
        (2, 2, [qubitron.H(b)], b, qubitron.InsertStrategy.EARLIEST),
        (-3, 1, [qubitron.H(a)], a, qubitron.InsertStrategy.EARLIEST),
    ]

    for given_index, actual_index, operation, qubit, strat in moment_list:
        c.insert(given_index, qubitron.Moment(operation), strat)
        assert c.operation_at(qubit, actual_index) == operation[0]


def test_circuit_length_inference():
    # tests that `get_earliest_accommodating_moment_index` properly computes circuit length
    circuit = qubitron.Circuit(qubitron.X(qubitron.q(0)))
    qubit_indices = {qubitron.q(0): 0}
    mkey_indices = {}
    ckey_indices = {}
    assert circuits.circuit.get_earliest_accommodating_moment_index(
        qubitron.Moment(), qubit_indices, mkey_indices, ckey_indices
    ) == len(circuit)


def test_insert_inline_near_start():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = qubitron.Circuit([qubitron.Moment(), qubitron.Moment()])

    c.insert(1, qubitron.X(a), strategy=qubitron.InsertStrategy.INLINE)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a)]), qubitron.Moment()])

    c.insert(1, qubitron.Y(a), strategy=qubitron.InsertStrategy.INLINE)
    assert c == qubitron.Circuit([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.Y(a)]), qubitron.Moment()])

    c.insert(0, qubitron.Z(b), strategy=qubitron.InsertStrategy.INLINE)
    assert c == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Y(a)]),
            qubitron.Moment(),
        ]
    )


def test_insert_at_frontier_init():
    x = qubitron.NamedQubit('x')
    op = qubitron.X(x)
    circuit = qubitron.Circuit(op)
    actual_frontier = circuit.insert_at_frontier(op, 3)
    expected_circuit = qubitron.Circuit(
        [qubitron.Moment([op]), qubitron.Moment(), qubitron.Moment(), qubitron.Moment([op])]
    )
    assert circuit == expected_circuit
    expected_frontier = defaultdict(lambda: 0)
    expected_frontier[x] = 4
    assert actual_frontier == expected_frontier

    with pytest.raises(ValueError):
        circuit = qubitron.Circuit([qubitron.Moment(), qubitron.Moment([op])])
        frontier = {x: 2}
        circuit.insert_at_frontier(op, 0, frontier)


def test_insert_at_frontier():
    class Replacer(qubitron.PointOptimizer):
        def __init__(self, replacer=(lambda x: x)):
            super().__init__()
            self.replacer = replacer

        def optimization_at(
            self, circuit: qubitron.Circuit, index: int, op: qubitron.Operation
        ) -> qubitron.PointOptimizationSummary | None:
            new_ops = self.replacer(op)
            return qubitron.PointOptimizationSummary(
                clear_span=1, clear_qubits=op.qubits, new_operations=new_ops
            )

    replacer = lambda op: ((qubitron.Z(op.qubits[0]),) * 2 + (op, qubitron.Y(op.qubits[0])))
    prepend_two_Xs_append_one_Y = Replacer(replacer)
    qubits = [qubitron.NamedQubit(s) for s in 'abcdef']
    a, b, c = qubits[:3]

    circuit = qubitron.Circuit(
        [qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment([qubitron.CZ(b, c)]), qubitron.Moment([qubitron.CZ(a, b)])]
    )

    prepend_two_Xs_append_one_Y.optimize_circuit(circuit)

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───Z───Z───@───Y───────────────Z───Z───@───Y───
              │                           │
b: ───────────@───Z───Z───@───Y───────────@───────
                          │
c: ───────────────────────@───────────────────────
""",
    )

    prepender = lambda op: (qubitron.X(op.qubits[0]),) * 3 + (op,)
    prepend_3_Xs = Replacer(prepender)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.CNOT(a, b)]),
            qubitron.Moment([qubitron.CNOT(b, c)]),
            qubitron.Moment([qubitron.CNOT(c, b)]),
        ]
    )
    prepend_3_Xs.optimize_circuit(circuit)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───X───X───X───@───────────────────────────────────
                  │
b: ───────────────X───X───X───X───@───────────────X───
                                  │               │
c: ───────────────────────────────X───X───X───X───@───
""",
    )

    duplicate = Replacer(lambda op: (op,) * 2)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.CZ(qubits[j], qubits[j + 1]) for j in range(i % 2, 5, 2)])
            for i in range(4)
        ]
    )

    duplicate.optimize_circuit(circuit)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───────────@───@───────────
      │   │           │   │
b: ───@───@───@───@───@───@───@───@───
              │   │           │   │
c: ───@───@───@───@───@───@───@───@───
      │   │           │   │
d: ───@───@───@───@───@───@───@───@───
              │   │           │   │
e: ───@───@───@───@───@───@───@───@───
      │   │           │   │
f: ───@───@───────────@───@───────────
""",
    )

    circuit = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.CZ(*qubits[2:4]), qubitron.CNOT(*qubits[:2])]),
            qubitron.Moment([qubitron.CNOT(*qubits[1::-1])]),
        ]
    )

    duplicate.optimize_circuit(circuit)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───X───X───
      │   │   │   │
b: ───X───X───@───@───

c: ───@───────@───────
      │       │
d: ───@───────@───────
""",
    )


def test_insert_into_range():
    x = qubitron.NamedQubit('x')
    y = qubitron.NamedQubit('y')
    c = qubitron.Circuit([qubitron.Moment([qubitron.X(x)])] * 4)
    c.insert_into_range([qubitron.Z(x), qubitron.CZ(x, y)], 2, 2)
    qubitron.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───
                  │
y: ───────────────@───────────
""",
    )

    c.insert_into_range([qubitron.Y(y), qubitron.Y(y), qubitron.Y(y), qubitron.CX(y, x)], 1, 4)
    qubitron.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───
                  │       │
y: ───────Y───Y───@───Y───@───────
""",
    )

    c.insert_into_range([qubitron.H(y), qubitron.H(y)], 6, 7)
    qubitron.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───────
                  │       │
y: ───────Y───Y───@───Y───@───H───H───
""",
    )

    c.insert_into_range([qubitron.T(y)], 0, 1)
    qubitron.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───────
                  │       │
y: ───T───Y───Y───@───Y───@───H───H───
""",
    )

    with pytest.raises(IndexError):
        c.insert_into_range([qubitron.CZ(x, y)], 10, 10)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_next_moment_operating_on(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls()
    assert c.next_moment_operating_on([a]) is None
    assert c.next_moment_operating_on([a], 0) is None
    assert c.next_moment_operating_on([a], 102) is None

    c = circuit_cls([qubitron.Moment([qubitron.X(a)])])
    assert c.next_moment_operating_on([a]) == 0
    assert c.next_moment_operating_on([a], 0) == 0
    assert c.next_moment_operating_on([a, b]) == 0
    assert c.next_moment_operating_on([a], 1) is None
    assert c.next_moment_operating_on([b]) is None

    c = circuit_cls(
        [qubitron.Moment(), qubitron.Moment([qubitron.X(a)]), qubitron.Moment(), qubitron.Moment([qubitron.CZ(a, b)])]
    )

    assert c.next_moment_operating_on([a], 0) == 1
    assert c.next_moment_operating_on([a], 1) == 1
    assert c.next_moment_operating_on([a], 2) == 3
    assert c.next_moment_operating_on([a], 3) == 3
    assert c.next_moment_operating_on([a], 4) is None

    assert c.next_moment_operating_on([b], 0) == 3
    assert c.next_moment_operating_on([b], 1) == 3
    assert c.next_moment_operating_on([b], 2) == 3
    assert c.next_moment_operating_on([b], 3) == 3
    assert c.next_moment_operating_on([b], 4) is None

    assert c.next_moment_operating_on([a, b], 0) == 1
    assert c.next_moment_operating_on([a, b], 1) == 1
    assert c.next_moment_operating_on([a, b], 2) == 3
    assert c.next_moment_operating_on([a, b], 3) == 3
    assert c.next_moment_operating_on([a, b], 4) is None


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_next_moment_operating_on_distance(circuit_cls):
    a = qubitron.NamedQubit('a')

    c = circuit_cls(
        [
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment(),
        ]
    )

    assert c.next_moment_operating_on([a], 0, max_distance=4) is None
    assert c.next_moment_operating_on([a], 1, max_distance=3) is None
    assert c.next_moment_operating_on([a], 2, max_distance=2) is None
    assert c.next_moment_operating_on([a], 3, max_distance=1) is None
    assert c.next_moment_operating_on([a], 4, max_distance=0) is None

    assert c.next_moment_operating_on([a], 0, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 1, max_distance=4) == 4
    assert c.next_moment_operating_on([a], 2, max_distance=3) == 4
    assert c.next_moment_operating_on([a], 3, max_distance=2) == 4
    assert c.next_moment_operating_on([a], 4, max_distance=1) == 4

    assert c.next_moment_operating_on([a], 5, max_distance=0) is None
    assert c.next_moment_operating_on([a], 1, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 3, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 1, max_distance=500) == 4

    # Huge max distances should be handled quickly due to capping.
    assert c.next_moment_operating_on([a], 5, max_distance=10**100) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        c.next_moment_operating_on([a], 0, max_distance=-1)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_prev_moment_operating_on(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls()
    assert c.prev_moment_operating_on([a]) is None
    assert c.prev_moment_operating_on([a], 0) is None
    assert c.prev_moment_operating_on([a], 102) is None

    c = circuit_cls([qubitron.Moment([qubitron.X(a)])])
    assert c.prev_moment_operating_on([a]) == 0
    assert c.prev_moment_operating_on([a], 1) == 0
    assert c.prev_moment_operating_on([a, b]) == 0
    assert c.prev_moment_operating_on([a], 0) is None
    assert c.prev_moment_operating_on([b]) is None

    c = circuit_cls(
        [qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment(), qubitron.Moment([qubitron.X(a)]), qubitron.Moment()]
    )

    assert c.prev_moment_operating_on([a], 4) == 2
    assert c.prev_moment_operating_on([a], 3) == 2
    assert c.prev_moment_operating_on([a], 2) == 0
    assert c.prev_moment_operating_on([a], 1) == 0
    assert c.prev_moment_operating_on([a], 0) is None

    assert c.prev_moment_operating_on([b], 4) == 0
    assert c.prev_moment_operating_on([b], 3) == 0
    assert c.prev_moment_operating_on([b], 2) == 0
    assert c.prev_moment_operating_on([b], 1) == 0
    assert c.prev_moment_operating_on([b], 0) is None

    assert c.prev_moment_operating_on([a, b], 4) == 2
    assert c.prev_moment_operating_on([a, b], 3) == 2
    assert c.prev_moment_operating_on([a, b], 2) == 0
    assert c.prev_moment_operating_on([a, b], 1) == 0
    assert c.prev_moment_operating_on([a, b], 0) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        assert c.prev_moment_operating_on([a, b], 4, max_distance=-1)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_prev_moment_operating_on_distance(circuit_cls):
    a = qubitron.NamedQubit('a')

    c = circuit_cls(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
        ]
    )

    assert c.prev_moment_operating_on([a], max_distance=4) is None
    assert c.prev_moment_operating_on([a], 6, max_distance=4) is None
    assert c.prev_moment_operating_on([a], 5, max_distance=3) is None
    assert c.prev_moment_operating_on([a], 4, max_distance=2) is None
    assert c.prev_moment_operating_on([a], 3, max_distance=1) is None
    assert c.prev_moment_operating_on([a], 2, max_distance=0) is None
    assert c.prev_moment_operating_on([a], 1, max_distance=0) is None
    assert c.prev_moment_operating_on([a], 0, max_distance=0) is None

    assert c.prev_moment_operating_on([a], 6, max_distance=5) == 1
    assert c.prev_moment_operating_on([a], 5, max_distance=4) == 1
    assert c.prev_moment_operating_on([a], 4, max_distance=3) == 1
    assert c.prev_moment_operating_on([a], 3, max_distance=2) == 1
    assert c.prev_moment_operating_on([a], 2, max_distance=1) == 1

    assert c.prev_moment_operating_on([a], 6, max_distance=10) == 1
    assert c.prev_moment_operating_on([a], 6, max_distance=100) == 1
    assert c.prev_moment_operating_on([a], 13, max_distance=500) == 1

    # Huge max distances should be handled quickly due to capping.
    assert c.prev_moment_operating_on([a], 1, max_distance=10**100) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        c.prev_moment_operating_on([a], 6, max_distance=-1)


def test_earliest_available_moment():
    q = qubitron.LineQubit.range(3)
    c = qubitron.Circuit(
        qubitron.Moment(qubitron.measure(q[0], key="m")),
        qubitron.Moment(qubitron.X(q[1]).with_classical_controls("m")),
    )
    assert c.earliest_available_moment(qubitron.Y(q[0])) == 1
    assert c.earliest_available_moment(qubitron.Y(q[1])) == 2
    assert c.earliest_available_moment(qubitron.Y(q[2])) == 0
    assert c.earliest_available_moment(qubitron.Y(q[2]).with_classical_controls("m")) == 1
    assert (
        c.earliest_available_moment(qubitron.Y(q[2]).with_classical_controls("m"), end_moment_index=1)
        == 1
    )

    # Returns `end_moment_index` by default without verifying if an operation already exists there.
    assert (
        c.earliest_available_moment(qubitron.Y(q[1]).with_classical_controls("m"), end_moment_index=1)
        == 1
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_operation_at(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls()
    assert c.operation_at(a, 0) is None
    assert c.operation_at(a, -1) is None
    assert c.operation_at(a, 102) is None

    c = circuit_cls([qubitron.Moment()])
    assert c.operation_at(a, 0) is None

    c = circuit_cls([qubitron.Moment([qubitron.X(a)])])
    assert c.operation_at(b, 0) is None
    assert c.operation_at(a, 1) is None
    assert c.operation_at(a, 0) == qubitron.X(a)

    c = circuit_cls([qubitron.Moment(), qubitron.Moment([qubitron.CZ(a, b)])])
    assert c.operation_at(a, 0) is None
    assert c.operation_at(a, 1) == qubitron.CZ(a, b)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_findall_operations(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    xa = qubitron.X.on(a)
    xb = qubitron.X.on(b)
    za = qubitron.Z.on(a)
    zb = qubitron.Z.on(b)

    def is_x(op: qubitron.Operation) -> bool:
        return isinstance(op, qubitron.GateOperation) and isinstance(op.gate, qubitron.XPowGate)

    c = circuit_cls()
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls(xa)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls(za)
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls([za, zb] * 8)
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls(xa, xb)
    assert list(c.findall_operations(is_x)) == [(0, xa), (0, xb)]

    c = circuit_cls(xa, zb)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls(xa, za)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls([xa] * 8)
    assert list(c.findall_operations(is_x)) == list(enumerate([xa] * 8))

    c = circuit_cls(za, zb, xa, xb)
    assert list(c.findall_operations(is_x)) == [(1, xa), (1, xb)]

    c = circuit_cls(xa, zb, za, xb)
    assert list(c.findall_operations(is_x)) == [(0, xa), (1, xb)]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_findall_operations_with_gate(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(a), qubitron.Z(b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.measure(a), qubitron.measure(b)]),
        ]
    )
    assert list(c.findall_operations_with_gate_type(qubitron.XPowGate)) == [
        (0, qubitron.X(a), qubitron.X),
        (2, qubitron.X(a), qubitron.X),
        (2, qubitron.X(b), qubitron.X),
    ]
    assert list(c.findall_operations_with_gate_type(qubitron.CZPowGate)) == [
        (3, qubitron.CZ(a, b), qubitron.CZ)
    ]
    assert list(c.findall_operations_with_gate_type(qubitron.MeasurementGate)) == [
        (4, qubitron.MeasurementGate(1, key='a').on(a), qubitron.MeasurementGate(1, key='a')),
        (4, qubitron.MeasurementGate(1, key='b').on(b), qubitron.MeasurementGate(1, key='b')),
    ]


def assert_findall_operations_until_blocked_as_expected(
    circuit=None, start_frontier=None, is_blocker=None, expected_ops=None
):
    if circuit is None:
        circuit = qubitron.Circuit()
    if start_frontier is None:
        start_frontier = {}
    kwargs = {} if is_blocker is None else {'is_blocker': is_blocker}
    found_ops = circuit.findall_operations_until_blocked(start_frontier, **kwargs)

    for i, op in found_ops:
        assert i >= min((start_frontier[q] for q in op.qubits if q in start_frontier), default=0)
        assert set(op.qubits).intersection(start_frontier)

    if expected_ops is None:
        return
    assert sorted(found_ops) == sorted(expected_ops)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_findall_operations_until_blocked(circuit_cls):
    a, b, c, d = qubitron.LineQubit.range(4)

    assert_findall_operations_until_blocked_as_expected()

    circuit = circuit_cls(
        qubitron.H(a),
        qubitron.CZ(a, b),
        qubitron.H(b),
        qubitron.CZ(b, c),
        qubitron.H(c),
        qubitron.CZ(c, d),
        qubitron.H(d),
        qubitron.CZ(c, d),
        qubitron.H(c),
        qubitron.CZ(b, c),
        qubitron.H(b),
        qubitron.CZ(a, b),
        qubitron.H(a),
    )
    expected_diagram = """
0: ───H───@───────────────────────────────────────@───H───
          │                                       │
1: ───────@───H───@───────────────────────@───H───@───────
                  │                       │
2: ───────────────@───H───@───────@───H───@───────────────
                          │       │
3: ───────────────────────@───H───@───────────────────────
""".strip()
    #     0   1   2   3   4   5   6   7   8   9   10  11  12
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)

    # Always return true to test basic features
    go_to_end = lambda op: False
    stop_if_op = lambda op: True
    stop_if_h_on_a = lambda op: op.gate == qubitron.H and a in op.qubits

    # Empty cases.
    assert_findall_operations_until_blocked_as_expected(is_blocker=go_to_end, expected_ops=[])
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, is_blocker=go_to_end, expected_ops=[]
    )

    # Clamped input cases. (out of bounds)
    assert_findall_operations_until_blocked_as_expected(
        start_frontier={a: 5}, is_blocker=stop_if_op, expected_ops=[]
    )
    assert_findall_operations_until_blocked_as_expected(
        start_frontier={a: -100}, is_blocker=stop_if_op, expected_ops=[]
    )
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier={a: 100}, is_blocker=stop_if_op, expected_ops=[]
    )

    # Test if all operations are blocked
    for idx in range(15):
        for q in (a, b, c, d):
            assert_findall_operations_until_blocked_as_expected(
                circuit=circuit, start_frontier={q: idx}, is_blocker=stop_if_op, expected_ops=[]
            )
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx, b: idx, c: idx, d: idx},
            is_blocker=stop_if_op,
            expected_ops=[],
        )

    # Cases where nothing is blocked, it goes to the end
    a_ending_ops = [(11, qubitron.CZ.on(a, b)), (12, qubitron.H.on(a))]
    for idx in range(2, 10):
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx},
            is_blocker=go_to_end,
            expected_ops=a_ending_ops,
        )

    # Block on H, but pick up the CZ
    for idx in range(2, 10):
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx},
            is_blocker=stop_if_h_on_a,
            expected_ops=[(11, qubitron.CZ.on(a, b))],
        )

    circuit = circuit_cls([qubitron.CZ(a, b), qubitron.CZ(a, b), qubitron.CZ(b, c)])
    expected_diagram = """
0: ───@───@───────
      │   │
1: ───@───@───@───
              │
2: ───────────@───
""".strip()
    #     0   1   2
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0}
    is_blocker = lambda next_op: sorted(next_op.qubits) != [a, b]
    expected_ops = [(0, qubitron.CZ(a, b)), (1, qubitron.CZ(a, b))]
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit,
        start_frontier=start_frontier,
        is_blocker=is_blocker,
        expected_ops=expected_ops,
    )

    circuit = circuit_cls([qubitron.ZZ(a, b), qubitron.ZZ(b, c)])
    expected_diagram = """
0: ───ZZ────────
      │
1: ───ZZ───ZZ───
           │
2: ────────ZZ───
""".strip()
    #     0    1
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0, c: 0}
    is_blocker = lambda op: a in op.qubits
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier=start_frontier, is_blocker=is_blocker, expected_ops=[]
    )

    circuit = circuit_cls([qubitron.ZZ(a, b), qubitron.XX(c, d), qubitron.ZZ(b, c), qubitron.Z(b)])
    expected_diagram = """
0: ───ZZ────────────
      │
1: ───ZZ───ZZ───Z───
           │
2: ───XX───ZZ───────
      │
3: ───XX────────────
""".strip()
    #     0    1    2
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0, c: 0, d: 0}
    is_blocker = lambda op: isinstance(op.gate, qubitron.XXPowGate)
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit,
        start_frontier=start_frontier,
        is_blocker=is_blocker,
        expected_ops=[(0, qubitron.ZZ(a, b))],
    )

    circuit = circuit_cls([qubitron.XX(a, b), qubitron.Z(a), qubitron.ZZ(b, c), qubitron.ZZ(c, d), qubitron.Z(d)])
    expected_diagram = """
0: ───XX───Z─────────────
      │
1: ───XX───ZZ────────────
           │
2: ────────ZZ───ZZ───────
                │
3: ─────────────ZZ───Z───
""".strip()
    #     0    1    2    3
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, d: 0}
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier=start_frontier, is_blocker=is_blocker, expected_ops=[]
    )


@pytest.mark.parametrize('seed', [randint(0, 2**31)])
@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_findall_operations_until_blocked_docstring_examples(seed, circuit_cls):
    prng = np.random.RandomState(seed)

    class ExampleGate(qubitron.Gate):
        def __init__(self, n_qubits, label):
            self.n_qubits = n_qubits
            self.label = label

        def num_qubits(self):
            return self.n_qubits

        def _circuit_diagram_info_(self, args):
            return qubitron.CircuitDiagramInfo(wire_symbols=[self.label] * self.n_qubits)

    def is_blocker(op):
        if op.gate.label == 'F':
            return False
        if op.gate.label == 'T':
            return True
        return prng.rand() < 0.5

    F2 = ExampleGate(2, 'F')
    T2 = ExampleGate(2, 'T')
    M2 = ExampleGate(2, 'M')
    a, b, c, d = qubitron.LineQubit.range(4)

    circuit = circuit_cls([F2(a, b), F2(a, b), T2(b, c)])
    start = {a: 0, b: 0}
    expected_diagram = """
0: ───F───F───────
      │   │
1: ───F───F───T───
              │
2: ───────────T───
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)
    expected_ops = [(0, F2(a, b)), (1, F2(a, b))]
    new_circuit = circuit_cls([op for _, op in expected_ops])
    expected_diagram = """
0: ───F───F───
      │   │
1: ───F───F───
    """
    qubitron.testing.assert_has_diagram(new_circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == expected_ops

    circuit = circuit_cls([M2(a, b), M2(b, c), F2(a, b), M2(c, d)])
    start = {a: 2, b: 2}
    expected_diagram = """
0: ───M───────F───
      │       │
1: ───M───M───F───
          │
2: ───────M───M───
              │
3: ───────────M───
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)
    expected_ops = [(2, F2(a, b))]
    new_circuit = circuit_cls([op for _, op in expected_ops])
    expected_diagram = """
0: ───F───
      │
1: ───F───
    """
    qubitron.testing.assert_has_diagram(new_circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == expected_ops

    circuit = circuit_cls([M2(a, b), T2(b, c), M2(a, b), M2(c, d)])
    start = {a: 1, b: 1}
    expected_diagram = """
0: ───M───────M───
      │       │
1: ───M───T───M───
          │
2: ───────T───M───
              │
3: ───────────M───
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == []

    ops = [(0, F2(a, b)), (1, F2(a, b))]
    circuit = circuit_cls([op for _, op in ops])
    start = {a: 0, b: 1}
    expected_diagram = """
0: ───F───F───
      │   │
1: ───F───F───
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == ops

    ops = [F2(a, b), F2(b, c), F2(c, d)]
    circuit = circuit_cls(ops)
    start = {a: 0, d: 0}
    expected_diagram = """
0: ───F───────────
      │
1: ───F───F───────
          │
2: ───────F───F───
              │
3: ───────────F───
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == [
        (0, F2(a, b)),
        (2, F2(c, d)),
    ]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_has_measurements(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    xa = qubitron.X.on(a)
    xb = qubitron.X.on(b)

    ma = qubitron.measure(a)
    mb = qubitron.measure(b)

    c = circuit_cls()
    assert not c.has_measurements()

    c = circuit_cls(xa, xb)
    assert not c.has_measurements()

    c = circuit_cls(ma)
    assert c.has_measurements()

    c = circuit_cls(ma, mb)
    assert c.has_measurements()

    c = circuit_cls(xa, ma)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xb, mb)
    assert c.has_measurements()

    c = circuit_cls(ma, xa)
    assert c.has_measurements()

    c = circuit_cls(ma, xa, mb)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xb, xa)
    assert c.has_measurements()

    c = circuit_cls(ma, ma)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xa)
    assert c.has_measurements()


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_are_all_or_any_measurements_terminal(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    xa = qubitron.X.on(a)
    xb = qubitron.X.on(b)

    ma = qubitron.measure(a)
    mb = qubitron.measure(b)

    c = circuit_cls()
    assert c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(xa, xb)
    assert c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(ma, mb)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xb, mb)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(ma, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma, xa, mb)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xb, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma, ma)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_all_or_any_terminal(circuit_cls):
    def is_x_pow_gate(op):
        return isinstance(op.gate, qubitron.XPowGate)

    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    xa = qubitron.X.on(a)
    xb = qubitron.X.on(b)

    ya = qubitron.Y.on(a)
    yb = qubitron.Y.on(b)

    c = circuit_cls()
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb, xa)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb, xa, xb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, xa)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, ya)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xb, ya, yb)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, ya, xa)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    def is_circuit_op(op):
        isinstance(op, qubitron.CircuitOperation)

    cop_1 = qubitron.CircuitOperation(qubitron.FrozenCircuit(xa, ya))
    cop_2 = qubitron.CircuitOperation(qubitron.FrozenCircuit(cop_1, xb))
    c = circuit_cls(cop_2, yb)
    # are_all_matches_terminal treats CircuitOperations as transparent.
    assert c.are_all_matches_terminal(is_circuit_op)
    assert not c.are_any_matches_terminal(is_circuit_op)


def test_clear_operations_touching():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = qubitron.Circuit()
    c.clear_operations_touching([a, b], range(10))
    assert c == qubitron.Circuit()

    c = qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment(),
        ]
    )
    c.clear_operations_touching([a], [1, 3, 4, 6, 7])
    assert c == qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment(),
        ]
    )

    c = qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(b)]),
            qubitron.Moment(),
        ]
    )
    c.clear_operations_touching([a, b], [1, 3, 4, 6, 7])
    assert c == qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
            qubitron.Moment(),
        ]
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_all_qubits(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)])])
    assert c.all_qubits() == {a, b}

    c = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])])
    assert c.all_qubits() == {a}

    c = circuit_cls([qubitron.Moment([qubitron.CZ(a, b)])])
    assert c.all_qubits() == {a, b}

    c = circuit_cls([qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment([qubitron.X(a)])])
    assert c.all_qubits() == {a, b}


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_all_operations(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    c = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)])])
    assert list(c.all_operations()) == [qubitron.X(a), qubitron.X(b)]

    c = circuit_cls([qubitron.Moment([qubitron.X(a), qubitron.X(b)])])
    assert list(c.all_operations()) == [qubitron.X(a), qubitron.X(b)]

    c = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)])])
    assert list(c.all_operations()) == [qubitron.X(a), qubitron.X(a)]

    c = circuit_cls([qubitron.Moment([qubitron.CZ(a, b)])])
    assert list(c.all_operations()) == [qubitron.CZ(a, b)]

    c = circuit_cls([qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment([qubitron.X(a)])])
    assert list(c.all_operations()) == [qubitron.CZ(a, b), qubitron.X(a)]

    c = circuit_cls(
        [
            qubitron.Moment([]),
            qubitron.Moment([qubitron.X(a), qubitron.Y(b)]),
            qubitron.Moment([]),
            qubitron.Moment([qubitron.CNOT(a, b)]),
            qubitron.Moment([qubitron.Z(b), qubitron.H(a)]),  # Different qubit order
            qubitron.Moment([]),
        ]
    )

    assert list(c.all_operations()) == [qubitron.X(a), qubitron.Y(b), qubitron.CNOT(a, b), qubitron.Z(b), qubitron.H(a)]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_qid_shape_qubit(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    circuit = circuit_cls([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)])])

    assert qubitron.qid_shape(circuit) == (2, 2)
    assert qubitron.num_qubits(circuit) == 2
    assert circuit.qid_shape() == (2, 2)
    assert circuit.qid_shape(qubit_order=[c, a, b]) == (2, 2, 2)
    with pytest.raises(ValueError, match='extra qubits'):
        _ = circuit.qid_shape(qubit_order=[a])


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_qid_shape_qudit(circuit_cls):
    class PlusOneMod3Gate(qubitron.testing.SingleQubitGate):
        def _qid_shape_(self):
            return (3,)

    class C2NotGate(qubitron.Gate):
        def _qid_shape_(self):
            return (3, 2)

    class IdentityGate(qubitron.testing.SingleQubitGate):
        def _qid_shape_(self):
            return (1,)

    a, b, c = qubitron.LineQid.for_qid_shape((3, 2, 1))

    circuit = circuit_cls(PlusOneMod3Gate().on(a), C2NotGate().on(a, b), IdentityGate().on_each(c))

    assert qubitron.num_qubits(circuit) == 3
    assert qubitron.qid_shape(circuit) == (3, 2, 1)
    assert circuit.qid_shape() == (3, 2, 1)
    assert circuit.qid_shape()
    with pytest.raises(ValueError, match='extra qubits'):
        _ = circuit.qid_shape(qubit_order=[b, c])


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_text_diagram_teleportation_to_diagram(circuit_cls):
    ali = qubitron.NamedQubit('(0, 0)')
    bob = qubitron.NamedQubit('(0, 1)')
    msg = qubitron.NamedQubit('(1, 0)')
    tmp = qubitron.NamedQubit('(1, 1)')

    c = circuit_cls(
        [
            qubitron.Moment([qubitron.H(ali)]),
            qubitron.Moment([qubitron.CNOT(ali, bob)]),
            qubitron.Moment([qubitron.X(msg) ** 0.5]),
            qubitron.Moment([qubitron.CNOT(msg, ali)]),
            qubitron.Moment([qubitron.H(msg)]),
            qubitron.Moment([qubitron.measure(msg), qubitron.measure(ali)]),
            qubitron.Moment([qubitron.CNOT(ali, bob)]),
            qubitron.Moment([qubitron.CNOT(msg, tmp)]),
            qubitron.Moment([qubitron.CZ(bob, tmp)]),
        ]
    )

    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0): ───H───@───────────X───────M───@───────────
               │           │           │
(0, 1): ───────X───────────┼───────────X───────@───
                           │                   │
(1, 0): ───────────X^0.5───@───H───M───────@───┼───
                                           │   │
(1, 1): ───────────────────────────────────X───@───
""",
    )

    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0): ---H---@-----------X-------M---@-----------
               |           |           |
(0, 1): -------X-----------|-----------X-------@---
                           |                   |
(1, 0): -----------X^0.5---@---H---M-------@---|---
                                           |   |
(1, 1): -----------------------------------X---@---
""",
        use_unicode_characters=False,
    )

    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0) (0, 1) (1, 0) (1, 1)
|      |      |      |
H      |      |      |
|      |      |      |
@------X      |      |
|      |      |      |
|      |      X^0.5  |
|      |      |      |
X-------------@      |
|      |      |      |
|      |      H      |
|      |      |      |
M      |      M      |
|      |      |      |
@------X      |      |
|      |      |      |
|      |      @------X
|      |      |      |
|      @-------------@
|      |      |      |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_diagram_with_unknown_exponent(circuit_cls):
    class WeirdGate(qubitron.testing.SingleQubitGate):
        def _circuit_diagram_info_(
            self, args: qubitron.CircuitDiagramInfoArgs
        ) -> qubitron.CircuitDiagramInfo:
            return qubitron.CircuitDiagramInfo(wire_symbols=('B',), exponent='fancy')

    class WeirderGate(qubitron.testing.SingleQubitGate):
        def _circuit_diagram_info_(
            self, args: qubitron.CircuitDiagramInfoArgs
        ) -> qubitron.CircuitDiagramInfo:
            return qubitron.CircuitDiagramInfo(wire_symbols=('W',), exponent='fancy-that')

    c = circuit_cls(WeirdGate().on(qubitron.NamedQubit('q')), WeirderGate().on(qubitron.NamedQubit('q')))

    # The hyphen in the exponent should cause parens to appear.
    qubitron.testing.assert_has_diagram(c, 'q: ───B^fancy───W^(fancy-that)───')


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_circuit_diagram_on_gate_without_info(circuit_cls):
    q = qubitron.NamedQubit('(0, 0)')
    q2 = qubitron.NamedQubit('(0, 1)')
    q3 = qubitron.NamedQubit('(0, 2)')

    class FGate(qubitron.Gate):
        def __init__(self, num_qubits=1):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def __repr__(self):
            return 'python-object-FGate:arbitrary-digits'

    # Fallback to repr.
    f = FGate()
    qubitron.testing.assert_has_diagram(
        circuit_cls([qubitron.Moment([f.on(q)])]),
        """
(0, 0): ---python-object-FGate:arbitrary-digits---
""",
        use_unicode_characters=False,
    )

    f3 = FGate(3)
    # When used on multiple qubits, show the qubit order as a digit suffix.
    qubitron.testing.assert_has_diagram(
        circuit_cls([qubitron.Moment([f3.on(q, q3, q2)])]),
        """
(0, 0): ---python-object-FGate:arbitrary-digits---
           |
(0, 1): ---#3-------------------------------------
           |
(0, 2): ---#2-------------------------------------
""",
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_text_diagram_multi_qubit_gate(circuit_cls):
    q1 = qubitron.NamedQubit('(0, 0)')
    q2 = qubitron.NamedQubit('(0, 1)')
    q3 = qubitron.NamedQubit('(0, 2)')
    c = circuit_cls(qubitron.measure(q1, q2, q3, key='msg'))
    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0): ───M('msg')───
           │
(0, 1): ───M──────────
           │
(0, 2): ───M──────────
""",
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0): ---M('msg')---
           |
(0, 1): ---M----------
           |
(0, 2): ---M----------
""",
        use_unicode_characters=False,
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
(0, 0)   (0, 1) (0, 2)
│        │      │
M('msg')─M──────M
│        │      │
""",
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_text_diagram_many_qubits_gate_but_multiple_wire_symbols(circuit_cls):
    class BadGate(qubitron.testing.ThreeQubitGate):
        def _circuit_diagram_info_(self, args: qubitron.CircuitDiagramInfoArgs) -> tuple[str, str]:
            return 'a', 'a'

    q1 = qubitron.NamedQubit('(0, 0)')
    q2 = qubitron.NamedQubit('(0, 1)')
    q3 = qubitron.NamedQubit('(0, 2)')
    c = circuit_cls([qubitron.Moment([BadGate().on(q1, q2, q3)])])
    with pytest.raises(ValueError, match='BadGate'):
        c.to_text_diagram()


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_text_diagram_parameterized_value(circuit_cls):
    q = qubitron.NamedQubit('cube')

    class PGate(qubitron.testing.SingleQubitGate):
        def __init__(self, val):
            self.val = val

        def _circuit_diagram_info_(
            self, args: qubitron.CircuitDiagramInfoArgs
        ) -> qubitron.CircuitDiagramInfo:
            return qubitron.CircuitDiagramInfo(('P',), self.val)

    c = circuit_cls(
        PGate(1).on(q),
        PGate(2).on(q),
        PGate(sympy.Symbol('a')).on(q),
        PGate(sympy.Symbol('%$&#*(')).on(q),
    )
    assert str(c).strip() == 'cube: ───P───P^2───P^a───P^(%$&#*()───'


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_text_diagram_custom_order(circuit_cls):
    qa = qubitron.NamedQubit('2')
    qb = qubitron.NamedQubit('3')
    qc = qubitron.NamedQubit('4')

    c = circuit_cls([qubitron.Moment([qubitron.X(qa), qubitron.X(qb), qubitron.X(qc)])])
    qubitron.testing.assert_has_diagram(
        c,
        """
3: ---X---

4: ---X---

2: ---X---
""",
        qubit_order=qubitron.QubitOrder.sorted_by(lambda e: int(str(e)) % 3),
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_overly_precise_diagram(circuit_cls):
    # Test default precision of 3
    qa = qubitron.NamedQubit('a')
    c = circuit_cls([qubitron.Moment([qubitron.X(qa) ** 0.12345678])])
    qubitron.testing.assert_has_diagram(
        c,
        """
a: ---X^0.123---
""",
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_none_precision_diagram(circuit_cls):
    # Test default precision of 3
    qa = qubitron.NamedQubit('a')
    c = circuit_cls([qubitron.Moment([qubitron.X(qa) ** 0.4921875])])
    qubitron.testing.assert_has_diagram(
        c,
        """
a: ---X^0.4921875---
""",
        use_unicode_characters=False,
        precision=None,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_diagram_custom_precision(circuit_cls):
    qa = qubitron.NamedQubit('a')
    c = circuit_cls([qubitron.Moment([qubitron.X(qa) ** 0.12341234])])
    qubitron.testing.assert_has_diagram(
        c,
        """
a: ---X^0.12341---
""",
        use_unicode_characters=False,
        precision=5,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_diagram_wgate(circuit_cls):
    qa = qubitron.NamedQubit('a')
    test_wgate = qubitron.PhasedXPowGate(exponent=0.12341234, phase_exponent=0.43214321)
    c = circuit_cls([qubitron.Moment([test_wgate.on(qa)])])
    qubitron.testing.assert_has_diagram(
        c,
        """
a: ---PhX(0.43)^(1/8)---
""",
        use_unicode_characters=False,
        precision=2,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_diagram_wgate_none_precision(circuit_cls):
    qa = qubitron.NamedQubit('a')
    test_wgate = qubitron.PhasedXPowGate(exponent=0.12341234, phase_exponent=0.43214321)
    c = circuit_cls([qubitron.Moment([test_wgate.on(qa)])])
    qubitron.testing.assert_has_diagram(
        c,
        """
a: ---PhX(0.43214321)^0.12341234---
""",
        use_unicode_characters=False,
        precision=None,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_diagram_global_phase(circuit_cls):
    qa = qubitron.NamedQubit('a')
    global_phase = qubitron.global_phase_operation(coefficient=1j)
    c = circuit_cls([global_phase])
    qubitron.testing.assert_has_diagram(
        c, "\n\nglobal phase:   0.5pi", use_unicode_characters=False, precision=2
    )
    qubitron.testing.assert_has_diagram(
        c, "\n\nglobal phase:   0.5π", use_unicode_characters=True, precision=2
    )

    c = circuit_cls([qubitron.X(qa), global_phase, global_phase])
    qubitron.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X───

global phase:   π""",
        use_unicode_characters=True,
        precision=2,
    )
    c = circuit_cls([qubitron.X(qa), global_phase], qubitron.Moment([qubitron.X(qa), global_phase]))
    qubitron.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X──────X──────

global phase:   0.5π   0.5π
""",
        use_unicode_characters=True,
        precision=2,
    )

    c = circuit_cls(
        qubitron.X(qubitron.LineQubit(2)),
        qubitron.CircuitOperation(
            circuit_cls(qubitron.global_phase_operation(-1).with_tags("tag")).freeze()
        ),
    )
    qubitron.testing.assert_has_diagram(
        c,
        """\
2: ───X────────

      π[tag]""",
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_has_unitary(circuit_cls):
    class NonUnitary(qubitron.testing.SingleQubitGate):
        pass

    class EventualUnitary(qubitron.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            return qubitron.X.on_each(*qubits)

    q = qubitron.NamedQubit('q')

    # Non-unitary operations cause a non-unitary circuit.
    assert qubitron.has_unitary(circuit_cls(qubitron.X(q)))
    assert not qubitron.has_unitary(circuit_cls(NonUnitary().on(q)))

    # Terminal measurements are ignored, though.
    assert qubitron.has_unitary(circuit_cls(qubitron.measure(q)))
    assert not qubitron.has_unitary(circuit_cls(qubitron.measure(q), qubitron.measure(q)))

    # Still unitary if operations decompose into unitary operations.
    assert qubitron.has_unitary(circuit_cls(EventualUnitary().on(q)))


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_text_diagram_jupyter(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    circuit = circuit_cls((qubitron.CNOT(a, b), qubitron.CNOT(b, c), qubitron.CNOT(c, a)) * 50)
    text_expected = circuit.to_text_diagram()

    # Test Jupyter console output from
    class FakePrinter:
        def __init__(self):
            self.text_pretty = ''

        def text(self, to_print):
            self.text_pretty += to_print

    p = FakePrinter()
    circuit._repr_pretty_(p, False)
    assert p.text_pretty == text_expected

    # Test cycle handling
    p = FakePrinter()
    circuit._repr_pretty_(p, True)
    assert p.text_pretty == f'{circuit_cls.__name__}(...)'

    # Test Jupyter notebook html output
    text_html = circuit._repr_html_()
    # Don't enforce specific html surrounding the diagram content
    assert text_expected in text_html


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_circuit_to_unitary_matrix(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    # Single qubit gates.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a) ** 0.5).unitary(),
        # fmt: off
        np.array(
            [
                [1j, 1],
                [1, 1j],
            ]
        )
        * np.sqrt(0.5),
        # fmt: on
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.Y(a) ** 0.25).unitary(), qubitron.unitary(qubitron.Y(a) ** 0.25), atol=1e-8
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.Z(a), qubitron.X(b)).unitary(),
        # fmt: off
        np.array(
            [
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, -1],
                [0, 0, -1, 0],
            ]
        ),
        # fmt: on
        atol=1e-8,
    )

    # Single qubit gates and two qubit gate.
    # fmt: off
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.Z(a), qubitron.X(b), qubitron.CNOT(a, b)).unitary(),
        np.array(
            [
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, -1],
            ]
        ),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.H(b), qubitron.CNOT(b, a) ** 0.5, qubitron.Y(a) ** 0.5).unitary(),
        np.array(
            [
                [1, 1, -1, -1],
                [1j, -1j, -1j, 1j],
                [1, 1, 1, 1],
                [1, -1, 1, -1],
            ]
        )
        * np.sqrt(0.25),
        atol=1e-8,
    )
    # fmt: on

    # Measurement gate has no corresponding matrix.
    c = circuit_cls(qubitron.measure(a))
    with pytest.raises(ValueError):
        _ = c.unitary(ignore_terminal_measurements=False)

    # Ignoring terminal measurements.
    c = circuit_cls(qubitron.measure(a))
    qubitron.testing.assert_allclose_up_to_global_phase(c.unitary(), np.eye(2), atol=1e-8)

    # Ignoring terminal measurements with further qubitron.
    c = circuit_cls(qubitron.Z(a), qubitron.measure(a), qubitron.Z(b))
    # fmt: off
    qubitron.testing.assert_allclose_up_to_global_phase(
        c.unitary(), np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]), atol=1e-8
    )
    # fmt: on

    # Optionally don't ignoring terminal measurements.
    c = circuit_cls(qubitron.measure(a))
    with pytest.raises(ValueError, match="measurement"):
        _ = (c.unitary(ignore_terminal_measurements=False),)

    # Non-terminal measurements are not ignored.
    c = circuit_cls(qubitron.measure(a), qubitron.X(a))
    with pytest.raises(ValueError):
        _ = c.unitary()

    # Non-terminal measurements are not ignored (multiple qubits).
    c = circuit_cls(qubitron.measure(a), qubitron.measure(b), qubitron.CNOT(a, b))
    with pytest.raises(ValueError):
        _ = c.unitary()

    # Gates without matrix or decomposition raise exception
    class MysteryGate(qubitron.testing.TwoQubitGate):
        pass

    c = circuit_cls(MysteryGate()(a, b))
    with pytest.raises(TypeError):
        _ = c.unitary()

    # Accounts for measurement bit flipping.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.measure(a, invert_mask=(True,))).unitary(), qubitron.unitary(qubitron.X), atol=1e-8
    )

    # dtype
    c = circuit_cls(qubitron.X(a))
    assert c.unitary(dtype=np.complex64).dtype == np.complex64
    assert c.unitary(dtype=np.complex128).dtype == np.complex128
    assert c.unitary(dtype=np.float64).dtype == np.float64


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_circuit_unitary(circuit_cls):
    q = qubitron.NamedQubit('q')

    with_inner_measure = circuit_cls(qubitron.H(q), qubitron.measure(q), qubitron.H(q))
    assert not qubitron.has_unitary(with_inner_measure)
    assert qubitron.unitary(with_inner_measure, None) is None

    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(circuit_cls(qubitron.X(q) ** 0.5), qubitron.measure(q)),
        np.array([[1j, 1], [1, 1j]]) * np.sqrt(0.5),
        atol=1e-8,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_simple_circuits_to_unitary_matrix(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    # Phase parity.
    c = circuit_cls(qubitron.CNOT(a, b), qubitron.Z(b), qubitron.CNOT(a, b))
    assert qubitron.has_unitary(c)
    m = c.unitary()
    # fmt: off
    qubitron.testing.assert_allclose_up_to_global_phase(
        m,
        np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on

    # 2-qubit matrix matches when qubits in order.
    for expected in [np.diag([1, 1j, -1, -1j]), qubitron.unitary(qubitron.CNOT)]:

        class Passthrough(qubitron.testing.TwoQubitGate):
            def _unitary_(self) -> np.ndarray:
                return expected

        c = circuit_cls(Passthrough()(a, b))
        m = c.unitary()
        qubitron.testing.assert_allclose_up_to_global_phase(m, expected, atol=1e-8)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_composite_gate_to_unitary_matrix(circuit_cls):
    class CnotComposite(qubitron.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            q0, q1 = qubits
            return qubitron.Y(q1) ** -0.5, qubitron.CZ(q0, q1), qubitron.Y(q1) ** 0.5

    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = circuit_cls(
        qubitron.X(a), CnotComposite()(a, b), qubitron.X(a), qubitron.measure(a), qubitron.X(b), qubitron.measure(b)
    )
    assert qubitron.has_unitary(c)

    mat = c.unitary()
    mat_expected = qubitron.unitary(qubitron.CNOT)

    qubitron.testing.assert_allclose_up_to_global_phase(mat, mat_expected, atol=1e-8)


def test_circuit_superoperator_too_many_qubits():
    circuit = qubitron.Circuit(qubitron.IdentityGate(num_qubits=11).on(*qubitron.LineQubit.range(11)))
    assert not circuit._has_superoperator_()
    with pytest.raises(ValueError, match="too many"):
        _ = circuit._superoperator_()


@pytest.mark.parametrize(
    'circuit, expected_superoperator',
    (
        (qubitron.Circuit(qubitron.I(q0)), np.eye(4)),
        (qubitron.Circuit(qubitron.IdentityGate(2).on(q0, q1)), np.eye(16)),
        (
            qubitron.Circuit(qubitron.H(q0)),
            # fmt: off
            np.array(
                [
                    [1, 1, 1, 1],
                    [1, -1, 1, -1],
                    [1, 1, -1, -1],
                    [1, -1, -1, 1]
                ]
            ) / 2,
            # fmt: on
        ),
        (qubitron.Circuit(qubitron.S(q0)), np.diag([1, -1j, 1j, 1])),
        (qubitron.Circuit(qubitron.depolarize(0.75).on(q0)), np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2),
        (
            qubitron.Circuit(qubitron.X(q0), qubitron.depolarize(0.75).on(q0)),
            np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
            qubitron.Circuit(qubitron.Y(q0), qubitron.depolarize(0.75).on(q0)),
            np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
            qubitron.Circuit(qubitron.Z(q0), qubitron.depolarize(0.75).on(q0)),
            np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
            qubitron.Circuit(qubitron.H(q0), qubitron.depolarize(0.75).on(q0)),
            np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (qubitron.Circuit(qubitron.H(q0), qubitron.H(q0)), np.eye(4)),
        (
            qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q1, q0), qubitron.H(q0)),
            np.diag([1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1]),
        ),
    ),
)
def test_circuit_superoperator_fixed_values(circuit, expected_superoperator):
    """Tests Circuit._superoperator_() on a few simple circuits."""
    assert circuit._has_superoperator_()
    assert np.allclose(circuit._superoperator_(), expected_superoperator)


@pytest.mark.parametrize(
    'rs, n_qubits',
    (
        ([0.1, 0.2], 1),
        ([0.1, 0.2], 2),
        ([0.8, 0.9], 1),
        ([0.8, 0.9], 2),
        ([0.1, 0.2, 0.3], 1),
        ([0.1, 0.2, 0.3], 2),
        ([0.1, 0.2, 0.3], 3),
    ),
)
def test_circuit_superoperator_depolarizing_channel_compositions(rs, n_qubits):
    """Tests Circuit._superoperator_() on compositions of depolarizing channels."""

    def pauli_error_probability(r: float, n_qubits: int) -> float:
        """Computes Pauli error probability for given depolarization parameter.

        Pauli error is what qubitron.depolarize takes as argument. Depolarization parameter
        makes it simple to compute the serial composition of depolarizing channels. It
        is multiplicative under channel composition.
        """
        d2 = 4**n_qubits
        return (1 - r) * (d2 - 1) / d2

    def depolarize(r: float, n_qubits: int) -> qubitron.DepolarizingChannel:
        """Returns depolarization channel with given depolarization parameter."""
        return qubitron.depolarize(pauli_error_probability(r, n_qubits=n_qubits), n_qubits=n_qubits)

    qubits = qubitron.LineQubit.range(n_qubits)
    circuit1 = qubitron.Circuit(depolarize(r, n_qubits).on(*qubits) for r in rs)
    circuit2 = qubitron.Circuit(depolarize(np.prod(rs), n_qubits).on(*qubits))

    assert circuit1._has_superoperator_()
    assert circuit2._has_superoperator_()

    cm1 = circuit1._superoperator_()
    cm2 = circuit2._superoperator_()
    assert np.allclose(cm1, cm2)


def density_operator_basis(n_qubits: int) -> Iterator[np.ndarray]:
    """Yields operator basis consisting of density operators."""
    RHO_0 = np.array([[1, 0], [0, 0]], dtype=np.complex64)
    RHO_1 = np.array([[0, 0], [0, 1]], dtype=np.complex64)
    RHO_2 = np.array([[1, 1], [1, 1]], dtype=np.complex64) / 2
    RHO_3 = np.array([[1, -1j], [1j, 1]], dtype=np.complex64) / 2
    RHO_BASIS = (RHO_0, RHO_1, RHO_2, RHO_3)

    if n_qubits < 1:
        yield np.array(1)
        return
    for rho1 in RHO_BASIS:
        for rho2 in density_operator_basis(n_qubits - 1):
            yield np.kron(rho1, rho2)


@pytest.mark.parametrize(
    'circuit, initial_state',
    itertools.chain(
        itertools.product(
            [
                qubitron.Circuit(qubitron.I(q0)),
                qubitron.Circuit(qubitron.X(q0)),
                qubitron.Circuit(qubitron.Y(q0)),
                qubitron.Circuit(qubitron.Z(q0)),
                qubitron.Circuit(qubitron.S(q0)),
                qubitron.Circuit(qubitron.T(q0)),
            ],
            density_operator_basis(n_qubits=1),
        ),
        itertools.product(
            [
                qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1)),
                qubitron.Circuit(qubitron.depolarize(0.2).on(q0), qubitron.CNOT(q0, q1)),
                qubitron.Circuit(
                    qubitron.X(q0),
                    qubitron.amplitude_damp(0.2).on(q0),
                    qubitron.depolarize(0.1).on(q1),
                    qubitron.CNOT(q0, q1),
                ),
            ],
            density_operator_basis(n_qubits=2),
        ),
        itertools.product(
            [
                qubitron.Circuit(
                    qubitron.depolarize(0.1, n_qubits=2).on(q0, q1),
                    qubitron.H(q2),
                    qubitron.CNOT(q1, q2),
                    qubitron.phase_damp(0.1).on(q0),
                ),
                qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.TOFFOLI(q0, q1, q2)),
            ],
            density_operator_basis(n_qubits=3),
        ),
    ),
)
def test_compare_circuits_superoperator_to_simulation(circuit, initial_state):
    """Compares action of circuit superoperator and circuit simulation."""
    assert circuit._has_superoperator_()
    superoperator = circuit._superoperator_()
    vectorized_initial_state = initial_state.reshape(-1)
    vectorized_final_state = superoperator @ vectorized_initial_state
    actual_state = np.reshape(vectorized_final_state, initial_state.shape)

    sim = qubitron.DensityMatrixSimulator()
    expected_state = sim.simulate(circuit, initial_state=initial_state).final_density_matrix

    assert np.allclose(actual_state, expected_state)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_expanding_gate_symbols(circuit_cls):
    class MultiTargetCZ(qubitron.Gate):
        def __init__(self, num_qubits):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def _circuit_diagram_info_(self, args: qubitron.CircuitDiagramInfoArgs) -> tuple[str, ...]:
            assert args.known_qubit_count is not None
            return ('@',) + ('Z',) * (args.known_qubit_count - 1)

    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    t0 = circuit_cls(MultiTargetCZ(1).on(c))
    t1 = circuit_cls(MultiTargetCZ(2).on(c, a))
    t2 = circuit_cls(MultiTargetCZ(3).on(c, a, b))

    qubitron.testing.assert_has_diagram(
        t0,
        """
c: ───@───
""",
    )

    qubitron.testing.assert_has_diagram(
        t1,
        """
a: ───Z───
      │
c: ───@───
""",
    )

    qubitron.testing.assert_has_diagram(
        t2,
        """
a: ───Z───
      │
b: ───Z───
      │
c: ───@───
""",
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_transposed_diagram_exponent_order(circuit_cls):
    a, b, c = qubitron.LineQubit.range(3)
    circuit = circuit_cls(qubitron.CZ(a, b) ** -0.5, qubitron.CZ(a, c) ** 0.5, qubitron.CZ(b, c) ** 0.125)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0 1      2
│ │      │
@─@^-0.5 │
│ │      │
@─┼──────@^0.5
│ │      │
│ @──────@^(1/8)
│ │      │
""",
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_transposed_diagram_can_depend_on_transpose(circuit_cls):
    class TestGate(qubitron.Gate):
        def num_qubits(self):
            return 1

        def _circuit_diagram_info_(self, args):
            return qubitron.CircuitDiagramInfo(wire_symbols=("t" if args.transpose else "r",))

    c = qubitron.Circuit(TestGate()(qubitron.NamedQubit("a")))

    qubitron.testing.assert_has_diagram(c, "a: ───r───")
    qubitron.testing.assert_has_diagram(
        c,
        """
a
│
t
│
""",
        transpose=True,
    )


def test_insert_moments():
    q = qubitron.NamedQubit('q')
    c = qubitron.Circuit()

    m0 = qubitron.Moment([qubitron.X(q)])
    c.append(m0)
    assert list(c) == [m0]
    assert c[0] == m0

    m1 = qubitron.Moment([qubitron.Y(q)])
    c.append(m1)
    assert list(c) == [m0, m1]
    assert c[1] == m1

    m2 = qubitron.Moment([qubitron.Z(q)])
    c.insert(0, m2)
    assert list(c) == [m2, m0, m1]
    assert c[0] == m2

    assert c._moments == [m2, m0, m1]
    assert c._moments[0] == m2


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_final_state_vector(circuit_cls):
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    # State ordering.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a) ** 0.5).final_state_vector(
            ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1j, 1]) * np.sqrt(0.5),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a) ** 0.5).final_state_vector(
            initial_state=0, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1j, 1]) * np.sqrt(0.5),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a) ** 0.5).final_state_vector(
            initial_state=1, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1, 1j]) * np.sqrt(0.5),
        atol=1e-8,
    )

    # Vector state.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a) ** 0.5).final_state_vector(
            initial_state=np.array([1j, 1]) * np.sqrt(0.5),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 1]),
        atol=1e-8,
    )

    # Qubit ordering.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=0, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1, 0, 0, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=1, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=2, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 0, 1]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=3, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Product state
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=qubitron.KET_ZERO(a) * qubitron.KET_ZERO(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([1, 0, 0, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=qubitron.KET_ZERO(a) * qubitron.KET_ONE(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=qubitron.KET_ONE(a) * qubitron.KET_ZERO(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 0, 0, 1]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.CNOT(a, b)).final_state_vector(
            initial_state=qubitron.KET_ONE(a) * qubitron.KET_ONE(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Measurements.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.measure(a)).final_state_vector(
            ignore_terminal_measurements=True, dtype=np.complex64
        ),
        np.array([1, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.X(a), qubitron.measure(a)).final_state_vector(
            ignore_terminal_measurements=True, dtype=np.complex64
        ),
        np.array([0, 1]),
        atol=1e-8,
    )
    with pytest.raises(ValueError):
        qubitron.testing.assert_allclose_up_to_global_phase(
            circuit_cls(qubitron.measure(a), qubitron.X(a)).final_state_vector(
                ignore_terminal_measurements=True, dtype=np.complex64
            ),
            np.array([1, 0]),
            atol=1e-8,
        )
    with pytest.raises(ValueError):
        qubitron.testing.assert_allclose_up_to_global_phase(
            circuit_cls(qubitron.measure(a)).final_state_vector(
                ignore_terminal_measurements=False, dtype=np.complex64
            ),
            np.array([1, 0]),
            atol=1e-8,
        )

    # Qubit order.
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.Z(a), qubitron.X(b)).final_state_vector(
            qubit_order=[a, b], ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        circuit_cls(qubitron.Z(a), qubitron.X(b)).final_state_vector(
            qubit_order=[b, a], ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Dtypes.
    dtypes = [np.complex64, np.complex128]
    if hasattr(np, 'complex256'):  # Some systems don't support 128 bit floats.
        dtypes.append(np.complex256)
    for dt in dtypes:
        qubitron.testing.assert_allclose_up_to_global_phase(
            circuit_cls(qubitron.X(a) ** 0.5).final_state_vector(
                initial_state=np.array([1j, 1]) * np.sqrt(0.5),
                ignore_terminal_measurements=False,
                dtype=dt,
            ),
            np.array([0, 1]),
            atol=1e-8,
        )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_is_parameterized(circuit_cls, resolve_fn):
    a, b = qubitron.LineQubit.range(2)
    circuit = circuit_cls(
        qubitron.CZ(a, b) ** sympy.Symbol('u'),
        qubitron.X(a) ** sympy.Symbol('v'),
        qubitron.Y(b) ** sympy.Symbol('w'),
    )
    assert qubitron.is_parameterized(circuit)

    circuit = resolve_fn(circuit, qubitron.ParamResolver({'u': 0.1, 'v': 0.3}))
    assert qubitron.is_parameterized(circuit)

    circuit = resolve_fn(circuit, qubitron.ParamResolver({'w': 0.2}))
    assert not qubitron.is_parameterized(circuit)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve_parameters(circuit_cls, resolve_fn):
    a, b = qubitron.LineQubit.range(2)
    circuit = circuit_cls(
        qubitron.CZ(a, b) ** sympy.Symbol('u'),
        qubitron.X(a) ** sympy.Symbol('v'),
        qubitron.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    qubitron.testing.assert_has_diagram(
        resolved_circuit,
        """
0: ───@───────X^0.3───
      │
1: ───@^0.1───Y^0.2───
""",
    )
    q = qubitron.NamedQubit('q')
    # no-op parameter resolution
    circuit = circuit_cls([qubitron.Moment(), qubitron.Moment([qubitron.X(q)])])
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({}))
    qubitron.testing.assert_same_circuits(circuit, resolved_circuit)
    # actually resolve something
    circuit = circuit_cls([qubitron.Moment(), qubitron.Moment([qubitron.X(q) ** sympy.Symbol('x')])])
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({'x': 0.2}))
    expected_circuit = circuit_cls([qubitron.Moment(), qubitron.Moment([qubitron.X(q) ** 0.2])])
    qubitron.testing.assert_same_circuits(expected_circuit, resolved_circuit)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve_parameters_no_change(circuit_cls, resolve_fn):
    a, b = qubitron.LineQubit.range(2)
    circuit = circuit_cls(qubitron.CZ(a, b), qubitron.X(a), qubitron.Y(b))
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    assert resolved_circuit is circuit

    circuit = circuit_cls(
        qubitron.CZ(a, b) ** sympy.Symbol('u'),
        qubitron.X(a) ** sympy.Symbol('v'),
        qubitron.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({}))
    assert resolved_circuit is circuit


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameter_names(circuit_cls, resolve_fn):
    a, b = qubitron.LineQubit.range(2)
    circuit = circuit_cls(
        qubitron.CZ(a, b) ** sympy.Symbol('u'),
        qubitron.X(a) ** sympy.Symbol('v'),
        qubitron.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, qubitron.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    assert qubitron.parameter_names(circuit) == {'u', 'v', 'w'}
    assert qubitron.parameter_names(resolved_circuit) == set()


def test_items():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.Circuit()
    m1 = qubitron.Moment([qubitron.X(a), qubitron.X(b)])
    m2 = qubitron.Moment([qubitron.X(a)])
    m3 = qubitron.Moment([])
    m4 = qubitron.Moment([qubitron.CZ(a, b)])

    c[:] = [m1, m2]
    qubitron.testing.assert_same_circuits(c, qubitron.Circuit([m1, m2]))

    assert c[0] == m1
    del c[0]
    qubitron.testing.assert_same_circuits(c, qubitron.Circuit([m2]))

    c.append(m1)
    c.append(m3)
    qubitron.testing.assert_same_circuits(c, qubitron.Circuit([m2, m1, m3]))

    assert c[0:2] == qubitron.Circuit([m2, m1])
    c[0:2] = [m4]
    qubitron.testing.assert_same_circuits(c, qubitron.Circuit([m4, m3]))

    c[:] = [m1]
    qubitron.testing.assert_same_circuits(c, qubitron.Circuit([m1]))

    with pytest.raises(TypeError):
        c[:] = [m1, 1]
    with pytest.raises(TypeError):
        c[0] = 1


def test_copy():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.Circuit(qubitron.X(a), qubitron.CZ(a, b), qubitron.Z(a), qubitron.Z(b))
    assert c == c.copy() == c.__copy__()
    c2 = c.copy()
    assert c2 == c
    c2[:] = []
    assert c2 != c


def test_batch_remove():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    original = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_remove([])
    assert after == original

    # Delete one.
    after = original.copy()
    after.batch_remove([(0, qubitron.X(a))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_remove([(500, qubitron.X(a))])
    assert after == original

    # Delete several.
    after = original.copy()
    after.batch_remove([(0, qubitron.X(a)), (2, qubitron.CZ(a, b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment(),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Delete all.
    after = original.copy()
    after.batch_remove(
        [(0, qubitron.X(a)), (1, qubitron.Z(b)), (2, qubitron.CZ(a, b)), (3, qubitron.X(a)), (3, qubitron.X(b))]
    )
    assert after == qubitron.Circuit([qubitron.Moment(), qubitron.Moment(), qubitron.Moment(), qubitron.Moment()])

    # Delete moment partially.
    after = original.copy()
    after.batch_remove([(3, qubitron.X(a))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(b)]),
        ]
    )

    # Deleting something that's not there.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_remove([(0, qubitron.X(b))])
    assert after == original

    # Duplicate delete.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_remove([(0, qubitron.X(a)), (0, qubitron.X(a))])
    assert after == original


def test_batch_replace():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    original = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_replace([])
    assert after == original

    # Replace one.
    after = original.copy()
    after.batch_replace([(0, qubitron.X(a), qubitron.Y(a))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.Y(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_replace([(500, qubitron.X(a), qubitron.Y(a))])
    assert after == original

    # Gate does not exist.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_replace([(0, qubitron.Z(a), qubitron.Y(a))])
    assert after == original

    # Replace several.
    after = original.copy()
    after.batch_replace([(0, qubitron.X(a), qubitron.Y(a)), (2, qubitron.CZ(a, b), qubitron.CNOT(a, b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.Y(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CNOT(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )


def test_batch_insert_into():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    original = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_insert_into([])
    assert after == original

    # Add into non-empty moment.
    after = original.copy()
    after.batch_insert_into([(0, qubitron.X(b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Add multiple operations into non-empty moment.
    after = original.copy()
    after.batch_insert_into([(0, [qubitron.X(b), qubitron.X(c)])])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a), qubitron.X(b), qubitron.X(c)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Add into empty moment.
    after = original.copy()
    after.batch_insert_into([(1, qubitron.Z(b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Add multiple operations into empty moment.
    after = original.copy()
    after.batch_insert_into([(1, [qubitron.Z(a), qubitron.Z(b)])])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.Z(a), qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Add into two moments.
    after = original.copy()
    after.batch_insert_into([(1, qubitron.Z(b)), (0, qubitron.X(b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
            qubitron.Moment([qubitron.Z(b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_insert_into([(500, qubitron.X(a))])
    assert after == original

    # Collision.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(0, qubitron.X(a))])
    assert after == original

    # Collision with multiple operations.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(0, [qubitron.X(b), qubitron.X(c), qubitron.X(a)])])
    assert after == original

    # Duplicate insertion collision.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(1, qubitron.X(a)), (1, qubitron.CZ(a, b))])
    assert after == original


def test_batch_insert():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    original = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_insert([])
    assert after == original

    # Pushing.
    after = original.copy()
    after.batch_insert([(0, qubitron.CZ(a, b)), (0, qubitron.CNOT(a, b)), (1, qubitron.Z(b))])
    assert after == qubitron.Circuit(
        [
            qubitron.Moment([qubitron.CNOT(a, b)]),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.Z(b)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.CZ(a, b)]),
            qubitron.Moment([qubitron.X(a), qubitron.X(b)]),
        ]
    )


def test_batch_insert_multiple_same_index():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit()
    c.batch_insert([(0, qubitron.Z(a)), (0, qubitron.Z(b)), (0, qubitron.Z(a))])
    qubitron.testing.assert_same_circuits(
        c, qubitron.Circuit([qubitron.Moment([qubitron.Z(a), qubitron.Z(b)]), qubitron.Moment([qubitron.Z(a)])])
    )


def test_batch_insert_reverses_order_for_same_index_inserts():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit()
    c.batch_insert([(0, qubitron.Z(a)), (0, qubitron.CZ(a, b)), (0, qubitron.Z(b))])
    assert c == qubitron.Circuit(qubitron.Z(b), qubitron.CZ(a, b), qubitron.Z(a))


def test_batch_insert_maintains_order_despite_multiple_previous_inserts():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.H(a))
    c.batch_insert([(0, qubitron.Z(a)), (0, qubitron.Z(a)), (0, qubitron.Z(a)), (1, qubitron.CZ(a, b))])
    assert c == qubitron.Circuit([qubitron.Z(a)] * 3, qubitron.H(a), qubitron.CZ(a, b))


def test_batch_insert_doesnt_overshift_due_to_previous_shifts():
    a = qubitron.NamedQubit('a')
    c = qubitron.Circuit([qubitron.H(a)] * 3)
    c.batch_insert([(0, qubitron.Z(a)), (0, qubitron.Z(a)), (1, qubitron.X(a)), (2, qubitron.Y(a))])
    assert c == qubitron.Circuit(
        qubitron.Z(a), qubitron.Z(a), qubitron.H(a), qubitron.X(a), qubitron.H(a), qubitron.Y(a), qubitron.H(a)
    )


def test_batch_insert_doesnt_overshift_due_to_inline_inserts():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SWAP(a, b), qubitron.SWAP(a, b), qubitron.H(a), qubitron.SWAP(a, b), qubitron.SWAP(a, b))
    c.batch_insert([(0, qubitron.X(a)), (3, qubitron.X(b)), (4, qubitron.Y(a))])
    assert c == qubitron.Circuit(
        qubitron.X(a),
        qubitron.SWAP(a, b),
        qubitron.SWAP(a, b),
        qubitron.H(a),
        qubitron.X(b),
        qubitron.SWAP(a, b),
        qubitron.Y(a),
        qubitron.SWAP(a, b),
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_next_moments_operating_on(circuit_cls):
    for _ in range(20):
        n_moments = randint(1, 10)
        circuit = qubitron.testing.random_circuit(randint(1, 20), n_moments, random())
        circuit_qubits = circuit.all_qubits()
        n_key_qubits = randint(int(bool(circuit_qubits)), len(circuit_qubits))
        key_qubits = sample(sorted(circuit_qubits), n_key_qubits)
        start = randrange(len(circuit))
        next_moments = circuit.next_moments_operating_on(key_qubits, start)
        for q, m in next_moments.items():
            if m == len(circuit):
                p = circuit.prev_moment_operating_on([q])
            else:
                p = circuit.prev_moment_operating_on([q], m - 1)
            assert (not p) or (p < start)


def test_pick_inserted_ops_moment_indices():
    for _ in range(20):
        n_moments = randint(1, 10)
        n_qubits = randint(1, 20)
        op_density = random()
        circuit = qubitron.testing.random_circuit(n_qubits, n_moments, op_density)
        start = randrange(n_moments)
        first_half = qubitron.Circuit(circuit[:start])
        second_half = qubitron.Circuit(circuit[start:])
        operations = tuple(op for moment in second_half for op in moment.operations)
        squeezed_second_half = qubitron.Circuit(operations, strategy=qubitron.InsertStrategy.EARLIEST)
        expected_circuit = qubitron.Circuit(first_half._moments + squeezed_second_half._moments)
        expected_circuit._moments += [
            qubitron.Moment() for _ in range(len(circuit) - len(expected_circuit))
        ]
        insert_indices, _ = circuits.circuit._pick_inserted_ops_moment_indices(operations, start)
        actual_circuit = qubitron.Circuit(
            first_half._moments + [qubitron.Moment() for _ in range(n_moments - start)]
        )
        for op, insert_index in zip(operations, insert_indices):
            actual_circuit._moments[insert_index] = actual_circuit._moments[
                insert_index
            ].with_operation(op)
        assert actual_circuit == expected_circuit


def test_push_frontier_new_moments():
    operation = qubitron.X(qubitron.NamedQubit('q'))
    insertion_index = 3
    circuit = qubitron.Circuit()
    circuit._insert_operations([operation], [insertion_index])
    assert circuit == qubitron.Circuit(
        [qubitron.Moment() for _ in range(insertion_index)] + [qubitron.Moment([operation])]
    )


def test_push_frontier_random_circuit():
    for _ in range(20):
        n_moments = randint(1, 10)
        circuit = qubitron.testing.random_circuit(randint(1, 20), n_moments, random())
        qubits = sorted(circuit.all_qubits())
        early_frontier = {q: randint(0, n_moments) for q in sample(qubits, randint(0, len(qubits)))}
        late_frontier = {q: randint(0, n_moments) for q in sample(qubits, randint(0, len(qubits)))}
        update_qubits = sample(qubits, randint(0, len(qubits)))

        orig_early_frontier = {q: f for q, f in early_frontier.items()}
        orig_moments = [m for m in circuit._moments]
        insert_index, n_new_moments = circuit._push_frontier(
            early_frontier, late_frontier, update_qubits
        )

        assert set(early_frontier.keys()) == set(orig_early_frontier.keys())
        for q in set(early_frontier).difference(update_qubits):
            assert early_frontier[q] == orig_early_frontier[q]
        for q, f in late_frontier.items():
            assert orig_early_frontier.get(q, 0) <= late_frontier[q] + n_new_moments
            if f != len(orig_moments):
                assert orig_moments[f] == circuit[f + n_new_moments]
        for q in set(update_qubits).intersection(early_frontier):
            if orig_early_frontier[q] == insert_index:
                assert orig_early_frontier[q] == early_frontier[q]
                assert (not n_new_moments) or (circuit._moments[early_frontier[q]] == qubitron.Moment())
            elif orig_early_frontier[q] == len(orig_moments):
                assert early_frontier[q] == len(circuit)
            else:
                assert orig_moments[orig_early_frontier[q]] == circuit._moments[early_frontier[q]]


@pytest.mark.parametrize(
    'circuit', [qubitron.testing.random_circuit(qubitron.LineQubit.range(10), 10, 0.5) for _ in range(20)]
)
def test_insert_operations_random_circuits(circuit):
    n_moments = len(circuit)
    operations, insert_indices = [], []
    for moment_index, moment in enumerate(circuit):
        for op in moment.operations:
            operations.append(op)
            insert_indices.append(moment_index)
    other_circuit = qubitron.Circuit([qubitron.Moment() for _ in range(n_moments)])
    other_circuit._insert_operations(operations, insert_indices)
    assert circuit == other_circuit


def test_insert_zero_index():
    # Should always go to moment[0], independent of qubit order or earliest/inline strategy.
    q0, q1 = qubitron.LineQubit.range(2)
    c0 = qubitron.Circuit(qubitron.X(q0))
    c0.insert(0, qubitron.Y.on_each(q0, q1), strategy=qubitron.InsertStrategy.EARLIEST)
    c1 = qubitron.Circuit(qubitron.X(q0))
    c1.insert(0, qubitron.Y.on_each(q1, q0), strategy=qubitron.InsertStrategy.EARLIEST)
    c2 = qubitron.Circuit(qubitron.X(q0))
    c2.insert(0, qubitron.Y.on_each(q0, q1), strategy=qubitron.InsertStrategy.INLINE)
    c3 = qubitron.Circuit(qubitron.X(q0))
    c3.insert(0, qubitron.Y.on_each(q1, q0), strategy=qubitron.InsertStrategy.INLINE)
    expected = qubitron.Circuit(qubitron.Moment(qubitron.Y(q0), qubitron.Y(q1)), qubitron.Moment(qubitron.X(q0)))
    assert c0 == expected
    assert c1 == expected
    assert c2 == expected
    assert c3 == expected


def test_insert_earliest_on_previous_moment():
    q = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.Moment(qubitron.X(q)), qubitron.Moment(), qubitron.Moment(), qubitron.Moment(qubitron.Z(q)))
    c.insert(3, qubitron.Y(q), strategy=qubitron.InsertStrategy.EARLIEST)
    # Should fall back to moment[1] since EARLIEST
    assert c == qubitron.Circuit(
        qubitron.Moment(qubitron.X(q)), qubitron.Moment(qubitron.Y(q)), qubitron.Moment(), qubitron.Moment(qubitron.Z(q))
    )


def test_insert_inline_end_of_circuit():
    # If end index is specified, INLINE should place all ops there independent of qubit order.
    q0, q1 = qubitron.LineQubit.range(2)
    c0 = qubitron.Circuit(qubitron.X(q0))
    c0.insert(1, qubitron.Y.on_each(q0, q1), strategy=qubitron.InsertStrategy.INLINE)
    c1 = qubitron.Circuit(qubitron.X(q0))
    c1.insert(1, qubitron.Y.on_each(q1, q0), strategy=qubitron.InsertStrategy.INLINE)
    c2 = qubitron.Circuit(qubitron.X(q0))
    c2.insert(5, qubitron.Y.on_each(q0, q1), strategy=qubitron.InsertStrategy.INLINE)
    c3 = qubitron.Circuit(qubitron.X(q0))
    c3.insert(5, qubitron.Y.on_each(q1, q0), strategy=qubitron.InsertStrategy.INLINE)
    expected = qubitron.Circuit(qubitron.Moment(qubitron.X(q0)), qubitron.Moment(qubitron.Y(q0), qubitron.Y(q1)))
    assert c0 == expected
    assert c1 == expected
    assert c2 == expected
    assert c3 == expected


def test_insert_operations_errors():
    a, b, c = (qubitron.NamedQubit(s) for s in 'abc')
    with pytest.raises(ValueError):
        circuit = qubitron.Circuit([qubitron.Moment([qubitron.Z(c)])])
        operations = [qubitron.X(a), qubitron.CZ(a, b)]
        insertion_indices = [0, 0]
        circuit._insert_operations(operations, insertion_indices)

    with pytest.raises(ValueError):
        circuit = qubitron.Circuit(qubitron.X(a))
        operations = [qubitron.CZ(a, b)]
        insertion_indices = [0]
        circuit._insert_operations(operations, insertion_indices)

    with pytest.raises(ValueError):
        circuit = qubitron.Circuit()
        operations = [qubitron.X(a), qubitron.CZ(a, b)]
        insertion_indices = []
        circuit._insert_operations(operations, insertion_indices)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_to_qasm(circuit_cls):
    q0 = qubitron.NamedQubit('q0')
    circuit = circuit_cls(qubitron.X(q0), qubitron.measure(q0, key='mmm'))
    assert circuit.to_qasm() == qubitron.qasm(circuit)
    assert (
        circuit.to_qasm()
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q0]
qreg q[1];
creg m_mmm[1];


x q[0];
measure q[0] -> m_mmm[0];
"""
    )
    assert circuit.to_qasm(version="3.0") == qubitron.qasm(circuit, args=qubitron.QasmArgs(version="3.0"))
    assert (
        circuit.to_qasm(version="3.0")
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 3.0;
include "stdgates.inc";


// Qubits: [q0]
qubit[1] q;
bit[1] m_mmm;


x q[0];
m_mmm[0] = measure q[0];
"""
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_save_qasm(tmpdir, circuit_cls):
    file_path = os.path.join(tmpdir, 'test.qasm')
    q0 = qubitron.NamedQubit('q0')
    circuit = circuit_cls(qubitron.X(q0))

    circuit.save_qasm(file_path)
    with open(file_path, 'r') as f:
        file_content = f.read()
    assert (
        file_content
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q0]
qreg q[1];


x q[0];
"""
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_findall_operations_between(circuit_cls):
    a, b, c, d = qubitron.LineQubit.range(4)

    #    0: ───H───@───────────────────────────────────────@───H───
    #              │                                       │
    #    1: ───────@───H───@───────────────────────@───H───@───────
    #                      │                       │
    #    2: ───────────────@───H───@───────@───H───@───────────────
    #                              │       │
    #    3: ───────────────────────@───H───@───────────────────────
    #
    # moments: 0   1   2   3   4   5   6   7   8   9   10  11  12
    circuit = circuit_cls(
        qubitron.H(a),
        qubitron.CZ(a, b),
        qubitron.H(b),
        qubitron.CZ(b, c),
        qubitron.H(c),
        qubitron.CZ(c, d),
        qubitron.H(d),
        qubitron.CZ(c, d),
        qubitron.H(c),
        qubitron.CZ(b, c),
        qubitron.H(b),
        qubitron.CZ(a, b),
        qubitron.H(a),
    )

    # Empty frontiers means no results.
    actual = circuit.findall_operations_between(start_frontier={}, end_frontier={})
    assert actual == []

    # Empty range is empty.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={a: 5})
    assert actual == []

    # Default end_frontier value is len(circuit.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={})
    assert actual == [(11, qubitron.CZ(a, b)), (12, qubitron.H(a))]

    # Default start_frontier value is 0.
    actual = circuit.findall_operations_between(start_frontier={}, end_frontier={a: 5})
    assert actual == [(0, qubitron.H(a)), (1, qubitron.CZ(a, b))]

    # omit_crossing_operations omits crossing operations.
    actual = circuit.findall_operations_between(
        start_frontier={a: 5}, end_frontier={}, omit_crossing_operations=True
    )
    assert actual == [(12, qubitron.H(a))]

    # omit_crossing_operations keeps operations across included regions.
    actual = circuit.findall_operations_between(
        start_frontier={a: 5, b: 5}, end_frontier={}, omit_crossing_operations=True
    )
    assert actual == [(10, qubitron.H(b)), (11, qubitron.CZ(a, b)), (12, qubitron.H(a))]

    # Regions are OR'd together, not AND'd together.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={b: 5})
    assert actual == [
        (1, qubitron.CZ(a, b)),
        (2, qubitron.H(b)),
        (3, qubitron.CZ(b, c)),
        (11, qubitron.CZ(a, b)),
        (12, qubitron.H(a)),
    ]

    # Regions are OR'd together, not AND'd together (2).
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={a: 5, b: 5})
    assert actual == [(1, qubitron.CZ(a, b)), (2, qubitron.H(b)), (3, qubitron.CZ(b, c))]

    # Inclusive start, exclusive end.
    actual = circuit.findall_operations_between(start_frontier={c: 4}, end_frontier={c: 8})
    assert actual == [(4, qubitron.H(c)), (5, qubitron.CZ(c, d)), (7, qubitron.CZ(c, d))]

    # Out of range is clamped.
    actual = circuit.findall_operations_between(start_frontier={a: -100}, end_frontier={a: +100})
    assert actual == [(0, qubitron.H(a)), (1, qubitron.CZ(a, b)), (11, qubitron.CZ(a, b)), (12, qubitron.H(a))]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_reachable_frontier_from(circuit_cls):
    a, b, c, d = qubitron.LineQubit.range(4)

    #    0: ───H───@───────────────────────────────────────@───H───
    #              │                                       │
    #    1: ───────@───H───@───────────────────────@───H───@───────
    #                      │                       │
    #    2: ───────────────@───H───@───────@───H───@───────────────
    #                              │       │
    #    3: ───────────────────────@───H───@───────────────────────
    #
    # moments: 0   1   2   3   4   5   6   7   8   9   10  11  12
    circuit = circuit_cls(
        qubitron.H(a),
        qubitron.CZ(a, b),
        qubitron.H(b),
        qubitron.CZ(b, c),
        qubitron.H(c),
        qubitron.CZ(c, d),
        qubitron.H(d),
        qubitron.CZ(c, d),
        qubitron.H(c),
        qubitron.CZ(b, c),
        qubitron.H(b),
        qubitron.CZ(a, b),
        qubitron.H(a),
    )

    # Empty cases.
    assert circuit_cls().reachable_frontier_from(start_frontier={}) == {}
    assert circuit.reachable_frontier_from(start_frontier={}) == {}

    # Clamped input cases.
    assert circuit_cls().reachable_frontier_from(start_frontier={a: 5}) == {a: 5}
    assert circuit_cls().reachable_frontier_from(start_frontier={a: -100}) == {a: 0}
    assert circuit.reachable_frontier_from(start_frontier={a: 100}) == {a: 100}

    # Stopped by crossing outside case.
    assert circuit.reachable_frontier_from({a: -1}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 0}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 1}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 2}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 5}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 10}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 11}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 12}) == {a: 13}
    assert circuit.reachable_frontier_from({a: 13}) == {a: 13}
    assert circuit.reachable_frontier_from({a: 14}) == {a: 14}

    # Inside crossing works only before blocked case.
    assert circuit.reachable_frontier_from({a: 0, b: 0}) == {a: 11, b: 3}
    assert circuit.reachable_frontier_from({a: 2, b: 2}) == {a: 11, b: 3}
    assert circuit.reachable_frontier_from({a: 0, b: 4}) == {a: 1, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 4}) == {a: 11, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 9}) == {a: 11, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 10}) == {a: 13, b: 13}

    # Travelling shadow.
    assert circuit.reachable_frontier_from({a: 0, b: 0, c: 0}) == {a: 11, b: 9, c: 5}

    # Full circuit
    assert circuit.reachable_frontier_from({a: 0, b: 0, c: 0, d: 0}) == {a: 13, b: 13, c: 13, d: 13}

    # Blocker.
    assert circuit.reachable_frontier_from(
        {a: 0, b: 0, c: 0, d: 0}, is_blocker=lambda op: op == qubitron.CZ(b, c)
    ) == {a: 11, b: 3, c: 3, d: 5}


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_submoments(circuit_cls):
    a, b, c, d, e, f = qubitron.LineQubit.range(6)
    circuit = circuit_cls(
        qubitron.H.on(a),
        qubitron.H.on(d),
        qubitron.CZ.on(a, d),
        qubitron.CZ.on(b, c),
        (qubitron.CNOT**0.5).on(a, d),
        (qubitron.CNOT**0.5).on(b, e),
        (qubitron.CNOT**0.5).on(c, f),
        qubitron.H.on(c),
        qubitron.H.on(e),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
          ┌───────────┐   ┌──────┐
0: ───H────@───────────────@─────────
           │               │
1: ───@────┼@──────────────┼─────────
      │    ││              │
2: ───@────┼┼────@─────────┼────H────
           ││    │         │
3: ───H────@┼────┼─────────X^0.5─────
            │    │
4: ─────────X^0.5┼─────────H─────────
                 │
5: ──────────────X^0.5───────────────
          └───────────┘   └──────┘
""",
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
  0 1 2 3     4     5
  │ │ │ │     │     │
  H @─@ H     │     │
  │ │ │ │     │     │
┌╴│ │ │ │     │     │    ╶┐
│ @─┼─┼─@     │     │     │
│ │ @─┼─┼─────X^0.5 │     │
│ │ │ @─┼─────┼─────X^0.5 │
└╴│ │ │ │     │     │    ╶┘
  │ │ │ │     │     │
┌╴│ │ │ │     │     │    ╶┐
│ @─┼─┼─X^0.5 H     │     │
│ │ │ H │     │     │     │
└╴│ │ │ │     │     │    ╶┘
  │ │ │ │     │     │
""",
        transpose=True,
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        r"""
          /-----------\   /------\
0: ---H----@---------------@---------
           |               |
1: ---@----|@--------------|---------
      |    ||              |
2: ---@----||----@---------|----H----
           ||    |         |
3: ---H----@|----|---------X^0.5-----
            |    |
4: ---------X^0.5|---------H---------
                 |
5: --------------X^0.5---------------
          \-----------/   \------/
""",
        use_unicode_characters=False,
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        r"""
  0 1 2 3     4     5
  | | | |     |     |
  H @-@ H     |     |
  | | | |     |     |
/ | | | |     |     |     \
| @-----@     |     |     |
| | @---------X^0.5 |     |
| | | @-------------X^0.5 |
\ | | | |     |     |     /
  | | | |     |     |
/ | | | |     |     |     \
| @-----X^0.5 H     |     |
| | | H |     |     |     |
\ | | | |     |     |     /
  | | | |     |     |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_decompose(circuit_cls):
    a, b = qubitron.LineQubit.range(2)
    assert qubitron.decompose(circuit_cls(qubitron.X(a), qubitron.Y(b), qubitron.CZ(a, b))) == [
        qubitron.X(a),
        qubitron.Y(b),
        qubitron.CZ(a, b),
    ]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_measurement_key_mapping(circuit_cls):
    a, b = qubitron.LineQubit.range(2)
    c = circuit_cls(qubitron.X(a), qubitron.measure(a, key='m1'), qubitron.measure(b, key='m2'))
    assert c.all_measurement_key_names() == {'m1', 'm2'}

    assert qubitron.with_measurement_key_mapping(c, {'m1': 'p1'}).all_measurement_key_names() == {
        'p1',
        'm2',
    }

    assert qubitron.with_measurement_key_mapping(
        c, {'m1': 'p1', 'm2': 'p2'}
    ).all_measurement_key_names() == {'p1', 'p2'}

    c_swapped = qubitron.with_measurement_key_mapping(c, {'m1': 'm2', 'm2': 'm1'})
    assert c_swapped.all_measurement_key_names() == {'m1', 'm2'}

    # Verify that the keys were actually swapped.
    simulator = qubitron.Simulator()
    assert simulator.run(c).measurements == {'m1': 1, 'm2': 0}
    assert simulator.run(c_swapped).measurements == {'m1': 0, 'm2': 1}

    assert qubitron.with_measurement_key_mapping(c, {'x': 'z'}).all_measurement_key_names() == {
        'm1',
        'm2',
    }


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_measurement_key_mapping_preserves_moments(circuit_cls):
    a, b = qubitron.LineQubit.range(2)
    c = circuit_cls(
        qubitron.Moment(qubitron.X(a)),
        qubitron.Moment(),
        qubitron.Moment(qubitron.measure(a, key='m1')),
        qubitron.Moment(qubitron.measure(b, key='m2')),
    )

    key_map = {'m1': 'p1'}
    remapped_circuit = qubitron.with_measurement_key_mapping(c, key_map)
    assert list(remapped_circuit.moments) == [
        qubitron.with_measurement_key_mapping(moment, key_map) for moment in c.moments
    ]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_inverse(circuit_cls):
    a, b = qubitron.LineQubit.range(2)
    forward = circuit_cls((qubitron.X**0.5)(a), (qubitron.Y**-0.2)(b), qubitron.CZ(a, b))
    backward = circuit_cls((qubitron.CZ ** (-1.0))(a, b), (qubitron.X ** (-0.5))(a), (qubitron.Y ** (0.2))(b))
    qubitron.testing.assert_same_circuits(qubitron.inverse(forward), backward)

    qubitron.testing.assert_same_circuits(qubitron.inverse(circuit_cls()), circuit_cls())

    no_inverse = circuit_cls(qubitron.measure(a, b))
    with pytest.raises(TypeError, match='__pow__'):
        qubitron.inverse(no_inverse)

    # Default when there is no inverse for an op.
    default = circuit_cls((qubitron.X**0.5)(a), (qubitron.Y**-0.2)(b))
    qubitron.testing.assert_same_circuits(qubitron.inverse(no_inverse, default), default)
    assert qubitron.inverse(no_inverse, None) is None


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_pow_valid_only_for_minus_1(circuit_cls):
    a, b = qubitron.LineQubit.range(2)
    forward = circuit_cls((qubitron.X**0.5)(a), (qubitron.Y**-0.2)(b), qubitron.CZ(a, b))

    backward = circuit_cls((qubitron.CZ ** (-1.0))(a, b), (qubitron.X ** (-0.5))(a), (qubitron.Y ** (0.2))(b))
    qubitron.testing.assert_same_circuits(qubitron.pow(forward, -1), backward)
    with pytest.raises(TypeError, match='__pow__'):
        qubitron.pow(forward, 1)
    with pytest.raises(TypeError, match='__pow__'):
        qubitron.pow(forward, 0)
    with pytest.raises(TypeError, match='__pow__'):
        qubitron.pow(forward, -2.5)


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_moment_groups(circuit_cls):
    qubits = [qubitron.GridQubit(x, y) for x in range(8) for y in range(8)]
    c0 = qubitron.H(qubits[0])
    c7 = qubitron.H(qubits[7])
    cz14 = qubitron.CZ(qubits[1], qubits[4])
    cz25 = qubitron.CZ(qubits[2], qubits[5])
    cz36 = qubitron.CZ(qubits[3], qubits[6])
    moment1 = qubitron.Moment([c0, cz14, cz25, c7])
    moment2 = qubitron.Moment([c0, cz14, cz25, cz36, c7])
    moment3 = qubitron.Moment([cz14, cz25, cz36])
    moment4 = qubitron.Moment([cz25, cz36])
    circuit = circuit_cls((moment1, moment2, moment3, moment4))
    qubitron.testing.assert_has_diagram(
        circuit,
        r"""
           ┌──┐   ┌───┐   ┌───┐   ┌──┐
(0, 0): ────H──────H─────────────────────

(0, 1): ────@──────@───────@─────────────
            │      │       │
(0, 2): ────┼@─────┼@──────┼@──────@─────
            ││     ││      ││      │
(0, 3): ────┼┼─────┼┼@─────┼┼@─────┼@────
            ││     │││     │││     ││
(0, 4): ────@┼─────@┼┼─────@┼┼─────┼┼────
             │      ││      ││     ││
(0, 5): ─────@──────@┼──────@┼─────@┼────
                     │       │      │
(0, 6): ─────────────@───────@──────@────

(0, 7): ────H──────H─────────────────────
           └──┘   └───┘   └───┘   └──┘
""",
        use_unicode_characters=True,
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_moments_property(circuit_cls):
    q = qubitron.NamedQubit('q')
    c = circuit_cls(qubitron.X(q), qubitron.Y(q))
    assert c.moments[0] == qubitron.Moment([qubitron.X(q)])
    assert c.moments[1] == qubitron.Moment([qubitron.Y(q)])


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_json_dict(circuit_cls):
    q0, q1 = qubitron.LineQubit.range(2)
    c = circuit_cls(qubitron.CNOT(q0, q1))
    moments = [qubitron.Moment([qubitron.CNOT(q0, q1)])]
    if circuit_cls == qubitron.FrozenCircuit:
        moments = tuple(moments)
    assert c._json_dict_() == {'moments': moments}


def test_with_noise():
    class Noise(qubitron.NoiseModel):
        def noisy_operation(self, operation):
            yield operation
            if qubitron.LineQubit(0) in operation.qubits:
                yield qubitron.H(qubitron.LineQubit(0))

    q0, q1 = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(q0), qubitron.Y(q1), qubitron.Z(q1), qubitron.Moment([qubitron.X(q0)]))
    c_expected = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(q0), qubitron.Y(q1)]),
            qubitron.Moment([qubitron.H(q0)]),
            qubitron.Moment([qubitron.Z(q1)]),
            qubitron.Moment([qubitron.X(q0)]),
            qubitron.Moment([qubitron.H(q0)]),
        ]
    )
    c_noisy = c.with_noise(Noise())
    assert c_noisy == c_expected

    # Accepts NOISE_MODEL_LIKE.
    assert c.with_noise(None) == c
    assert c.with_noise(qubitron.depolarize(0.1)) == qubitron.Circuit(
        qubitron.X(q0),
        qubitron.Y(q1),
        qubitron.Moment([d.with_tags(ops.VirtualTag()) for d in qubitron.depolarize(0.1).on_each(q0, q1)]),
        qubitron.Z(q1),
        qubitron.Moment([d.with_tags(ops.VirtualTag()) for d in qubitron.depolarize(0.1).on_each(q0, q1)]),
        qubitron.Moment([qubitron.X(q0)]),
        qubitron.Moment([d.with_tags(ops.VirtualTag()) for d in qubitron.depolarize(0.1).on_each(q0, q1)]),
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_init_contents(circuit_cls):
    a, b = qubitron.LineQubit.range(2)

    # Moments are not subject to insertion rules.
    c = circuit_cls(
        qubitron.Moment([qubitron.H(a)]), qubitron.Moment([qubitron.X(b)]), qubitron.Moment([qubitron.CNOT(a, b)])
    )
    assert len(c.moments) == 3

    # Earliest packing by default.
    c = circuit_cls(qubitron.H(a), qubitron.X(b), qubitron.CNOT(a, b))
    assert c == circuit_cls(qubitron.Moment([qubitron.H(a), qubitron.X(b)]), qubitron.Moment([qubitron.CNOT(a, b)]))

    # Packing can be controlled.
    c = circuit_cls(qubitron.H(a), qubitron.X(b), qubitron.CNOT(a, b), strategy=qubitron.InsertStrategy.NEW)
    assert c == circuit_cls(
        qubitron.Moment([qubitron.H(a)]), qubitron.Moment([qubitron.X(b)]), qubitron.Moment([qubitron.CNOT(a, b)])
    )

    circuit_cls()


def test_transform_qubits():
    a, b, c = qubitron.LineQubit.range(3)
    original = qubitron.Circuit(
        qubitron.X(a), qubitron.CNOT(a, b), qubitron.Moment(), qubitron.Moment([qubitron.CNOT(b, c)])
    )
    x, y, z = qubitron.GridQubit.rect(3, 1, 10, 20)
    desired = qubitron.Circuit(
        qubitron.X(x), qubitron.CNOT(x, y), qubitron.Moment(), qubitron.Moment([qubitron.CNOT(y, z)])
    )
    assert original.transform_qubits(lambda q: qubitron.GridQubit(10 + q.x, 20)) == desired
    assert (
        original.transform_qubits(
            {
                a: qubitron.GridQubit(10 + a.x, 20),
                b: qubitron.GridQubit(10 + b.x, 20),
                c: qubitron.GridQubit(10 + c.x, 20),
            }
        )
        == desired
    )
    with pytest.raises(TypeError, match='must be a function or dict'):
        _ = original.transform_qubits('bad arg')


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_indexing_by_pair(circuit_cls):
    # 0: ───H───@───X───@───
    #           │       │
    # 1: ───────H───@───@───
    #               │   │
    # 2: ───────────H───X───
    q = qubitron.LineQubit.range(3)
    c = circuit_cls(
        [
            qubitron.H(q[0]),
            qubitron.H(q[1]).controlled_by(q[0]),
            qubitron.H(q[2]).controlled_by(q[1]),
            qubitron.X(q[0]),
            qubitron.CCNOT(*q),
        ]
    )

    # Indexing by single moment and qubit.
    assert c[0, q[0]] == c[0][q[0]] == qubitron.H(q[0])
    assert c[1, q[0]] == c[1, q[1]] == qubitron.H(q[1]).controlled_by(q[0])
    assert c[2, q[0]] == c[2][q[0]] == qubitron.X(q[0])
    assert c[2, q[1]] == c[2, q[2]] == qubitron.H(q[2]).controlled_by(q[1])
    assert c[3, q[0]] == c[3, q[1]] == c[3, q[2]] == qubitron.CCNOT(*q)

    # Indexing by moment and qubit - throws if there is no operation.
    with pytest.raises(KeyError, match="Moment doesn't act on given qubit"):
        _ = c[0, q[1]]

    # Indexing by single moment and multiple qubits.
    assert c[0, q] == c[0]
    assert c[1, q] == c[1]
    assert c[2, q] == c[2]
    assert c[3, q] == c[3]
    assert c[0, q[0:2]] == c[0]
    assert c[0, q[1:3]] == qubitron.Moment([])
    assert c[1, q[1:2]] == c[1]
    assert c[2, [q[0]]] == qubitron.Moment([qubitron.X(q[0])])
    assert c[2, q[1:3]] == qubitron.Moment([qubitron.H(q[2]).controlled_by(q[1])])
    assert c[np.int64(2), q[0:2]] == c[2]

    # Indexing by single qubit.
    assert c[:, q[0]] == circuit_cls(
        [
            qubitron.Moment([qubitron.H(q[0])]),
            qubitron.Moment([qubitron.H(q[1]).controlled_by(q[0])]),
            qubitron.Moment([qubitron.X(q[0])]),
            qubitron.Moment([qubitron.CCNOT(q[0], q[1], q[2])]),
        ]
    )
    assert c[:, q[1]] == circuit_cls(
        [
            qubitron.Moment([]),
            qubitron.Moment([qubitron.H(q[1]).controlled_by(q[0])]),
            qubitron.Moment([qubitron.H(q[2]).controlled_by(q[1])]),
            qubitron.Moment([qubitron.CCNOT(q[0], q[1], q[2])]),
        ]
    )
    assert c[:, q[2]] == circuit_cls(
        [
            qubitron.Moment([]),
            qubitron.Moment([]),
            qubitron.Moment([qubitron.H(q[2]).controlled_by(q[1])]),
            qubitron.Moment([qubitron.CCNOT(q[0], q[1], q[2])]),
        ]
    )

    # Indexing by several qubits.
    assert c[:, q] == c[:, q[0:2]] == c[:, [q[0], q[2]]] == c
    assert c[:, q[1:3]] == circuit_cls(
        [
            qubitron.Moment([]),
            qubitron.Moment([qubitron.H(q[1]).controlled_by(q[0])]),
            qubitron.Moment([qubitron.H(q[2]).controlled_by(q[1])]),
            qubitron.Moment([qubitron.CCNOT(q[0], q[1], q[2])]),
        ]
    )

    # Indexing by several moments and one qubit.
    assert c[1:3, q[0]] == circuit_cls([qubitron.H(q[1]).controlled_by(q[0]), qubitron.X(q[0])])
    assert c[1::2, q[2]] == circuit_cls([qubitron.Moment([]), qubitron.Moment([qubitron.CCNOT(*q)])])

    # Indexing by several moments and several qubits.
    assert c[0:2, q[1:3]] == circuit_cls(
        [qubitron.Moment([]), qubitron.Moment([qubitron.H(q[1]).controlled_by(q[0])])]
    )
    assert c[::2, q[0:2]] == circuit_cls(
        [qubitron.Moment([qubitron.H(q[0])]), qubitron.Moment([qubitron.H(q[2]).controlled_by(q[1]), qubitron.X(q[0])])]
    )

    # Equivalent ways of indexing.
    assert c[0:2, q[1:3]] == c[0:2][:, q[1:3]] == c[:, q[1:3]][0:2]

    # Passing more than 2 items is forbidden.
    with pytest.raises(ValueError, match='If key is tuple, it must be a pair.'):
        _ = c[0, q[1], 0]

    # Can't swap indices.
    with pytest.raises(TypeError, match='indices must be integers or slices'):
        _ = c[q[1], 0]


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_indexing_by_numpy_integer(circuit_cls):
    q = qubitron.NamedQubit('q')
    c = circuit_cls(qubitron.X(q), qubitron.Y(q))

    assert c[np.int32(1)] == qubitron.Moment([qubitron.Y(q)])
    assert c[np.int64(1)] == qubitron.Moment([qubitron.Y(q)])


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_all_measurement_key_names(circuit_cls):
    class Unknown(qubitron.testing.SingleQubitGate):
        def _measurement_key_name_(self):
            return 'test'

    a, b = qubitron.LineQubit.range(2)
    c = circuit_cls(
        qubitron.X(a),
        qubitron.CNOT(a, b),
        qubitron.measure(a, key='x'),
        qubitron.measure(b, key='y'),
        qubitron.reset(a),
        qubitron.measure(a, b, key='xy'),
        Unknown().on(a),
    )

    # Big case.
    assert c.all_measurement_key_names() == {'x', 'y', 'xy', 'test'}
    assert c.all_measurement_key_names() == qubitron.measurement_key_names(c)
    assert c.all_measurement_key_names() == c.all_measurement_key_objs()

    # Empty case.
    assert circuit_cls().all_measurement_key_names() == set()

    # Order does not matter.
    assert circuit_cls(
        qubitron.Moment([qubitron.measure(a, key='x'), qubitron.measure(b, key='y')])
    ).all_measurement_key_names() == {'x', 'y'}
    assert circuit_cls(
        qubitron.Moment([qubitron.measure(b, key='y'), qubitron.measure(a, key='x')])
    ).all_measurement_key_names() == {'x', 'y'}


def test_zip():
    a, b, c, d = qubitron.LineQubit.range(4)

    circuit1 = qubitron.Circuit(qubitron.H(a), qubitron.CNOT(a, b))
    circuit2 = qubitron.Circuit(qubitron.X(c), qubitron.Y(c), qubitron.Z(c))
    circuit3 = qubitron.Circuit(qubitron.Moment(), qubitron.Moment(qubitron.S(d)))

    # Calling works both static-style and instance-style.
    assert circuit1.zip(circuit2) == qubitron.Circuit.zip(circuit1, circuit2)

    # Empty cases.
    assert qubitron.Circuit.zip() == qubitron.Circuit()
    assert qubitron.Circuit.zip(qubitron.Circuit()) == qubitron.Circuit()
    assert qubitron.Circuit().zip(qubitron.Circuit()) == qubitron.Circuit()
    assert circuit1.zip(qubitron.Circuit()) == circuit1
    assert qubitron.Circuit(qubitron.Moment()).zip(qubitron.Circuit()) == qubitron.Circuit(qubitron.Moment())
    assert qubitron.Circuit().zip(qubitron.Circuit(qubitron.Moment())) == qubitron.Circuit(qubitron.Moment())

    # Small cases.
    assert (
        circuit1.zip(circuit2)
        == circuit2.zip(circuit1)
        == qubitron.Circuit(
            qubitron.Moment(qubitron.H(a), qubitron.X(c)),
            qubitron.Moment(qubitron.CNOT(a, b), qubitron.Y(c)),
            qubitron.Moment(qubitron.Z(c)),
        )
    )
    assert circuit1.zip(circuit2, circuit3) == qubitron.Circuit(
        qubitron.Moment(qubitron.H(a), qubitron.X(c)),
        qubitron.Moment(qubitron.CNOT(a, b), qubitron.Y(c), qubitron.S(d)),
        qubitron.Moment(qubitron.Z(c)),
    )

    # Overlapping operations.
    with pytest.raises(ValueError, match="moment index 1.*\n.*CNOT"):
        _ = qubitron.Circuit.zip(
            qubitron.Circuit(qubitron.X(a), qubitron.CNOT(a, b)), qubitron.Circuit(qubitron.X(b), qubitron.Z(b))
        )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_zip_alignment(circuit_cls):
    a, b, c = qubitron.LineQubit.range(3)

    circuit1 = circuit_cls([qubitron.H(a)] * 5)
    circuit2 = circuit_cls([qubitron.H(b)] * 3)
    circuit3 = circuit_cls([qubitron.H(c)] * 2)

    c_start = circuit_cls.zip(circuit1, circuit2, circuit3, align='LEFT')
    assert c_start == circuit_cls(
        qubitron.Moment(qubitron.H(a), qubitron.H(b), qubitron.H(c)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b), qubitron.H(c)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b)),
        qubitron.Moment(qubitron.H(a)),
        qubitron.Moment(qubitron.H(a)),
    )

    c_end = circuit_cls.zip(circuit1, circuit2, circuit3, align='RIGHT')
    assert c_end == circuit_cls(
        qubitron.Moment(qubitron.H(a)),
        qubitron.Moment(qubitron.H(a)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b), qubitron.H(c)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b), qubitron.H(c)),
    )


@pytest.mark.parametrize('circuit_cls', [qubitron.Circuit, qubitron.FrozenCircuit])
def test_repr_html_escaping(circuit_cls):
    class TestGate(qubitron.Gate):
        def num_qubits(self):
            return 2

        def _circuit_diagram_info_(self, args):
            return qubitron.CircuitDiagramInfo(wire_symbols=["< ' F ' >", "< ' F ' >"])

    F2 = TestGate()
    a = qubitron.LineQubit(1)
    c = qubitron.NamedQubit("|c>")

    circuit = circuit_cls([F2(a, c)])

    # Escaping Special Characters in Gate names.
    assert '&lt; &#x27; F &#x27; &gt;' in circuit._repr_html_()

    # Escaping Special Characters in Qubit names.
    assert '|c&gt;' in circuit._repr_html_()


def test_concat_ragged():
    a, b = qubitron.LineQubit.range(2)
    empty = qubitron.Circuit()

    assert qubitron.Circuit.concat_ragged(empty, empty) == empty
    assert qubitron.Circuit.concat_ragged() == empty
    assert empty.concat_ragged(empty) == empty
    assert empty.concat_ragged(empty, empty) == empty

    ha = qubitron.Circuit(qubitron.H(a))
    hb = qubitron.Circuit(qubitron.H(b))
    assert ha.concat_ragged(hb) == ha.zip(hb)

    assert ha.concat_ragged(empty) == ha
    assert empty.concat_ragged(ha) == ha

    hac = qubitron.Circuit(qubitron.H(a), qubitron.CNOT(a, b))
    assert hac.concat_ragged(hb) == hac + hb
    assert hb.concat_ragged(hac) == hb.zip(hac)

    zig = qubitron.Circuit(qubitron.H(a), qubitron.CNOT(a, b), qubitron.H(b))
    assert zig.concat_ragged(zig) == qubitron.Circuit(
        qubitron.H(a), qubitron.CNOT(a, b), qubitron.Moment(qubitron.H(a), qubitron.H(b)), qubitron.CNOT(a, b), qubitron.H(b)
    )

    zag = qubitron.Circuit(qubitron.H(a), qubitron.H(a), qubitron.CNOT(a, b), qubitron.H(b), qubitron.H(b))
    assert zag.concat_ragged(zag) == qubitron.Circuit(
        qubitron.H(a),
        qubitron.H(a),
        qubitron.CNOT(a, b),
        qubitron.Moment(qubitron.H(a), qubitron.H(b)),
        qubitron.Moment(qubitron.H(a), qubitron.H(b)),
        qubitron.CNOT(a, b),
        qubitron.H(b),
        qubitron.H(b),
    )

    space = qubitron.Circuit(qubitron.Moment()) * 10
    f = qubitron.Circuit.concat_ragged
    assert len(f(space, ha)) == 10
    assert len(f(space, ha, ha, ha)) == 10
    assert len(f(space, f(ha, ha, ha))) == 10
    assert len(f(space, ha, align='LEFT')) == 10
    assert len(f(space, ha, ha, ha, align='RIGHT')) == 12
    assert len(f(space, f(ha, ha, ha, align='LEFT'))) == 10
    assert len(f(space, f(ha, ha, ha, align='RIGHT'))) == 10
    assert len(f(space, f(ha, ha, ha), align='LEFT')) == 10
    assert len(f(space, f(ha, ha, ha), align='RIGHT')) == 10

    # L shape overlap (vary c1).
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 4),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 1),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )
    assert 8 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 6),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )
    assert 9 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 7),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )

    # L shape overlap (vary c2).
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 5, qubitron.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 4, qubitron.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 1, qubitron.CZ(a, b)),
        )
    )
    assert 8 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 6, qubitron.CZ(a, b)),
        )
    )
    assert 9 == len(
        f(
            qubitron.Circuit(qubitron.CZ(a, b), [qubitron.H(a)] * 5),
            qubitron.Circuit([qubitron.H(b)] * 7, qubitron.CZ(a, b)),
        )
    )

    # When scanning sees a possible hit, continues scanning for earlier hit.
    assert 10 == len(
        f(
            qubitron.Circuit(
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(qubitron.H(a)),
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(qubitron.H(b)),
            ),
            qubitron.Circuit(
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(),
                qubitron.Moment(qubitron.H(a)),
                qubitron.Moment(),
                qubitron.Moment(qubitron.H(b)),
            ),
        )
    )
    # Correct tie breaker when one operation sees two possible hits.
    for cz_order in [qubitron.CZ(a, b), qubitron.CZ(b, a)]:
        assert 3 == len(
            f(
                qubitron.Circuit(qubitron.Moment(cz_order), qubitron.Moment(), qubitron.Moment()),
                qubitron.Circuit(qubitron.Moment(qubitron.H(a)), qubitron.Moment(qubitron.H(b))),
            )
        )

    # Types.
    v = ha.freeze().concat_ragged(empty)
    assert type(v) is qubitron.FrozenCircuit and v == ha.freeze()
    v = ha.concat_ragged(empty.freeze())
    assert type(v) is qubitron.Circuit and v == ha
    v = ha.freeze().concat_ragged(empty)
    assert type(v) is qubitron.FrozenCircuit and v == ha.freeze()
    v = qubitron.Circuit.concat_ragged(ha, empty)
    assert type(v) is qubitron.Circuit and v == ha
    v = qubitron.FrozenCircuit.concat_ragged(ha, empty)
    assert type(v) is qubitron.FrozenCircuit and v == ha.freeze()


def test_concat_ragged_alignment():
    a, b = qubitron.LineQubit.range(2)

    assert qubitron.Circuit.concat_ragged(
        qubitron.Circuit(qubitron.X(a)), qubitron.Circuit(qubitron.Y(b)) * 4, qubitron.Circuit(qubitron.Z(a)), align='first'
    ) == qubitron.Circuit(
        qubitron.Moment(qubitron.X(a), qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.Z(a), qubitron.Y(b)),
    )

    assert qubitron.Circuit.concat_ragged(
        qubitron.Circuit(qubitron.X(a)), qubitron.Circuit(qubitron.Y(b)) * 4, qubitron.Circuit(qubitron.Z(a)), align='left'
    ) == qubitron.Circuit(
        qubitron.Moment(qubitron.X(a), qubitron.Y(b)),
        qubitron.Moment(qubitron.Z(a), qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
    )

    assert qubitron.Circuit.concat_ragged(
        qubitron.Circuit(qubitron.X(a)), qubitron.Circuit(qubitron.Y(b)) * 4, qubitron.Circuit(qubitron.Z(a)), align='right'
    ) == qubitron.Circuit(
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.Y(b)),
        qubitron.Moment(qubitron.X(a), qubitron.Y(b)),
        qubitron.Moment(qubitron.Z(a)),
    )


def test_freeze_not_relocate_moments():
    q = qubitron.q(0)
    c = qubitron.Circuit(qubitron.X(q), qubitron.measure(q))
    f = c.freeze()
    assert [mc is fc for mc, fc in zip(c, f)] == [True, True]


def test_freeze_is_cached():
    q = qubitron.q(0)
    c = qubitron.Circuit(qubitron.X(q), qubitron.measure(q))
    f0 = c.freeze()
    f1 = c.freeze()
    assert f1 is f0

    c.append(qubitron.Y(q))
    f2 = c.freeze()
    f3 = c.freeze()
    assert f2 is not f1
    assert f3 is f2

    c[-1] = qubitron.Moment(qubitron.Y(q))
    f4 = c.freeze()
    f5 = c.freeze()
    assert f4 is not f3
    assert f5 is f4


@pytest.mark.parametrize(
    "circuit, mutate",
    [
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.__setitem__(0, qubitron.Moment(qubitron.Y(qubitron.q(0)))),
        ),
        (qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))), lambda c: c.__delitem__(0)),
        (qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))), lambda c: c.__imul__(2)),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.insert(1, qubitron.Y(qubitron.q(0))),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.insert_into_range([qubitron.Y(qubitron.q(1)), qubitron.M(qubitron.q(1))], 0, 2),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.insert_at_frontier([qubitron.Y(qubitron.q(0)), qubitron.Y(qubitron.q(1))], 1),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.batch_replace([(0, qubitron.X(qubitron.q(0)), qubitron.Y(qubitron.q(0)))]),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0), qubitron.q(1))),
            lambda c: c.batch_insert_into([(0, qubitron.X(qubitron.q(1)))]),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.batch_insert([(1, qubitron.Y(qubitron.q(0)))]),
        ),
        (
            qubitron.Circuit(qubitron.X(qubitron.q(0)), qubitron.M(qubitron.q(0))),
            lambda c: c.clear_operations_touching([qubitron.q(0)], [0]),
        ),
    ],
)
def test_mutation_clears_cached_attributes(circuit, mutate):
    cached_attributes = [
        "_all_qubits",
        "_frozen",
        "_is_measurement",
        "_is_parameterized",
        "_parameter_names",
    ]

    for attr in cached_attributes:
        assert getattr(circuit, attr) is None, f"{attr=} is not None"

    # Check that attributes are cached after getting them.
    qubits = circuit.all_qubits()
    frozen = circuit.freeze()
    is_measurement = qubitron.is_measurement(circuit)
    is_parameterized = qubitron.is_parameterized(circuit)
    parameter_names = qubitron.parameter_names(circuit)

    for attr in cached_attributes:
        assert getattr(circuit, attr) is not None, f"{attr=} is None"

    # Check that getting again returns same object.
    assert circuit.all_qubits() is qubits
    assert circuit.freeze() is frozen
    assert qubitron.is_measurement(circuit) is is_measurement
    assert qubitron.is_parameterized(circuit) is is_parameterized
    assert qubitron.parameter_names(circuit) is parameter_names

    # Check that attributes are cleared after mutation.
    mutate(circuit)
    for attr in cached_attributes:
        assert getattr(circuit, attr) is None, f"{attr=} is not None"


def test_factorize_one_factor():
    circuit = qubitron.Circuit()
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit.append(
        [qubitron.Moment([qubitron.CZ(q0, q1), qubitron.H(q2)]), qubitron.Moment([qubitron.H(q0), qubitron.CZ(q1, q2)])]
    )
    factors = list(circuit.factorize())
    assert len(factors) == 1
    assert factors[0] == circuit
    desired = """
0: ───@───H───
      │
1: ───@───@───
          │
2: ───H───@───
"""
    qubitron.testing.assert_has_diagram(factors[0], desired)


def test_factorize_simple_circuit_two_factors():
    circuit = qubitron.Circuit()
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit.append([qubitron.H(q1), qubitron.CZ(q0, q1), qubitron.H(q2), qubitron.H(q0), qubitron.H(q0)])
    factors = list(circuit.factorize())
    assert len(factors) == 2
    desired = [
        """
0: ───────@───H───H───
          │
1: ───H───@───────────
""",
        """
2: ───H───────────────
""",
    ]
    for f, d in zip(factors, desired):
        qubitron.testing.assert_has_diagram(f, d)


def test_factorize_large_circuit():
    circuit = qubitron.Circuit()
    qubits = qubitron.GridQubit.rect(3, 3)
    circuit.append(qubitron.Moment(qubitron.X(q) for q in qubits))
    pairset = [[(0, 2), (4, 6)], [(1, 2), (4, 8)]]
    for pairs in pairset:
        circuit.append(qubitron.Moment(qubitron.CZ(qubits[a], qubits[b]) for (a, b) in pairs))
    circuit.append(qubitron.Moment(qubitron.Y(q) for q in qubits))
    # expect 5 factors
    factors = list(circuit.factorize())
    desired = [
        """
(0, 0): ───X───@───────Y───
               │
(0, 1): ───X───┼───@───Y───
               │   │
(0, 2): ───X───@───@───Y───
""",
        """
(1, 0): ───X───────────Y───
""",
        """
(1, 1): ───X───@───@───Y───
               │   │
(2, 0): ───X───@───┼───Y───
                   │
(2, 2): ───X───────@───Y───
""",
        """
(1, 2): ───X───────────Y───
""",
        """
(2, 1): ───X───────────Y───
    """,
    ]
    assert len(factors) == 5
    for f, d in zip(factors, desired):
        qubitron.testing.assert_has_diagram(f, d)


def test_zero_target_operations_go_below_diagram():
    class CustomOperationAnnotation(qubitron.Operation):
        def __init__(self, text: str):
            self.text = text

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            return ()

        def _circuit_diagram_info_(self, args) -> str:
            return self.text

    class CustomOperationAnnotationNoInfo(qubitron.Operation):
        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            return ()

        def __str__(self):
            return "custom!"

    class CustomGateAnnotation(qubitron.Gate):
        def __init__(self, text: str):
            self.text = text

        def _num_qubits_(self):
            return 0

        def _circuit_diagram_info_(self, args) -> str:
            return self.text

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.Moment(
                CustomOperationAnnotation("a"),
                CustomGateAnnotation("b").on(),
                CustomOperationAnnotation("c"),
            ),
            qubitron.Moment(CustomOperationAnnotation("e"), CustomOperationAnnotation("d")),
        ),
        """
    a   e
    b   d
    c
    """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(0)),
                CustomOperationAnnotation("a"),
                qubitron.global_phase_operation(1j),
            )
        ),
        """
0: ─────────────H──────

global phase:   0.5π
                a
    """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(0)),
                qubitron.CircuitOperation(qubitron.FrozenCircuit(CustomOperationAnnotation("a"))),
            )
        ),
        """
0: ───H───
      a
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.Moment(
                qubitron.X(qubitron.LineQubit(0)),
                CustomOperationAnnotation("a"),
                CustomGateAnnotation("b").on(),
                CustomOperationAnnotation("c"),
            ),
            qubitron.Moment(CustomOperationAnnotation("eee"), CustomOperationAnnotation("d")),
            qubitron.Moment(
                qubitron.CNOT(qubitron.LineQubit(0), qubitron.LineQubit(2)),
                qubitron.CNOT(qubitron.LineQubit(1), qubitron.LineQubit(3)),
                CustomOperationAnnotationNoInfo(),
                CustomOperationAnnotation("zzz"),
            ),
            qubitron.Moment(qubitron.H(qubitron.LineQubit(2))),
        ),
        """
                ┌────────┐
0: ───X──────────@───────────────
                 │
1: ──────────────┼──────@────────
                 │      │
2: ──────────────X──────┼────H───
                        │
3: ─────────────────────X────────
      a   eee    custom!
      b   d      zzz
      c
                └────────┘
    """,
    )


def test_create_speed():
    # Added in https://github.com/amyssnippet/Qubitron/pull/5332
    # Previously this took ~30s to run. Now it should take ~150ms. However the coverage test can
    # run this slowly, so allowing 4 sec to account for things like that. Feel free to increase the
    # buffer time or delete the test entirely if it ends up causing flakes.
    qs = 100
    moments = 500
    xs = [qubitron.X(qubitron.LineQubit(i)) for i in range(qs)]
    ops = [xs[i] for i in range(qs) for _ in range(moments)]
    t = time.perf_counter()
    c = qubitron.Circuit(ops)
    duration = time.perf_counter() - t
    assert len(c) == moments
    assert duration < 4


def test_append_speed():
    # Previously this took ~17s to run. Now it should take ~150ms. However the coverage test can
    # run this slowly, so allowing 5 sec to account for things like that. Feel free to increase the
    # buffer time or delete the test entirely if it ends up causing flakes.
    #
    # The `append` improvement mainly helps for deep circuits. It is less useful for wide circuits
    # because the Moment (immutable) needs verified and reconstructed each time an op is added.
    qs = 2
    moments = 10000
    xs = [qubitron.X(qubitron.LineQubit(i)) for i in range(qs)]
    c = qubitron.Circuit()
    t = time.perf_counter()
    # Iterating with the moments in the inner loop highlights the improvement: when filling in the
    # second qubit, we no longer have to search backwards from moment 10000 for a placement index.
    for q in range(qs):
        for _ in range(moments):
            c.append(xs[q])
    duration = time.perf_counter() - t
    assert len(c) == moments
    assert duration < 5
