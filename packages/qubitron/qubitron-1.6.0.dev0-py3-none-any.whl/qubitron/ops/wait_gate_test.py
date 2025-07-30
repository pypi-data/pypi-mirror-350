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

import datetime

import pytest
import sympy

import qubitron


def test_init():
    g = qubitron.WaitGate(datetime.timedelta(0, 0, 5))
    assert g.duration == qubitron.Duration(micros=5)

    g = qubitron.WaitGate(qubitron.Duration(nanos=4))
    assert g.duration == qubitron.Duration(nanos=4)

    g = qubitron.WaitGate(0)
    assert g.duration == qubitron.Duration(0)

    with pytest.raises(ValueError, match='duration < 0'):
        _ = qubitron.WaitGate(qubitron.Duration(nanos=-4))

    with pytest.raises(TypeError, match='Not a `qubitron.DURATION_LIKE`'):
        _ = qubitron.WaitGate(2)


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.WaitGate(0), qubitron.WaitGate(qubitron.Duration()))
    eq.make_equality_group(lambda: qubitron.WaitGate(qubitron.Duration(nanos=4)))


def test_protocols():
    t = sympy.Symbol('t')
    p = qubitron.WaitGate(qubitron.Duration(millis=5 * t))
    c = qubitron.WaitGate(qubitron.Duration(millis=2))
    q = qubitron.LineQubit(0)

    qubitron.testing.assert_implements_consistent_protocols(qubitron.wait(q, nanos=0))
    qubitron.testing.assert_implements_consistent_protocols(c.on(q))
    qubitron.testing.assert_implements_consistent_protocols(p.on(q))

    assert qubitron.has_unitary(p)
    assert qubitron.has_unitary(c)
    assert qubitron.is_parameterized(p)
    assert not qubitron.is_parameterized(c)
    assert qubitron.resolve_parameters(p, {'t': 2}) == qubitron.WaitGate(qubitron.Duration(millis=10))
    assert qubitron.resolve_parameters(c, {'t': 2}) == c
    assert qubitron.resolve_parameters_once(c, {'t': 2}) == c
    assert qubitron.trace_distance_bound(p) == 0
    assert qubitron.trace_distance_bound(c) == 0
    assert qubitron.inverse(c) == c
    assert qubitron.inverse(p) == p
    assert qubitron.decompose(c.on(q)) == []
    assert qubitron.decompose(p.on(q)) == []


def test_qid_shape():
    assert qubitron.qid_shape(qubitron.WaitGate(0, qid_shape=(2, 3))) == (2, 3)
    assert qubitron.qid_shape(qubitron.WaitGate(0, num_qubits=3)) == (2, 2, 2)
    with pytest.raises(ValueError, match='empty set of qubits'):
        qubitron.WaitGate(0, num_qubits=0)
    with pytest.raises(ValueError, match='num_qubits'):
        qubitron.WaitGate(0, qid_shape=(2, 2), num_qubits=1)


@pytest.mark.parametrize('num_qubits', [1, 2, 3])
def test_resolve_parameters(num_qubits: int) -> None:
    gate = qubitron.WaitGate(duration=qubitron.Duration(nanos=sympy.Symbol('t_ns')), num_qubits=num_qubits)
    resolved = qubitron.resolve_parameters(gate, {'t_ns': 10})
    assert resolved.duration == qubitron.Duration(nanos=10)
    assert qubitron.num_qubits(resolved) == num_qubits


def test_json():
    q0, q1 = qubitron.GridQubit.rect(1, 2)
    qtrit = qubitron.GridQid(1, 2, dimension=3)
    qubitron.testing.assert_json_roundtrip_works(qubitron.wait(q0, nanos=10))
    qubitron.testing.assert_json_roundtrip_works(qubitron.wait(q0, q1, nanos=10))
    qubitron.testing.assert_json_roundtrip_works(qubitron.wait(qtrit, nanos=10))
    qubitron.testing.assert_json_roundtrip_works(qubitron.wait(qtrit, q1, nanos=10))


def test_str():
    assert str(qubitron.WaitGate(qubitron.Duration(nanos=5))) == 'WaitGate(5 ns)'
