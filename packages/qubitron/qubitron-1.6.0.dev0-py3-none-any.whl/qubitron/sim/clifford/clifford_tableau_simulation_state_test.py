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

import numpy as np
import pytest

import qubitron


def test_unitary_fallback() -> None:
    class UnitaryXGate(qubitron.testing.SingleQubitGate):
        def _unitary_(self):
            return np.array([[0, 1], [1, 0]])

    class UnitaryYGate(qubitron.Gate):
        def _qid_shape_(self) -> tuple[int, ...]:
            return (2,)

        def _unitary_(self):
            return np.array([[0, -1j], [1j, 0]])

    original_tableau = qubitron.CliffordTableau(num_qubits=3)
    args = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(3),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(UnitaryXGate(), args, [qubitron.LineQubit(1)])
    assert args.tableau == qubitron.CliffordTableau(num_qubits=3, initial_state=2)

    args = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(3),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(UnitaryYGate(), args, [qubitron.LineQubit(1)])
    expected_args = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(3),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(qubitron.Y, expected_args, [qubitron.LineQubit(1)])
    assert args.tableau == expected_args.tableau


def test_cannot_act() -> None:
    class NoDetails:
        pass

    class NoDetailsSingleQubitGate(qubitron.testing.SingleQubitGate):
        pass

    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=3),
        qubits=qubitron.LineQubit.range(3),
        prng=np.random.RandomState(),
    )

    with pytest.raises(TypeError, match="no _num_qubits_ or _qid_shape_"):
        qubitron.act_on(NoDetails(), args, [qubitron.LineQubit(1)])

    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(NoDetailsSingleQubitGate(), args, [qubitron.LineQubit(1)])


def test_copy() -> None:
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=3),
        qubits=qubitron.LineQubit.range(3),
        prng=np.random.RandomState(),
    )
    args1 = args.copy()
    assert isinstance(args1, qubitron.CliffordTableauSimulationState)
    assert args is not args1
    assert args.tableau is not args1.tableau
    assert args.tableau == args1.tableau
    assert args.qubits is args1.qubits
    assert args.qubit_map == args1.qubit_map
    assert args.prng is args1.prng
    assert args.log_of_measurement_results is not args1.log_of_measurement_results
    assert args.log_of_measurement_results == args1.log_of_measurement_results
