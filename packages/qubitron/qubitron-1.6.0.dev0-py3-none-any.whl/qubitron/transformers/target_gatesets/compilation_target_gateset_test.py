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

from typing import TYPE_CHECKING

import pytest

import qubitron

if TYPE_CHECKING:
    from qubitron.protocols.decompose_protocol import DecomposeResult


def test_compilation_target_gateset() -> None:
    class ExampleTargetGateset(qubitron.CompilationTargetGateset):
        def __init__(self):
            super().__init__(qubitron.AnyUnitaryGateFamily(2))

        @property
        def num_qubits(self) -> int:
            return 2

        def decompose_to_target_gateset(self, op: qubitron.Operation, _) -> DecomposeResult:
            return op if qubitron.num_qubits(op) == 2 and qubitron.has_unitary(op) else NotImplemented

        @property
        def preprocess_transformers(self) -> list[qubitron.TRANSFORMER]:
            return []

    gateset = ExampleTargetGateset()

    q = qubitron.LineQubit.range(2)
    assert qubitron.X(q[0]) not in gateset
    assert qubitron.CNOT(*q) in gateset
    assert qubitron.measure(*q) not in gateset
    circuit_op = qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.CZ(*q), qubitron.CNOT(*q), qubitron.CZ(*q)))
    assert circuit_op in gateset
    assert circuit_op.with_tags(gateset._intermediate_result_tag) not in gateset

    assert gateset.num_qubits == 2
    assert gateset.decompose_to_target_gateset(qubitron.X(q[0]), 1) is NotImplemented
    assert gateset.decompose_to_target_gateset(qubitron.CNOT(*q), 2) == qubitron.CNOT(*q)
    assert gateset.decompose_to_target_gateset(qubitron.measure(*q), 3) is NotImplemented

    assert gateset.preprocess_transformers == []
    assert gateset.postprocess_transformers == [
        qubitron.merge_single_qubit_moments_to_phxz,
        qubitron.drop_negligible_operations,
        qubitron.drop_empty_moments,
    ]


class ExampleCXTargetGateset(qubitron.TwoQubitCompilationTargetGateset):
    def __init__(self):
        super().__init__(qubitron.AnyUnitaryGateFamily(1), qubitron.CNOT)

    def _decompose_two_qubit_operation(self, op: qubitron.Operation, _) -> DecomposeResult:
        if not qubitron.has_unitary(op):
            return NotImplemented

        assert self._intermediate_result_tag in op.tags
        q0, q1 = op.qubits
        return [
            qubitron.X.on_each(q0, q1),
            qubitron.CNOT(q0, q1),
            qubitron.Y.on_each(q0, q1),
            qubitron.CNOT(q0, q1),
            qubitron.Z.on_each(q0, q1),
        ]

    def _decompose_single_qubit_operation(self, op: qubitron.Operation, _) -> DecomposeResult:
        if not qubitron.has_unitary(op):
            return NotImplemented
        assert self._intermediate_result_tag in op.tags
        op_untagged = op.untagged
        assert isinstance(op_untagged, qubitron.CircuitOperation)
        return (
            qubitron.decompose(op_untagged.circuit)
            if len(op_untagged.circuit) == 1
            else super()._decompose_single_qubit_operation(op, _)
        )


def test_two_qubit_compilation_leaves_single_gates_in_gateset() -> None:
    q = qubitron.LineQubit.range(2)
    gateset = ExampleCXTargetGateset()

    c = qubitron.Circuit(qubitron.X(q[0]) ** 0.5)
    qubitron.testing.assert_same_circuits(qubitron.optimize_for_target_gateset(c, gateset=gateset), c)

    c = qubitron.Circuit(qubitron.CNOT(*q[:2]))
    qubitron.testing.assert_same_circuits(qubitron.optimize_for_target_gateset(c, gateset=gateset), c)


def test_two_qubit_compilation_merges_runs_of_single_qubit_gates() -> None:
    q = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.CNOT(*q), qubitron.X(q[0]), qubitron.Y(q[0]), qubitron.CNOT(*q))
    qubitron.testing.assert_same_circuits(
        qubitron.optimize_for_target_gateset(c, gateset=ExampleCXTargetGateset()),
        qubitron.Circuit(
            qubitron.CNOT(*q),
            qubitron.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0, z_exponent=-1).on(q[0]),
            qubitron.CNOT(*q),
        ),
    )


def test_two_qubit_compilation_decompose_operation_not_implemented() -> None:
    gateset = ExampleCXTargetGateset()
    q = qubitron.LineQubit.range(3)
    assert gateset.decompose_to_target_gateset(qubitron.measure(q[0]), 1) is NotImplemented
    assert gateset.decompose_to_target_gateset(qubitron.measure(*q[:2]), 1) is NotImplemented
    assert (
        gateset.decompose_to_target_gateset(qubitron.X(q[0]).with_classical_controls("m"), 1)
        is NotImplemented
    )
    assert gateset.decompose_to_target_gateset(qubitron.CCZ(*q), 1) is NotImplemented


def test_two_qubit_compilation_merge_and_replace_to_target_gateset() -> None:
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.Moment(qubitron.Z(q[1]), qubitron.X(q[0])),
        qubitron.Moment(qubitron.CZ(*q).with_tags("no_compile")),
        qubitron.Moment(qubitron.Z.on_each(*q)),
        qubitron.Moment(qubitron.X(q[0])),
        qubitron.Moment(qubitron.CZ(*q)),
        qubitron.Moment(qubitron.Z.on_each(*q)),
        qubitron.Moment(qubitron.X(q[0])),
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───@[no_compile]───Z───X───@───Z───X───
          │                       │
1: ───Z───@───────────────Z───────@───Z───────
''',
    )
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=ExampleCXTargetGateset(),
        context=qubitron.TransformerContext(tags_to_ignore=("no_compile",)),
    )
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───X───@[no_compile]───X───@───Y───@───Z───
          │                   │       │
1: ───Z───@───────────────X───X───Y───X───Z───
''',
    )


def test_two_qubit_compilation_merge_and_replace_inefficient_component() -> None:
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.Moment(qubitron.X(q[0])),
        qubitron.Moment(qubitron.CNOT(*q)),
        qubitron.Moment(qubitron.X(q[0])),
        qubitron.Moment(qubitron.CZ(*q).with_tags("no_compile")),
        qubitron.Moment(qubitron.Z.on_each(*q)),
        qubitron.Moment(qubitron.X(q[0])),
        qubitron.Moment(qubitron.CNOT(*q)),
        qubitron.Moment(qubitron.CNOT(*q)),
        qubitron.Moment(qubitron.Z.on_each(*q)),
        qubitron.Moment(qubitron.X(q[0])),
        qubitron.Moment(qubitron.CNOT(*q)),
        qubitron.measure(q[0], key="m"),
        qubitron.X(q[1]).with_classical_controls("m"),
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───@───X───@[no_compile]───Z───X───@───@───Z───X───@───M───────
          │       │                       │   │           │   ║
1: ───────X───────@───────────────Z───────X───X───Z───────X───╫───X───
                                                              ║   ║
m: ═══════════════════════════════════════════════════════════@═══^═══
''',
    )
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=ExampleCXTargetGateset(),
        context=qubitron.TransformerContext(tags_to_ignore=("no_compile",)),
    )
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───X───@───X───@[no_compile]───X───@───Y───@───Z───M───────
          │       │                   │       │       ║
1: ───────X───────@───────────────X───X───Y───X───Z───╫───X───
                                                      ║   ║
m: ═══════════════════════════════════════════════════@═══^═══
''',
    )


def test_two_qubit_compilation_replaces_only_if_2q_gate_count_is_less() -> None:
    class ExampleTargetGateset(qubitron.TwoQubitCompilationTargetGateset):
        def __init__(self):
            super().__init__(qubitron.X, qubitron.CNOT)

        def _decompose_two_qubit_operation(self, op: qubitron.Operation, _) -> DecomposeResult:
            q0, q1 = op.qubits
            return [qubitron.X.on_each(q0, q1), qubitron.CNOT(q0, q1)] * 10

        def _decompose_single_qubit_operation(self, op: qubitron.Operation, _) -> DecomposeResult:
            return qubitron.X(*op.qubits) if op.gate == qubitron.Y else NotImplemented

    q = qubitron.LineQubit.range(2)
    ops = [qubitron.Y.on_each(*q), qubitron.CNOT(*q), qubitron.Z.on_each(*q)]
    c_orig = qubitron.Circuit(ops)
    c_expected = qubitron.Circuit(qubitron.X.on_each(*q), ops[-2:])
    c_new = qubitron.optimize_for_target_gateset(c_orig, gateset=ExampleTargetGateset())
    qubitron.testing.assert_same_circuits(c_new, c_expected)


def test_create_transformer_with_kwargs_raises() -> None:
    with pytest.raises(SyntaxError, match="must not contain `context`"):
        qubitron.create_transformer_with_kwargs(
            qubitron.merge_k_qubit_unitaries, k=2, context=qubitron.TransformerContext()
        )
