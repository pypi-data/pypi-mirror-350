# Copyright 2022 The Qubitron Developers
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


def test_assert_consistent_channel_valid() -> None:
    channel = qubitron.KrausChannel(kraus_ops=(np.array([[0, 1], [0, 0]]), np.array([[1, 0], [0, 0]])))
    qubitron.testing.assert_consistent_channel(channel)


def test_assert_consistent_channel_tolerances() -> None:
    # This channel is off by 1e-5 from the identity matrix in the consistency condition.
    channel = qubitron.KrausChannel(
        kraus_ops=(np.array([[0, np.sqrt(1 - 1e-5)], [0, 0]]), np.array([[1, 0], [0, 0]]))
    )
    # We are comparing to identity, so rtol is same as atol for non-zero entries.
    qubitron.testing.assert_consistent_channel(channel, rtol=1e-5, atol=0)
    with pytest.raises(AssertionError):
        qubitron.testing.assert_consistent_channel(channel, rtol=1e-6, atol=0)
    qubitron.testing.assert_consistent_channel(channel, rtol=0, atol=1e-5)
    with pytest.raises(AssertionError):
        qubitron.testing.assert_consistent_channel(channel, rtol=0, atol=1e-6)


def test_assert_consistent_channel_invalid() -> None:
    channel = qubitron.KrausChannel(kraus_ops=(np.array([[1, 1], [0, 0]]), np.array([[1, 0], [0, 0]])))
    with pytest.raises(AssertionError, match=r"qubitron.KrausChannel.*2 1"):
        qubitron.testing.assert_consistent_channel(channel)


def test_assert_consistent_channel_not_kraus() -> None:
    with pytest.raises(AssertionError, match="12.*has_kraus"):
        qubitron.testing.assert_consistent_channel(12)


def test_assert_consistent_mixture_valid() -> None:
    mixture = qubitron.X.with_probability(0.1)
    qubitron.testing.assert_consistent_mixture(mixture)


def test_assert_consistent_mixture_not_mixture() -> None:
    not_mixture = qubitron.amplitude_damp(0.1)
    with pytest.raises(AssertionError, match="has_mixture"):
        qubitron.testing.assert_consistent_mixture(not_mixture)


class _MixtureGate(qubitron.testing.SingleQubitGate):
    def __init__(self, p, q):
        self._p = p
        self._q = q
        super().__init__()

    def _mixture_(self):
        return (self._p, qubitron.unitary(qubitron.I)), (self._q, qubitron.unitary(qubitron.X))


def test_assert_consistent_mixture_not_normalized() -> None:
    mixture = _MixtureGate(0.1, 0.85)
    with pytest.raises(AssertionError, match="sum to 1"):
        qubitron.testing.assert_consistent_mixture(mixture)

    mixture = _MixtureGate(0.2, 0.85)
    with pytest.raises(AssertionError, match="sum to 1"):
        qubitron.testing.assert_consistent_mixture(mixture)


def test_assert_consistent_mixture_tolerances() -> None:

    # This gate is 1e-5 off being properly normalized.
    mixture = _MixtureGate(0.1, 0.9 - 1e-5)
    # Defaults of rtol=1e-5, atol=1e-8 are fine.
    qubitron.testing.assert_consistent_mixture(mixture)

    with pytest.raises(AssertionError, match="sum to 1"):
        qubitron.testing.assert_consistent_mixture(mixture, rtol=0, atol=1e-6)

    with pytest.raises(AssertionError, match="sum to 1"):
        qubitron.testing.assert_consistent_mixture(mixture, rtol=1e-6, atol=0)
