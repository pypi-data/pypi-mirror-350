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

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


def test_validation():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    d = qubitron.NamedQubit('d')

    _ = qubitron.Moment([])
    _ = qubitron.Moment([qubitron.X(a)])
    _ = qubitron.Moment([qubitron.CZ(a, b)])
    _ = qubitron.Moment([qubitron.CZ(b, d)])
    _ = qubitron.Moment([qubitron.CZ(a, b), qubitron.CZ(c, d)])
    _ = qubitron.Moment([qubitron.CZ(a, c), qubitron.CZ(b, d)])
    _ = qubitron.Moment([qubitron.CZ(a, c), qubitron.X(b)])

    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a), qubitron.X(a)])
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, c), qubitron.X(c)])
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, c), qubitron.CZ(c, d)])


def test_equality():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    d = qubitron.NamedQubit('d')

    eq = qubitron.testing.EqualsTester()

    # Default is empty. Iterables get frozen into tuples.
    eq.add_equality_group(qubitron.Moment(), qubitron.Moment([]), qubitron.Moment(()))
    eq.add_equality_group(qubitron.Moment([qubitron.X(d)]), qubitron.Moment((qubitron.X(d),)))

    # Equality depends on gate and qubits.
    eq.add_equality_group(qubitron.Moment([qubitron.X(a)]))
    eq.add_equality_group(qubitron.Moment([qubitron.X(b)]))
    eq.add_equality_group(qubitron.Moment([qubitron.Y(a)]))

    # Equality doesn't depend on order.
    eq.add_equality_group(qubitron.Moment([qubitron.X(a), qubitron.X(b)]), qubitron.Moment([qubitron.X(a), qubitron.X(b)]))

    # Two qubit gates.
    eq.make_equality_group(lambda: qubitron.Moment([qubitron.CZ(c, d)]))
    eq.make_equality_group(lambda: qubitron.Moment([qubitron.CZ(a, c)]))
    eq.make_equality_group(lambda: qubitron.Moment([qubitron.CZ(a, b), qubitron.CZ(c, d)]))
    eq.make_equality_group(lambda: qubitron.Moment([qubitron.CZ(a, c), qubitron.CZ(b, d)]))


def test_approx_eq():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert not qubitron.approx_eq(qubitron.Moment([qubitron.X(a)]), qubitron.X(a))

    # Default is empty. Iterables get frozen into tuples.
    assert qubitron.approx_eq(qubitron.Moment(), qubitron.Moment([]))
    assert qubitron.approx_eq(qubitron.Moment([]), qubitron.Moment(()))

    assert qubitron.approx_eq(qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(a)]))
    assert not qubitron.approx_eq(qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.X(b)]))

    assert qubitron.approx_eq(
        qubitron.Moment([qubitron.XPowGate(exponent=0)(a)]), qubitron.Moment([qubitron.XPowGate(exponent=1e-9)(a)])
    )
    assert not qubitron.approx_eq(
        qubitron.Moment([qubitron.XPowGate(exponent=0)(a)]), qubitron.Moment([qubitron.XPowGate(exponent=1e-7)(a)])
    )
    assert qubitron.approx_eq(
        qubitron.Moment([qubitron.XPowGate(exponent=0)(a)]),
        qubitron.Moment([qubitron.XPowGate(exponent=1e-7)(a)]),
        atol=1e-6,
    )


def test_operates_on_single_qubit():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # Empty case.
    assert not qubitron.Moment().operates_on_single_qubit(a)
    assert not qubitron.Moment().operates_on_single_qubit(b)

    # One-qubit operation case.
    assert qubitron.Moment([qubitron.X(a)]).operates_on_single_qubit(a)
    assert not qubitron.Moment([qubitron.X(a)]).operates_on_single_qubit(b)

    # Two-qubit operation case.
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on_single_qubit(a)
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on_single_qubit(b)
    assert not qubitron.Moment([qubitron.CZ(a, b)]).operates_on_single_qubit(c)

    # Multiple operations case.
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on_single_qubit(a)
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on_single_qubit(b)
    assert not qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on_single_qubit(c)


def test_operates_on():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # Empty case.
    assert not qubitron.Moment().operates_on([])
    assert not qubitron.Moment().operates_on([a])
    assert not qubitron.Moment().operates_on([b])
    assert not qubitron.Moment().operates_on([a, b])

    # One-qubit operation case.
    assert not qubitron.Moment([qubitron.X(a)]).operates_on([])
    assert qubitron.Moment([qubitron.X(a)]).operates_on([a])
    assert not qubitron.Moment([qubitron.X(a)]).operates_on([b])
    assert qubitron.Moment([qubitron.X(a)]).operates_on([a, b])

    # Two-qubit operation case.
    assert not qubitron.Moment([qubitron.CZ(a, b)]).operates_on([])
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on([a])
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on([b])
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on([a, b])
    assert not qubitron.Moment([qubitron.CZ(a, b)]).operates_on([c])
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on([a, c])
    assert qubitron.Moment([qubitron.CZ(a, b)]).operates_on([a, b, c])

    # Multiple operations case.
    assert not qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([])
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([a])
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([b])
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([a, b])
    assert not qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([c])
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([a, c])
    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).operates_on([a, b, c])


def test_operation_at():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # No operation on that qubit
    assert qubitron.Moment().operation_at(a) is None

    # One Operation on the quibt
    assert qubitron.Moment([qubitron.X(a)]).operation_at(a) == qubitron.X(a)

    # Multiple Operations on the qubits
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).operation_at(a) == qubitron.CZ(a, b)


def test_from_ops():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.Moment.from_ops(qubitron.X(a), qubitron.Y(b)) == qubitron.Moment(qubitron.X(a), qubitron.Y(b))


def test_with_operation():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.Moment().with_operation(qubitron.X(a)) == qubitron.Moment([qubitron.X(a)])

    assert qubitron.Moment([qubitron.X(a)]).with_operation(qubitron.X(b)) == qubitron.Moment([qubitron.X(a), qubitron.X(b)])

    # One-qubit operation case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a)]).with_operation(qubitron.X(a))

    # Two-qubit operation case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, b)]).with_operation(qubitron.X(a))
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, b)]).with_operation(qubitron.X(b))

    # Multiple operations case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a), qubitron.X(b)]).with_operation(qubitron.X(a))
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a), qubitron.X(b)]).with_operation(qubitron.X(b))


def test_with_operations():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    assert qubitron.Moment().with_operations(qubitron.X(a)) == qubitron.Moment([qubitron.X(a)])
    assert qubitron.Moment().with_operations(qubitron.X(a), qubitron.X(b)) == qubitron.Moment(
        [qubitron.X(a), qubitron.X(b)]
    )

    assert qubitron.Moment([qubitron.X(a)]).with_operations(qubitron.X(b)) == qubitron.Moment(
        [qubitron.X(a), qubitron.X(b)]
    )
    assert qubitron.Moment([qubitron.X(a)]).with_operations(qubitron.X(b), qubitron.X(c)) == qubitron.Moment(
        [qubitron.X(a), qubitron.X(b), qubitron.X(c)]
    )

    # One-qubit operation case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a)]).with_operations(qubitron.X(a))

    # Two-qubit operation case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, b)]).with_operations(qubitron.X(a))
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.CZ(a, b)]).with_operations(qubitron.X(b))

    # Multiple operations case.
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a), qubitron.X(b)]).with_operations(qubitron.X(a))
    with pytest.raises(ValueError):
        _ = qubitron.Moment([qubitron.X(a), qubitron.X(b)]).with_operations(qubitron.X(b))


def test_without_operations_touching():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # Empty case.
    assert qubitron.Moment().without_operations_touching([]) == qubitron.Moment()
    assert qubitron.Moment().without_operations_touching([a]) == qubitron.Moment()
    assert qubitron.Moment().without_operations_touching([a, b]) == qubitron.Moment()

    # One-qubit operation case.
    assert qubitron.Moment([qubitron.X(a)]).without_operations_touching([]) == qubitron.Moment([qubitron.X(a)])
    assert qubitron.Moment([qubitron.X(a)]).without_operations_touching([a]) == qubitron.Moment()
    assert qubitron.Moment([qubitron.X(a)]).without_operations_touching([b]) == qubitron.Moment([qubitron.X(a)])

    # Two-qubit operation case.
    assert qubitron.Moment([qubitron.CZ(a, b)]).without_operations_touching([]) == qubitron.Moment(
        [qubitron.CZ(a, b)]
    )
    assert qubitron.Moment([qubitron.CZ(a, b)]).without_operations_touching([a]) == qubitron.Moment()
    assert qubitron.Moment([qubitron.CZ(a, b)]).without_operations_touching([b]) == qubitron.Moment()
    assert qubitron.Moment([qubitron.CZ(a, b)]).without_operations_touching([c]) == qubitron.Moment(
        [qubitron.CZ(a, b)]
    )

    # Multiple operation case.
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching([]) == qubitron.Moment(
        [qubitron.CZ(a, b), qubitron.X(c)]
    )
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching([a]) == qubitron.Moment(
        [qubitron.X(c)]
    )
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching([b]) == qubitron.Moment(
        [qubitron.X(c)]
    )
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching([c]) == qubitron.Moment(
        [qubitron.CZ(a, b)]
    )
    assert qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching(
        [a, b]
    ) == qubitron.Moment([qubitron.X(c)])
    assert (
        qubitron.Moment([qubitron.CZ(a, b), qubitron.X(c)]).without_operations_touching([a, c]) == qubitron.Moment()
    )


def test_is_parameterized():
    a, b = qubitron.LineQubit.range(2)
    moment = qubitron.Moment(qubitron.X(a) ** sympy.Symbol('v'), qubitron.Y(b) ** sympy.Symbol('w'))
    assert qubitron.is_parameterized(moment)
    assert not qubitron.is_parameterized(qubitron.Moment(qubitron.X(a), qubitron.Y(b)))


def test_resolve_parameters():
    a, b = qubitron.LineQubit.range(2)
    moment = qubitron.Moment(qubitron.X(a) ** sympy.Symbol('v'), qubitron.Y(b) ** sympy.Symbol('w'))
    resolved_moment = qubitron.resolve_parameters(moment, qubitron.ParamResolver({'v': 0.1, 'w': 0.2}))
    assert resolved_moment == qubitron.Moment(qubitron.X(a) ** 0.1, qubitron.Y(b) ** 0.2)
    # sympy constant is resolved to a Python number
    moment = qubitron.Moment(qubitron.Rz(rads=sympy.pi).on(a))
    resolved_moment = qubitron.resolve_parameters(moment, {'pi': np.pi})
    assert resolved_moment == qubitron.Moment(qubitron.Rz(rads=np.pi).on(a))
    resolved_gate = resolved_moment.operations[0].gate
    assert not isinstance(resolved_gate.exponent, sympy.Basic)
    assert isinstance(resolved_gate.exponent, float)
    assert not qubitron.is_parameterized(resolved_moment)


def test_resolve_parameters_no_change():
    a, b = qubitron.LineQubit.range(2)
    moment = qubitron.Moment(qubitron.X(a), qubitron.Y(b))
    resolved_moment = qubitron.resolve_parameters(moment, qubitron.ParamResolver({'v': 0.1, 'w': 0.2}))
    assert resolved_moment is moment

    moment = qubitron.Moment(qubitron.X(a) ** sympy.Symbol('v'), qubitron.Y(b) ** sympy.Symbol('w'))
    resolved_moment = qubitron.resolve_parameters(moment, qubitron.ParamResolver({}))
    assert resolved_moment is moment


def test_parameter_names():
    a, b = qubitron.LineQubit.range(2)
    moment = qubitron.Moment(qubitron.X(a) ** sympy.Symbol('v'), qubitron.Y(b) ** sympy.Symbol('w'))
    assert qubitron.parameter_names(moment) == {'v', 'w'}
    assert qubitron.parameter_names(qubitron.Moment(qubitron.X(a), qubitron.Y(b))) == set()


def test_with_measurement_keys():
    a, b = qubitron.LineQubit.range(2)
    m = qubitron.Moment(qubitron.measure(a, key='m1'), qubitron.measure(b, key='m2'))

    new_moment = qubitron.with_measurement_key_mapping(m, {'m1': 'p1', 'm2': 'p2', 'x': 'z'})

    assert new_moment.operations[0] == qubitron.measure(a, key='p1')
    assert new_moment.operations[1] == qubitron.measure(b, key='p2')


def test_with_key_path():
    a, b = qubitron.LineQubit.range(2)
    m = qubitron.Moment(qubitron.measure(a, key='m1'), qubitron.measure(b, key='m2'))

    new_moment = qubitron.with_key_path(m, ('a', 'b'))

    assert new_moment.operations[0] == qubitron.measure(
        a, key=qubitron.MeasurementKey.parse_serialized('a:b:m1')
    )
    assert new_moment.operations[1] == qubitron.measure(
        b, key=qubitron.MeasurementKey.parse_serialized('a:b:m2')
    )


def test_with_key_path_prefix():
    a, b, c = qubitron.LineQubit.range(3)
    m = qubitron.Moment(qubitron.measure(a, key='m1'), qubitron.measure(b, key='m2'), qubitron.X(c))
    mb = qubitron.with_key_path_prefix(m, ('b',))
    mab = qubitron.with_key_path_prefix(mb, ('a',))
    assert mab.operations[0] == qubitron.measure(a, key=qubitron.MeasurementKey.parse_serialized('a:b:m1'))
    assert mab.operations[1] == qubitron.measure(b, key=qubitron.MeasurementKey.parse_serialized('a:b:m2'))
    assert mab.operations[2] is m.operations[2]


def test_copy():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    original = qubitron.Moment([qubitron.CZ(a, b)])
    copy = original.__copy__()
    assert original == copy
    assert id(original) != id(copy)


def test_qubits():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.Moment([qubitron.X(a), qubitron.X(b)]).qubits == {a, b}
    assert qubitron.Moment([qubitron.X(a)]).qubits == {a}
    assert qubitron.Moment([qubitron.CZ(a, b)]).qubits == {a, b}


def test_container_methods():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    m = qubitron.Moment([qubitron.H(a), qubitron.H(b)])
    assert list(m) == list(m.operations)
    # __iter__
    assert list(iter(m)) == list(m.operations)
    # __contains__ for free.
    assert qubitron.H(b) in m

    assert len(m) == 2


def test_decompose():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    m = qubitron.Moment(qubitron.X(a), qubitron.X(b))
    assert list(qubitron.decompose(m)) == list(m.operations)


def test_measurement_keys():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    m = qubitron.Moment(qubitron.X(a), qubitron.X(b))
    assert qubitron.measurement_key_names(m) == set()
    assert not qubitron.is_measurement(m)

    m2 = qubitron.Moment(qubitron.measure(a, b, key='foo'))
    assert qubitron.measurement_key_objs(m2) == {qubitron.MeasurementKey('foo')}
    assert qubitron.measurement_key_names(m2) == {'foo'}
    assert qubitron.is_measurement(m2)


def test_measurement_key_objs_caching():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    m = qubitron.Moment(qubitron.measure(q0, key='foo'))
    assert m._measurement_key_objs is None
    key_objs = qubitron.measurement_key_objs(m)
    assert m._measurement_key_objs == key_objs

    # Make sure it gets updated when adding an operation.
    m = m.with_operation(qubitron.measure(q1, key='bar'))
    assert m._measurement_key_objs == {
        qubitron.MeasurementKey(name='bar'),
        qubitron.MeasurementKey(name='foo'),
    }
    # Or multiple operations.
    m = m.with_operations(qubitron.measure(q2, key='doh'), qubitron.measure(q3, key='baz'))
    assert m._measurement_key_objs == {
        qubitron.MeasurementKey(name='bar'),
        qubitron.MeasurementKey(name='foo'),
        qubitron.MeasurementKey(name='doh'),
        qubitron.MeasurementKey(name='baz'),
    }


def test_control_keys_caching():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    m = qubitron.Moment(qubitron.X(q0).with_classical_controls('foo'))
    assert m._control_keys is None
    keys = qubitron.control_keys(m)
    assert m._control_keys == keys

    # Make sure it gets updated when adding an operation.
    m = m.with_operation(qubitron.X(q1).with_classical_controls('bar'))
    assert m._control_keys == {qubitron.MeasurementKey(name='bar'), qubitron.MeasurementKey(name='foo')}
    # Or multiple operations.
    m = m.with_operations(
        qubitron.X(q2).with_classical_controls('doh'), qubitron.X(q3).with_classical_controls('baz')
    )
    assert m._control_keys == {
        qubitron.MeasurementKey(name='bar'),
        qubitron.MeasurementKey(name='foo'),
        qubitron.MeasurementKey(name='doh'),
        qubitron.MeasurementKey(name='baz'),
    }


def test_bool():
    assert not qubitron.Moment()
    a = qubitron.NamedQubit('a')
    assert qubitron.Moment([qubitron.X(a)])


def test_repr():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    qubitron.testing.assert_equivalent_repr(qubitron.Moment())
    qubitron.testing.assert_equivalent_repr(qubitron.Moment(qubitron.CZ(a, b)))
    qubitron.testing.assert_equivalent_repr(qubitron.Moment(qubitron.X(a), qubitron.Y(b)))


def test_json_dict():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    mom = qubitron.Moment([qubitron.CZ(a, b)])
    assert mom._json_dict_() == {'operations': (qubitron.CZ(a, b),)}


def test_inverse():
    a, b, c = qubitron.LineQubit.range(3)
    m = qubitron.Moment([qubitron.S(a), qubitron.CNOT(b, c)])
    assert m**1 is m
    assert m**-1 == qubitron.Moment([qubitron.S(a) ** -1, qubitron.CNOT(b, c)])
    assert m**0.5 == qubitron.Moment([qubitron.T(a), qubitron.CNOT(b, c) ** 0.5])
    assert qubitron.inverse(m) == m**-1
    assert qubitron.inverse(qubitron.inverse(m)) == m
    assert qubitron.inverse(qubitron.Moment([qubitron.measure(a)]), default=None) is None


def test_immutable_moment():
    with pytest.raises(AttributeError):
        q1, q2 = qubitron.LineQubit.range(2)
        circuit = qubitron.Circuit(qubitron.X(q1))
        moment = circuit.moments[0]
        moment.operations += (qubitron.Y(q2),)


def test_add():
    a, b, c = qubitron.LineQubit.range(3)
    expected_circuit = qubitron.Circuit([qubitron.CNOT(a, b), qubitron.X(a), qubitron.Y(b)])

    circuit1 = qubitron.Circuit([qubitron.CNOT(a, b), qubitron.X(a)])
    circuit1[1] += qubitron.Y(b)
    assert circuit1 == expected_circuit

    circuit2 = qubitron.Circuit(qubitron.CNOT(a, b), qubitron.Y(b))
    circuit2[1] += qubitron.X(a)
    assert circuit2 == expected_circuit

    m1 = qubitron.Moment([qubitron.X(a)])
    m2 = qubitron.Moment([qubitron.CNOT(a, b)])
    m3 = qubitron.Moment([qubitron.X(c)])
    assert m1 + m3 == qubitron.Moment([qubitron.X(a), qubitron.X(c)])
    assert m2 + m3 == qubitron.Moment([qubitron.CNOT(a, b), qubitron.X(c)])
    with pytest.raises(ValueError, match='Overlap'):
        _ = m1 + m2

    assert m1 + [[[[qubitron.Y(b)]]]] == qubitron.Moment(qubitron.X(a), qubitron.Y(b))
    assert m1 + [] == m1
    assert m1 + [] is m1


def test_sub():
    a, b, c = qubitron.LineQubit.range(3)
    m = qubitron.Moment(qubitron.X(a), qubitron.Y(b))
    assert m - [] == m
    assert m - qubitron.X(a) == qubitron.Moment(qubitron.Y(b))
    assert m - [[[[qubitron.X(a)]], []]] == qubitron.Moment(qubitron.Y(b))
    assert m - [qubitron.X(a), qubitron.Y(b)] == qubitron.Moment()
    assert m - [qubitron.Y(b)] == qubitron.Moment(qubitron.X(a))

    with pytest.raises(ValueError, match="missing operations"):
        _ = m - qubitron.X(b)
    with pytest.raises(ValueError, match="missing operations"):
        _ = m - [qubitron.X(a), qubitron.Z(c)]

    # Preserves relative order.
    m2 = qubitron.Moment(qubitron.X(a), qubitron.Y(b), qubitron.Z(c))
    assert m2 - qubitron.Y(b) == qubitron.Moment(qubitron.X(a), qubitron.Z(c))


def test_op_tree():
    eq = qubitron.testing.EqualsTester()
    a, b = qubitron.LineQubit.range(2)

    eq.add_equality_group(qubitron.Moment(), qubitron.Moment([]), qubitron.Moment([[], [[[]]]]))

    eq.add_equality_group(
        qubitron.Moment(qubitron.X(a)), qubitron.Moment([qubitron.X(a)]), qubitron.Moment({qubitron.X(a)})
    )

    eq.add_equality_group(qubitron.Moment(qubitron.X(a), qubitron.Y(b)), qubitron.Moment([qubitron.X(a), qubitron.Y(b)]))


def test_indexes_by_qubit():
    a, b, c = qubitron.LineQubit.range(3)
    moment = qubitron.Moment([qubitron.H(a), qubitron.CNOT(b, c)])

    assert moment[a] == qubitron.H(a)
    assert moment[b] == qubitron.CNOT(b, c)
    assert moment[c] == qubitron.CNOT(b, c)


def test_throws_when_indexed_by_unused_qubit():
    a, b = qubitron.LineQubit.range(2)
    moment = qubitron.Moment([qubitron.H(a)])

    with pytest.raises(KeyError, match="Moment doesn't act on given qubit"):
        _ = moment[b]


def test_indexes_by_list_of_qubits():
    q = qubitron.LineQubit.range(4)
    moment = qubitron.Moment([qubitron.Z(q[0]), qubitron.CNOT(q[1], q[2])])

    assert moment[[q[0]]] == qubitron.Moment([qubitron.Z(q[0])])
    assert moment[[q[1]]] == qubitron.Moment([qubitron.CNOT(q[1], q[2])])
    assert moment[[q[2]]] == qubitron.Moment([qubitron.CNOT(q[1], q[2])])
    assert moment[[q[3]]] == qubitron.Moment([])
    assert moment[q[0:2]] == moment
    assert moment[q[1:3]] == qubitron.Moment([qubitron.CNOT(q[1], q[2])])
    assert moment[q[2:4]] == qubitron.Moment([qubitron.CNOT(q[1], q[2])])
    assert moment[[q[0], q[3]]] == qubitron.Moment([qubitron.Z(q[0])])
    assert moment[q] == moment


def test_moment_text_diagram():
    a, b, c, d = qubitron.GridQubit.rect(2, 2)
    m = qubitron.Moment(qubitron.CZ(a, b), qubitron.CNOT(c, d))
    assert (
        str(m).strip()
        == """
  ╷ 0 1
╶─┼─────
0 │ @─@
  │
1 │ @─X
  │
    """.strip()
    )

    m = qubitron.Moment(qubitron.CZ(a, b), qubitron.CNOT(c, d))
    qubitron.testing.assert_has_diagram(
        m,
        """
   ╷ None 0 1
╶──┼──────────
aa │
   │
0  │      @─@
   │
1  │      @─X
   │
        """,
        extra_qubits=[qubitron.NamedQubit("aa")],
    )

    m = qubitron.Moment(qubitron.S(c), qubitron.ISWAP(a, d))
    qubitron.testing.assert_has_diagram(
        m,
        """
  ╷ 0     1
╶─┼─────────────
0 │ iSwap─┐
  │       │
1 │ S     iSwap
  │
    """,
    )

    m = qubitron.Moment(qubitron.S(c) ** 0.1, qubitron.ISWAP(a, d) ** 0.5)
    qubitron.testing.assert_has_diagram(
        m,
        """
  ╷ 0         1
╶─┼─────────────────
0 │ iSwap^0.5─┐
  │           │
1 │ Z^0.05    iSwap
  │
    """,
    )

    a, b, c = qubitron.LineQubit.range(3)
    m = qubitron.Moment(qubitron.X(a), qubitron.SWAP(b, c))
    qubitron.testing.assert_has_diagram(
        m,
        """
  ╷ a b c
╶─┼───────
0 │ X
  │
1 │   ×─┐
  │     │
2 │     ×
  │
    """,
        xy_breakdown_func=lambda q: ('abc'[q.x], q.x),
    )

    class EmptyGate(qubitron.testing.SingleQubitGate):
        def __str__(self):
            return 'Empty'

    m = qubitron.Moment(EmptyGate().on(a))
    qubitron.testing.assert_has_diagram(
        m,
        """
  ╷ 0
╶─┼───────
0 │ Empty
  │
    """,
    )


def test_text_diagram_does_not_depend_on_insertion_order():
    q = qubitron.LineQubit.range(4)
    ops = [qubitron.CNOT(q[0], q[3]), qubitron.CNOT(q[1], q[2])]
    m1, m2 = qubitron.Moment(ops), qubitron.Moment(ops[::-1])
    assert m1 == m2
    assert str(m1) == str(m2)


def test_commutes_moment_and_operation():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    d = qubitron.NamedQubit('d')

    moment = qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.H(c)])

    assert qubitron.commutes(moment, a, default=None) is None

    assert qubitron.commutes(moment, qubitron.X(a))
    assert qubitron.commutes(moment, qubitron.Y(b))
    assert qubitron.commutes(moment, qubitron.H(c))
    assert qubitron.commutes(moment, qubitron.H(d))

    # X and H do not commute
    assert not qubitron.commutes(moment, qubitron.H(a))
    assert not qubitron.commutes(moment, qubitron.H(b))
    assert not qubitron.commutes(moment, qubitron.X(c))

    # Empty moment commutes with everything
    moment = qubitron.Moment()
    assert qubitron.commutes(moment, qubitron.X(a))
    assert qubitron.commutes(moment, qubitron.measure(b))

    # Two qubit operation
    moment = qubitron.Moment(qubitron.Z(a), qubitron.Z(b))
    assert qubitron.commutes(moment, qubitron.XX(a, b))


def test_commutes_moment_and_moment():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # Test cases where individual operations don't commute but moments do
    # Two Z gates (Z⊗Z) commutes with RXX even though individual Z's don't
    assert not qubitron.commutes(qubitron.Moment(qubitron.Z(a)), qubitron.Moment(qubitron.XX(a, b)))
    assert qubitron.commutes(qubitron.Moment(qubitron.Z(a), qubitron.Z(b)), qubitron.Moment(qubitron.XX(a, b)))

    # Moments that do not commute if acting on same qubits
    assert qubitron.commutes(qubitron.Moment(qubitron.X(a)), qubitron.Moment(qubitron.Y(b)))
    assert not qubitron.commutes(qubitron.Moment(qubitron.X(a)), qubitron.Moment(qubitron.Y(a)))

    # Moments commute with themselves
    assert qubitron.commutes(
        qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.H(c)]),
        qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.H(c)]),
    )


def test_commutes_moment_with_controls():
    a, b = qubitron.LineQubit.range(2)
    assert qubitron.commutes(
        qubitron.Moment(qubitron.measure(a, key='k0')), qubitron.Moment(qubitron.X(b).with_classical_controls('k1'))
    )
    assert qubitron.commutes(
        qubitron.Moment(qubitron.X(b).with_classical_controls('k1')), qubitron.Moment(qubitron.measure(a, key='k0'))
    )
    assert qubitron.commutes(
        qubitron.Moment(qubitron.X(a).with_classical_controls('k0')),
        qubitron.Moment(qubitron.H(b).with_classical_controls('k0')),
    )
    assert qubitron.commutes(
        qubitron.Moment(qubitron.X(a).with_classical_controls('k0')),
        qubitron.Moment(qubitron.X(a).with_classical_controls('k0')),
    )
    assert not qubitron.commutes(
        qubitron.Moment(qubitron.measure(a, key='k0')), qubitron.Moment(qubitron.X(b).with_classical_controls('k0'))
    )
    assert not qubitron.commutes(
        qubitron.Moment(qubitron.X(b).with_classical_controls('k0')), qubitron.Moment(qubitron.measure(a, key='k0'))
    )
    assert not qubitron.commutes(
        qubitron.Moment(qubitron.X(a).with_classical_controls('k0')),
        qubitron.Moment(qubitron.H(a).with_classical_controls('k0')),
    )


def test_commutes_moment_and_moment_comprehensive():
    a, b, c, d = qubitron.LineQubit.range(4)

    # Basic Z⊗Z commuting with XX at different angles
    m1 = qubitron.Moment([qubitron.Z(a), qubitron.Z(b)])
    m2 = qubitron.Moment([qubitron.XXPowGate(exponent=0.5)(a, b)])
    assert qubitron.commutes(m1, m2)

    # Disjoint qubit sets
    m1 = qubitron.Moment([qubitron.X(a), qubitron.Y(b)])
    m2 = qubitron.Moment([qubitron.Z(c), qubitron.H(d)])
    assert qubitron.commutes(m1, m2)

    # Mixed case - some commute individually, some as group
    m1 = qubitron.Moment([qubitron.Z(a), qubitron.Z(b), qubitron.X(c)])
    m2 = qubitron.Moment([qubitron.XXPowGate(exponent=0.5)(a, b), qubitron.X(c)])
    assert qubitron.commutes(m1, m2)

    # Non-commuting case: X on first qubit, Z on second with XX gate
    m1 = qubitron.Moment([qubitron.X(a), qubitron.Z(b)])
    m2 = qubitron.Moment([qubitron.XX(a, b)])
    assert not qubitron.commutes(m1, m2)

    # Complex case requiring unitary calculation - non-commuting case
    m1 = qubitron.Moment([qubitron.Z(a), qubitron.Z(b), qubitron.Z(c)])
    m2 = qubitron.Moment([qubitron.XXPowGate(exponent=0.5)(a, b), qubitron.X(c)])
    assert not qubitron.commutes(m1, m2)  # Z⊗Z⊗Z doesn't commute with XX⊗X


def test_commutes_handles_non_unitary_operation():
    a = qubitron.NamedQubit('a')
    op_damp_a = qubitron.AmplitudeDampingChannel(gamma=0.1).on(a)
    assert qubitron.commutes(qubitron.Moment(qubitron.X(a)), op_damp_a, default=None) is None
    assert qubitron.commutes(qubitron.Moment(qubitron.X(a)), qubitron.Moment(op_damp_a), default=None) is None
    assert qubitron.commutes(qubitron.Moment(op_damp_a), qubitron.Moment(op_damp_a))


def test_transform_qubits():
    a, b = qubitron.LineQubit.range(2)
    x, y = qubitron.GridQubit.rect(2, 1, 10, 20)

    original = qubitron.Moment([qubitron.X(a), qubitron.Y(b)])
    modified = qubitron.Moment([qubitron.X(x), qubitron.Y(y)])

    assert original.transform_qubits({a: x, b: y}) == modified
    assert original.transform_qubits(lambda q: qubitron.GridQubit(10 + q.x, 20)) == modified
    with pytest.raises(TypeError, match='must be a function or dict'):
        _ = original.transform_qubits('bad arg')


def test_expand_to():
    a, b = qubitron.LineQubit.range(2)
    m1 = qubitron.Moment(qubitron.H(a))
    m2 = m1.expand_to({a})
    assert m1 == m2

    m3 = m1.expand_to({a, b})
    assert m1 != m3
    assert m3.qubits == {a, b}
    assert m3.operations == (qubitron.H(a), qubitron.I(b))

    with pytest.raises(ValueError, match='superset'):
        _ = m1.expand_to({b})


def test_kraus():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.diag([1, -1])

    a, b = qubitron.LineQubit.range(2)

    m = qubitron.Moment()
    assert qubitron.has_kraus(m)
    k = qubitron.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.array([[1.0]]))

    m = qubitron.Moment(qubitron.S(a))
    assert qubitron.has_kraus(m)
    k = qubitron.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.diag([1, 1j]))

    m = qubitron.Moment(qubitron.CNOT(a, b))
    assert qubitron.has_kraus(m)
    k = qubitron.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))

    p = 0.1
    m = qubitron.Moment(qubitron.depolarize(p).on(a))
    assert qubitron.has_kraus(m)
    k = qubitron.kraus(m)
    assert len(k) == 4
    assert np.allclose(k[0], np.sqrt(1 - p) * I)
    assert np.allclose(k[1], np.sqrt(p / 3) * X)
    assert np.allclose(k[2], np.sqrt(p / 3) * Y)
    assert np.allclose(k[3], np.sqrt(p / 3) * Z)

    p = 0.2
    q = 0.3
    m = qubitron.Moment(qubitron.bit_flip(p).on(a), qubitron.phase_flip(q).on(b))
    assert qubitron.has_kraus(m)
    k = qubitron.kraus(m)
    assert len(k) == 4
    assert np.allclose(k[0], np.sqrt((1 - p) * (1 - q)) * np.kron(I, I))
    assert np.allclose(k[1], np.sqrt(q * (1 - p)) * np.kron(I, Z))
    assert np.allclose(k[2], np.sqrt(p * (1 - q)) * np.kron(X, I))
    assert np.allclose(k[3], np.sqrt(p * q) * np.kron(X, Z))


def test_kraus_too_big():
    m = qubitron.Moment(qubitron.IdentityGate(11).on(*qubitron.LineQubit.range(11)))
    assert not qubitron.has_kraus(m)
    assert not m._has_superoperator_()
    assert m._kraus_() is NotImplemented
    assert m._superoperator_() is NotImplemented
    assert qubitron.kraus(m, default=None) is None


def test_op_has_no_kraus():
    class EmptyGate(qubitron.testing.SingleQubitGate):
        pass

    m = qubitron.Moment(EmptyGate().on(qubitron.NamedQubit("a")))
    assert not qubitron.has_kraus(m)
    assert not m._has_superoperator_()
    assert m._kraus_() is NotImplemented
    assert m._superoperator_() is NotImplemented
    assert qubitron.kraus(m, default=None) is None


def test_superoperator():
    cnot = qubitron.unitary(qubitron.CNOT)

    a, b = qubitron.LineQubit.range(2)

    m = qubitron.Moment()
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.array([[1.0]]))

    m = qubitron.Moment(qubitron.I(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.eye(4))

    m = qubitron.Moment(qubitron.IdentityGate(2).on(a, b))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.eye(16))

    m = qubitron.Moment(qubitron.S(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.diag([1, -1j, 1j, 1]))

    m = qubitron.Moment(qubitron.CNOT(a, b))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.kron(cnot, cnot))

    m = qubitron.Moment(qubitron.depolarize(0.75).on(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.array([[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]]) / 2)
