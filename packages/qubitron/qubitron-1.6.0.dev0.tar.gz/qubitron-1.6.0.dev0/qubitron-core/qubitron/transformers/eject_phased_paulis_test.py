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

import dataclasses
from typing import cast, Iterable

import numpy as np
import pytest
import sympy

import qubitron


def assert_optimizes(
    before: qubitron.Circuit,
    expected: qubitron.Circuit,
    compare_unitaries: bool = True,
    eject_parameterized: bool = False,
    *,
    with_context: bool = False,
):
    context = qubitron.TransformerContext(tags_to_ignore=("nocompile",)) if with_context else None
    circuit = qubitron.eject_phased_paulis(
        before, eject_parameterized=eject_parameterized, context=context
    )

    # They should have equivalent effects.
    if compare_unitaries:
        if qubitron.is_parameterized(circuit):
            for a in (0, 0.1, 0.5, -1.0, np.pi, np.pi / 2):
                params: qubitron.ParamDictType = {'x': a, 'y': a / 2, 'z': -2 * a}
                (
                    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                        qubitron.resolve_parameters(circuit, params),
                        qubitron.resolve_parameters(expected, params),
                        1e-8,
                    )
                )
        else:
            (
                qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                    circuit, expected, 1e-8
                )
            )

    # And match the expected circuit.
    qubitron.testing.assert_same_circuits(circuit, expected)

    # And it should be idempotent.
    circuit = qubitron.eject_phased_paulis(
        circuit, eject_parameterized=eject_parameterized, context=context
    )
    qubitron.testing.assert_same_circuits(circuit, expected)

    # Nested sub-circuits should also get optimized.
    q = before.all_qubits()
    c_nested = qubitron.Circuit(
        [qubitron.PhasedXPowGate(phase_exponent=0.5).on_each(*q), (qubitron.Z**0.5).on_each(*q)],
        qubitron.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore"),
        [qubitron.Y.on_each(*q), qubitron.X.on_each(*q)],
        qubitron.CircuitOperation(before.freeze()).repeat(3).with_tags("preserve_tag"),
    )
    c_expected = qubitron.Circuit(
        qubitron.PhasedXPowGate(phase_exponent=0.75).on_each(*q),
        qubitron.Moment(qubitron.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        qubitron.Z.on_each(*q),
        qubitron.Moment(qubitron.CircuitOperation(expected.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    if context is None:
        context = qubitron.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    else:
        context = dataclasses.replace(
            context, tags_to_ignore=context.tags_to_ignore + ("ignore",), deep=True
        )
    c_nested = qubitron.eject_phased_paulis(
        c_nested, context=context, eject_parameterized=eject_parameterized
    )
    qubitron.testing.assert_same_circuits(c_nested, c_expected)
    c_nested = qubitron.eject_phased_paulis(
        c_nested, context=context, eject_parameterized=eject_parameterized
    )
    qubitron.testing.assert_same_circuits(c_nested, c_expected)


def quick_circuit(*moments: Iterable[qubitron.OP_TREE]) -> qubitron.Circuit:
    return qubitron.Circuit(
        [qubitron.Moment(cast(Iterable[qubitron.Operation], qubitron.flatten_op_tree(m))) for m in moments]
    )


def test_absorbs_z() -> None:
    q = qubitron.NamedQubit('q')
    x = sympy.Symbol('x')

    # Full Z.
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)], [qubitron.Z(q)]),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.625).on(q)]),
    )

    # PhasedXZGate
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)],
            [qubitron.PhasedXZGate(x_exponent=0, axis_phase_exponent=0, z_exponent=1).on(q)],
        ),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.625).on(q)]),
    )

    # Partial Z. PhasedXZGate with z_exponent = 0.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXZGate(x_exponent=1, axis_phase_exponent=0.125, z_exponent=0).on(q)],
            [qubitron.S(q)],
        ),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.375).on(q)]),
    )

    # parameterized Z.
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)], [qubitron.Z(q) ** x]),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.125 + x / 2).on(q)]),
        eject_parameterized=True,
    )
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)], [qubitron.Z(q) ** (x + 1)]
        ),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.625 + x / 2).on(q)]),
        eject_parameterized=True,
    )

    # Multiple Zs.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)], [qubitron.S(q)], [qubitron.T(q) ** -1]
        ),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)]),
    )

    # Multiple Parameterized Zs.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)], [qubitron.S(q) ** x], [qubitron.T(q) ** -x]
        ),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.125 + x * 0.125).on(q)]),
        eject_parameterized=True,
    )

    # Parameterized Phase and Partial Z
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=x).on(q)], [qubitron.S(q)]),
        expected=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=x + 0.25).on(q)]),
        eject_parameterized=True,
    )


def test_crosses_czs() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')

    # Full CZ.
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)], [qubitron.CZ(a, b)]),
        expected=quick_circuit(
            [qubitron.Z(b)], [qubitron.CZ(a, b)], [qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)]
        ),
    )
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.125).on(a)], [qubitron.CZ(b, a)]),
        expected=quick_circuit(
            [qubitron.Z(b)], [qubitron.CZ(a, b)], [qubitron.PhasedXPowGate(phase_exponent=0.125).on(a)]
        ),
    )
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=x).on(a)], [qubitron.CZ(b, a)]),
        expected=quick_circuit(
            [qubitron.Z(b)], [qubitron.CZ(a, b)], [qubitron.PhasedXPowGate(phase_exponent=x).on(a)]
        ),
        eject_parameterized=True,
    )

    # Partial CZ.
    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b) ** 0.25]),
        expected=quick_circuit([qubitron.Z(b) ** 0.25], [qubitron.CZ(a, b) ** -0.25], [qubitron.X(a)]),
    )
    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b) ** x]),
        expected=quick_circuit([qubitron.Z(b) ** x], [qubitron.CZ(a, b) ** -x], [qubitron.X(a)]),
        eject_parameterized=True,
    )

    # Double cross.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(a)],
            [qubitron.PhasedXPowGate(phase_exponent=0.375).on(b)],
            [qubitron.CZ(a, b) ** 0.25],
        ),
        expected=quick_circuit(
            [qubitron.CZ(a, b) ** 0.25], [qubitron.Y(b), qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)]
        ),
    )
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=x).on(a)],
            [qubitron.PhasedXPowGate(phase_exponent=y).on(b)],
            [qubitron.CZ(a, b) ** z],
        ),
        expected=quick_circuit(
            [qubitron.CZ(a, b) ** z],
            [
                qubitron.PhasedXPowGate(phase_exponent=y + z / 2).on(b),
                qubitron.PhasedXPowGate(phase_exponent=x + z / 2).on(a),
            ],
        ),
        eject_parameterized=True,
    )


def test_toggles_measurements() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    x = sympy.Symbol('x')

    # Single.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)], [qubitron.measure(a, b)]
        ),
        expected=quick_circuit([qubitron.measure(a, b, invert_mask=(True,))]),
    )
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(b)], [qubitron.measure(a, b)]
        ),
        expected=quick_circuit([qubitron.measure(a, b, invert_mask=(False, True))]),
    )
    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=x).on(b)], [qubitron.measure(a, b)]),
        expected=quick_circuit([qubitron.measure(a, b, invert_mask=(False, True))]),
        eject_parameterized=True,
    )

    # Multiple.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(b)],
            [qubitron.measure(a, b)],
        ),
        expected=quick_circuit([qubitron.measure(a, b, invert_mask=(True, True))]),
    )

    # Xmon.
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)], [qubitron.measure(a, b, key='t')]
        ),
        expected=quick_circuit([qubitron.measure(a, b, invert_mask=(True,), key='t')]),
    )

    # CCOs
    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [qubitron.measure(a, key="m")],
            [qubitron.X(b).with_classical_controls("m")],
        ),
        expected=quick_circuit(
            [qubitron.measure(a, invert_mask=(True,), key="m")],
            [qubitron.X(b).with_classical_controls("m")],
        ),
        compare_unitaries=False,
    )


def test_eject_phased_xz() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.Circuit(
        qubitron.PhasedXZGate(x_exponent=1, z_exponent=0.5, axis_phase_exponent=0.5).on(a),
        qubitron.CZ(a, b) ** 0.25,
    )
    c_expected = qubitron.Circuit(
        qubitron.CZ(a, b) ** -0.25, qubitron.PhasedXPowGate(phase_exponent=0.75).on(a), qubitron.T(b)
    )
    qubitron.testing.assert_same_circuits(
        qubitron.eject_z(qubitron.eject_phased_paulis(qubitron.eject_z(c))), c_expected
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c, c_expected, 1e-8)


def test_cancels_other_full_w() -> None:
    q = qubitron.NamedQubit('q')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ),
        expected=quick_circuit(),
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=x).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=x).on(q)],
        ),
        expected=quick_circuit(),
        eject_parameterized=True,
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=0.125).on(q)],
        ),
        expected=quick_circuit([qubitron.Z(q) ** -0.25]),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.X(q)], [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)]),
        expected=quick_circuit([qubitron.Z(q) ** 0.5]),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.Y(q)], [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)]),
        expected=quick_circuit([qubitron.Z(q) ** -0.5]),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)], [qubitron.X(q)]),
        expected=quick_circuit([qubitron.Z(q) ** -0.5]),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)], [qubitron.Y(q)]),
        expected=quick_circuit([qubitron.Z(q) ** 0.5]),
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=x).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=y).on(q)],
        ),
        expected=quick_circuit([qubitron.Z(q) ** (2 * (y - x))]),
        eject_parameterized=True,
    )


def test_phases_partial_ws() -> None:
    q = qubitron.NamedQubit('q')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')

    assert_optimizes(
        before=quick_circuit(
            [qubitron.X(q)], [qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=0.5).on(q)]
        ),
        expected=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=-0.25, exponent=0.5).on(q)], [qubitron.X(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)], [qubitron.X(q) ** 0.5]),
        expected=quick_circuit(
            [qubitron.Y(q) ** 0.5], [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=0.5, exponent=0.75).on(q)],
        ),
        expected=quick_circuit(
            [qubitron.X(q) ** 0.75], [qubitron.PhasedXPowGate(phase_exponent=0.25).on(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.X(q)], [qubitron.PhasedXPowGate(exponent=-0.25, phase_exponent=0.5).on(q)]
        ),
        expected=quick_circuit(
            [qubitron.PhasedXPowGate(exponent=-0.25, phase_exponent=-0.5).on(q)], [qubitron.X(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=x).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=y, exponent=z).on(q)],
        ),
        expected=quick_circuit(
            [qubitron.PhasedXPowGate(phase_exponent=2 * x - y, exponent=z).on(q)],
            [qubitron.PhasedXPowGate(phase_exponent=x).on(q)],
        ),
        eject_parameterized=True,
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('x'), sympy.Symbol('x') + 1])
def test_blocked_by_unknown_and_symbols(sym) -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.SWAP(a, b)], [qubitron.X(a)]),
        expected=quick_circuit([qubitron.X(a)], [qubitron.SWAP(a, b)], [qubitron.X(a)]),
    )

    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.Z(a) ** sym], [qubitron.X(a)]),
        expected=quick_circuit([qubitron.X(a)], [qubitron.Z(a) ** sym], [qubitron.X(a)]),
        compare_unitaries=False,
    )

    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b) ** sym], [qubitron.X(a)]),
        expected=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b) ** sym], [qubitron.X(a)]),
        compare_unitaries=False,
    )


def test_blocked_by_nocompile_tag() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert_optimizes(
        before=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b).with_tags("nocompile")], [qubitron.X(a)]),
        expected=quick_circuit([qubitron.X(a)], [qubitron.CZ(a, b).with_tags("nocompile")], [qubitron.X(a)]),
        with_context=True,
    )


def test_zero_x_rotation() -> None:
    a = qubitron.NamedQubit('a')

    assert_optimizes(before=quick_circuit([qubitron.rx(0)(a)]), expected=quick_circuit([qubitron.rx(0)(a)]))
