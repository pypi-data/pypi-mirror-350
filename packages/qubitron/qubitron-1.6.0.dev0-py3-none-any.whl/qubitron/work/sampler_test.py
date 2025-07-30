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

"""Tests for qubitron.Sampler."""

from __future__ import annotations

from typing import Sequence

import duet
import numpy as np
import pandas as pd
import pytest
import sympy

import qubitron


@duet.sync
async def test_run_async() -> None:
    sim = qubitron.Simulator()
    result = await sim.run_async(
        qubitron.Circuit(qubitron.measure(qubitron.GridQubit(0, 0), key='m')), repetitions=10
    )
    np.testing.assert_equal(result.records['m'], np.zeros((10, 1, 1)))


@duet.sync
async def test_run_sweep_async() -> None:
    sim = qubitron.Simulator()
    results = await sim.run_sweep_async(
        qubitron.Circuit(qubitron.measure(qubitron.GridQubit(0, 0), key='m')),
        qubitron.Linspace('foo', 0, 1, 10),
        repetitions=10,
    )
    assert len(results) == 10
    for result in results:
        np.testing.assert_equal(result.records['m'], np.zeros((10, 1, 1)))


@duet.sync
async def test_sampler_async_fail() -> None:
    class FailingSampler(qubitron.Sampler):
        def run_sweep(self, program, params, repetitions: int = 1):
            raise ValueError('test')

    with pytest.raises(ValueError, match='test'):
        await FailingSampler().run_async(qubitron.Circuit(), repetitions=1)

    with pytest.raises(ValueError, match='test'):
        await FailingSampler().run_sweep_async(qubitron.Circuit(), repetitions=1, params=None)


def test_run_sweep_impl() -> None:
    """Test run_sweep implemented in terms of run_sweep_async."""

    class AsyncSampler(qubitron.Sampler):
        async def run_sweep_async(self, program, params, repetitions: int = 1):
            await duet.sleep(0.001)
            return qubitron.Simulator().run_sweep(program, params, repetitions)

    results = AsyncSampler().run_sweep(
        qubitron.Circuit(qubitron.measure(qubitron.GridQubit(0, 0), key='m')),
        qubitron.Linspace('foo', 0, 1, 10),
        repetitions=10,
    )
    assert len(results) == 10
    for result in results:
        np.testing.assert_equal(result.records['m'], np.zeros((10, 1, 1)))


@duet.sync
async def test_run_sweep_async_impl() -> None:
    """Test run_sweep_async implemented in terms of run_sweep."""

    class SyncSampler(qubitron.Sampler):
        def run_sweep(self, program, params, repetitions: int = 1):
            return qubitron.Simulator().run_sweep(program, params, repetitions)

    results = await SyncSampler().run_sweep_async(
        qubitron.Circuit(qubitron.measure(qubitron.GridQubit(0, 0), key='m')),
        qubitron.Linspace('foo', 0, 1, 10),
        repetitions=10,
    )
    assert len(results) == 10
    for result in results:
        np.testing.assert_equal(result.records['m'], np.zeros((10, 1, 1)))


def test_sampler_sample_multiple_params() -> None:
    a, b = qubitron.LineQubit.range(2)
    s = sympy.Symbol('s')
    t = sympy.Symbol('t')
    sampler = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.X(a) ** s, qubitron.X(b) ** t, qubitron.measure(a, b, key='out'))
    results = sampler.sample(
        circuit,
        repetitions=3,
        params=[{'s': 0, 't': 0}, {'s': 0, 't': 1}, {'s': 1, 't': 0}, {'s': 1, 't': 1}],
    )
    pd.testing.assert_frame_equal(
        results,
        pd.DataFrame(
            columns=['s', 't', 'out'],
            index=[0, 1, 2] * 4,
            data=[
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 1],
                [0, 1, 1],
                [0, 1, 1],
                [1, 0, 2],
                [1, 0, 2],
                [1, 0, 2],
                [1, 1, 3],
                [1, 1, 3],
                [1, 1, 3],
            ],
        ),
    )


def test_sampler_sample_sweep() -> None:
    a = qubitron.LineQubit(0)
    t = sympy.Symbol('t')
    sampler = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.X(a) ** t, qubitron.measure(a, key='out'))
    results = sampler.sample(circuit, repetitions=3, params=qubitron.Linspace('t', 0, 2, 3))
    pd.testing.assert_frame_equal(
        results,
        pd.DataFrame(
            columns=['t', 'out'],
            index=[0, 1, 2] * 3,
            data=[
                [0.0, 0],
                [0.0, 0],
                [0.0, 0],
                [1.0, 1],
                [1.0, 1],
                [1.0, 1],
                [2.0, 0],
                [2.0, 0],
                [2.0, 0],
            ],
        ),
    )


def test_sampler_sample_no_params() -> None:
    a, b = qubitron.LineQubit.range(2)
    sampler = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.X(a), qubitron.measure(a, b, key='out'))
    results = sampler.sample(circuit, repetitions=3)
    pd.testing.assert_frame_equal(
        results, pd.DataFrame(columns=['out'], index=[0, 1, 2], data=[[2], [2], [2]])
    )


def test_sampler_sample_inconsistent_keys() -> None:
    q = qubitron.LineQubit(0)
    sampler = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.measure(q, key='out'))
    with pytest.raises(ValueError, match='Inconsistent sweep parameters'):
        _ = sampler.sample(circuit, params=[{'a': 1}, {'a': 1, 'b': 2}])


@duet.sync
async def test_sampler_async_not_run_inline() -> None:
    ran = False

    class S(qubitron.Sampler):
        def run_sweep(self, *args, **kwargs):
            nonlocal ran
            ran = True
            return []

    a = S().run_sweep_async(qubitron.Circuit(), params=None)
    assert not ran
    assert await a == []
    assert ran


def test_sampler_run_batch() -> None:
    sampler = qubitron.ZerosSampler()
    a = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.X(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    circuit2 = qubitron.Circuit(qubitron.Y(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    params1 = qubitron.Points('t', [0.3, 0.7])
    params2 = qubitron.Points('t', [0.4, 0.6])
    results = sampler.run_batch(
        [circuit1, circuit2], params_list=[params1, params2], repetitions=[1, 2]
    )
    assert len(results) == 2
    for result, param in zip(results[0], [0.3, 0.7]):
        assert result.repetitions == 1
        assert result.params.param_dict == {'t': param}
        assert result.measurements == {'m': np.array([[0]], dtype='uint8')}
    for result, param in zip(results[1], [0.4, 0.6]):
        assert result.repetitions == 2
        assert result.params.param_dict == {'t': param}
        assert len(result.measurements) == 1
        assert np.array_equal(result.measurements['m'], np.array([[0], [0]], dtype='uint8'))


@duet.sync
async def test_run_batch_async_calls_run_sweep_asynchronously() -> None:
    """Test run_batch_async calls run_sweep_async without waiting."""
    finished = []
    a = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.X(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    circuit2 = qubitron.Circuit(qubitron.Y(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    params1 = qubitron.Points('t', [0.3, 0.7])
    params2 = qubitron.Points('t', [0.4, 0.6])
    params_list = [params1, params2]

    class AsyncSampler(qubitron.Sampler):
        async def run_sweep_async(
            self, program, params, repetitions: int = 1, unused: duet.Limiter = duet.Limiter(None)
        ):
            if params == params1:
                await duet.sleep(0.001)

            finished.append(params)

    await AsyncSampler().run_batch_async(
        [circuit1, circuit2], params_list=params_list, repetitions=[1, 2]
    )

    assert finished == list(reversed(params_list))


def test_sampler_run_batch_default_params_and_repetitions() -> None:
    sampler = qubitron.ZerosSampler()
    a = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.X(a), qubitron.measure(a, key='m'))
    circuit2 = qubitron.Circuit(qubitron.Y(a), qubitron.measure(a, key='m'))
    results = sampler.run_batch([circuit1, circuit2])
    assert len(results) == 2
    for result_list in results:
        assert len(result_list) == 1
        result = result_list[0]
        assert result.repetitions == 1
        assert result.params.param_dict == {}
        assert result.measurements == {'m': np.array([[0]], dtype='uint8')}


def test_sampler_run_batch_bad_input_lengths() -> None:
    sampler = qubitron.ZerosSampler()
    a = qubitron.LineQubit(0)
    circuit1 = qubitron.Circuit(qubitron.X(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    circuit2 = qubitron.Circuit(qubitron.Y(a) ** sympy.Symbol('t'), qubitron.measure(a, key='m'))
    params1 = qubitron.Points('t', [0.3, 0.7])
    params2 = qubitron.Points('t', [0.4, 0.6])
    with pytest.raises(ValueError, match='2 and 1'):
        _ = sampler.run_batch([circuit1, circuit2], params_list=[params1])
    with pytest.raises(ValueError, match='2 and 3'):
        _ = sampler.run_batch(
            [circuit1, circuit2], params_list=[params1, params2], repetitions=[1, 2, 3]
        )


def test_sampler_simple_sample_expectation_values() -> None:
    a = qubitron.LineQubit(0)
    sampler = qubitron.Simulator()
    circuit = qubitron.Circuit(qubitron.H(a))
    obs = qubitron.X(a)
    results = sampler.sample_expectation_values(circuit, [obs], num_samples=1000)

    assert np.allclose(results, [[1]])


def test_sampler_sample_expectation_values_calculation() -> None:
    class DeterministicImbalancedStateSampler(qubitron.Sampler):
        """A simple, deterministic mock sampler.
        Pretends to sample from a state vector with a 3:1 balance between the
        probabilities of the |0) and |1) state.
        """

        def run_sweep(
            self, program: qubitron.AbstractCircuit, params: qubitron.Sweepable, repetitions: int = 1
        ) -> Sequence[qubitron.Result]:
            results = np.zeros((repetitions, 1), dtype=bool)
            for idx in range(repetitions // 4):
                results[idx][0] = 1
            return [
                qubitron.ResultDict(params=pr, measurements={'z': results})
                for pr in qubitron.study.to_resolvers(params)
            ]

    a = qubitron.LineQubit(0)
    sampler = DeterministicImbalancedStateSampler()
    # This circuit is not actually sampled, but the mock sampler above gives
    # a reasonable approximation of it.
    circuit = qubitron.Circuit(qubitron.X(a) ** (1 / 3))
    obs = qubitron.Z(a)
    results = sampler.sample_expectation_values(circuit, [obs], num_samples=1000)

    # (0.75 * 1) + (0.25 * -1) = 0.5
    assert np.allclose(results, [[0.5]])


def test_sampler_sample_expectation_values_multi_param() -> None:
    a = qubitron.LineQubit(0)
    t = sympy.Symbol('t')
    sampler = qubitron.Simulator(seed=1)
    circuit = qubitron.Circuit(qubitron.X(a) ** t)
    obs = qubitron.Z(a)
    results = sampler.sample_expectation_values(
        circuit, [obs], num_samples=5, params=qubitron.Linspace('t', 0, 2, 3)
    )

    assert np.allclose(results, [[1], [-1], [1]])


def test_sampler_sample_expectation_values_complex_param() -> None:
    a = qubitron.LineQubit(0)
    t = sympy.Symbol('t')
    sampler = qubitron.Simulator(seed=1)
    circuit = qubitron.Circuit(qubitron.global_phase_operation(t))
    obs = qubitron.Z(a)
    results = sampler.sample_expectation_values(
        circuit,
        [obs],
        num_samples=5,
        params=qubitron.Points('t', [1, 1j, (1 + 1j) / np.sqrt(2)]),  # type: ignore[list-item]
    )

    assert np.allclose(results, [[1], [1], [1]])


def test_sampler_sample_expectation_values_multi_qubit() -> None:
    q = qubitron.LineQubit.range(3)
    sampler = qubitron.Simulator(seed=1)
    circuit = qubitron.Circuit(qubitron.X(q[0]), qubitron.X(q[1]), qubitron.X(q[2]))
    obs = qubitron.Z(q[0]) + qubitron.Z(q[1]) + qubitron.Z(q[2])
    results = sampler.sample_expectation_values(circuit, [obs], num_samples=5)

    assert np.allclose(results, [[-3]])


def test_sampler_sample_expectation_values_composite() -> None:
    # Tests multi-{param,qubit} sampling together in one circuit.
    q = qubitron.LineQubit.range(3)
    t = [sympy.Symbol(f't{x}') for x in range(3)]

    sampler = qubitron.Simulator(seed=1)
    circuit = qubitron.Circuit(qubitron.X(q[0]) ** t[0], qubitron.X(q[1]) ** t[1], qubitron.X(q[2]) ** t[2])

    obs = [qubitron.Z(q[x]) for x in range(3)]
    # t0 is in the inner loop to make bit-ordering easier below.
    params = ([{'t0': t0, 't1': t1, 't2': t2} for t2 in [0, 1] for t1 in [0, 1] for t0 in [0, 1]],)
    results = sampler.sample_expectation_values(circuit, obs, num_samples=5, params=params)

    assert len(results) == 8
    assert np.allclose(
        results,
        [
            [+1, +1, +1],
            [-1, +1, +1],
            [+1, -1, +1],
            [-1, -1, +1],
            [+1, +1, -1],
            [-1, +1, -1],
            [+1, -1, -1],
            [-1, -1, -1],
        ],
    )


def test_sampler_simple_sample_expectation_requirements() -> None:
    a = qubitron.LineQubit(0)
    sampler = qubitron.Simulator(seed=1)
    circuit = qubitron.Circuit(qubitron.H(a))
    obs = qubitron.X(a)
    with pytest.raises(ValueError, match='at least one sample'):
        _ = sampler.sample_expectation_values(circuit, [obs], num_samples=0)

    with pytest.raises(ValueError, match='At least one observable'):
        _ = sampler.sample_expectation_values(circuit, [], num_samples=1)

    circuit.append(qubitron.measure(a, key='out'))
    with pytest.raises(ValueError, match='permit_terminal_measurements'):
        _ = sampler.sample_expectation_values(circuit, [obs], num_samples=1)
