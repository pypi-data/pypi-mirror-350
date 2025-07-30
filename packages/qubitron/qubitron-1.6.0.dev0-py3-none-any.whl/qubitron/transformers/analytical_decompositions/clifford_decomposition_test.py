# Copyright 2021 The Qubitron Developers
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

import numpy as np
import pytest

import qubitron
from qubitron.testing import assert_allclose_up_to_global_phase


def test_misaligned_qubits():
    qubits = qubitron.LineQubit.range(1)
    tableau = qubitron.CliffordTableau(num_qubits=2)
    with pytest.raises(ValueError):
        qubitron.decompose_clifford_tableau_to_operations(qubits, tableau)


def test_clifford_decompose_one_qubit():
    """Two random instance for one qubit decomposition."""
    qubits = qubitron.LineQubit.range(1)
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=1), qubits=qubits, prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.X, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.S, args, qubits=[qubits[0]], allow_decompose=False)
    expect_circ = qubitron.Circuit(qubitron.X(qubits[0]), qubitron.H(qubits[0]), qubitron.S(qubits[0]))
    ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = qubitron.Circuit(ops)
    assert_allclose_up_to_global_phase(qubitron.unitary(expect_circ), qubitron.unitary(circ), atol=1e-7)

    qubits = qubitron.LineQubit.range(1)
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=1), qubits=qubits, prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.Z, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.S, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.X, args, qubits=[qubits[0]], allow_decompose=False)
    expect_circ = qubitron.Circuit(
        qubitron.Z(qubits[0]),
        qubitron.H(qubits[0]),
        qubitron.S(qubits[0]),
        qubitron.H(qubits[0]),
        qubitron.X(qubits[0]),
    )
    ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = qubitron.Circuit(ops)
    assert_allclose_up_to_global_phase(qubitron.unitary(expect_circ), qubitron.unitary(circ), atol=1e-7)


def test_clifford_decompose_two_qubits():
    """Two random instance for two qubits decomposition."""
    qubits = qubitron.LineQubit.range(2)
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=2), qubits=qubits, prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    expect_circ = qubitron.Circuit(qubitron.H(qubits[0]), qubitron.CNOT(qubits[0], qubits[1]))
    ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = qubitron.Circuit(ops)
    assert_allclose_up_to_global_phase(qubitron.unitary(expect_circ), qubitron.unitary(circ), atol=1e-7)

    qubits = qubitron.LineQubit.range(2)
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=2), qubits=qubits, prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    qubitron.act_on(qubitron.H, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.S, args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.X, args, qubits=[qubits[1]], allow_decompose=False)
    expect_circ = qubitron.Circuit(
        qubitron.H(qubits[0]),
        qubitron.CNOT(qubits[0], qubits[1]),
        qubitron.H(qubits[0]),
        qubitron.S(qubits[0]),
        qubitron.X(qubits[1]),
    )

    ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = qubitron.Circuit(ops)
    assert_allclose_up_to_global_phase(qubitron.unitary(expect_circ), qubitron.unitary(circ), atol=1e-7)


def test_clifford_decompose_by_unitary():
    """Validate the decomposition of random Clifford Tableau by unitary matrix.

    Due to the exponential growth in dimension, it cannot validate very large number of qubits.
    """
    n, num_ops = 5, 20
    gate_candidate = [qubitron.X, qubitron.Y, qubitron.Z, qubitron.H, qubitron.S, qubitron.CNOT, qubitron.CZ]
    for seed in range(100):
        prng = np.random.RandomState(seed)
        t = qubitron.CliffordTableau(num_qubits=n)
        qubits = qubitron.LineQubit.range(n)
        expect_circ = qubitron.Circuit()
        args = qubitron.CliffordTableauSimulationState(tableau=t, qubits=qubits, prng=prng)
        for _ in range(num_ops):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            qubitron.act_on(
                gate_candidate[g], args, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            expect_circ.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)
        circ = qubitron.Circuit(ops)
        circ.append(qubitron.I.on_each(qubits))
        expect_circ.append(qubitron.I.on_each(qubits))
        assert_allclose_up_to_global_phase(qubitron.unitary(expect_circ), qubitron.unitary(circ), atol=1e-7)


def test_clifford_decompose_by_reconstruction():
    """Validate the decomposition of random Clifford Tableau by reconstruction.

    This approach can validate large number of qubits compared with the unitary one.
    """
    n, num_ops = 100, 500
    gate_candidate = [qubitron.X, qubitron.Y, qubitron.Z, qubitron.H, qubitron.S, qubitron.CNOT, qubitron.CZ]
    for seed in range(10):
        prng = np.random.RandomState(seed)
        t = qubitron.CliffordTableau(num_qubits=n)
        qubits = qubitron.LineQubit.range(n)
        expect_circ = qubitron.Circuit()
        args = qubitron.CliffordTableauSimulationState(tableau=t, qubits=qubits, prng=prng)
        for _ in range(num_ops):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            qubitron.act_on(
                gate_candidate[g], args, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            expect_circ.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        ops = qubitron.decompose_clifford_tableau_to_operations(qubits, args.tableau)

        reconstruct_t = qubitron.CliffordTableau(num_qubits=n)
        reconstruct_args = qubitron.CliffordTableauSimulationState(
            tableau=reconstruct_t, qubits=qubits, prng=prng
        )
        for op in ops:
            qubitron.act_on(op.gate, reconstruct_args, qubits=op.qubits, allow_decompose=False)

        assert t == reconstruct_t
