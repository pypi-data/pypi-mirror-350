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
import sympy

import qubitron


def test_commutes_on_matrices():
    I, X, Y, Z = (qubitron.unitary(A) for A in (qubitron.I, qubitron.X, qubitron.Y, qubitron.Z))
    IX, IY = (np.kron(I, A) for A in (X, Y))
    XI, YI, ZI = (np.kron(A, I) for A in (X, Y, Z))
    XX, YY, ZZ = (np.kron(A, A) for A in (X, Y, Z))
    for A in (X, Y, Z):
        assert qubitron.commutes(I, A)
        assert qubitron.commutes(A, A)
        assert qubitron.commutes(I, XX, default='default') == 'default'
    for A, B in [(X, Y), (X, Z), (Z, Y), (IX, IY), (XI, ZI)]:
        assert not qubitron.commutes(A, B)
        assert not qubitron.commutes(A, B, atol=1)
        assert qubitron.commutes(A, B, atol=2)
    for A, B in [(XX, YY), (XX, ZZ), (ZZ, YY), (IX, YI), (IX, IX), (ZI, IY)]:
        assert qubitron.commutes(A, B)


def test_commutes_on_gates_and_gate_operations():
    X, Y, Z = tuple(qubitron.unitary(A) for A in (qubitron.X, qubitron.Y, qubitron.Z))
    XGate, YGate, ZGate = (qubitron.MatrixGate(A) for A in (X, Y, Z))
    XXGate, YYGate, ZZGate = (qubitron.MatrixGate(qubitron.kron(A, A)) for A in (X, Y, Z))
    a, b = qubitron.LineQubit.range(2)
    for A in (XGate, YGate, ZGate):
        assert qubitron.commutes(A, A)
        assert A._commutes_on_qids_(a, A, atol=1e-8) is NotImplemented
        with pytest.raises(TypeError):
            qubitron.commutes(A(a), A)
        with pytest.raises(TypeError):
            qubitron.commutes(A, A(a))
        assert qubitron.commutes(A(a), A(a))
        assert qubitron.commutes(A, XXGate, default='default') == 'default'
    for A, B in [
        (XGate, YGate),
        (XGate, ZGate),
        (ZGate, YGate),
        (XGate, qubitron.Y),
        (XGate, qubitron.Z),
        (ZGate, qubitron.Y),
    ]:
        assert not qubitron.commutes(A, B)
        assert qubitron.commutes(A(a), B(b))
        assert not qubitron.commutes(A(a), B(a))
        with pytest.raises(TypeError):
            qubitron.commutes(A, B(a))
        qubitron.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    for A, B in [(XXGate, YYGate), (XXGate, ZZGate)]:
        assert qubitron.commutes(A, B)
        with pytest.raises(TypeError):
            qubitron.commutes(A(a, b), B)
        with pytest.raises(TypeError):
            qubitron.commutes(A, B(a, b))
        assert qubitron.commutes(A(a, b), B(a, b))
        assert qubitron.definitely_commutes(A(a, b), B(a, b))
        qubitron.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    for A, B in [(XGate, XXGate), (XGate, YYGate)]:
        with pytest.raises(TypeError):
            qubitron.commutes(A, B(a, b))
        assert not qubitron.definitely_commutes(A, B(a, b))
        with pytest.raises(TypeError):
            assert qubitron.commutes(A(b), B)
        with pytest.raises(TypeError):
            assert qubitron.commutes(A, B)
        qubitron.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    with pytest.raises(TypeError):
        assert qubitron.commutes(XGate, qubitron.X ** sympy.Symbol('e'))
    with pytest.raises(TypeError):
        assert qubitron.commutes(XGate(a), 'Gate')
    assert qubitron.commutes(XGate(a), 'Gate', default='default') == 'default'


def test_operation_commutes_using_overlap_and_unitary():
    class CustomCnotGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 2

        def _unitary_(self):
            return qubitron.unitary(qubitron.CNOT)

    custom_cnot_gate = CustomCnotGate()

    class CustomCnotOp(qubitron.Operation):
        def __init__(self, *qs: qubitron.Qid):
            self.qs = qs

        def _unitary_(self):
            return qubitron.unitary(qubitron.CNOT)

        @property
        def qubits(self):
            return self.qs

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    class NoDetails(qubitron.Operation):
        def __init__(self, *qs: qubitron.Qid):
            self.qs = qs

        @property
        def qubits(self):
            return self.qs

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    a, b, c = qubitron.LineQubit.range(3)

    # If ops overlap with known unitaries, fallback to matrix commutation.
    assert not qubitron.commutes(CustomCnotOp(a, b), CustomCnotOp(b, a))
    assert not qubitron.commutes(CustomCnotOp(a, b), CustomCnotOp(b, c))
    assert qubitron.commutes(CustomCnotOp(a, b), CustomCnotOp(c, b))
    assert qubitron.commutes(CustomCnotOp(a, b), CustomCnotOp(a, b))

    # If ops don't overlap, they commute. Even when no specified unitary.
    assert qubitron.commutes(CustomCnotOp(a, b), NoDetails(c))

    # If ops overlap and there's no unitary, result is indeterminate.
    assert qubitron.commutes(CustomCnotOp(a, b), NoDetails(a), default=None) is None

    # Same stuff works with custom gate, or mix of custom gate and custom op.
    assert qubitron.commutes(custom_cnot_gate(a, b), CustomCnotOp(a, b))
    assert qubitron.commutes(custom_cnot_gate(a, b), custom_cnot_gate(a, b))
    assert qubitron.commutes(custom_cnot_gate(a, b), CustomCnotOp(c, b))
    assert qubitron.commutes(custom_cnot_gate(a, b), custom_cnot_gate(c, b))
    assert not qubitron.commutes(custom_cnot_gate(a, b), CustomCnotOp(b, a))
    assert not qubitron.commutes(custom_cnot_gate(a, b), custom_cnot_gate(b, a))
    assert not qubitron.commutes(custom_cnot_gate(a, b), CustomCnotOp(b, c))
    assert not qubitron.commutes(custom_cnot_gate(a, b), custom_cnot_gate(b, c))
