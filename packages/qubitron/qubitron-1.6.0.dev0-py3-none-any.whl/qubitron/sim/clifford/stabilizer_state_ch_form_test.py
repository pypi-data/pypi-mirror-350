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

import numpy as np
import pytest

import qubitron
import qubitron.testing

# TODO: This and clifford tableau need tests.
# Github issue: https://github.com/amyssnippet/Qubitron/issues/3021


def test_initial_state() -> None:
    with pytest.raises(ValueError, match='Out of range'):
        _ = qubitron.StabilizerStateChForm(initial_state=-31, num_qubits=5)
    with pytest.raises(ValueError, match='Out of range'):
        _ = qubitron.StabilizerStateChForm(initial_state=32, num_qubits=5)
    state = qubitron.StabilizerStateChForm(initial_state=23, num_qubits=5)
    expected_state_vector = np.zeros(32)
    expected_state_vector[23] = 1
    np.testing.assert_allclose(state.state_vector(), expected_state_vector)


def test_run() -> None:
    (q0, q1, q2) = (qubitron.LineQubit(0), qubitron.LineQubit(1), qubitron.LineQubit(2))

    """
    0: ───H───@───────────────X───M───────────
              │
    1: ───────X───@───────X───────────X───M───
                  │                   │
    2: ───────────X───M───────────────@───────

    After the third moment, before the measurement, the state is |000> + |111>.
    After measurement of q2, q0 and q1 both get a bit flip, so the q0
    measurement always yields opposite of the q2 measurement. q1 has an
    additional controlled not from q2, making it yield 1 always when measured.
    If there were no measurements in the circuit, the final state would be
    |110> + |011>.
    """
    circuit = qubitron.Circuit(
        qubitron.H(q0),
        qubitron.CNOT(q0, q1),
        qubitron.CNOT(q1, q2),
        qubitron.measure(q2),
        qubitron.X(q1),
        qubitron.X(q0),
        qubitron.measure(q0),
        qubitron.CNOT(q2, q1),
        qubitron.measure(q1),
        strategy=qubitron.InsertStrategy.NEW,
    )
    for _ in range(10):
        state = qubitron.StabilizerStateChForm(num_qubits=3)
        classical_data = qubitron.ClassicalDataDictionaryStore()
        for op in circuit.all_operations():
            args = qubitron.StabilizerChFormSimulationState(
                qubits=list(circuit.all_qubits()),
                prng=np.random.RandomState(),
                classical_data=classical_data,
                initial_state=state,
            )
            qubitron.act_on(op, args)
        measurements = {str(k): list(v[-1]) for k, v in classical_data.records.items()}
        assert measurements['q(1)'] == [1]
        assert measurements['q(0)'] != measurements['q(2)']
