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

import pytest

import qubitron
from qubitron import quirk_url_to_circuit
from qubitron.interop.quirk.cells.testing import assert_url_to_circuit_returns


def test_swap() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    assert_url_to_circuit_returns('{"cols":[["Swap","Swap"]]}', qubitron.Circuit(qubitron.SWAP(a, b)))
    assert_url_to_circuit_returns(
        '{"cols":[["Swap","X","Swap"]]}', qubitron.Circuit(qubitron.SWAP(a, c), qubitron.X(b))
    )

    with pytest.raises(ValueError, match='number of swap gates'):
        _ = quirk_url_to_circuit('https://algassert.com/quirk#circuit={"cols":[["Swap"]]}')
    with pytest.raises(ValueError, match='number of swap gates'):
        _ = quirk_url_to_circuit(
            'https://algassert.com/quirk#circuit={"cols":[["Swap","Swap","Swap"]]}'
        )


def test_controlled_swap() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    assert_url_to_circuit_returns(
        '{"cols":[["Swap","•","Swap"]]}', qubitron.Circuit(qubitron.SWAP(a, c).controlled_by(b))
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Swap","•","Swap","•"]]}', qubitron.Circuit(qubitron.SWAP(a, c).controlled_by(b, d))
    )


def test_with_line_qubits_mapped_to() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    a2, b2, c2, d2 = qubitron.NamedQubit.range(4, prefix='q')
    cell = qubitron.interop.quirk.cells.swap_cell.SwapCell(qubits=[a, b], controls=[c, d])
    mapped_cell = qubitron.interop.quirk.cells.swap_cell.SwapCell(qubits=[a2, b2], controls=[c2, d2])
    assert cell != mapped_cell
    assert cell.with_line_qubits_mapped_to([a2, b2, c2, d2]) == mapped_cell


def test_repr() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)
    qubitron.testing.assert_equivalent_repr(
        qubitron.interop.quirk.cells.swap_cell.SwapCell(qubits=[a, b], controls=[c, d])
    )
