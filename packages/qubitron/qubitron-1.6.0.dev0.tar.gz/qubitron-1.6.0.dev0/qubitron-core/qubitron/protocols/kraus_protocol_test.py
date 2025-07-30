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

"""Tests for kraus_protocol.py."""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
import pytest

import qubitron

LOCAL_DEFAULT: list[np.ndarray] = [np.array([])]


def test_kraus_no_methods() -> None:
    class NoMethod:
        pass

    with pytest.raises(TypeError, match='no _kraus_ or _mixture_ or _unitary_ method'):
        _ = qubitron.kraus(NoMethod())

    assert qubitron.kraus(NoMethod(), None) is None
    assert qubitron.kraus(NoMethod, NotImplemented) is NotImplemented
    assert qubitron.kraus(NoMethod(), (1,)) == (1,)
    assert qubitron.kraus(NoMethod(), LOCAL_DEFAULT) is LOCAL_DEFAULT

    assert not qubitron.has_kraus(NoMethod())


def assert_not_implemented(val):
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = qubitron.kraus(val)

    assert qubitron.kraus(val, None) is None
    assert qubitron.kraus(val, NotImplemented) is NotImplemented
    assert qubitron.kraus(val, (1,)) == (1,)
    assert qubitron.kraus(val, LOCAL_DEFAULT) is LOCAL_DEFAULT

    assert not qubitron.has_kraus(val)


def test_kraus_returns_not_implemented() -> None:
    class ReturnsNotImplemented:
        def _kraus_(self):
            return NotImplemented

    assert_not_implemented(ReturnsNotImplemented())


def test_mixture_returns_not_implemented() -> None:
    class ReturnsNotImplemented:
        def _mixture_(self):
            return NotImplemented

    assert_not_implemented(ReturnsNotImplemented())


def test_unitary_returns_not_implemented() -> None:
    class ReturnsNotImplemented:
        def _unitary_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = qubitron.kraus(ReturnsNotImplemented())
    assert qubitron.kraus(ReturnsNotImplemented(), None) is None
    assert qubitron.kraus(ReturnsNotImplemented(), NotImplemented) is NotImplemented
    assert qubitron.kraus(ReturnsNotImplemented(), (1,)) == (1,)
    assert qubitron.kraus(ReturnsNotImplemented(), LOCAL_DEFAULT) is LOCAL_DEFAULT


def test_explicit_kraus() -> None:
    a0 = np.array([[0, 0], [1, 0]])
    a1 = np.array([[1, 0], [0, 0]])
    c = (a0, a1)

    class ReturnsKraus:
        def _kraus_(self) -> Sequence[np.ndarray]:
            return c

    assert qubitron.kraus(ReturnsKraus()) is c
    assert qubitron.kraus(ReturnsKraus(), None) is c
    assert qubitron.kraus(ReturnsKraus(), NotImplemented) is c
    assert qubitron.kraus(ReturnsKraus(), (1,)) is c
    assert qubitron.kraus(ReturnsKraus(), LOCAL_DEFAULT) is c

    assert qubitron.has_kraus(ReturnsKraus())


def test_kraus_fallback_to_mixture() -> None:
    m = ((0.3, qubitron.unitary(qubitron.X)), (0.4, qubitron.unitary(qubitron.Y)), (0.3, qubitron.unitary(qubitron.Z)))

    class ReturnsMixture:
        def _mixture_(self) -> Iterable[tuple[float, np.ndarray]]:
            return m

    c = (
        np.sqrt(0.3) * qubitron.unitary(qubitron.X),
        np.sqrt(0.4) * qubitron.unitary(qubitron.Y),
        np.sqrt(0.3) * qubitron.unitary(qubitron.Z),
    )

    np.testing.assert_equal(qubitron.kraus(ReturnsMixture()), c)
    np.testing.assert_equal(qubitron.kraus(ReturnsMixture(), None), c)
    np.testing.assert_equal(qubitron.kraus(ReturnsMixture(), NotImplemented), c)
    np.testing.assert_equal(qubitron.kraus(ReturnsMixture(), (1,)), c)
    np.testing.assert_equal(qubitron.kraus(ReturnsMixture(), LOCAL_DEFAULT), c)

    assert qubitron.has_kraus(ReturnsMixture())


def test_kraus_fallback_to_unitary() -> None:
    u = np.array([[1, 0], [1, 0]])

    class ReturnsUnitary:
        def _unitary_(self) -> np.ndarray:
            return u

    np.testing.assert_equal(qubitron.kraus(ReturnsUnitary()), (u,))
    np.testing.assert_equal(qubitron.kraus(ReturnsUnitary(), None), (u,))
    np.testing.assert_equal(qubitron.kraus(ReturnsUnitary(), NotImplemented), (u,))
    np.testing.assert_equal(qubitron.kraus(ReturnsUnitary(), (1,)), (u,))
    np.testing.assert_equal(qubitron.kraus(ReturnsUnitary(), LOCAL_DEFAULT), (u,))

    assert qubitron.has_kraus(ReturnsUnitary())


class HasKraus(qubitron.testing.SingleQubitGate):
    def _has_kraus_(self) -> bool:
        return True


class HasMixture(qubitron.testing.SingleQubitGate):
    def _has_mixture_(self) -> bool:
        return True


class HasUnitary(qubitron.testing.SingleQubitGate):
    def _has_unitary_(self) -> bool:
        return True


class HasKrausWhenDecomposed(qubitron.testing.SingleQubitGate):
    def __init__(self, decomposed_cls):
        self.decomposed_cls = decomposed_cls

    def _decompose_(self, qubits):
        return [self.decomposed_cls().on(q) for q in qubits]


@pytest.mark.parametrize('cls', [HasKraus, HasMixture, HasUnitary])
def test_has_kraus(cls) -> None:
    assert qubitron.has_kraus(cls())


@pytest.mark.parametrize('decomposed_cls', [HasKraus, HasMixture, HasUnitary])
def test_has_kraus_when_decomposed(decomposed_cls) -> None:
    op = HasKrausWhenDecomposed(decomposed_cls).on(qubitron.NamedQubit('test'))
    assert qubitron.has_kraus(op)
    assert not qubitron.has_kraus(op, allow_decompose=False)
