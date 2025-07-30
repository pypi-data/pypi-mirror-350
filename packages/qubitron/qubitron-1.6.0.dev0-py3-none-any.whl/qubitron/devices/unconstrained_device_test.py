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

import qubitron


def test_repr():
    qubitron.testing.assert_equivalent_repr(qubitron.UNCONSTRAINED_DEVICE)


def test_infinitely_fast():
    assert qubitron.UNCONSTRAINED_DEVICE.duration_of(qubitron.X(qubitron.NamedQubit('a'))) == qubitron.Duration(
        picos=0
    )


def test_any_qubit_works():
    moment = qubitron.Moment([qubitron.X(qubitron.LineQubit(987654321))])
    qubitron.UNCONSTRAINED_DEVICE.validate_moment(moment)
    qubitron.UNCONSTRAINED_DEVICE.validate_circuit(qubitron.Circuit(moment))
