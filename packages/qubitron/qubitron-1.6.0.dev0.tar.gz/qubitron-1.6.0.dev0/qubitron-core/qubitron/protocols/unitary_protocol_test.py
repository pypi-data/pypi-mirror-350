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
from qubitron import testing

m0: np.ndarray = np.array([])
# yapf: disable
# X on one qubit
m1 = np.array([[0, 1],
               [1, 0]])
# X on two qubits
m2 = np.array([[0, 0, 0, 1],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [1, 0, 0, 0]])
# X on qubit 1 and 3
m3 = np.array([[0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 1, 0],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0]])
# yapf: enable
a = qubitron.NamedQubit('a')
b = qubitron.NamedQubit('b')
c = qubitron.NamedQubit('c')


class NoMethod:
    pass


class ReturnsNotImplemented(qubitron.Gate):
    def _has_unitary_(self):
        return NotImplemented

    def _unitary_(self):
        return NotImplemented

    def num_qubits(self):
        return 1


class ReturnsMatrix(qubitron.Gate):
    def _unitary_(self) -> np.ndarray:
        return m1

    def num_qubits(self):
        return 1  # pragma: no cover


class FullyImplemented(qubitron.Gate):
    def __init__(self, unitary_value):
        self.unitary_value = unitary_value

    def _has_unitary_(self) -> bool:
        return self.unitary_value

    def _unitary_(self) -> np.ndarray | None:
        if not self.unitary_value:
            return None
        return m1

    def num_qubits(self):
        return 1


class DecomposableGate(qubitron.Gate):
    def __init__(self, unitary_value):
        self.unitary_value = unitary_value

    def num_qubits(self):
        return 1

    def _decompose_(self, qubits):
        yield FullyImplemented(self.unitary_value).on(qubits[0])


class DecomposableOperation(qubitron.Operation):
    qubits = ()
    with_qubits = NotImplemented

    def __init__(self, qubits, unitary_value):
        self.qubits = qubits
        self.unitary_value = unitary_value

    def _decompose_(self):
        for q in self.qubits:
            yield FullyImplemented(self.unitary_value)(q)


class DecomposableOrder(qubitron.Operation):
    qubits = ()
    with_qubits = NotImplemented

    def __init__(self, qubits):
        self.qubits = qubits

    def _decompose_(self):
        yield FullyImplemented(True)(self.qubits[2])
        yield FullyImplemented(True)(self.qubits[0])


class DecomposableNoUnitary(qubitron.Operation):
    qubits = ()
    with_qubits = NotImplemented

    def __init__(self, qubits):
        self.qubits = qubits

    def _decompose_(self):
        for q in self.qubits:
            yield ReturnsNotImplemented()(q)


class ExampleOperation(qubitron.Operation):
    qubits = ()
    with_qubits = NotImplemented

    def __init__(self, qubits):
        self.qubits = qubits

    def _decompose_(self):
        return ()


class ExampleComposite:
    def _decompose_(self):
        return ()


class OtherComposite:
    def _decompose_(self):
        yield qubitron.X(qubitron.LineQubit(0))
        yield qubitron.X(qubitron.LineQubit(3))


def test_unitary():
    with pytest.raises(TypeError, match='unitary effect'):
        _ = qubitron.unitary(NoMethod())
    with pytest.raises(TypeError, match='unitary effect'):
        _ = qubitron.unitary(ReturnsNotImplemented())
    assert qubitron.unitary(ReturnsMatrix()) is m1

    assert qubitron.unitary(NoMethod(), None) is None
    assert qubitron.unitary(ReturnsNotImplemented(), None) is None
    assert qubitron.unitary(ReturnsMatrix(), None) is m1

    assert qubitron.unitary(NoMethod(), NotImplemented) is NotImplemented
    assert qubitron.unitary(ReturnsNotImplemented(), NotImplemented) is NotImplemented
    assert qubitron.unitary(ReturnsMatrix(), NotImplemented) is m1

    assert qubitron.unitary(NoMethod(), 1) == 1
    assert qubitron.unitary(ReturnsNotImplemented(), 1) == 1
    assert qubitron.unitary(ReturnsMatrix(), 1) is m1

    assert qubitron.unitary(NoMethod(), m0) is m0
    assert qubitron.unitary(ReturnsNotImplemented(), m0) is m0
    assert qubitron.unitary(ReturnsMatrix(), m0) is m1
    assert qubitron.unitary(FullyImplemented(True), m0) is m1
    assert qubitron.unitary(FullyImplemented(False), default=None) is None


def test_has_unitary():
    assert not qubitron.has_unitary(NoMethod())
    assert not qubitron.has_unitary(ReturnsNotImplemented())
    assert qubitron.has_unitary(ReturnsMatrix())

    # Explicit function should override
    assert qubitron.has_unitary(FullyImplemented(True))
    assert not qubitron.has_unitary(FullyImplemented(False))


def _test_gate_that_allocates_qubits(gate):
    from qubitron.protocols.unitary_protocol import _strat_unitary_from_decompose

    op = gate.on(*qubitron.LineQubit.range(qubitron.num_qubits(gate)))
    moment = qubitron.Moment(op)
    circuit = qubitron.FrozenCircuit(op)
    circuit_op = qubitron.CircuitOperation(circuit)
    for val in [gate, op, moment, circuit, circuit_op]:
        unitary_from_strat = _strat_unitary_from_decompose(val)
        assert unitary_from_strat is not None
        np.testing.assert_allclose(unitary_from_strat, gate.narrow_unitary())


@pytest.mark.parametrize('theta', np.linspace(0, 2 * np.pi, 10))
@pytest.mark.parametrize('phase_state', [0, 1])
@pytest.mark.parametrize('target_bitsize', [1, 2, 3])
@pytest.mark.parametrize('ancilla_bitsize', [1, 4])
def test_decompose_gate_that_allocates_clean_qubits(
    theta: float, phase_state: int, target_bitsize: int, ancilla_bitsize: int
):
    gate = testing.PhaseUsingCleanAncilla(theta, phase_state, target_bitsize, ancilla_bitsize)
    _test_gate_that_allocates_qubits(gate)


@pytest.mark.parametrize('phase_state', [0, 1])
@pytest.mark.parametrize('target_bitsize', [1, 2, 3])
@pytest.mark.parametrize('ancilla_bitsize', [1, 4])
def test_decompose_gate_that_allocates_dirty_qubits(
    phase_state: int, target_bitsize: int, ancilla_bitsize: int
):
    gate = testing.PhaseUsingDirtyAncilla(phase_state, target_bitsize, ancilla_bitsize)
    _test_gate_that_allocates_qubits(gate)


def test_decompose_and_get_unitary():
    from qubitron.protocols.unitary_protocol import _strat_unitary_from_decompose

    np.testing.assert_allclose(_strat_unitary_from_decompose(DecomposableOperation((a,), True)), m1)
    np.testing.assert_allclose(
        _strat_unitary_from_decompose(DecomposableOperation((a, b), True)), m2
    )
    np.testing.assert_allclose(_strat_unitary_from_decompose(DecomposableOrder((a, b, c))), m3)
    np.testing.assert_allclose(_strat_unitary_from_decompose(ExampleOperation((a,))), np.eye(2))
    np.testing.assert_allclose(_strat_unitary_from_decompose(ExampleOperation((a, b))), np.eye(4))
    np.testing.assert_allclose(_strat_unitary_from_decompose(ExampleComposite()), np.eye(1))
    np.testing.assert_allclose(_strat_unitary_from_decompose(OtherComposite()), m2)


def test_decomposed_has_unitary():
    # Gates
    assert qubitron.has_unitary(DecomposableGate(True))
    assert not qubitron.has_unitary(DecomposableGate(False))

    # GateOperations
    assert qubitron.has_unitary(DecomposableGate(True).on(a))
    assert not qubitron.has_unitary(DecomposableGate(False).on(a))

    # Operations
    assert qubitron.has_unitary(DecomposableOperation((a, b), True))
    assert qubitron.has_unitary(ExampleOperation((a,)))
    assert qubitron.has_unitary(ExampleOperation((a, b)))

    # No qid shape
    assert qubitron.has_unitary(ExampleComposite())
    assert qubitron.has_unitary(OtherComposite())


def test_decomposed_unitary():
    # Gates
    np.testing.assert_allclose(qubitron.unitary(DecomposableGate(True)), m1)

    # GateOperations
    np.testing.assert_allclose(qubitron.unitary(DecomposableGate(True).on(a)), m1)

    # Operations
    np.testing.assert_allclose(qubitron.unitary(DecomposableOperation((a,), True)), m1)
    np.testing.assert_allclose(qubitron.unitary(DecomposableOperation((a, b), True)), m2)
    np.testing.assert_allclose(qubitron.unitary(DecomposableOrder((a, b, c))), m3)
    np.testing.assert_allclose(qubitron.unitary(ExampleOperation((a,))), np.eye(2))
    np.testing.assert_allclose(qubitron.unitary(ExampleOperation((a, b))), np.eye(4))
    assert qubitron.unitary(DecomposableNoUnitary((a,)), None) is None

    # No qid shape
    np.testing.assert_allclose(qubitron.unitary(ExampleComposite()), np.eye(1))
    np.testing.assert_allclose(qubitron.unitary(OtherComposite()), m2)


def test_unitary_from_apply_unitary():
    class ApplyGate(qubitron.Gate):
        def num_qubits(self):
            return 1

        def _apply_unitary_(self, args):
            return qubitron.apply_unitary(qubitron.X(qubitron.LineQubit(0)), args)

    class UnknownType:
        def _apply_unitary_(self, args):
            assert False  # pragma: no cover

    class ApplyGateNotUnitary(qubitron.Gate):
        def num_qubits(self):
            return 1

        def _apply_unitary_(self, args):
            return None

    class ApplyOp(qubitron.Operation):
        def __init__(self, q):
            self.q = q

        @property
        def qubits(self):
            return (self.q,)

        def with_qubits(self, *new_qubits):  # pragma: no cover
            return ApplyOp(*new_qubits)

        def _apply_unitary_(self, args):
            return qubitron.apply_unitary(qubitron.X(self.q), args)

    assert qubitron.has_unitary(ApplyGate())
    assert qubitron.has_unitary(ApplyOp(qubitron.LineQubit(0)))
    assert not qubitron.has_unitary(ApplyGateNotUnitary())
    assert not qubitron.has_unitary(UnknownType())

    np.testing.assert_allclose(qubitron.unitary(ApplyGate()), np.array([[0, 1], [1, 0]]))
    np.testing.assert_allclose(qubitron.unitary(ApplyOp(qubitron.LineQubit(0))), np.array([[0, 1], [1, 0]]))
    assert qubitron.unitary(ApplyGateNotUnitary(), default=None) is None
    assert qubitron.unitary(UnknownType(), default=None) is None
