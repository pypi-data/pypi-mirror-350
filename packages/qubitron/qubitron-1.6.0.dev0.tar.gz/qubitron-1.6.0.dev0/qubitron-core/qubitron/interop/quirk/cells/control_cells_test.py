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

import qubitron
from qubitron.interop.quirk.cells.testing import assert_url_to_circuit_returns


def test_controls() -> None:
    a, b = qubitron.LineQubit.range(2)

    assert_url_to_circuit_returns('{"cols":[["•","X"]]}', qubitron.Circuit(qubitron.X(b).controlled_by(a)))
    assert_url_to_circuit_returns(
        '{"cols":[["◦","X"]]}', qubitron.Circuit(qubitron.X(a), qubitron.X(b).controlled_by(a), qubitron.X(a))
    )

    assert_url_to_circuit_returns(
        '{"cols":[["⊕","X"]]}',
        qubitron.Circuit(qubitron.Y(a) ** 0.5, qubitron.X(b).controlled_by(a), qubitron.Y(a) ** -0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": -0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
        ],
    )
    assert_url_to_circuit_returns(
        '{"cols":[["⊖","X"]]}',
        qubitron.Circuit(qubitron.Y(a) ** -0.5, qubitron.X(b).controlled_by(a), qubitron.Y(a) ** +0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": -0.5, "i": 0},
        ],
    )

    assert_url_to_circuit_returns(
        '{"cols":[["⊗","X"]]}',
        qubitron.Circuit(qubitron.X(a) ** -0.5, qubitron.X(b).controlled_by(a), qubitron.X(a) ** +0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0, "i": -0.5},
            {"r": 0.5, "i": 0},
            {"r": 0, "i": 0.5},
        ],
    )
    assert_url_to_circuit_returns(
        '{"cols":[["(/)","X"]]}',
        qubitron.Circuit(qubitron.X(a) ** +0.5, qubitron.X(b).controlled_by(a), qubitron.X(a) ** -0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0, "i": 0.5},
            {"r": 0.5, "i": 0},
            {"r": 0, "i": -0.5},
        ],
    )

    qs = qubitron.LineQubit.range(8)
    assert_url_to_circuit_returns(
        '{"cols":[["X","•","◦","⊕","⊖","⊗","(/)","Z"]]}',
        qubitron.Circuit(
            qubitron.X(qs[2]),
            qubitron.Y(qs[3]) ** 0.5,
            qubitron.Y(qs[4]) ** -0.5,
            qubitron.X(qs[5]) ** -0.5,
            qubitron.X(qs[6]) ** 0.5,
            qubitron.X(qs[0]).controlled_by(*qs[1:7]),
            qubitron.Z(qs[7]).controlled_by(*qs[1:7]),
            qubitron.X(qs[6]) ** -0.5,
            qubitron.X(qs[5]) ** 0.5,
            qubitron.Y(qs[4]) ** 0.5,
            qubitron.Y(qs[3]) ** -0.5,
            qubitron.X(qs[2]),
        ),
    )


def test_parity_controls() -> None:
    a, b, c, d, e = qubitron.LineQubit.range(5)

    assert_url_to_circuit_returns(
        '{"cols":[["Y","xpar","ypar","zpar","Z"]]}',
        qubitron.Circuit(
            qubitron.Y(b) ** 0.5,
            qubitron.X(c) ** -0.5,
            qubitron.CNOT(c, b),
            qubitron.CNOT(d, b),
            qubitron.Y(a).controlled_by(b),
            qubitron.Z(e).controlled_by(b),
            qubitron.CNOT(d, b),
            qubitron.CNOT(c, b),
            qubitron.X(c) ** 0.5,
            qubitron.Y(b) ** -0.5,
        ),
    )


def test_control_with_line_qubits_mapped_to() -> None:
    a, b = qubitron.LineQubit.range(2)
    a2, b2 = qubitron.NamedQubit.range(2, prefix='q')
    cell = qubitron.interop.quirk.cells.control_cells.ControlCell(a, [qubitron.Y(b) ** 0.5])
    mapped_cell = qubitron.interop.quirk.cells.control_cells.ControlCell(a2, [qubitron.Y(b2) ** 0.5])
    assert cell != mapped_cell
    assert cell.with_line_qubits_mapped_to([a2, b2]) == mapped_cell


def test_parity_control_with_line_qubits_mapped_to() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    a2, b2, c2 = qubitron.NamedQubit.range(3, prefix='q')
    cell = qubitron.interop.quirk.cells.control_cells.ParityControlCell([a, b], [qubitron.Y(c) ** 0.5])
    mapped_cell = qubitron.interop.quirk.cells.control_cells.ParityControlCell(
        [a2, b2], [qubitron.Y(c2) ** 0.5]
    )
    assert cell != mapped_cell
    assert cell.with_line_qubits_mapped_to([a2, b2, c2]) == mapped_cell


def test_repr() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    qubitron.testing.assert_equivalent_repr(
        qubitron.interop.quirk.cells.control_cells.ControlCell(a, [qubitron.Y(b) ** 0.5])
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.interop.quirk.cells.control_cells.ParityControlCell([a, b], [qubitron.Y(c) ** 0.5])
    )
