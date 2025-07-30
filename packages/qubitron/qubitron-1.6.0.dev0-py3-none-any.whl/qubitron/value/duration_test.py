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

from datetime import timedelta

import numpy as np
import pytest
import sympy

import qubitron
from qubitron.value import Duration


def test_init():
    assert Duration().total_picos() == 0
    assert Duration(picos=513).total_picos() == 513
    assert Duration(picos=-5).total_picos() == -5
    assert Duration(nanos=211).total_picos() == 211000
    assert Duration(nanos=211, picos=1051).total_picos() == 212051

    assert isinstance(Duration(picos=1).total_picos(), int)
    assert isinstance(Duration(nanos=1).total_picos(), int)
    assert isinstance(Duration(picos=1.0).total_picos(), float)
    assert isinstance(Duration(nanos=1.0).total_picos(), float)

    assert Duration(Duration(nanos=2)) == Duration(nanos=2)
    assert Duration(timedelta(0, 0, 5)) == Duration(micros=5)
    assert Duration(0) == Duration()
    assert Duration(None) == Duration()
    assert (
        Duration(timedelta(0, 5), millis=4, micros=3, nanos=2, picos=1).total_picos()
        == 5004003002001
    )

    with pytest.raises(TypeError):
        _ = Duration(object())


def test_numpy_types():
    assert Duration(nanos=np.float64(1)).total_nanos() == 1.0
    assert Duration(nanos=np.int64(1)).total_nanos() == 1.0
    assert type(Duration(nanos=np.float64(1)).total_nanos()) == float
    assert type(Duration(nanos=np.int64(1)).total_nanos()) == float


def test_init_timedelta():
    assert Duration(timedelta(microseconds=0)).total_picos() == 0
    assert Duration(timedelta(microseconds=513)).total_picos() == 513 * 10**6
    assert Duration(timedelta(microseconds=-5)).total_picos() == -5 * 10**6
    assert Duration(timedelta(microseconds=211)).total_picos() == 211 * 10**6

    assert Duration(timedelta(seconds=3)).total_picos() == 3 * 10**12
    assert Duration(timedelta(seconds=-5)).total_picos() == -5 * 10**12
    assert Duration(timedelta(seconds=3)).total_nanos() == 3 * 10**9
    assert Duration(timedelta(seconds=-5)).total_nanos() == -5 * 10**9


def test_total():
    assert Duration().total_nanos() == 0
    assert Duration(picos=3000).total_nanos() == 3
    assert Duration(nanos=5).total_nanos() == 5

    assert Duration().total_nanos() == 0
    assert Duration(picos=500).total_nanos() == 0.5
    assert Duration(nanos=500).total_micros() == 0.5
    assert Duration(micros=500).total_millis() == 0.5
    assert Duration(millis=500).total_millis() == 500


def test_repr():
    qubitron.testing.assert_equivalent_repr(Duration(millis=2))
    qubitron.testing.assert_equivalent_repr(Duration(micros=2))
    qubitron.testing.assert_equivalent_repr(Duration(picos=1000, nanos=1000))
    qubitron.testing.assert_equivalent_repr(Duration(picos=5000))
    qubitron.testing.assert_equivalent_repr(Duration(nanos=1.0))
    qubitron.testing.assert_equivalent_repr(Duration(micros=sympy.Symbol('t')))
    qubitron.testing.assert_equivalent_repr(Duration(micros=1.5 * sympy.Symbol('t')))


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(Duration(), Duration(picos=0), Duration(nanos=0.0), timedelta(0))
    eq.add_equality_group(Duration(picos=1000), Duration(nanos=1))
    eq.make_equality_group(lambda: Duration(picos=-1))
    eq.add_equality_group(Duration(micros=5.0), Duration(micros=5), timedelta(0, 0, 5))

    # Can't hash match 0, but no-duration is equal to 0.
    assert Duration() == 0
    assert Duration(picos=1) != 0


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterized(resolve_fn):
    t = sympy.Symbol('t')
    assert not qubitron.is_parameterized(Duration())
    assert not qubitron.is_parameterized(Duration(nanos=500))
    assert qubitron.is_parameterized(Duration(nanos=500 * t))

    assert resolve_fn(Duration(), {'t': 2}) == Duration()
    assert resolve_fn(Duration(nanos=500), {'t': 2}) == Duration(nanos=500)
    assert resolve_fn(Duration(nanos=500 * t), {'t': 2}) == Duration(nanos=1000)


def test_cmp():
    order = qubitron.testing.OrderTester()

    order.add_ascending_equivalence_group(Duration(picos=-1), Duration(picos=-1.0))
    order.add_ascending_equivalence_group(Duration(), timedelta(0))
    order.add_ascending_equivalence_group(Duration(picos=1))
    order.add_ascending_equivalence_group(Duration(nanos=1))
    order.add_ascending_equivalence_group(Duration(micros=1))
    order.add_ascending_equivalence_group(Duration(micros=5), timedelta(0, 0, 5))
    order.add_ascending_equivalence_group(Duration(micros=6), timedelta(0, 0, 6))
    order.add_ascending_equivalence_group(Duration(millis=1))

    assert Duration(picos=-1) < 0 < Duration(picos=+1)
    assert Duration(picos=-1) <= 0 <= Duration(picos=+1)
    assert Duration() <= 0 <= Duration()


def test_add():
    assert Duration() + Duration() == Duration()
    assert Duration(picos=1) + Duration(picos=2) == Duration(picos=3)

    assert Duration(picos=1) + timedelta(microseconds=2) == Duration(picos=2000001)
    assert timedelta(microseconds=1) + Duration(picos=2) == Duration(picos=1000002)

    t = sympy.Symbol('t')
    assert Duration(picos=3) + Duration(picos=t) == Duration(picos=3 + t)

    with pytest.raises(TypeError):
        _ = 1 + Duration()
    with pytest.raises(TypeError):
        _ = Duration() + 1


def test_bool():
    assert bool(qubitron.Duration(picos=1))
    assert not bool(qubitron.Duration())


def test_sub():
    assert Duration() - Duration() == Duration()
    assert Duration(picos=1) - Duration(picos=2) == Duration(picos=-1)

    assert Duration(picos=1) - timedelta(microseconds=2) == Duration(picos=-1999999)
    assert timedelta(microseconds=1) - Duration(picos=2) == Duration(picos=999998)

    t = sympy.Symbol('t')
    assert Duration(picos=3) - Duration(picos=t) == Duration(picos=3 - t)

    with pytest.raises(TypeError):
        _ = 1 - Duration()
    with pytest.raises(TypeError):
        _ = Duration() - 1


def test_mul():
    assert Duration(picos=2) * 3 == Duration(picos=6)
    assert 4 * Duration(picos=3) == Duration(picos=12)
    assert 0 * Duration(picos=10) == Duration()

    t = sympy.Symbol('t')
    assert t * Duration(picos=3) == Duration(picos=3 * t)
    assert 0 * Duration(picos=t) == Duration(picos=0)

    with pytest.raises(TypeError):
        _ = Duration() * Duration()


def test_div():
    assert Duration(picos=6) / 2 == Duration(picos=3)
    assert Duration(picos=6) / Duration(picos=2) == 3
    with pytest.raises(TypeError):
        _ = 4 / Duration(picos=3)


def test_json_dict():
    d = Duration(picos=6)
    assert d._json_dict_() == {'picos': 6}


def test_str():
    assert str(Duration(picos=-2)) == '-2 ps'
    assert str(Duration()) == 'Duration(0)'
    assert str(Duration(picos=2)) == '2 ps'
    assert str(Duration(nanos=2)) == '2 ns'
    assert str(Duration(micros=2)) == '2 us'
    assert str(Duration(millis=2)) == '2 ms'
    assert str(Duration(micros=1.5)) == '1500.0 ns'
    assert str(Duration(micros=1.5 * sympy.Symbol('t'))) == '(1500.0*t) ns'


def test_repr_preserves_type_information():
    t = sympy.Symbol('t')

    assert repr(qubitron.Duration(micros=1500)) == 'qubitron.Duration(micros=1500)'
    assert repr(qubitron.Duration(micros=1500.0)) == 'qubitron.Duration(micros=1500.0)'
    assert repr(qubitron.Duration(millis=1.5)) == 'qubitron.Duration(micros=1500.0)'

    assert repr(qubitron.Duration(micros=1500 * t)) == (
        "qubitron.Duration(micros=sympy.Mul(sympy.Integer(1500), sympy.Symbol('t')))"
    )
    assert repr(qubitron.Duration(micros=1500.0 * t)) == (
        "qubitron.Duration(micros=sympy.Mul(sympy.Float('1500.0', precision=53), sympy.Symbol('t')))"
    )
    assert repr(qubitron.Duration(millis=1.5 * t)) == (
        "qubitron.Duration(micros=sympy.Mul(sympy.Float('1500.0', precision=53), sympy.Symbol('t')))"
    )
