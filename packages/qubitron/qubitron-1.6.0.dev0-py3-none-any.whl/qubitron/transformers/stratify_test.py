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

from __future__ import annotations

import pytest

import qubitron


def test_stratified_circuit_classifier_types():
    a, b, c, d = qubitron.LineQubit.range(4)

    circuit = qubitron.Circuit(qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.X(c) ** 0.5, qubitron.X(d)]))

    gate_result = qubitron.stratified_circuit(circuit, categories=[qubitron.X])
    qubitron.testing.assert_same_circuits(
        gate_result,
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(a), qubitron.X(d)]), qubitron.Moment([qubitron.Y(b), qubitron.X(c) ** 0.5])
        ),
    )

    gate_type_result = qubitron.stratified_circuit(circuit, categories=[qubitron.XPowGate])
    qubitron.testing.assert_same_circuits(
        gate_type_result,
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(a), qubitron.X(c) ** 0.5, qubitron.X(d)]), qubitron.Moment([qubitron.Y(b)])
        ),
    )

    operation_result = qubitron.stratified_circuit(circuit, categories=[qubitron.X(a)])
    qubitron.testing.assert_same_circuits(
        operation_result,
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.Y(b), qubitron.X(c) ** 0.5, qubitron.X(d)])
        ),
    )

    operation_type_result = qubitron.stratified_circuit(circuit, categories=[qubitron.GateOperation])
    qubitron.testing.assert_same_circuits(
        operation_type_result,
        qubitron.Circuit(qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.X(c) ** 0.5, qubitron.X(d)])),
    )

    predicate_result = qubitron.stratified_circuit(circuit, categories=[lambda op: op.qubits == (b,)])
    qubitron.testing.assert_same_circuits(
        predicate_result,
        qubitron.Circuit(
            qubitron.Moment([qubitron.Y(b)]), qubitron.Moment([qubitron.X(a), qubitron.X(d), qubitron.X(c) ** 0.5])
        ),
    )

    with pytest.raises(TypeError, match='Unrecognized'):
        _ = qubitron.stratified_circuit(circuit, categories=['unknown'])


def test_overlapping_categories():
    a, b, c, d = qubitron.LineQubit.range(4)

    result = qubitron.stratified_circuit(
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.Z(c)]),
            qubitron.Moment([qubitron.CNOT(a, b)]),
            qubitron.Moment([qubitron.CNOT(c, d)]),
            qubitron.Moment([qubitron.X(a), qubitron.Y(b), qubitron.Z(c)]),
        ),
        categories=[
            lambda op: len(op.qubits) == 1 and not isinstance(op.gate, qubitron.XPowGate),
            lambda op: len(op.qubits) == 1 and not isinstance(op.gate, qubitron.ZPowGate),
        ],
    )

    qubitron.testing.assert_same_circuits(
        result,
        qubitron.Circuit(
            qubitron.Moment([qubitron.Y(b), qubitron.Z(c)]),
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment([qubitron.CNOT(a, b), qubitron.CNOT(c, d)]),
            qubitron.Moment([qubitron.Y(b), qubitron.Z(c)]),
            qubitron.Moment([qubitron.X(a)]),
        ),
    )


def test_empty():
    a = qubitron.LineQubit(0)
    assert qubitron.stratified_circuit(qubitron.Circuit(), categories=[]) == qubitron.Circuit()
    assert qubitron.stratified_circuit(qubitron.Circuit(), categories=[qubitron.X]) == qubitron.Circuit()
    assert qubitron.stratified_circuit(qubitron.Circuit(qubitron.X(a)), categories=[]) == qubitron.Circuit(
        qubitron.X(a)
    )


def test_greedy_merging():
    """Tests a tricky situation where the algorithm of "Merge single-qubit
    gates, greedily align single-qubit then 2-qubit operations" doesn't work.
    Our algorithm succeeds because we also run it in reverse order."""
    q1, q2, q3, q4 = qubitron.LineQubit.range(4)
    input_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.X(q1)]),
        qubitron.Moment([qubitron.SWAP(q1, q2), qubitron.SWAP(q3, q4)]),
        qubitron.Moment([qubitron.X(q3)]),
        qubitron.Moment([qubitron.SWAP(q3, q4)]),
    )
    expected = qubitron.Circuit(
        qubitron.Moment([qubitron.SWAP(q3, q4)]),
        qubitron.Moment([qubitron.X(q1), qubitron.X(q3)]),
        qubitron.Moment([qubitron.SWAP(q1, q2), qubitron.SWAP(q3, q4)]),
    )
    qubitron.testing.assert_same_circuits(
        qubitron.stratified_circuit(input_circuit, categories=[qubitron.X]), expected
    )


def test_greedy_merging_reverse():
    """Same as the above test, except that the aligning is done in reverse."""
    q1, q2, q3, q4 = qubitron.LineQubit.range(4)
    input_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.SWAP(q1, q2), qubitron.SWAP(q3, q4)]),
        qubitron.Moment([qubitron.X(q4)]),
        qubitron.Moment([qubitron.SWAP(q3, q4)]),
        qubitron.Moment([qubitron.X(q1)]),
    )
    expected = qubitron.Circuit(
        qubitron.Moment([qubitron.SWAP(q1, q2), qubitron.SWAP(q3, q4)]),
        qubitron.Moment([qubitron.X(q1), qubitron.X(q4)]),
        qubitron.Moment([qubitron.SWAP(q3, q4)]),
    )
    qubitron.testing.assert_same_circuits(
        qubitron.stratified_circuit(input_circuit, categories=[qubitron.X]), expected
    )


def test_complex_circuit():
    """Tests that a complex circuit is correctly optimized."""
    q1, q2, q3, q4, q5 = qubitron.LineQubit.range(5)
    input_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.X(q1), qubitron.ISWAP(q2, q3), qubitron.Z(q5)]),
        qubitron.Moment([qubitron.X(q1), qubitron.ISWAP(q4, q5)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2), qubitron.X(q4)]),
    )
    expected = qubitron.Circuit(
        qubitron.Moment([qubitron.X(q1)]),
        qubitron.Moment([qubitron.Z(q5)]),
        qubitron.Moment([qubitron.ISWAP(q2, q3), qubitron.ISWAP(q4, q5)]),
        qubitron.Moment([qubitron.X(q1), qubitron.X(q4)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2)]),
    )
    qubitron.testing.assert_same_circuits(
        qubitron.stratified_circuit(input_circuit, categories=[qubitron.X, qubitron.Z]), expected
    )


def test_complex_circuit_deep():
    q = qubitron.LineQubit.range(5)
    c_nested = qubitron.FrozenCircuit(
        qubitron.Moment(
            qubitron.X(q[0]).with_tags("ignore"),
            qubitron.ISWAP(q[1], q[2]).with_tags("ignore"),
            qubitron.Z(q[4]),
        ),
        qubitron.Moment(qubitron.Z(q[1]), qubitron.ISWAP(q[3], q[4])),
        qubitron.Moment(qubitron.ISWAP(q[0], q[1]), qubitron.X(q[3])),
        qubitron.Moment(qubitron.X.on_each(q[0])),
    )
    c_nested_stratified = qubitron.FrozenCircuit(
        qubitron.Moment(qubitron.X(q[0]).with_tags("ignore"), qubitron.ISWAP(q[1], q[2]).with_tags("ignore")),
        qubitron.Moment(qubitron.Z.on_each(q[1], q[4])),
        qubitron.Moment(qubitron.ISWAP(*q[:2]), qubitron.ISWAP(*q[3:])),
        qubitron.Moment(qubitron.X.on_each(q[0], q[3])),
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
        c_nested,
    )
    c_expected = qubitron.Circuit(
        c_nested_stratified,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
        c_nested_stratified,
        qubitron.CircuitOperation(c_nested_stratified).repeat(6).with_tags("preserve_tag"),
        c_nested_stratified,
    )
    context = qubitron.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_stratified = qubitron.stratified_circuit(c_orig, context=context, categories=[qubitron.X, qubitron.Z])
    qubitron.testing.assert_same_circuits(c_stratified, c_expected)


def test_no_categories_earliest_insert():
    q1, q2, q3, q4, q5 = qubitron.LineQubit.range(5)
    input_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.ISWAP(q2, q3)]),
        qubitron.Moment([qubitron.X(q1), qubitron.ISWAP(q4, q5)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2), qubitron.X(q4)]),
    )
    qubitron.testing.assert_same_circuits(
        qubitron.Circuit(input_circuit.all_operations()), qubitron.stratified_circuit(input_circuit)
    )


def test_stratify_respects_no_compile_operations():
    q1, q2, q3, q4, q5 = qubitron.LineQubit.range(5)
    input_circuit = qubitron.Circuit(
        qubitron.Moment(
            [
                qubitron.X(q1).with_tags("nocompile"),
                qubitron.ISWAP(q2, q3).with_tags("nocompile"),
                qubitron.Z(q5),
            ]
        ),
        qubitron.Moment([qubitron.X(q1), qubitron.ISWAP(q4, q5)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2), qubitron.X(q4)]),
    )
    expected = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.Z(qubitron.LineQubit(4))),
            qubitron.Moment(qubitron.ISWAP(qubitron.LineQubit(3), qubitron.LineQubit(4))),
            qubitron.Moment(
                qubitron.TaggedOperation(qubitron.X(qubitron.LineQubit(0)), 'nocompile'),
                qubitron.TaggedOperation(qubitron.ISWAP(qubitron.LineQubit(1), qubitron.LineQubit(2)), 'nocompile'),
            ),
            qubitron.Moment(qubitron.X(qubitron.LineQubit(0)), qubitron.X(qubitron.LineQubit(3))),
            qubitron.Moment(qubitron.ISWAP(qubitron.LineQubit(0), qubitron.LineQubit(1))),
        ]
    )
    qubitron.testing.assert_has_diagram(
        input_circuit,
        '''
0: ───X[nocompile]───────X───────iSwap───
                                 │
1: ───iSwap[nocompile]───────────iSwap───
      │
2: ───iSwap──────────────────────────────

3: ──────────────────────iSwap───X───────
                         │
4: ───Z──────────────────iSwap───────────
''',
    )
    qubitron.testing.assert_has_diagram(
        expected,
        '''
0: ───────────────X[nocompile]───────X───iSwap───
                                         │
1: ───────────────iSwap[nocompile]───────iSwap───
                  │
2: ───────────────iSwap──────────────────────────

3: ───────iSwap──────────────────────X───────────
          │
4: ───Z───iSwap──────────────────────────────────
''',
    )
    qubitron.testing.assert_same_circuits(
        qubitron.stratified_circuit(
            input_circuit,
            categories=[qubitron.X, qubitron.Z],
            context=qubitron.TransformerContext(tags_to_ignore=("nocompile",)),
        ),
        expected,
    )


def test_does_not_move_ccos_behind_measurement():
    q = qubitron.LineQubit.range(3)
    c_orig = qubitron.Circuit(
        qubitron.measure(q[0], key='m'),
        qubitron.X(q[1]).with_classical_controls('m'),
        qubitron.Moment(qubitron.X.on_each(q[1], q[2])),
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───M───────────
      ║
1: ───╫───X───X───
      ║   ║
2: ───╫───╫───X───
      ║   ║
m: ═══@═══^═══════
''',
    )
    c_out = qubitron.stratified_circuit(
        c_orig, categories=[qubitron.GateOperation, qubitron.ClassicallyControlledOperation]
    )
    qubitron.testing.assert_has_diagram(
        c_out,
        '''
      ┌──┐
0: ────M─────────────
       ║
1: ────╫─────X───X───
       ║     ║
2: ────╫X────╫───────
       ║     ║
m: ════@═════^═══════
      └──┘
''',
    )


def test_heterogeneous_circuit():
    """Tests that a circuit that is very heterogeneous is correctly optimized"""
    q1, q2, q3, q4, q5, q6 = qubitron.LineQubit.range(6)
    input_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.X(q1), qubitron.X(q2), qubitron.ISWAP(q3, q4), qubitron.ISWAP(q5, q6)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2), qubitron.ISWAP(q3, q4), qubitron.X(q5), qubitron.X(q6)]),
        qubitron.Moment([qubitron.X(q1), qubitron.Z(q2), qubitron.X(q3), qubitron.Z(q4), qubitron.X(q5), qubitron.Z(q6)]),
    )
    expected = qubitron.Circuit(
        qubitron.Moment([qubitron.ISWAP(q3, q4), qubitron.ISWAP(q5, q6)]),
        qubitron.Moment([qubitron.X(q1), qubitron.X(q2), qubitron.X(q5), qubitron.X(q6)]),
        qubitron.Moment([qubitron.ISWAP(q1, q2), qubitron.ISWAP(q3, q4)]),
        qubitron.Moment([qubitron.Z(q2), qubitron.Z(q4), qubitron.Z(q6)]),
        qubitron.Moment([qubitron.X(q1), qubitron.X(q3), qubitron.X(q5)]),
    )

    qubitron.testing.assert_same_circuits(
        qubitron.stratified_circuit(input_circuit, categories=[qubitron.X, qubitron.Z]), expected
    )


def test_surface_code_cycle_stratifies_without_growing():
    g = qubitron.GridQubit
    circuit = qubitron.Circuit(
        qubitron.H(g(9, 11)),
        qubitron.H(g(11, 12)),
        qubitron.H(g(12, 9)),
        qubitron.H(g(9, 8)),
        qubitron.H(g(8, 11)),
        qubitron.H(g(11, 9)),
        qubitron.H(g(10, 9)),
        qubitron.H(g(10, 8)),
        qubitron.H(g(11, 10)),
        qubitron.H(g(12, 10)),
        qubitron.H(g(9, 9)),
        qubitron.H(g(9, 10)),
        qubitron.H(g(10, 11)),
        qubitron.CZ(g(10, 9), g(9, 9)),
        qubitron.CZ(g(10, 11), g(9, 11)),
        qubitron.CZ(g(9, 10), g(8, 10)),
        qubitron.CZ(g(11, 10), g(10, 10)),
        qubitron.CZ(g(12, 9), g(11, 9)),
        qubitron.CZ(g(11, 12), g(10, 12)),
        qubitron.H(g(9, 11)),
        qubitron.H(g(9, 9)),
        qubitron.H(g(10, 10)),
        qubitron.H(g(11, 9)),
        qubitron.H(g(10, 12)),
        qubitron.H(g(8, 10)),
        qubitron.CZ(g(11, 10), g(11, 11)),
        qubitron.CZ(g(10, 9), g(10, 8)),
        qubitron.CZ(g(12, 9), g(12, 10)),
        qubitron.CZ(g(10, 11), g(10, 10)),
        qubitron.CZ(g(9, 8), g(9, 9)),
        qubitron.CZ(g(9, 10), g(9, 11)),
        qubitron.CZ(g(8, 11), g(8, 10)),
        qubitron.CZ(g(11, 10), g(11, 9)),
        qubitron.CZ(g(11, 12), g(11, 11)),
        qubitron.H(g(10, 8)),
        qubitron.H(g(12, 10)),
        qubitron.H(g(12, 9)),
        qubitron.CZ(g(9, 10), g(9, 9)),
        qubitron.CZ(g(10, 9), g(10, 10)),
        qubitron.CZ(g(10, 11), g(10, 12)),
        qubitron.H(g(11, 11)),
        qubitron.H(g(9, 11)),
        qubitron.H(g(11, 9)),
        qubitron.CZ(g(9, 8), g(10, 8)),
        qubitron.CZ(g(11, 10), g(12, 10)),
        qubitron.H(g(11, 12)),
        qubitron.H(g(8, 10)),
        qubitron.H(g(10, 10)),
        qubitron.CZ(g(8, 11), g(9, 11)),
        qubitron.CZ(g(10, 9), g(11, 9)),
        qubitron.CZ(g(10, 11), g(11, 11)),
        qubitron.H(g(9, 8)),
        qubitron.H(g(10, 12)),
        qubitron.H(g(11, 10)),
        qubitron.CZ(g(9, 10), g(10, 10)),
        qubitron.H(g(11, 11)),
        qubitron.H(g(9, 11)),
        qubitron.H(g(8, 11)),
        qubitron.H(g(11, 9)),
        qubitron.H(g(10, 9)),
        qubitron.H(g(10, 11)),
        qubitron.H(g(9, 10)),
    )
    assert len(circuit) == 8
    stratified = qubitron.stratified_circuit(circuit, categories=[qubitron.H, qubitron.CZ])
    # Ideally, this would not grow at all, but for now the algorithm has it
    # grow to a 9. Note that this optimizer uses a fairly simple algorithm
    # that is known not to be optimal - optimal stratification is a CSP
    # problem with high dimensionality that quickly becomes intractable. See
    # https://github.com/amyssnippet/Qubitron/pull/2772/ for some discussion on
    # this, as well as a more optimal but much more complex and slow solution.
    assert len(stratified) == 9


def test_unclassified_ops():
    op = qubitron.X(qubitron.q(0))
    classifiers = []
    with pytest.raises(ValueError, match='not identified by any classifier'):
        qubitron.transformers.stratify._get_op_class(op, classifiers)
