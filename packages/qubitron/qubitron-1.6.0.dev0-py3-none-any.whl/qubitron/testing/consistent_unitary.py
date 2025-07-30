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

from typing import Any

import numpy as np

import qubitron


def assert_unitary_is_consistent(val: Any, ignoring_global_phase: bool = False):
    if not isinstance(val, (qubitron.Operation, qubitron.Gate)):
        return

    if not qubitron.has_unitary(val):
        return

    # Ensure that `u` is a unitary.
    u = qubitron.unitary(val)
    assert not (u is None or u is NotImplemented)
    assert qubitron.is_unitary(u)

    if isinstance(val, qubitron.Operation):
        qubits = val.qubits
        decomposition = qubitron.decompose_once(val, default=None)
    else:
        qubits = tuple(qubitron.LineQid.for_gate(val))
        decomposition = qubitron.decompose_once_with_qubits(val, qubits, default=None)

    if decomposition is None or decomposition is NotImplemented:
        return

    c = qubitron.Circuit(decomposition)
    if len(c.all_qubits().difference(qubits)) == 0:
        return

    clean_qubits = tuple(q for q in c.all_qubits() if isinstance(q, qubitron.ops.CleanQubit))
    borrowable_qubits = tuple(q for q in c.all_qubits() if isinstance(q, qubitron.ops.BorrowableQubit))
    qubit_order = clean_qubits + borrowable_qubits + qubits

    # Check that the decomposition uses all data qubits in addition to
    # clean and/or borrowable qubits.
    assert set(qubit_order) == c.all_qubits()

    qid_shape = qubitron.qid_shape(qubit_order)
    full_unitary = qubitron.apply_unitaries(
        decomposition,
        qubits=qubit_order,
        args=qubitron.ApplyUnitaryArgs.for_unitary(qid_shape=qid_shape),
        default=None,
    )
    if full_unitary is None:
        raise ValueError(f'apply_unitaries failed on the decomposition of {val}')
    vol = np.prod(qid_shape, dtype=np.int64)
    full_unitary = full_unitary.reshape((vol, vol))

    vol = np.prod(qubitron.qid_shape(borrowable_qubits + qubits), dtype=np.int64)

    # Extract the submatrix acting on the |0..0> subspace of clean qubits.
    # This submatirx must be a unitary.
    clean_qubits_zero_subspace = full_unitary[:vol, :vol]

    # If the borrowable qubits are restored to their initial state, then
    # the decomposition's effect on it is the identity matrix.
    # This means that the `clean_qubits_zero_subspace` must be I \otimes u.
    # So checking that `clean_qubits_zero_subspace` is I \otimes u checks correctness
    # for both clean and borrowable qubits at the same time.
    expected = np.kron(np.eye(2 ** len(borrowable_qubits), dtype=np.complex128), u)

    if ignoring_global_phase:
        qubitron.testing.assert_allclose_up_to_global_phase(
            clean_qubits_zero_subspace, expected, atol=1e-8
        )
    else:
        np.testing.assert_allclose(clean_qubits_zero_subspace, expected, atol=1e-8)
