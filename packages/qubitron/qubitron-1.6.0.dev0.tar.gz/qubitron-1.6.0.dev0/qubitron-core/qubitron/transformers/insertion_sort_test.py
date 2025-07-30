# Copyright 2024 The Qubitron Developers
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
import qubitron.transformers


def test_insertion_sort() -> None:
    c = qubitron.Circuit(
        qubitron.CZ(qubitron.q(2), qubitron.q(1)),
        qubitron.CZ(qubitron.q(2), qubitron.q(4)),
        qubitron.CZ(qubitron.q(0), qubitron.q(1)),
        qubitron.CZ(qubitron.q(2), qubitron.q(1)),
        qubitron.GlobalPhaseGate(1j).on(),
    )
    sorted_circuit = qubitron.transformers.insertion_sort_transformer(c)
    assert sorted_circuit == qubitron.Circuit(
        qubitron.GlobalPhaseGate(1j).on(),
        qubitron.CZ(qubitron.q(0), qubitron.q(1)),
        qubitron.CZ(qubitron.q(2), qubitron.q(1)),
        qubitron.CZ(qubitron.q(2), qubitron.q(1)),
        qubitron.CZ(qubitron.q(2), qubitron.q(4)),
    )
