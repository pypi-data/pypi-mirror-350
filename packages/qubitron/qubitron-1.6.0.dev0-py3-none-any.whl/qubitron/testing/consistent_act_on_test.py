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

from typing import Sequence

import numpy as np
import pytest

import qubitron


class GoodGate(qubitron.testing.SingleQubitGate):
    def _unitary_(self):
        return np.array([[0, 1], [1, 0]])

    def _act_on_(self, sim_state: qubitron.SimulationStateBase, qubits: Sequence[qubitron.Qid]):
        if isinstance(sim_state, qubitron.CliffordTableauSimulationState):
            tableau = sim_state.tableau
            q = sim_state.qubit_map[qubits[0]]
            tableau.rs[:] ^= tableau.zs[:, q]
            return True
        return NotImplemented


class BadGate(qubitron.testing.SingleQubitGate):
    def _unitary_(self):
        return np.array([[0, 1j], [1, 0]])

    def _act_on_(self, sim_state: qubitron.SimulationStateBase, qubits: Sequence[qubitron.Qid]):
        if isinstance(sim_state, qubitron.CliffordTableauSimulationState):
            tableau = sim_state.tableau
            q = sim_state.qubit_map[qubits[0]]
            tableau.rs[:] ^= tableau.zs[:, q]
            return True
        return NotImplemented


class UnimplementedGate(qubitron.testing.TwoQubitGate):
    pass


class UnimplementedUnitaryGate(qubitron.testing.TwoQubitGate):
    def _unitary_(self):
        return np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])


def test_assert_act_on_clifford_tableau_effect_matches_unitary() -> None:
    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(GoodGate())
    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
        GoodGate().on(qubitron.LineQubit(1))
    )
    with pytest.raises(
        AssertionError,
        match='act_on clifford tableau is not consistent with final_state_vector simulation.',
    ):
        qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(BadGate())

    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(UnimplementedGate())
    with pytest.raises(
        AssertionError, match='Could not assert if any act_on methods were implemented'
    ):
        qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
            UnimplementedGate(), assert_tableau_implemented=True
        )
    with pytest.raises(
        AssertionError, match='Could not assert if any act_on methods were implemented'
    ):
        qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
            UnimplementedGate(), assert_ch_form_implemented=True
        )

    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(UnimplementedUnitaryGate())
    with pytest.raises(AssertionError, match='Failed to generate final tableau'):
        qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
            UnimplementedUnitaryGate(), assert_tableau_implemented=True
        )
    with pytest.raises(AssertionError, match='Failed to generate final stabilizer state'):
        qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
            UnimplementedUnitaryGate(), assert_ch_form_implemented=True
        )
