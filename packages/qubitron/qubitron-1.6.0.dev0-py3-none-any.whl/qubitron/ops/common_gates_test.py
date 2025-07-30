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
import sympy

import qubitron
from qubitron.protocols.act_on_protocol_test import ExampleSimulationState

H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
HH = qubitron.kron(H, H)
QFT2 = np.array([[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]]) * 0.5


@pytest.mark.parametrize(
    'eigen_gate_type', [qubitron.CZPowGate, qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate]
)
def test_phase_insensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    qubitron.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


@pytest.mark.parametrize('eigen_gate_type', [qubitron.CNotPowGate, qubitron.HPowGate])
def test_phase_sensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    qubitron.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


def test_cz_init():
    assert qubitron.CZPowGate(exponent=0.5).exponent == 0.5
    assert qubitron.CZPowGate(exponent=5).exponent == 5
    assert (qubitron.CZ**0.5).exponent == 0.5


@pytest.mark.parametrize('theta,pi', [(0.4, np.pi), (sympy.Symbol("theta"), sympy.pi)])
def test_transformations(theta, pi):
    initialRx = qubitron.rx(theta)
    expectedPowx = qubitron.X ** (theta / pi)
    receivedPowx = initialRx.with_canonical_global_phase()
    backToRx = receivedPowx.in_su2()
    assert receivedPowx == expectedPowx
    assert backToRx == initialRx
    initialRy = qubitron.ry(theta)
    expectedPowy = qubitron.Y ** (theta / pi)
    receivedPowy = initialRy.with_canonical_global_phase()
    backToRy = receivedPowy.in_su2()
    assert receivedPowy == expectedPowy
    assert backToRy == initialRy
    initialRz = qubitron.rz(theta)
    expectedPowz = qubitron.Z ** (theta / pi)
    receivedPowz = initialRz.with_canonical_global_phase()
    backToRz = receivedPowz.in_su2()
    assert receivedPowz == expectedPowz
    assert backToRz == initialRz


def test_cz_str():
    assert str(qubitron.CZ) == 'CZ'
    assert str(qubitron.CZ**0.5) == 'CZ**0.5'
    assert str(qubitron.CZ**-0.25) == 'CZ**-0.25'


def test_cz_repr():
    assert repr(qubitron.CZ) == 'qubitron.CZ'
    assert repr(qubitron.CZ**0.5) == '(qubitron.CZ**0.5)'
    assert repr(qubitron.CZ**-0.25) == '(qubitron.CZ**-0.25)'


def test_cz_unitary():
    assert np.allclose(
        qubitron.unitary(qubitron.CZ), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
    )

    assert np.allclose(
        qubitron.unitary(qubitron.CZ**0.5),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]]),
    )

    assert np.allclose(
        qubitron.unitary(qubitron.CZ**0), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    )

    assert np.allclose(
        qubitron.unitary(qubitron.CZ**-0.5),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1j]]),
    )


def test_z_init():
    z = qubitron.ZPowGate(exponent=5)
    assert z.exponent == 5

    # Canonicalizes exponent for equality, but keeps the inner details.
    assert qubitron.Z**0.5 != qubitron.Z**-0.5
    assert (qubitron.Z**-1) ** 0.5 == qubitron.Z**-0.5
    assert qubitron.Z**-1 == qubitron.Z


@pytest.mark.parametrize(
    'input_gate, specialized_output, base_gate',
    [
        (qubitron.Z, qubitron.CZ, qubitron.Z),
        (qubitron.CZ, qubitron.CCZ, qubitron.Z),
        (qubitron.X, qubitron.CX, qubitron.X),
        (qubitron.CX, qubitron.CCX, qubitron.X),
        (qubitron.ZPowGate(exponent=0.5), qubitron.CZPowGate(exponent=0.5), qubitron.S),
        (qubitron.CZPowGate(exponent=0.5), qubitron.CCZPowGate(exponent=0.5), qubitron.S),
        (qubitron.XPowGate(exponent=0.5), qubitron.CXPowGate(exponent=0.5), qubitron.XPowGate(exponent=0.5)),
        (qubitron.CXPowGate(exponent=0.5), qubitron.CCXPowGate(exponent=0.5), qubitron.XPowGate(exponent=0.5)),
    ],
)
def test_specialized_control(input_gate, specialized_output, base_gate):
    # Single qubit control on the input gate gives the specialized output
    assert input_gate.controlled() == specialized_output
    assert input_gate.controlled(num_controls=1) == specialized_output
    assert input_gate.controlled(control_values=((1,),)) == specialized_output
    assert input_gate.controlled(control_values=qubitron.SumOfProducts([[1]])) == specialized_output
    assert input_gate.controlled(control_qid_shape=(2,)) == specialized_output
    assert np.allclose(
        qubitron.unitary(specialized_output),
        qubitron.unitary(qubitron.ControlledGate(input_gate, num_controls=1)),
    )

    # For multi-qudit controls, if the last control is a qubit with control
    # value 1, construct the specialized output leaving the rest of the
    # controls as they are.
    assert input_gate.controlled().controlled() == specialized_output.controlled(num_controls=1)
    assert input_gate.controlled(num_controls=2) == specialized_output.controlled(num_controls=1)
    assert input_gate.controlled(
        control_values=((0,), (0,), (1,))
    ) == specialized_output.controlled(num_controls=2, control_values=((0,), (0,)))
    assert input_gate.controlled(control_qid_shape=(3, 3, 2)) == specialized_output.controlled(
        num_controls=2, control_qid_shape=(3, 3)
    )
    assert input_gate.controlled(control_qid_shape=(2,)).controlled(
        control_qid_shape=(3,)
    ).controlled(control_qid_shape=(4,)) != specialized_output.controlled(
        num_controls=2, control_qid_shape=(3, 4)
    )

    # When a control_value 1 qubit is not acting first, results in a regular
    # ControlledGate on the base gate instance, with any extra control layer
    # of the input gate being absorbed into the ControlledGate.
    absorbed = 0 if base_gate == input_gate else 1
    absorbed_values = ((1,),) * absorbed
    absorbed_shape = (2,) * absorbed
    assert input_gate.controlled(num_controls=1, control_qid_shape=(3,)) == qubitron.ControlledGate(
        base_gate, num_controls=1 + absorbed, control_qid_shape=(3,) + absorbed_shape
    )
    assert input_gate.controlled(control_values=((0,), (1,), (0,))) == qubitron.ControlledGate(
        base_gate, num_controls=3 + absorbed, control_values=((0,), (1,), (0,)) + absorbed_values
    )
    assert input_gate.controlled(control_qid_shape=(3, 2, 3)) == qubitron.ControlledGate(
        base_gate, num_controls=3 + absorbed, control_qid_shape=(3, 2, 3) + absorbed_shape
    )
    assert input_gate.controlled(control_qid_shape=(3,)).controlled(
        control_qid_shape=(2,)
    ).controlled(control_qid_shape=(4,)) != qubitron.ControlledGate(
        base_gate, num_controls=3 + absorbed, control_qid_shape=(3, 2, 4) + absorbed_shape
    )


@pytest.mark.parametrize(
    'input_gate, specialized_output',
    [
        (qubitron.Z, qubitron.CCZ),
        (qubitron.X, qubitron.CCX),
        (qubitron.ZPowGate(exponent=0.5), qubitron.CCZPowGate(exponent=0.5)),
        (qubitron.XPowGate(exponent=0.5), qubitron.CCXPowGate(exponent=0.5)),
    ],
)
def test_specialized_control_two_step(input_gate, specialized_output):
    # Two-qubit control on the input gate gives the specialized output
    assert input_gate.controlled().controlled() == specialized_output
    assert input_gate.controlled(num_controls=2) == specialized_output
    assert input_gate.controlled(control_values=[1, 1]) == specialized_output
    assert input_gate.controlled(control_values=qubitron.SumOfProducts([[1, 1]])) == specialized_output
    assert input_gate.controlled(control_qid_shape=(2, 2)) == specialized_output
    assert np.allclose(
        qubitron.unitary(specialized_output),
        qubitron.unitary(qubitron.ControlledGate(input_gate, num_controls=2)),
    )


@pytest.mark.parametrize(
    'gate, specialized_type',
    [
        (qubitron.ZPowGate(global_shift=-0.5, exponent=0.5), qubitron.CZPowGate),
        (qubitron.CZPowGate(global_shift=-0.5, exponent=0.5), qubitron.CCZPowGate),
        (qubitron.XPowGate(global_shift=-0.5, exponent=0.5), qubitron.CXPowGate),
        (qubitron.CXPowGate(global_shift=-0.5, exponent=0.5), qubitron.CCXPowGate),
    ],
)
def test_no_specialized_control_for_global_shift_non_zero(gate, specialized_type):
    assert not isinstance(gate.controlled(), specialized_type)


@pytest.mark.parametrize(
    'gate, matrix',
    [
        (qubitron.ZPowGate(global_shift=-0.5, exponent=1), np.diag([1, 1, -1j, 1j])),
        (qubitron.CZPowGate(global_shift=-0.5, exponent=1), np.diag([1, 1, 1, 1, -1j, -1j, -1j, 1j])),
        (
            qubitron.XPowGate(global_shift=-0.5, exponent=1),
            np.block(
                [[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), np.array([[0, -1j], [-1j, 0]])]]
            ),
        ),
        (
            qubitron.CXPowGate(global_shift=-0.5, exponent=1),
            np.block(
                [
                    [np.diag([1, 1, 1, 1, -1j, -1j]), np.zeros((6, 2))],
                    [np.zeros((2, 6)), np.array([[0, -1j], [-1j, 0]])],
                ]
            ),
        ),
    ],
)
def test_global_phase_controlled_gate(gate, matrix):
    np.testing.assert_equal(qubitron.unitary(gate.controlled()), matrix)


def test_rot_gates_eq():
    eq = qubitron.testing.EqualsTester()
    gates = [
        lambda p: qubitron.CZ**p,
        lambda p: qubitron.X**p,
        lambda p: qubitron.Y**p,
        lambda p: qubitron.Z**p,
        lambda p: qubitron.CNOT**p,
    ]
    for gate in gates:
        eq.add_equality_group(gate(3.5), gate(-0.5))
        eq.make_equality_group(lambda: gate(0))
        eq.make_equality_group(lambda: gate(0.5))

    eq.add_equality_group(qubitron.XPowGate(), qubitron.XPowGate(exponent=1), qubitron.X)
    eq.add_equality_group(qubitron.YPowGate(), qubitron.YPowGate(exponent=1), qubitron.Y)
    eq.add_equality_group(qubitron.ZPowGate(), qubitron.ZPowGate(exponent=1), qubitron.Z)
    eq.add_equality_group(
        qubitron.ZPowGate(exponent=1, global_shift=-0.5),
        qubitron.ZPowGate(exponent=5, global_shift=-0.5),
        qubitron.ZPowGate(exponent=5, global_shift=-0.1),
    )
    eq.add_equality_group(qubitron.ZPowGate(exponent=3, global_shift=-0.5))
    eq.add_equality_group(qubitron.ZPowGate(exponent=1, global_shift=-0.1))
    eq.add_equality_group(
        qubitron.CNotPowGate(), qubitron.CXPowGate(), qubitron.CNotPowGate(exponent=1), qubitron.CNOT
    )
    eq.add_equality_group(qubitron.CZPowGate(), qubitron.CZPowGate(exponent=1), qubitron.CZ)


def test_z_unitary():
    assert np.allclose(qubitron.unitary(qubitron.Z), np.array([[1, 0], [0, -1]]))
    assert np.allclose(qubitron.unitary(qubitron.Z**0.5), np.array([[1, 0], [0, 1j]]))
    assert np.allclose(qubitron.unitary(qubitron.Z**0), np.array([[1, 0], [0, 1]]))
    assert np.allclose(qubitron.unitary(qubitron.Z**-0.5), np.array([[1, 0], [0, -1j]]))


def test_y_unitary():
    assert np.allclose(qubitron.unitary(qubitron.Y), np.array([[0, -1j], [1j, 0]]))

    assert np.allclose(
        qubitron.unitary(qubitron.Y**0.5), np.array([[1 + 1j, -1 - 1j], [1 + 1j, 1 + 1j]]) / 2
    )

    assert np.allclose(qubitron.unitary(qubitron.Y**0), np.array([[1, 0], [0, 1]]))

    assert np.allclose(
        qubitron.unitary(qubitron.Y**-0.5), np.array([[1 - 1j, 1 - 1j], [-1 + 1j, 1 - 1j]]) / 2
    )


def test_x_unitary():
    assert np.allclose(qubitron.unitary(qubitron.X), np.array([[0, 1], [1, 0]]))

    assert np.allclose(
        qubitron.unitary(qubitron.X**0.5), np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2
    )

    assert np.allclose(qubitron.unitary(qubitron.X**0), np.array([[1, 0], [0, 1]]))

    assert np.allclose(
        qubitron.unitary(qubitron.X**-0.5), np.array([[1 - 1j, 1 + 1j], [1 + 1j, 1 - 1j]]) / 2
    )


def test_h_unitary():
    sqrt = qubitron.unitary(qubitron.H**0.5)
    m = np.dot(sqrt, sqrt)
    assert np.allclose(m, qubitron.unitary(qubitron.H), atol=1e-8)


def test_h_init():
    h = qubitron.HPowGate(exponent=0.5)
    assert h.exponent == 0.5


def test_h_str():
    assert str(qubitron.H) == 'H'
    assert str(qubitron.H**0.5) == 'H**0.5'


def test_phase_exponent():
    assert qubitron.XPowGate(exponent=0.5).phase_exponent == 0.0
    assert qubitron.YPowGate(exponent=0.5).phase_exponent == 0.5


def test_x_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.X, ExampleSimulationState(), qubits=())
    original_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=23)

    state = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(qubitron.X**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.X**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.X, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    qubitron.act_on(qubitron.X**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.X**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.X**2, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.X**foo, state, [qubitron.LineQubit(1)])


class iZGate(qubitron.testing.SingleQubitGate):
    """Equivalent to an iZ gate without _act_on_ defined on it."""

    def _unitary_(self):
        return np.array([[1j, 0], [0, -1j]])


class MinusOnePhaseGate(qubitron.testing.SingleQubitGate):
    """Equivalent to a -1 global phase without _act_on_ defined on it."""

    def _unitary_(self):
        return np.array([[-1, 0], [0, -1]])


def test_y_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.Y, ExampleSimulationState(), qubits=())
    original_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=23)

    state = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(qubitron.Y**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Y**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(iZGate(), state, [qubitron.LineQubit(1)])
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.Y, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(iZGate(), state, [qubitron.LineQubit(1)], allow_decompose=True)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    qubitron.act_on(qubitron.Y**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Y**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(iZGate(), state, [qubitron.LineQubit(1)])
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.Y**2, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.Y**foo, state, [qubitron.LineQubit(1)])


def test_z_h_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.Z, ExampleSimulationState(), qubits=())
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.H, ExampleSimulationState(), qubits=())
    original_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=23)

    state = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Z**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Z**0.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Z, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Z**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.Z**3.5, state, [qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.H, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.Z**2, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    qubitron.act_on(qubitron.H**2, state, [qubitron.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.Z**foo, state, [qubitron.LineQubit(1)])

    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.H**foo, state, [qubitron.LineQubit(1)])

    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.H**1.5, state, [qubitron.LineQubit(1)])


def test_cx_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.CX, ExampleSimulationState(), qubits=())
    original_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=31)

    state = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(qubitron.CX, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau.stabilizers() == [
        qubitron.DensePauliString('ZIIII', coefficient=-1),
        qubitron.DensePauliString('ZZIII', coefficient=-1),
        qubitron.DensePauliString('IIZII', coefficient=-1),
        qubitron.DensePauliString('IIIZI', coefficient=-1),
        qubitron.DensePauliString('IIIIZ', coefficient=-1),
    ]
    assert state.tableau.destabilizers() == [
        qubitron.DensePauliString('XXIII', coefficient=1),
        qubitron.DensePauliString('IXIII', coefficient=1),
        qubitron.DensePauliString('IIXII', coefficient=1),
        qubitron.DensePauliString('IIIXI', coefficient=1),
        qubitron.DensePauliString('IIIIX', coefficient=1),
    ]

    qubitron.act_on(qubitron.CX, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    qubitron.act_on(qubitron.CX**4, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.CX**foo, state, qubitron.LineQubit.range(2))

    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.CX**1.5, state, qubitron.LineQubit.range(2))


def test_cz_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.CZ, ExampleSimulationState(), qubits=())
    original_tableau = qubitron.CliffordTableau(num_qubits=5, initial_state=31)

    state = qubitron.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(qubitron.CZ, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau.stabilizers() == [
        qubitron.DensePauliString('ZIIII', coefficient=-1),
        qubitron.DensePauliString('IZIII', coefficient=-1),
        qubitron.DensePauliString('IIZII', coefficient=-1),
        qubitron.DensePauliString('IIIZI', coefficient=-1),
        qubitron.DensePauliString('IIIIZ', coefficient=-1),
    ]
    assert state.tableau.destabilizers() == [
        qubitron.DensePauliString('XZIII', coefficient=1),
        qubitron.DensePauliString('ZXIII', coefficient=1),
        qubitron.DensePauliString('IIXII', coefficient=1),
        qubitron.DensePauliString('IIIXI', coefficient=1),
        qubitron.DensePauliString('IIIIX', coefficient=1),
    ]

    qubitron.act_on(qubitron.CZ, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    qubitron.act_on(qubitron.CZ**4, state, qubitron.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.CZ**foo, state, qubitron.LineQubit.range(2))

    with pytest.raises(TypeError, match="Failed to act action on state"):
        qubitron.act_on(qubitron.CZ**1.5, state, qubitron.LineQubit.range(2))


def test_cz_act_on_equivalent_to_h_cx_h_tableau():
    state1 = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=2),
        qubits=qubitron.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    state2 = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=2),
        qubits=qubitron.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(qubitron.S, sim_state=state1, qubits=[qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.S, sim_state=state2, qubits=[qubitron.LineQubit(1)], allow_decompose=False)

    # state1 uses H*CNOT*H
    qubitron.act_on(qubitron.H, sim_state=state1, qubits=[qubitron.LineQubit(1)], allow_decompose=False)
    qubitron.act_on(qubitron.CNOT, sim_state=state1, qubits=qubitron.LineQubit.range(2), allow_decompose=False)
    qubitron.act_on(qubitron.H, sim_state=state1, qubits=[qubitron.LineQubit(1)], allow_decompose=False)
    # state2 uses CZ
    qubitron.act_on(qubitron.CZ, sim_state=state2, qubits=qubitron.LineQubit.range(2), allow_decompose=False)

    assert state1.tableau == state2.tableau


foo = sympy.Symbol('foo')


@pytest.mark.parametrize(
    'input_gate_sequence, outcome',
    [
        ([qubitron.X**foo], 'Error'),
        ([qubitron.X**0.25], 'Error'),
        ([qubitron.X**4], 'Original'),
        ([qubitron.X**0.5, qubitron.X**0.5], 'Flipped'),
        ([qubitron.X], 'Flipped'),
        ([qubitron.X**3.5, qubitron.X**3.5], 'Flipped'),
        ([qubitron.Y**foo], 'Error'),
        ([qubitron.Y**0.25], 'Error'),
        ([qubitron.Y**4], 'Original'),
        ([qubitron.Y**0.5, qubitron.Y**0.5, iZGate()], 'Flipped'),
        ([qubitron.Y, iZGate()], 'Flipped'),
        ([qubitron.Y**3.5, qubitron.Y**3.5, iZGate()], 'Flipped'),
        ([qubitron.Z**foo], 'Error'),
        ([qubitron.H**foo], 'Error'),
        ([qubitron.H**1.5], 'Error'),
        ([qubitron.Z**4], 'Original'),
        ([qubitron.H**4], 'Original'),
        ([qubitron.H, qubitron.S, qubitron.S, qubitron.H], 'Flipped'),
        ([qubitron.H, qubitron.Z, qubitron.H], 'Flipped'),
        ([qubitron.H, qubitron.Z**3.5, qubitron.Z**3.5, qubitron.H], 'Flipped'),
        ([qubitron.CX**foo], 'Error'),
        ([qubitron.CX**1.5], 'Error'),
        ([qubitron.CX**4], 'Original'),
        ([qubitron.CX], 'Flipped'),
        ([qubitron.CZ**foo], 'Error'),
        ([qubitron.CZ**1.5], 'Error'),
        ([qubitron.CZ**4], 'Original'),
        ([qubitron.CZ, MinusOnePhaseGate()], 'Original'),
    ],
)
def test_act_on_ch_form(input_gate_sequence, outcome):
    original_state = qubitron.StabilizerStateChForm(num_qubits=5, initial_state=31)
    num_qubits = qubitron.num_qubits(input_gate_sequence[0])
    if num_qubits == 1:
        qubits = [qubitron.LineQubit(1)]
    else:
        assert num_qubits == 2
        qubits = qubitron.LineQubit.range(2)
    state = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(2),
        prng=np.random.RandomState(),
        initial_state=original_state.copy(),
    )

    flipped_state = qubitron.StabilizerStateChForm(num_qubits=5, initial_state=23)

    if outcome == 'Error':
        with pytest.raises(TypeError, match="Failed to act action on state"):
            for input_gate in input_gate_sequence:
                qubitron.act_on(input_gate, state, qubits)
        return

    for input_gate in input_gate_sequence:
        qubitron.act_on(input_gate, state, qubits)

    if outcome == 'Original':
        np.testing.assert_allclose(state.state.state_vector(), original_state.state_vector())

    if outcome == 'Flipped':
        np.testing.assert_allclose(state.state.state_vector(), flipped_state.state_vector())


@pytest.mark.parametrize(
    'input_gate, assert_implemented',
    [
        (qubitron.X, True),
        (qubitron.Y, True),
        (qubitron.Z, True),
        (qubitron.X**0.5, True),
        (qubitron.Y**0.5, True),
        (qubitron.Z**0.5, True),
        (qubitron.X**3.5, True),
        (qubitron.Y**3.5, True),
        (qubitron.Z**3.5, True),
        (qubitron.X**4, True),
        (qubitron.Y**4, True),
        (qubitron.Z**4, True),
        (qubitron.H, True),
        (qubitron.CX, True),
        (qubitron.CZ, True),
        (qubitron.H**4, True),
        (qubitron.CX**4, True),
        (qubitron.CZ**4, True),
        # Unsupported gates should not fail too.
        (qubitron.X**0.25, False),
        (qubitron.Y**0.25, False),
        (qubitron.Z**0.25, False),
        (qubitron.H**0.5, False),
        (qubitron.CX**0.5, False),
        (qubitron.CZ**0.5, False),
    ],
)
def test_act_on_consistency(input_gate, assert_implemented):
    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(
        input_gate, assert_implemented, assert_implemented
    )


def test_runtime_types_of_rot_gates():
    for gate_type in [
        lambda p: qubitron.CZPowGate(exponent=p),
        lambda p: qubitron.XPowGate(exponent=p),
        lambda p: qubitron.YPowGate(exponent=p),
        lambda p: qubitron.ZPowGate(exponent=p),
    ]:
        p = gate_type(sympy.Symbol('a'))
        assert qubitron.unitary(p, None) is None
        assert qubitron.pow(p, 2, None) == gate_type(2 * sympy.Symbol('a'))
        assert qubitron.inverse(p, None) == gate_type(-sympy.Symbol('a'))

        c = gate_type(0.5)
        assert qubitron.unitary(c, None) is not None
        assert qubitron.pow(c, 2) == gate_type(1)
        assert qubitron.inverse(c) == gate_type(-0.5)


def test_interchangeable_qubit_eq():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    eq = qubitron.testing.EqualsTester()

    eq.add_equality_group(qubitron.CZ(a, b), qubitron.CZ(b, a))
    eq.add_equality_group(qubitron.CZ(a, c))

    eq.add_equality_group(qubitron.CNOT(a, b))
    eq.add_equality_group(qubitron.CNOT(b, a))
    eq.add_equality_group(qubitron.CNOT(a, c))


def test_identity_multiplication():
    a, b, c = qubitron.LineQubit.range(3)
    assert qubitron.I(a) * qubitron.CX(a, b) == qubitron.CX(a, b)
    assert qubitron.CX(a, b) * qubitron.I(a) == qubitron.CX(a, b)
    assert qubitron.CZ(a, b) * qubitron.I(c) == qubitron.CZ(a, b)
    assert qubitron.CX(a, b) ** 0.5 * qubitron.I(c) == qubitron.CX(a, b) ** 0.5
    assert qubitron.I(c) * qubitron.CZ(b, c) ** 0.5 == qubitron.CZ(b, c) ** 0.5
    assert qubitron.T(a) * qubitron.I(a) == qubitron.T(a)
    assert qubitron.T(b) * qubitron.I(c) == qubitron.T(b)
    assert qubitron.T(a) ** 0.25 * qubitron.I(c) == qubitron.T(a) ** 0.25
    assert qubitron.I(c) * qubitron.T(b) ** 0.25 == qubitron.T(b) ** 0.25


def test_text_diagrams():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(
        qubitron.X(a),
        qubitron.Y(a),
        qubitron.Z(a),
        qubitron.Z(a) ** sympy.Symbol('x'),
        qubitron.rx(sympy.Symbol('x')).on(a),
        qubitron.CZ(a, b),
        qubitron.CNOT(a, b),
        qubitron.CNOT(b, a),
        qubitron.CNOT(a, b) ** 0.5,
        qubitron.CNOT(b, a) ** 0.5,
        qubitron.H(a) ** 0.5,
        qubitron.I(a),
        qubitron.IdentityGate(2)(a, b),
        qubitron.cphase(sympy.pi * sympy.Symbol('t')).on(a, b),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───X───Y───Z───Z^x───Rx(x)───@───@───X───@───────X^0.5───H^0.5───I───I───@─────
                                │   │   │   │       │                   │   │
b: ─────────────────────────────@───X───@───X^0.5───@───────────────────I───@^t───
""",
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ---X---Y---Z---Z^x---Rx(x)---@---@---X---@-------X^0.5---H^0.5---I---I---@-----
                                |   |   |   |       |                   |   |
b: -----------------------------@---X---@---X^0.5---@-------------------I---@^t---
""",
        use_unicode_characters=False,
    )


def test_cnot_unitary():
    np.testing.assert_almost_equal(
        qubitron.unitary(qubitron.CNOT**0.5),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
                [0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
            ]
        ),
    )


def test_cnot_decompose():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    assert qubitron.decompose_once(qubitron.CNOT(a, b) ** sympy.Symbol('x')) is not None


def test_repr():
    assert repr(qubitron.X) == 'qubitron.X'
    assert repr(qubitron.X**0.5) == '(qubitron.X**0.5)'

    assert repr(qubitron.Z) == 'qubitron.Z'
    assert repr(qubitron.Z**0.5) == 'qubitron.S'
    assert repr(qubitron.Z**0.25) == 'qubitron.T'
    assert repr(qubitron.Z**0.125) == '(qubitron.Z**0.125)'

    assert repr(qubitron.S) == 'qubitron.S'
    assert repr(qubitron.S**-1) == '(qubitron.S**-1)'
    assert repr(qubitron.T) == 'qubitron.T'
    assert repr(qubitron.T**-1) == '(qubitron.T**-1)'

    assert repr(qubitron.Y) == 'qubitron.Y'
    assert repr(qubitron.Y**0.5) == '(qubitron.Y**0.5)'

    assert repr(qubitron.CNOT) == 'qubitron.CNOT'
    assert repr(qubitron.CNOT**0.5) == '(qubitron.CNOT**0.5)'

    qubitron.testing.assert_equivalent_repr(
        qubitron.X ** (sympy.Symbol('a') / 2 - sympy.Symbol('c') * 3 + 5)
    )
    qubitron.testing.assert_equivalent_repr(qubitron.Rx(rads=sympy.Symbol('theta')))
    qubitron.testing.assert_equivalent_repr(qubitron.Ry(rads=sympy.Symbol('theta')))
    qubitron.testing.assert_equivalent_repr(qubitron.Rz(rads=sympy.Symbol('theta')))

    # There should be no floating point error during initialization, and repr
    # should be using the "shortest decimal value closer to X than any other
    # floating point value" strategy, as opposed to the "exactly value in
    # decimal" strategy.
    assert repr(qubitron.CZ**0.2) == '(qubitron.CZ**0.2)'


def test_str():
    assert str(qubitron.X) == 'X'
    assert str(qubitron.X**0.5) == 'X**0.5'
    assert str(qubitron.rx(np.pi)) == 'Rx(π)'
    assert str(qubitron.rx(0.5 * np.pi)) == 'Rx(0.5π)'
    assert str(qubitron.XPowGate(global_shift=-0.25)) == 'XPowGate(exponent=1.0, global_shift=-0.25)'

    assert str(qubitron.Z) == 'Z'
    assert str(qubitron.Z**0.5) == 'S'
    assert str(qubitron.Z**0.125) == 'Z**0.125'
    assert str(qubitron.rz(np.pi)) == 'Rz(π)'
    assert str(qubitron.rz(1.4 * np.pi)) == 'Rz(1.4π)'
    assert str(qubitron.ZPowGate(global_shift=0.25)) == 'ZPowGate(exponent=1.0, global_shift=0.25)'

    assert str(qubitron.S) == 'S'
    assert str(qubitron.S**-1) == 'S**-1'
    assert str(qubitron.T) == 'T'
    assert str(qubitron.T**-1) == 'T**-1'

    assert str(qubitron.Y) == 'Y'
    assert str(qubitron.Y**0.5) == 'Y**0.5'
    assert str(qubitron.ry(np.pi)) == 'Ry(π)'
    assert str(qubitron.ry(3.14 * np.pi)) == 'Ry(3.14π)'
    assert (
        str(qubitron.YPowGate(exponent=2, global_shift=-0.25))
        == 'YPowGate(exponent=2, global_shift=-0.25)'
    )

    assert str(qubitron.CX) == 'CNOT'
    assert str(qubitron.CNOT**0.5) == 'CNOT**0.5'
    assert str(qubitron.CZ) == 'CZ'
    assert str(qubitron.CZ**0.5) == 'CZ**0.5'
    assert str(qubitron.cphase(np.pi)) == 'CZ'
    assert str(qubitron.cphase(np.pi / 2)) == 'CZ**0.5'


def test_rx_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.rx(np.pi / 2)), np.array([[s, -s * 1j], [-s * 1j, s]])
    )

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.rx(-np.pi / 2)), np.array([[s, s * 1j], [s * 1j, s]])
    )

    np.testing.assert_allclose(qubitron.unitary(qubitron.rx(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rx(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rx(np.pi)), np.array([[0, -1j], [-1j, 0]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rx(-np.pi)), np.array([[0, 1j], [1j, 0]]))


def test_ry_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(np.pi / 2)), np.array([[s, -s], [s, s]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(-np.pi / 2)), np.array([[s, s], [-s, s]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(np.pi)), np.array([[0, -1], [1, 0]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.ry(-np.pi)), np.array([[0, 1], [-1, 0]]))


def test_rz_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.rz(np.pi / 2)), np.array([[s - s * 1j, 0], [0, s + s * 1j]])
    )

    np.testing.assert_allclose(
        qubitron.unitary(qubitron.rz(-np.pi / 2)), np.array([[s + s * 1j, 0], [0, s - s * 1j]])
    )

    np.testing.assert_allclose(qubitron.unitary(qubitron.rz(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rz(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rz(np.pi)), np.array([[-1j, 0], [0, 1j]]))

    np.testing.assert_allclose(qubitron.unitary(qubitron.rz(-np.pi)), np.array([[1j, 0], [0, -1j]]))


@pytest.mark.parametrize(
    'angle_rads, expected_unitary',
    [(0, np.eye(4)), (1, np.diag([1, 1, 1, np.exp(1j)])), (np.pi / 2, np.diag([1, 1, 1, 1j]))],
)
def test_cphase_unitary(angle_rads, expected_unitary):
    np.testing.assert_allclose(qubitron.unitary(qubitron.cphase(angle_rads)), expected_unitary)


def test_parameterized_cphase():
    assert qubitron.cphase(sympy.pi) == qubitron.CZ
    assert qubitron.cphase(sympy.pi / 2) == qubitron.CZ**0.5


@pytest.mark.parametrize('gate', [qubitron.X, qubitron.Y, qubitron.Z])
def test_x_y_z_stabilizer(gate):
    assert qubitron.has_stabilizer_effect(gate)
    assert qubitron.has_stabilizer_effect(gate**0.5)
    assert qubitron.has_stabilizer_effect(gate**0)
    assert qubitron.has_stabilizer_effect(gate**-0.5)
    assert qubitron.has_stabilizer_effect(gate**4)
    assert not qubitron.has_stabilizer_effect(gate**1.2)
    foo = sympy.Symbol('foo')
    assert not qubitron.has_stabilizer_effect(gate**foo)


def test_h_stabilizer():
    gate = qubitron.H
    assert qubitron.has_stabilizer_effect(gate)
    assert not qubitron.has_stabilizer_effect(gate**0.5)
    assert qubitron.has_stabilizer_effect(gate**0)
    assert not qubitron.has_stabilizer_effect(gate**-0.5)
    assert qubitron.has_stabilizer_effect(gate**4)
    assert not qubitron.has_stabilizer_effect(gate**1.2)
    foo = sympy.Symbol('foo')
    assert not qubitron.has_stabilizer_effect(gate**foo)


@pytest.mark.parametrize('gate', [qubitron.CX, qubitron.CZ])
def test_cx_cz_stabilizer(gate):
    assert qubitron.has_stabilizer_effect(gate)
    assert not qubitron.has_stabilizer_effect(gate**0.5)
    assert qubitron.has_stabilizer_effect(gate**0)
    assert not qubitron.has_stabilizer_effect(gate**-0.5)
    assert qubitron.has_stabilizer_effect(gate**4)
    assert not qubitron.has_stabilizer_effect(gate**1.2)
    foo = sympy.Symbol('foo')
    assert not qubitron.has_stabilizer_effect(gate**foo)


def test_phase_by_xy():
    assert qubitron.phase_by(qubitron.X, 0.25, 0) == qubitron.Y
    assert qubitron.phase_by(qubitron.X**0.5, 0.25, 0) == qubitron.Y**0.5
    assert qubitron.phase_by(qubitron.X**-0.5, 0.25, 0) == qubitron.Y**-0.5


def test_ixyz_circuit_diagram():
    q = qubitron.NamedQubit('q')
    ix = qubitron.XPowGate(exponent=1, global_shift=0.5)
    iy = qubitron.YPowGate(exponent=1, global_shift=0.5)
    iz = qubitron.ZPowGate(exponent=1, global_shift=0.5)

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            ix(q),
            ix(q) ** -1,
            ix(q) ** -0.99999,
            ix(q) ** -1.00001,
            ix(q) ** 3,
            ix(q) ** 4.5,
            ix(q) ** 4.500001,
        ),
        """
q: ───X───X───X───X───X───X^0.5───X^0.5───
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(iy(q), iy(q) ** -1, iy(q) ** 3, iy(q) ** 4.5, iy(q) ** 4.500001),
        """
q: ───Y───Y───Y───Y^0.5───Y^0.5───
    """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(iz(q), iz(q) ** -1, iz(q) ** 3, iz(q) ** 4.5, iz(q) ** 4.500001),
        """
q: ───Z───Z───Z───S───S───
    """,
    )


@pytest.mark.parametrize(
    'theta,exp',
    [
        (sympy.Symbol("theta"), 1 / 2),
        (np.pi / 2, 1 / 2),
        (np.pi / 2, sympy.Symbol("exp")),
        (sympy.Symbol("theta"), sympy.Symbol("exp")),
    ],
)
def test_rxyz_exponent(theta, exp):
    def resolve(gate):
        return qubitron.resolve_parameters(gate, {'theta': np.pi / 4}, {'exp': 1 / 4})

    assert resolve(qubitron.Rx(rads=theta) ** exp) == resolve(qubitron.Rx(rads=theta * exp))
    assert resolve(qubitron.Ry(rads=theta) ** exp) == resolve(qubitron.Ry(rads=theta * exp))
    assert resolve(qubitron.Rz(rads=theta) ** exp) == resolve(qubitron.Rz(rads=theta * exp))


def test_rxyz_circuit_diagram():
    q = qubitron.NamedQubit('q')

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.rx(np.pi).on(q),
            qubitron.rx(-np.pi).on(q),
            qubitron.rx(-np.pi + 0.00001).on(q),
            qubitron.rx(-np.pi - 0.00001).on(q),
            qubitron.rx(3 * np.pi).on(q),
            qubitron.rx(7 * np.pi / 2).on(q),
            qubitron.rx(9 * np.pi / 2 + 0.00001).on(q),
        ),
        """
q: ───Rx(π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-0.5π)───Rx(0.5π)───
    """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.rx(np.pi).on(q),
            qubitron.rx(np.pi / 2).on(q),
            qubitron.rx(-np.pi + 0.00001).on(q),
            qubitron.rx(-np.pi - 0.00001).on(q),
        ),
        """
q: ---Rx(pi)---Rx(0.5pi)---Rx(-pi)---Rx(-pi)---
        """,
        use_unicode_characters=False,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.ry(np.pi).on(q),
            qubitron.ry(-np.pi).on(q),
            qubitron.ry(3 * np.pi).on(q),
            qubitron.ry(9 * np.pi / 2).on(q),
        ),
        """
q: ───Ry(π)───Ry(-π)───Ry(-π)───Ry(0.5π)───
    """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.rz(np.pi).on(q),
            qubitron.rz(-np.pi).on(q),
            qubitron.rz(3 * np.pi).on(q),
            qubitron.rz(9 * np.pi / 2).on(q),
            qubitron.rz(9 * np.pi / 2 + 0.00001).on(q),
        ),
        """
q: ───Rz(π)───Rz(-π)───Rz(-π)───Rz(0.5π)───Rz(0.5π)───
    """,
    )


def test_trace_distance():
    foo = sympy.Symbol('foo')
    sx = qubitron.X**foo
    sy = qubitron.Y**foo
    sz = qubitron.Z**foo
    sh = qubitron.H**foo
    scx = qubitron.CX**foo
    scz = qubitron.CZ**foo
    # These values should have 1.0 or 0.0 directly returned
    assert qubitron.trace_distance_bound(sx) == 1.0
    assert qubitron.trace_distance_bound(sy) == 1.0
    assert qubitron.trace_distance_bound(sz) == 1.0
    assert qubitron.trace_distance_bound(scx) == 1.0
    assert qubitron.trace_distance_bound(scz) == 1.0
    assert qubitron.trace_distance_bound(sh) == 1.0
    assert qubitron.trace_distance_bound(qubitron.I) == 0.0
    # These values are calculated, so we use approx_eq
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.X), 1.0)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.Y**-1), 1.0)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.Z**0.5), np.sin(np.pi / 4))
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.H**0.25), np.sin(np.pi / 8))
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.CX**2), 0.0)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.CZ ** (1 / 9)), np.sin(np.pi / 18))


def test_commutes():
    assert qubitron.commutes(qubitron.ZPowGate(exponent=sympy.Symbol('t')), qubitron.Z)
    assert qubitron.commutes(qubitron.Z, qubitron.Z(qubitron.LineQubit(0)), default=None) is None
    assert qubitron.commutes(qubitron.Z**0.1, qubitron.XPowGate(exponent=0))


def test_approx_eq():
    assert qubitron.approx_eq(qubitron.Z**0.1, qubitron.Z**0.2, atol=0.3)
    assert not qubitron.approx_eq(qubitron.Z**0.1, qubitron.Z**0.2, atol=0.05)
    assert qubitron.approx_eq(qubitron.Y**0.1, qubitron.Y**0.2, atol=0.3)
    assert not qubitron.approx_eq(qubitron.Y**0.1, qubitron.Y**0.2, atol=0.05)
    assert qubitron.approx_eq(qubitron.X**0.1, qubitron.X**0.2, atol=0.3)
    assert not qubitron.approx_eq(qubitron.X**0.1, qubitron.X**0.2, atol=0.05)


def test_xpow_dim_3():
    x = qubitron.XPowGate(dimension=3)
    assert qubitron.X != x
    # fmt: off
    expected = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(qubitron.unitary(x), expected)

    sim = qubitron.Simulator()
    circuit = qubitron.Circuit([x(qubitron.LineQid(0, 3)) ** 0.5] * 6)
    svs = [step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit)]
    # fmt: off
    expected = [
        [0.67, 0.67, 0.33],
        [0.0, 1.0, 0.0],
        [0.33, 0.67, 0.67],
        [0.0, 0.0, 1.0],
        [0.67, 0.33, 0.67],
        [1.0, 0.0, 0.0],
    ]
    # fmt: on
    assert np.allclose(np.abs(svs), expected, atol=1e-2)


def test_xpow_dim_4():
    x = qubitron.XPowGate(dimension=4)
    assert qubitron.X != x
    # fmt: off
    expected = [
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(qubitron.unitary(x), expected)

    sim = qubitron.Simulator()
    circuit = qubitron.Circuit([x(qubitron.LineQid(0, 4)) ** 0.5] * 8)
    svs = [step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit)]
    # fmt: off
    expected = [
        [0.65, 0.65, 0.27, 0.27],
        [0.0, 1.0, 0.0, 0.0],
        [0.27, 0.65, 0.65, 0.27],
        [0.0, 0.0, 1.0, 0.0],
        [0.27, 0.27, 0.65, 0.65],
        [0.0, 0.0, 0.0, 1.0],
        [0.65, 0.27, 0.27, 0.65],
        [1.0, 0.0, 0.0, 0.0],
    ]
    # fmt: on
    assert np.allclose(np.abs(svs), expected, atol=1e-2)


def test_zpow_dim_3():
    L = np.exp(2 * np.pi * 1j / 3)
    L2 = L**2
    z = qubitron.ZPowGate(dimension=3)
    assert qubitron.Z != z
    # fmt: off
    expected = [
        [1, 0, 0],
        [0, L, 0],
        [0, 0, L2],
    ]
    # fmt: on
    assert np.allclose(qubitron.unitary(z), expected)

    sim = qubitron.Simulator()
    circuit = qubitron.Circuit([z(qubitron.LineQid(0, 3)) ** 0.5] * 6)
    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=0)
    ]
    expected = [[1, 0, 0]] * 6
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=1)
    ]
    # fmt: off
    expected = [
        [0, L**0.5, 0],
        [0, L**1.0, 0],
        [0, L**1.5, 0],
        [0, L**2.0, 0],
        [0, L**2.5, 0],
        [0, 1, 0],
    ]
    # fmt: on
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=2)
    ]
    # fmt: off
    expected = [
        [0, 0, L],
        [0, 0, L2],
        [0, 0, 1],
        [0, 0, L],
        [0, 0, L2],
        [0, 0, 1],
    ]
    # fmt: on
    assert np.allclose((svs), expected)


def test_zpow_dim_4():
    z = qubitron.ZPowGate(dimension=4)
    assert qubitron.Z != z
    # fmt: off
    expected = [
        [1, 0, 0, 0],
        [0, 1j, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1j],
    ]
    # fmt: on
    assert np.allclose(qubitron.unitary(z), expected)

    sim = qubitron.Simulator()
    circuit = qubitron.Circuit([z(qubitron.LineQid(0, 4)) ** 0.5] * 8)
    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=0)
    ]
    expected = [[1, 0, 0, 0]] * 8
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=1)
    ]
    # fmt: off
    expected = [
        [0, 1j**0.5, 0, 0],
        [0, 1j**1.0, 0, 0],
        [0, 1j**1.5, 0, 0],
        [0, 1j**2.0, 0, 0],
        [0, 1j**2.5, 0, 0],
        [0, 1j**3.0, 0, 0],
        [0, 1j**3.5, 0, 0],
        [0, 1, 0, 0],
    ]
    # fmt: on
    assert np.allclose(svs, expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=2)
    ]
    # fmt: off
    expected = [
        [0, 0, 1j, 0],
        [0, 0, -1, 0],
        [0, 0, -1j, 0],
        [0, 0, 1, 0],
        [0, 0, 1j, 0],
        [0, 0, -1, 0],
        [0, 0, -1j, 0],
        [0, 0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(svs, expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=3)
    ]
    # fmt: off
    expected = [
        [0, 0, 0, 1j**1.5],
        [0, 0, 0, 1j**3],
        [0, 0, 0, 1j**0.5],
        [0, 0, 0, 1j**2],
        [0, 0, 0, 1j**3.5],
        [0, 0, 0, 1j**1],
        [0, 0, 0, 1j**2.5],
        [0, 0, 0, 1],
    ]
    # fmt: on
    assert np.allclose(svs, expected)


def test_wrong_dims():
    x3 = qubitron.XPowGate(dimension=3)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = x3.on(qubitron.LineQubit(0))
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = x3.on(qubitron.LineQid(0, dimension=4))

    z3 = qubitron.ZPowGate(dimension=3)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = z3.on(qubitron.LineQubit(0))
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = z3.on(qubitron.LineQid(0, dimension=4))

    with pytest.raises(ValueError, match='Wrong shape'):
        _ = qubitron.X.on(qubitron.LineQid(0, dimension=3))

    with pytest.raises(ValueError, match='Wrong shape'):
        _ = qubitron.Z.on(qubitron.LineQid(0, dimension=3))


@pytest.mark.parametrize('gate_type', [qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate])
@pytest.mark.parametrize('exponent', [sympy.Symbol('s'), sympy.Symbol('s') * 2])
def test_parameterized_pauli_expansion(gate_type, exponent):
    gate = gate_type(exponent=exponent)
    pauli = qubitron.pauli_expansion(gate)
    gate_resolved = qubitron.resolve_parameters(gate, {'s': 0.5})
    pauli_resolved = qubitron.resolve_parameters(pauli, {'s': 0.5})
    assert qubitron.approx_eq(pauli_resolved, qubitron.pauli_expansion(gate_resolved))
