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

from typing import Collection, Sequence, TYPE_CHECKING

import numpy as np
import pytest

import qubitron

if TYPE_CHECKING:
    from qubitron.ops import control_values as cv


class GoodGate(qubitron.EigenGate, qubitron.testing.SingleQubitGate):
    def _eigen_components(self) -> list[tuple[float, np.ndarray]]:  # pragma: no cover
        return [(0, np.diag([1, 0])), (1, np.diag([0, 1]))]


class BadGateOperation(qubitron.GateOperation):
    def controlled_by(
        self,
        *control_qubits: qubitron.Qid,
        control_values: cv.AbstractControlValues | Sequence[int | Collection[int]] | None = None,
    ) -> qubitron.Operation:
        return qubitron.ControlledOperation(control_qubits, self, control_values)


class BadGate(qubitron.EigenGate, qubitron.testing.SingleQubitGate):
    def _eigen_components(self) -> list[tuple[float, np.ndarray]]:
        return [(0, np.diag([1, 0])), (1, np.diag([0, 1]))]

    def on(self, *qubits: qubitron.Qid) -> qubitron.Operation:
        return BadGateOperation(self, list(qubits))

    def controlled(
        self,
        num_controls: int | None = None,
        control_values: cv.AbstractControlValues | Sequence[int | Collection[int]] | None = None,
        control_qid_shape: tuple[int, ...] | None = None,
    ) -> qubitron.Gate:
        ret = super().controlled(num_controls, control_values, control_qid_shape)
        if num_controls == 1 and control_values is None:
            return qubitron.CZPowGate(exponent=self._exponent, global_shift=self._global_shift)
        return ret


def test_assert_controlled_and_controlled_by_identical() -> None:
    qubitron.testing.assert_controlled_and_controlled_by_identical(GoodGate())

    with pytest.raises(AssertionError):
        qubitron.testing.assert_controlled_and_controlled_by_identical(BadGate())

    with pytest.raises(ValueError, match=r'len\(num_controls\) != len\(control_values\)'):
        qubitron.testing.assert_controlled_and_controlled_by_identical(
            GoodGate(), num_controls=[1, 2], control_values=[(1,)]
        )

    with pytest.raises(ValueError, match=r'len\(control_values\[1\]\) != num_controls\[1\]'):
        qubitron.testing.assert_controlled_and_controlled_by_identical(
            GoodGate(), num_controls=[1, 2], control_values=[(1,), (1, 1, 1)]
        )


def test_assert_controlled_unitary_consistent() -> None:
    qubitron.testing.assert_controlled_and_controlled_by_identical(
        GoodGate(exponent=0.5, global_shift=1 / 3)
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_controlled_and_controlled_by_identical(
            BadGate(exponent=0.5, global_shift=1 / 3)
        )
