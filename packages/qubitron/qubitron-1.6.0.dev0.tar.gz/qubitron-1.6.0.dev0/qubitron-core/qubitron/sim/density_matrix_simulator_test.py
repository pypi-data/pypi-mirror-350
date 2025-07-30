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

import itertools
import random
from unittest import mock

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


class _TestMixture(qubitron.Gate):
    def __init__(self, gate_options):
        self.gate_options = gate_options

    def _qid_shape_(self):
        return qubitron.qid_shape(self.gate_options[0], ())

    def _mixture_(self):
        return [(1 / len(self.gate_options), qubitron.unitary(g)) for g in self.gate_options]


class _TestDecomposingChannel(qubitron.Gate):
    def __init__(self, channels):
        self.channels = channels

    def _qid_shape_(self):
        return tuple(d for chan in self.channels for d in qubitron.qid_shape(chan))

    def _decompose_(self, qubits):
        return [chan.on(q) for chan, q in zip(self.channels, qubits)]


def test_invalid_dtype():
    with pytest.raises(ValueError, match='complex'):
        qubitron.DensityMatrixSimulator(dtype=np.int32)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_measurements(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)

    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_results(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)

    circuit = qubitron.Circuit(qubitron.X(q0), qubitron.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_empty_circuit(dtype: type[np.complexfloating], split: bool):
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(qubitron.Circuit())


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_bit_flips(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
            )
            result = simulator.run(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_bit_flips_with_dephasing(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
            )
            result = simulator.run(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_qudit_increments(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((3, 4))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1, 2]:
        for b1 in [0, 1, 2, 3]:
            circuit = qubitron.Circuit(
                [qubitron.XPowGate(dimension=3)(q0)] * b0,
                [qubitron.XPowGate(dimension=4)(q1)] * b1,
                qubitron.measure(q0),
                qubitron.measure(q1),
            )
            result = simulator.run(circuit)
            np.testing.assert_equal(
                result.measurements, {'q(0) (d=3)': [[b0]], 'q(1) (d=4)': [[b1]]}
            )


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_not_channel_op(dtype: type[np.complexfloating], split: bool):
    class BadOp(qubitron.Operation):
        def __init__(self, qubits):
            self._qubits = qubits

        @property
        def qubits(self):
            return self._qubits

        def with_qubits(self, *new_qubits):  # pragma: no cover
            return BadOp(self._qubits)

    q0 = qubitron.LineQubit(0)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit([BadOp([q0])])
    with pytest.raises(TypeError):
        simulator.simulate(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_mixture(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.bit_flip(0.5)(q0), qubitron.measure(q0), qubitron.measure(q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    result = simulator.run(circuit, repetitions=100)
    np.testing.assert_equal(result.measurements['q(1)'], [[0]] * 100)
    # Test that we get at least one of each result. Probability of this test
    # failing is 2 ** (-99).
    q0_measurements = set(x[0] for x in result.measurements['q(0)'].tolist())
    assert q0_measurements == {0, 1}


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_qudit_mixture(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((3, 2))
    mixture = _TestMixture(
        [
            qubitron.XPowGate(dimension=3) ** 0,
            qubitron.XPowGate(dimension=3),
            qubitron.XPowGate(dimension=3) ** 2,
        ]
    )
    circuit = qubitron.Circuit(mixture(q0), qubitron.measure(q0), qubitron.measure(q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    result = simulator.run(circuit, repetitions=100)
    np.testing.assert_equal(result.measurements['q(1) (d=2)'], [[0]] * 100)
    # Test that we get at least one of each result. Probability of this test
    # failing is about 3 * (2/3) ** 100.
    q0_measurements = set(x[0] for x in result.measurements['q(0) (d=3)'].tolist())
    assert q0_measurements == {0, 1, 2}


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_channel(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(q0), qubitron.amplitude_damp(0.5)(q0), qubitron.measure(q0), qubitron.measure(q1)
    )

    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    result = simulator.run(circuit, repetitions=100)
    np.testing.assert_equal(result.measurements['q(1)'], [[0]] * 100)
    # Test that we get at least one of each result. Probability of this test
    # failing is 2 ** (-99).
    q0_measurements = set(x[0] for x in result.measurements['q(0)'].tolist())
    assert q0_measurements == {0, 1}


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_decomposable_channel(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)

    circuit = qubitron.Circuit(
        qubitron.X(q0),
        _TestDecomposingChannel([qubitron.amplitude_damp(0.5), qubitron.amplitude_damp(0)]).on(q0, q1),
        qubitron.measure(q0),
        qubitron.measure(q1),
    )

    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    result = simulator.run(circuit, repetitions=100)
    np.testing.assert_equal(result.measurements['q(1)'], [[0]] * 100)
    # Test that we get at least one of each result. Probability of this test
    # failing is 2 ** (-99).
    q0_measurements = set(x[0] for x in result.measurements['q(0)'].tolist())
    assert q0_measurements == {0, 1}


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_qudit_channel(dtype: type[np.complexfloating], split: bool):
    class TestChannel(qubitron.Gate):
        def _qid_shape_(self):
            return (3,)

        def _kraus_(self):
            return [
                np.array([[1, 0, 0], [0, 0.5**0.5, 0], [0, 0, 0.5**0.5]]),
                np.array([[0, 0.5**0.5, 0], [0, 0, 0], [0, 0, 0]]),
                np.array([[0, 0, 0], [0, 0, 0.5**0.5], [0, 0, 0]]),
            ]

    q0, q1 = qubitron.LineQid.for_qid_shape((3, 4))
    circuit = qubitron.Circuit(
        qubitron.XPowGate(dimension=3)(q0) ** 2,
        TestChannel()(q0),
        TestChannel()(q0),
        qubitron.measure(q0),
        qubitron.measure(q1),
    )

    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    result = simulator.run(circuit, repetitions=100)
    np.testing.assert_equal(result.measurements['q(1) (d=4)'], [[0]] * 100)
    # Test that we get at least one of each result. Probability of this test
    # failing is about (3/4) ** 100.
    q0_measurements = set(x[0] for x in result.measurements['q(0) (d=3)'].tolist())
    assert q0_measurements == {0, 1, 2}


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_at_end_no_repetitions(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_repetitions_measure_at_end(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
        assert mock_sim.call_count == 8


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_qudits_repetitions_measure_at_end(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1, 2]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    qubitron.XPowGate(dimension=3)(q1) ** b1,
                    qubitron.measure(q0),
                    qubitron.measure(q1),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0) (d=2)': [[b0]] * 3, 'q(1) (d=3)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        assert mock_sim.call_count == 12


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measurement_not_terminal_no_repetitions(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
        assert mock_sim.call_count == 16


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_qudits_repetitions_measurement_not_terminal(
    dtype: type[np.complexfloating], split: bool
):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1, 2]:
                circuit = qubitron.Circuit(
                    (qubitron.X**b0)(q0),
                    qubitron.XPowGate(dimension=3)(q1) ** b1,
                    qubitron.measure(q0),
                    qubitron.measure(q1),
                    qubitron.H(q0),
                    qubitron.XPowGate(dimension=3)(q1) ** (-b1),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0) (d=2)': [[b0]] * 3, 'q(1) (d=3)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        assert mock_sim.call_count == 24


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0),
                (qubitron.X ** sympy.Symbol('b1'))(q1),
                qubitron.measure(q0),
                qubitron.measure(q1),
            )
            param_resolver = {'b0': b0, 'b1': b1}
            result = simulator.run(circuit, param_resolver=param_resolver)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})
            # pylint: disable=line-too-long
            np.testing.assert_equal(result.params, qubitron.ParamResolver(param_resolver))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_correlations(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1), qubitron.measure(q0, q1))
    for _ in range(10):
        result = simulator.run(circuit)
        bits = result.measurements['q(0),q(1)'][0]
        assert bits[0] == bits[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_multiple_qubits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0, q1))
            result = simulator.run(circuit, repetitions=3)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [[b0, b1]] * 3})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_multiple_qudits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1, 2]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), qubitron.XPowGate(dimension=3)(q1) ** b1, qubitron.measure(q0, q1)
            )
            result = simulator.run(circuit, repetitions=3)
            np.testing.assert_equal(result.measurements, {'q(0) (d=2),q(1) (d=3)': [[b0, b1]] * 3})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_sweeps_param_resolvers(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
def test_simulate_no_circuit(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit()
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    expected = np.zeros((4, 4))
    expected[0, 0] = 1.0
    np.testing.assert_almost_equal(result.final_density_matrix, expected)
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1))
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_density_matrix, np.ones((4, 4)) * 0.25)
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qudits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.XPowGate(dimension=3)(q1) ** 2)
    result = simulator.simulate(circuit, qubit_order=[q1, q0])
    expected = np.zeros((6, 6))
    expected[4:, 4:] = np.ones((2, 2)) / 2
    np.testing.assert_almost_equal(result.final_density_matrix, expected)
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_reset_one_qubit_does_not_affect_partial_trace_of_other_qubits(
    dtype: type[np.complexfloating], split: bool
):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CX(q0, q1), qubitron.reset(q0))
    result = simulator.simulate(circuit)
    expected = np.zeros((4, 4), dtype=dtype)
    expected[0, 0] = 0.5
    expected[1, 1] = 0.5
    np.testing.assert_almost_equal(result.final_density_matrix, expected)


@pytest.mark.parametrize(
    'dtype,circuit',
    itertools.product(
        [np.complex64, np.complex128],
        [qubitron.testing.random_circuit(qubitron.LineQubit.range(4), 5, 0.9) for _ in range(20)],
    ),
)
def test_simulate_compare_to_state_vector_simulator(dtype: type[np.complexfloating], circuit):
    qubits = qubitron.LineQubit.range(4)
    pure_result = (
        qubitron.Simulator(dtype=dtype).simulate(circuit, qubit_order=qubits).density_matrix_of()
    )
    mixed_result = (
        qubitron.DensityMatrixSimulator(dtype=dtype)
        .simulate(circuit, qubit_order=qubits)
        .final_density_matrix
    )
    assert mixed_result.shape == (16, 16)
    np.testing.assert_almost_equal(mixed_result, pure_result, decimal=6)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_bit_flips(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0), qubitron.measure(q1)
            )
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [b0], 'q(1)': [b1]})
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[b0 * 2 + b1, b0 * 2 + b1] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qudit_increments(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1, 2]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0),
                (qubitron.XPowGate(dimension=3)(q1),) * b1,
                qubitron.measure(q0),
                qubitron.measure(q1),
            )
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0) (d=2)': [b0], 'q(1) (d=3)': [b1]})
            expected_density_matrix = np.zeros(shape=(6, 6))
            expected_density_matrix[b0 * 3 + b1, b0 * 3 + b1] = 1.0
            np.testing.assert_allclose(result.final_density_matrix, expected_density_matrix)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
@pytest.mark.parametrize(
    'initial_state',
    [1, qubitron.DensityMatrixSimulationState(initial_state=1, qubits=qubitron.LineQubit.range(2))],
)
def test_simulate_initial_state(
    dtype: type[np.complexfloating],
    split: bool,
    initial_state: int | qubitron.DensityMatrixSimulationState,
):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            result = simulator.simulate(circuit, initial_state=1)
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[b0 * 2 + 1 - b1, b0 * 2 + 1 - b1] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulation_state(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            args = simulator._create_simulation_state(initial_state=1, qubits=(q0, q1))
            result = simulator.simulate(circuit, initial_state=args)
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[b0 * 2 + 1 - b1, b0 * 2 + 1 - b1] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)


def test_simulate_tps_initial_state():
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator()
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            result = simulator.simulate(circuit, initial_state=qubitron.KET_ZERO(q0) * qubitron.KET_ONE(q1))
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[b0 * 2 + 1 - b1, b0 * 2 + 1 - b1] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_initial_qudit_state(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((3, 4))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1, 2]:
        for b1 in [0, 1, 2, 3]:
            circuit = qubitron.Circuit(
                qubitron.XPowGate(dimension=3)(q0) ** b0, qubitron.XPowGate(dimension=4)(q1) ** b1
            )
            result = simulator.simulate(circuit, initial_state=6)
            expected_density_matrix = np.zeros(shape=(12, 12))
            expected_density_matrix[
                (b0 + 1) % 3 * 4 + (b1 + 2) % 4, (b0 + 1) % 3 * 4 + (b1 + 2) % 4
            ] = 1.0
            np.testing.assert_allclose(
                result.final_density_matrix, expected_density_matrix, atol=1e-15
            )


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qubit_order(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1))
            result = simulator.simulate(circuit, qubit_order=[q1, q0])
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[2 * b1 + b0, 2 * b1 + b0] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit(
                (qubitron.X ** sympy.Symbol('b0'))(q0), (qubitron.X ** sympy.Symbol('b1'))(q1)
            )
            resolver = qubitron.ParamResolver({'b0': b0, 'b1': b1})
            result = simulator.simulate(circuit, param_resolver=resolver)
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[2 * b0 + b1, 2 * b0 + b1] = 1.0
            np.testing.assert_equal(result.final_density_matrix, expected_density_matrix)
            assert result.params == resolver
            assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_measure_multiple_qubits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = qubitron.Circuit((qubitron.X**b0)(q0), (qubitron.X**b1)(q1), qubitron.measure(q0, q1))
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [b0, b1]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_measure_multiple_qudits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1, 2]:
            circuit = qubitron.Circuit(
                (qubitron.X**b0)(q0), qubitron.XPowGate(dimension=3)(q1) ** b1, qubitron.measure(q0, q1)
            )
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0) (d=2),q(1) (d=3)': [b0, b1]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_sweeps_param_resolver(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[2 * b0 + b1, 2 * b0 + b1] = 1.0
            np.testing.assert_equal(results[0].final_density_matrix, expected_density_matrix)

            expected_density_matrix = np.zeros(shape=(4, 4))
            expected_density_matrix[2 * b1 + b0, 2 * b1 + b0] = 1.0
            np.testing.assert_equal(results[1].final_density_matrix, expected_density_matrix)

            assert results[0].params == params[0]
            assert results[1].params == params[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.H(q0), qubitron.H(q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        assert qubitron.qid_shape(step) == (2, 2)
        if i == 0:
            np.testing.assert_almost_equal(step.density_matrix(), np.ones((4, 4)) / 4)
        else:
            np.testing.assert_almost_equal(step.density_matrix(), np.diag([1, 0, 0, 0]), decimal=6)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_qudits(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    circuit = qubitron.Circuit(
        qubitron.XPowGate(dimension=2)(q0),
        qubitron.XPowGate(dimension=3)(q1),
        qubitron.reset(q1),
        qubitron.XPowGate(dimension=3)(q1),
    )
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        assert qubitron.qid_shape(step) == (2, 3)
        if i == 0:
            np.testing.assert_almost_equal(step.density_matrix(), np.diag([0, 0, 0, 0, 1, 0]))
        elif i == 1:
            np.testing.assert_almost_equal(step.density_matrix(), np.diag([0, 0, 0, 1, 0, 0]))
        else:
            np.testing.assert_almost_equal(step.density_matrix(), np.diag([0, 0, 0, 0, 1, 0]))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_empty_circuit(dtype: type[np.complexfloating], split: bool):
    circuit = qubitron.Circuit()
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    step = None
    for step in simulator.simulate_moment_steps(circuit):
        pass
    assert np.allclose(step.density_matrix(), np.array([[1]]))
    assert not qubitron.qid_shape(step)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_sample(dtype: type[np.complexfloating], split: bool):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CNOT(q0, q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
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
def test_simulate_moment_steps_sample_qudits(dtype: type[np.complexfloating], split: bool):
    class TestGate(qubitron.Gate):
        """Swaps the 2nd qid |0> and |2> states when the 1st is |1>."""

        def _qid_shape_(self):
            return (2, 3)

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs):
            args.available_buffer[..., 1, 0] = args.target_tensor[..., 1, 2]
            args.target_tensor[..., 1, 2] = args.target_tensor[..., 1, 0]
            args.target_tensor[..., 1, 0] = args.available_buffer[..., 1, 0]
            return args.target_tensor

    q0, q1 = qubitron.LineQid.for_qid_shape((2, 3))
    circuit = qubitron.Circuit(qubitron.H(q0), TestGate()(q0, q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, 0]) or np.array_equal(sample, [False, 0])
        else:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, 2]) or np.array_equal(sample, [False, 0])


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_intermediate_measurement(
    dtype: type[np.complexfloating], split: bool
):
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0), qubitron.H(q0))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 1:
            result = int(step.measurements['q(0)'][0])
            expected = np.zeros((2, 2))
            expected[result, result] = 1
            np.testing.assert_almost_equal(step.density_matrix(), expected)
        if i == 2:
            expected = np.array([[0.5, 0.5 * (-1) ** result], [0.5 * (-1) ** result, 0.5]])
            np.testing.assert_almost_equal(step.density_matrix(), expected)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
def test_simulate_expectation_values(dtype):
    # Compare with test_expectation_from_state_vector_two_qubit_states
    # in file: qubitron/ops/linear_combinations_test.py
    q0, q1 = qubitron.LineQubit.range(2)
    psum1 = qubitron.Z(q0) + 3.2 * qubitron.Z(q1)
    psum2 = -1 * qubitron.X(q0) + 2 * qubitron.X(q1)
    c1 = qubitron.Circuit(qubitron.I(q0), qubitron.X(q1))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype)
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
def test_simulate_noisy_expectation_values(dtype):
    q0 = qubitron.LineQubit(0)
    psums = [qubitron.Z(q0), qubitron.X(q0)]
    c1 = qubitron.Circuit(qubitron.X(q0), qubitron.amplitude_damp(gamma=0.1).on(q0))
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype)
    result = simulator.simulate_expectation_values(c1, psums)
    # <Z> = (gamma - 1) + gamma = -0.8
    assert qubitron.approx_eq(result[0], -0.8, atol=1e-6)
    assert qubitron.approx_eq(result[1], 0, atol=1e-6)

    c2 = qubitron.Circuit(qubitron.H(q0), qubitron.depolarize(p=0.3).on(q0))
    result = simulator.simulate_expectation_values(c2, psums)
    assert qubitron.approx_eq(result[0], 0, atol=1e-6)
    # <X> = (1 - p) + (-p / 3) = 0.6
    assert qubitron.approx_eq(result[1], 0.6, atol=1e-6)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
def test_simulate_expectation_values_terminal_measure(dtype):
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.measure(q0))
    obs = qubitron.Z(q0)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype)
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
def test_simulate_expectation_values_qubit_order(dtype):
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.H(q1), qubitron.X(q2))
    obs = qubitron.X(q0) + qubitron.X(q1) - qubitron.Z(q2)
    simulator = qubitron.DensityMatrixSimulator(dtype=dtype)

    result = simulator.simulate_expectation_values(circuit, obs)
    assert qubitron.approx_eq(result[0], 3, atol=1e-6)

    # Adjusting the qubit order has no effect on the observables.
    result_flipped = simulator.simulate_expectation_values(circuit, obs, qubit_order=[q1, q2, q0])
    assert qubitron.approx_eq(result_flipped[0], 3, atol=1e-6)


def test_density_matrix_step_result_repr():
    q0 = qubitron.LineQubit(0)
    assert (
        repr(
            qubitron.DensityMatrixStepResult(
                sim_state=qubitron.DensityMatrixSimulationState(
                    initial_state=np.ones((2, 2)) * 0.5, qubits=[q0]
                )
            )
        )
        == "qubitron.DensityMatrixStepResult("
        "sim_state=qubitron.DensityMatrixSimulationState("
        "initial_state=np.array([[(0.5+0j), (0.5+0j)], [(0.5+0j), (0.5+0j)]], "
        "dtype=np.dtype('complex64')), "
        "qubits=(qubitron.LineQubit(0),), "
        "classical_data=qubitron.ClassicalDataDictionaryStore()), "
        "dtype=np.dtype('complex64'))"
    )


def test_density_matrix_trial_result_eq():
    q0 = qubitron.LineQubit(0)
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        initial_state=np.ones((2, 2)) * 0.5, qubits=[q0]
    )
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({}),
            measurements={},
            final_simulator_state=final_simulator_state,
        ),
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({}),
            measurements={},
            final_simulator_state=final_simulator_state,
        ),
    )
    eq.add_equality_group(
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({'s': 1}),
            measurements={},
            final_simulator_state=final_simulator_state,
        )
    )
    eq.add_equality_group(
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({'s': 1}),
            measurements={'m': np.array([[1]])},
            final_simulator_state=final_simulator_state,
        )
    )


def test_density_matrix_trial_result_qid_shape():
    q0, q1 = qubitron.LineQubit.range(2)
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        initial_state=np.ones((4, 4)) / 4, qubits=[q0, q1]
    )
    assert qubitron.qid_shape(
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({}),
            measurements={},
            final_simulator_state=final_simulator_state,
        )
    ) == (2, 2)
    q0, q1 = qubitron.LineQid.for_qid_shape((3, 4))
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        initial_state=np.ones((12, 12)) / 12, qubits=[q0, q1]
    )
    assert qubitron.qid_shape(
        qubitron.DensityMatrixTrialResult(
            params=qubitron.ParamResolver({}),
            measurements={},
            final_simulator_state=final_simulator_state,
        )
    ) == (3, 4)


def test_density_matrix_trial_result_repr():
    q0 = qubitron.LineQubit(0)
    dtype = np.complex64
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        available_buffer=[],
        prng=np.random.RandomState(0),
        qubits=[q0],
        initial_state=np.ones((2, 2), dtype=dtype) * 0.5,
        dtype=dtype,
    )
    trial_result = qubitron.DensityMatrixTrialResult(
        params=qubitron.ParamResolver({'s': 1}),
        measurements={'m': np.array([[1]], dtype=np.int32)},
        final_simulator_state=final_simulator_state,
    )
    expected_repr = (
        "qubitron.DensityMatrixTrialResult("
        "params=qubitron.ParamResolver({'s': 1}), "
        "measurements={'m': np.array([[1]], dtype=np.dtype('int32'))}, "
        "final_simulator_state=qubitron.DensityMatrixSimulationState("
        "initial_state=np.array([[(0.5+0j), (0.5+0j)], [(0.5+0j), (0.5+0j)]], "
        "dtype=np.dtype('complex64')), "
        "qubits=(qubitron.LineQubit(0),), "
        "classical_data=qubitron.ClassicalDataDictionaryStore()))"
    )
    assert repr(trial_result) == expected_repr
    assert eval(expected_repr) == trial_result


class XAsOp(qubitron.Operation):
    def __init__(self, q):
        self.q = q  # pragma: no cover

    @property
    def qubits(self):
        return (self.q,)  # pragma: no cover

    def with_qubits(self, *new_qubits):
        return XAsOp(new_qubits[0])  # pragma: no cover

    def _kraus_(self):
        return qubitron.kraus(qubitron.X)  # pragma: no cover


def test_works_on_operation():
    class XAsOp(qubitron.Operation):
        def __init__(self, q):
            self.q = q

        @property
        def qubits(self):
            return (self.q,)

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        def _kraus_(self):
            return qubitron.kraus(qubitron.X)

    s = qubitron.DensityMatrixSimulator()
    c = qubitron.Circuit(XAsOp(qubitron.LineQubit(0)))
    np.testing.assert_allclose(s.simulate(c).final_density_matrix, np.diag([0, 1]), atol=1e-8)


def test_works_on_pauli_string_phasor():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(np.exp(0.5j * np.pi * qubitron.X(a) * qubitron.X(b)))
    sim = qubitron.DensityMatrixSimulator()
    result = sim.simulate(c).final_density_matrix
    np.testing.assert_allclose(result.reshape(4, 4), np.diag([0, 0, 0, 1]), atol=1e-8)


def test_works_on_pauli_string():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.X(a) * qubitron.X(b))
    sim = qubitron.DensityMatrixSimulator()
    result = sim.simulate(c).final_density_matrix
    np.testing.assert_allclose(result.reshape(4, 4), np.diag([0, 0, 0, 1]), atol=1e-8)


def test_density_matrix_trial_result_str():
    q0 = qubitron.LineQubit(0)
    dtype = np.complex64
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        available_buffer=[],
        prng=np.random.RandomState(0),
        qubits=[q0],
        initial_state=np.ones((2, 2), dtype=dtype) * 0.5,
        dtype=dtype,
    )
    result = qubitron.DensityMatrixTrialResult(
        params=qubitron.ParamResolver({}), measurements={}, final_simulator_state=final_simulator_state
    )

    # numpy varies whitespace in its representation for different versions
    # Eliminate whitespace to harden tests against this variation
    result_no_whitespace = str(result).replace('\n', '').replace(' ', '')
    assert result_no_whitespace == (
        'measurements:(nomeasurements)'
        'qubits:(qubitron.LineQubit(0),)'
        'finaldensitymatrix:[[0.5+0.j0.5+0.j][0.5+0.j0.5+0.j]]'
    )


def test_density_matrix_trial_result_repr_pretty():
    q0 = qubitron.LineQubit(0)
    dtype = np.complex64
    final_simulator_state = qubitron.DensityMatrixSimulationState(
        available_buffer=[],
        prng=np.random.RandomState(0),
        qubits=[q0],
        initial_state=np.ones((2, 2), dtype=dtype) * 0.5,
        dtype=dtype,
    )
    result = qubitron.DensityMatrixTrialResult(
        params=qubitron.ParamResolver({}), measurements={}, final_simulator_state=final_simulator_state
    )

    fake_printer = qubitron.testing.FakePrinter()
    result._repr_pretty_(fake_printer, cycle=False)
    # numpy varies whitespace in its representation for different versions
    # Eliminate whitespace to harden tests against this variation
    result_no_whitespace = fake_printer.text_pretty.replace('\n', '').replace(' ', '')
    assert result_no_whitespace == (
        'measurements:(nomeasurements)'
        'qubits:(qubitron.LineQubit(0),)'
        'finaldensitymatrix:[[0.5+0.j0.5+0.j][0.5+0.j0.5+0.j]]'
    )

    qubitron.testing.assert_repr_pretty(result, "qubitron.DensityMatrixTrialResult(...)", cycle=True)


def test_run_sweep_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.DensityMatrixSimulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.run_sweep(circuit, qubitron.ParamResolver({}))


def test_simulate_sweep_parameters_not_resolved():
    a = qubitron.LineQubit(0)
    simulator = qubitron.DensityMatrixSimulator()
    circuit = qubitron.Circuit(qubitron.XPowGate(exponent=sympy.Symbol('a'))(a), qubitron.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.simulate_sweep(circuit, qubitron.ParamResolver({}))


def test_random_seed():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a))

    sim = qubitron.DensityMatrixSimulator(seed=1234)
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )

    sim = qubitron.DensityMatrixSimulator(seed=np.random.RandomState(1234))
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )


def test_random_seed_does_not_modify_global_state_terminal_measurements():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a))

    sim = qubitron.DensityMatrixSimulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = qubitron.DensityMatrixSimulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_does_not_modify_global_state_non_terminal_measurements():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(
        qubitron.X(a) ** 0.5, qubitron.measure(a, key='a0'), qubitron.X(a) ** 0.5, qubitron.measure(a, key='a1')
    )

    sim = qubitron.DensityMatrixSimulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = qubitron.DensityMatrixSimulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_terminal_measurements_deterministic():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.X(a) ** 0.5, qubitron.measure(a, key='a'))
    sim = qubitron.DensityMatrixSimulator(seed=1234)
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
    sim = qubitron.DensityMatrixSimulator(seed=1234)
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


def test_simulate_with_invert_mask():
    q0, q1, q2, q3, q4 = qubitron.LineQid.for_qid_shape((2, 3, 3, 3, 4))
    c = qubitron.Circuit(
        qubitron.XPowGate(dimension=2)(q0),
        qubitron.XPowGate(dimension=3)(q2),
        qubitron.XPowGate(dimension=3)(q3) ** 2,
        qubitron.XPowGate(dimension=4)(q4) ** 3,
        qubitron.measure(q0, q1, q2, q3, q4, key='a', invert_mask=(True,) * 4),
    )
    assert np.all(qubitron.DensityMatrixSimulator().run(c).measurements['a'] == [[0, 1, 0, 2, 3]])


def test_simulate_noise_with_terminal_measurements():
    q = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.measure(q))
    circuit2 = circuit1 + qubitron.I(q)

    simulator = qubitron.DensityMatrixSimulator(noise=qubitron.X)
    result1 = simulator.run(circuit1, repetitions=10)
    result2 = simulator.run(circuit2, repetitions=10)

    assert result1 == result2


def test_simulate_noise_with_subcircuit_measurements():
    q = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.measure(q))
    circuit2 = qubitron.Circuit(qubitron.CircuitOperation(qubitron.Circuit(qubitron.measure(q)).freeze()))

    simulator = qubitron.DensityMatrixSimulator(noise=qubitron.X)
    result1 = simulator.run(circuit1, repetitions=10)
    result2 = simulator.run(circuit2, repetitions=10)

    assert result1 == result2


def test_nonmeasuring_subcircuits_do_not_cause_sweep_repeat():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(qubitron.Circuit(qubitron.H(q)).freeze()), qubitron.measure(q, key='x')
    )
    simulator = qubitron.DensityMatrixSimulator()
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        simulator.run(circuit, repetitions=10)
        assert mock_sim.call_count == 2


def test_measuring_subcircuits_cause_sweep_repeat():
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(qubitron.Circuit(qubitron.measure(q)).freeze()), qubitron.measure(q, key='x')
    )
    simulator = qubitron.DensityMatrixSimulator()
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        simulator.run(circuit, repetitions=10)
        assert mock_sim.call_count == 11


def test_density_matrix_copy():
    sim = qubitron.DensityMatrixSimulator(split_untangled_states=False)

    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.H(q), qubitron.H(q))

    matrices = []
    for step in sim.simulate_moment_steps(circuit):
        matrices.append(step.density_matrix(copy=True))
    assert all(np.isclose(np.trace(x), 1.0) for x in matrices)
    for x, y in itertools.combinations(matrices, 2):
        assert not np.shares_memory(x, y)

    # If the density matrix is not copied, then applying second Hadamard
    # causes old state to be modified.
    matrices = []
    traces = []
    for step in sim.simulate_moment_steps(circuit):
        matrices.append(step.density_matrix(copy=False))
        traces.append(np.trace(step.density_matrix(copy=False)))
    assert any(not np.isclose(np.trace(x), 1.0) for x in matrices)
    assert all(np.isclose(x, 1.0) for x in traces)
    assert all(not np.shares_memory(x, y) for x, y in itertools.combinations(matrices, 2))


def test_final_density_matrix_is_not_last_object():
    sim = qubitron.DensityMatrixSimulator()

    q = qubitron.LineQubit(0)
    initial_state = np.array([[1, 0], [0, 0]], dtype=np.complex64)
    circuit = qubitron.Circuit(qubitron.wait(q))
    result = sim.simulate(circuit, initial_state=initial_state)
    assert result.final_density_matrix is not initial_state
    assert not np.shares_memory(result.final_density_matrix, initial_state)
    np.testing.assert_equal(result.final_density_matrix, initial_state)


def test_density_matrices_same_with_or_without_split_untangled_states():
    sim = qubitron.DensityMatrixSimulator(split_untangled_states=False)
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.H(q0), qubitron.CX.on(q0, q1), qubitron.reset(q1))
    result1 = sim.simulate(circuit).final_density_matrix
    sim = qubitron.DensityMatrixSimulator()
    result2 = sim.simulate(circuit).final_density_matrix
    assert np.allclose(result1, result2)


def test_large_untangled_okay():
    circuit = qubitron.Circuit()
    for i in range(59):
        for _ in range(9):
            circuit.append(qubitron.X(qubitron.LineQubit(i)))
        circuit.append(qubitron.measure(qubitron.LineQubit(i)))

    # Validate this can't be allocated with entangled state
    with pytest.raises(MemoryError, match='Unable to allocate'):
        _ = qubitron.DensityMatrixSimulator(split_untangled_states=False).simulate(circuit)

    # Validate a simulation run
    result = qubitron.DensityMatrixSimulator().simulate(circuit)
    assert set(result._final_simulator_state.qubits) == set(qubitron.LineQubit.range(59))
    # _ = result.final_density_matrix hangs (as expected)

    # Validate a trial run and sampling
    result = qubitron.DensityMatrixSimulator().run(circuit, repetitions=1000)
    assert len(result.measurements) == 59
    assert len(result.measurements['q(0)']) == 1000
    assert (result.measurements['q(0)'] == np.full(1000, 1)).all()


def test_separated_states_str_does_not_merge():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.measure(q0), qubitron.measure(q1), qubitron.X(q0))

    result = qubitron.DensityMatrixSimulator().simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (qubitron.LineQubit(0),)
final density matrix:
[[0.+0.j 0.+0.j]
 [0.+0.j 1.+0.j]]

qubits: (qubitron.LineQubit(1),)
final density matrix:
[[1.+0.j 0.+0.j]
 [0.+0.j 0.+0.j]]

phase:
final density matrix:
[[1.+0.j]]"""
    )


def test_unseparated_states_str():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.measure(q0), qubitron.measure(q1), qubitron.X(q0))

    result = qubitron.DensityMatrixSimulator(split_untangled_states=False).simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (qubitron.LineQubit(0), qubitron.LineQubit(1))
final density matrix:
[[0.+0.j 0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 1.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j 0.+0.j]]"""
    )


def test_sweep_unparameterized_prefix_not_repeated_even_non_unitaries():
    q = qubitron.LineQubit(0)

    class NonUnitaryOp(qubitron.Operation):
        count = 0

        def _act_on_(self, sim_state):
            self.count += 1
            return True

        def with_qubits(self, qubits):
            pass

        @property
        def qubits(self):
            return (q,)

    simulator = qubitron.DensityMatrixSimulator()
    params = [qubitron.ParamResolver({'a': 0}), qubitron.ParamResolver({'a': 1})]

    op1 = NonUnitaryOp()
    op2 = NonUnitaryOp()
    circuit = qubitron.Circuit(op1, qubitron.XPowGate(exponent=sympy.Symbol('a'))(q), op2)
    simulator.simulate_sweep(program=circuit, params=params)
    assert op1.count == 1
    assert op2.count == 2
