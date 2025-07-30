# Copyright 2019 The Qubitron Developers
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
import sympy

import qubitron


def test_init():
    op = qubitron.global_phase_operation(1j)
    assert op.gate.coefficient == 1j
    assert op.qubits == ()
    assert op.with_qubits() == op
    assert qubitron.has_stabilizer_effect(op)

    with pytest.raises(ValueError, match='not unitary'):
        _ = qubitron.global_phase_operation(2)
    with pytest.raises(ValueError, match='0 qubits'):
        _ = qubitron.global_phase_operation(1j).with_qubits(qubitron.LineQubit(0))


def test_protocols():
    for p in [1, 1j, -1, sympy.Symbol('s')]:
        qubitron.testing.assert_implements_consistent_protocols(qubitron.global_phase_operation(p))

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.global_phase_operation(1j)), np.array([[1j]]), atol=1e-8
    )


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_act_on_tableau(phase):
    original_tableau = qubitron.CliffordTableau(0)
    args = qubitron.CliffordTableauSimulationState(original_tableau.copy(), np.random.RandomState())
    qubitron.act_on(qubitron.global_phase_operation(phase), args, allow_decompose=False)
    assert args.tableau == original_tableau


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_act_on_ch_form(phase):
    state = qubitron.StabilizerStateChForm(0)
    args = qubitron.StabilizerChFormSimulationState(
        qubits=[], prng=np.random.RandomState(), initial_state=state
    )
    qubitron.act_on(qubitron.global_phase_operation(phase), args, allow_decompose=False)
    assert state.state_vector() == [[phase]]


def test_str():
    assert str(qubitron.global_phase_operation(1j)) == '1j'


def test_repr():
    op = qubitron.global_phase_operation(1j)
    qubitron.testing.assert_equivalent_repr(op)


def test_diagram():
    a, b = qubitron.LineQubit.range(2)
    x, y = qubitron.LineQubit.range(10, 12)

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            [qubitron.Moment([qubitron.CNOT(a, x), qubitron.CNOT(b, y), qubitron.global_phase_operation(-1)])]
        ),
        """
                ┌──┐
0: ──────────────@─────
                 │
1: ──────────────┼@────
                 ││
10: ─────────────X┼────
                  │
11: ──────────────X────

global phase:    π
                └──┘
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            [
                qubitron.Moment(
                    [
                        qubitron.CNOT(a, x),
                        qubitron.CNOT(b, y),
                        qubitron.global_phase_operation(-1),
                        qubitron.global_phase_operation(-1),
                    ]
                )
            ]
        ),
        """
                ┌──┐
0: ──────────────@─────
                 │
1: ──────────────┼@────
                 ││
10: ─────────────X┼────
                  │
11: ──────────────X────

global phase:
                └──┘
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            [
                qubitron.Moment(
                    [
                        qubitron.CNOT(a, x),
                        qubitron.CNOT(b, y),
                        qubitron.global_phase_operation(-1),
                        qubitron.global_phase_operation(-1),
                    ]
                ),
                qubitron.Moment([qubitron.global_phase_operation(1j)]),
                qubitron.Moment([qubitron.X(a)]),
            ]
        ),
        """
                ┌──┐
0: ──────────────@────────────X───
                 │
1: ──────────────┼@───────────────
                 ││
10: ─────────────X┼───────────────
                  │
11: ──────────────X───────────────

global phase:          0.5π
                └──┘
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit([qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.global_phase_operation(-1j)])]),
        """
0: ─────────────X───────────

global phase:       -0.5π
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.global_phase_operation(np.exp(1j))])]),
        """
0: ─────────────X────────

global phase:   0.318π
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit([qubitron.Moment([qubitron.X(a), qubitron.global_phase_operation(np.exp(1j))])]),
        """
0: ─────────────X──────────

global phase:   0.31831π
        """,
        precision=5,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            [
                qubitron.Moment([qubitron.X(a), qubitron.global_phase_operation(1j)]),
                qubitron.Moment([qubitron.global_phase_operation(-1j)]),
            ]
        ),
        """
0: -------------X----------------

global phase:   0.5pi   -0.5pi
        """,
        use_unicode_characters=False,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit([qubitron.Moment([qubitron.global_phase_operation(-1j)])]),
        """
global phase:   -0.5π
        """,
    )


def test_gate_init():
    gate = qubitron.GlobalPhaseGate(1j)
    assert gate.coefficient == 1j
    assert isinstance(gate.on(), qubitron.GateOperation)
    assert gate.on().gate == gate
    assert qubitron.has_stabilizer_effect(gate)

    with pytest.raises(ValueError, match='Coefficient is not unitary'):
        _ = qubitron.GlobalPhaseGate(2)
    with pytest.raises(ValueError, match='Wrong number of qubits'):
        _ = gate.on(qubitron.LineQubit(0))


def test_gate_protocols():
    for p in [1, 1j, -1]:
        qubitron.testing.assert_implements_consistent_protocols(qubitron.GlobalPhaseGate(p))

    np.testing.assert_allclose(qubitron.unitary(qubitron.GlobalPhaseGate(1j)), np.array([[1j]]), atol=1e-8)


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_gate_act_on_tableau(phase):
    original_tableau = qubitron.CliffordTableau(0)
    args = qubitron.CliffordTableauSimulationState(original_tableau.copy(), np.random.RandomState())
    qubitron.act_on(qubitron.GlobalPhaseGate(phase), args, qubits=(), allow_decompose=False)
    assert args.tableau == original_tableau


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_gate_act_on_ch_form(phase):
    state = qubitron.StabilizerStateChForm(0)
    args = qubitron.StabilizerChFormSimulationState(
        qubits=[], prng=np.random.RandomState(), initial_state=state
    )
    qubitron.act_on(qubitron.GlobalPhaseGate(phase), args, qubits=(), allow_decompose=False)
    assert state.state_vector() == [[phase]]


def test_gate_str():
    assert str(qubitron.GlobalPhaseGate(1j)) == '1j'


def test_gate_repr():
    gate = qubitron.GlobalPhaseGate(1j)
    qubitron.testing.assert_equivalent_repr(gate)


def test_gate_op_repr():
    gate = qubitron.GlobalPhaseGate(1j)
    qubitron.testing.assert_equivalent_repr(gate.on())


def test_gate_global_phase_op_json_dict():
    assert qubitron.GlobalPhaseGate(-1j)._json_dict_() == {'coefficient': -1j}


def test_parameterization():
    t = sympy.Symbol('t')
    gpt = qubitron.GlobalPhaseGate(coefficient=t)
    assert qubitron.is_parameterized(gpt)
    assert qubitron.parameter_names(gpt) == {'t'}
    assert not qubitron.has_unitary(gpt)
    assert gpt.coefficient == t
    assert (gpt**2).coefficient == t**2


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve(resolve_fn):
    t = sympy.Symbol('t')
    gpt = qubitron.GlobalPhaseGate(coefficient=t)
    assert resolve_fn(gpt, {'t': -1}) == qubitron.GlobalPhaseGate(coefficient=-1)


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_resolve_error(resolve_fn):
    t = sympy.Symbol('t')
    gpt = qubitron.GlobalPhaseGate(coefficient=t)
    with pytest.raises(ValueError, match='Coefficient is not unitary'):
        resolve_fn(gpt, {'t': -2})


@pytest.mark.parametrize(
    'coeff, exp', [(-1, 1), (1j, 0.5), (-1j, -0.5), (1 / np.sqrt(2) * (1 + 1j), 0.25)]
)
def test_global_phase_gate_controlled(coeff, exp):
    g = qubitron.GlobalPhaseGate(coeff)
    op = qubitron.global_phase_operation(coeff)
    q = qubitron.LineQubit.range(3)
    for num_controls, target_gate in zip(range(1, 4), [qubitron.Z, qubitron.CZ, qubitron.CCZ]):
        assert g.controlled(num_controls) == target_gate**exp
        np.testing.assert_allclose(
            qubitron.unitary(qubitron.ControlledGate(g, num_controls)),
            qubitron.unitary(g.controlled(num_controls)),
        )
        assert op.controlled_by(*q[:num_controls]) == target_gate(*q[:num_controls]) ** exp
    assert g.controlled(control_values=[0]) == qubitron.ControlledGate(g, control_values=[0])
    xor_control_values = qubitron.SumOfProducts(((0, 0), (1, 1)))
    assert g.controlled(control_values=xor_control_values) == qubitron.ControlledGate(
        g, control_values=xor_control_values
    )
