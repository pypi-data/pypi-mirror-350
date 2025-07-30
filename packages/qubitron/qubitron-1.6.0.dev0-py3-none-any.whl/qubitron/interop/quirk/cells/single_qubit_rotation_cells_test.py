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

import sympy

import qubitron
from qubitron.interop.quirk.cells.testing import assert_url_to_circuit_returns


def test_fixed_single_qubit_rotations() -> None:
    a, b, c, d = qubitron.LineQubit.range(4)

    assert_url_to_circuit_returns(
        '{"cols":[["H","X","Y","Z"]]}', qubitron.Circuit(qubitron.H(a), qubitron.X(b), qubitron.Y(c), qubitron.Z(d))
    )

    assert_url_to_circuit_returns(
        '{"cols":[["X^½","X^⅓","X^¼"],'
        '["X^⅛","X^⅟₁₆","X^⅟₃₂"],'
        '["X^-½","X^-⅓","X^-¼"],'
        '["X^-⅛","X^-⅟₁₆","X^-⅟₃₂"]]}',
        qubitron.Circuit(
            qubitron.X(a) ** (1 / 2),
            qubitron.X(b) ** (1 / 3),
            qubitron.X(c) ** (1 / 4),
            qubitron.X(a) ** (1 / 8),
            qubitron.X(b) ** (1 / 16),
            qubitron.X(c) ** (1 / 32),
            qubitron.X(a) ** (-1 / 2),
            qubitron.X(b) ** (-1 / 3),
            qubitron.X(c) ** (-1 / 4),
            qubitron.X(a) ** (-1 / 8),
            qubitron.X(b) ** (-1 / 16),
            qubitron.X(c) ** (-1 / 32),
        ),
    )

    assert_url_to_circuit_returns(
        '{"cols":[["Y^½","Y^⅓","Y^¼"],'
        '["Y^⅛","Y^⅟₁₆","Y^⅟₃₂"],'
        '["Y^-½","Y^-⅓","Y^-¼"],'
        '["Y^-⅛","Y^-⅟₁₆","Y^-⅟₃₂"]]}',
        qubitron.Circuit(
            qubitron.Y(a) ** (1 / 2),
            qubitron.Y(b) ** (1 / 3),
            qubitron.Y(c) ** (1 / 4),
            qubitron.Y(a) ** (1 / 8),
            qubitron.Y(b) ** (1 / 16),
            qubitron.Y(c) ** (1 / 32),
            qubitron.Y(a) ** (-1 / 2),
            qubitron.Y(b) ** (-1 / 3),
            qubitron.Y(c) ** (-1 / 4),
            qubitron.Y(a) ** (-1 / 8),
            qubitron.Y(b) ** (-1 / 16),
            qubitron.Y(c) ** (-1 / 32),
        ),
    )

    assert_url_to_circuit_returns(
        '{"cols":[["Z^½","Z^⅓","Z^¼"],'
        '["Z^⅛","Z^⅟₁₆","Z^⅟₃₂"],'
        '["Z^⅟₆₄","Z^⅟₁₂₈"],'
        '["Z^-½","Z^-⅓","Z^-¼"],'
        '["Z^-⅛","Z^-⅟₁₆"]]}',
        qubitron.Circuit(
            qubitron.Z(a) ** (1 / 2),
            qubitron.Z(b) ** (1 / 3),
            qubitron.Z(c) ** (1 / 4),
            qubitron.Z(a) ** (1 / 8),
            qubitron.Z(b) ** (1 / 16),
            qubitron.Z(c) ** (1 / 32),
            qubitron.Z(a) ** (1 / 64),
            qubitron.Z(b) ** (1 / 128),
            qubitron.Moment([qubitron.Z(a) ** (-1 / 2), qubitron.Z(b) ** (-1 / 3), qubitron.Z(c) ** (-1 / 4)]),
            qubitron.Z(a) ** (-1 / 8),
            qubitron.Z(b) ** (-1 / 16),
        ),
    )


def test_dynamic_single_qubit_rotations() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    t = sympy.Symbol('t')

    # Dynamic single qubit rotations.
    assert_url_to_circuit_returns(
        '{"cols":[["X^t","Y^t","Z^t"],["X^-t","Y^-t","Z^-t"]]}',
        qubitron.Circuit(
            qubitron.X(a) ** t,
            qubitron.Y(b) ** t,
            qubitron.Z(c) ** t,
            qubitron.X(a) ** -t,
            qubitron.Y(b) ** -t,
            qubitron.Z(c) ** -t,
        ),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["e^iXt","e^iYt","e^iZt"],["e^-iXt","e^-iYt","e^-iZt"]]}',
        qubitron.Circuit(
            qubitron.rx(2 * sympy.pi * t).on(a),
            qubitron.ry(2 * sympy.pi * t).on(b),
            qubitron.rz(2 * sympy.pi * t).on(c),
            qubitron.rx(2 * sympy.pi * -t).on(a),
            qubitron.ry(2 * sympy.pi * -t).on(b),
            qubitron.rz(2 * sympy.pi * -t).on(c),
        ),
    )


def test_formulaic_gates() -> None:
    a, b = qubitron.LineQubit.range(2)
    t = sympy.Symbol('t')

    assert_url_to_circuit_returns(
        '{"cols":[["X^ft",{"id":"X^ft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.X(a) ** sympy.sin(sympy.pi * t), qubitron.X(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Y^ft",{"id":"Y^ft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.Y(a) ** sympy.sin(sympy.pi * t), qubitron.Y(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Z^ft",{"id":"Z^ft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.Z(a) ** sympy.sin(sympy.pi * t), qubitron.Z(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Rxft",{"id":"Rxft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.rx(sympy.pi * t * t).on(a), qubitron.rx(t * t).on(b)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Ryft",{"id":"Ryft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.ry(sympy.pi * t * t).on(a), qubitron.ry(t * t).on(b)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Rzft",{"id":"Rzft","arg":"t*t"}]]}',
        qubitron.Circuit(qubitron.rz(sympy.pi * t * t).on(a), qubitron.rz(t * t).on(b)),
    )
