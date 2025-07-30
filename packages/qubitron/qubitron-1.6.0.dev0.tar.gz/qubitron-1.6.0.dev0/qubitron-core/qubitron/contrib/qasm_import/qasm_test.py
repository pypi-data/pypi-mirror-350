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

import numpy as np

import qubitron
import qubitron.testing as ct
from qubitron.contrib.qasm_import import circuit_from_qasm
from qubitron.testing import consistent_qasm as cq


def test_consistency_with_qasm_output_and_qiskit():
    qubits = [qubitron.NamedQubit(f'q_{i}') for i in range(4)]
    a, b, c, d = qubits
    circuit1 = qubitron.Circuit(
        qubitron.rx(np.pi / 2).on(a),
        qubitron.ry(np.pi / 2).on(b),
        qubitron.rz(np.pi / 2).on(b),
        qubitron.X.on(a),
        qubitron.Y.on(b),
        qubitron.Z.on(c),
        qubitron.H.on(d),
        qubitron.S.on(a),
        qubitron.T.on(b),
        qubitron.S.on(c) ** -1,
        qubitron.T.on(d) ** -1,
        qubitron.X.on(d) ** 0.125,
        qubitron.TOFFOLI.on(a, b, c),
        qubitron.CSWAP.on(d, a, b),
        qubitron.SWAP.on(c, d),
        qubitron.CX.on(a, b),
        qubitron.ControlledGate(qubitron.Y).on(c, d),
        qubitron.CZ.on(a, b),
        qubitron.ControlledGate(qubitron.H).on(b, c),
        qubitron.IdentityGate(1).on(c),
        qubitron.circuits.qasm_output.QasmUGate(1.0, 2.0, 3.0).on(d),
    )

    qasm = qubitron.qasm(circuit1)

    circuit2 = circuit_from_qasm(qasm)

    qubitron_unitary = qubitron.unitary(circuit2)
    ct.assert_allclose_up_to_global_phase(qubitron_unitary, qubitron.unitary(circuit1), atol=1e-8)

    cq.assert_qiskit_parsed_qasm_consistent_with_unitary(qasm, qubitron_unitary)
