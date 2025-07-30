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

"""Tests for the expand composite transformer pass."""

from __future__ import annotations

import qubitron


def assert_equal_mod_empty(expected, actual):
    actual = qubitron.drop_empty_moments(actual)
    qubitron.testing.assert_same_circuits(actual, expected)


def test_empty_circuit():
    circuit = qubitron.Circuit()
    circuit = qubitron.expand_composite(circuit)
    assert_equal_mod_empty(qubitron.Circuit(), circuit)


def test_empty_moment():
    circuit = qubitron.Circuit([])
    circuit = qubitron.expand_composite(circuit)
    assert_equal_mod_empty(qubitron.Circuit([]), circuit)


def test_ignore_non_composite():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit()
    circuit.append([qubitron.X(q0), qubitron.Y(q1), qubitron.CZ(q0, q1), qubitron.Z(q0)])
    expected = circuit.copy()
    circuit = qubitron.expand_composite(circuit)
    assert_equal_mod_empty(expected, circuit)


def test_composite_default():
    q0, q1 = qubitron.LineQubit.range(2)
    cnot = qubitron.CNOT(q0, q1)
    circuit = qubitron.Circuit()
    circuit.append(cnot)
    circuit = qubitron.expand_composite(circuit)
    expected = qubitron.Circuit()
    expected.append([qubitron.Y(q1) ** -0.5, qubitron.CZ(q0, q1), qubitron.Y(q1) ** 0.5])
    assert_equal_mod_empty(expected, circuit)


def test_multiple_composite_default():
    q0, q1 = qubitron.LineQubit.range(2)
    cnot = qubitron.CNOT(q0, q1)
    circuit = qubitron.Circuit()
    circuit.append([cnot, cnot])
    circuit = qubitron.expand_composite(circuit)
    expected = qubitron.Circuit()
    decomp = [qubitron.Y(q1) ** -0.5, qubitron.CZ(q0, q1), qubitron.Y(q1) ** 0.5]
    expected.append([decomp, decomp])
    assert_equal_mod_empty(expected, circuit)


def test_mix_composite_non_composite():
    q0, q1 = qubitron.LineQubit.range(2)

    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.CNOT(q0, q1), qubitron.X(q1))
    circuit = qubitron.expand_composite(circuit)

    expected = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.Y(q1) ** -0.5,
        qubitron.CZ(q0, q1),
        qubitron.Y(q1) ** 0.5,
        qubitron.X(q1),
        strategy=qubitron.InsertStrategy.NEW,
    )
    assert_equal_mod_empty(expected, circuit)


def test_recursive_composite():
    q0, q1 = qubitron.LineQubit.range(2)
    swap = qubitron.SWAP(q0, q1)
    circuit = qubitron.Circuit()
    circuit.append(swap)

    circuit = qubitron.expand_composite(circuit)
    expected = qubitron.Circuit(
        qubitron.Y(q1) ** -0.5,
        qubitron.CZ(q0, q1),
        qubitron.Y(q1) ** 0.5,
        qubitron.Y(q0) ** -0.5,
        qubitron.CZ(q1, q0),
        qubitron.Y(q0) ** 0.5,
        qubitron.Y(q1) ** -0.5,
        qubitron.CZ(q0, q1),
        qubitron.Y(q1) ** 0.5,
    )
    assert_equal_mod_empty(expected, circuit)


def test_decompose_returns_not_flat_op_tree():
    class ExampleGate(qubitron.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            (q0,) = qubits
            # Yield a tuple of gates instead of yielding a gate
            yield qubitron.X(q0),

    q0 = qubitron.NamedQubit('q0')
    circuit = qubitron.Circuit(ExampleGate()(q0))

    circuit = qubitron.expand_composite(circuit)
    expected = qubitron.Circuit(qubitron.X(q0))
    assert_equal_mod_empty(expected, circuit)


def test_decompose_returns_deep_op_tree():
    class ExampleGate(qubitron.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            q0, q1 = qubits
            # Yield a tuple
            yield ((qubitron.X(q0), qubitron.Y(q0)), qubitron.Z(q0))
            # Yield nested lists
            yield [qubitron.X(q0), [qubitron.Y(q0), qubitron.Z(q0)]]

            def generator(depth):
                if depth <= 0:
                    yield qubitron.CZ(q0, q1), qubitron.Y(q0)
                else:
                    yield qubitron.X(q0), generator(depth - 1)
                    yield qubitron.Z(q0)

            # Yield nested generators
            yield generator(2)

    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(ExampleGate()(q0, q1))

    circuit = qubitron.expand_composite(circuit)
    expected = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.Y(q0),
        qubitron.Z(q0),  # From tuple
        qubitron.X(q0),
        qubitron.Y(q0),
        qubitron.Z(q0),  # From nested lists
        # From nested generators
        qubitron.X(q0),
        qubitron.X(q0),
        qubitron.CZ(q0, q1),
        qubitron.Y(q0),
        qubitron.Z(q0),
        qubitron.Z(q0),
    )
    assert_equal_mod_empty(expected, circuit)


def test_non_recursive_expansion():
    qubits = [qubitron.NamedQubit(s) for s in 'xy']
    no_decomp = lambda op: (isinstance(op, qubitron.GateOperation) and op.gate == qubitron.ISWAP)
    unexpanded_circuit = qubitron.Circuit(qubitron.ISWAP(*qubits))

    circuit = qubitron.expand_composite(unexpanded_circuit, no_decomp=no_decomp)
    assert circuit == unexpanded_circuit

    no_decomp = lambda op: (
        isinstance(op, qubitron.GateOperation)
        and isinstance(op.gate, (qubitron.CNotPowGate, qubitron.HPowGate))
    )
    circuit = qubitron.expand_composite(unexpanded_circuit, no_decomp=no_decomp)
    actual_text_diagram = circuit.to_text_diagram().strip()
    expected_text_diagram = """
x: ───@───H───X───S───X───S^-1───H───@───
      │       │       │              │
y: ───X───────@───────@──────────────X───
    """.strip()
    assert actual_text_diagram == expected_text_diagram


def test_do_not_decompose_no_compile():
    q0, q1 = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.CNOT(q0, q1).with_tags("no_compile"))
    context = qubitron.TransformerContext(tags_to_ignore=("no_compile",))
    assert_equal_mod_empty(c, qubitron.expand_composite(c, context=context))


def test_expands_composite_recursively_preserving_structur():
    q = qubitron.LineQubit.range(2)
    c_nested = qubitron.FrozenCircuit(
        qubitron.SWAP(*q[:2]), qubitron.SWAP(*q[:2]).with_tags("ignore"), qubitron.SWAP(*q[:2])
    )
    c_nested_expanded = qubitron.FrozenCircuit(
        [qubitron.CNOT(*q), qubitron.CNOT(*q[::-1]), qubitron.CNOT(*q)],
        qubitron.SWAP(*q[:2]).with_tags("ignore"),
        [qubitron.CNOT(*q), qubitron.CNOT(*q[::-1]), qubitron.CNOT(*q)],
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                c_nested,
                qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                qubitron.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                qubitron.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(4)
        .with_tags("ignore"),
        c_nested,
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                c_nested,
                qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                qubitron.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                qubitron.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(5)
        .with_tags("preserve_tag"),
        c_nested,
    )
    c_expected = qubitron.Circuit(
        c_nested_expanded,
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                c_nested,
                qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                qubitron.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                qubitron.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(4)
        .with_tags("ignore"),
        c_nested_expanded,
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                c_nested_expanded,
                qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                qubitron.CircuitOperation(c_nested_expanded).repeat(6).with_tags("preserve_tag"),
                qubitron.CircuitOperation(c_nested_expanded).repeat(7),
                c_nested_expanded,
            )
        )
        .repeat(5)
        .with_tags("preserve_tag"),
        c_nested_expanded,
    )

    context = qubitron.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_expanded = qubitron.expand_composite(
        c_orig, no_decomp=lambda op: op.gate == qubitron.CNOT, context=context
    )
    qubitron.testing.assert_same_circuits(c_expanded, c_expected)
