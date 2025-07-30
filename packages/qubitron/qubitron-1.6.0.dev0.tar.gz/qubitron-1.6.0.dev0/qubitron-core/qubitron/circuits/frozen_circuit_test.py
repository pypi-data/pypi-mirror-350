# Copyright 2020 The Qubitron Developers
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
"""Tests exclusively for FrozenCircuits.

Behavior shared with Circuit is tested with parameters in circuit_test.py.
"""

from __future__ import annotations

import pytest
import sympy

import qubitron


def test_from_moments():
    a, b, c, d = qubitron.LineQubit.range(4)
    moment = qubitron.Moment(qubitron.Z(a), qubitron.Z(b))
    subcircuit = qubitron.FrozenCircuit.from_moments(qubitron.X(c), qubitron.Y(d))
    circuit = qubitron.FrozenCircuit.from_moments(
        moment,
        subcircuit,
        [qubitron.X(a), qubitron.Y(b)],
        [qubitron.X(c)],
        [],
        qubitron.Z(d),
        [qubitron.measure(a, b, key='ab'), qubitron.measure(c, d, key='cd')],
    )
    assert circuit == qubitron.FrozenCircuit(
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


def test_freeze_and_unfreeze():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(a), qubitron.H(b))

    f = c.freeze()
    # Circuits equal their frozen versions, similar to set(x) == frozenset(x).
    assert f == c
    assert qubitron.approx_eq(f, c)

    # Freezing a FrozenCircuit will return the original.
    ff = f.freeze()
    assert ff is f

    unf = f.unfreeze()
    assert unf.moments == c.moments
    assert unf is not c

    # Unfreezing always returns a copy.
    cc = c.unfreeze()
    assert cc is not c

    fcc = cc.freeze()
    assert fcc.moments == f.moments
    assert fcc is not f


def test_immutable():
    q = qubitron.LineQubit(0)
    c = qubitron.FrozenCircuit(qubitron.X(q), qubitron.H(q))

    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'moments' of 'FrozenCircuit' object has no setter)",
    ):
        c.moments = (qubitron.Moment(qubitron.H(q)), qubitron.Moment(qubitron.X(q)))


def test_tagged_circuits():
    q = qubitron.LineQubit(0)
    ops = [qubitron.X(q), qubitron.H(q)]
    tags = [sympy.Symbol("a"), "b"]
    circuit = qubitron.Circuit(ops)
    frozen_circuit = qubitron.FrozenCircuit(ops)
    tagged_circuit = qubitron.FrozenCircuit(ops, tags=tags)
    # Test equality
    assert tagged_circuit.tags == tuple(tags)
    assert circuit == frozen_circuit != tagged_circuit
    assert qubitron.approx_eq(circuit, frozen_circuit)
    assert qubitron.approx_eq(frozen_circuit, tagged_circuit)
    # Test hash
    assert hash(frozen_circuit) != hash(tagged_circuit)
    # Test _repr_ and _json_ round trips.
    qubitron.testing.assert_equivalent_repr(tagged_circuit)
    qubitron.testing.assert_json_roundtrip_works(tagged_circuit)
    # Test utility methods and constructors
    assert frozen_circuit.with_tags() is frozen_circuit
    assert frozen_circuit.with_tags(*tags) == tagged_circuit
    assert tagged_circuit.with_tags("c") == qubitron.FrozenCircuit(ops, tags=[*tags, "c"])
    assert tagged_circuit.untagged == frozen_circuit
    assert frozen_circuit.untagged is frozen_circuit
    # Test parameterized protocols
    assert qubitron.is_parameterized(frozen_circuit) is False
    assert qubitron.is_parameterized(tagged_circuit) is True
    assert qubitron.parameter_names(tagged_circuit) == {"a"}
    # Tags are not propagated to diagrams yet.
    assert str(frozen_circuit) == str(tagged_circuit)
