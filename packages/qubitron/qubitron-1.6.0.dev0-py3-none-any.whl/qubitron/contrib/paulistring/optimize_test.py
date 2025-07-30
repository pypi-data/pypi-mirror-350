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
from qubitron.contrib.paulistring import optimized_circuit


def test_optimize() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)
    c_orig = qubitron.Circuit(
        qubitron.X(q0) ** 0.5,
        qubitron.X(q1),
        qubitron.CZ(q1, q2),
        qubitron.X(q2) ** 0.125,
        qubitron.Z(q1) ** 0.5,
        qubitron.Y(q1) ** 0.5,
        qubitron.CZ(q0, q1),
        qubitron.Z(q1) ** 0.5,
        qubitron.CZ(q1, q2),
        qubitron.Z(q1) ** 0.5,
        qubitron.X(q2) ** 0.875,
        qubitron.CZ(q1, q2),
        qubitron.X(q2) ** 0.125,
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        """
0: ───X^0.5─────────────────────────@───────────────────────────────────
                                    │
1: ───X───────@───S─────────Y^0.5───@───S───@───S─────────@─────────────
              │                             │             │
2: ───────────@───X^(1/8)───────────────────@───X^(7/8)───@───X^(1/8)───
""",
    )

    c_opt = optimized_circuit(c_orig)

    qubitron.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    qubitron.testing.assert_has_diagram(
        c_opt,
        """
0: ───X^0.5────────────@────────────────────────────────────────
                       │
1: ───@───────X^-0.5───@───@────────────────@───Z^-0.5──────────
      │                    │                │
2: ───@────────────────────@───[X]^(-7/8)───@───[X]^-0.25───Z───
""",
    )


def test_optimize_large_circuit() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)
    c_orig = qubitron.testing.nonoptimal_toffoli_circuit(q0, q1, q2)

    c_opt = optimized_circuit(c_orig)

    qubitron.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    assert (
        sum(
            1
            for op in c_opt.all_operations()
            if isinstance(op, qubitron.GateOperation) and isinstance(op.gate, qubitron.CZPowGate)
        )
        == 10
    )


def test_repeat_limit() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)
    c_orig = qubitron.testing.nonoptimal_toffoli_circuit(q0, q1, q2)

    c_opt = optimized_circuit(c_orig, repeat=1)

    qubitron.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    assert (
        sum(
            1
            for op in c_opt.all_operations()
            if isinstance(op, qubitron.GateOperation) and isinstance(op.gate, qubitron.CZPowGate)
        )
        >= 10
    )
