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

import itertools

import numpy as np
import pytest
import sympy

import qubitron


@pytest.mark.parametrize(
    'phase_exponent', [-0.5, 0, 0.5, 1, sympy.Symbol('p'), sympy.Symbol('p') + 1]
)
def test_phased_x_consistent_protocols(phase_exponent):
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.PhasedXPowGate(phase_exponent=phase_exponent, exponent=1.0)
    )
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.PhasedXPowGate(phase_exponent=phase_exponent, exponent=1.0, global_shift=0.1)
    )


def test_init():
    g = qubitron.PhasedXPowGate(phase_exponent=0.75, exponent=0.25, global_shift=0.1)
    assert g.phase_exponent == 0.75
    assert g.exponent == 0.25
    assert g._global_shift == 0.1

    x = qubitron.PhasedXPowGate(phase_exponent=0, exponent=0.1, global_shift=0.2)
    assert x.phase_exponent == 0
    assert x.exponent == 0.1
    assert x._global_shift == 0.2

    y = qubitron.PhasedXPowGate(phase_exponent=0.5, exponent=0.1, global_shift=0.2)
    assert y.phase_exponent == 0.5
    assert y.exponent == 0.1
    assert y._global_shift == 0.2


@pytest.mark.parametrize('sym', [sympy.Symbol('a'), sympy.Symbol('a') + 1])
def test_no_symbolic_qasm_but_fails_gracefully(sym):
    q = qubitron.NamedQubit('q')
    v = qubitron.PhasedXPowGate(phase_exponent=sym).on(q)
    assert qubitron.qasm(v, args=qubitron.QasmArgs(), default=None) is None


def test_extrapolate():
    g = qubitron.PhasedXPowGate(phase_exponent=0.25)
    assert g**0.25 == (g**0.5) ** 0.5

    # The gate is self-inverse, but there are hidden variables tracking the
    # exponent's sign and scale.
    assert g**-1 == g
    assert g.exponent == 1
    assert (g**-1).exponent == -1
    assert g**-0.5 == (g**-1) ** 0.5 != g**0.5
    assert g == g**3
    assert g**0.5 != (g**3) ** 0.5 == g**-0.5


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.PhasedXPowGate(phase_exponent=0),
        qubitron.PhasedXPowGate(phase_exponent=0, exponent=1),
        qubitron.PhasedXPowGate(exponent=1, phase_exponent=0),
        qubitron.PhasedXPowGate(exponent=1, phase_exponent=2),
        qubitron.PhasedXPowGate(exponent=1, phase_exponent=-2),
    )
    eq.add_equality_group(qubitron.X)
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=1, phase_exponent=2, global_shift=0.1))

    eq.add_equality_group(
        qubitron.PhasedXPowGate(phase_exponent=0.5, exponent=1),
        qubitron.PhasedXPowGate(phase_exponent=2.5, exponent=3),
    )
    eq.add_equality_group(qubitron.Y)
    eq.add_equality_group(qubitron.PhasedXPowGate(phase_exponent=0.5, exponent=0.25))
    eq.add_equality_group(qubitron.Y**0.25)

    eq.add_equality_group(qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=0.25, global_shift=0.1))
    eq.add_equality_group(qubitron.PhasedXPowGate(phase_exponent=2.25, exponent=0.25, global_shift=0.2))

    eq.make_equality_group(
        lambda: qubitron.PhasedXPowGate(exponent=sympy.Symbol('a'), phase_exponent=0)
    )
    eq.make_equality_group(
        lambda: qubitron.PhasedXPowGate(exponent=sympy.Symbol('a') + 1, phase_exponent=0)
    )
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=sympy.Symbol('a'), phase_exponent=0.25))
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=sympy.Symbol('a') + 1, phase_exponent=0.25))
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=0, phase_exponent=0))
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=0, phase_exponent=sympy.Symbol('a')))
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=0, phase_exponent=sympy.Symbol('a') + 1))
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=0, phase_exponent=0.5))
    eq.add_equality_group(
        qubitron.PhasedXPowGate(exponent=sympy.Symbol('ab'), phase_exponent=sympy.Symbol('xy'))
    )
    eq.add_equality_group(
        qubitron.PhasedXPowGate(exponent=sympy.Symbol('ab') + 1, phase_exponent=sympy.Symbol('xy') + 1)
    )

    eq.add_equality_group(
        qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=0.125, global_shift=-0.5),
        qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=4.125, global_shift=-0.5),
    )
    eq.add_equality_group(
        qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=2.125, global_shift=-0.5)
    )


def test_approx_eq():
    assert qubitron.approx_eq(
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.3),
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.3),
        atol=1e-4,
    )
    assert not qubitron.approx_eq(
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.4),
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.3),
        atol=1e-4,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.4),
        qubitron.PhasedXPowGate(phase_exponent=0.1, exponent=0.2, global_shift=0.3),
        atol=0.2,
    )


def test_str_repr():
    assert str(qubitron.PhasedXPowGate(phase_exponent=0.25)) == 'PhX(0.25)'
    assert str(qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=0.5)) == 'PhX(0.25)**0.5'
    assert repr(
        qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=4, global_shift=0.125)
        == 'qubitron.PhasedXPowGate(phase_exponent=0.25, '
        'exponent=4, global_shift=0.125)'
    )
    assert (
        repr(qubitron.PhasedXPowGate(phase_exponent=0.25)) == 'qubitron.PhasedXPowGate(phase_exponent=0.25)'
    )


@pytest.mark.parametrize(
    'resolve_fn, global_shift', [(qubitron.resolve_parameters, 0), (qubitron.resolve_parameters_once, 0.1)]
)
def test_parameterize(resolve_fn, global_shift):
    parameterized_gate = qubitron.PhasedXPowGate(
        exponent=sympy.Symbol('a'), phase_exponent=sympy.Symbol('b'), global_shift=global_shift
    )
    assert qubitron.pow(parameterized_gate, 5) == qubitron.PhasedXPowGate(
        exponent=sympy.Symbol('a') * 5, phase_exponent=sympy.Symbol('b'), global_shift=global_shift
    )
    assert qubitron.unitary(parameterized_gate, default=None) is None
    assert qubitron.is_parameterized(parameterized_gate)
    q = qubitron.NamedQubit("q")
    parameterized_decomposed_circuit = qubitron.Circuit(qubitron.decompose(parameterized_gate(q)))
    for resolver in qubitron.Linspace('a', 0, 2, 10) * qubitron.Linspace('b', 0, 2, 10):
        resolved_gate = resolve_fn(parameterized_gate, resolver)
        assert resolved_gate == qubitron.PhasedXPowGate(
            exponent=resolver.value_of('a'),
            phase_exponent=resolver.value_of('b'),
            global_shift=global_shift,
        )
        np.testing.assert_allclose(
            qubitron.unitary(resolved_gate(q)),
            qubitron.unitary(resolve_fn(parameterized_decomposed_circuit, resolver)),
            atol=1e-8,
        )

    unparameterized_gate = qubitron.PhasedXPowGate(
        exponent=0.1, phase_exponent=0.2, global_shift=global_shift
    )
    assert not qubitron.is_parameterized(unparameterized_gate)
    assert qubitron.is_parameterized(unparameterized_gate ** sympy.Symbol('a'))
    assert qubitron.is_parameterized(unparameterized_gate ** (sympy.Symbol('a') + 1))

    resolver = {'a': 0.5j}
    with pytest.raises(ValueError, match='complex value'):
        resolve_fn(
            qubitron.PhasedXPowGate(
                exponent=sympy.Symbol('a'), phase_exponent=0.2, global_shift=global_shift
            ),
            resolver,
        )
    with pytest.raises(ValueError, match='complex value'):
        resolve_fn(
            qubitron.PhasedXPowGate(
                exponent=0.1, phase_exponent=sympy.Symbol('a'), global_shift=global_shift
            ),
            resolver,
        )


def test_trace_bound():
    assert (
        qubitron.trace_distance_bound(qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=0.001)) < 0.01
    )
    assert (
        qubitron.trace_distance_bound(
            qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=sympy.Symbol('a'))
        )
        >= 1
    )


def test_diagram():
    q = qubitron.NamedQubit('q')
    c = qubitron.Circuit(
        qubitron.PhasedXPowGate(phase_exponent=sympy.Symbol('a'), exponent=sympy.Symbol('b')).on(q),
        qubitron.PhasedXPowGate(
            phase_exponent=sympy.Symbol('a') * 2, exponent=sympy.Symbol('b') + 1
        ).on(q),
        qubitron.PhasedXPowGate(phase_exponent=0.25, exponent=1).on(q),
        qubitron.PhasedXPowGate(phase_exponent=1, exponent=1).on(q),
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
q: ───PhX(a)^b───PhX(2*a)^(b + 1)───PhX(0.25)───PhX(1)───
""",
    )


def test_phase_by():
    g = qubitron.PhasedXPowGate(phase_exponent=0.25)
    g2 = qubitron.phase_by(g, 0.25, 0)
    assert g2 == qubitron.PhasedXPowGate(phase_exponent=0.75)

    g = qubitron.PhasedXPowGate(phase_exponent=0)
    g2 = qubitron.phase_by(g, 0.125, 0)
    assert g2 == qubitron.PhasedXPowGate(phase_exponent=0.25)

    g = qubitron.PhasedXPowGate(phase_exponent=0.5)
    g2 = qubitron.phase_by(g, 0.125, 0)
    assert g2 == qubitron.PhasedXPowGate(phase_exponent=0.75)

    g = qubitron.PhasedXPowGate(phase_exponent=0.5)
    g2 = qubitron.phase_by(g, sympy.Symbol('b') + 1, 0)
    assert g2 == qubitron.PhasedXPowGate(phase_exponent=2 * sympy.Symbol('b') + 2.5)


@pytest.mark.parametrize(
    'exponent,phase_exponent', itertools.product(np.arange(-2.5, 2.75, 0.25), repeat=2)
)
def test_exponent_consistency(exponent, phase_exponent):
    """Verifies that instances of PhasedX gate expose consistent exponents."""
    g = qubitron.PhasedXPowGate(exponent=exponent, phase_exponent=phase_exponent)
    assert g.exponent in [exponent, -exponent]
    assert g.phase_exponent in [qubitron.value.canonicalize_half_turns(g.phase_exponent)]

    g2 = qubitron.PhasedXPowGate(exponent=g.exponent, phase_exponent=g.phase_exponent)
    assert g == g2

    u = qubitron.protocols.unitary(g)
    u2 = qubitron.protocols.unitary(g2)
    assert np.all(u == u2)


def test_approx_eq_for_close_phase_exponents():
    gate1 = qubitron.PhasedXPowGate(phase_exponent=0)
    gate2 = qubitron.PhasedXPowGate(phase_exponent=1e-12)
    gate3 = qubitron.PhasedXPowGate(phase_exponent=2e-12)
    gate4 = qubitron.PhasedXPowGate(phase_exponent=0.345)

    assert qubitron.approx_eq(gate2, gate3)
    assert qubitron.approx_eq(gate2, gate1)
    assert not qubitron.approx_eq(gate2, gate4)

    assert qubitron.equal_up_to_global_phase(gate2, gate3)
    assert qubitron.equal_up_to_global_phase(gate2, gate1)
    assert not qubitron.equal_up_to_global_phase(gate2, gate4)
