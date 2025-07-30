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


def test_product_duplicate_keys():
    with pytest.raises(ValueError):
        _ = qubitron.Linspace('a', 0, 9, 10) * qubitron.Linspace('a', 0, 10, 11)


def test_zip_duplicate_keys():
    with pytest.raises(ValueError):
        _ = qubitron.Linspace('a', 0, 9, 10) + qubitron.Linspace('a', 0, 10, 11)


def test_product_wrong_type():
    with pytest.raises(TypeError):
        _ = qubitron.Linspace('a', 0, 9, 10) * 2


def test_zip_wrong_type():
    with pytest.raises(TypeError):
        _ = qubitron.Linspace('a', 0, 9, 10) + 2


def test_linspace():
    sweep = qubitron.Linspace('a', 0.34, 9.16, 7)
    assert len(sweep) == 7
    params = list(sweep.param_tuples())
    assert len(params) == 7
    assert params[0] == (('a', 0.34),)
    assert params[-1] == (('a', 9.16),)


def test_linspace_one_point():
    sweep = qubitron.Linspace('a', 0.34, 9.16, 1)
    assert len(sweep) == 1
    params = list(sweep.param_tuples())
    assert len(params) == 1
    assert params[0] == (('a', 0.34),)


def test_linspace_sympy_symbol():
    a = sympy.Symbol('a')
    sweep = qubitron.Linspace(a, 0.34, 9.16, 7)
    assert len(sweep) == 7
    params = list(sweep.param_tuples())
    assert len(params) == 7
    assert params[0] == (('a', 0.34),)
    assert params[-1] == (('a', 9.16),)


def test_points():
    sweep = qubitron.Points('a', [1, 2, 3, 4])
    assert len(sweep) == 4
    params = list(sweep)
    assert len(params) == 4


def test_zip():
    sweep = qubitron.Points('a', [1, 2, 3]) + qubitron.Points('b', [4, 5, 6, 7])
    assert len(sweep) == 3
    assert _values(sweep, 'a') == [1, 2, 3]
    assert _values(sweep, 'b') == [4, 5, 6]
    assert list(sweep.param_tuples()) == [
        (('a', 1), ('b', 4)),
        (('a', 2), ('b', 5)),
        (('a', 3), ('b', 6)),
    ]


def test_zip_longest():
    sweep = qubitron.ZipLongest(qubitron.Points('a', [1, 2, 3]), qubitron.Points('b', [4, 5, 6, 7]))
    assert tuple(sweep.param_tuples()) == (
        (('a', 1), ('b', 4)),
        (('a', 2), ('b', 5)),
        (('a', 3), ('b', 6)),
        (('a', 3), ('b', 7)),
    )
    assert sweep.keys == ['a', 'b']
    assert (
        str(sweep) == 'ZipLongest(qubitron.Points(\'a\', [1, 2, 3]), qubitron.Points(\'b\', [4, 5, 6, 7]))'
    )
    assert (
        repr(sweep)
        == 'qubitron_google.ZipLongest(qubitron.Points(\'a\', [1, 2, 3]), qubitron.Points(\'b\', [4, 5, 6, 7]))'
    )


def test_zip_longest_compatibility():
    sweep = qubitron.Zip(qubitron.Points('a', [1, 2, 3]), qubitron.Points('b', [4, 5, 6]))
    sweep_longest = qubitron.ZipLongest(qubitron.Points('a', [1, 2, 3]), qubitron.Points('b', [4, 5, 6]))
    assert tuple(sweep.param_tuples()) == tuple(sweep_longest.param_tuples())

    sweep = qubitron.Zip(
        (qubitron.Points('a', [1, 3]) * qubitron.Points('b', [2, 4])), qubitron.Points('c', [4, 5, 6, 7])
    )
    sweep_longest = qubitron.ZipLongest(
        (qubitron.Points('a', [1, 3]) * qubitron.Points('b', [2, 4])), qubitron.Points('c', [4, 5, 6, 7])
    )
    assert tuple(sweep.param_tuples()) == tuple(sweep_longest.param_tuples())


def test_empty_zip():
    assert len(qubitron.Zip()) == 0
    assert len(qubitron.ZipLongest()) == 0
    assert str(qubitron.Zip()) == 'Zip()'
    with pytest.raises(ValueError, match='non-empty'):
        _ = qubitron.ZipLongest(qubitron.Points('e', []), qubitron.Points('a', [1, 2, 3]))


def test_zip_eq():
    et = qubitron.testing.EqualsTester()
    point_sweep1 = qubitron.Points('a', [1, 2, 3])
    point_sweep2 = qubitron.Points('b', [4, 5, 6, 7])
    point_sweep3 = qubitron.Points('c', [1, 2])

    et.add_equality_group(qubitron.ZipLongest(), qubitron.ZipLongest())

    et.add_equality_group(
        qubitron.ZipLongest(point_sweep1, point_sweep2), qubitron.ZipLongest(point_sweep1, point_sweep2)
    )

    et.add_equality_group(qubitron.ZipLongest(point_sweep3, point_sweep2))
    et.add_equality_group(qubitron.ZipLongest(point_sweep2, point_sweep1))
    et.add_equality_group(qubitron.ZipLongest(point_sweep1, point_sweep2, point_sweep3))

    et.add_equality_group(qubitron.Zip(point_sweep1, point_sweep2, point_sweep3))
    et.add_equality_group(qubitron.Zip(point_sweep1, point_sweep2))


def test_product():
    sweep = qubitron.Points('a', [1, 2, 3]) * qubitron.Points('b', [4, 5, 6, 7])
    assert len(sweep) == 12
    assert _values(sweep, 'a') == [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    assert _values(sweep, 'b') == [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7]

    sweep = qubitron.Points('a', [1, 2]) * (qubitron.Points('b', [3, 4]) * qubitron.Points('c', [5, 6]))
    assert len(sweep) == 8
    assert _values(sweep, 'a') == [1, 1, 1, 1, 2, 2, 2, 2]
    assert _values(sweep, 'b') == [3, 3, 4, 4, 3, 3, 4, 4]
    assert _values(sweep, 'c') == [5, 6, 5, 6, 5, 6, 5, 6]


def test_zip_addition():
    zip_sweep = qubitron.Zip(qubitron.Points('a', [1, 2]), qubitron.Points('b', [3, 4]))
    zip_sweep2 = qubitron.Points('c', [5, 6]) + zip_sweep
    assert len(zip_sweep2) == 2
    assert _values(zip_sweep2, 'a') == [1, 2]
    assert _values(zip_sweep2, 'b') == [3, 4]
    assert _values(zip_sweep2, 'c') == [5, 6]


def test_empty_product():
    sweep = qubitron.Product()
    assert len(sweep) == len(list(sweep)) == 1
    assert str(sweep) == 'Product()'


def test_slice_access_error():
    sweep = qubitron.Points('a', [1, 2, 3])
    with pytest.raises(TypeError, match='<class \'str\'>'):
        _ = sweep['junk']

    with pytest.raises(IndexError):
        _ = sweep[4]

    with pytest.raises(IndexError):
        _ = sweep[-4]


def test_slice_sweep():
    sweep = qubitron.Points('a', [1, 2, 3]) * qubitron.Points('b', [4, 5, 6, 7])

    first_two = sweep[:2]
    assert list(first_two.param_tuples())[0] == (('a', 1), ('b', 4))
    assert list(first_two.param_tuples())[1] == (('a', 1), ('b', 5))
    assert len(list(first_two)) == 2

    middle_three = sweep[5:8]
    assert list(middle_three.param_tuples())[0] == (('a', 2), ('b', 5))
    assert list(middle_three.param_tuples())[1] == (('a', 2), ('b', 6))
    assert list(middle_three.param_tuples())[2] == (('a', 2), ('b', 7))
    assert len(list(middle_three.param_tuples())) == 3

    odd_elems = sweep[6:1:-2]
    assert list(odd_elems.param_tuples())[2] == (('a', 1), ('b', 6))
    assert list(odd_elems.param_tuples())[1] == (('a', 2), ('b', 4))
    assert list(odd_elems.param_tuples())[0] == (('a', 2), ('b', 6))
    assert len(list(odd_elems.param_tuples())) == 3

    sweep_reversed = sweep[::-1]
    assert list(sweep) == list(reversed(list(sweep_reversed)))

    single_sweep = sweep[5:6]
    assert list(single_sweep.param_tuples())[0] == (('a', 2), ('b', 5))
    assert len(list(single_sweep.param_tuples())) == 1


def test_access_sweep():
    sweep = qubitron.Points('a', [1, 2, 3]) * qubitron.Points('b', [4, 5, 6, 7])

    first_elem = sweep[-12]
    assert first_elem == qubitron.ParamResolver({'a': 1, 'b': 4})

    sixth_elem = sweep[5]
    assert sixth_elem == qubitron.ParamResolver({'a': 2, 'b': 5})


# We use factories since some of these produce generators and we want to
# test for passing in a generator to initializer.
@pytest.mark.parametrize(
    'r_list_factory',
    [
        lambda: [{'a': a, 'b': a + 1} for a in (0, 0.5, 1, -10)],
        lambda: ({'a': a, 'b': a + 1} for a in (0, 0.5, 1, -10)),
        lambda: ({sympy.Symbol('a'): a, 'b': a + 1} for a in (0, 0.5, 1, -10)),
    ],
)
def test_list_sweep(r_list_factory):
    sweep = qubitron.ListSweep(r_list_factory())
    assert sweep.keys == ['a', 'b']
    assert len(sweep) == 4
    assert len(list(sweep)) == 4
    assert list(sweep)[1] == qubitron.ParamResolver({'a': 0.5, 'b': 1.5})
    params = list(sweep.param_tuples())
    assert len(params) == 4
    assert params[3] == (('a', -10), ('b', -9))


def test_list_sweep_empty():
    assert qubitron.ListSweep([]).keys == []


def test_list_sweep_type_error():
    with pytest.raises(TypeError, match='Not a ParamResolver'):
        _ = qubitron.ListSweep([qubitron.ParamResolver(), 'bad'])


def _values(sweep, key):
    p = sympy.Symbol(key)
    return [resolver.value_of(p) for resolver in sweep]


def test_equality():
    et = qubitron.testing.EqualsTester()

    et.add_equality_group(qubitron.UnitSweep, qubitron.UnitSweep)

    # Test singleton
    assert qubitron.UNIT_SWEEP is qubitron.UnitSweep

    # Simple sweeps with the same key are equal to themselves, but different
    # from each other even if they happen to contain the same points.
    et.make_equality_group(lambda: qubitron.Linspace('a', 0, 10, 11))
    et.make_equality_group(lambda: qubitron.Linspace('b', 0, 10, 11))
    et.make_equality_group(lambda: qubitron.Points('a', list(range(11))))
    et.make_equality_group(lambda: qubitron.Points('b', list(range(11))))
    et.make_equality_group(lambda: qubitron.Concat(qubitron.Linspace('a', 0, 10, 11)))
    et.make_equality_group(lambda: qubitron.Concat(qubitron.Linspace('b', 0, 10, 11)))

    # Product and Zip sweeps can also be equated.
    et.make_equality_group(lambda: qubitron.Linspace('a', 0, 5, 6) * qubitron.Linspace('b', 10, 15, 6))
    et.make_equality_group(lambda: qubitron.Linspace('a', 0, 5, 6) + qubitron.Linspace('b', 10, 15, 6))
    et.make_equality_group(
        lambda: qubitron.Points('a', [1, 2])
        * (qubitron.Linspace('b', 0, 5, 6) + qubitron.Linspace('c', 10, 15, 6))
    )

    # ListSweep
    et.make_equality_group(
        lambda: qubitron.ListSweep([{'var': 1}, {'var': -1}]),
        lambda: qubitron.ListSweep(({'var': 1}, {'var': -1})),
        lambda: qubitron.ListSweep(r for r in ({'var': 1}, {'var': -1})),
    )
    et.make_equality_group(lambda: qubitron.ListSweep([{'var': -1}, {'var': 1}]))
    et.make_equality_group(lambda: qubitron.ListSweep([{'var': 1}]))
    et.make_equality_group(lambda: qubitron.ListSweep([{'x': 1}, {'x': -1}]))


def test_repr():
    qubitron.testing.assert_equivalent_repr(
        qubitron.study.sweeps.Product(qubitron.UnitSweep),
        setup_code='import qubitron\nfrom collections import OrderedDict',
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.study.sweeps.Zip(qubitron.UnitSweep),
        setup_code='import qubitron\nfrom collections import OrderedDict',
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.ListSweep(qubitron.Linspace('a', start=0, stop=3, length=4)),
        setup_code='import qubitron\nfrom collections import OrderedDict',
    )
    qubitron.testing.assert_equivalent_repr(qubitron.Points('zero&pi', [0, 3.14159]))
    qubitron.testing.assert_equivalent_repr(qubitron.Linspace('I/10', 0, 1, 10))
    qubitron.testing.assert_equivalent_repr(
        qubitron.Points('zero&pi', [0, 3.14159], metadata='example str')
    )
    qubitron.testing.assert_equivalent_repr(
        qubitron.Linspace('for_q0', 0, 1, 10, metadata=qubitron.LineQubit(0))
    )


def test_zip_product_str():
    assert (
        str(qubitron.UnitSweep + qubitron.UnitSweep + qubitron.UnitSweep)
        == 'qubitron.UnitSweep + qubitron.UnitSweep + qubitron.UnitSweep'
    )
    assert (
        str(qubitron.UnitSweep * qubitron.UnitSweep * qubitron.UnitSweep)
        == 'qubitron.UnitSweep * qubitron.UnitSweep * qubitron.UnitSweep'
    )
    assert (
        str(qubitron.UnitSweep + qubitron.UnitSweep * qubitron.UnitSweep)
        == 'qubitron.UnitSweep + qubitron.UnitSweep * qubitron.UnitSweep'
    )
    assert (
        str((qubitron.UnitSweep + qubitron.UnitSweep) * qubitron.UnitSweep)
        == '(qubitron.UnitSweep + qubitron.UnitSweep) * qubitron.UnitSweep'
    )


def test_list_sweep_str():
    assert (
        str(qubitron.UnitSweep)
        == '''Sweep:
{}'''
    )
    assert (
        str(qubitron.Linspace('a', start=0, stop=3, length=4))
        == '''Sweep:
{'a': 0.0}
{'a': 1.0}
{'a': 2.0}
{'a': 3.0}'''
    )
    assert (
        str(qubitron.Linspace('a', start=0, stop=15.75, length=64))
        == '''Sweep:
{'a': 0.0}
{'a': 0.25}
{'a': 0.5}
{'a': 0.75}
{'a': 1.0}
...
{'a': 14.75}
{'a': 15.0}
{'a': 15.25}
{'a': 15.5}
{'a': 15.75}'''
    )
    assert (
        str(qubitron.ListSweep(qubitron.Linspace('a', 0, 3, 4) + qubitron.Linspace('b', 1, 2, 2)))
        == '''Sweep:
{'a': 0.0, 'b': 1.0}
{'a': 1.0, 'b': 2.0}'''
    )
    assert (
        str(qubitron.ListSweep(qubitron.Linspace('a', 0, 3, 4) * qubitron.Linspace('b', 1, 2, 2)))
        == '''Sweep:
{'a': 0.0, 'b': 1.0}
{'a': 0.0, 'b': 2.0}
{'a': 1.0, 'b': 1.0}
{'a': 1.0, 'b': 2.0}
{'a': 2.0, 'b': 1.0}
{'a': 2.0, 'b': 2.0}
{'a': 3.0, 'b': 1.0}
{'a': 3.0, 'b': 2.0}'''
    )


def test_dict_to_product_sweep():
    assert qubitron.dict_to_product_sweep({'t': [0, 2, 3]}) == (
        qubitron.Product(qubitron.Points('t', [0, 2, 3]))
    )

    assert qubitron.dict_to_product_sweep({'t': [0, 1], 's': [2, 3], 'r': 4}) == (
        qubitron.Product(qubitron.Points('t', [0, 1]), qubitron.Points('s', [2, 3]), qubitron.Points('r', [4]))
    )


def test_dict_to_zip_sweep():
    assert qubitron.dict_to_zip_sweep({'t': [0, 2, 3]}) == (qubitron.Zip(qubitron.Points('t', [0, 2, 3])))

    assert qubitron.dict_to_zip_sweep({'t': [0, 1], 's': [2, 3], 'r': 4}) == (
        qubitron.Zip(qubitron.Points('t', [0, 1]), qubitron.Points('s', [2, 3]), qubitron.Points('r', [4]))
    )


def test_concat_linspace():
    sweep1 = qubitron.Linspace('a', 0.34, 9.16, 4)
    sweep2 = qubitron.Linspace('a', 10, 20, 4)
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    assert len(concat_sweep) == 8
    assert concat_sweep.keys == ['a']
    params = list(concat_sweep.param_tuples())
    assert len(params) == 8
    assert params[0] == (('a', 0.34),)
    assert params[3] == (('a', 9.16),)
    assert params[4] == (('a', 10.0),)
    assert params[7] == (('a', 20.0),)


def test_concat_points():
    sweep1 = qubitron.Points('a', [1, 2])
    sweep2 = qubitron.Points('a', [3, 4, 5])
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    assert concat_sweep.keys == ['a']
    assert len(concat_sweep) == 5
    params = list(concat_sweep)
    assert len(params) == 5
    assert _values(concat_sweep, 'a') == [1, 2, 3, 4, 5]


def test_concat_many_points():
    sweep1 = qubitron.Points('a', [1, 2])
    sweep2 = qubitron.Points('a', [3, 4, 5])
    sweep3 = qubitron.Points('a', [6, 7, 8])
    concat_sweep = qubitron.Concat(sweep1, sweep2, sweep3)

    assert len(concat_sweep) == 8
    params = list(concat_sweep)
    assert len(params) == 8
    assert _values(concat_sweep, 'a') == [1, 2, 3, 4, 5, 6, 7, 8]


def test_concat_mixed():
    sweep1 = qubitron.Linspace('a', 0, 1, 3)
    sweep2 = qubitron.Points('a', [2, 3])
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    assert len(concat_sweep) == 5
    assert _values(concat_sweep, 'a') == [0.0, 0.5, 1.0, 2, 3]


def test_concat_inconsistent_keys():
    sweep1 = qubitron.Linspace('a', 0, 1, 3)
    sweep2 = qubitron.Points('b', [2, 3])

    with pytest.raises(ValueError, match="All sweeps must have the same descriptors"):
        qubitron.Concat(sweep1, sweep2)


def test_concat_sympy_symbol():
    a = sympy.Symbol('a')
    sweep1 = qubitron.Linspace(a, 0, 1, 3)
    sweep2 = qubitron.Points(a, [2, 3])
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    assert len(concat_sweep) == 5
    assert _values(concat_sweep, 'a') == [0.0, 0.5, 1.0, 2, 3]


def test_concat_repr_and_str():
    sweep1 = qubitron.Linspace('a', 0, 1, 3)
    sweep2 = qubitron.Points('a', [2, 3])
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    expected_repr = (
        "qubitron.Concat(qubitron.Linspace('a', start=0, stop=1, length=3), qubitron.Points('a', [2, 3]))"
    )
    expected_str = "Concat(qubitron.Linspace('a', start=0, stop=1, length=3), qubitron.Points('a', [2, 3]))"

    assert repr(concat_sweep) == expected_repr
    assert str(concat_sweep) == expected_str


def test_concat_large_sweep():
    sweep1 = qubitron.Points('a', list(range(101)))
    sweep2 = qubitron.Points('a', list(range(101, 202)))
    concat_sweep = qubitron.Concat(sweep1, sweep2)

    assert len(concat_sweep) == 202
    assert _values(concat_sweep, 'a') == list(range(101)) + list(range(101, 202))


def test_concat_different_keys_raises():
    sweep1 = qubitron.Linspace('a', 0, 1, 3)
    sweep2 = qubitron.Points('b', [2, 3])

    with pytest.raises(ValueError, match="All sweeps must have the same descriptors."):
        _ = qubitron.Concat(sweep1, sweep2)


def test_concat_empty_sweep_raises():
    with pytest.raises(ValueError, match="Concat requires at least one sweep."):
        _ = qubitron.Concat()
