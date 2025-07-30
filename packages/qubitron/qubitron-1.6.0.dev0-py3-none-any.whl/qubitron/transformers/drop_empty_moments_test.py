# Copyright 2022 The Qubitron Developers
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


def test_drop() -> None:
    q1 = qubitron.NamedQubit('q1')
    q2 = qubitron.NamedQubit('q2')
    qubitron.testing.assert_same_circuits(
        qubitron.drop_empty_moments(
            qubitron.Circuit(
                qubitron.Moment(), qubitron.Moment(), qubitron.Moment([qubitron.CNOT(q1, q2)]), qubitron.Moment()
            )
        ),
        qubitron.Circuit(qubitron.Moment([qubitron.CNOT(q1, q2)])),
    )


def test_drop_empty_moments() -> None:
    q1, q2 = qubitron.LineQubit.range(2)
    c_nested = qubitron.FrozenCircuit(
        qubitron.Moment(), qubitron.Moment(), qubitron.Moment([qubitron.CNOT(q1, q2)]), qubitron.Moment()
    )
    c_nested_dropped = qubitron.FrozenCircuit(qubitron.CNOT(q1, q2))
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
        c_nested,
    )
    c_expected = qubitron.Circuit(
        c_nested_dropped,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested_dropped,
        qubitron.CircuitOperation(c_nested_dropped).repeat(5).with_tags("preserve_tag"),
        c_nested_dropped,
    )
    context = qubitron.TransformerContext(tags_to_ignore=("nocompile",), deep=True)
    qubitron.testing.assert_same_circuits(qubitron.drop_empty_moments(c_orig, context=context), c_expected)
