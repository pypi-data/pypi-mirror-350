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

import pytest

import qubitron


def test_routed_circuit_with_mapping_simple() -> None:
    q = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit([qubitron.Moment(qubitron.SWAP(q[0], q[1]).with_tags(qubitron.RoutingSwapTag()))])
    expected_diagram = """
0: ───q(0)───×[<r>]───q(1)───
      │      │        │
1: ───q(1)───×────────q(0)───"""
    qubitron.testing.assert_has_diagram(qubitron.routed_circuit_with_mapping(circuit), expected_diagram)

    expected_diagram_with_initial_mapping = """
0: ───a───×[<r>]───b───
      │   │        │
1: ───b───×────────a───"""
    qubitron.testing.assert_has_diagram(
        qubitron.routed_circuit_with_mapping(
            circuit, {qubitron.NamedQubit("a"): q[0], qubitron.NamedQubit("b"): q[1]}
        ),
        expected_diagram_with_initial_mapping,
    )

    # if swap is untagged should not affect the mapping
    circuit = qubitron.Circuit([qubitron.Moment(qubitron.SWAP(q[0], q[1]))])
    expected_diagram = """
0: ───q(0)───×───
      │      │
1: ───q(1)───×───"""
    qubitron.testing.assert_has_diagram(qubitron.routed_circuit_with_mapping(circuit), expected_diagram)

    circuit = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.X(q[0]).with_tags(qubitron.RoutingSwapTag())),
            qubitron.Moment(qubitron.SWAP(q[0], q[1])),
        ]
    )
    with pytest.raises(
        ValueError, match="Invalid circuit. A non-SWAP gate cannot be tagged a RoutingSwapTag."
    ):
        qubitron.routed_circuit_with_mapping(circuit)


def test_routed_circuit_with_mapping_multi_swaps() -> None:
    q = qubitron.LineQubit.range(6)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.CNOT(q[3], q[4])),
            qubitron.Moment(qubitron.CNOT(q[5], q[4]), qubitron.CNOT(q[2], q[3])),
            qubitron.Moment(
                qubitron.CNOT(q[2], q[1]), qubitron.SWAP(q[4], q[3]).with_tags(qubitron.RoutingSwapTag())
            ),
            qubitron.Moment(
                qubitron.SWAP(q[0], q[1]).with_tags(qubitron.RoutingSwapTag()),
                qubitron.SWAP(q[3], q[2]).with_tags(qubitron.RoutingSwapTag()),
            ),
            qubitron.Moment(qubitron.CNOT(q[2], q[1])),
            qubitron.Moment(qubitron.CNOT(q[1], q[0])),
        ]
    )
    expected_diagram = """
0: ───q(0)────────────────────q(0)───×[<r>]───q(1)───────X───
      │                       │      │        │          │
1: ───q(1)───────────X────────q(1)───×────────q(0)───X───@───
      │              │        │               │      │
2: ───q(2)───────@───@────────q(2)───×────────q(4)───@───────
      │          │            │      │        │
3: ───q(3)───@───X───×────────q(4)───×[<r>]───q(2)───────────
      │      │       │        │               │
4: ───q(4)───X───X───×[<r>]───q(3)────────────q(3)───────────
      │          │            │               │
5: ───q(5)───────@────────────q(5)────────────q(5)───────────
"""
    qubitron.testing.assert_has_diagram(qubitron.routed_circuit_with_mapping(circuit), expected_diagram)
