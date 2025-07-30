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


def test_init_state() -> None:
    args = qubitron.StabilizerChFormSimulationState(qubits=qubitron.LineQubit.range(1), initial_state=1)
    np.testing.assert_allclose(args.state.state_vector(), [0, 1])
    with pytest.raises(ValueError, match='Must specify qubits'):
        _ = qubitron.StabilizerChFormSimulationState(initial_state=1)


def test_cannot_act() -> None:
    class NoDetails(qubitron.testing.SingleQubitGate):
        pass

    args = qubitron.StabilizerChFormSimulationState(qubits=[], prng=np.random.RandomState())

    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(NoDetails(), args, qubits=())


def test_gate_with_act_on() -> None:
    class CustomGate(qubitron.testing.SingleQubitGate):
        def _act_on_(self, sim_state, qubits):
            if isinstance(sim_state, qubitron.StabilizerChFormSimulationState):
                qubit = sim_state.qubit_map[qubits[0]]
                sim_state.state.gamma[qubit] += 1
                return True

    state = qubitron.StabilizerStateChForm(num_qubits=3)
    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState(), initial_state=state
    )

    qubitron.act_on(CustomGate(), args, [qubitron.LineQubit(1)])

    np.testing.assert_allclose(state.gamma, [0, 1, 0])


def test_unitary_fallback_y() -> None:
    class UnitaryYGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _unitary_(self):
            return np.array([[0, -1j], [1j, 0]])

    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState()
    )
    qubitron.act_on(UnitaryYGate(), args, [qubitron.LineQubit(1)])
    expected_args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.Y, expected_args, [qubitron.LineQubit(1)])
    np.testing.assert_allclose(args.state.state_vector(), expected_args.state.state_vector())


def test_unitary_fallback_h() -> None:
    class UnitaryHGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _unitary_(self):
            return np.array([[1, 1], [1, -1]]) / (2**0.5)

    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState()
    )
    qubitron.act_on(UnitaryHGate(), args, [qubitron.LineQubit(1)])
    expected_args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.H, expected_args, [qubitron.LineQubit(1)])
    np.testing.assert_allclose(args.state.state_vector(), expected_args.state.state_vector())


def test_copy() -> None:
    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState()
    )
    args1 = args.copy()
    assert isinstance(args1, qubitron.StabilizerChFormSimulationState)
    assert args is not args1
    assert args.state is not args1.state
    np.testing.assert_equal(args.state.state_vector(), args1.state.state_vector())
    assert args.qubits == args1.qubits
    assert args.prng is args1.prng
    assert args.log_of_measurement_results is not args1.log_of_measurement_results
    assert args.log_of_measurement_results == args1.log_of_measurement_results
