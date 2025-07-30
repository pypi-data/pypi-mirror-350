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

import numpy as np
import pytest

import qubitron


def _operations_to_matrix(operations, qubits):
    return qubitron.Circuit(operations).unitary(
        qubit_order=qubitron.QubitOrder.explicit(qubits), qubits_that_should_be_present=qubits
    )


def _random_single_MS_effect():
    t = random.random()
    s = np.sin(t)
    c = np.cos(t)
    return qubitron.dot(
        qubitron.kron(qubitron.testing.random_unitary(2), qubitron.testing.random_unitary(2)),
        np.array([[c, 0, 0, -1j * s], [0, c, -1j * s, 0], [0, -1j * s, c, 0], [-1j * s, 0, 0, c]]),
        qubitron.kron(qubitron.testing.random_unitary(2), qubitron.testing.random_unitary(2)),
    )


def _random_double_MS_effect():
    t1 = random.random()
    s1 = np.sin(t1)
    c1 = np.cos(t1)

    t2 = random.random()
    s2 = np.sin(t2)
    c2 = np.cos(t2)
    return qubitron.dot(
        qubitron.kron(qubitron.testing.random_unitary(2), qubitron.testing.random_unitary(2)),
        np.array(
            [[c1, 0, 0, -1j * s1], [0, c1, -1j * s1, 0], [0, -1j * s1, c1, 0], [-1j * s1, 0, 0, c1]]
        ),
        qubitron.kron(qubitron.testing.random_unitary(2), qubitron.testing.random_unitary(2)),
        np.array(
            [[c2, 0, 0, -1j * s2], [0, c2, -1j * s2, 0], [0, -1j * s2, c2, 0], [-1j * s2, 0, 0, c2]]
        ),
        qubitron.kron(qubitron.testing.random_unitary(2), qubitron.testing.random_unitary(2)),
    )


def assert_ops_implement_unitary(q0, q1, operations, intended_effect, atol=0.01):
    actual_effect = _operations_to_matrix(operations, (q0, q1))
    assert qubitron.allclose_up_to_global_phase(actual_effect, intended_effect, atol=atol)


def assert_ms_depth_below(operations, threshold):
    total_ms = 0

    for op in operations:
        assert len(op.qubits) <= 2
        if len(op.qubits) == 2:
            assert isinstance(op, qubitron.GateOperation)
            assert isinstance(op.gate, qubitron.XXPowGate)
            total_ms += abs(op.gate.exponent)
    assert total_ms <= threshold


# yapf: disable
@pytest.mark.parametrize('max_ms_depth,effect', [
    (0, np.eye(4)),
    (0, np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0j]
    ])),
    (1, qubitron.unitary(qubitron.ms(np.pi/4))),

    (0, qubitron.unitary(qubitron.CZ ** 0.00000001)),
    (0.5, qubitron.unitary(qubitron.CZ ** 0.5)),

    (1, qubitron.unitary(qubitron.CZ)),
    (1, qubitron.unitary(qubitron.CNOT)),
    (1, np.array([
        [1, 0, 0, 1j],
        [0, 1, 1j, 0],
        [0, 1j, 1, 0],
        [1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),
    (1, np.array([
        [1, 0, 0, -1j],
        [0, 1, -1j, 0],
        [0, -1j, 1, 0],
        [-1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),
    (1, np.array([
        [1, 0, 0, 1j],
        [0, 1, -1j, 0],
        [0, -1j, 1, 0],
        [1j, 0, 0, 1],
    ]) * np.sqrt(0.5)),

    (1.5, qubitron.map_eigenvalues(qubitron.unitary(qubitron.SWAP),
                               lambda e: e ** 0.5)),

    (2, qubitron.unitary(qubitron.SWAP).dot(qubitron.unitary(qubitron.CZ))),

    (3, qubitron.unitary(qubitron.SWAP)),
    (3, np.array([
        [0, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0j],
    ])),
] + [
    (1, _random_single_MS_effect()) for _ in range(10)
] + [
    (3, qubitron.testing.random_unitary(4)) for _ in range(10)
] + [
    (2, _random_double_MS_effect()) for _ in range(10)
])
# yapf: enable
def test_two_to_ops(max_ms_depth: int, effect: np.ndarray) -> None:
    q0 = qubitron.NamedQubit('q0')
    q1 = qubitron.NamedQubit('q1')

    operations = qubitron.two_qubit_matrix_to_ion_operations(q0, q1, effect)
    assert_ops_implement_unitary(q0, q1, operations, effect)
    assert_ms_depth_below(operations, max_ms_depth)
