# Copyright 2020 The Qubitron Developers
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


def test_run_sweep() -> None:
    a, b, c = [qubitron.NamedQubit(s) for s in ['a', 'b', 'c']]
    circuit = qubitron.Circuit([qubitron.measure(a)], [qubitron.measure(b, c)])
    sampler = qubitron.ZerosSampler()

    result = sampler.run_sweep(circuit, None, 3)

    assert len(result) == 1
    assert result[0].measurements.keys() == {'a', 'b,c'}
    assert result[0].measurements['a'].shape == (3, 1)
    assert np.all(result[0].measurements['a'] == 0)
    assert result[0].measurements['b,c'].shape == (3, 2)
    assert np.all(result[0].measurements['b,c'] == 0)


def test_sample() -> None:
    # Create a circuit whose measurements are always zeros, and check that
    # results of ZeroSampler on this circuit are identical to results of
    # actual simulation.
    qs = qubitron.LineQubit.range(6)
    c = qubitron.Circuit([qubitron.CNOT(qs[0], qs[1]), qubitron.X(qs[2]), qubitron.X(qs[2])])
    c += qubitron.Z(qs[3]) ** sympy.Symbol('p')
    c += [qubitron.measure(q) for q in qs[0:3]]
    c += qubitron.measure(qs[4], qs[5])
    # Z to even power is an identity.
    params = qubitron.Points(sympy.Symbol('p'), [0, 2, 4, 6])

    result1 = qubitron.ZerosSampler().sample(c, repetitions=10, params=params)
    result2 = qubitron.Simulator().sample(c, repetitions=10, params=params)

    assert np.all(result1 == result2)


def test_repeated_keys() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)

    c = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, q2, key='b'),
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, q2, key='b'),
        qubitron.measure(q1, q2, key='b'),
    )
    result = qubitron.ZerosSampler().run(c, repetitions=10)
    assert result.records['a'].shape == (10, 2, 1)
    assert result.records['b'].shape == (10, 3, 2)

    c2 = qubitron.Circuit(qubitron.measure(q0, key='a'), qubitron.measure(q1, q2, key='a'))
    with pytest.raises(ValueError, match="Different qid shapes for repeated measurement"):
        qubitron.ZerosSampler().run(c2, repetitions=10)


class OnlyMeasurementsDevice(qubitron.Device):
    def validate_operation(self, operation: qubitron.Operation) -> None:
        if not qubitron.is_measurement(operation):
            raise ValueError(f'{operation} is not a measurement and this device only measures!')


def test_validate_device() -> None:
    device = OnlyMeasurementsDevice()
    sampler = qubitron.ZerosSampler(device)

    a, b, c = [qubitron.NamedQubit(s) for s in ['a', 'b', 'c']]
    circuit = qubitron.Circuit(qubitron.measure(a), qubitron.measure(b, c))

    _ = sampler.run_sweep(circuit, None, 3)

    circuit = qubitron.Circuit(qubitron.measure(a), qubitron.X(b))
    with pytest.raises(ValueError, match=r'X\(b\) is not a measurement'):
        _ = sampler.run_sweep(circuit, None, 3)
