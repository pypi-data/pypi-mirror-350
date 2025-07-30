# Copyright 2019 The Qubitron Developers
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


class ReturnsStr:
    def _measurement_key_name_(self):
        return 'door locker'


class ReturnsObj:
    def _measurement_key_obj_(self):
        return qubitron.MeasurementKey(name='door locker')


@pytest.mark.parametrize('gate', [ReturnsStr(), ReturnsObj()])
def test_measurement_key_name(gate) -> None:
    assert isinstance(qubitron.measurement_key_name(gate), str)
    assert qubitron.measurement_key_name(gate) == 'door locker'
    assert qubitron.measurement_key_obj(gate) == qubitron.MeasurementKey(name='door locker')

    assert qubitron.measurement_key_name(gate, None) == 'door locker'
    assert qubitron.measurement_key_name(gate, NotImplemented) == 'door locker'
    assert qubitron.measurement_key_name(gate, 'a') == 'door locker'


@pytest.mark.parametrize('gate', [ReturnsStr(), ReturnsObj()])
def test_measurement_key_obj(gate) -> None:
    assert isinstance(qubitron.measurement_key_obj(gate), qubitron.MeasurementKey)
    assert qubitron.measurement_key_obj(gate) == qubitron.MeasurementKey(name='door locker')
    assert qubitron.measurement_key_obj(gate) == 'door locker'

    assert qubitron.measurement_key_obj(gate, None) == 'door locker'
    assert qubitron.measurement_key_obj(gate, NotImplemented) == 'door locker'
    assert qubitron.measurement_key_obj(gate, 'a') == 'door locker'


@pytest.mark.parametrize('key_method', [qubitron.measurement_key_name, qubitron.measurement_key_obj])
def test_measurement_key_no_method(key_method) -> None:
    class NoMethod:
        pass

    with pytest.raises(TypeError, match='no measurement keys'):
        key_method(NoMethod())

    with pytest.raises(ValueError, match='multiple measurement keys'):
        key_method(
            qubitron.Circuit(
                qubitron.measure(qubitron.LineQubit(0), key='a'), qubitron.measure(qubitron.LineQubit(0), key='b')
            )
        )

    assert key_method(NoMethod(), None) is None
    assert key_method(NoMethod(), NotImplemented) is NotImplemented
    assert key_method(NoMethod(), 'a') == 'a'

    assert key_method(qubitron.X, None) is None
    assert key_method(qubitron.X(qubitron.LineQubit(0)), None) is None


@pytest.mark.parametrize('key_method', [qubitron.measurement_key_name, qubitron.measurement_key_obj])
def test_measurement_key_not_implemented_default_behavior(key_method) -> None:
    class ReturnsNotImplemented:
        def _measurement_key_name_(self):
            return NotImplemented

        def _measurement_key_obj_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='NotImplemented'):
        key_method(ReturnsNotImplemented())

    assert key_method(ReturnsNotImplemented(), None) is None
    assert key_method(ReturnsNotImplemented(), NotImplemented) is NotImplemented
    assert key_method(ReturnsNotImplemented(), 'a') == 'a'


def test_is_measurement() -> None:
    q = qubitron.NamedQubit('q')
    assert qubitron.is_measurement(qubitron.measure(q))
    assert qubitron.is_measurement(qubitron.MeasurementGate(num_qubits=1, key='b'))

    assert not qubitron.is_measurement(qubitron.X(q))
    assert not qubitron.is_measurement(qubitron.X)
    assert not qubitron.is_measurement(qubitron.bit_flip(1))

    class NotImplementedOperation(qubitron.Operation):
        # pylint: disable=undefined-variable
        def with_qubits(self, *new_qubits) -> NotImplementedOperation:
            raise NotImplementedError()

        @property
        def qubits(self):
            return qubitron.LineQubit.range(2)  # pragma: no cover

    assert not qubitron.is_measurement(NotImplementedOperation())


def test_measurement_without_key() -> None:
    class MeasurementWithoutKey:
        def _is_measurement_(self):
            return True

    with pytest.raises(TypeError, match='no measurement keys'):
        _ = qubitron.measurement_key_name(MeasurementWithoutKey())

    assert qubitron.is_measurement(MeasurementWithoutKey())


def test_non_measurement_with_key() -> None:
    class NonMeasurementGate(qubitron.Gate):
        def _is_measurement_(self):
            return False  # pragma: no cover

        def _decompose_(self, qubits):
            # Decompose should not be called by `is_measurement`
            assert False  # pragma: no cover

        def _measurement_key_name_(self):
            # `measurement_key_name`` should not be called by `is_measurement`
            assert False  # pragma: no cover

        def _measurement_key_names_(self):
            # `measurement_key_names`` should not be called by `is_measurement`
            assert False  # pragma: no cover

        def _measurement_key_obj_(self):
            # `measurement_key_obj`` should not be called by `is_measurement`
            assert False  # pragma: no cover

        def _measurement_key_objs_(self):
            # `measurement_key_objs`` should not be called by `is_measurement`
            assert False  # pragma: no cover

        def num_qubits(self) -> int:
            return 2  # pragma: no cover

    assert not qubitron.is_measurement(NonMeasurementGate())


@pytest.mark.parametrize(
    ('key_method', 'keys'),
    [(qubitron.measurement_key_names, {'a', 'b'}), (qubitron.measurement_key_objs, {'c', 'd'})],
)
def test_measurement_keys(key_method, keys) -> None:
    class MeasurementKeysGate(qubitron.Gate):
        def _measurement_key_names_(self):
            return frozenset(['a', 'b'])

        def _measurement_key_objs_(self):
            return frozenset([qubitron.MeasurementKey('c'), qubitron.MeasurementKey('d')])

        def num_qubits(self) -> int:
            return 1

    a, b = qubitron.LineQubit.range(2)
    assert key_method(None) == set()
    assert key_method([]) == set()
    assert key_method(qubitron.X) == set()
    assert key_method(qubitron.X(a)) == set()
    assert key_method(qubitron.measure(a, key='out')) == {'out'}
    assert key_method(qubitron.Circuit(qubitron.measure(a, key='a'), qubitron.measure(b, key='2'))) == {
        'a',
        '2',
    }
    assert key_method(MeasurementKeysGate()) == keys
    assert key_method(MeasurementKeysGate().on(a)) == keys


def test_measurement_key_mapping() -> None:
    class MultiKeyGate:
        def __init__(self, keys):
            self._keys = frozenset(keys)

        def _measurement_key_names_(self):
            return self._keys

        def _with_measurement_key_mapping_(self, key_map):
            if not all(key in key_map for key in self._keys):
                raise ValueError('missing keys')
            return MultiKeyGate([key_map[key] for key in self._keys])

    assert qubitron.measurement_key_names(MultiKeyGate([])) == set()
    assert qubitron.measurement_key_names(MultiKeyGate(['a'])) == {'a'}

    mkg_ab = MultiKeyGate(['a', 'b'])
    assert qubitron.measurement_key_names(mkg_ab) == {'a', 'b'}

    mkg_cd = qubitron.with_measurement_key_mapping(mkg_ab, {'a': 'c', 'b': 'd'})
    assert qubitron.measurement_key_names(mkg_cd) == {'c', 'd'}

    mkg_ac = qubitron.with_measurement_key_mapping(mkg_ab, {'a': 'a', 'b': 'c'})
    assert qubitron.measurement_key_names(mkg_ac) == {'a', 'c'}

    mkg_ba = qubitron.with_measurement_key_mapping(mkg_ab, {'a': 'b', 'b': 'a'})
    assert qubitron.measurement_key_names(mkg_ba) == {'a', 'b'}

    with pytest.raises(ValueError):
        qubitron.with_measurement_key_mapping(mkg_ab, {'a': 'c'})

    assert qubitron.with_measurement_key_mapping(qubitron.X, {'a': 'c'}) is NotImplemented

    mkg_cdx = qubitron.with_measurement_key_mapping(mkg_ab, {'a': 'c', 'b': 'd', 'x': 'y'})
    assert qubitron.measurement_key_names(mkg_cdx) == {'c', 'd'}


def test_measurement_key_path() -> None:
    class MultiKeyGate:
        def __init__(self, keys):
            self._keys = frozenset(qubitron.MeasurementKey.parse_serialized(key) for key in keys)

        def _measurement_key_names_(self):
            return frozenset(str(key) for key in self._keys)

        def _with_key_path_(self, path):
            return MultiKeyGate([str(key._with_key_path_(path)) for key in self._keys])

    assert qubitron.measurement_key_names(MultiKeyGate([])) == set()
    assert qubitron.measurement_key_names(MultiKeyGate(['a'])) == {'a'}

    mkg_ab = MultiKeyGate(['a', 'b'])
    assert qubitron.measurement_key_names(mkg_ab) == {'a', 'b'}

    mkg_cd = qubitron.with_key_path(mkg_ab, ('c', 'd'))
    assert qubitron.measurement_key_names(mkg_cd) == {'c:d:a', 'c:d:b'}

    assert qubitron.with_key_path(qubitron.X, ('c', 'd')) is NotImplemented
