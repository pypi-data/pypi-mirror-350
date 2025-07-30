# Copyright 2021 The Qubitron Developers
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

import qubitron


def test_default():
    a2 = qubitron.NamedQubit('a2')
    a10 = qubitron.NamedQubit('a10')
    b = qubitron.NamedQubit('b')
    q4 = qubitron.LineQubit(4)
    q5 = qubitron.LineQubit(5)
    assert qubitron.QubitOrder.DEFAULT.order_for([]) == ()
    assert qubitron.QubitOrder.DEFAULT.order_for([a10, a2, b]) == (a2, a10, b)
    assert sorted([]) == []
    assert sorted([a10, a2, b]) == [a2, a10, b]
    assert sorted([q5, a10, a2, b, q4]) == [q4, q5, a2, a10, b]


def test_default_grouping():
    presorted = (
        qubitron.GridQubit(0, 1),
        qubitron.GridQubit(1, 0),
        qubitron.GridQubit(999, 999),
        qubitron.LineQubit(0),
        qubitron.LineQubit(1),
        qubitron.LineQubit(999),
        qubitron.NamedQubit(''),
        qubitron.NamedQubit('0'),
        qubitron.NamedQubit('1'),
        qubitron.NamedQubit('999'),
        qubitron.NamedQubit('a'),
    )
    assert qubitron.QubitOrder.DEFAULT.order_for(presorted) == presorted
    assert qubitron.QubitOrder.DEFAULT.order_for(reversed(presorted)) == presorted


def test_explicit():
    a2 = qubitron.NamedQubit('a2')
    a10 = qubitron.NamedQubit('a10')
    b = qubitron.NamedQubit('b')
    with pytest.raises(ValueError):
        _ = qubitron.QubitOrder.explicit([b, b])
    q = qubitron.QubitOrder.explicit([a10, a2, b])
    assert q.order_for([b]) == (a10, a2, b)
    assert q.order_for([a2]) == (a10, a2, b)
    assert q.order_for([]) == (a10, a2, b)
    with pytest.raises(ValueError):
        _ = q.order_for([qubitron.NamedQubit('c')])


def test_explicit_with_fallback():
    a2 = qubitron.NamedQubit('a2')
    a10 = qubitron.NamedQubit('a10')
    b = qubitron.NamedQubit('b')
    q = qubitron.QubitOrder.explicit([b], fallback=qubitron.QubitOrder.DEFAULT)
    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)
    assert q.order_for([b, a2]) == (b, a2)
    assert q.order_for([a2]) == (b, a2)
    assert q.order_for([a10, a2]) == (b, a2, a10)


def test_sorted_by():
    a = qubitron.NamedQubit('2')
    b = qubitron.NamedQubit('10')
    c = qubitron.NamedQubit('-5')

    q = qubitron.QubitOrder.sorted_by(lambda e: -int(str(e)))
    assert q.order_for([]) == ()
    assert q.order_for([a]) == (a,)
    assert q.order_for([a, b]) == (b, a)
    assert q.order_for([a, b, c]) == (b, a, c)


def test_map():
    b = qubitron.NamedQubit('b!')
    q = qubitron.QubitOrder.explicit([qubitron.NamedQubit('b')]).map(
        internalize=lambda e: qubitron.NamedQubit(e.name[:-1]),
        externalize=lambda e: qubitron.NamedQubit(e.name + '!'),
    )

    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)


def test_qubit_order_or_list():
    b = qubitron.NamedQubit('b')

    implied_by_list = qubitron.QubitOrder.as_qubit_order([b])
    assert implied_by_list.order_for([]) == (b,)

    implied_by_generator = qubitron.QubitOrder.as_qubit_order(
        qubitron.NamedQubit(e.name + '!') for e in [b]
    )
    assert implied_by_generator.order_for([]) == (qubitron.NamedQubit('b!'),)
    assert implied_by_generator.order_for([]) == (qubitron.NamedQubit('b!'),)

    ordered = qubitron.QubitOrder.sorted_by(repr)
    passed_through = qubitron.QubitOrder.as_qubit_order(ordered)
    assert ordered is passed_through


def test_qubit_order_iterator():
    generator = (q for q in qubitron.LineQubit.range(5))
    assert qubitron.QubitOrder.explicit(generator).order_for((qubitron.LineQubit(3),)) == tuple(
        qubitron.LineQubit.range(5)
    )

    generator = (q for q in qubitron.LineQubit.range(5))
    assert qubitron.QubitOrder.as_qubit_order(generator).order_for((qubitron.LineQubit(3),)) == tuple(
        qubitron.LineQubit.range(5)
    )


def test_qubit_order_invalid():
    with pytest.raises(ValueError, match="Don't know how to interpret <5> as a Basis."):
        _ = qubitron.QubitOrder.as_qubit_order(5)
