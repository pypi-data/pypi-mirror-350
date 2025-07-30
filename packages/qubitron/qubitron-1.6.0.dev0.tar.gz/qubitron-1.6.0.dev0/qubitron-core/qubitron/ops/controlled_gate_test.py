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

from types import EllipsisType, NotImplementedType
from typing import Any, cast, Sequence

import numpy as np
import pytest
import sympy

import qubitron


class GateUsingWorkspaceForApplyUnitary(qubitron.testing.SingleQubitGate):
    def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray | NotImplementedType:
        args.available_buffer[...] = args.target_tensor
        args.target_tensor[...] = 0
        return args.available_buffer

    def _unitary_(self):
        return np.eye(2)

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return 'qubitron.ops.controlled_gate_test.GateUsingWorkspaceForApplyUnitary()'


class GateAllocatingNewSpaceForResult(qubitron.testing.SingleQubitGate):
    def __init__(self):
        self._matrix = qubitron.testing.random_unitary(2, random_state=4321)

    def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray | NotImplementedType:
        assert len(args.axes) == 1
        a = args.axes[0]
        seed = cast(tuple[int | slice | EllipsisType, ...], (slice(None),))
        zero = seed * a + (0, Ellipsis)
        one = seed * a + (1, Ellipsis)
        result = np.zeros(args.target_tensor.shape, args.target_tensor.dtype)
        result[zero] = (
            args.target_tensor[zero] * self._matrix[0][0]
            + args.target_tensor[one] * self._matrix[0][1]
        )
        result[one] = (
            args.target_tensor[zero] * self._matrix[1][0]
            + args.target_tensor[one] * self._matrix[1][1]
        )
        return result

    def _unitary_(self):
        return self._matrix

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return 'qubitron.ops.controlled_gate_test.GateAllocatingNewSpaceForResult()'


class RestrictedGate(qubitron.testing.SingleQubitGate):
    def _unitary_(self):
        return True

    def __str__(self):
        return 'Restricted'


q = qubitron.NamedQubit('q')
p = qubitron.NamedQubit('p')
q3 = q.with_dimension(3)
p3 = p.with_dimension(3)

CY = qubitron.ControlledGate(qubitron.Y)
CCH = qubitron.ControlledGate(qubitron.ControlledGate(qubitron.H))
CRestricted = qubitron.ControlledGate(RestrictedGate())

C0Y = qubitron.ControlledGate(qubitron.Y, control_values=[0])
C0C1H = qubitron.ControlledGate(qubitron.ControlledGate(qubitron.H, control_values=[1]), control_values=[0])

nand_control_values = qubitron.SumOfProducts([(0, 1), (1, 0), (1, 1)])
xor_control_values = qubitron.SumOfProducts([[0, 1], [1, 0]], name="xor")
C_01_10_11H = qubitron.ControlledGate(qubitron.H, control_values=nand_control_values)
C_xorH = qubitron.ControlledGate(qubitron.H, control_values=xor_control_values)
C0C_xorH = qubitron.ControlledGate(C_xorH, control_values=[0])

C0Restricted = qubitron.ControlledGate(RestrictedGate(), control_values=[0])
C_xorRestricted = qubitron.ControlledGate(RestrictedGate(), control_values=xor_control_values)

C2Y = qubitron.ControlledGate(qubitron.Y, control_values=[2], control_qid_shape=(3,))
C2C2H = qubitron.ControlledGate(
    qubitron.ControlledGate(qubitron.H, control_values=[2], control_qid_shape=(3,)),
    control_values=[2],
    control_qid_shape=(3,),
)
C_02_20H = qubitron.ControlledGate(
    qubitron.H, control_values=qubitron.SumOfProducts([[0, 2], [1, 0]]), control_qid_shape=(2, 3)
)
C2Restricted = qubitron.ControlledGate(RestrictedGate(), control_values=[2], control_qid_shape=(3,))


def test_init():
    gate = qubitron.ControlledGate(qubitron.Z)
    assert gate.sub_gate is qubitron.Z
    assert gate.num_qubits() == 2


def test_init2():
    with pytest.raises(ValueError, match=r'qubitron\.num_qubits\(control_values\) != num_controls'):
        qubitron.ControlledGate(qubitron.Z, num_controls=1, control_values=(1, 0))
    with pytest.raises(ValueError, match=r'len\(control_qid_shape\) != num_controls'):
        qubitron.ControlledGate(qubitron.Z, num_controls=1, control_qid_shape=(2, 2))
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        qubitron.ControlledGate(qubitron.Z, control_values=[2])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        qubitron.ControlledGate(qubitron.Z, control_values=[(1, -1)])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        qubitron.ControlledGate(qubitron.Z, control_values=[3], control_qid_shape=[3])
    with pytest.raises(ValueError, match='Cannot control measurement'):
        qubitron.ControlledGate(qubitron.MeasurementGate(1))
    with pytest.raises(ValueError, match='Cannot control channel'):
        qubitron.ControlledGate(qubitron.PhaseDampingChannel(1))

    gate = qubitron.ControlledGate(qubitron.Z, 1)
    assert gate.sub_gate is qubitron.Z
    assert gate.num_controls() == 1
    assert gate.control_values == qubitron.ProductOfSums(((1,),))
    assert gate.control_qid_shape == (2,)
    assert gate.num_qubits() == 2
    assert qubitron.qid_shape(gate) == (2, 2)

    gate = qubitron.ControlledGate(qubitron.Z, 2)
    assert gate.sub_gate is qubitron.Z
    assert gate.num_controls() == 2
    assert gate.control_values == qubitron.ProductOfSums(((1,), (1,)))
    assert gate.control_qid_shape == (2, 2)
    assert gate.num_qubits() == 3
    assert qubitron.qid_shape(gate) == (2, 2, 2)

    gate = qubitron.ControlledGate(
        qubitron.ControlledGate(qubitron.ControlledGate(qubitron.Z, 3), num_controls=2), 2
    )
    assert gate.sub_gate is qubitron.Z
    assert gate.num_controls() == 7
    assert gate.control_values == qubitron.ProductOfSums(((1,),) * 7)
    assert gate.control_qid_shape == (2,) * 7
    assert gate.num_qubits() == 8
    assert qubitron.qid_shape(gate) == (2,) * 8
    op = gate(*qubitron.LineQubit.range(8))
    assert op.qubits == (
        qubitron.LineQubit(0),
        qubitron.LineQubit(1),
        qubitron.LineQubit(2),
        qubitron.LineQubit(3),
        qubitron.LineQubit(4),
        qubitron.LineQubit(5),
        qubitron.LineQubit(6),
        qubitron.LineQubit(7),
    )

    gate = qubitron.ControlledGate(qubitron.Z, control_values=(0, (0, 1)))
    assert gate.sub_gate is qubitron.Z
    assert gate.num_controls() == 2
    assert gate.control_values == qubitron.ProductOfSums(((0,), (0, 1)))
    assert gate.control_qid_shape == (2, 2)
    assert gate.num_qubits() == 3
    assert qubitron.qid_shape(gate) == (2, 2, 2)

    gate = qubitron.ControlledGate(qubitron.Z, control_qid_shape=(3, 3))
    assert gate.sub_gate is qubitron.Z
    assert gate.num_controls() == 2
    assert gate.control_values == qubitron.ProductOfSums(((1,), (1,)))
    assert gate.control_qid_shape == (3, 3)
    assert gate.num_qubits() == 3
    assert qubitron.qid_shape(gate) == (3, 3, 2)


def test_validate_args():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    # Need a control qubit.
    with pytest.raises(ValueError):
        CRestricted.validate_args([])
    with pytest.raises(ValueError):
        CRestricted.validate_args([a])
    CRestricted.validate_args([a, b])

    # CY is a two-qubit operation (control + single-qubit sub gate).
    with pytest.raises(ValueError):
        CY.validate_args([a])
    with pytest.raises(ValueError):
        CY.validate_args([a, b, c])
    CY.validate_args([a, b])

    # Applies when creating operations.
    with pytest.raises(ValueError):
        _ = CY.on()
    with pytest.raises(ValueError):
        _ = CY.on(a)
    with pytest.raises(ValueError):
        _ = CY.on(a, b, c)
    _ = CY.on(a, b)

    # Applies when creating operations.
    with pytest.raises(ValueError):
        _ = CCH.on()
    with pytest.raises(ValueError):
        _ = CCH.on(a)
    with pytest.raises(ValueError):
        _ = CCH.on(a, b)

    # Applies when creating operations. Control qids have different dimensions.
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = CY.on(q3, b)
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = C2Y.on(a, b)
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = C2C2H.on(a, b, c)
    _ = C2C2H.on(q3, p3, a)


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(CY, qubitron.ControlledGate(qubitron.Y))
    eq.add_equality_group(CCH)
    eq.add_equality_group(qubitron.ControlledGate(qubitron.H))
    eq.add_equality_group(qubitron.ControlledGate(qubitron.X))
    eq.add_equality_group(qubitron.X)
    eq.add_equality_group(
        qubitron.ControlledGate(qubitron.H, control_values=[1, (0, 2)], control_qid_shape=[2, 3]),
        qubitron.ControlledGate(qubitron.H, control_values=(1, [0, 2]), control_qid_shape=(2, 3)),
        qubitron.ControlledGate(
            qubitron.H, control_values=qubitron.SumOfProducts([[1, 0], [1, 2]]), control_qid_shape=(2, 3)
        ),
    )
    eq.add_equality_group(
        qubitron.ControlledGate(qubitron.H, control_values=[(2, 0), 1], control_qid_shape=[3, 2]),
        qubitron.ControlledGate(
            qubitron.H, control_values=qubitron.SumOfProducts([[2, 1], [0, 1]]), control_qid_shape=(3, 2)
        ),
    )
    eq.add_equality_group(
        qubitron.ControlledGate(qubitron.H, control_values=[1, 0], control_qid_shape=[2, 3]),
        qubitron.ControlledGate(qubitron.H, control_values=(1, 0), control_qid_shape=(2, 3)),
    )
    eq.add_equality_group(
        qubitron.ControlledGate(qubitron.H, control_values=[0, 1], control_qid_shape=[3, 2])
    )
    eq.add_equality_group(
        qubitron.ControlledGate(qubitron.H, control_values=[1, 0]),
        qubitron.ControlledGate(qubitron.H, control_values=(1, 0)),
    )
    eq.add_equality_group(qubitron.ControlledGate(qubitron.H, control_values=[0, 1]))
    for group in eq._groups:
        if isinstance(group[0], qubitron.Gate):
            for item in group:
                np.testing.assert_allclose(qubitron.unitary(item), qubitron.unitary(group[0]))


def test_control():
    class G(qubitron.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    g = G()

    # Ignores empty.
    assert g.controlled() == qubitron.ControlledGate(g)

    # Combined.
    cg = g.controlled()
    assert isinstance(cg, qubitron.ControlledGate)
    assert cg.sub_gate == g
    assert cg.num_controls() == 1

    # Equality ignores ordering but cares about set and quantity.
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(g)
    eq.add_equality_group(
        g.controlled(),
        g.controlled(control_values=[1]),
        g.controlled(control_qid_shape=(2,)),
        qubitron.ControlledGate(g, num_controls=1),
        g.controlled(control_values=qubitron.SumOfProducts([[1]])),
    )
    eq.add_equality_group(
        qubitron.ControlledGate(g, num_controls=2),
        g.controlled(control_values=[1, 1]),
        g.controlled(control_qid_shape=[2, 2]),
        g.controlled(num_controls=2),
        g.controlled().controlled(),
        g.controlled(control_values=qubitron.SumOfProducts([[1, 1]])),
    )
    eq.add_equality_group(
        qubitron.ControlledGate(g, control_values=[0, 1]),
        g.controlled(control_values=[0, 1]),
        g.controlled(control_values=[1]).controlled(control_values=[0]),
        g.controlled(control_values=qubitron.SumOfProducts([[1]])).controlled(control_values=[0]),
    )
    eq.add_equality_group(g.controlled(control_values=[0]).controlled(control_values=[1]))
    eq.add_equality_group(
        qubitron.ControlledGate(g, control_qid_shape=[4, 3]),
        g.controlled(control_qid_shape=[4, 3]),
        g.controlled(control_qid_shape=[3]).controlled(control_qid_shape=[4]),
    )
    eq.add_equality_group(g.controlled(control_qid_shape=[4]).controlled(control_qid_shape=[3]))


def test_unitary():
    cxa = qubitron.ControlledGate(qubitron.X ** sympy.Symbol('a'))
    assert not qubitron.has_unitary(cxa)
    assert qubitron.unitary(cxa, None) is None

    assert qubitron.has_unitary(CY)
    assert qubitron.has_unitary(CCH)
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(CY),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, -1j],
                [0, 0, 1j, 0],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(C0Y),
        np.array(
            [
                [0, -1j, 0, 0],
                [1j, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(CCH),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, np.sqrt(0.5), np.sqrt(0.5)],
                [0, 0, 0, 0, 0, 0, np.sqrt(0.5), -np.sqrt(0.5)],
            ]
        ),
        atol=1e-8,
    )

    C_xorX = qubitron.ControlledGate(qubitron.X, control_values=xor_control_values)
    # fmt: off
    np.testing.assert_allclose(qubitron.unitary(C_xorX), np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]]
    ))
    # fmt: on


@pytest.mark.parametrize(
    'gate, should_decompose_to_target',
    [
        (qubitron.X, True),
        (qubitron.X**0.5, True),
        (qubitron.rx(np.pi), True),
        (qubitron.rx(np.pi / 2), True),
        (qubitron.Z, True),
        (qubitron.H, True),
        (qubitron.CNOT, True),
        (qubitron.SWAP, True),
        (qubitron.CCZ, True),
        (qubitron.ControlledGate(qubitron.ControlledGate(qubitron.CCZ)), True),
        (GateUsingWorkspaceForApplyUnitary(), True),
        (GateAllocatingNewSpaceForResult(), True),
        (qubitron.IdentityGate(qid_shape=(3, 4)), True),
        (
            qubitron.ControlledGate(
                qubitron.XXPowGate(exponent=0.25, global_shift=-0.5),
                num_controls=2,
                control_values=(1, (1, 0)),
            ),
            True,
        ),
        (qubitron.GlobalPhaseGate(-1), True),
        (qubitron.GlobalPhaseGate(1j**0.7), True),
        (qubitron.GlobalPhaseGate(sympy.Symbol("s")), False),
        (qubitron.CZPowGate(exponent=1.2, global_shift=0.3), True),
        (qubitron.CZPowGate(exponent=sympy.Symbol("s"), global_shift=0.3), False),
        # Single qudit gate with dimension 4.
        (qubitron.MatrixGate(np.kron(*(qubitron.unitary(qubitron.H),) * 2), qid_shape=(4,)), False),
        (qubitron.MatrixGate(qubitron.testing.random_unitary(4, random_state=1234)), False),
        (qubitron.XX ** sympy.Symbol("s"), True),
        (qubitron.CZ ** sympy.Symbol("s"), True),
        # Non-trivial `qubitron.ProductOfSum` controls.
        (C_01_10_11H, False),
        (C_xorH, False),
        (C0C_xorH, False),
    ],
)
def test_controlled_gate_is_consistent(gate: qubitron.Gate, should_decompose_to_target):
    _test_controlled_gate_is_consistent(gate, should_decompose_to_target)


@pytest.mark.parametrize(
    'gate',
    [
        qubitron.I,
        qubitron.GlobalPhaseGate(1),
        qubitron.GlobalPhaseGate(-1),
        qubitron.GlobalPhaseGate(1j),
        qubitron.GlobalPhaseGate(1j**0.7),
        qubitron.Z,
        qubitron.ZPowGate(exponent=1.2, global_shift=0.3),
        qubitron.CZ,
        qubitron.CZPowGate(exponent=1.2, global_shift=0.3),
        qubitron.CCZ,
        qubitron.CCZPowGate(exponent=1.2, global_shift=0.3),
        qubitron.X,
        qubitron.XPowGate(exponent=1.2, global_shift=0.3),
        qubitron.CX,
        qubitron.CXPowGate(exponent=1.2, global_shift=0.3),
        qubitron.CCX,
        qubitron.CCXPowGate(exponent=1.2, global_shift=0.3),
    ],
)
@pytest.mark.parametrize(
    'control_qid_shape, control_values, should_decompose_to_target',
    [
        ([2, 2], None, True),
        ([2, 2], xor_control_values, False),
        ([3], None, False),
        ([3, 4], xor_control_values, False),
    ],
)
def test_nontrivial_controlled_gate_is_consistent(
    gate: qubitron.Gate,
    control_qid_shape: Sequence[int],
    control_values: Any,
    should_decompose_to_target: bool,
):
    _test_controlled_gate_is_consistent(
        gate, should_decompose_to_target, control_qid_shape, control_values
    )


def _test_controlled_gate_is_consistent(
    gate: qubitron.Gate,
    should_decompose_to_target: bool,
    control_qid_shape: Sequence[int] | None = None,
    control_values: Any = None,
):
    cgate = qubitron.ControlledGate(
        gate, control_qid_shape=control_qid_shape, control_values=control_values
    )
    qubitron.testing.assert_implements_consistent_protocols(cgate)
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=not should_decompose_to_target
    )
    # The above only decompose once, which doesn't check that the sub-gate's phase is handled.
    # We need to check full decomposition here.
    if not qubitron.is_parameterized(gate):
        shape = qubitron.qid_shape(cgate)
        qids = qubitron.LineQid.for_qid_shape(shape)
        decomposed = qubitron.decompose(cgate.on(*qids))
        first_op = qubitron.IdentityGate(qid_shape=shape).on(*qids)  # To ensure same qid order
        circuit = qubitron.Circuit(first_op, *decomposed)
        np.testing.assert_allclose(qubitron.unitary(cgate), qubitron.unitary(circuit), atol=1e-13)


@pytest.mark.parametrize(
    'sub_gate, expected_decomposition',
    [
        (qubitron.X, [qubitron.CX]),
        (qubitron.CX, [qubitron.CCX]),
        (qubitron.XPowGate(), [qubitron.CXPowGate()]),
        (qubitron.CXPowGate(), [qubitron.CCXPowGate()]),
        (qubitron.Z, [qubitron.CZ]),
        (qubitron.CZ, [qubitron.CCZ]),
        (qubitron.ZPowGate(), [qubitron.CZPowGate()]),
        (qubitron.CZPowGate(), [qubitron.CCZPowGate()]),
    ],
)
def test_controlled_gate_decomposition_uses_canonical_version(
    sub_gate: qubitron.Gate, expected_decomposition: list[qubitron.Gate]
):
    cgate = qubitron.ControlledGate(sub_gate, num_controls=1)
    qubits = qubitron.LineQubit.range(1 + sub_gate.num_qubits())
    dec = qubitron.decompose_once(cgate.on(*qubits))
    assert dec == [gate.on(*qubits) for gate in expected_decomposition]


@pytest.mark.parametrize(
    'sub_gate, expected_decomposition', [(qubitron.Z, [qubitron.CZ]), (qubitron.ZPowGate(), [qubitron.CZPowGate()])]
)
def test_controlled_gate_full_decomposition(
    sub_gate: qubitron.Gate, expected_decomposition: list[qubitron.Gate]
):
    cgate = qubitron.ControlledGate(sub_gate, num_controls=1)
    qubits = qubitron.LineQubit.range(1 + sub_gate.num_qubits())
    dec = qubitron.decompose(cgate.on(*qubits))
    assert dec == [gate.on(*qubits) for gate in expected_decomposition]


def test_pow_inverse():
    assert qubitron.inverse(CRestricted, None) is None
    assert qubitron.pow(CRestricted, 1.5, None) is None
    assert qubitron.pow(CY, 1.5) == qubitron.ControlledGate(qubitron.Y**1.5)
    assert qubitron.inverse(CY) == CY**-1 == CY

    assert qubitron.inverse(C0Restricted, None) is None
    assert qubitron.pow(C0Restricted, 1.5, None) is None
    assert qubitron.pow(C0Y, 1.5) == qubitron.ControlledGate(qubitron.Y**1.5, control_values=[0])
    assert qubitron.inverse(C0Y) == C0Y**-1 == C0Y

    assert qubitron.inverse(C2Restricted, None) is None
    assert qubitron.pow(C2Restricted, 1.5, None) is None
    assert qubitron.pow(C2Y, 1.5) == qubitron.ControlledGate(
        qubitron.Y**1.5, control_values=[2], control_qid_shape=(3,)
    )
    assert qubitron.inverse(C2Y) == C2Y**-1 == C2Y


def test_extrapolatable_effect():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.ControlledGate(qubitron.Z) ** 0.5 == qubitron.ControlledGate(qubitron.Z**0.5)

    assert qubitron.ControlledGate(qubitron.Z).on(a, b) ** 0.5 == qubitron.ControlledGate(qubitron.Z**0.5).on(a, b)

    assert qubitron.ControlledGate(qubitron.Z) ** 0.5 == qubitron.ControlledGate(qubitron.Z**0.5)


def test_reversible():
    assert qubitron.inverse(qubitron.ControlledGate(qubitron.S)) == qubitron.ControlledGate(qubitron.S**-1)
    assert qubitron.inverse(qubitron.ControlledGate(qubitron.S, num_controls=4)) == qubitron.ControlledGate(
        qubitron.S**-1, num_controls=4
    )
    assert qubitron.inverse(qubitron.ControlledGate(qubitron.S, control_values=[1])) == qubitron.ControlledGate(
        qubitron.S**-1, control_values=[1]
    )
    assert qubitron.inverse(qubitron.ControlledGate(qubitron.S, control_qid_shape=(3,))) == qubitron.ControlledGate(
        qubitron.S**-1, control_qid_shape=(3,)
    )


class UnphaseableGate(qubitron.Gate):
    pass


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    a = sympy.Symbol('a')
    cy = qubitron.ControlledGate(qubitron.Y)
    cya = qubitron.ControlledGate(qubitron.YPowGate(exponent=a))
    assert qubitron.is_parameterized(cya)
    assert not qubitron.is_parameterized(cy)
    assert resolve_fn(cya, qubitron.ParamResolver({'a': 1})) == cy

    cchan = qubitron.ControlledGate(
        qubitron.RandomGateChannel(sub_gate=qubitron.PhaseDampingChannel(0.1), probability=a)
    )
    with pytest.raises(ValueError, match='Cannot control channel'):
        resolve_fn(cchan, qubitron.ParamResolver({'a': 0.1}))


def test_circuit_diagram_info():
    assert qubitron.circuit_diagram_info(CY) == qubitron.CircuitDiagramInfo(
        wire_symbols=('@', 'Y'), exponent=1
    )

    assert qubitron.circuit_diagram_info(C0Y) == qubitron.CircuitDiagramInfo(
        wire_symbols=('(0)', 'Y'), exponent=1
    )

    assert qubitron.circuit_diagram_info(C2Y) == qubitron.CircuitDiagramInfo(
        wire_symbols=('(2)', 'Y'), exponent=1
    )

    assert qubitron.circuit_diagram_info(qubitron.ControlledGate(qubitron.Y**0.5)) == qubitron.CircuitDiagramInfo(
        wire_symbols=('@', 'Y'), exponent=0.5
    )

    assert qubitron.circuit_diagram_info(qubitron.ControlledGate(qubitron.S)) == qubitron.CircuitDiagramInfo(
        wire_symbols=('@', 'S'), exponent=1
    )

    class UndiagrammableGate(qubitron.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

    assert (
        qubitron.circuit_diagram_info(qubitron.ControlledGate(UndiagrammableGate()), default=None) is None
    )


# A contrived multiqubit Hadamard gate that asserts the consistency of
# the passed in Args and puts an H on all qubits
# displays them as 'H(qubit)' on the wire
class MultiH(qubitron.Gate):
    def num_qubits(self) -> int:
        return self._num_qubits

    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def _circuit_diagram_info_(self, args: qubitron.CircuitDiagramInfoArgs) -> qubitron.CircuitDiagramInfo:
        assert args.known_qubit_count is not None
        assert args.known_qubits is not None

        return qubitron.CircuitDiagramInfo(
            wire_symbols=tuple(f'H({q})' for q in args.known_qubits), connected=True
        )

    def _has_unitary_(self):
        return True


def test_circuit_diagram_product_of_sums():
    qubits = qubitron.LineQubit.range(3)
    c = qubitron.Circuit()
    c.append(qubitron.ControlledGate(MultiH(2))(*qubits))

    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───@─────────
      │
1: ───H(q(1))───
      │
2: ───H(q(2))───
""",
    )

    qubits = qubitron.LineQid.for_qid_shape((3, 3, 3, 2))
    c = qubitron.Circuit(
        MultiH(1)(*qubits[3:]).controlled_by(*qubits[:3], control_values=[1, (0, 1), (2, 0)])
    )

    qubitron.testing.assert_has_diagram(
        c,
        """
0 (d=3): ───@───────────────
            │
1 (d=3): ───(0,1)───────────
            │
2 (d=3): ───(0,2)───────────
            │
3 (d=2): ───H(q(3) (d=2))───
""",
    )


def test_circuit_diagram_sum_of_products():
    q = qubitron.LineQubit.range(4)
    c = qubitron.Circuit(C_xorH.on(*q[:3]), C_01_10_11H.on(*q[:3]), C0C_xorH.on(*q))
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───@────────@(011)───@(00)───
      │        │        │
1: ───@(xor)───@(101)───@(01)───
      │        │        │
2: ───H────────H────────@(10)───
                        │
3: ─────────────────────H───────
""",
    )
    q = qubitron.LineQid.for_qid_shape((2, 3, 2))
    c = qubitron.Circuit(C_02_20H(*q))
    qubitron.testing.assert_has_diagram(
        c,
        """
0 (d=2): ───@(01)───
            │
1 (d=3): ───@(20)───
            │
2 (d=2): ───H───────
""",
    )


class MockGate(qubitron.testing.TwoQubitGate):
    def _circuit_diagram_info_(self, args: qubitron.CircuitDiagramInfoArgs) -> qubitron.CircuitDiagramInfo:
        self.captured_diagram_args = args
        return qubitron.CircuitDiagramInfo(wire_symbols=tuple(['M1', 'M2']), exponent=1, connected=True)

    def _has_unitary_(self):
        return True


def test_uninformed_circuit_diagram_info():
    qbits = qubitron.LineQubit.range(3)
    mock_gate = MockGate()
    cgate = qubitron.ControlledGate(mock_gate)(*qbits)

    args = qubitron.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT

    assert qubitron.circuit_diagram_info(cgate, args) == qubitron.CircuitDiagramInfo(
        wire_symbols=('@', 'M1', 'M2'), exponent=1, connected=True, exponent_qubit_index=1
    )
    assert mock_gate.captured_diagram_args == args


def test_bounded_effect():
    assert qubitron.trace_distance_bound(CY**0.001) < 0.01
    assert qubitron.approx_eq(qubitron.trace_distance_bound(CCH), 1.0)
    foo = sympy.Symbol('foo')
    assert qubitron.trace_distance_bound(qubitron.ControlledGate(qubitron.X**foo)) == 1


@pytest.mark.parametrize(
    'gate',
    [
        qubitron.ControlledGate(qubitron.Z),
        qubitron.ControlledGate(qubitron.Z, num_controls=1),
        qubitron.ControlledGate(qubitron.Z, num_controls=2),
        C0C1H,
        C2C2H,
        C_01_10_11H,
        C_xorH,
        C_02_20H,
    ],
)
def test_repr(gate):
    qubitron.testing.assert_equivalent_repr(gate)


def test_str():
    assert str(qubitron.ControlledGate(qubitron.X)) == 'CX'
    assert str(qubitron.ControlledGate(qubitron.Z)) == 'CZ'
    assert str(qubitron.ControlledGate(qubitron.S)) == 'CS'
    assert str(qubitron.ControlledGate(qubitron.Z**0.125)) == 'CZ**0.125'
    assert str(qubitron.ControlledGate(qubitron.ControlledGate(qubitron.S))) == 'CCS'
    assert str(C0Y) == 'C0Y'
    assert str(C0C1H) == 'C0C1H'
    assert str(C0Restricted) == 'C0Restricted'
    assert str(C2Y) == 'C2Y'
    assert str(C2C2H) == 'C2C2H'
    assert str(C2Restricted) == 'C2Restricted'


def test_controlled_mixture():
    c_yes = qubitron.ControlledGate(sub_gate=qubitron.phase_flip(0.25), num_controls=1)
    assert qubitron.has_mixture(c_yes)
    assert qubitron.approx_eq(qubitron.mixture(c_yes), [(0.75, np.eye(4)), (0.25, qubitron.unitary(qubitron.CZ))])
