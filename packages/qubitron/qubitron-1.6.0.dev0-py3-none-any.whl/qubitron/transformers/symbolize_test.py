# Copyright 2025 The Qubitron Developers
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
import sympy

import qubitron
from qubitron.transformers.symbolize import SymbolizeTag


def test_symbolize_single_qubit_gates_by_indexed_tags_success():
    q = qubitron.NamedQubit("a")
    input_circuit = qubitron.Circuit(
        qubitron.X(q).with_tags("phxz_1"), qubitron.Y(q).with_tags("tag1"), qubitron.Z(q).with_tags("phxz_0")
    )
    output_circuit = qubitron.symbolize_single_qubit_gates_by_indexed_tags(
        input_circuit, symbolize_tag=SymbolizeTag(prefix="phxz")
    )
    qubitron.testing.assert_same_circuits(
        output_circuit,
        qubitron.Circuit(
            qubitron.PhasedXZGate(
                x_exponent=sympy.Symbol("x1"),
                z_exponent=sympy.Symbol("z1"),
                axis_phase_exponent=sympy.Symbol("a1"),
            ).on(q),
            qubitron.Y(q).with_tags("tag1"),
            qubitron.PhasedXZGate(
                x_exponent=sympy.Symbol("x0"),
                z_exponent=sympy.Symbol("z0"),
                axis_phase_exponent=sympy.Symbol("a0"),
            ).on(q),
        ),
    )


def test_symbolize_single_qubit_gates_by_indexed_tags_multiple_tags():
    q = qubitron.NamedQubit("a")
    input_circuit = qubitron.Circuit(qubitron.X(q).with_tags("TO-PHXZ_0", "TO-PHXZ_2"))

    with pytest.raises(ValueError, match="Multiple tags are prefixed with TO-PHXZ."):
        qubitron.symbolize_single_qubit_gates_by_indexed_tags(input_circuit)


def test_symbolize_tag_invalid_prefix():
    with pytest.raises(ValueError, match="Length of 'prefix' must be >= 1: 0"):
        SymbolizeTag(prefix="")
    with pytest.raises(TypeError, match="'prefix' must be <class 'str'>"):
        SymbolizeTag(prefix=[1])
