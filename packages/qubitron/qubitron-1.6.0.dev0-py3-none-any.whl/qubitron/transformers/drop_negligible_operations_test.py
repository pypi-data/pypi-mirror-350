# Copyright 2022 The Qubitron Developers
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

import qubitron

NO_COMPILE_TAG = "no_compile_tag"


def test_leaves_big():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.Moment(qubitron.Z(a) ** 0.1))
    qubitron.testing.assert_same_circuits(qubitron.drop_negligible_operations(circuit, atol=0.001), circuit)


def test_clears_small():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.Moment(qubitron.Z(a) ** 0.000001))
    qubitron.testing.assert_same_circuits(
        qubitron.drop_negligible_operations(circuit, atol=0.001), qubitron.Circuit(qubitron.Moment())
    )


def test_does_not_clear_small_no_compile():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.Moment((qubitron.Z(a) ** 0.000001).with_tags(NO_COMPILE_TAG)))
    qubitron.testing.assert_same_circuits(
        qubitron.drop_negligible_operations(
            circuit, context=qubitron.TransformerContext(tags_to_ignore=(NO_COMPILE_TAG,)), atol=0.001
        ),
        circuit,
    )


def test_clears_known_empties_even_at_zero_tolerance():
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.Z(a) ** 0, qubitron.Y(a) ** 0.0000001, qubitron.X(a) ** -0.0000001, qubitron.CZ(a, b) ** 0
    )
    qubitron.testing.assert_same_circuits(
        qubitron.drop_negligible_operations(circuit, atol=0.001), qubitron.Circuit([qubitron.Moment()] * 4)
    )
    qubitron.testing.assert_same_circuits(
        qubitron.drop_negligible_operations(circuit, atol=0),
        qubitron.Circuit(
            qubitron.Moment(),
            qubitron.Moment(qubitron.Y(a) ** 0.0000001),
            qubitron.Moment(qubitron.X(a) ** -0.0000001),
            qubitron.Moment(),
        ),
    )


def test_recursively_runs_inside_circuit_ops_deep():
    a = qubitron.NamedQubit('a')
    small_op = qubitron.Z(a) ** 0.000001
    nested_circuit = qubitron.FrozenCircuit(
        qubitron.X(a), small_op, small_op.with_tags(NO_COMPILE_TAG), small_op, qubitron.Y(a)
    )
    nested_circuit_dropped = qubitron.FrozenCircuit(
        qubitron.Moment(qubitron.X(a)),
        qubitron.Moment(),
        qubitron.Moment(small_op.with_tags(NO_COMPILE_TAG)),
        qubitron.Moment(),
        qubitron.Moment(qubitron.Y(a)),
    )
    c_orig = qubitron.Circuit(
        small_op,
        qubitron.CircuitOperation(nested_circuit).repeat(6).with_tags(NO_COMPILE_TAG),
        small_op,
        qubitron.CircuitOperation(nested_circuit).repeat(5).with_tags("preserve_tag"),
        small_op,
    )
    c_expected = qubitron.Circuit(
        qubitron.Moment(),
        qubitron.Moment(qubitron.CircuitOperation(nested_circuit).repeat(6).with_tags(NO_COMPILE_TAG)),
        qubitron.Moment(),
        qubitron.Moment(
            qubitron.CircuitOperation(nested_circuit_dropped).repeat(5).with_tags("preserve_tag")
        ),
        qubitron.Moment(),
    )
    context = qubitron.TransformerContext(tags_to_ignore=[NO_COMPILE_TAG], deep=True)
    qubitron.testing.assert_same_circuits(
        qubitron.drop_negligible_operations(c_orig, context=context, atol=0.001), c_expected
    )


def test_ignores_large_ops():
    qnum = 20
    qubits = qubitron.LineQubit.range(qnum)
    subcircuit = qubitron.FrozenCircuit(qubitron.X.on_each(*qubits))
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(subcircuit).repeat(10), qubitron.measure(*qubits, key='out')
    )
    qubitron.testing.assert_same_circuits(
        circuit,
        qubitron.drop_negligible_operations(circuit, context=qubitron.TransformerContext(deep=True)),
    )
