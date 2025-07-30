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

"""Tests for sweepable.py."""

from __future__ import annotations

import itertools

import pytest
import sympy

import qubitron


def test_to_resolvers_none():
    assert list(qubitron.to_resolvers(None)) == [qubitron.ParamResolver({})]


def test_to_resolvers_single():
    resolver = qubitron.ParamResolver({})
    assert list(qubitron.to_resolvers(resolver)) == [resolver]
    assert list(qubitron.to_resolvers({})) == [resolver]


def test_to_resolvers_sweep():
    sweep = qubitron.Linspace('a', 0, 1, 10)
    assert list(qubitron.to_resolvers(sweep)) == list(sweep)


def test_to_resolvers_iterable():
    resolvers = [qubitron.ParamResolver({'a': 2}), qubitron.ParamResolver({'a': 1})]
    assert list(qubitron.to_resolvers(resolvers)) == resolvers
    assert list(qubitron.to_resolvers([{'a': 2}, {'a': 1}])) == resolvers


def test_to_resolvers_iterable_sweeps():
    sweeps = [qubitron.Linspace('a', 0, 1, 10), qubitron.Linspace('b', 0, 1, 10)]
    assert list(qubitron.to_resolvers(sweeps)) == list(itertools.chain(*sweeps))


def test_to_resolvers_bad():
    with pytest.raises(TypeError, match='Unrecognized sweepable'):
        for _ in qubitron.study.to_resolvers('nope'):
            pass


def test_to_sweeps_none():
    assert qubitron.study.to_sweeps(None) == [qubitron.UnitSweep]


def test_to_sweeps_single():
    resolver = qubitron.ParamResolver({})
    assert qubitron.study.to_sweeps(resolver) == [qubitron.UnitSweep]
    assert qubitron.study.to_sweeps({}) == [qubitron.UnitSweep]


def test_to_sweeps_sweep():
    sweep = qubitron.Linspace('a', 0, 1, 10)
    assert qubitron.study.to_sweeps(sweep) == [sweep]


def test_to_sweeps_iterable():
    resolvers = [qubitron.ParamResolver({'a': 2}), qubitron.ParamResolver({'a': 1})]
    sweeps = [qubitron.study.Zip(qubitron.Points('a', [2])), qubitron.study.Zip(qubitron.Points('a', [1]))]
    assert qubitron.study.to_sweeps(resolvers) == sweeps
    assert qubitron.study.to_sweeps([{'a': 2}, {'a': 1}]) == sweeps


def test_to_sweeps_iterable_sweeps():
    sweeps = [qubitron.Linspace('a', 0, 1, 10), qubitron.Linspace('b', 0, 1, 10)]
    assert qubitron.study.to_sweeps(sweeps) == sweeps


def test_to_sweeps_dictionary_of_list():
    with pytest.warns(DeprecationWarning, match='dict_to_product_sweep'):
        assert qubitron.study.to_sweeps({'t': [0, 2, 3]}) == qubitron.study.to_sweeps(
            [{'t': 0}, {'t': 2}, {'t': 3}]
        )
        assert qubitron.study.to_sweeps({'t': [0, 1], 's': [2, 3], 'r': 4}) == qubitron.study.to_sweeps(
            [
                {'t': 0, 's': 2, 'r': 4},
                {'t': 0, 's': 3, 'r': 4},
                {'t': 1, 's': 2, 'r': 4},
                {'t': 1, 's': 3, 'r': 4},
            ]
        )


def test_to_sweeps_invalid():
    with pytest.raises(TypeError, match='Unrecognized sweepable'):
        qubitron.study.to_sweeps('nope')


def test_to_sweep_sweep():
    sweep = qubitron.Linspace('a', 0, 1, 10)
    assert qubitron.to_sweep(sweep) is sweep


@pytest.mark.parametrize(
    'r_gen',
    [
        lambda: {'a': 1},
        lambda: {sympy.Symbol('a'): 1},
        lambda: qubitron.ParamResolver({'a': 1}),
        lambda: qubitron.ParamResolver({sympy.Symbol('a'): 1}),
    ],
)
def test_to_sweep_single_resolver(r_gen):
    sweep = qubitron.to_sweep(r_gen())
    assert isinstance(sweep, qubitron.Sweep)
    assert list(sweep) == [qubitron.ParamResolver({'a': 1})]


@pytest.mark.parametrize(
    'r_list_gen',
    [
        # Lists
        lambda: [{'a': 1}, {'a': 1.5}],
        lambda: [{sympy.Symbol('a'): 1}, {sympy.Symbol('a'): 1.5}],
        lambda: [qubitron.ParamResolver({'a': 1}), qubitron.ParamResolver({'a': 1.5})],
        lambda: [
            qubitron.ParamResolver({sympy.Symbol('a'): 1}),
            qubitron.ParamResolver({sympy.Symbol('a'): 1.5}),
        ],
        lambda: [{'a': 1}, qubitron.ParamResolver({sympy.Symbol('a'): 1.5})],
        lambda: ({'a': 1}, {'a': 1.5}),
        # Iterators
        lambda: (r for r in [{'a': 1}, {'a': 1.5}]),
        lambda: {object(): r for r in [{'a': 1}, {'a': 1.5}]}.values(),
    ],
)
def test_to_sweep_resolver_list(r_list_gen):
    sweep = qubitron.to_sweep(r_list_gen())
    assert isinstance(sweep, qubitron.Sweep)
    assert list(sweep) == [qubitron.ParamResolver({'a': 1}), qubitron.ParamResolver({'a': 1.5})]


def test_to_sweep_type_error():
    with pytest.raises(TypeError, match='Unexpected sweep'):
        qubitron.to_sweep(5)


def test_to_sweeps_with_param_dict_appends_metadata():
    params = {'a': 1, 'b': 2, 'c': 3}
    unit_map = {'a': 'ns', 'b': 'ns'}

    sweep = qubitron.to_sweeps(params, unit_map)

    assert sweep == [
        qubitron.Zip(
            qubitron.Points('a', [1], metadata='ns'),
            qubitron.Points('b', [2], metadata='ns'),
            qubitron.Points('c', [3]),
        )
    ]


def test_to_sweeps_with_param_list_appends_metadata():
    resolvers = [qubitron.ParamResolver({'a': 2}), qubitron.ParamResolver({'a': 1})]
    unit_map = {'a': 'ns'}

    sweeps = qubitron.study.to_sweeps(resolvers, unit_map)

    assert sweeps == [
        qubitron.Zip(qubitron.Points('a', [2], metadata='ns')),
        qubitron.Zip(qubitron.Points('a', [1], metadata='ns')),
    ]
