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

import numpy as np
import pytest

import qubitron


def test_assert_specifies_has_unitary_if_unitary_from_matrix() -> None:
    class Bad:
        def _unitary_(self):
            return np.array([[1]])

    assert qubitron.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        qubitron.testing.assert_specifies_has_unitary_if_unitary(Bad())


def test_assert_specifies_has_unitary_if_unitary_from_apply() -> None:
    class Bad(qubitron.Operation):
        @property
        def qubits(self):
            return ()

        def with_qubits(self, *new_qubits):
            return self  # pragma: no cover

        def _apply_unitary_(self, args):
            return args.target_tensor

    assert qubitron.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        qubitron.testing.assert_specifies_has_unitary_if_unitary(Bad())


def test_assert_specifies_has_unitary_if_unitary_from_decompose() -> None:
    class Bad:
        def _decompose_(self):
            return []

    assert qubitron.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        qubitron.testing.assert_specifies_has_unitary_if_unitary(Bad())

    class Bad2:
        def _decompose_(self):
            return [qubitron.X(qubitron.LineQubit(0))]

    assert qubitron.has_unitary(Bad2())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        qubitron.testing.assert_specifies_has_unitary_if_unitary(Bad2())

    class Okay:
        def _decompose_(self):
            return [qubitron.depolarize(0.5).on(qubitron.LineQubit(0))]

    assert not qubitron.has_unitary(Okay())
    qubitron.testing.assert_specifies_has_unitary_if_unitary(Okay())


def test_assert_specifies_has_unitary_if_unitary_pass() -> None:
    class Good:
        def _has_unitary_(self):
            return True

    assert qubitron.has_unitary(Good())
    qubitron.testing.assert_specifies_has_unitary_if_unitary(Good())
