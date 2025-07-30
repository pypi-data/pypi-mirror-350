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

import duet

import qubitron


@duet.sync
async def test_pauli_string_sample_collector() -> None:
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliSumCollector(
        circuit=qubitron.Circuit(qubitron.H(a), qubitron.CNOT(a, b), qubitron.X(a), qubitron.Z(b)),
        observable=(1 + 0j) * qubitron.X(a) * qubitron.X(b)
        - 16 * qubitron.Y(a) * qubitron.Y(b)
        + 4 * qubitron.Z(a) * qubitron.Z(b)
        + (1 - 0j),
        samples_per_term=100,
    )
    await p.collect_async(sampler=qubitron.Simulator())
    energy = p.estimated_energy()
    assert isinstance(energy, float) and energy == 12


@duet.sync
async def test_pauli_string_sample_single() -> None:
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliSumCollector(
        circuit=qubitron.Circuit(qubitron.H(a), qubitron.CNOT(a, b), qubitron.X(a), qubitron.Z(b)),
        observable=qubitron.X(a) * qubitron.X(b),
        samples_per_term=100,
    )
    await p.collect_async(sampler=qubitron.Simulator())
    assert p.estimated_energy() == -1


def test_pauli_string_sample_collector_identity() -> None:
    p = qubitron.PauliSumCollector(
        circuit=qubitron.Circuit(), observable=qubitron.PauliSum() + 2j, samples_per_term=100
    )
    p.collect(sampler=qubitron.Simulator())
    assert p.estimated_energy() == 2j


def test_pauli_string_sample_collector_extra_qubit_z() -> None:
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliSumCollector(
        circuit=qubitron.Circuit(qubitron.H(a)), observable=3 * qubitron.Z(b), samples_per_term=100
    )
    p.collect(sampler=qubitron.Simulator())
    assert p.estimated_energy() == 3


def test_pauli_string_sample_collector_extra_qubit_x() -> None:
    a, b = qubitron.LineQubit.range(2)
    p = qubitron.PauliSumCollector(
        circuit=qubitron.Circuit(qubitron.H(a)), observable=3 * qubitron.X(b), samples_per_term=10000
    )
    p.collect(sampler=qubitron.Simulator())
    assert abs(p.estimated_energy()) < 0.5
