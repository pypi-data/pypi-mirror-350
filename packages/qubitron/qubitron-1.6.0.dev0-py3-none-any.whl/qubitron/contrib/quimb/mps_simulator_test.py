# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.contrib.quimb as ccq
import qubitron.testing
from qubitron import value


def assert_same_output_as_dense(circuit, qubit_order, initial_state=0, grouping=None):
    mps_simulator = ccq.mps_simulator.MPSSimulator(grouping=grouping)
    ref_simulator = qubitron.Simulator()

    actual = mps_simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
    expected = ref_simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
    np.testing.assert_allclose(
        actual.final_state.to_numpy(), expected.final_state_vector, atol=1e-4
    )
    assert len(actual.measurements) == 0


def test_various_gates_1d():
    gate_op_cls = [qubitron.I, qubitron.H, qubitron.X, qubitron.Y, qubitron.Z, qubitron.T]
    cross_gate_op_cls = [qubitron.CNOT, qubitron.SWAP]

    q0, q1 = qubitron.LineQubit.range(2)

    for q0_gate_op in gate_op_cls:
        for q1_gate_op in gate_op_cls:
            for cross_gate_op in cross_gate_op_cls:
                circuit = qubitron.Circuit(q0_gate_op(q0), q1_gate_op(q1), cross_gate_op(q0, q1))
                for initial_state in range(2 * 2):
                    assert_same_output_as_dense(
                        circuit=circuit, qubit_order=[q0, q1], initial_state=initial_state
                    )


def test_various_gates_1d_flip():
    q0, q1 = qubitron.LineQubit.range(2)

    circuit = qubitron.Circuit(qubitron.H(q1), qubitron.CNOT(q1, q0))

    assert_same_output_as_dense(circuit=circuit, qubit_order=[q0, q1])
    assert_same_output_as_dense(circuit=circuit, qubit_order=[q1, q0])


def test_various_gates_2d():
    gate_op_cls = [qubitron.I, qubitron.H]
    cross_gate_op_cls = [qubitron.CNOT, qubitron.SWAP]

    q0, q1, q2, q3, q4, q5 = qubitron.GridQubit.rect(3, 2)

    for q0_gate_op in gate_op_cls:
        for q1_gate_op in gate_op_cls:
            for q2_gate_op in gate_op_cls:
                for q3_gate_op in gate_op_cls:
                    for cross_gate_op1 in cross_gate_op_cls:
                        for cross_gate_op2 in cross_gate_op_cls:
                            circuit = qubitron.Circuit(
                                q0_gate_op(q0),
                                q1_gate_op(q1),
                                cross_gate_op1(q0, q1),
                                q2_gate_op(q2),
                                q3_gate_op(q3),
                                cross_gate_op2(q3, q1),
                            )
                            assert_same_output_as_dense(
                                circuit=circuit, qubit_order=[q0, q1, q2, q3, q4, q5]
                            )


def test_grouping():
    q0, q1, q2 = qubitron.LineQubit.range(3)

    circuit = qubitron.Circuit(
        qubitron.X(q0) ** 0.1,
        qubitron.Y(q1) ** 0.2,
        qubitron.Z(q2) ** 0.3,
        qubitron.CNOT(q0, q1),
        qubitron.Y(q1) ** 0.4,
    )

    groupings = [
        None,
        {q0: 0, q1: 1, q2: 2},
        {q0: 0, q1: 0, q2: 1},
        {q0: 0, q1: 1, q2: 0},
        {q0: 1, q1: 0, q2: 0},
        {q0: 0, q1: 0, q2: 0},
    ]

    for grouping in groupings:
        for initial_state in range(2 * 2 * 2):
            assert_same_output_as_dense(
                circuit=circuit,
                qubit_order=[q0, q1, q2],
                initial_state=initial_state,
                grouping=grouping,
            )


def test_grouping_does_not_overlap():
    q0, q1 = qubitron.LineQubit.range(2)
    mps_simulator = ccq.mps_simulator.MPSSimulator(grouping={q0: 0})

    with pytest.raises(ValueError, match="Grouping must cover exactly the qubits"):
        mps_simulator.simulate(qubitron.Circuit(), qubit_order={q0: 0, q1: 1})


def test_same_partial_trace():
    qubit_order = qubitron.LineQubit.range(2)
    q0, q1 = qubit_order

    mps_simulator = ccq.mps_simulator.MPSSimulator()

    for _ in range(50):
        for initial_state in range(4):
            circuit = qubitron.testing.random_circuit(qubit_order, 3, 0.9)
            expected_density_matrix = qubitron.final_density_matrix(
                circuit, qubit_order=qubit_order, initial_state=initial_state
            )
            expected_partial_trace = qubitron.partial_trace(
                expected_density_matrix.reshape(2, 2, 2, 2), keep_indices=[0]
            )

            final_state = mps_simulator.simulate(
                circuit, qubit_order=qubit_order, initial_state=initial_state
            ).final_state
            actual_density_matrix = final_state.partial_trace([q0, q1])
            actual_partial_trace = final_state.partial_trace([q0])

            np.testing.assert_allclose(actual_density_matrix, expected_density_matrix, atol=1e-4)
            np.testing.assert_allclose(actual_partial_trace, expected_partial_trace, atol=1e-4)


def test_probs_dont_sum_up_to_one():
    q0 = qubitron.NamedQid('q0', dimension=2)
    circuit = qubitron.Circuit(qubitron.measure(q0))

    simulator = ccq.mps_simulator.MPSSimulator(
        simulation_options=ccq.mps_simulator.MPSOptions(sum_prob_atol=-0.5)
    )

    with pytest.raises(ValueError, match="Sum of probabilities exceeds tolerance"):
        simulator.run(circuit, repetitions=1)


def test_empty():
    q0 = qubitron.NamedQid('q0', dimension=2)
    q1 = qubitron.NamedQid('q1', dimension=3)
    q2 = qubitron.NamedQid('q2', dimension=5)
    circuit = qubitron.Circuit()

    for initial_state in range(2 * 3 * 5):
        assert_same_output_as_dense(
            circuit=circuit, qubit_order=[q0, q1, q2], initial_state=initial_state
        )


def test_cnot():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.CNOT(q0, q1))

    for initial_state in range(4):
        assert_same_output_as_dense(
            circuit=circuit, qubit_order=[q0, q1], initial_state=initial_state
        )


def test_cnot_flipped():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.CNOT(q1, q0))

    for initial_state in range(4):
        assert_same_output_as_dense(
            circuit=circuit, qubit_order=[q0, q1], initial_state=initial_state
        )


def test_simulation_state():
    q0, q1 = qubit_order = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.CNOT(q1, q0))
    mps_simulator = ccq.mps_simulator.MPSSimulator()
    ref_simulator = qubitron.Simulator()
    for initial_state in range(4):
        args = mps_simulator._create_simulation_state(initial_state=initial_state, qubits=(q0, q1))
        actual = mps_simulator.simulate(circuit, qubit_order=qubit_order, initial_state=args)
        expected = ref_simulator.simulate(
            circuit, qubit_order=qubit_order, initial_state=initial_state
        )
        np.testing.assert_allclose(
            actual.final_state.to_numpy(), expected.final_state_vector, atol=1e-4
        )
        assert len(actual.measurements) == 0


def test_three_qubits():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.CCX(q0, q1, q2))

    with pytest.raises(ValueError, match="Can only handle 1 and 2 qubit operations"):
        assert_same_output_as_dense(circuit=circuit, qubit_order=[q0, q1, q2])


def test_measurement_1qubit():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.H(q1), qubitron.measure(q1))

    simulator = ccq.mps_simulator.MPSSimulator()

    result = simulator.run(circuit, repetitions=100)
    assert sum(result.measurements['q(1)'])[0] < 80
    assert sum(result.measurements['q(1)'])[0] > 20


def test_reset():
    q = qubitron.LineQubit(0)
    simulator = ccq.mps_simulator.MPSSimulator()
    c = qubitron.Circuit(qubitron.X(q), qubitron.reset(q), qubitron.measure(q))
    assert simulator.sample(c)['q(0)'][0] == 0
    c = qubitron.Circuit(qubitron.H(q), qubitron.reset(q), qubitron.measure(q))
    assert simulator.sample(c)['q(0)'][0] == 0
    c = qubitron.Circuit(qubitron.reset(q), qubitron.measure(q))
    assert simulator.sample(c)['q(0)'][0] == 0


def test_measurement_2qubits():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.H(q2), qubitron.measure(q0, q2))

    simulator = ccq.mps_simulator.MPSSimulator()

    repetitions = 1024
    measurement = simulator.run(circuit, repetitions=repetitions).measurements['q(0),q(2)']

    result_counts = {'00': 0, '01': 0, '10': 0, '11': 0}
    for i in range(repetitions):
        key = str(measurement[i, 0]) + str(measurement[i, 1])
        result_counts[key] += 1

    for result_count in result_counts.values():
        # Expected value is 1/4:
        assert result_count > repetitions * 0.15
        assert result_count < repetitions * 0.35


def test_measurement_str():
    q0 = qubitron.NamedQid('q0', dimension=3)
    circuit = qubitron.Circuit(qubitron.measure(q0))

    simulator = ccq.mps_simulator.MPSSimulator()
    result = simulator.run(circuit, repetitions=7)

    assert str(result) == "q0 (d=3)=0000000"


def test_trial_result_str():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = ccq.mps_simulator.MPSState(
        qubits=(q0,),
        prng=value.parse_random_state(0),
        simulation_options=ccq.mps_simulator.MPSOptions(),
    )
    result = ccq.mps_simulator.MPSTrialResult(
        params=qubitron.ParamResolver({}),
        measurements={'m': np.array([[1]])},
        final_simulator_state=final_simulator_state,
    )
    assert 'output state: TensorNetwork' in str(result)


def test_trial_result_repr_pretty():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = ccq.mps_simulator.MPSState(
        qubits=(q0,),
        prng=value.parse_random_state(0),
        simulation_options=ccq.mps_simulator.MPSOptions(),
    )
    result = ccq.mps_simulator.MPSTrialResult(
        params=qubitron.ParamResolver({}),
        measurements={'m': np.array([[1]])},
        final_simulator_state=final_simulator_state,
    )
    qubitron.testing.assert_repr_pretty_contains(result, 'output state: TensorNetwork')
    qubitron.testing.assert_repr_pretty(result, "qubitron.MPSTrialResult(...)", cycle=True)


def test_empty_step_result():
    q0 = qubitron.LineQubit(0)
    sim = ccq.mps_simulator.MPSSimulator()
    step_result = next(sim.simulate_moment_steps(qubitron.Circuit(qubitron.measure(q0))))
    assert 'TensorNetwork' in str(step_result)


def test_step_result_repr_pretty():
    q0 = qubitron.LineQubit(0)
    sim = ccq.mps_simulator.MPSSimulator()
    step_result = next(sim.simulate_moment_steps(qubitron.Circuit(qubitron.measure(q0))))
    qubitron.testing.assert_repr_pretty_contains(step_result, 'TensorNetwork')
    qubitron.testing.assert_repr_pretty(step_result, "qubitron.MPSSimulatorStepResult(...)", cycle=True)


def test_state_equal():
    q0, q1 = qubitron.LineQubit.range(2)
    state0 = ccq.mps_simulator.MPSState(
        qubits=(q0,),
        prng=value.parse_random_state(0),
        simulation_options=ccq.mps_simulator.MPSOptions(cutoff=1e-3, sum_prob_atol=1e-3),
    )
    state1a = ccq.mps_simulator.MPSState(
        qubits=(q1,),
        prng=value.parse_random_state(0),
        simulation_options=ccq.mps_simulator.MPSOptions(cutoff=1e-3, sum_prob_atol=1e-3),
    )
    state1b = ccq.mps_simulator.MPSState(
        qubits=(q1,),
        prng=value.parse_random_state(0),
        simulation_options=ccq.mps_simulator.MPSOptions(cutoff=1729.0, sum_prob_atol=1e-3),
    )
    assert state0 == state0
    assert state0 != state1a
    assert state1a != state1b


def test_random_circuits_equal_more_rows():
    circuit = qubitron.testing.random_circuit(
        qubits=qubitron.GridQubit.rect(3, 2), n_moments=6, op_density=1.0
    )
    qubits = circuit.all_qubits()
    assert_same_output_as_dense(circuit, qubits)


def test_random_circuits_equal_more_cols():
    circuit = qubitron.testing.random_circuit(
        qubits=qubitron.GridQubit.rect(2, 3), n_moments=6, op_density=1.0
    )
    qubits = circuit.all_qubits()
    assert_same_output_as_dense(circuit, qubits)


def test_tensor_index_names():
    qubits = qubitron.LineQubit.range(12)
    qubit_map = {qubit: i for i, qubit in enumerate(qubits)}
    state = ccq.mps_simulator.MPSState(qubits=qubit_map, prng=value.parse_random_state(0))

    assert state.i_str(0) == "i_00"
    assert state.i_str(11) == "i_11"
    assert state.mu_str(0, 3) == "mu_0_3"
    assert state.mu_str(3, 0) == "mu_0_3"


def test_simulate_moment_steps_sample():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1))

    simulator = ccq.mps_simulator.MPSSimulator()

    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            np.testing.assert_almost_equal(
                step._simulator_state().to_numpy(),
                np.asarray([1.0 / math.sqrt(2), 0.0, 1.0 / math.sqrt(2), 0.0]),
            )
            # There are two "Tensor()" copies in the string.
            assert len(str(step).split('Tensor(')) == 3
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, False]) or np.array_equal(
                    sample, [False, False]
                )
            np.testing.assert_almost_equal(
                step._simulator_state().to_numpy(),
                np.asarray([1.0 / math.sqrt(2), 0.0, 1.0 / math.sqrt(2), 0.0]),
            )
        else:
            np.testing.assert_almost_equal(
                step._simulator_state().to_numpy(),
                np.asarray([1.0 / math.sqrt(2), 0.0, 0.0, 1.0 / math.sqrt(2)]),
            )
            # There are two "Tensor()" copies in the string.
            assert len(str(step).split('Tensor(')) == 3
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, True]) or np.array_equal(
                    sample, [False, False]
                )


def test_sample_seed():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
    simulator = ccq.mps_simulator.MPSSimulator(seed=1234)
    result = simulator.run(circuit, repetitions=20)
    measured = result.measurements['q']
    result_string = ''.join(map(lambda x: str(int(x[0])), measured))
    assert result_string == '01011001110111011011'


def test_run_no_repetitions():
    q0 = qubitron.LineQubit(0)
    simulator = ccq.mps_simulator.MPSSimulator()
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=0)
    assert len(result.measurements['q(0)']) == 0


def test_run_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = ccq.mps_simulator.MPSSimulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.run_sweep(circuit, qubitron.ParamResolver({}))


def test_deterministic_gate_noise():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.I(q), qubitron.measure(q))

    simulator1 = ccq.mps_simulator.MPSSimulator(noise=qubitron.X)
    result1 = simulator1.run(circuit, repetitions=10)

    simulator2 = ccq.mps_simulator.MPSSimulator(noise=qubitron.X)
    result2 = simulator2.run(circuit, repetitions=10)

    assert result1 == result2

    simulator3 = ccq.mps_simulator.MPSSimulator(noise=qubitron.Z)
    result3 = simulator3.run(circuit, repetitions=10)

    assert result1 != result3


def test_nondeterministic_mixture_noise():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.I(q), qubitron.measure(q))

    simulator = ccq.mps_simulator.MPSSimulator(
        noise=qubitron.ConstantQubitNoiseModel(qubitron.depolarize(0.5))
    )
    result1 = simulator.run(circuit, repetitions=50)
    result2 = simulator.run(circuit, repetitions=50)

    assert result1 != result2


def test_unsupported_noise_fails():
    with pytest.raises(ValueError, match='noise must be unitary or mixture but was'):
        ccq.mps_simulator.MPSSimulator(noise=qubitron.amplitude_damp(0.5))


def test_state_copy():
    sim = ccq.mps_simulator.MPSSimulator()

    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.H(q))

    state_Ms = []
    for step in sim.simulate_moment_steps(circuit):
        state_Ms.append(step.state.M)
    for x, y in itertools.combinations(state_Ms, 2):
        assert len(x) == len(y)
        for i in range(len(x)):
            assert not np.shares_memory(x[i], y[i])


def test_simulation_state_initializer():
    expected_classical_data = qubitron.ClassicalDataDictionaryStore(
        _records={qubitron.MeasurementKey('test'): [(4,)]}
    )
    s = ccq.mps_simulator.MPSState(
        qubits=(qubitron.LineQubit(0),),
        prng=np.random.RandomState(0),
        classical_data=expected_classical_data,
    )
    assert s.qubits == (qubitron.LineQubit(0),)
    assert s.classical_data == expected_classical_data
    assert s.estimation_stats() == {
        'estimated_fidelity': 1.0,
        'memory_bytes': 16,
        'num_coefs_used': 2,
    }


def test_act_on_gate():
    args = ccq.mps_simulator.MPSState(qubits=qubitron.LineQubit.range(3), prng=np.random.RandomState(0))

    qubitron.act_on(qubitron.X, args, [qubitron.LineQubit(1)])
    np.testing.assert_allclose(
        args.state_vector().reshape((2, 2, 2)),
        qubitron.one_hot(index=(0, 1, 0), shape=(2, 2, 2), dtype=np.complex64),
    )
