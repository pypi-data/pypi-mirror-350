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

import qubitron
from qubitron.devices.grid_qubit_test import _test_qid_pickled_hash
from qubitron.ops.named_qubit import _pad_digits


def test_init():
    q = qubitron.NamedQubit('a')
    assert q.name == 'a'

    q = qubitron.NamedQid('a', dimension=3)
    assert q.name == 'a'
    assert q.dimension == 3


def test_named_qubit_str():
    q = qubitron.NamedQubit('a')
    assert q.name == 'a'
    assert str(q) == 'a'
    qid = qubitron.NamedQid('a', dimension=3)
    assert qid.name == 'a'
    assert str(qid) == 'a (d=3)'


def test_named_qubit_repr():
    q = qubitron.NamedQubit('a')
    assert repr(q) == "qubitron.NamedQubit('a')"
    qid = qubitron.NamedQid('a', dimension=3)
    assert repr(qid) == "qubitron.NamedQid('a', dimension=3)"


def test_named_qubit_pickled_hash():
    # Use a name that is unlikely to be used by any other tests.
    x = "test_named_qubit_pickled_hash"
    q_bad = qubitron.NamedQubit(x)
    qubitron.NamedQubit._cache.pop(x)
    q = qubitron.NamedQubit(x)
    _test_qid_pickled_hash(q, q_bad)


def test_named_qid_pickled_hash():
    # Use a name that is unlikely to be used by any other tests.
    x = "test_named_qid_pickled_hash"
    q_bad = qubitron.NamedQid(x, dimension=3)
    qubitron.NamedQid._cache.pop((x, 3))
    q = qubitron.NamedQid(x, dimension=3)
    _test_qid_pickled_hash(q, q_bad)


def test_named_qubit_order():
    order = qubitron.testing.OrderTester()
    order.add_ascending(
        qubitron.NamedQid('', dimension=1),
        qubitron.NamedQubit(''),
        qubitron.NamedQid('', dimension=3),
        qubitron.NamedQid('1', dimension=1),
        qubitron.NamedQubit('1'),
        qubitron.NamedQid('1', dimension=3),
        qubitron.NamedQid('a', dimension=1),
        qubitron.NamedQubit('a'),
        qubitron.NamedQid('a', dimension=3),
        qubitron.NamedQid('a00000000', dimension=1),
        qubitron.NamedQubit('a00000000'),
        qubitron.NamedQid('a00000000', dimension=3),
        qubitron.NamedQid('a00000000:8', dimension=1),
        qubitron.NamedQubit('a00000000:8'),
        qubitron.NamedQid('a00000000:8', dimension=3),
        qubitron.NamedQid('a9', dimension=1),
        qubitron.NamedQubit('a9'),
        qubitron.NamedQid('a9', dimension=3),
        qubitron.NamedQid('a09', dimension=1),
        qubitron.NamedQubit('a09'),
        qubitron.NamedQid('a09', dimension=3),
        qubitron.NamedQid('a10', dimension=1),
        qubitron.NamedQubit('a10'),
        qubitron.NamedQid('a10', dimension=3),
        qubitron.NamedQid('a11', dimension=1),
        qubitron.NamedQubit('a11'),
        qubitron.NamedQid('a11', dimension=3),
        qubitron.NamedQid('aa', dimension=1),
        qubitron.NamedQubit('aa'),
        qubitron.NamedQid('aa', dimension=3),
        qubitron.NamedQid('ab', dimension=1),
        qubitron.NamedQubit('ab'),
        qubitron.NamedQid('ab', dimension=3),
        qubitron.NamedQid('b', dimension=1),
        qubitron.NamedQubit('b'),
        qubitron.NamedQid('b', dimension=3),
    )
    order.add_ascending_equivalence_group(
        qubitron.NamedQubit('c'),
        qubitron.NamedQubit('c'),
        qubitron.NamedQid('c', dimension=2),
        qubitron.NamedQid('c', dimension=2),
    )


def test_pad_digits():
    assert _pad_digits('') == ''
    assert _pad_digits('a') == 'a'
    assert _pad_digits('a0') == 'a00000000:1'
    assert _pad_digits('a00') == 'a00000000:2'
    assert _pad_digits('a1bc23') == 'a00000001:1bc00000023:2'
    assert _pad_digits('a9') == 'a00000009:1'
    assert _pad_digits('a09') == 'a00000009:2'
    assert _pad_digits('a00000000:8') == 'a00000000:8:00000008:1'


def test_named_qubit_range():
    qubits = qubitron.NamedQubit.range(2, prefix='a')
    assert qubits == [qubitron.NamedQubit('a0'), qubitron.NamedQubit('a1')]

    qubits = qubitron.NamedQubit.range(-1, 4, 2, prefix='a')
    assert qubits == [qubitron.NamedQubit('a-1'), qubitron.NamedQubit('a1'), qubitron.NamedQubit('a3')]


def test_named_qid_range():
    qids = qubitron.NamedQid.range(2, prefix='a', dimension=3)
    assert qids == [qubitron.NamedQid('a0', dimension=3), qubitron.NamedQid('a1', dimension=3)]

    qids = qubitron.NamedQid.range(-1, 4, 2, prefix='a', dimension=3)
    assert qids == [
        qubitron.NamedQid('a-1', dimension=3),
        qubitron.NamedQid('a1', dimension=3),
        qubitron.NamedQid('a3', dimension=3),
    ]

    qids = qubitron.NamedQid.range(2, prefix='a', dimension=4)
    assert qids == [qubitron.NamedQid('a0', dimension=4), qubitron.NamedQid('a1', dimension=4)]

    qids = qubitron.NamedQid.range(-1, 4, 2, prefix='a', dimension=4)
    assert qids == [
        qubitron.NamedQid('a-1', dimension=4),
        qubitron.NamedQid('a1', dimension=4),
        qubitron.NamedQid('a3', dimension=4),
    ]


def test_to_json():
    assert qubitron.NamedQubit('c')._json_dict_() == {'name': 'c'}

    assert qubitron.NamedQid('c', dimension=3)._json_dict_() == {'name': 'c', 'dimension': 3}
