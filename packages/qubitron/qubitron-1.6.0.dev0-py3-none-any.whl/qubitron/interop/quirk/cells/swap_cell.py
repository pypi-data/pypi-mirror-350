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

from typing import Any, Iterable, Iterator, TYPE_CHECKING

from qubitron import ops, value
from qubitron.interop.quirk.cells.cell import Cell, CellMaker

if TYPE_CHECKING:
    import qubitron


@value.value_equality(unhashable=True)
class SwapCell(Cell):
    def __init__(self, qubits: Iterable[qubitron.Qid], controls: Iterable[qubitron.Qid]):
        self._qubits = list(qubits)
        self._controls = list(controls)

    def gate_count(self) -> int:
        return 1

    def with_line_qubits_mapped_to(self, qubits: list[qubitron.Qid]) -> Cell:
        return SwapCell(
            qubits=Cell._replace_qubits(self._qubits, qubits),
            controls=Cell._replace_qubits(self._controls, qubits),
        )

    def modify_column(self, column: list[Cell | None]):
        # Swallow other swap cells.
        for i in range(len(column)):
            gate = column[i]
            if gate is not self and isinstance(gate, SwapCell):
                assert self._controls == gate._controls
                self._qubits += gate._qubits
                column[i] = None

    def operations(self) -> qubitron.OP_TREE:
        if len(self._qubits) != 2:
            raise ValueError('Wrong number of swap gates in a column.')
        return ops.SWAP(*self._qubits).controlled_by(*self._controls)

    def controlled_by(self, qubit: qubitron.Qid):
        return SwapCell(self._qubits, self._controls + [qubit])

    def _value_equality_values_(self) -> Any:
        return self._qubits, self._controls

    def __repr__(self) -> str:
        return (
            f'qubitron.interop.quirk.cells.swap_cell.SwapCell('
            f'\n    {self._qubits!r},'
            f'\n    {self._controls!r})'
        )


def generate_all_swap_cell_makers() -> Iterator[CellMaker]:
    yield CellMaker("Swap", 1, lambda args: SwapCell(args.qubits, []))
