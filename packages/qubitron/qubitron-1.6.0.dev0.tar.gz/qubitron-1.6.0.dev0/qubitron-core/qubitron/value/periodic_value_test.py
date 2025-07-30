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

import pytest
import sympy

import qubitron


def test_periodic_value_equality() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.PeriodicValue(1, 2),
        qubitron.PeriodicValue(1, 2),
        qubitron.PeriodicValue(3, 2),
        qubitron.PeriodicValue(3, 2),
        qubitron.PeriodicValue(5, 2),
        qubitron.PeriodicValue(-1, 2),
    )
    eq.add_equality_group(qubitron.PeriodicValue(1.5, 2.0), qubitron.PeriodicValue(1.5, 2.0))
    eq.add_equality_group(qubitron.PeriodicValue(0, 2))
    eq.add_equality_group(qubitron.PeriodicValue(1, 3))
    eq.add_equality_group(qubitron.PeriodicValue(2, 4))


def test_periodic_value_approx_eq_basic() -> None:
    assert qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.0, 2.0), atol=0.1)
    assert qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.2, 2.0), atol=0.3)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.2, 2.0), atol=0.1)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.0, 2.2), atol=0.3)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.0, 2.2), atol=0.1)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.2, 2.2), atol=0.3)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(1.0, 2.0), qubitron.PeriodicValue(1.2, 2.2), atol=0.1)
    assert qubitron.approx_eq(
        qubitron.PeriodicValue(sympy.Symbol('t'), 2.0),
        qubitron.PeriodicValue(sympy.Symbol('t'), 2.0),
        atol=0.1,
    )


def test_periodic_value_approx_eq_normalized() -> None:
    assert qubitron.approx_eq(qubitron.PeriodicValue(1.0, 3.0), qubitron.PeriodicValue(4.1, 3.0), atol=0.2)
    assert qubitron.approx_eq(qubitron.PeriodicValue(1.0, 3.0), qubitron.PeriodicValue(-2.1, 3.0), atol=0.2)


def test_periodic_value_approx_eq_boundary() -> None:
    assert qubitron.approx_eq(qubitron.PeriodicValue(0.0, 2.0), qubitron.PeriodicValue(1.9, 2.0), atol=0.2)
    assert qubitron.approx_eq(qubitron.PeriodicValue(0.1, 2.0), qubitron.PeriodicValue(1.9, 2.0), atol=0.3)
    assert qubitron.approx_eq(qubitron.PeriodicValue(1.9, 2.0), qubitron.PeriodicValue(0.1, 2.0), atol=0.3)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(0.1, 2.0), qubitron.PeriodicValue(1.9, 2.0), atol=0.1)
    assert qubitron.approx_eq(qubitron.PeriodicValue(0, 1.0), qubitron.PeriodicValue(0.5, 1.0), atol=0.6)
    assert not qubitron.approx_eq(qubitron.PeriodicValue(0, 1.0), qubitron.PeriodicValue(0.5, 1.0), atol=0.1)
    assert qubitron.approx_eq(qubitron.PeriodicValue(0.4, 1.0), qubitron.PeriodicValue(0.6, 1.0), atol=0.3)


def test_periodic_value_types_mismatch() -> None:
    assert not qubitron.approx_eq(qubitron.PeriodicValue(0.0, 2.0), 0.0, atol=0.2)
    assert not qubitron.approx_eq(0.0, qubitron.PeriodicValue(0.0, 2.0), atol=0.2)


@pytest.mark.parametrize(
    'value, is_parameterized, parameter_names',
    [
        (qubitron.PeriodicValue(1.0, 3.0), False, set()),
        (qubitron.PeriodicValue(0.0, sympy.Symbol('p')), True, {'p'}),
        (qubitron.PeriodicValue(sympy.Symbol('v'), 3.0), True, {'v'}),
        (qubitron.PeriodicValue(sympy.Symbol('v'), sympy.Symbol('p')), True, {'p', 'v'}),
    ],
)
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_periodic_value_is_parameterized(
    value, is_parameterized, parameter_names, resolve_fn
) -> None:
    assert qubitron.is_parameterized(value) == is_parameterized
    assert qubitron.parameter_names(value) == parameter_names
    resolved = resolve_fn(value, {p: 1 for p in parameter_names})
    assert not qubitron.is_parameterized(resolved)


@pytest.mark.parametrize(
    'val',
    [
        qubitron.PeriodicValue(0.4, 1.0),
        qubitron.PeriodicValue(0.0, 2.0),
        qubitron.PeriodicValue(1.0, 3),
        qubitron.PeriodicValue(-2.1, 3.0),
        qubitron.PeriodicValue(sympy.Symbol('v'), sympy.Symbol('p')),
        qubitron.PeriodicValue(2.0, sympy.Symbol('p')),
        qubitron.PeriodicValue(sympy.Symbol('v'), 3),
    ],
)
def test_periodic_value_repr(val) -> None:
    qubitron.testing.assert_equivalent_repr(val)
