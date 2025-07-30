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

from typing import Sequence

import numpy as np
import pytest

import qubitron


def test_single_qubit_readout_result_repr():
    result = qubitron.experiments.SingleQubitReadoutCalibrationResult(
        zero_state_errors={qubitron.LineQubit(0): 0.1},
        one_state_errors={qubitron.LineQubit(0): 0.2},
        repetitions=1000,
        timestamp=0.3,
    )
    qubitron.testing.assert_equivalent_repr(result)


class NoisySingleQubitReadoutSampler(qubitron.Sampler):
    def __init__(self, p0: float, p1: float, seed: qubitron.RANDOM_STATE_OR_SEED_LIKE = None):
        """Sampler that flips some bits upon readout.

        Args:
            p0: Probability of flipping a 0 to a 1.
            p1: Probability of flipping a 1 to a 0.
            seed: A seed for the pseudorandom number generator.
        """
        self.p0 = p0
        self.p1 = p1
        self.prng = qubitron.value.parse_random_state(seed)
        self.simulator = qubitron.Simulator(seed=self.prng, split_untangled_states=False)

    def run_sweep(
        self, program: qubitron.AbstractCircuit, params: qubitron.Sweepable, repetitions: int = 1
    ) -> Sequence[qubitron.Result]:
        results = self.simulator.run_sweep(program, params, repetitions)
        for result in results:
            for bits in result.measurements.values():
                rand_num = self.prng.uniform(size=bits.shape)
                should_flip = np.logical_or(
                    np.logical_and(bits == 0, rand_num < self.p0),
                    np.logical_and(bits == 1, rand_num < self.p1),
                )
                bits[should_flip] ^= 1
        return results


def test_estimate_single_qubit_readout_errors_no_noise():
    qubits = qubitron.LineQubit.range(10)
    sampler = qubitron.Simulator()
    repetitions = 1000
    result = qubitron.estimate_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions
    )
    assert result.zero_state_errors == {q: 0 for q in qubits}
    assert result.one_state_errors == {q: 0 for q in qubits}
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)


def test_estimate_single_qubit_readout_errors_with_noise():
    qubits = qubitron.LineQubit.range(5)
    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.2, seed=1234)
    repetitions = 1000
    result = qubitron.estimate_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions
    )
    for error in result.zero_state_errors.values():
        assert 0.08 < error < 0.12
    for error in result.one_state_errors.values():
        assert 0.18 < error < 0.22
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)


def test_estimate_parallel_readout_errors_no_noise():
    qubits = [qubitron.GridQubit(i, 0) for i in range(10)]
    sampler = qubitron.Simulator()
    repetitions = 1000
    result = qubitron.estimate_parallel_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions
    )
    assert result.zero_state_errors == {q: 0 for q in qubits}
    assert result.one_state_errors == {q: 0 for q in qubits}
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)
    _ = result.plot_integrated_histogram()
    _, _ = result.plot_heatmap()


def test_estimate_parallel_readout_errors_all_zeros():
    qubits = qubitron.LineQubit.range(10)
    sampler = qubitron.ZerosSampler()
    repetitions = 1000
    result = qubitron.estimate_parallel_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions
    )
    assert result.zero_state_errors == {q: 0 for q in qubits}
    assert result.one_state_errors == {q: 1 for q in qubits}
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)


def test_estimate_parallel_readout_errors_bad_bit_string():
    qubits = qubitron.LineQubit.range(4)
    with pytest.raises(ValueError, match='but was None'):
        _ = qubitron.estimate_parallel_single_qubit_readout_errors(
            qubitron.ZerosSampler(),
            qubits=qubits,
            repetitions=1000,
            trials=35,
            trials_per_batch=10,
            bit_strings=[[1] * 4],
        )
    with pytest.raises(ValueError, match='0 or 1'):
        _ = qubitron.estimate_parallel_single_qubit_readout_errors(
            qubitron.ZerosSampler(),
            qubits=qubits,
            repetitions=1000,
            trials=2,
            bit_strings=np.array([[12, 47, 2, -4], [0.1, 7, 0, 0]]),
        )


def test_estimate_parallel_readout_errors_zero_reps():
    qubits = qubitron.LineQubit.range(10)
    with pytest.raises(ValueError, match='non-zero repetition'):
        _ = qubitron.estimate_parallel_single_qubit_readout_errors(
            qubitron.ZerosSampler(), qubits=qubits, repetitions=0, trials=35, trials_per_batch=10
        )


def test_estimate_parallel_readout_errors_zero_trials():
    qubits = qubitron.LineQubit.range(10)
    with pytest.raises(ValueError, match='non-zero trials'):
        _ = qubitron.estimate_parallel_single_qubit_readout_errors(
            qubitron.ZerosSampler(), qubits=qubits, repetitions=1000, trials=0, trials_per_batch=10
        )


def test_estimate_parallel_readout_errors_zero_batch():
    qubits = qubitron.LineQubit.range(10)
    with pytest.raises(ValueError, match='non-zero trials_per_batch'):
        _ = qubitron.estimate_parallel_single_qubit_readout_errors(
            qubitron.ZerosSampler(), qubits=qubits, repetitions=1000, trials=10, trials_per_batch=0
        )


def test_estimate_parallel_readout_errors_batching():
    qubits = qubitron.LineQubit.range(5)
    sampler = qubitron.ZerosSampler()
    repetitions = 1000
    result = qubitron.estimate_parallel_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions, trials=35, trials_per_batch=10
    )
    assert result.zero_state_errors == {q: 0.0 for q in qubits}
    assert result.one_state_errors == {q: 1.0 for q in qubits}
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)


def test_estimate_parallel_readout_errors_with_noise():
    qubits = qubitron.LineQubit.range(5)
    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.2, seed=1234)
    repetitions = 1000
    result = qubitron.estimate_parallel_single_qubit_readout_errors(
        sampler, qubits=qubits, repetitions=repetitions, trials=40
    )
    for error in result.one_state_errors.values():
        assert 0.17 < error < 0.23
    for error in result.zero_state_errors.values():
        assert 0.07 < error < 0.13
    assert result.repetitions == repetitions
    assert isinstance(result.timestamp, float)


def test_estimate_parallel_readout_errors_missing_qubits():
    qubits = qubitron.LineQubit.range(4)

    result = qubitron.estimate_parallel_single_qubit_readout_errors(
        qubitron.ZerosSampler(),
        qubits=qubits,
        repetitions=2000,
        trials=1,
        bit_strings=np.array([[0] * 4]),
    )
    assert result.zero_state_errors == {q: 0 for q in qubits}
    # Trial did not include a one-state
    assert all(np.isnan(result.one_state_errors[q]) for q in qubits)
    assert result.repetitions == 2000
    assert isinstance(result.timestamp, float)
