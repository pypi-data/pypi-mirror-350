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
from qubitron.devices.noise_utils import OpIdentifier


def test_op_identifier():
    op_id = OpIdentifier(qubitron.XPowGate)
    assert qubitron.X(qubitron.LineQubit(1)) in op_id
    assert qubitron.Rx(rads=1) in op_id


def test_op_identifier_subtypes():
    gate_id = OpIdentifier(qubitron.Gate)
    xpow_id = OpIdentifier(qubitron.XPowGate)
    x_on_q0_id = OpIdentifier(qubitron.XPowGate, qubitron.LineQubit(0))
    assert xpow_id.is_proper_subtype_of(gate_id)
    assert x_on_q0_id.is_proper_subtype_of(xpow_id)
    assert x_on_q0_id.is_proper_subtype_of(gate_id)
    assert not xpow_id.is_proper_subtype_of(xpow_id)


def test_op_id_str():
    op_id = OpIdentifier(qubitron.XPowGate, qubitron.LineQubit(0))
    assert str(op_id) == "<class 'qubitron.ops.common_gates.XPowGate'>(qubitron.LineQubit(0),)"
    assert repr(op_id) == (
        "qubitron.devices.noise_utils.OpIdentifier(qubitron.ops.common_gates.XPowGate, qubitron.LineQubit(0))"
    )


def test_op_id_swap():
    q0, q1 = qubitron.LineQubit.range(2)
    base_id = OpIdentifier(qubitron.CZPowGate, q0, q1)
    swap_id = OpIdentifier(base_id.gate_type, *base_id.qubits[::-1])
    assert qubitron.CZ(q0, q1) in base_id
    assert qubitron.CZ(q0, q1) not in swap_id
    assert qubitron.CZ(q1, q0) not in base_id
    assert qubitron.CZ(q1, q0) in swap_id


def test_op_id_instance():
    q0 = qubitron.LineQubit.range(1)[0]
    gate = qubitron.SingleQubitCliffordGate.from_xz_map((qubitron.X, False), (qubitron.Z, False))
    op_id = OpIdentifier(gate, q0)
    qubitron.testing.assert_equivalent_repr(op_id)
