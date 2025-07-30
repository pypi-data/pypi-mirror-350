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

import pytest

import qubitron
from qubitron import Operation, PointOptimizationSummary, PointOptimizer
from qubitron.testing import EqualsTester


def test_equality() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    xa = qubitron.X(a)
    ya = qubitron.Y(a)

    eq = EqualsTester()

    eq.make_equality_group(
        lambda: PointOptimizationSummary(clear_span=0, clear_qubits=[], new_operations=[])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a, b], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=2, clear_qubits=[a], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[ya])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[xa, xa])
    )


class ReplaceWithXGates(PointOptimizer):
    """Replaces a block of operations with X gates.

    Searches ahead for gates covering a subset of the focused operation's
    qubits, clears the whole range, and inserts X gates for each cleared
    operation's qubits.
    """

    def optimization_at(
        self, circuit: qubitron.Circuit, index: int, op: qubitron.Operation
    ) -> qubitron.PointOptimizationSummary | None:
        end = index + 1
        new_ops = [qubitron.X(q) for q in op.qubits]
        done = False
        while not done:
            n = circuit.next_moment_operating_on(op.qubits, end)
            if n is None:
                break
            next_ops: set[Operation | None] = {circuit.operation_at(q, n) for q in op.qubits}
            next_ops_list: list[Operation] = [e for e in next_ops if e]
            next_ops_sorted = sorted(next_ops_list, key=lambda e: str(e.qubits))
            for next_op in next_ops_sorted:
                if next_op:
                    if set(next_op.qubits).issubset(op.qubits):
                        end = n + 1
                        new_ops.extend(qubitron.X(q) for q in next_op.qubits)
                    else:
                        done = True

        return PointOptimizationSummary(
            clear_span=end - index, clear_qubits=op.qubits, new_operations=new_ops
        )


def test_point_optimizer_can_write_new_gates_inline() -> None:
    x = qubitron.NamedQubit('x')
    y = qubitron.NamedQubit('y')
    z = qubitron.NamedQubit('z')
    c = qubitron.Circuit(
        qubitron.CZ(x, y),
        qubitron.Y(x),
        qubitron.Z(x),
        qubitron.X(y),
        qubitron.CNOT(y, z),
        qubitron.Z(y),
        qubitron.Z(x),
        qubitron.CNOT(y, z),
        qubitron.CNOT(z, y),
    )

    ReplaceWithXGates()(c)

    actual_text_diagram = c.to_text_diagram().strip()
    expected_text_diagram = """
x: ───X───X───X───X───────────

y: ───X───X───────X───X───X───

z: ───────────────────X───X───
    """.strip()

    assert actual_text_diagram == expected_text_diagram


def test_point_optimizer_post_clean_up() -> None:
    x = qubitron.NamedQubit('x')
    y = qubitron.NamedQubit('y')
    z = qubitron.NamedQubit('z')
    c = qubitron.Circuit(
        qubitron.CZ(x, y),
        qubitron.Y(x),
        qubitron.Z(x),
        qubitron.X(y),
        qubitron.CNOT(y, z),
        qubitron.Z(y),
        qubitron.Z(x),
        qubitron.CNOT(y, z),
        qubitron.CNOT(z, y),
    )

    def clean_up(operations):
        for op in operations:
            yield op**0.5

    ReplaceWithXGates(post_clean_up=clean_up)(c)

    actual_text_diagram = c.to_text_diagram().strip()
    expected_text_diagram = """
x: ───X^0.5───X^0.5───X^0.5───X^0.5───────────────────

y: ───X^0.5───X^0.5───────────X^0.5───X^0.5───X^0.5───

z: ───────────────────────────────────X^0.5───X^0.5───
    """.strip()

    assert actual_text_diagram == expected_text_diagram


def test_point_optimizer_raises_on_gates_changing_qubits() -> None:
    class EverythingIs42(qubitron.PointOptimizer):
        """Changes all single qubit operations to act on LineQubit(42)"""

        def optimization_at(
            self, circuit: qubitron.Circuit, index: int, op: qubitron.Operation
        ) -> qubitron.PointOptimizationSummary | None:
            new_op = op
            if len(op.qubits) == 1 and isinstance(op, qubitron.GateOperation):
                new_op = op.gate(qubitron.LineQubit(42))

            return qubitron.PointOptimizationSummary(
                clear_span=1, clear_qubits=op.qubits, new_operations=new_op
            )

    c = qubitron.Circuit(qubitron.X(qubitron.LineQubit(0)), qubitron.X(qubitron.LineQubit(1)))

    with pytest.raises(ValueError, match='new qubits'):
        EverythingIs42().optimize_circuit(c)


def test_repr() -> None:
    assert (
        repr(qubitron.PointOptimizationSummary(clear_span=0, clear_qubits=[], new_operations=[]))
        == 'qubitron.PointOptimizationSummary(0, (), ())'
    )
