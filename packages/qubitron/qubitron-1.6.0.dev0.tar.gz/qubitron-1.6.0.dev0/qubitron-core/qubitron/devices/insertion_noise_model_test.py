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
from qubitron.devices.noise_utils import OpIdentifier, PHYSICAL_GATE_TAG


def test_insertion_noise() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    op_id0 = OpIdentifier(qubitron.XPowGate, q0)
    op_id1 = OpIdentifier(qubitron.ZPowGate, q1)
    model = InsertionNoiseModel(
        {op_id0: qubitron.T(q0), op_id1: qubitron.H(q1)}, require_physical_tag=False
    )
    assert not model.prepend

    moment_0 = qubitron.Moment(qubitron.X(q0), qubitron.X(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        moment_0,
        qubitron.Moment(qubitron.T(q0)),
    ]

    moment_1 = qubitron.Moment(qubitron.Z(q0), qubitron.Z(q1))
    assert model.noisy_moment(moment_1, system_qubits=[q0, q1]) == [
        moment_1,
        qubitron.Moment(qubitron.H(q1)),
    ]

    moment_2 = qubitron.Moment(qubitron.X(q0), qubitron.Z(q1))
    assert model.noisy_moment(moment_2, system_qubits=[q0, q1]) == [
        moment_2,
        qubitron.Moment(qubitron.T(q0), qubitron.H(q1)),
    ]

    moment_3 = qubitron.Moment(qubitron.Z(q0), qubitron.X(q1))
    assert model.noisy_moment(moment_3, system_qubits=[q0, q1]) == [moment_3]

    qubitron.testing.assert_equivalent_repr(model)


def test_colliding_noise_qubits() -> None:
    # Check that noise affecting other qubits doesn't cause issues.
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    op_id0 = OpIdentifier(qubitron.CZPowGate)
    model = InsertionNoiseModel({op_id0: qubitron.CNOT(q1, q2)}, require_physical_tag=False)

    moment_0 = qubitron.Moment(qubitron.CZ(q0, q1), qubitron.CZ(q2, q3))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1, q2, q3]) == [
        moment_0,
        qubitron.Moment(qubitron.CNOT(q1, q2)),
        qubitron.Moment(qubitron.CNOT(q1, q2)),
    ]

    qubitron.testing.assert_equivalent_repr(model)


def test_prepend() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    op_id0 = OpIdentifier(qubitron.XPowGate, q0)
    op_id1 = OpIdentifier(qubitron.ZPowGate, q1)
    model = InsertionNoiseModel(
        {op_id0: qubitron.T(q0), op_id1: qubitron.H(q1)}, prepend=True, require_physical_tag=False
    )

    moment_0 = qubitron.Moment(qubitron.X(q0), qubitron.Z(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        qubitron.Moment(qubitron.T(q0), qubitron.H(q1)),
        moment_0,
    ]


def test_require_physical_tag() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    op_id0 = OpIdentifier(qubitron.XPowGate, q0)
    op_id1 = OpIdentifier(qubitron.ZPowGate, q1)
    model = InsertionNoiseModel({op_id0: qubitron.T(q0), op_id1: qubitron.H(q1)})
    assert model.require_physical_tag

    moment_0 = qubitron.Moment(qubitron.X(q0).with_tags(PHYSICAL_GATE_TAG), qubitron.Z(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        moment_0,
        qubitron.Moment(qubitron.T(q0)),
    ]


def test_supertype_matching() -> None:
    # Demonstrate that the model applies the closest matching type
    # if multiple types match a given gate.
    q0 = qubitron.LineQubit(0)
    op_id0 = OpIdentifier(qubitron.Gate, q0)
    op_id1 = OpIdentifier(qubitron.XPowGate, q0)
    model = InsertionNoiseModel(
        {op_id0: qubitron.T(q0), op_id1: qubitron.S(q0)}, require_physical_tag=False
    )

    moment_0 = qubitron.Moment(qubitron.Rx(rads=1).on(q0))
    assert model.noisy_moment(moment_0, system_qubits=[q0]) == [moment_0, qubitron.Moment(qubitron.S(q0))]

    moment_1 = qubitron.Moment(qubitron.Y(q0))
    assert model.noisy_moment(moment_1, system_qubits=[q0]) == [moment_1, qubitron.Moment(qubitron.T(q0))]

    qubitron.testing.assert_equivalent_repr(model)
