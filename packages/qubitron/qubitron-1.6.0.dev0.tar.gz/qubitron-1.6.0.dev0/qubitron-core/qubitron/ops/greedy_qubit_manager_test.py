# Copyright 2023 The Qubitron Developers
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


class GateAllocInDecompose(qubitron.Gate):
    def __init__(self, num_alloc: int = 1):
        self.num_alloc = num_alloc

    def _num_qubits_(self) -> int:
        return 1

    def _decompose_with_context_(self, qubits, context):
        assert context is not None
        qm = context.qubit_manager
        for q in qm.qalloc(self.num_alloc):
            yield qubitron.CNOT(qubits[0], q)
            qm.qfree([q])


def test_greedy_qubit_manager() -> None:
    def make_circuit(qm: qubitron.QubitManager):
        q = qubitron.LineQubit.range(2)
        g = GateAllocInDecompose(1)
        context = qubitron.DecompositionContext(qubit_manager=qm)
        circuit = qubitron.Circuit(
            qubitron.decompose_once(g.on(q[0]), context=context),
            qubitron.decompose_once(g.on(q[1]), context=context),
        )
        return circuit

    qm = qubitron.GreedyQubitManager(prefix="ancilla", size=1)
    # Qubit manager with only 1 managed qubit. Will always repeat the same qubit.
    circuit = make_circuit(qm)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───────────@───────
              │
1: ───────────┼───@───
              │   │
ancilla_0: ───X───X───
        """,
    )

    qm = qubitron.GreedyQubitManager(prefix="ancilla", size=2)
    # Qubit manager with 2 managed qubits and maximize_reuse=False, tries to minimize adding
    # additional data dependencies by minimizing qubit reuse.
    circuit = make_circuit(qm)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
              ┌──┐
0: ────────────@─────
               │
1: ────────────┼@────
               ││
ancilla_0: ────X┼────
                │
ancilla_1: ─────X────
              └──┘
        """,
    )

    qm = qubitron.GreedyQubitManager(prefix="ancilla", size=2, maximize_reuse=True)
    # Qubit manager with 2 managed qubits and maximize_reuse=True, tries to maximize reuse by
    # potentially adding new data dependencies.
    circuit = make_circuit(qm)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───────────@───────
              │
1: ───────────┼───@───
              │   │
ancilla_1: ───X───X───
     """,
    )


def test_empty_qubits() -> None:
    qm = qubitron.GreedyQubitManager(prefix="anc")
    assert qm.qalloc(0) == []


def test_greedy_qubit_manager_preserves_order() -> None:
    qm = qubitron.GreedyQubitManager(prefix="anc")
    ancillae = [qubitron.q(f"anc_{i}") for i in range(100)]
    assert qm.qalloc(100) == ancillae
    qm.qfree(ancillae)
    assert qm.qalloc(100) == ancillae
