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
"""This module defines building blocks for parsing Quirk circuits."""

from qubitron.interop.quirk.cells.all_cells import (
    generate_all_quirk_cell_makers as generate_all_quirk_cell_makers,
)

from qubitron.interop.quirk.cells.cell import (
    Cell as Cell,
    CellMaker as CellMaker,
    CellMakerArgs as CellMakerArgs,
    ExplicitOperationsCell as ExplicitOperationsCell,
)

from qubitron.interop.quirk.cells.composite_cell import CompositeCell as CompositeCell

from qubitron.interop.quirk.cells.qubit_permutation_cells import (
    QuirkQubitPermutationGate as QuirkQubitPermutationGate,
)

from qubitron.interop.quirk.cells.arithmetic_cells import QuirkArithmeticGate as QuirkArithmeticGate

from qubitron.interop.quirk.cells.input_rotation_cells import (
    QuirkInputRotationOperation as QuirkInputRotationOperation,
)

import qubitron.interop.quirk.cells.swap_cell
import qubitron.interop.quirk.cells.control_cells
