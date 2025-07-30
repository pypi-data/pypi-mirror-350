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

# pylint: skip-file

from __future__ import annotations

import numpy as np
import pytest

import qubitron


def assert_optimizes(optimized: qubitron.AbstractCircuit, expected: qubitron.AbstractCircuit):
    # Ignore differences that would be caught by follow-up optimizations.
    followup_transformers: list[qubitron.TRANSFORMER] = [
        qubitron.drop_negligible_operations,
        qubitron.drop_empty_moments,
    ]
    for transform in followup_transformers:
        optimized = transform(optimized)
        expected = transform(expected)

    qubitron.testing.assert_same_circuits(optimized, expected)


def test_merge_1q_unitaries() -> None:
    q, q2 = qubitron.LineQubit.range(2)
    # 1. Combines trivial 1q sequence.
    c = qubitron.Circuit(qubitron.X(q) ** 0.5, qubitron.Z(q) ** 0.5, qubitron.X(q) ** -0.5)
    c = qubitron.merge_k_qubit_unitaries(c, k=1)
    op_list = [*c.all_operations()]
    assert len(op_list) == 1
    assert isinstance(op_list[0].gate, qubitron.MatrixGate)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(c), qubitron.unitary(qubitron.Y**0.5), atol=1e-7
    )

    # 2. Gets blocked at a 2q operation.
    c = qubitron.Circuit([qubitron.Z(q), qubitron.H(q), qubitron.X(q), qubitron.H(q), qubitron.CZ(q, q2), qubitron.H(q)])
    c = qubitron.drop_empty_moments(qubitron.merge_k_qubit_unitaries(c, k=1))
    assert len(c) == 3
    qubitron.testing.assert_allclose_up_to_global_phase(qubitron.unitary(c[0]), np.eye(2), atol=1e-7)
    assert isinstance(c[-1][q].gate, qubitron.MatrixGate)


def test_respects_nocompile_tags() -> None:
    q = qubitron.NamedQubit("q")
    c = qubitron.Circuit(
        [qubitron.Z(q), qubitron.H(q), qubitron.X(q), qubitron.H(q), qubitron.X(q).with_tags("nocompile"), qubitron.H(q)]
    )
    context = qubitron.TransformerContext(tags_to_ignore=("nocompile",))
    c = qubitron.drop_empty_moments(qubitron.merge_k_qubit_unitaries(c, k=1, context=context))
    assert len(c) == 3
    qubitron.testing.assert_allclose_up_to_global_phase(qubitron.unitary(c[0]), np.eye(2), atol=1e-7)
    assert c[1][q] == qubitron.X(q).with_tags("nocompile")
    assert isinstance(c[-1][q].gate, qubitron.MatrixGate)


def test_ignores_2qubit_target() -> None:
    c = qubitron.Circuit(qubitron.CZ(*qubitron.LineQubit.range(2)))
    assert_optimizes(optimized=qubitron.merge_k_qubit_unitaries(c, k=1), expected=c)


def test_ignore_unsupported_gate() -> None:
    class UnsupportedExample(qubitron.testing.SingleQubitGate):
        pass

    c = qubitron.Circuit(UnsupportedExample()(qubitron.LineQubit(0)))
    assert_optimizes(optimized=qubitron.merge_k_qubit_unitaries(c, k=1), expected=c)


def test_1q_rewrite() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(q0), qubitron.Y(q0), qubitron.X(q1), qubitron.CZ(q0, q1), qubitron.Y(q1), qubitron.measure(q0, q1)
    )
    assert_optimizes(
        optimized=qubitron.merge_k_qubit_unitaries(
            circuit, k=1, rewriter=lambda ops: qubitron.H(ops.qubits[0])
        ),
        expected=qubitron.Circuit(
            qubitron.H(q0), qubitron.H(q1), qubitron.CZ(q0, q1), qubitron.H(q1), qubitron.measure(q0, q1)
        ),
    )


def test_merge_k_qubit_unitaries_raises() -> None:
    with pytest.raises(ValueError, match="k should be greater than or equal to 1"):
        _ = qubitron.merge_k_qubit_unitaries(qubitron.Circuit())


def test_merge_complex_circuit_preserving_moment_structure() -> None:
    q = qubitron.LineQubit.range(3)
    c_orig = qubitron.Circuit(
        qubitron.Moment(qubitron.H.on_each(*q)),
        qubitron.CNOT(q[0], q[2]),
        qubitron.CNOT(*q[0:2]),
        qubitron.H(q[0]),
        qubitron.CZ(*q[:2]),
        qubitron.X(q[0]),
        qubitron.Y(q[1]),
        qubitron.CNOT(*q[0:2]),
        qubitron.CNOT(*q[1:3]).with_tags("ignore"),
        qubitron.X(q[0]),
        qubitron.Moment(qubitron.X(q[0]).with_tags("ignore"), qubitron.Y(q[1]), qubitron.Z(q[2])),
        qubitron.Moment(qubitron.CNOT(*q[:2]), qubitron.measure(q[2], key="a")),
        qubitron.X(q[0]).with_classical_controls("a"),
        strategy=qubitron.InsertStrategy.NEW,
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───H───@───@───H───@───X───────@───────────────X───X[ignore]───@───X───
          │   │       │           │                               │   ║
1: ───H───┼───X───────@───────Y───X───@[ignore]───────Y───────────X───╫───
          │                           │                               ║
2: ───H───X───────────────────────────X───────────────Z───────────M───╫───
                                                                  ║   ║
a: ═══════════════════════════════════════════════════════════════@═══^═══
''',
    )
    component_id = 0

    def rewriter_merge_to_circuit_op(op: qubitron.CircuitOperation) -> qubitron.OP_TREE:
        nonlocal component_id
        component_id = component_id + 1
        return op.with_tags(f'{component_id}')

    c_new = qubitron.merge_k_qubit_unitaries(
        c_orig,
        k=2,
        context=qubitron.TransformerContext(tags_to_ignore=("ignore",)),
        rewriter=rewriter_merge_to_circuit_op,
    )
    qubitron.testing.assert_has_diagram(
        qubitron.drop_empty_moments(c_new),
        '''
      [ 0: ───H───@─── ]      [ 0: ───────@───H───@───X───@───X─── ]                                      [ 0: ───────@─── ]
0: ───[           │    ]──────[           │       │       │        ]──────────────────X[ignore]───────────[           │    ]──────X───
      [ 2: ───H───X─── ][1]   [ 1: ───H───X───────@───Y───X─────── ][2]                                   [ 1: ───Y───X─── ][4]   ║
      │                       │                                                                           │                       ║
1: ───┼───────────────────────#2──────────────────────────────────────────@[ignore]───────────────────────#2──────────────────────╫───
      │                                                                   │                                                       ║
2: ───#2──────────────────────────────────────────────────────────────────X───────────[ 2: ───Z─── ][3]───M───────────────────────╫───
                                                                                                          ║                       ║
a: ═══════════════════════════════════════════════════════════════════════════════════════════════════════@═══════════════════════^═══''',
    )

    component_id = 0

    def rewriter_replace_with_decomp(op: qubitron.CircuitOperation) -> qubitron.OP_TREE:
        nonlocal component_id
        component_id = component_id + 1
        tag = f'{component_id}'
        if len(op.qubits) == 1:
            return [qubitron.T(op.qubits[0]).with_tags(tag)]
        one_layer = [op.with_tags(tag) for op in qubitron.T.on_each(*op.qubits)]
        two_layer = [qubitron.SQRT_ISWAP(*op.qubits).with_tags(tag)]
        return [one_layer, two_layer, one_layer]

    c_new = qubitron.merge_k_qubit_unitaries(
        c_orig,
        k=2,
        context=qubitron.TransformerContext(tags_to_ignore=("ignore",)),
        rewriter=rewriter_replace_with_decomp,
    )
    qubitron.testing.assert_has_diagram(
        qubitron.drop_empty_moments(c_new),
        '''
0: ───T[1]───iSwap[1]────T[1]───T[2]───iSwap[2]────T[2]───────────────X[ignore]───T[4]───iSwap[4]────T[4]───X───
             │                         │                                                 │                  ║
1: ──────────┼──────────────────T[2]───iSwap^0.5───T[2]───@[ignore]───────────────T[4]───iSwap^0.5───T[4]───╫───
             │                                            │                                                 ║
2: ───T[1]───iSwap^0.5───T[1]─────────────────────────────X───────────T[3]────────M─────────────────────────╫───
                                                                                  ║                         ║
a: ═══════════════════════════════════════════════════════════════════════════════@═════════════════════════^═══''',
    )


def test_merge_k_qubit_unitaries_deep() -> None:
    q = qubitron.LineQubit.range(2)
    h_cz_y = [qubitron.H(q[0]), qubitron.CZ(*q), qubitron.Y(q[1])]
    c_orig = qubitron.Circuit(
        h_cz_y,
        qubitron.Moment(qubitron.X(q[0]).with_tags("ignore"), qubitron.Y(q[1])),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        [qubitron.CNOT(*q), qubitron.CNOT(*q)],
        qubitron.CircuitOperation(qubitron.FrozenCircuit(h_cz_y)).repeat(4),
        [qubitron.CNOT(*q), qubitron.CZ(*q), qubitron.CNOT(*q)],
        qubitron.CircuitOperation(qubitron.FrozenCircuit(h_cz_y)).repeat(5).with_tags("preserve_tag"),
    )

    def _wrap_in_cop(ops: qubitron.OP_TREE, tag: str):
        return qubitron.CircuitOperation(qubitron.FrozenCircuit(ops)).with_tags(tag)

    c_expected = qubitron.Circuit(
        _wrap_in_cop([h_cz_y, qubitron.Y(q[1])], '1'),
        qubitron.Moment(qubitron.X(q[0]).with_tags("ignore")),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        _wrap_in_cop([qubitron.CNOT(*q), qubitron.CNOT(*q)], '2'),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(_wrap_in_cop(h_cz_y, '3'))).repeat(4),
        _wrap_in_cop([qubitron.CNOT(*q), qubitron.CZ(*q), qubitron.CNOT(*q)], '4'),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(_wrap_in_cop(h_cz_y, '5')))
        .repeat(5)
        .with_tags("preserve_tag"),
        strategy=qubitron.InsertStrategy.NEW,
    )

    component_id = 0

    def rewriter_merge_to_circuit_op(op: qubitron.CircuitOperation) -> qubitron.OP_TREE:
        nonlocal component_id
        component_id = component_id + 1
        return op.with_tags(f'{component_id}')

    context = qubitron.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    c_new = qubitron.merge_k_qubit_unitaries(
        c_orig, k=2, context=context, rewriter=rewriter_merge_to_circuit_op
    )
    qubitron.testing.assert_same_circuits(c_new, c_expected)

    def _wrap_in_matrix_gate(ops: qubitron.OP_TREE):
        op = _wrap_in_cop(ops, 'temp')
        return qubitron.MatrixGate(qubitron.unitary(op)).on(*op.qubits)

    c_expected_matrix = qubitron.Circuit(
        _wrap_in_matrix_gate([h_cz_y, qubitron.Y(q[1])]),
        qubitron.Moment(qubitron.X(q[0]).with_tags("ignore")),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        _wrap_in_matrix_gate([qubitron.CNOT(*q), qubitron.CNOT(*q)]),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(_wrap_in_matrix_gate(h_cz_y))).repeat(4),
        _wrap_in_matrix_gate([qubitron.CNOT(*q), qubitron.CZ(*q), qubitron.CNOT(*q)]),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(_wrap_in_matrix_gate(h_cz_y)))
        .repeat(5)
        .with_tags("preserve_tag"),
        strategy=qubitron.InsertStrategy.NEW,
    )
    c_new_matrix = qubitron.merge_k_qubit_unitaries(c_orig, k=2, context=context)
    qubitron.testing.assert_same_circuits(c_new_matrix, c_expected_matrix)


def test_merge_k_qubit_unitaries_deep_recurses_on_large_circuit_op() -> None:
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.X(q[0]), qubitron.H(q[0]), qubitron.CNOT(*q)))
    )
    c_expected = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.X(q[0]), qubitron.H(q[0]))).with_tags(
                    "merged"
                ),
                qubitron.CNOT(*q),
            )
        )
    )
    c_new = qubitron.merge_k_qubit_unitaries(
        c_orig,
        context=qubitron.TransformerContext(deep=True),
        k=1,
        rewriter=lambda op: op.with_tags("merged"),
    )
    qubitron.testing.assert_same_circuits(c_new, c_expected)
