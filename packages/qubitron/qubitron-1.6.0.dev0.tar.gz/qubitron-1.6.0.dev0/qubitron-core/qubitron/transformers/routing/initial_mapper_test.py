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


def test_hardcoded_initial_mapper():
    input_map = {qubitron.NamedQubit(str(i)): qubitron.NamedQubit(str(-i)) for i in range(1, 6)}
    circuit = qubitron.Circuit([qubitron.H(qubitron.NamedQubit(str(i))) for i in range(1, 6)])
    initial_mapper = qubitron.HardCodedInitialMapper(input_map)

    assert input_map == initial_mapper.initial_mapping(circuit)
    assert str(initial_mapper) == f'qubitron.HardCodedInitialMapper({input_map})'
    qubitron.testing.assert_equivalent_repr(initial_mapper)

    circuit.append(qubitron.H(qubitron.NamedQubit(str(6))))
    with pytest.raises(
        ValueError, match="The qubits in circuit must be a subset of the keys in the mapping"
    ):
        initial_mapper.initial_mapping(circuit)
