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
import pytest

import qubitron
from qubitron.devices.grid_qubit_test import _test_qid_pickled_hash


def test_init():
    q = qubitron.LineQubit(1)
    assert q.x == 1

    q = qubitron.LineQid(1, dimension=3)
    assert q.x == 1
    assert q.dimension == 3


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(lambda: qubitron.LineQubit(1), lambda: qubitron.LineQid(1, dimension=2))
    eq.add_equality_group(qubitron.LineQubit(2))
    eq.add_equality_group(qubitron.LineQubit(0))
    eq.add_equality_group(qubitron.LineQid(1, dimension=3))


def test_str():
    assert str(qubitron.LineQubit(5)) == 'q(5)'
    assert str(qubitron.LineQid(5, dimension=3)) == 'q(5) (d=3)'


def test_repr():
    qubitron.testing.assert_equivalent_repr(qubitron.LineQubit(5))
    qubitron.testing.assert_equivalent_repr(qubitron.LineQid(5, dimension=3))


def test_cmp():
    order = qubitron.testing.OrderTester()
    order.add_ascending_equivalence_group(qubitron.LineQubit(0), qubitron.LineQid(0, 2))
    order.add_ascending(
        qubitron.LineQid(0, dimension=3),
        qubitron.LineQid(1, dimension=1),
        qubitron.LineQubit(1),
        qubitron.LineQid(1, dimension=3),
        qubitron.LineQid(2, dimension=1),
    )


def test_cmp_failure():
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < qubitron.LineQubit(1)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = qubitron.LineQubit(1) < 0
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < qubitron.LineQid(1, 3)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = qubitron.LineQid(1, 3) < 0


def test_line_qubit_pickled_hash():
    # Use a large number that is unlikely to be used by any other tests.
    x = 1234567891011
    q_bad = qubitron.LineQubit(x)
    qubitron.LineQubit._cache.pop(x)
    q = qubitron.LineQubit(x)
    _test_qid_pickled_hash(q, q_bad)


def test_line_qid_pickled_hash():
    # Use a large number that is unlikely to be used by any other tests.
    x = 1234567891011
    q_bad = qubitron.LineQid(x, dimension=3)
    qubitron.LineQid._cache.pop((x, 3))
    q = qubitron.LineQid(x, dimension=3)
    _test_qid_pickled_hash(q, q_bad)


def test_is_adjacent():
    assert qubitron.LineQubit(1).is_adjacent(qubitron.LineQubit(2))
    assert qubitron.LineQubit(1).is_adjacent(qubitron.LineQubit(0))
    assert qubitron.LineQubit(2).is_adjacent(qubitron.LineQubit(3))
    assert not qubitron.LineQubit(1).is_adjacent(qubitron.LineQubit(3))
    assert not qubitron.LineQubit(2).is_adjacent(qubitron.LineQubit(0))

    assert qubitron.LineQubit(2).is_adjacent(qubitron.LineQid(3, 3))
    assert not qubitron.LineQubit(2).is_adjacent(qubitron.LineQid(0, 3))


def test_neighborhood():
    assert qubitron.LineQubit(1).neighbors() == {qubitron.LineQubit(0), qubitron.LineQubit(2)}
    restricted_qubits = [qubitron.LineQubit(2), qubitron.LineQubit(3)]
    assert qubitron.LineQubit(1).neighbors(restricted_qubits) == {qubitron.LineQubit(2)}


def test_range():
    assert qubitron.LineQubit.range(0) == []
    assert qubitron.LineQubit.range(1) == [qubitron.LineQubit(0)]
    assert qubitron.LineQubit.range(2) == [qubitron.LineQubit(0), qubitron.LineQubit(1)]
    assert qubitron.LineQubit.range(5) == [
        qubitron.LineQubit(0),
        qubitron.LineQubit(1),
        qubitron.LineQubit(2),
        qubitron.LineQubit(3),
        qubitron.LineQubit(4),
    ]

    assert qubitron.LineQubit.range(0, 0) == []
    assert qubitron.LineQubit.range(0, 1) == [qubitron.LineQubit(0)]
    assert qubitron.LineQubit.range(1, 4) == [qubitron.LineQubit(1), qubitron.LineQubit(2), qubitron.LineQubit(3)]

    assert qubitron.LineQubit.range(3, 1, -1) == [qubitron.LineQubit(3), qubitron.LineQubit(2)]
    assert qubitron.LineQubit.range(3, 5, -1) == []
    assert qubitron.LineQubit.range(1, 5, 2) == [qubitron.LineQubit(1), qubitron.LineQubit(3)]


def test_qid_range():
    assert qubitron.LineQid.range(0, dimension=3) == []
    assert qubitron.LineQid.range(1, dimension=3) == [qubitron.LineQid(0, 3)]
    assert qubitron.LineQid.range(2, dimension=3) == [qubitron.LineQid(0, 3), qubitron.LineQid(1, 3)]
    assert qubitron.LineQid.range(5, dimension=3) == [
        qubitron.LineQid(0, 3),
        qubitron.LineQid(1, 3),
        qubitron.LineQid(2, 3),
        qubitron.LineQid(3, 3),
        qubitron.LineQid(4, 3),
    ]

    assert qubitron.LineQid.range(0, 0, dimension=4) == []
    assert qubitron.LineQid.range(0, 1, dimension=4) == [qubitron.LineQid(0, 4)]
    assert qubitron.LineQid.range(1, 4, dimension=4) == [
        qubitron.LineQid(1, 4),
        qubitron.LineQid(2, 4),
        qubitron.LineQid(3, 4),
    ]

    assert qubitron.LineQid.range(3, 1, -1, dimension=1) == [qubitron.LineQid(3, 1), qubitron.LineQid(2, 1)]
    assert qubitron.LineQid.range(3, 5, -1, dimension=2) == []
    assert qubitron.LineQid.range(1, 5, 2, dimension=2) == [qubitron.LineQid(1, 2), qubitron.LineQid(3, 2)]


def test_for_qid_shape():
    assert qubitron.LineQid.for_qid_shape(()) == []
    assert qubitron.LineQid.for_qid_shape((4, 2, 3, 1)) == [
        qubitron.LineQid(0, 4),
        qubitron.LineQid(1, 2),
        qubitron.LineQid(2, 3),
        qubitron.LineQid(3, 1),
    ]
    assert qubitron.LineQid.for_qid_shape((4, 2, 3, 1), start=5) == [
        qubitron.LineQid(5, 4),
        qubitron.LineQid(6, 2),
        qubitron.LineQid(7, 3),
        qubitron.LineQid(8, 1),
    ]
    assert qubitron.LineQid.for_qid_shape((4, 2, 3, 1), step=2) == [
        qubitron.LineQid(0, 4),
        qubitron.LineQid(2, 2),
        qubitron.LineQid(4, 3),
        qubitron.LineQid(6, 1),
    ]
    assert qubitron.LineQid.for_qid_shape((4, 2, 3, 1), start=5, step=-1) == [
        qubitron.LineQid(5, 4),
        qubitron.LineQid(4, 2),
        qubitron.LineQid(3, 3),
        qubitron.LineQid(2, 1),
    ]


def test_addition_subtraction():
    assert qubitron.LineQubit(1) + 2 == qubitron.LineQubit(3)
    assert qubitron.LineQubit(3) - 1 == qubitron.LineQubit(2)
    assert 1 + qubitron.LineQubit(4) == qubitron.LineQubit(5)
    assert 5 - qubitron.LineQubit(3) == qubitron.LineQubit(2)

    assert qubitron.LineQid(1, 3) + 2 == qubitron.LineQid(3, 3)
    assert qubitron.LineQid(3, 3) - 1 == qubitron.LineQid(2, 3)
    assert 1 + qubitron.LineQid(4, 3) == qubitron.LineQid(5, 3)
    assert 5 - qubitron.LineQid(3, 3) == qubitron.LineQid(2, 3)

    assert qubitron.LineQid(1, dimension=3) + qubitron.LineQid(3, dimension=3) == qubitron.LineQid(
        4, dimension=3
    )
    assert qubitron.LineQid(3, dimension=3) - qubitron.LineQid(2, dimension=3) == qubitron.LineQid(
        1, dimension=3
    )


def test_addition_subtraction_type_error():
    with pytest.raises(TypeError, match='dave'):
        _ = qubitron.LineQubit(1) + 'dave'
    with pytest.raises(TypeError, match='dave'):
        _ = qubitron.LineQubit(1) - 'dave'

    with pytest.raises(TypeError, match='dave'):
        _ = qubitron.LineQid(1, 3) + 'dave'
    with pytest.raises(TypeError, match='dave'):
        _ = qubitron.LineQid(1, 3) - 'dave'

    with pytest.raises(TypeError, match="Can only add LineQids with identical dimension."):
        _ = qubitron.LineQid(5, dimension=3) + qubitron.LineQid(3, dimension=4)

    with pytest.raises(TypeError, match="Can only subtract LineQids with identical dimension."):
        _ = qubitron.LineQid(5, dimension=3) - qubitron.LineQid(3, dimension=4)


def test_neg():
    assert -qubitron.LineQubit(1) == qubitron.LineQubit(-1)
    assert -qubitron.LineQid(1, dimension=3) == qubitron.LineQid(-1, dimension=3)


def test_json_dict():
    assert qubitron.LineQubit(5)._json_dict_() == {'x': 5}
    assert qubitron.LineQid(5, 3)._json_dict_() == {'x': 5, 'dimension': 3}


def test_for_gate():
    class NoQidGate:
        def _qid_shape_(self):
            return ()

    class QuditGate:
        def _qid_shape_(self):
            return (4, 2, 3, 1)

    assert qubitron.LineQid.for_gate(NoQidGate()) == []
    assert qubitron.LineQid.for_gate(QuditGate()) == [
        qubitron.LineQid(0, 4),
        qubitron.LineQid(1, 2),
        qubitron.LineQid(2, 3),
        qubitron.LineQid(3, 1),
    ]
    assert qubitron.LineQid.for_gate(QuditGate(), start=5) == [
        qubitron.LineQid(5, 4),
        qubitron.LineQid(6, 2),
        qubitron.LineQid(7, 3),
        qubitron.LineQid(8, 1),
    ]
    assert qubitron.LineQid.for_gate(QuditGate(), step=2) == [
        qubitron.LineQid(0, 4),
        qubitron.LineQid(2, 2),
        qubitron.LineQid(4, 3),
        qubitron.LineQid(6, 1),
    ]
    assert qubitron.LineQid.for_gate(QuditGate(), start=5, step=-1) == [
        qubitron.LineQid(5, 4),
        qubitron.LineQid(4, 2),
        qubitron.LineQid(3, 3),
        qubitron.LineQid(2, 1),
    ]


def test_immutable():
    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'x' of 'LineQubit' object has no setter)",
    ):
        q = qubitron.LineQubit(5)
        q.x = 6

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'x' of 'LineQid' object has no setter)",
    ):
        q = qubitron.LineQid(5, dimension=4)
        q.x = 6


def test_numeric():
    assert int(qubitron.LineQubit(x=5)) == 5
    assert float(qubitron.LineQubit(x=5)) == 5
    assert complex(qubitron.LineQubit(x=5)) == 5 + 0j
    assert isinstance(int(qubitron.LineQubit(x=5)), int)
    assert isinstance(float(qubitron.LineQubit(x=5)), float)
    assert isinstance(complex(qubitron.LineQubit(x=5)), complex)


@pytest.mark.parametrize('dtype', (np.int8, np.int64, float, np.float64))
def test_numpy_index(dtype):
    np5 = dtype(5)
    q = qubitron.LineQubit(np5)
    assert hash(q) == 5
    assert q.x == 5
    assert q.dimension == 2
    assert isinstance(q.dimension, int)

    q = qubitron.LineQid(np5, dtype(3))
    hash(q)  # doesn't throw
    assert q.x == 5
    assert q.dimension == 3
    assert isinstance(q.dimension, int)


@pytest.mark.parametrize('dtype', (float, np.float64))
def test_non_integer_index(dtype):
    # Not supported type-wise, but is used in practice, so behavior needs to be preserved.
    q = qubitron.LineQubit(dtype(5.5))
    assert q.x == 5.5
    assert q.x == dtype(5.5)
    assert isinstance(q.x, dtype)
