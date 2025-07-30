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

import qubitron


class No:
    pass


class No1:
    def _has_stabilizer_effect_(self):
        return NotImplemented


class No2:
    def _has_stabilizer_effect_(self):
        return None


class No3:
    def _has_stabilizer_effect_(self):
        return False


class Yes:
    def _has_stabilizer_effect_(self):
        return True


class EmptyOp(qubitron.Operation):
    """A trivial operation."""

    def __init__(self, q: qubitron.Qid = qubitron.LineQubit(0)):
        self.q = q

    @property
    def qubits(self):
        return (self.q,)

    def with_qubits(self, *new_qubits):  # pragma: no cover
        return self


class NoOp(EmptyOp):
    @property
    def gate(self):
        return No()


class NoOp1(EmptyOp):
    @property
    def gate(self):
        return No1()


class NoOp2(EmptyOp):
    @property
    def gate(self):
        return No2()


class NoOp3(EmptyOp):
    @property
    def gate(self):
        return No3()


class YesOp(EmptyOp):
    @property
    def gate(self):
        return Yes()


class OpWithUnitary(EmptyOp):
    def __init__(self, unitary):
        self.unitary = unitary

    def _unitary_(self):
        return self.unitary

    @property
    def qubits(self):
        return qubitron.LineQubit.range(self.unitary.shape[0].bit_length() - 1)


class GateDecomposes(qubitron.Gate):
    def _num_qubits_(self):
        return 1

    def _decompose_(self, qubits):
        yield YesOp(*qubits)


def test_inconclusive() -> None:
    assert not qubitron.has_stabilizer_effect(object())
    assert not qubitron.has_stabilizer_effect('boo')
    assert not qubitron.has_stabilizer_effect(qubitron.testing.SingleQubitGate())
    assert not qubitron.has_stabilizer_effect(No())
    assert not qubitron.has_stabilizer_effect(NoOp())


def test_via_has_stabilizer_effect_method() -> None:
    assert not qubitron.has_stabilizer_effect(No1())
    assert not qubitron.has_stabilizer_effect(No2())
    assert not qubitron.has_stabilizer_effect(No3())
    assert qubitron.has_stabilizer_effect(Yes())


def test_via_gate_of_op() -> None:
    assert qubitron.has_stabilizer_effect(YesOp())
    assert not qubitron.has_stabilizer_effect(NoOp1())
    assert not qubitron.has_stabilizer_effect(NoOp2())
    assert not qubitron.has_stabilizer_effect(NoOp3())


def test_via_unitary() -> None:
    op1 = OpWithUnitary(np.array([[0, 1], [1, 0]]))
    assert qubitron.has_stabilizer_effect(op1)

    op2 = OpWithUnitary(np.array([[0, 1j], [1j, 0]]))
    assert qubitron.has_stabilizer_effect(op2)

    op3 = OpWithUnitary(np.array([[1, 0], [0, np.sqrt(1j)]]))
    assert not qubitron.has_stabilizer_effect(op3)

    # 2+ qubit cliffords
    assert qubitron.has_stabilizer_effect(qubitron.CNOT)
    assert qubitron.has_stabilizer_effect(qubitron.XX)
    assert qubitron.has_stabilizer_effect(qubitron.ZZ)

    # Non Cliffords
    assert not qubitron.has_stabilizer_effect(qubitron.T)
    assert not qubitron.has_stabilizer_effect(qubitron.CCNOT)
    assert not qubitron.has_stabilizer_effect(qubitron.CCZ)


def test_via_decompose() -> None:
    assert qubitron.has_stabilizer_effect(qubitron.Circuit(qubitron.H.on_each(qubitron.LineQubit.range(4))))
    assert not qubitron.has_stabilizer_effect(qubitron.Circuit(qubitron.T.on_each(qubitron.LineQubit.range(4))))
    assert not qubitron.has_stabilizer_effect(
        OpWithUnitary(qubitron.unitary(qubitron.Circuit(qubitron.T.on_each(qubitron.LineQubit.range(4)))))
    )
    assert qubitron.has_stabilizer_effect(GateDecomposes())
