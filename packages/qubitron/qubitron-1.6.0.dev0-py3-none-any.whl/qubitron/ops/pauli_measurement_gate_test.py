# Copyright 2021 The Qubitron Developers
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

import pytest

import qubitron


@pytest.mark.parametrize(
    'key',
    ['q0_1_0', qubitron.MeasurementKey(name='q0_1_0'), qubitron.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_eval_repr(key):
    # Basic safeguard against repr-inequality.
    op = qubitron.GateOperation(
        gate=qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y], key),
        qubits=[qubitron.GridQubit(0, 1), qubitron.GridQubit(1, 1)],
    )
    qubitron.testing.assert_equivalent_repr(op)
    assert qubitron.is_measurement(op)
    assert qubitron.measurement_key_name(op) == str(key)


@pytest.mark.parametrize('observable', [[qubitron.X], [qubitron.Y, qubitron.Z], qubitron.DensePauliString('XYZ')])
@pytest.mark.parametrize('key', ['a', qubitron.MeasurementKey('a')])
def test_init(observable, key):
    g = qubitron.PauliMeasurementGate(observable, key)
    assert g.num_qubits() == len(observable)
    assert g.key == 'a'
    assert g.mkey == qubitron.MeasurementKey('a')
    assert g._observable == qubitron.DensePauliString(observable)
    assert qubitron.qid_shape(g) == (2,) * len(observable)


def test_measurement_has_unitary_returns_false():
    gate = qubitron.PauliMeasurementGate([qubitron.X], 'a')
    assert not qubitron.has_unitary(gate)


def test_measurement_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(
        lambda: qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y], 'a'),
        lambda: qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y], qubitron.MeasurementKey('a')),
    )
    eq.add_equality_group(qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y], 'b'))
    eq.add_equality_group(qubitron.PauliMeasurementGate([qubitron.Y, qubitron.X], 'a'))


@pytest.mark.parametrize(
    'protocol,args,key',
    [
        (None, None, 'b'),
        (qubitron.with_key_path, ('p', 'q'), 'p:q:a'),
        (qubitron.with_key_path_prefix, ('p', 'q'), 'p:q:a'),
        (qubitron.with_measurement_key_mapping, {'a': 'b'}, 'b'),
    ],
)
@pytest.mark.parametrize(
    'gate',
    [
        qubitron.PauliMeasurementGate([qubitron.X], 'a'),
        qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y, qubitron.Z], 'a'),
    ],
)
def test_measurement_with_key(protocol, args, key, gate):
    if protocol:
        gate_with_key = protocol(gate, args)
    else:
        gate_with_key = gate.with_key('b')
    assert gate_with_key.key == key
    assert gate_with_key.num_qubits() == gate.num_qubits()
    assert gate_with_key.observable() == gate.observable()
    assert qubitron.qid_shape(gate_with_key) == qubitron.qid_shape(gate)
    if protocol:
        same_gate = qubitron.with_measurement_key_mapping(gate, {'a': 'a'})
    else:
        same_gate = gate.with_key('a')
    assert same_gate == gate


def test_measurement_gate_diagram():
    # Shows observable & key.
    assert qubitron.circuit_diagram_info(
        qubitron.PauliMeasurementGate([qubitron.X], key='test')
    ) == qubitron.CircuitDiagramInfo(("M(X)('test')",))

    # Shows multiple observables.
    assert qubitron.circuit_diagram_info(
        qubitron.PauliMeasurementGate([qubitron.X, qubitron.Y, qubitron.Z], 'a')
    ) == qubitron.CircuitDiagramInfo(("M(X)('a')", 'M(Y)', 'M(Z)'))

    # Omits key when it is the default.
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure_single_paulistring(qubitron.X(a) * qubitron.Y(b))),
        """
a: ───M(X)───
      │
b: ───M(Y)───
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure_single_paulistring(qubitron.X(a) * qubitron.Y(b), key='test')),
        """
a: ───M(X)('test')───
      │
b: ───M(Y)───────────
""",
    )


@pytest.mark.parametrize('observable', [[qubitron.X], [qubitron.X, qubitron.Y, qubitron.Z]])
@pytest.mark.parametrize(
    'key',
    ['q0_1_0', qubitron.MeasurementKey(name='q0_1_0'), qubitron.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_consistent_protocols(observable, key):
    gate = qubitron.PauliMeasurementGate(observable, key=key)
    qubitron.testing.assert_implements_consistent_protocols(gate)
    assert qubitron.is_measurement(gate)
    assert qubitron.measurement_key_name(gate) == str(key)


def test_op_repr():
    a, b, c = qubitron.LineQubit.range(3)
    ps = qubitron.X(a) * qubitron.Y(b) * qubitron.Z(c)
    assert (
        repr(qubitron.measure_single_paulistring(ps))
        == 'qubitron.measure_single_paulistring(((1+0j)*qubitron.X(qubitron.LineQubit(0))'
        '*qubitron.Y(qubitron.LineQubit(1))*qubitron.Z(qubitron.LineQubit(2))))'
    )
    assert (
        repr(qubitron.measure_single_paulistring(ps, key='out'))
        == "qubitron.measure_single_paulistring(((1+0j)*qubitron.X(qubitron.LineQubit(0))"
        "*qubitron.Y(qubitron.LineQubit(1))*qubitron.Z(qubitron.LineQubit(2))), "
        "key=qubitron.MeasurementKey(name='out'))"
    )


def test_bad_observable_raises():
    with pytest.raises(ValueError, match='Pauli observable .* is empty'):
        _ = qubitron.PauliMeasurementGate([])

    with pytest.raises(ValueError, match=r'Pauli observable .* must be Iterable\[`qubitron.Pauli`\]'):
        _ = qubitron.PauliMeasurementGate([qubitron.I, qubitron.X, qubitron.Y])

    with pytest.raises(ValueError, match=r'Pauli observable .* must be Iterable\[`qubitron.Pauli`\]'):
        _ = qubitron.PauliMeasurementGate(qubitron.DensePauliString('XYZI'))

    with pytest.raises(ValueError, match=r'must have coefficient \+1/-1.'):
        _ = qubitron.PauliMeasurementGate(qubitron.DensePauliString('XYZ', coefficient=1j))


def test_with_observable():
    o1 = [qubitron.Z, qubitron.Y, qubitron.X]
    o2 = [qubitron.X, qubitron.Y, qubitron.Z]
    g1 = qubitron.PauliMeasurementGate(o1, key='a')
    g2 = qubitron.PauliMeasurementGate(o2, key='a')
    assert g1.with_observable(o2) == g2
    assert g1.with_observable(o1) is g1


@pytest.mark.parametrize(
    'rot, obs, out',
    [
        (qubitron.I, qubitron.DensePauliString("Z", coefficient=+1), 0),
        (qubitron.I, qubitron.DensePauliString("Z", coefficient=-1), 1),
        (qubitron.Y**0.5, qubitron.DensePauliString("X", coefficient=+1), 0),
        (qubitron.Y**0.5, qubitron.DensePauliString("X", coefficient=-1), 1),
        (qubitron.X**-0.5, qubitron.DensePauliString("Y", coefficient=+1), 0),
        (qubitron.X**-0.5, qubitron.DensePauliString("Y", coefficient=-1), 1),
    ],
)
def test_pauli_measurement_gate_samples(rot, obs, out):
    q = qubitron.NamedQubit("q")
    c = qubitron.Circuit(rot(q), qubitron.PauliMeasurementGate(obs, key='out').on(q))
    assert qubitron.Simulator().sample(c)['out'][0] == out
