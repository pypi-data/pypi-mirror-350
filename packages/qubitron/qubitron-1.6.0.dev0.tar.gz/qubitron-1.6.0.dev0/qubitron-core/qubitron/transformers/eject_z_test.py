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

import numpy as np
import pytest
import sympy

import qubitron
from qubitron.transformers.eject_z import _is_swaplike


def assert_optimizes(
    before: qubitron.Circuit,
    expected: qubitron.Circuit,
    eject_parameterized: bool = False,
    *,
    with_context: bool = False,
):
    if qubitron.has_unitary(before):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            before, expected, atol=1e-8
        )
    context = qubitron.TransformerContext(tags_to_ignore=("nocompile",)) if with_context else None
    circuit = qubitron.eject_z(before, eject_parameterized=eject_parameterized, context=context)
    expected = qubitron.eject_z(expected, eject_parameterized=eject_parameterized, context=context)
    qubitron.testing.assert_same_circuits(circuit, expected)

    # And it should be idempotent.
    circuit = qubitron.eject_z(before, eject_parameterized=eject_parameterized, context=context)
    qubitron.testing.assert_same_circuits(circuit, expected)

    # Nested sub-circuits should also get optimized.
    q = before.all_qubits()
    c_nested = qubitron.Circuit(
        [(qubitron.Z**0.5).on_each(*q), (qubitron.Y**0.25).on_each(*q)],
        qubitron.Moment(qubitron.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        [(qubitron.Z**0.5).on_each(*q), (qubitron.Y**0.25).on_each(*q)],
        qubitron.Moment(qubitron.CircuitOperation(before.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    c_expected = qubitron.Circuit(
        (qubitron.X**0.25).on_each(*q),
        (qubitron.Z**0.5).on_each(*q),
        qubitron.Moment(qubitron.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        (qubitron.X**0.25).on_each(*q),
        (qubitron.Z**0.5).on_each(*q),
        qubitron.Moment(qubitron.CircuitOperation(expected.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    if context is None:
        context = qubitron.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    else:
        context = dataclasses.replace(
            context, tags_to_ignore=context.tags_to_ignore + ("ignore",), deep=True
        )
    c_nested = qubitron.eject_z(c_nested, context=context, eject_parameterized=eject_parameterized)
    qubitron.testing.assert_same_circuits(c_nested, c_expected)
    c_nested = qubitron.eject_z(c_nested, context=context, eject_parameterized=eject_parameterized)
    qubitron.testing.assert_same_circuits(c_nested, c_expected)


def assert_removes_all_z_gates(circuit: qubitron.Circuit, eject_parameterized: bool = True):
    optimized = qubitron.eject_z(circuit, eject_parameterized=eject_parameterized)
    for op in optimized.all_operations():
        # assert _try_get_known_z_half_turns(op, eject_parameterized) is None
        if isinstance(op.gate, qubitron.PhasedXZGate) and (
            eject_parameterized or not qubitron.is_parameterized(op.gate.z_exponent)
        ):
            assert op.gate.z_exponent == 0

    if qubitron.is_parameterized(circuit):
        for a in (0, 0.1, 0.5, 1.0, -1.0, 3.0):
            (
                qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                    qubitron.resolve_parameters(circuit, {'a': a}),
                    qubitron.resolve_parameters(optimized, {'a': a}),
                    atol=1e-8,
                )
            )
    else:
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            circuit, optimized, atol=1e-8
        )


def test_single_z_stays():
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5])]),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5])]),
    )


def test_single_phased_xz_stays():
    gate = qubitron.PhasedXZGate(axis_phase_exponent=0.2, x_exponent=0.3, z_exponent=0.4)
    q = qubitron.NamedQubit('q')
    assert_optimizes(before=qubitron.Circuit(gate(q)), expected=qubitron.Circuit(gate(q)))


def test_ignores_xz_and_cz():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.X(a) ** 0.5]),
                qubitron.Moment([qubitron.Y(b) ** 0.5]),
                qubitron.Moment([qubitron.CZ(a, b) ** 0.25]),
                qubitron.Moment([qubitron.Y(a) ** 0.5]),
                qubitron.Moment([qubitron.X(b) ** 0.5]),
            ]
        ),
        expected=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.X(a) ** 0.5]),
                qubitron.Moment([qubitron.Y(b) ** 0.5]),
                qubitron.Moment([qubitron.CZ(a, b) ** 0.25]),
                qubitron.Moment([qubitron.Y(a) ** 0.5]),
                qubitron.Moment([qubitron.X(b) ** 0.5]),
            ]
        ),
    )


def test_early_z():
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5]), qubitron.Moment(), qubitron.Moment()]),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5]), qubitron.Moment(), qubitron.Moment()]),
    )


def test_multi_z_merges():
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5]), qubitron.Moment([qubitron.Z(q) ** 0.25])]),
        expected=qubitron.Circuit([qubitron.Moment(), qubitron.Moment([qubitron.Z(q) ** 0.75])]),
    )


def test_z_pushes_past_xy_and_phases_it():
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.5]), qubitron.Moment([qubitron.Y(q) ** 0.25])]),
        expected=qubitron.Circuit(
            [qubitron.Moment(), qubitron.Moment([qubitron.X(q) ** 0.25]), qubitron.Moment([qubitron.Z(q) ** 0.5])]
        ),
    )


def test_z_pushes_past_cz():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    assert_optimizes(
        before=qubitron.Circuit(
            [qubitron.Moment([qubitron.Z(a) ** 0.5]), qubitron.Moment([qubitron.CZ(a, b) ** 0.25])]
        ),
        expected=qubitron.Circuit(
            [qubitron.Moment(), qubitron.Moment([qubitron.CZ(a, b) ** 0.25]), qubitron.Moment([qubitron.Z(a) ** 0.5])]
        ),
    )


def test_measurement_consumes_zs():
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.Z(q) ** 0.5]),
                qubitron.Moment([qubitron.Z(q) ** 0.25]),
                qubitron.Moment([qubitron.measure(q)]),
            ]
        ),
        expected=qubitron.Circuit([qubitron.Moment(), qubitron.Moment(), qubitron.Moment([qubitron.measure(q)])]),
    )


def test_unphaseable_causes_earlier_merge_without_size_increase():
    class UnknownGate(qubitron.testing.SingleQubitGate):
        pass

    u = UnknownGate()

    # pylint: disable=not-callable
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.Z(q)]),
                qubitron.Moment([u(q)]),
                qubitron.Moment([qubitron.Z(q) ** 0.5]),
                qubitron.Moment([qubitron.X(q)]),
                qubitron.Moment([qubitron.Z(q) ** 0.25]),
                qubitron.Moment([qubitron.X(q)]),
                qubitron.Moment([u(q)]),
            ]
        ),
        expected=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.Z(q)]),
                qubitron.Moment([u(q)]),
                qubitron.Moment(),
                qubitron.Moment([qubitron.PhasedXPowGate(phase_exponent=-0.5)(q)]),
                qubitron.Moment(),
                qubitron.Moment([qubitron.PhasedXPowGate(phase_exponent=-0.75).on(q)]),
                qubitron.Moment([qubitron.Z(q) ** 0.75]),
                qubitron.Moment([u(q)]),
            ]
        ),
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('a'), sympy.Symbol('a') + 1])
def test_symbols_block(sym):
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.Z(q)]),
                qubitron.Moment([qubitron.Z(q) ** sym]),
                qubitron.Moment([qubitron.Z(q) ** 0.25]),
            ]
        ),
        expected=qubitron.Circuit(
            [qubitron.Moment(), qubitron.Moment([qubitron.Z(q) ** sym]), qubitron.Moment([qubitron.Z(q) ** 1.25])]
        ),
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('a'), sympy.Symbol('a') + 1])
def test_symbols_eject(sym):
    q = qubitron.NamedQubit('q')
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.Z(q)]),
                qubitron.Moment([qubitron.Z(q) ** sym]),
                qubitron.Moment([qubitron.Z(q) ** 0.25]),
            ]
        ),
        expected=qubitron.Circuit(
            [qubitron.Moment(), qubitron.Moment(), qubitron.Moment([qubitron.Z(q) ** (sym + 1.25)])]
        ),
        eject_parameterized=True,
    )


def test_removes_zs():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.measure(a)))

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.measure(a, b)))

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.Z(a), qubitron.measure(a)))

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.measure(a, key='k')))

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.X(a), qubitron.measure(a)))

    assert_removes_all_z_gates(qubitron.Circuit(qubitron.Z(a), qubitron.X(a), qubitron.X(a), qubitron.measure(a)))

    assert_removes_all_z_gates(
        qubitron.Circuit(qubitron.Z(a), qubitron.Z(b), qubitron.CZ(a, b), qubitron.CZ(a, b), qubitron.measure(a, b))
    )

    assert_removes_all_z_gates(
        qubitron.Circuit(
            qubitron.PhasedXZGate(axis_phase_exponent=0, x_exponent=0, z_exponent=1).on(a),
            qubitron.measure(a),
        )
    )

    assert_removes_all_z_gates(
        qubitron.Circuit(
            qubitron.Z(a) ** sympy.Symbol('a'),
            qubitron.Z(b) ** (sympy.Symbol('a') + 1),
            qubitron.CZ(a, b),
            qubitron.CZ(a, b),
            qubitron.measure(a, b),
        ),
        eject_parameterized=True,
    )


def test_unknown_operation_blocks():
    q = qubitron.NamedQubit('q')

    class UnknownOp(qubitron.Operation):
        @property
        def qubits(self):
            return [q]

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    u = UnknownOp()

    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q)]), qubitron.Moment([u])]),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.Z(q)]), qubitron.Moment([u])]),
    )


def test_tagged_nocompile_operation_blocks():
    q = qubitron.NamedQubit('q')
    u = qubitron.Z(q).with_tags("nocompile")
    assert_optimizes(
        before=qubitron.Circuit([qubitron.Moment([qubitron.Z(q)]), qubitron.Moment([u])]),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.Z(q)]), qubitron.Moment([u])]),
        with_context=True,
    )


def test_swap():
    a, b = qubitron.LineQubit.range(2)
    original = qubitron.Circuit([qubitron.rz(0.123).on(a), qubitron.SWAP(a, b)])
    optimized = original.copy()

    optimized = qubitron.eject_z(optimized)
    optimized = qubitron.drop_empty_moments(optimized)

    assert optimized[0].operations == (qubitron.SWAP(a, b),)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (qubitron.Z(b) ** (0.123 / np.pi),)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(original), qubitron.unitary(optimized), atol=1e-8
    )


@pytest.mark.parametrize('exponent', (0, 2, 1.1, -2, -1.6))
def test_not_a_swap(exponent):
    a, b = qubitron.LineQubit.range(2)
    assert not _is_swaplike(qubitron.SWAP(a, b) ** exponent)


@pytest.mark.parametrize('theta', (np.pi / 2, -np.pi / 2, np.pi / 2 + 5 * np.pi))
def test_swap_fsim(theta):
    a, b = qubitron.LineQubit.range(2)
    original = qubitron.Circuit([qubitron.rz(0.123).on(a), qubitron.FSimGate(theta=theta, phi=0.123).on(a, b)])
    optimized = original.copy()

    optimized = qubitron.eject_z(optimized)
    optimized = qubitron.drop_empty_moments(optimized)

    assert optimized[0].operations == (qubitron.FSimGate(theta=theta, phi=0.123).on(a, b),)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (qubitron.Z(b) ** (0.123 / np.pi),)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(original), qubitron.unitary(optimized), atol=1e-8
    )


@pytest.mark.parametrize('theta', (0, 5 * np.pi, -np.pi))
def test_not_a_swap_fsim(theta):
    a, b = qubitron.LineQubit.range(2)
    assert not _is_swaplike(qubitron.FSimGate(theta=theta, phi=0.456).on(a, b))


@pytest.mark.parametrize('exponent', (1, -1))
def test_swap_iswap(exponent):
    a, b = qubitron.LineQubit.range(2)
    original = qubitron.Circuit([qubitron.rz(0.123).on(a), qubitron.ISWAP(a, b) ** exponent])
    optimized = original.copy()

    optimized = qubitron.eject_z(optimized)
    optimized = qubitron.drop_empty_moments(optimized)

    assert optimized[0].operations == (qubitron.ISWAP(a, b) ** exponent,)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (qubitron.Z(b) ** (0.123 / np.pi),)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(original), qubitron.unitary(optimized), atol=1e-8
    )
