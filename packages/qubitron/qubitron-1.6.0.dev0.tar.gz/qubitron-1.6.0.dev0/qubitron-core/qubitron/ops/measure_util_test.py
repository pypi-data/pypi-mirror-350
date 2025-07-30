# Copyright 2019 The Qubitron Developers
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

import qubitron


def test_measure_qubits():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    # Empty application.
    with pytest.raises(ValueError, match='empty set of qubits'):
        _ = qubitron.measure()

    with pytest.raises(ValueError, match='empty set of qubits'):
        _ = qubitron.measure([])

    assert qubitron.measure(a) == qubitron.MeasurementGate(num_qubits=1, key='a').on(a)
    assert qubitron.measure([a]) == qubitron.MeasurementGate(num_qubits=1, key='a').on(a)
    assert qubitron.measure(a, b) == qubitron.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    assert qubitron.measure([a, b]) == qubitron.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    qubit_generator = (q for q in (a, b))
    assert qubitron.measure(qubit_generator) == qubitron.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    assert qubitron.measure(b, a) == qubitron.MeasurementGate(num_qubits=2, key='b,a').on(b, a)
    assert qubitron.measure(a, key='b') == qubitron.MeasurementGate(num_qubits=1, key='b').on(a)
    assert qubitron.measure(a, invert_mask=(True,)) == qubitron.MeasurementGate(
        num_qubits=1, key='a', invert_mask=(True,)
    ).on(a)
    assert qubitron.measure(*qubitron.LineQid.for_qid_shape((1, 2, 3)), key='a') == qubitron.MeasurementGate(
        num_qubits=3, key='a', qid_shape=(1, 2, 3)
    ).on(*qubitron.LineQid.for_qid_shape((1, 2, 3)))
    assert qubitron.measure(qubitron.LineQid.for_qid_shape((1, 2, 3)), key='a') == qubitron.MeasurementGate(
        num_qubits=3, key='a', qid_shape=(1, 2, 3)
    ).on(*qubitron.LineQid.for_qid_shape((1, 2, 3)))
    cmap = {(0,): np.array([[0, 1], [1, 0]])}
    assert qubitron.measure(a, confusion_map=cmap) == qubitron.MeasurementGate(
        num_qubits=1, key='a', confusion_map=cmap
    ).on(a)

    with pytest.raises(ValueError, match='ndarray'):
        _ = qubitron.measure(np.array([1, 0]))

    with pytest.raises(ValueError, match='Qid'):
        _ = qubitron.measure("bork")

    with pytest.raises(ValueError, match='Qid'):
        _ = qubitron.measure([a, [b]])

    with pytest.raises(ValueError, match='Qid'):
        _ = qubitron.measure([a], [b])


def test_measure_each():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.measure_each() == []
    assert qubitron.measure_each([]) == []
    assert qubitron.measure_each(a) == [qubitron.measure(a)]
    assert qubitron.measure_each([a]) == [qubitron.measure(a)]
    assert qubitron.measure_each(a, b) == [qubitron.measure(a), qubitron.measure(b)]
    assert qubitron.measure_each([a, b]) == [qubitron.measure(a), qubitron.measure(b)]
    qubit_generator = (q for q in (a, b))
    assert qubitron.measure_each(qubit_generator) == [qubitron.measure(a), qubitron.measure(b)]
    assert qubitron.measure_each(a.with_dimension(3), b.with_dimension(3)) == [
        qubitron.measure(a.with_dimension(3)),
        qubitron.measure(b.with_dimension(3)),
    ]

    assert qubitron.measure_each(a, b, key_func=lambda e: e.name + '!') == [
        qubitron.measure(a, key='a!'),
        qubitron.measure(b, key='b!'),
    ]


def test_measure_single_paulistring():
    # Correct application
    q = qubitron.LineQubit.range(3)
    ps = qubitron.X(q[0]) * qubitron.Y(q[1]) * qubitron.Z(q[2])
    assert qubitron.measure_single_paulistring(ps, key='a') == qubitron.PauliMeasurementGate(
        ps.values(), key='a'
    ).on(*ps.keys())

    # Test with negative coefficient
    ps_neg = -qubitron.Y(qubitron.LineQubit(0)) * qubitron.Y(qubitron.LineQubit(1))
    assert qubitron.measure_single_paulistring(ps_neg, key='1').gate == qubitron.PauliMeasurementGate(
        qubitron.DensePauliString('YY', coefficient=-1), key='1'
    )

    # Empty application
    with pytest.raises(ValueError, match='should be an instance of qubitron.PauliString'):
        _ = qubitron.measure_single_paulistring(qubitron.I(q[0]) * qubitron.I(q[1]))

    # Wrong type
    with pytest.raises(ValueError, match='should be an instance of qubitron.PauliString'):
        _ = qubitron.measure_single_paulistring(q)

    # Coefficient != +1 or -1
    with pytest.raises(ValueError, match='must have a coefficient'):
        _ = qubitron.measure_single_paulistring(-2 * ps)


def test_measure_paulistring_terms():
    # Correct application
    q = qubitron.LineQubit.range(3)
    ps = qubitron.X(q[0]) * qubitron.Y(q[1]) * qubitron.Z(q[2])
    assert qubitron.measure_paulistring_terms(ps) == [
        qubitron.PauliMeasurementGate([qubitron.X], key=str(q[0])).on(q[0]),
        qubitron.PauliMeasurementGate([qubitron.Y], key=str(q[1])).on(q[1]),
        qubitron.PauliMeasurementGate([qubitron.Z], key=str(q[2])).on(q[2]),
    ]

    # Empty application
    with pytest.raises(ValueError, match='should be an instance of qubitron.PauliString'):
        _ = qubitron.measure_paulistring_terms(qubitron.I(q[0]) * qubitron.I(q[1]))

    # Wrong type
    with pytest.raises(ValueError, match='should be an instance of qubitron.PauliString'):
        _ = qubitron.measure_paulistring_terms(q)
