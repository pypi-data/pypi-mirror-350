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

import itertools
import random
from unittest import mock

import numpy as np
import pytest
import sympy

import qubitron


def test_invalid_dtype():
    with pytest.raises(ValueError, match='complex'):
        qubitron.Simulator(dtype=np.int32)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_measurements(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)

    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_results(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)

    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_empty_circuit(dtype: type[np.complexfloating], split: bool):
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(qubitron.Circuit())


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_reset(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(
        qubitron.H(q0),
        qubitron.XPowGate(dimension=3)(q1) ** 2,
        qubitron.reset(q0),
        qubitron.measure(q0, key='m0'),
        qubitron.measure(q1, key='m1a'),
        qubitron.reset(q1),
        qubitron.measure(q1, key='m1b'),
    )
    meas = simulator.run(circuit, repetitions=100).measurements
    assert np.array_equal(meas['m0'], np.zeros((100, 1)))
    assert np.array_equal(meas['m1a'], np.full((100, 1), 2))
    assert np.array_equal(meas['m1b'], np.zeros((100, 1)))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_bit_flips(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
            )
            result = simulator.run(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_at_end_no_repetitions(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
                )
                result = simulator.run(circuit, repetitions=0)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': np.empty([0, 1]), 'q(1)': np.empty([0, 1])}
                )
                assert result.repetitions == 0
        assert mock_sim.call_count == 0


def test_run_repetitions_terminal_measurement_stochastic():
    q = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.H(q), qubitron.measure(q, key='q'))
    results = qubitron.Simulator().run(c, repetitions=10000)
    assert 1000 <= np.count_nonzero(results.measurements['q']) < 9000


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_repetitions_measure_at_end(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': [[b0]] * 3, 'q(1)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        # We expect one call per b0,b1.
        assert mock_sim.call_count == 8


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_invert_mask_measure_not_terminal(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    (qubitron.X**b1)(q1),
                    qubitron.measure(q0, q1, key='m', invert_mask=(True, False)),
                    qubitron.X(q0),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(result.measurements, {'m': [[1 - b0, b1]] * 3})
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_partial_invert_mask_measure_not_terminal(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    (qubitron.X**b1)(q1),
                    qubitron.measure(q0, q1, key='m', invert_mask=(True,)),
                    qubitron.X(q0),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(result.measurements, {'m': [[1 - b0, b1]] * 3})
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measurement_not_terminal_no_repetitions(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    (qubitron.X**b1)(q1),
                    qubitron.measure(q0),
                    qubitron.measure(q1),
                    qubitron.H(q0),
                    qubitron.H(q1),
                )
                result = simulator.run(circuit, repetitions=0)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': np.empty([0, 1]), 'q(1)': np.empty([0, 1])}
                )
                assert result.repetitions == 0
        assert mock_sim.call_count == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_repetitions_measurement_not_terminal(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    (qubitron.X**b1)(q1),
                    qubitron.measure(q0),
                    qubitron.measure(q1),
                    qubitron.H(q0),
                    qubitron.H(q1),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': [[b0]] * 3, 'q(1)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0),
                (qubitron.X ** sympy.Symbol('b1'))(q1),
                qubitron.measure(q0),
                qubitron.measure(q1),
            )
            param_resolver = qubitron.ParamResolver({'b0': b0, 'b1': b1})
            result = simulator.run(circuit, param_resolver=param_resolver)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})
            np.testing.assert_equal(result.params, param_resolver)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_mixture(dtype: type[np.complexfloating], split: bool):
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.bit_flip(0.5)(q0), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert 20 < np.count_nonzero(result.measurements['q(0)']) < 80


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_mixture_with_gates(dtype: type[np.complexfloating], split: bool):
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split, seed=23)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.phase_flip(0.5)(q0), qubitron.H(q0), qubitron.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert np.count_nonzero(result.measurements['q(0)']) < 80
    assert np.count_nonzero(result.measurements['q(0)']) > 20


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_correlations(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1), qubitron.measure(q0, q1))
    for _ in range(10):
        result = simulator.run(circuit)
        bits = result.measurements['q(0),q(1)'][0]
        assert bits[0] == bits[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_multiple_qubits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0, q1))
            result = simulator.run(circuit, repetitions=3)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [[b0, b1]] * 3})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_sweeps_param_resolvers(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0),
                (qubitron.X ** sympy.Symbol('b1'))(q1),
                qubitron.measure(q0),
                qubitron.measure(q1),
            )
            params = [
                qubitron.ParamResolver({'b0': b0, 'b1': b1}),
                qubitron.ParamResolver({'b0': b1, 'b1': b0}),
            ]
            results = simulator.run_sweep(circuit, params=params)

            assert len(results) == 2
            np.testing.assert_equal(results[0].measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})
            np.testing.assert_equal(results[1].measurements, {'q(0)': [[b1]], 'q(1)': [[b0]]})
            assert results[0].params == params[0]
            assert results[1].params == params[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_random_unitary(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for _ in range(10):
        random_circuit = qubitron.testing.random_circuit(qubits=[q0, q1], n_moments=8, op_density=0.99)
        circuit_unitary = []
        for x in range(4):
            result = simulator.simulate(random_circuit, qubit_order=[q0, q1], initial_state=x)
            circuit_unitary.append(result.final_state_vector)
        np.testing.assert_almost_equal(
            np.transpose(np.array(circuit_unitary)),
            random_circuit.unitary(qubit_order=[q0, q1]),
            decimal=6,
        )


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_no_circuit(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit()
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state_vector, np.array([1, 0, 0, 0]))
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1))
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state_vector, np.array([0.5, 0.5, 0.5, 0.5]))
    assert len(result.measurements) == 0


class _TestMixture(qubitron.Gate):
    def __init__(self, gate_options):
        self.gate_options = gate_options

    def _qid_shape_(self):
        return qubitron.qid_shape(self.gate_options[0], ())

    def _mixture_(self):
        return [(1 / len(self.gate_options), qubitron.unitary(g)) for g in self.gate_options]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qudits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((3, 4))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.XPowGate(dimension=3)(q0), qubitron.XPowGate(dimension=4)(q1) ** 3)
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    expected = np.zeros(12)
    expected[4 * 1 + 3] = 1
    np.testing.assert_almost_equal(result.final_state_vector, expected)
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_mixtures(dtype: type[np.complexfloating], split: bool):
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.bit_flip(0.5)(q0), qubitron.measure(q0))
    count = 0
    for _ in range(100):
        result = simulator.simulate(circuit, qubit_order=[q0])
        if result.measurements['q(0)']:
            np.testing.assert_almost_equal(result.final_state_vector, np.array([0, 1]))
            count += 1
        else:
            np.testing.assert_almost_equal(result.final_state_vector, np.array([1, 0]))
    assert count < 80 and count > 20


@pytest.mark.parametrize(
    'dtype, split', itertools.product([np.complex64, np.complex128], [True, False])
)
def test_simulate_qudit_mixtures(dtype: type[np.complexfloating], split: bool):
    q0 = qubitron.LineQid(0, 3)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    mixture = _TestMixture(
        [
            qubitron.XPowGate(dimension=3) ** 0,
            qubitron.XPowGate(dimension=3),
            qubitron.XPowGate(dimension=3) ** 2,
        ]
    )
    circuit = qubitron.Circuit(mixture(q0), qubitron.measure(q0))
    counts = {0: 0, 1: 0, 2: 0}
    for _ in range(300):
        result = simulator.simulate(circuit, qubit_order=[q0])
        meas = result.measurements['q(0) (d=3)'][0]
        counts[meas] += 1
        np.testing.assert_almost_equal(
            result.final_state_vector, np.array([meas == 0, meas == 1, meas == 2])
        )
    assert counts[0] < 160 and counts[0] > 40
    assert counts[1] < 160 and counts[1] > 40
    assert counts[2] < 160 and counts[2] > 40


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_bit_flips(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
            )
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [b0], 'q(1)': [b1]})
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
@pytest.mark.parametrize(
    'initial_state',
    [1, qubitron.StateVectorSimulationState(initial_state=1, qubits=qubitron.LineQubit.range(2))],
)
def test_simulate_initial_state(
    dtype: type[np.complexfloating],
    split: bool,
    initial_state: int | qubitron.StateVectorSimulationState,
):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            result = simulator.simulate(circuit, initial_state=1)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][1 - b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulation_state(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            args = simulator._create_simulation_state(initial_state=1, qubits=(q0, q1))
            result = simulator.simulate(circuit, initial_state=args)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][1 - b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qubit_order(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            result = simulator.simulate(circuit, qubit_order=[q1, q0])
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b1][b0] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0), (qubitron.X ** sympy.Symbol('b1'))(q1)
            )
            resolver = {'b0': b0, 'b1': b1}
            result = simulator.simulate(circuit, param_resolver=resolver)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))
            assert result.params == qubitron.ParamResolver(resolver)
            assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_measure_multiple_qubits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0, q1))
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [b0, b1]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_sweeps_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0), (qubitron.X ** sympy.Symbol('b1'))(q1)
            )
            params = [
                qubitron.ParamResolver({'b0': b0, 'b1': b1}),
                qubitron.ParamResolver({'b0': b1, 'b1': b0}),
            ]
            results = simulator.simulate_sweep(circuit, params=params)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(results[0].final_state_vector, np.reshape(expected_state, 4))

            expected_state = np.zeros(shape=(2, 2))
            expected_state[b1][b0] = 1.0
            np.testing.assert_equal(results[1].final_state_vector, np.reshape(expected_state, 4))

            assert results[0].params == params[0]
            assert results[1].params == params[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.H(q0), qubitron.H(q1))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            np.testing.assert_almost_equal(step.state_vector(copy=True), np.array([0.5] * 4))
        else:
            np.testing.assert_almost_equal(step.state_vector(copy=True), np.array([1, 0, 0, 0]))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_empty_circuit(dtype: type[np.complexfloating], split: bool):
    circuit = qubitron.Circuit()
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    step = None
    for step in simulator.simulate_moment_steps(circuit):
        pass
    assert np.allclose(step.state_vector(copy=True), np.array([1]))
    assert not step.qubit_map


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_sample(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
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


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_intermediate_measurement(
    dtype: type[np.complexfloating], split: bool
):
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0), qubitron.H(q0))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 1:
            result = int(step.measurements['q(0)'][0])
            expected = np.zeros(2)
            expected[result] = 1
            np.testing.assert_almost_equal(step.state_vector(copy=True), expected)
        if i == 2:
            expected = np.array([np.sqrt(0.5), np.sqrt(0.5) * (-1) ** result])
            np.testing.assert_almost_equal(step.state_vector(copy=True), expected)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values(dtype: type[np.complexfloating], split: bool):
    # Compare with test_expectation_from_state_vector_two_qubit_states
    # in file: qubitron/ops/linear_combinations_test.py
    q0, q1 = qubitron.LineQubit.range(2)
    psum1 = qubitron.Z(q0) + 3.2 * qubitron.Z(q1)
    psum2 = -1 * qubitron.X(q0) + 2 * qubitron.X(q1)
    c1 = qubitron.Circuit(qubitron.I(q0), qubitron.X(q1))
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    result = simulator.simulate_expectation_values(c1, [psum1, psum2])
    assert qubitron.approx_eq(result[0], -2.2, atol=1e-6)
    assert qubitron.approx_eq(result[1], 0, atol=1e-6)

    c2 = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1))
    result = simulator.simulate_expectation_values(c2, [psum1, psum2])
    assert qubitron.approx_eq(result[0], 0, atol=1e-6)
    assert qubitron.approx_eq(result[1], 1, atol=1e-6)

    psum3 = qubitron.Z(q0) + qubitron.X(q1)
    c3 = qubitron.Circuit(qubitron.I(q0), qubitron.H(q1))
    result = simulator.simulate_expectation_values(c3, psum3)
    assert qubitron.approx_eq(result[0], 2, atol=1e-6)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values_terminal_measure(dtype: type[np.complexfloating], split: bool):
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0))
    obs = qubitron.Z(q0)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)
    with pytest.raises(ValueError):
        _ = simulator.simulate_expectation_values(circuit, obs)

    results = {-1: 0, 1: 0}
    for _ in range(100):
        result = simulator.simulate_expectation_values(
            circuit, obs, permit_terminal_measurements=True
        )
        if qubitron.approx_eq(result[0], -1, atol=1e-6):
            results[-1] += 1
        if qubitron.approx_eq(result[0], 1, atol=1e-6):
            results[1] += 1

    # With a measurement after H, the Z-observable expects a specific state.
    assert results[-1] > 0
    assert results[1] > 0
    assert results[-1] + results[1] == 100

    circuit = qubitron.Circuit(qubitron.H(q0))
    results = {0: 0}
    for _ in range(100):
        result = simulator.simulate_expectation_values(
            circuit, obs, permit_terminal_measurements=True
        )
        if qubitron.approx_eq(result[0], 0, atol=1e-6):
            results[0] += 1

    # Without measurement after H, the Z-observable is indeterminate.
    assert results[0] == 100


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values_qubit_order(dtype: type[np.complexfloating], split: bool):
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.X(q2))
    obs = qubitron.X(q0) + qubitron.X(q1) - qubitron.Z(q2)
    simulator = qubitron.Simulator(dtype=dtype, split_untangled_states=split)

    result = simulator.simulate_expectation_values(circuit, obs)
    assert qubitron.approx_eq(result[0], 3, atol=1e-6)

    # Adjusting the qubit order has no effect on the observables.
    result_flipped = simulator.simulate_expectation_values(circuit, obs, qubit_order=[q1, q2, q0])
    assert qubitron.approx_eq(result_flipped[0], 3, atol=1e-6)


def test_invalid_run_no_unitary():
    class NoUnitary(qubitron.testing.SingleQubitGate):
        pass

    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator()
    circuit = qubitron.Circuit(NoUnitary()(q0))
    circuit.append([qubitron.measure(q0, key='meas')])
    with pytest.raises(TypeError, match='unitary'):
        simulator.run(circuit)


def test_allocates_new_state():
    class NoUnitary(qubitron.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs):
            return np.copy(args.target_tensor)

    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator()
    circuit = qubitron.Circuit(NoUnitary()(q0))

    initial_state = np.array([np.sqrt(0.5), np.sqrt(0.5)], dtype=np.complex64)
    result = simulator.simulate(circuit, initial_state=initial_state)
    np.testing.assert_array_almost_equal(result.state_vector(), initial_state)
    assert not initial_state is result.state_vector()


def test_does_not_modify_initial_state():
    q0 = qubitron.LineQubit(0)
    simulator = qubitron.Simulator()

    class InPlaceUnitary(qubitron.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs):
            args.target_tensor[0], args.target_tensor[1] = (
                args.target_tensor[1],
                args.target_tensor[0],
            )
            return args.target_tensor

    circuit = qubitron.Circuit(InPlaceUnitary()(q0))

    initial_state = np.array([1, 0], dtype=np.complex64)
    result = simulator.simulate(circuit, initial_state=initial_state)
    np.testing.assert_array_almost_equal(np.array([1, 0], dtype=np.complex64), initial_state)
    np.testing.assert_array_almost_equal(
        result.state_vector(), np.array([0, 1], dtype=np.complex64)
    )


def test_simulator_step_state_mixin():
    qubits = qubitron.LineQubit.range(2)
    args = qubitron.StateVectorSimulationState(
        available_buffer=np.array([0, 1, 0, 0]).reshape((2, 2)),
        prng=qubitron.value.parse_random_state(0),
        qubits=qubits,
        initial_state=np.array([0, 1, 0, 0], dtype=np.complex64).reshape((2, 2)),
        dtype=np.complex64,
    )
    result = qubitron.SparseSimulatorStep(sim_state=args, dtype=np.complex64)
    rho = np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(rho, result.density_matrix_of(qubits))
    bloch = np.array([0, 0, -1])
    np.testing.assert_array_almost_equal(bloch, result.bloch_vector_of(qubits[1]))

    assert result.dirac_notation() == '|01⟩'


def test_sparse_simulator_repr():
    qubits = qubitron.LineQubit.range(2)
    args = qubitron.StateVectorSimulationState(
        available_buffer=np.array([0, 1, 0, 0]).reshape((2, 2)),
        prng=qubitron.value.parse_random_state(0),
        qubits=qubits,
        initial_state=np.array([0, 1, 0, 0], dtype=np.complex64).reshape((2, 2)),
        dtype=np.complex64,
    )
    step = qubitron.SparseSimulatorStep(sim_state=args, dtype=np.complex64)
    # No equality so cannot use qubitron.testing.assert_equivalent_repr
    assert (
        repr(step) == "qubitron.SparseSimulatorStep(sim_state=qubitron.StateVectorSimulationState("
        "initial_state=np.array([[0j, (1+0j)], [0j, 0j]], dtype=np.dtype('complex64')), "
        "qubits=(qubitron.LineQubit(0), qubitron.LineQubit(1)), "
        "classical_data=qubitron.ClassicalDataDictionaryStore()), dtype=np.dtype('complex64'))"
    )


class MultiHTestGate(qubitron.testing.TwoQubitGate):
    def _decompose_(self, qubits):
        return qubitron.H.on_each(*qubits)


def test_simulates_composite():
    c = qubitron.Circuit(MultiHTestGate().on(*qubitron.LineQubit.range(2)))
    expected = np.array([0.5] * 4)
    np.testing.assert_allclose(
        c.final_state_vector(ignore_terminal_measurements=False, dtype=np.complex64), expected
    )
    np.testing.assert_allclose(qubitron.Simulator().simulate(c).state_vector(), expected)


def test_simulate_measurement_inversions():
    q = qubitron.NamedQubit('q')

    c = qubitron.Circuit(qubitron.measure(q, key='q', invert_mask=(True,)))
    assert qubitron.Simulator().simulate(c).measurements == {'q': np.array([True])}

    c = qubitron.Circuit(qubitron.measure(q, key='q', invert_mask=(False,)))
    assert qubitron.Simulator().simulate(c).measurements == {'q': np.array([False])}


def test_works_on_pauli_string_phasor():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(np.exp(0.5j * np.pi * qubitron.X(a) * qubitron.X(b)))
    sim = qubitron.Simulator()
    result = sim.simulate(c).state_vector()
    np.testing.assert_allclose(result.reshape(4), np.array([0, 0, 0, 1j]), atol=1e-8)


def test_works_on_pauli_string():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(a) * qubitron.X(b))
    sim = qubitron.Simulator()
    result = sim.simulate(c).state_vector()
    np.testing.assert_allclose(result.reshape(4), np.array([0, 0, 0, 1]), atol=1e-8)


def test_measure_at_end_invert_mask():
    simulator = qubitron.Simulator()
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.measure(a, key='a', invert_mask=(True,)))
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['a'], np.array([[1]] * 4))


def test_measure_at_end_invert_mask_multiple_qubits():
    simulator = qubitron.Simulator()
    a, b, c = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(a, key='a', invert_mask=(True,)),
        qubitron.measure(b, c, key='bc', invert_mask=(False, True)),
    )
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['a'], np.array([[True]] * 4))
    np.testing.assert_equal(result.measurements['bc'], np.array([[0, 1]] * 4))


def test_measure_at_end_invert_mask_partial():
    simulator = qubitron.Simulator()
    a, _, c = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.measure(a, c, key='ac', invert_mask=(True,)))
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['ac'], np.array([[1, 0]] * 4))


def test_qudit_invert_mask():
    q0, q1, q2, q3, q4 = qubitron.LineQid.for_qid_shape((2, 3, 3, 3, 4))
    c = qubitron.Circuit(
        qubitron.XPowGate(dimension=2)(q0),
        qubitron.XPowGate(dimension=3)(q2),
        qubitron.XPowGate(dimension=3)(q3) ** 2,
        qubitron.XPowGate(dimension=4)(q4) ** 3,
        qubitron.measure(q0, q1, q2, q3, q4, key='a', invert_mask=(True,) * 4),
    )
    assert np.all(qubitron.Simulator().run(c).measurements['a'] == [[0, 1, 0, 2, 3]])


def test_compute_amplitudes():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(a), qubitron.H(a), qubitron.H(b))
    sim = qubitron.Simulator()

    result = sim.compute_amplitudes(c, [0])
    np.testing.assert_allclose(np.array(result), np.array([0.5]))

    result = sim.compute_amplitudes(c, [1, 2, 3])
    np.testing.assert_allclose(np.array(result), np.array([0.5, -0.5, -0.5]))

    result = sim.compute_amplitudes(c, (1, 2, 3), qubit_order=(b, a))
    np.testing.assert_allclose(np.array(result), np.array([-0.5, 0.5, -0.5]))


def test_compute_amplitudes_bad_input():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(a), qubitron.H(a), qubitron.H(b))
    sim = qubitron.Simulator()

    with pytest.raises(ValueError, match='1-dimensional'):
        _ = sim.compute_amplitudes(c, np.array([[0, 0]]))


def test_sample_from_amplitudes():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1), qubitron.X(q1))
    sim = qubitron.Simulator(seed=1)
    result = sim.sample_from_amplitudes(circuit, {}, sim._prng, repetitions=100)
    assert 40 < result[1] < 60
    assert 40 < result[2] < 60
    assert 0 not in result
    assert 3 not in result


def test_sample_from_amplitudes_teleport():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    # Initialize q0 to some state, teleport it to q2, then clean up.
    circuit = qubitron.Circuit(
        qubitron.H(q1),
        qubitron.CNOT(q1, q2),
        qubitron.X(q0) ** sympy.Symbol('t'),
        qubitron.CNOT(q0, q1),
        qubitron.H(q0),
        qubitron.CNOT(q1, q2),
        qubitron.CZ(q0, q2),
        qubitron.H(q0),
        qubitron.H(q1),
    )
    sim = qubitron.Simulator(seed=1)

    # Full X, always produces |1) state
    result_a = sim.sample_from_amplitudes(circuit, {'t': 1}, sim._prng, repetitions=100)
    assert result_a == {1: 100}

    # sqrt of X, produces 50:50 state
    result_b = sim.sample_from_amplitudes(circuit, {'t': 0.5}, sim._prng, repetitions=100)
    assert 40 < result_b[0] < 60
    assert 40 < result_b[1] < 60

    # X^(1/4), produces ~85:15 state
    result_c = sim.sample_from_amplitudes(circuit, {'t': 0.25}, sim._prng, repetitions=100)
    assert 80 < result_c[0]
    assert result_c[1] < 20


def test_sample_from_amplitudes_nonunitary_fails():
    q0, q1 = qubitron.LineQubit.range(2)
    sim = qubitron.Simulator(seed=1)

    circuit1 = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0, key='m'))
    with pytest.raises(ValueError, match='does not support intermediate measurement'):
        _ = sim.sample_from_amplitudes(circuit1, {}, sim._prng)

    circuit2 = qubitron.Circuit(
        qubitron.H(q0), qubitron.CNOT(q0, q1), qubitron.amplitude_damp(0.01)(q0), qubitron.amplitude_damp(0.01)(q1)
    )
    with pytest.raises(ValueError, match='does not support non-unitary'):
        _ = sim.sample_from_amplitudes(circuit2, {}, sim._prng)


def test_run_sweep_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.run_sweep(circuit, qubitron.ParamResolver({}))


def test_simulate_sweep_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.simulate_sweep(circuit, qubitron.ParamResolver({}))


def test_random_seed():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a))

    sim = qubitron.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )

    sim = qubitron.Simulator(seed=np.random.RandomState(1234))
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )


def test_random_seed_does_not_modify_global_state_terminal_measurements():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a))

    sim = qubitron.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = qubitron.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_does_not_modify_global_state_non_terminal_measurements():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(
        qubitron.X(a) ** 0.5, qubitron.measure(a, key='a0'), qubitron.X(a) ** 0.5, qubitron.measure(a, key='a1')
    )

    sim = qubitron.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = qubitron.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_does_not_modify_global_state_mixture():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.depolarize(0.5).on(a), qubitron.measure(a))

    sim = qubitron.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = qubitron.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_terminal_measurements_deterministic():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a, key='a'))
    sim = qubitron.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=30)
    result2 = sim.run(circuit, repetitions=30)
    assert np.all(
        result1.measurements['a']
        == [
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
        ]
    )
    assert np.all(
        result2.measurements['a']
        == [
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ]
    )


def test_random_seed_non_terminal_measurements_deterministic():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(
        qubitron.X(a) ** 0.5, qubitron.measure(a, key='a'), qubitron.X(a) ** 0.5, qubitron.measure(a, key='b')
    )
    sim = qubitron.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=30)
    assert np.all(
        result.measurements['a']
        == [
            [0],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [0],
            [0],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
        ]
    )
    assert np.all(
        result.measurements['b']
        == [
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
        ]
    )


def test_random_seed_mixture_deterministic():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(
        qubitron.depolarize(0.9).on(a),
        qubitron.depolarize(0.9).on(a),
        qubitron.depolarize(0.9).on(a),
        qubitron.depolarize(0.9).on(a),
        qubitron.depolarize(0.9).on(a),
        qubitron.measure(a, key='a'),
    )
    sim = qubitron.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=30)
    assert np.all(
        result.measurements['a']
        == [
            [1],
            [0],
            [0],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [0],
            [0],
            [0],
            [0],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
        ]
    )


def test_entangled_reset_does_not_break_randomness():
    """Test for bad assumptions on caching the wave function on general channels.

    A previous version of qubitron made the mistake of assuming that it was okay to
    cache the wavefunction produced by general channels on unrelated qubits
    before repeatedly sampling measurements. This test checks for that mistake.
    """

    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.H(a), qubitron.CNOT(a, b), qubitron.ResetChannel().on(a), qubitron.measure(b, key='out')
    )
    samples = qubitron.Simulator().sample(circuit, repetitions=100)['out']
    counts = samples.value_counts()
    assert len(counts) == 2
    assert 10 <= counts[0] <= 90
    assert 10 <= counts[1] <= 90


def test_overlapping_measurements_at_end():
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.H(a),
        qubitron.CNOT(a, b),
        # These measurements are not on independent qubits but they commute.
        qubitron.measure(a, key='a'),
        qubitron.measure(a, key='not a', invert_mask=(True,)),
        qubitron.measure(b, key='b'),
        qubitron.measure(a, b, key='ab'),
    )

    samples = qubitron.Simulator().sample(circuit, repetitions=100)
    np.testing.assert_array_equal(samples['a'].values, samples['not a'].values ^ 1)
    np.testing.assert_array_equal(
        samples['a'].values * 2 + samples['b'].values, samples['ab'].values
    )

    counts = samples['b'].value_counts()
    assert len(counts) == 2
    assert 10 <= counts[0] <= 90
    assert 10 <= counts[1] <= 90


def test_separated_measurements():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        [
            qubitron.H(a),
            qubitron.H(b),
            qubitron.CZ(a, b),
            qubitron.measure(a, key='a'),
            qubitron.CZ(a, b),
            qubitron.H(b),
            qubitron.measure(b, key='zero'),
        ]
    )
    sample = qubitron.Simulator().sample(c, repetitions=10)
    np.testing.assert_array_equal(sample['zero'].values, [0] * 10)


def test_state_vector_copy():
    sim = qubitron.Simulator(split_untangled_states=False)

    class InplaceGate(qubitron.testing.SingleQubitGate):
        """A gate that modifies the target tensor in place, multiply by -1."""

        def _apply_unitary_(self, args):
            args.target_tensor *= -1.0
            return args.target_tensor

    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(InplaceGate()(q), InplaceGate()(q))

    vectors = []
    for step in sim.simulate_moment_steps(circuit):
        vectors.append(step.state_vector(copy=True))
    for x, y in itertools.combinations(vectors, 2):
        assert not np.shares_memory(x, y)

    # If the state vector is not copied, then applying second InplaceGate
    # causes old state to be modified.
    vectors = []
    copy_of_vectors = []
    for step in sim.simulate_moment_steps(circuit):
        state_vector = step.state_vector()
        vectors.append(state_vector)
        copy_of_vectors.append(state_vector.copy())
    assert any(not np.array_equal(x, y) for x, y in zip(vectors, copy_of_vectors))


def test_final_state_vector_is_not_last_object():
    sim = qubitron.Simulator()

    q = qubitron.LineQubit(0)
    initial_state = np.array([1, 0], dtype=np.complex64)
    circuit = qubitron.Circuit(qubitron.wait(q))
    result = sim.simulate(circuit, initial_state=initial_state)
    assert result.state_vector() is not initial_state
    assert not np.shares_memory(result.state_vector(), initial_state)
    np.testing.assert_equal(result.state_vector(), initial_state)


def test_deterministic_gate_noise():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.I(q), qubitron.measure(q))

    simulator1 = qubitron.Simulator(noise=qubitron.X)
    result1 = simulator1.run(circuit, repetitions=10)

    simulator2 = qubitron.Simulator(noise=qubitron.X)
    result2 = simulator2.run(circuit, repetitions=10)

    assert result1 == result2

    simulator3 = qubitron.Simulator(noise=qubitron.Z)
    result3 = simulator3.run(circuit, repetitions=10)

    assert result1 != result3


def test_nondeterministic_mixture_noise():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.I(q), qubitron.measure(q))

    simulator = qubitron.Simulator(noise=qubitron.ConstantQubitNoiseModel(qubitron.depolarize(0.5)))
    result1 = simulator.run(circuit, repetitions=50)
    result2 = simulator.run(circuit, repetitions=50)

    assert result1 != result2


def test_pure_state_creation():
    sim = qubitron.Simulator()
    qids = qubitron.LineQubit.range(3)
    shape = qubitron.qid_shape(qids)
    args = sim._create_simulation_state(1, qids)
    values = list(args.values())
    arg = (
        values[0]
        .kronecker_product(values[1])
        .kronecker_product(values[2])
        .transpose_to_qubit_order(qids)
    )
    expected = qubitron.to_valid_state_vector(1, len(qids), qid_shape=shape)
    np.testing.assert_allclose(arg.target_tensor, expected.reshape(shape))


def test_noise_model():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))

    noise_model = qubitron.NoiseModel.from_noise_model_like(qubitron.depolarize(p=0.01))
    simulator = qubitron.Simulator(noise=noise_model)
    result = simulator.run(circuit, repetitions=100)

    assert 20 <= sum(result.measurements['q(0)'])[0] < 80


def test_separated_states_str_does_not_merge():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0), qubitron.measure(q1), qubitron.H(q0), qubitron.global_phase_operation(0 + 1j)
    )

    result = qubitron.Simulator().simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (qubitron.LineQubit(0),)
output vector: 0.707|0⟩ + 0.707|1⟩

qubits: (qubitron.LineQubit(1),)
output vector: |0⟩

phase:
output vector: 1j|⟩"""
    )


def test_separable_non_dirac_str():
    circuit = qubitron.Circuit()
    for i in range(4):
        circuit.append(qubitron.H(qubitron.LineQubit(i)))
        circuit.append(qubitron.CX(qubitron.LineQubit(0), qubitron.LineQubit(i + 1)))

    result = qubitron.Simulator().simulate(circuit)
    assert '+0.j' in str(result)


def test_unseparated_states_str():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0), qubitron.measure(q1), qubitron.H(q0), qubitron.global_phase_operation(0 + 1j)
    )

    result = qubitron.Simulator(split_untangled_states=False).simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (qubitron.LineQubit(0), qubitron.LineQubit(1))
output vector: 0.707j|00⟩ + 0.707j|10⟩"""
    )


@pytest.mark.parametrize('split', [True, False])
def test_measurement_preserves_phase(split: bool):
    c1, c2, t = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.H(t),
        qubitron.measure(t, key='t'),
        qubitron.CZ(c1, c2).with_classical_controls('t'),
        qubitron.reset(t),
    )
    simulator = qubitron.Simulator(split_untangled_states=split)
    # Run enough times that both options of |110> - |111> are likely measured.
    for _ in range(20):
        result = simulator.simulate(circuit, initial_state=(1, 1, 1), qubit_order=(c1, c2, t))
        assert result.dirac_notation() == '|110⟩'
