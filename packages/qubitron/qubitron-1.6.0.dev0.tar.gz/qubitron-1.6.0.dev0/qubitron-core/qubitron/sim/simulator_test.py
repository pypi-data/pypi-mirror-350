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

"""Tests for simulator.py"""

from __future__ import annotations

import abc
from typing import Any, Generic, Sequence
from unittest import mock

import duet
import numpy as np
import pytest

import qubitron
from qubitron import study
from qubitron.sim.simulation_state import TSimulationState
from qubitron.sim.simulator import (
    SimulatesAmplitudes,
    SimulatesExpectationValues,
    SimulatesFinalState,
    SimulatesIntermediateState,
    SimulatesSamples,
    SimulationTrialResult,
    TStepResult,
)


class FakeSimulatesSamples(SimulatesSamples):
    """A SimulatesSamples that returns specified values from _run."""

    def __init__(self, run_output: dict[str, np.ndarray]):
        self._run_output = run_output

    def _run(self, *args, **kwargs) -> dict[str, np.ndarray]:
        return self._run_output


class FakeStepResult(qubitron.StepResult):
    def __init__(self, *, ones_qubits=None, final_state=None):
        self._ones_qubits = set(ones_qubits or [])
        self._final_state = final_state

    def _simulator_state(self):
        return self._final_state  # pragma: no cover

    def state_vector(self):
        pass

    def __setstate__(self, state):
        pass

    def sample(self, qubits, repetitions=1, seed=None):
        return np.array([[qubit in self._ones_qubits for qubit in qubits]] * repetitions)


class SimulatesIntermediateStateImpl(
    Generic[TStepResult, TSimulationState],
    SimulatesIntermediateState[TStepResult, SimulationTrialResult, TSimulationState],
    metaclass=abc.ABCMeta,
):
    """A SimulatesIntermediateState that uses the default SimulationTrialResult type."""

    def _create_simulator_trial_result(
        self,
        params: study.ParamResolver,
        measurements: dict[str, np.ndarray],
        final_simulator_state: qubitron.SimulationStateBase[TSimulationState],
    ) -> SimulationTrialResult:
        """This method creates a default trial result.

        Args:
            params: The ParamResolver for this trial.
            measurements: The measurement results for this trial.
            final_simulator_state: The final state of the simulation.

        Returns:
            The SimulationTrialResult.
        """
        return SimulationTrialResult(
            params=params, measurements=measurements, final_simulator_state=final_simulator_state
        )


def test_run_simulator_run():
    expected_records = {'a': np.array([[[1]]])}
    simulator = FakeSimulatesSamples(expected_records)
    circuit = qubitron.Circuit(qubitron.measure(qubitron.LineQubit(0), key='k'))
    param_resolver = qubitron.ParamResolver({})
    expected_result = qubitron.ResultDict(records=expected_records, params=param_resolver)
    assert expected_result == simulator.run(
        program=circuit, repetitions=10, param_resolver=param_resolver
    )


def test_run_simulator_sweeps():
    expected_records = {'a': np.array([[[1]]])}
    simulator = FakeSimulatesSamples(expected_records)
    circuit = qubitron.Circuit(qubitron.measure(qubitron.LineQubit(0), key='k'))
    param_resolvers = [qubitron.ParamResolver({}), qubitron.ParamResolver({})]
    expected_results = [
        qubitron.ResultDict(records=expected_records, params=param_resolvers[0]),
        qubitron.ResultDict(records=expected_records, params=param_resolvers[1]),
    ]
    assert expected_results == simulator.run_sweep(
        program=circuit, repetitions=10, params=param_resolvers
    )


@mock.patch.multiple(
    SimulatesIntermediateStateImpl, __abstractmethods__=set(), simulate_moment_steps=mock.Mock()
)
def test_intermediate_simulator():
    simulator = SimulatesIntermediateStateImpl()

    final_simulator_state = np.array([1, 0, 0, 0])

    def steps(*args, **kwargs):
        result = mock.Mock()
        result.measurements = {'a': [True, True]}
        yield result
        result = mock.Mock()
        result.measurements = {'b': [True, False]}
        result._simulator_state.return_value = final_simulator_state
        yield result

    simulator.simulate_moment_steps.side_effect = steps
    circuit = mock.Mock(qubitron.Circuit)
    param_resolver = qubitron.ParamResolver({})
    qubit_order = mock.Mock(qubitron.QubitOrder)
    result = simulator.simulate(
        program=circuit, param_resolver=param_resolver, qubit_order=qubit_order, initial_state=2
    )
    np.testing.assert_equal(result.measurements['a'], [True, True])
    np.testing.assert_equal(result.measurements['b'], [True, False])
    assert set(result.measurements.keys()) == {'a', 'b'}
    assert result.params == param_resolver
    np.testing.assert_equal(result._final_simulator_state, final_simulator_state)


@mock.patch.multiple(
    SimulatesIntermediateStateImpl, __abstractmethods__=set(), simulate_moment_steps=mock.Mock()
)
def test_intermediate_sweeps():
    simulator = SimulatesIntermediateStateImpl()

    final_state = np.array([1, 0, 0, 0])

    def steps(*args, **kwargs):
        result = mock.Mock()
        result.measurements = {'a': np.array([True, True])}
        result._simulator_state.return_value = final_state
        yield result

    simulator.simulate_moment_steps.side_effect = steps
    circuit = mock.Mock(qubitron.Circuit)
    param_resolvers = [qubitron.ParamResolver({}), qubitron.ParamResolver({})]
    qubit_order = mock.Mock(qubitron.QubitOrder)
    results = simulator.simulate_sweep(
        program=circuit, params=param_resolvers, qubit_order=qubit_order, initial_state=2
    )

    expected_results = [
        qubitron.SimulationTrialResult(
            measurements={'a': np.array([True, True])},
            params=param_resolvers[0],
            final_simulator_state=final_state,
        ),
        qubitron.SimulationTrialResult(
            measurements={'a': np.array([True, True])},
            params=param_resolvers[1],
            final_simulator_state=final_state,
        ),
    ]
    assert results == expected_results


def test_step_sample_measurement_ops():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    measurement_ops = [qubitron.measure(q0, q1), qubitron.measure(q2)]
    step_result = FakeStepResult(ones_qubits=[q1])

    measurements = step_result.sample_measurement_ops(measurement_ops)
    np.testing.assert_equal(measurements, {'q(0),q(1)': [[False, True]], 'q(2)': [[False]]})


def test_step_sample_measurement_ops_repetitions():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    measurement_ops = [qubitron.measure(q0, q1), qubitron.measure(q2)]
    step_result = FakeStepResult(ones_qubits=[q1])

    measurements = step_result.sample_measurement_ops(measurement_ops, repetitions=3)
    np.testing.assert_equal(measurements, {'q(0),q(1)': [[False, True]] * 3, 'q(2)': [[False]] * 3})


def test_step_sample_measurement_ops_invert_mask():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    measurement_ops = [
        qubitron.measure(q0, q1, invert_mask=(True,)),
        qubitron.measure(q2, invert_mask=(False,)),
    ]
    step_result = FakeStepResult(ones_qubits=[q1])

    measurements = step_result.sample_measurement_ops(measurement_ops)
    np.testing.assert_equal(measurements, {'q(0),q(1)': [[True, True]], 'q(2)': [[False]]})


def test_step_sample_measurement_ops_confusion_map():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    cmap_01 = {(0, 1): np.array([[0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0]])}
    cmap_2 = {(0,): np.array([[0, 1], [1, 0]])}
    measurement_ops = [
        qubitron.measure(q0, q1, confusion_map=cmap_01),
        qubitron.measure(q2, confusion_map=cmap_2),
    ]
    step_result = FakeStepResult(ones_qubits=[q2])

    measurements = step_result.sample_measurement_ops(measurement_ops)
    np.testing.assert_equal(measurements, {'q(0),q(1)': [[False, True]], 'q(2)': [[False]]})


def test_step_sample_measurement_ops_no_measurements():
    step_result = FakeStepResult(ones_qubits=[])

    measurements = step_result.sample_measurement_ops([])
    assert measurements == {}


def test_step_sample_measurement_ops_not_measurement():
    q0 = qubitron.LineQubit(0)
    step_result = FakeStepResult(ones_qubits=[q0])
    with pytest.raises(ValueError, match='MeasurementGate'):
        step_result.sample_measurement_ops([qubitron.X(q0)])


def test_step_sample_measurement_ops_repeated_qubit():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    step_result = FakeStepResult(ones_qubits=[q0])
    with pytest.raises(ValueError, match=r'Measurement key q\(0\) repeated'):
        step_result.sample_measurement_ops(
            [qubitron.measure(q0), qubitron.measure(q1, q2), qubitron.measure(q0)]
        )


def test_simulation_trial_result_equality():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({}), measurements={}, final_simulator_state=()
        ),
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({}), measurements={}, final_simulator_state=()
        ),
    )
    eq.add_equality_group(
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({'s': 1}), measurements={}, final_simulator_state=()
        )
    )
    eq.add_equality_group(
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({'s': 1}),
            measurements={'m': np.array([1])},
            final_simulator_state=(),
        )
    )
    eq.add_equality_group(
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({'s': 1}),
            measurements={'m': np.array([1])},
            final_simulator_state=(0, 1),
        )
    )


def test_simulation_trial_result_repr():
    assert repr(
        qubitron.SimulationTrialResult(
            params=qubitron.ParamResolver({'s': 1}),
            measurements={'m': np.array([1])},
            final_simulator_state=(0, 1),
        )
    ) == (
        "qubitron.SimulationTrialResult("
        "params=qubitron.ParamResolver({'s': 1}), "
        "measurements={'m': array([1])}, "
        "final_simulator_state=(0, 1))"
    )


def test_simulation_trial_result_str():
    assert (
        str(
            qubitron.SimulationTrialResult(
                params=qubitron.ParamResolver({'s': 1}), measurements={}, final_simulator_state=(0, 1)
            )
        )
        == '(no measurements)'
    )

    assert (
        str(
            qubitron.SimulationTrialResult(
                params=qubitron.ParamResolver({'s': 1}),
                measurements={'m': np.array([1])},
                final_simulator_state=(0, 1),
            )
        )
        == 'm=1'
    )

    assert (
        str(
            qubitron.SimulationTrialResult(
                params=qubitron.ParamResolver({'s': 1}),
                measurements={'m': np.array([1, 2, 3])},
                final_simulator_state=(0, 1),
            )
        )
        == 'm=123'
    )

    assert (
        str(
            qubitron.SimulationTrialResult(
                params=qubitron.ParamResolver({'s': 1}),
                measurements={'m': np.array([9, 10, 11])},
                final_simulator_state=(0, 1),
            )
        )
        == 'm=9 10 11'
    )


def test_pretty_print():
    result = qubitron.SimulationTrialResult(qubitron.ParamResolver(), {}, np.array([1]))

    # Test Jupyter console output from
    class FakePrinter:
        def __init__(self):
            self.text_pretty = ''

        def text(self, to_print):
            self.text_pretty += to_print

    p = FakePrinter()
    result._repr_pretty_(p, False)
    assert p.text_pretty == '(no measurements)'

    # Test cycle handling
    p = FakePrinter()
    result._repr_pretty_(p, True)
    assert p.text_pretty == 'SimulationTrialResult(...)'


@duet.sync
async def test_async_sample():
    m = {'mock': np.array([[[0]], [[1]]])}
    simulator = FakeSimulatesSamples(m)

    q = qubitron.LineQubit(0)
    f = simulator.run_async(qubitron.Circuit(qubitron.measure(q)), repetitions=10)
    result = await f
    np.testing.assert_equal(result.records, m)


def test_simulation_trial_result_qubit_map():
    q = qubitron.LineQubit.range(2)
    result = qubitron.Simulator().simulate(qubitron.Circuit([qubitron.CZ(q[0], q[1])]))
    assert result.qubit_map == {q[0]: 0, q[1]: 1}

    result = qubitron.DensityMatrixSimulator().simulate(qubitron.Circuit([qubitron.CZ(q[0], q[1])]))
    assert result.qubit_map == {q[0]: 0, q[1]: 1}


def test_sample_repeated_measurement_keys():
    q = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit()
    circuit.append(
        [
            qubitron.measure(q[0], key='a'),
            qubitron.measure(q[1], key='a'),
            qubitron.measure(q[0], key='b'),
            qubitron.measure(q[1], key='b'),
        ]
    )
    result = qubitron.sample(circuit)
    assert len(result.records['a']) == 1
    assert len(result.records['b']) == 1
    assert len(result.records['a'][0]) == 2
    assert len(result.records['b'][0]) == 2


def test_classical_controls_go_to_suffix_if_corresponding_measurement_does():
    subcircuit = qubitron.CircuitOperation(qubitron.FrozenCircuit()).with_classical_controls('a')
    m = qubitron.measure(qubitron.LineQubit(0), key='a')
    circuit = qubitron.Circuit(m, subcircuit)
    prefix, suffix = qubitron.sim.simulator.split_into_matching_protocol_then_general(
        circuit, lambda op: op != m  # any op but m goes into prefix
    )
    assert not prefix
    assert suffix == circuit


def test_simulate_with_invert_mask():
    q0, q1, q2, q3, q4 = qubitron.LineQid.for_qid_shape((2, 3, 3, 3, 4))
    c = qubitron.Circuit(
        qubitron.XPowGate(dimension=2)(q0),
        qubitron.XPowGate(dimension=3)(q2),
        qubitron.XPowGate(dimension=3)(q3) ** 2,
        qubitron.XPowGate(dimension=4)(q4) ** 3,
        qubitron.measure(q0, q1, q2, q3, q4, key='a', invert_mask=(True,) * 4),
    )
    assert np.all(qubitron.Simulator().run(c).measurements['a'] == [[0, 1, 0, 2, 3]])


def test_monte_carlo_on_unknown_channel():
    class Reset11To00(qubitron.Gate):
        def num_qubits(self) -> int:
            return 2

        def _kraus_(self):
            return [
                np.eye(4) - qubitron.one_hot(index=(3, 3), shape=(4, 4), dtype=np.complex64),
                qubitron.one_hot(index=(0, 3), shape=(4, 4), dtype=np.complex64),
            ]

    for k in range(4):
        out = qubitron.Simulator().simulate(
            qubitron.Circuit(Reset11To00().on(*qubitron.LineQubit.range(2))), initial_state=k
        )
        np.testing.assert_allclose(
            out.state_vector(), qubitron.one_hot(index=k % 3, shape=4, dtype=np.complex64), atol=1e-8
        )


def test_iter_definitions():
    mock_trial_result = SimulationTrialResult(params={}, measurements={}, final_simulator_state=[])

    class FakeNonIterSimulatorImpl(
        SimulatesAmplitudes, SimulatesExpectationValues, SimulatesFinalState
    ):
        """A class which defines the non-Iterator simulator API methods.

        After v0.12, simulators are expected to implement the *_iter methods.
        """

        def compute_amplitudes_sweep(
            self,
            program: qubitron.AbstractCircuit,
            bitstrings: Sequence[int],
            params: study.Sweepable,
            qubit_order: qubitron.QubitOrderOrList = qubitron.QubitOrder.DEFAULT,
        ) -> Sequence[Sequence[complex]]:
            return [[1.0]]

        def simulate_expectation_values_sweep(
            self,
            program: qubitron.AbstractCircuit,
            observables: qubitron.PauliSumLike | list[qubitron.PauliSumLike],
            params: study.Sweepable,
            qubit_order: qubitron.QubitOrderOrList = qubitron.QubitOrder.DEFAULT,
            initial_state: Any = None,
            permit_terminal_measurements: bool = False,
        ) -> list[list[float]]:
            return [[1.0]]

        def simulate_sweep(
            self,
            program: qubitron.AbstractCircuit,
            params: study.Sweepable,
            qubit_order: qubitron.QubitOrderOrList = qubitron.QubitOrder.DEFAULT,
            initial_state: Any = None,
        ) -> list[SimulationTrialResult]:
            return [mock_trial_result]

    non_iter_sim = FakeNonIterSimulatorImpl()
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.X(q0))
    bitstrings = [0b0]
    params = {}
    assert non_iter_sim.compute_amplitudes_sweep(circuit, bitstrings, params) == [[1.0]]
    amp_iter = non_iter_sim.compute_amplitudes_sweep_iter(circuit, bitstrings, params)
    assert next(amp_iter) == [1.0]

    obs = qubitron.X(q0)
    assert non_iter_sim.simulate_expectation_values_sweep(circuit, obs, params) == [[1.0]]
    ev_iter = non_iter_sim.simulate_expectation_values_sweep_iter(circuit, obs, params)
    assert next(ev_iter) == [1.0]

    assert non_iter_sim.simulate_sweep(circuit, params) == [mock_trial_result]
    state_iter = non_iter_sim.simulate_sweep_iter(circuit, params)
    assert next(state_iter) == mock_trial_result


def test_missing_iter_definitions():
    class FakeMissingIterSimulatorImpl(
        SimulatesAmplitudes, SimulatesExpectationValues, SimulatesFinalState
    ):
        """A class which fails to define simulator methods."""

    missing_iter_sim = FakeMissingIterSimulatorImpl()
    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.X(q0))
    bitstrings = [0b0]
    params = {}
    with pytest.raises(RecursionError):
        missing_iter_sim.compute_amplitudes_sweep(circuit, bitstrings, params)
    with pytest.raises(RecursionError):
        amp_iter = missing_iter_sim.compute_amplitudes_sweep_iter(circuit, bitstrings, params)
        next(amp_iter)

    obs = qubitron.X(q0)
    with pytest.raises(RecursionError):
        missing_iter_sim.simulate_expectation_values_sweep(circuit, obs, params)
    with pytest.raises(RecursionError):
        ev_iter = missing_iter_sim.simulate_expectation_values_sweep_iter(circuit, obs, params)
        next(ev_iter)

    with pytest.raises(RecursionError):
        missing_iter_sim.simulate_sweep(circuit, params)
    with pytest.raises(RecursionError):
        state_iter = missing_iter_sim.simulate_sweep_iter(circuit, params)
        next(state_iter)


def test_trial_result_initializer():
    resolver = qubitron.ParamResolver()
    state = 3
    x = SimulationTrialResult(resolver, {}, state)
    assert x._final_simulator_state == 3
    x = SimulationTrialResult(resolver, {}, final_simulator_state=state)
    assert x._final_simulator_state == 3
