# Copyright 2021 The Qubitron Developers
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

import qubitron
from qubitron.devices.insertion_noise_model import InsertionNoiseModel
from qubitron.devices.noise_properties import NoiseModelFromNoiseProperties, NoiseProperties
from qubitron.devices.noise_utils import OpIdentifier, PHYSICAL_GATE_TAG


# These properties are for testing purposes only - they are not representative
# of device behavior for any existing hardware.
class SampleNoiseProperties(NoiseProperties):
    def __init__(self, system_qubits: list[qubitron.Qid], qubit_pairs: list[tuple[qubitron.Qid, qubitron.Qid]]):
        self.qubits = system_qubits
        self.qubit_pairs = qubit_pairs

    def build_noise_models(self):
        add_h = InsertionNoiseModel({OpIdentifier(qubitron.Gate, q): qubitron.H(q) for q in self.qubits})
        add_iswap = InsertionNoiseModel(
            {OpIdentifier(qubitron.Gate, *qs): qubitron.ISWAP(*qs) for qs in self.qubit_pairs}
        )
        return [add_h, add_iswap]


def test_sample_model() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    props = SampleNoiseProperties([q0, q1], [(q0, q1), (q1, q0)])
    model = NoiseModelFromNoiseProperties(props)
    circuit = qubitron.Circuit(
        qubitron.X(q0), qubitron.CNOT(q0, q1), qubitron.Z(q1), qubitron.measure(q0, q1, key='meas')
    )
    noisy_circuit = circuit.with_noise(model)
    expected_circuit = qubitron.Circuit(
        qubitron.Moment(qubitron.X(q0).with_tags(PHYSICAL_GATE_TAG)),
        qubitron.Moment(qubitron.H(q0)),
        qubitron.Moment(qubitron.CNOT(q0, q1).with_tags(PHYSICAL_GATE_TAG)),
        qubitron.Moment(qubitron.ISWAP(q0, q1)),
        qubitron.Moment(qubitron.Z(q1).with_tags(PHYSICAL_GATE_TAG)),
        qubitron.Moment(qubitron.H(q1)),
        qubitron.Moment(qubitron.measure(q0, q1, key='meas')),
        qubitron.Moment(qubitron.H(q0), qubitron.H(q1)),
    )
    assert noisy_circuit == expected_circuit
