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

import random
from typing import cast, Sequence

import numpy as np
import pytest

import qubitron
import qubitron.testing


def test_random_circuit_errors() -> None:
    with pytest.raises(ValueError, match='but was -1'):
        _ = qubitron.testing.random_circuit(qubits=5, n_moments=5, op_density=-1)

    with pytest.raises(ValueError, match='empty'):
        _ = qubitron.testing.random_circuit(qubits=5, n_moments=5, op_density=0.5, gate_domain={})

    with pytest.raises(ValueError, match='At least one'):
        _ = qubitron.testing.random_circuit(qubits=0, n_moments=5, op_density=0.5)

    with pytest.raises(ValueError, match='At least one'):
        _ = qubitron.testing.random_circuit(qubits=(), n_moments=5, op_density=0.5)

    with pytest.raises(
        ValueError,
        match='After removing gates that act on less than 1 qubits, gate_domain had no gates',
    ):
        _ = qubitron.testing.random_circuit(
            qubits=1, n_moments=5, op_density=0.5, gate_domain={qubitron.CNOT: 2}
        )


def _cases_for_random_circuit():
    i = 0
    while i < 10:
        n_qubits = random.randint(1, 20)
        n_moments = random.randint(1, 10)
        op_density = random.random()
        if random.randint(0, 1):
            gate_domain = dict(
                random.sample(
                    tuple(qubitron.testing.DEFAULT_GATE_DOMAIN.items()),
                    random.randint(1, len(qubitron.testing.DEFAULT_GATE_DOMAIN)),
                )
            )
            # Sometimes we generate gate domains whose gates all act on a
            # number of qubits greater than the number of qubits for the
            # circuit. In this case, try again.
            if all(n > n_qubits for n in gate_domain.values()):
                continue  # pragma: no cover
        else:
            gate_domain = None
        pass_qubits = random.choice((True, False))
        yield (n_qubits, n_moments, op_density, gate_domain, pass_qubits)
        i += 1


@pytest.mark.parametrize(
    'n_qubits,n_moments,op_density,gate_domain,pass_qubits', _cases_for_random_circuit()
)
def test_random_circuit(
    n_qubits: int | Sequence[qubitron.Qid],
    n_moments: int,
    op_density: float,
    gate_domain: dict[qubitron.Gate, int] | None,
    pass_qubits: bool,
) -> None:
    qubit_set = qubitron.LineQubit.range(n_qubits)
    qubit_arg = qubit_set if pass_qubits else n_qubits
    circuit = qubitron.testing.random_circuit(qubit_arg, n_moments, op_density, gate_domain)
    if qubit_arg is qubit_set:
        assert circuit.all_qubits().issubset(qubit_set)
    assert len(circuit) == n_moments
    if gate_domain is None:
        gate_domain = qubitron.testing.DEFAULT_GATE_DOMAIN
    assert set(cast(qubitron.GateOperation, op).gate for op in circuit.all_operations()).issubset(
        gate_domain
    )


@pytest.mark.parametrize('seed', [random.randint(0, 2**32) for _ in range(10)])
def test_random_circuit_reproducible_with_seed(seed) -> None:
    wrappers = (lambda s: s, np.random.RandomState)
    circuits = [
        qubitron.testing.random_circuit(
            qubits=10, n_moments=10, op_density=0.7, random_state=wrapper(seed)
        )
        for wrapper in wrappers
        for _ in range(2)
    ]
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(*circuits)


def test_random_circuit_not_expected_number_of_qubits() -> None:
    circuit = qubitron.testing.random_circuit(
        qubits=3, n_moments=1, op_density=1.0, gate_domain={qubitron.CNOT: 2}
    )
    # Despite having an op density of 1, we always only end up acting on
    # two qubits.
    assert len(circuit.all_qubits()) == 2


def test_random_circuit_reproducible_between_runs() -> None:
    circuit = qubitron.testing.random_circuit(5, 8, 0.5, random_state=77)
    expected_diagram = """
                  ┌──┐
0: ────────────────S─────iSwap───────Y───X───
                         │
1: ───────────Y──────────iSwap───────Y───────

2: ─────────────────X────T───────────S───S───
                    │
3: ───────@────────S┼────H───────────────Z───
          │         │
4: ───────@─────────@────────────────────X───
                  └──┘
    """
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)


def test_random_two_qubit_circuit_with_czs() -> None:
    num_czs = lambda circuit: len(
        [o for o in circuit.all_operations() if isinstance(o.gate, qubitron.CZPowGate)]
    )

    c = qubitron.testing.random_two_qubit_circuit_with_czs()
    assert num_czs(c) == 3
    assert {qubitron.NamedQubit('q0'), qubitron.NamedQubit('q1')} == c.all_qubits()
    assert all(isinstance(op.gate, qubitron.PhasedXPowGate) for op in c[0].operations)
    assert c[0].qubits == c.all_qubits()

    c = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=0)
    assert num_czs(c) == 0
    assert {qubitron.NamedQubit('q0'), qubitron.NamedQubit('q1')} == c.all_qubits()
    assert all(isinstance(op.gate, qubitron.PhasedXPowGate) for op in c[0].operations)
    assert c[0].qubits == c.all_qubits()

    a, b = qubitron.LineQubit.range(2)
    c = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=1, q1=b)
    assert num_czs(c) == 1
    assert {b, qubitron.NamedQubit('q0')} == c.all_qubits()
    assert all(isinstance(op.gate, qubitron.PhasedXPowGate) for op in c[0].operations)
    assert c[0].qubits == c.all_qubits()

    c = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=2, q0=a)
    assert num_czs(c) == 2
    assert {a, qubitron.NamedQubit('q1')} == c.all_qubits()
    assert all(isinstance(op.gate, qubitron.PhasedXPowGate) for op in c[0].operations)
    assert c[0].qubits == c.all_qubits()

    c = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=3, q0=a, q1=b)
    assert num_czs(c) == 3
    assert c.all_qubits() == {a, b}
    assert all(isinstance(op.gate, qubitron.PhasedXPowGate) for op in c[0].operations)
    assert c[0].qubits == c.all_qubits()

    seed = 77

    c1 = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=4, q0=a, q1=b, random_state=seed)
    assert num_czs(c1) == 4
    assert c1.all_qubits() == {a, b}

    c2 = qubitron.testing.random_two_qubit_circuit_with_czs(num_czs=4, q0=a, q1=b, random_state=seed)

    assert c1 == c2
