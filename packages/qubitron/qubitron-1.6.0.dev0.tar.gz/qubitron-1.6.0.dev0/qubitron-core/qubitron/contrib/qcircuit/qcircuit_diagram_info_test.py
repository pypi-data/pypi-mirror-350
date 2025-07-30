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
import qubitron.contrib.qcircuit as ccq


def test_get_qcircuit_diagram_info():
    qubits = qubitron.NamedQubit('x'), qubitron.NamedQubit('y')

    gate = qubitron.SwapPowGate(exponent=0.5)
    op = gate(*qubits)
    qubit_map = {q: i for i, q in enumerate(qubits)}
    args = qubitron.CircuitDiagramInfoArgs(
        known_qubits=qubits,
        known_qubit_count=None,
        use_unicode_characters=True,
        precision=3,
        label_map=qubit_map,
    )
    actual_info = ccq.get_qcircuit_diagram_info(op, args)
    name = r'{\text{SWAP}^{0.5}}'
    expected_info = qubitron.CircuitDiagramInfo(
        (r'\multigate{1}' + name, r'\ghost' + name), exponent=1, connected=False
    )
    assert actual_info == expected_info

    gate = qubitron.SWAP
    op = gate(*qubits)
    qubit_map = {q: i for q, i in zip(qubits, (4, 3))}
    args = qubitron.CircuitDiagramInfoArgs(
        known_qubits=qubits,
        known_qubit_count=None,
        use_unicode_characters=True,
        precision=3,
        label_map=qubit_map,
    )
    actual_info = ccq.get_qcircuit_diagram_info(op, args)
    expected_info = qubitron.CircuitDiagramInfo(
        (r'\ghost{\text{SWAP}}', r'\multigate{1}{\text{SWAP}}'), connected=False
    )
    assert actual_info == expected_info

    qubit_map = {q: i for q, i in zip(qubits, (2, 5))}
    args = qubitron.CircuitDiagramInfoArgs(
        known_qubits=qubits,
        known_qubit_count=None,
        use_unicode_characters=True,
        precision=3,
        label_map=qubit_map,
    )
    actual_info = ccq.get_qcircuit_diagram_info(op, args)
    expected_info = qubitron.CircuitDiagramInfo((r'\gate{\text{Swap}}',) * 2)
    assert actual_info == expected_info

    actual_info = ccq.get_qcircuit_diagram_info(op, qubitron.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT)
    assert actual_info == expected_info
