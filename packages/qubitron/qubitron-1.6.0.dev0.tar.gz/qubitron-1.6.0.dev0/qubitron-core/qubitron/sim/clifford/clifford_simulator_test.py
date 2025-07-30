# Copyright 2025 The Qubitron Developers
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

import itertools

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


def test_simulate_no_circuit():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit()
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state.to_numpy(), np.array([1, 0, 0, 0]))
    assert len(result.measurements) == 0


def test_run_no_repetitions():
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=0)
    assert sum(result.measurements['q(0)']) == 0


def test_run_hadamard():
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert sum(result.measurements['q(0)'])[0] < 80
    assert sum(result.measurements['q(0)'])[0] > 20


def test_run_GHZ():
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert sum(result.measurements['q(0)'])[0] < 80
    assert sum(result.measurements['q(0)'])[0] > 20


def test_run_correlations():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1), qubitron.measure(q0, q1))
    for _ in range(10):
        result = simulator.run(circuit)
        bits = result.measurements['q(0),q(1)'][0]
        assert bits[0] == bits[1]


def test_run_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.run_sweep(circuit, qubitron.ParamResolver({}))


def test_simulate_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.simulate_sweep(circuit, qubitron.ParamResolver({}))


def test_simulate():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1))
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state.to_numpy(), np.array([0.5, 0.5, 0.5, 0.5]))
    assert len(result.measurements) == 0


def test_simulate_initial_state():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit()
            if b0:
                circuit.append(qubitron.X(q0))
            if b1:
                circuit.append(qubitron.X(q1))
            circuit.append(qubitron.measure(q0, q1))

            for initial_state in [
                qubitron.StabilizerChFormSimulationState(
                    qubits=qubitron.LineQubit.range(2), initial_state=1
                )
            ]:
                result = simulator.simulate(circuit, initial_state=initial_state)
                expected_state = np.zeros(shape=(2, 2))
                expected_state[b0][1 - b1] = 1.0
                np.testing.assert_almost_equal(
                    result.final_state.to_numpy(), np.reshape(expected_state, 4)
                )


def test_simulation_state():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit()
            if b0:
                circuit.append(qubitron.X(q0))
            if b1:
                circuit.append(qubitron.X(q1))
            circuit.append(qubitron.measure(q0, q1))

            args = simulator._create_simulation_state(initial_state=1, qubits=(q0, q1))
            result = simulator.simulate(circuit, initial_state=args)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][1 - b1] = 1.0
            np.testing.assert_almost_equal(
                result.final_state.to_numpy(), np.reshape(expected_state, 4)
            )


def test_simulate_qubit_order():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit()
            if b0:
                circuit.append(qubitron.X(q0))
            if b1:
                circuit.append(qubitron.X(q1))
            circuit.append(qubitron.measure(q0, q1))

            result = simulator.simulate(circuit, qubit_order=[q1, q0])
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b1][b0] = 1.0
            np.testing.assert_almost_equal(
                result.final_state.to_numpy(), np.reshape(expected_state, 4)
            )


def test_run_measure_multiple_qubits():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.CliffordSimulator()
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit()
            if b0:
                circuit.append(qubitron.X(q0))
            if b1:
                circuit.append(qubitron.X(q1))
            circuit.append(qubitron.measure(q0, q1))
            result = simulator.run(circuit, repetitions=3)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [[b0, b1]] * 3})


def test_simulate_moment_steps():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.H(q0), qubitron.H(q1))
    simulator = qubitron.CliffordSimulator()
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            np.testing.assert_almost_equal(step.state.to_numpy(), np.array([0.5] * 4))
        else:
            np.testing.assert_almost_equal(step.state.to_numpy(), np.array([1, 0, 0, 0]))


def test_simulate_moment_steps_sample():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1))
    simulator = qubitron.CliffordSimulator()
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, False]) or np.array_equal(
                    sample, [False, False]
                )
        else:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, True]) or np.array_equal(
                    sample, [False, False]
                )


@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_intermediate_measurement(split):
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0), qubitron.H(q0))
    simulator = qubitron.CliffordSimulator(split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 1:
            result = int(step.measurements['q(0)'][0])
            expected = np.zeros(2)
            expected[result] = 1
            np.testing.assert_almost_equal(step.state.to_numpy(), expected)
        if i == 2:
            expected = np.array([np.sqrt(0.5), np.sqrt(0.5) * (-1) ** result])
            np.testing.assert_almost_equal(step.state.to_numpy(), expected)


def test_clifford_state_initial_state():
    q0 = qubitron.LineQubit(0)
    with pytest.raises(ValueError, match='Out of range'):
        _ = qubitron.CliffordState(qubit_map={q0: 0}, initial_state=2)
    state = qubitron.CliffordState(qubit_map={q0: 0}, initial_state=1)
    np.testing.assert_allclose(state.state_vector(), [0, 1])

    assert state.copy() == state


def test_clifford_trial_result_repr():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = qubitron.StabilizerChFormSimulationState(qubits=[q0])
    assert (
        repr(
            qubitron.CliffordTrialResult(
                params=qubitron.ParamResolver({}),
                measurements={'m': np.array([[1]])},
                final_simulator_state=final_simulator_state,
            )
        )
        == "qubitron.SimulationTrialResult(params=qubitron.ParamResolver({}), "
        "measurements={'m': array([[1]])}, "
        "final_simulator_state=qubitron.StabilizerChFormSimulationState("
        "initial_state=StabilizerStateChForm(num_qubits=1), "
        "qubits=(qubitron.LineQubit(0),), "
        "classical_data=qubitron.ClassicalDataDictionaryStore()))"
    )


def test_clifford_trial_result_str():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = qubitron.StabilizerChFormSimulationState(qubits=[q0])
    assert (
        str(
            qubitron.CliffordTrialResult(
                params=qubitron.ParamResolver({}),
                measurements={'m': np.array([[1]])},
                final_simulator_state=final_simulator_state,
            )
        )
        == "measurements: m=1\n"
        "output state: |0⟩"
    )


def test_clifford_trial_result_repr_pretty():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = qubitron.StabilizerChFormSimulationState(qubits=[q0])
    result = qubitron.CliffordTrialResult(
        params=qubitron.ParamResolver({}),
        measurements={'m': np.array([[1]])},
        final_simulator_state=final_simulator_state,
    )

    qubitron.testing.assert_repr_pretty(result, "measurements: m=1\n" "output state: |0⟩")
    qubitron.testing.assert_repr_pretty(result, "qubitron.CliffordTrialResult(...)", cycle=True)


def test_clifford_step_result_str():
    q0 = qubitron.LineQubit(0)
    result = next(
        qubitron.CliffordSimulator().simulate_moment_steps(qubitron.Circuit(qubitron.measure(q0, key='m')))
    )
    assert str(result) == "m=0\n" "|0⟩"


def test_clifford_step_result_repr_pretty():
    q0 = qubitron.LineQubit(0)
    result = next(
        qubitron.CliffordSimulator().simulate_moment_steps(qubitron.Circuit(qubitron.measure(q0, key='m')))
    )
    qubitron.testing.assert_repr_pretty(result, "m=0\n" "|0⟩")
    qubitron.testing.assert_repr_pretty(result, "qubitron.CliffordSimulatorStateResult(...)", cycle=True)


def test_clifford_step_result_no_measurements_str():
    q0 = qubitron.LineQubit(0)
    result = next(qubitron.CliffordSimulator().simulate_moment_steps(qubitron.Circuit(qubitron.I(q0))))
    assert str(result) == "|0⟩"


def test_clifford_state_str():
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    state = qubitron.CliffordState(qubit_map={q0: 0, q1: 1})

    assert str(state) == "|00⟩"


def test_clifford_state_state_vector():
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    state = qubitron.CliffordState(qubit_map={q0: 0, q1: 1})

    np.testing.assert_equal(state.state_vector(), [1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j])


def test_stabilizerStateChForm_H():
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    state = qubitron.CliffordState(qubit_map={q0: 0, q1: 1})
    with pytest.raises(ValueError, match="|y> is equal to |z>"):
        state.ch_form._H_decompose(0, 1, 1, 0)


def test_clifford_stabilizerStateChForm_repr():
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    state = qubitron.CliffordState(qubit_map={q0: 0, q1: 1})
    assert repr(state) == 'StabilizerStateChForm(num_qubits=2)'


def test_clifford_circuit_SHSYSHS():
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(
        qubitron.S(q0),
        qubitron.H(q0),
        qubitron.S(q0),
        qubitron.Y(q0),
        qubitron.S(q0),
        qubitron.H(q0),
        qubitron.S(q0),
        qubitron.measure(q0),
    )

    clifford_simulator = qubitron.CliffordSimulator()
    state_vector_simulator = qubitron.Simulator()

    # workaround until #6402 is resolved.
    final_state_vector = state_vector_simulator.simulate(circuit).final_state_vector
    final_state_vector /= np.linalg.norm(final_state_vector)
    np.testing.assert_almost_equal(
        clifford_simulator.simulate(circuit).final_state.state_vector(), final_state_vector
    )


@pytest.mark.parametrize('split', [True, False])
def test_clifford_circuit(split):
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    circuit = qubitron.Circuit()

    for _ in range(100):
        x = np.random.randint(7)

        if x == 0:
            circuit.append(qubitron.X(np.random.choice((q0, q1))))
        elif x == 1:
            circuit.append(qubitron.Z(np.random.choice((q0, q1))))
        elif x == 2:
            circuit.append(qubitron.Y(np.random.choice((q0, q1))))
        elif x == 3:
            circuit.append(qubitron.S(np.random.choice((q0, q1))))
        elif x == 4:
            circuit.append(qubitron.H(np.random.choice((q0, q1))))
        elif x == 5:
            circuit.append(qubitron.CNOT(q0, q1))
        elif x == 6:
            circuit.append(qubitron.CZ(q0, q1))

    clifford_simulator = qubitron.CliffordSimulator(split_untangled_states=split)
    state_vector_simulator = qubitron.Simulator()

    np.testing.assert_almost_equal(
        clifford_simulator.simulate(circuit).final_state.state_vector(),
        state_vector_simulator.simulate(circuit).final_state_vector,
    )


@pytest.mark.parametrize("qubits", [qubitron.LineQubit.range(2), qubitron.LineQubit.range(4)])
@pytest.mark.parametrize('split', [True, False])
def test_clifford_circuit_2(qubits, split):
    circuit = qubitron.Circuit()

    np.random.seed(2)

    for _ in range(50):
        x = np.random.randint(7)

        if x == 0:
            circuit.append(qubitron.X(np.random.choice(qubits)))  # pragma: no cover
        elif x == 1:
            circuit.append(qubitron.Z(np.random.choice(qubits)))  # pragma: no cover
        elif x == 2:
            circuit.append(qubitron.Y(np.random.choice(qubits)))  # pragma: no cover
        elif x == 3:
            circuit.append(qubitron.S(np.random.choice(qubits)))  # pragma: no cover
        elif x == 4:
            circuit.append(qubitron.H(np.random.choice(qubits)))  # pragma: no cover
        elif x == 5:
            circuit.append(qubitron.CNOT(qubits[0], qubits[1]))  # pragma: no cover
        elif x == 6:
            circuit.append(qubitron.CZ(qubits[0], qubits[1]))  # pragma: no cover

    circuit.append(qubitron.measure(qubits[0]))
    result = qubitron.CliffordSimulator(split_untangled_states=split).run(circuit, repetitions=100)

    assert sum(result.measurements['q(0)'])[0] < 80
    assert sum(result.measurements['q(0)'])[0] > 20


@pytest.mark.parametrize('split', [True, False])
def test_clifford_circuit_3(split):
    # This test tests the simulator on arbitrary 1-qubit Clifford gates.
    (q0, q1) = (qubitron.LineQubit(0), qubitron.LineQubit(1))
    circuit = qubitron.Circuit()

    def random_clifford_gate():
        matrix = np.eye(2)
        for _ in range(10):
            matrix = matrix @ qubitron.unitary(np.random.choice((qubitron.H, qubitron.S)))
        matrix *= np.exp(1j * np.random.uniform(0, 2 * np.pi))
        return qubitron.MatrixGate(matrix)

    for _ in range(20):
        if np.random.randint(5) == 0:
            circuit.append(qubitron.CNOT(q0, q1))
        else:
            circuit.append(random_clifford_gate()(np.random.choice((q0, q1))))

    clifford_simulator = qubitron.CliffordSimulator(split_untangled_states=split)
    state_vector_simulator = qubitron.Simulator()

    np.testing.assert_almost_equal(
        clifford_simulator.simulate(circuit).final_state.state_vector(),
        state_vector_simulator.simulate(circuit).final_state_vector,
        decimal=6,
    )


def test_non_clifford_circuit():
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit()
    circuit.append(qubitron.T(q0))
    with pytest.raises(TypeError, match="support qubitron.T"):
        qubitron.CliffordSimulator().simulate(circuit)


def test_swap():
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(a),
        qubitron.SWAP(a, b),
        qubitron.SWAP(a, b) ** 4,
        qubitron.measure(a, key="a"),
        qubitron.measure(b, key="b"),
    )
    r = qubitron.CliffordSimulator().sample(circuit)
    assert not r["a"][0]
    assert r["b"][0]

    with pytest.raises(TypeError, match="CliffordSimulator doesn't support"):
        qubitron.CliffordSimulator().simulate((qubitron.Circuit(qubitron.SWAP(a, b) ** 3.5)))


def test_sample_seed():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
    simulator = qubitron.CliffordSimulator(seed=1234)
    result = simulator.run(circuit, repetitions=20)
    measured = result.measurements['q']
    result_string = ''.join(map(lambda x: str(int(x[0])), measured))
    assert result_string == '11010001111100100000'


def test_is_supported_operation():
    class MultiQubitOp(qubitron.Operation):
        """Multi-qubit operation with unitary.

        Used to verify that `is_supported_operation` does not attempt to
        allocate the unitary for multi-qubit operations.
        """

        @property
        def qubits(self):
            return qubitron.LineQubit.range(100)

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        def _has_unitary_(self):
            return True  # pragma: no cover

        def _unitary_(self):
            assert False  # pragma: no cover

    q1, q2 = qubitron.LineQubit.range(2)
    assert qubitron.CliffordSimulator.is_supported_operation(qubitron.X(q1))
    assert qubitron.CliffordSimulator.is_supported_operation(qubitron.H(q1))
    assert qubitron.CliffordSimulator.is_supported_operation(qubitron.CNOT(q1, q2))
    assert qubitron.CliffordSimulator.is_supported_operation(qubitron.measure(q1))
    assert qubitron.CliffordSimulator.is_supported_operation(qubitron.global_phase_operation(1j))

    assert not qubitron.CliffordSimulator.is_supported_operation(qubitron.T(q1))
    assert not qubitron.CliffordSimulator.is_supported_operation(MultiQubitOp())


def test_simulate_pauli_string():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit([qubitron.PauliString({q: 'X'}), qubitron.PauliString({q: 'Z'})])
    simulator = qubitron.CliffordSimulator()

    result = simulator.simulate(circuit).final_state.state_vector()

    assert np.allclose(result, [0, -1])


def test_simulate_global_phase_operation():
    q1, q2 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit([qubitron.I(q1), qubitron.I(q2), qubitron.global_phase_operation(-1j)])
    simulator = qubitron.CliffordSimulator()

    result = simulator.simulate(circuit).final_state.state_vector()

    assert np.allclose(result, [-1j, 0, 0, 0])


def test_json_roundtrip():
    (q0, q1, q2) = (qubitron.LineQubit(0), qubitron.LineQubit(1), qubitron.LineQubit(2))
    state = qubitron.CliffordState(qubit_map={q0: 0, q1: 1, q2: 2})

    # Apply some transformations.
    state.apply_unitary(qubitron.X(q0))
    state.apply_unitary(qubitron.H(q1))

    with pytest.raises(ValueError, match='T cannot be run with Clifford simulator.'):
        state.apply_unitary(qubitron.T(q1))

    # Roundtrip serialize, then deserialize.
    state_roundtrip = qubitron.CliffordState._from_json_dict_(**state._json_dict_())

    # Apply the same transformation on both the original object and the one that
    # went through the roundtrip.
    state.apply_unitary(qubitron.S(q1))
    state_roundtrip.apply_unitary(qubitron.S(q1))

    # And the CH form isn't changed either.
    assert np.allclose(state.ch_form.state_vector(), state_roundtrip.ch_form.state_vector())


def test_invalid_apply_measurement():
    q0 = qubitron.LineQubit(0)
    state = qubitron.CliffordState(qubit_map={q0: 0})
    measurements = {}
    with pytest.raises(TypeError, match='only supports qubitron.MeasurementGate'):
        state.apply_measurement(qubitron.H(q0), measurements, np.random.RandomState())
    assert measurements == {}


def test_valid_apply_measurement():
    q0 = qubitron.LineQubit(0)
    state = qubitron.CliffordState(qubit_map={q0: 0}, initial_state=1)
    measurements = {}
    _ = state.apply_measurement(
        qubitron.measure(q0), measurements, np.random.RandomState(), collapse_state_vector=False
    )
    assert measurements == {'q(0)': [1]}
    state.apply_measurement(qubitron.measure(q0), measurements, np.random.RandomState())
    assert measurements == {'q(0)': [1]}


@pytest.mark.parametrize('split', [True, False])
def test_reset(split):
    q = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.X(q), qubitron.reset(q), qubitron.measure(q, key="out"))
    sim = qubitron.CliffordSimulator(split_untangled_states=split)
    assert sim.sample(c)["out"][0] == 0
    c = qubitron.Circuit(qubitron.H(q), qubitron.reset(q), qubitron.measure(q, key="out"))
    assert sim.sample(c)["out"][0] == 0
    c = qubitron.Circuit(qubitron.reset(q), qubitron.measure(q, key="out"))
    assert sim.sample(c)["out"][0] == 0


def test_state_copy():
    sim = qubitron.CliffordSimulator()

    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.H(q))

    state_ch_forms = []
    for step in sim.simulate_moment_steps(circuit):
        state_ch_forms.append(step.state.ch_form)
    for x, y in itertools.combinations(state_ch_forms, 2):
        assert not np.shares_memory(x.v, y.v)
