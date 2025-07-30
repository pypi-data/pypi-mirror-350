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

import itertools
import re
from types import EllipsisType, NotImplementedType
from typing import cast

import numpy as np
import pytest
import sympy

import qubitron
from qubitron import protocols


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
        return 'qubitron.ops.controlled_operation_test.GateUsingWorkspaceForApplyUnitary()'


class GateAllocatingNewSpaceForResult(qubitron.testing.SingleQubitGate):
    def __init__(self):
        self._matrix = qubitron.testing.random_unitary(2, random_state=1234)

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
        return 'qubitron.ops.controlled_operation_test.GateAllocatingNewSpaceForResult()'


def test_controlled_operation_init():
    class G(qubitron.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    g = G()
    cb = qubitron.NamedQubit('ctr')
    q = qubitron.NamedQubit('q')
    v = qubitron.GateOperation(g, (q,))
    c = qubitron.ControlledOperation([cb], v)
    assert c.sub_operation == v
    assert c.controls == (cb,)
    assert c.qubits == (cb, q)
    assert c == c.with_qubits(cb, q)
    assert c.control_values == qubitron.SumOfProducts(((1,),))
    assert qubitron.qid_shape(c) == (2, 2)

    c = qubitron.ControlledOperation([cb], v, control_values=[0])
    assert c.sub_operation == v
    assert c.controls == (cb,)
    assert c.qubits == (cb, q)
    assert c == c.with_qubits(cb, q)
    assert c.control_values == qubitron.SumOfProducts(((0,),))
    assert qubitron.qid_shape(c) == (2, 2)

    c = qubitron.ControlledOperation([cb.with_dimension(3)], v)
    assert c.sub_operation == v
    assert c.controls == (cb.with_dimension(3),)
    assert c.qubits == (cb.with_dimension(3), q)
    assert c == c.with_qubits(cb.with_dimension(3), q)
    assert c.control_values == qubitron.SumOfProducts(((1,),))
    assert qubitron.qid_shape(c) == (3, 2)

    with pytest.raises(ValueError, match=r'qubitron\.num_qubits\(control_values\) != len\(controls\)'):
        _ = qubitron.ControlledOperation([cb], v, control_values=[1, 1])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        _ = qubitron.ControlledOperation([cb], v, control_values=[2])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        _ = qubitron.ControlledOperation([cb], v, control_values=[(1, -1)])
    with pytest.raises(ValueError, match=re.escape("Duplicate control qubits ['ctr'].")):
        _ = qubitron.ControlledOperation([cb, qubitron.LineQubit(0), cb], qubitron.X(q))
    with pytest.raises(ValueError, match=re.escape("Sub-op and controls share qubits ['ctr']")):
        _ = qubitron.ControlledOperation([cb, qubitron.LineQubit(0)], qubitron.CX(cb, q))
    with pytest.raises(ValueError, match='Cannot control measurement'):
        _ = qubitron.ControlledOperation([cb], qubitron.measure(q))
    with pytest.raises(ValueError, match='Cannot control channel'):
        _ = qubitron.ControlledOperation([cb], qubitron.PhaseDampingChannel(1)(q))


def test_controlled_operation_eq():
    c1 = qubitron.NamedQubit('c1')
    q1 = qubitron.NamedQubit('q1')
    c2 = qubitron.NamedQubit('c2')

    eq = qubitron.testing.EqualsTester()

    eq.make_equality_group(lambda: qubitron.ControlledOperation([c1], qubitron.X(q1)))
    eq.make_equality_group(lambda: qubitron.ControlledOperation([c2], qubitron.X(q1)))
    eq.make_equality_group(lambda: qubitron.ControlledOperation([c1], qubitron.Z(q1)))
    eq.add_equality_group(qubitron.ControlledOperation([c2], qubitron.Z(q1)))
    eq.add_equality_group(
        qubitron.ControlledOperation([c1, c2], qubitron.Z(q1)),
        qubitron.ControlledOperation([c2, c1], qubitron.Z(q1)),
    )
    eq.add_equality_group(
        qubitron.ControlledOperation(
            [c1, c2.with_dimension(3)], qubitron.Z(q1), control_values=[1, (0, 2)]
        ),
        qubitron.ControlledOperation(
            [c2.with_dimension(3), c1], qubitron.Z(q1), control_values=[(2, 0), 1]
        ),
    )


def test_str():
    c1 = qubitron.NamedQubit('c1')
    c2 = qubitron.NamedQubit('c2')
    q2 = qubitron.NamedQubit('q2')

    assert str(qubitron.ControlledOperation([c1], qubitron.CZ(c2, q2))) == "CCZ(c1, c2, q2)"

    class SingleQubitOp(qubitron.Operation):
        @property
        def qubits(self) -> tuple[qubitron.Qid, ...]:
            return ()

        def with_qubits(self, *new_qubits: qubitron.Qid):
            return self

        def __str__(self):
            return "Op(q2)"

        def _has_mixture_(self):
            return True

    assert str(qubitron.ControlledOperation([c1, c2], SingleQubitOp())) == "CC(c1, c2, Op(q2))"

    assert (
        str(
            qubitron.ControlledOperation(
                [c1, c2.with_dimension(3)], SingleQubitOp().with_qubits(qubitron.q(1))
            )
        )
        == "CC(c1, c2 (d=3), Op(q2))"
    )

    assert (
        str(
            qubitron.ControlledOperation(
                [c1, c2.with_dimension(3)], SingleQubitOp(), control_values=[1, (2, 0)]
            )
        )
        == "C1C02(c1, c2 (d=3), Op(q2))"
    )


def test_repr():
    a, b, c, d = qubitron.LineQubit.range(4)

    ch = qubitron.H(a).controlled_by(b)
    cch = qubitron.H(a).controlled_by(b, c)
    ccz = qubitron.ControlledOperation([a], qubitron.CZ(b, c))
    c1c02z = qubitron.ControlledOperation(
        [a, b.with_dimension(3)], qubitron.CZ(d, c), control_values=[1, (2, 0)]
    )

    assert repr(ch) == ('qubitron.H(qubitron.LineQubit(0)).controlled_by(qubitron.LineQubit(1))')
    qubitron.testing.assert_equivalent_repr(ch)
    qubitron.testing.assert_equivalent_repr(cch)
    qubitron.testing.assert_equivalent_repr(ccz)
    qubitron.testing.assert_equivalent_repr(c1c02z)


# A contrived multiqubit Hadamard gate that asserts the consistency of
# the passed in Args and puts an H on all qubits
# displays them as 'H(qubit)' on the wire
class MultiH(qubitron.Gate):
    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def num_qubits(self) -> int:
        return self._num_qubits

    def _circuit_diagram_info_(
        self, args: protocols.CircuitDiagramInfoArgs
    ) -> protocols.CircuitDiagramInfo:
        assert args.known_qubit_count is not None
        assert args.known_qubits is not None

        return protocols.CircuitDiagramInfo(
            wire_symbols=tuple(f'H({q})' for q in args.known_qubits), connected=True
        )

    def _has_mixture_(self):
        return True


def test_circuit_diagram():
    qubits = qubitron.LineQubit.range(3)
    c = qubitron.Circuit()
    c.append(qubitron.ControlledOperation(qubits[:1], MultiH(2)(*qubits[1:])))

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

    c = qubitron.Circuit()
    c.append(qubitron.ControlledOperation(qubits[:2], MultiH(1)(*qubits[2:])))

    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───@─────────
      │
1: ───@─────────
      │
2: ───H(q(2))───
""",
    )

    qubits = qubitron.LineQid.for_qid_shape((3, 3, 3, 2))
    c = qubitron.Circuit()
    c.append(
        qubitron.ControlledOperation(
            qubits[:3], MultiH(1)(*qubits[3:]), control_values=[1, (0, 1), (2, 0)]
        )
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


class MockGate(qubitron.testing.TwoQubitGate):
    def __init__(self, exponent_qubit_index=None):
        self._exponent_qubit_index = exponent_qubit_index

    def _circuit_diagram_info_(
        self, args: protocols.CircuitDiagramInfoArgs
    ) -> protocols.CircuitDiagramInfo:
        self.captured_diagram_args = args
        return qubitron.CircuitDiagramInfo(
            wire_symbols=tuple(['M1', 'M2']),
            exponent=1,
            exponent_qubit_index=self._exponent_qubit_index,
            connected=True,
        )

    def _has_mixture_(self):
        return True


def test_controlled_diagram_exponent():
    for q in itertools.permutations(qubitron.LineQubit.range(5)):
        for idx in [None, 0, 1]:
            op = MockGate(idx)(*q[:2]).controlled_by(*q[2:])
            add = 0 if idx is None else idx
            assert qubitron.circuit_diagram_info(op).exponent_qubit_index == len(q[2:]) + add


def test_uninformed_circuit_diagram_info():
    qbits = qubitron.LineQubit.range(3)
    mock_gate = MockGate()
    c_op = qubitron.ControlledOperation(qbits[:1], mock_gate(*qbits[1:]))

    args = protocols.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT

    assert qubitron.circuit_diagram_info(c_op, args) == qubitron.CircuitDiagramInfo(
        wire_symbols=('@', 'M1', 'M2'), exponent=1, connected=True, exponent_qubit_index=1
    )
    assert mock_gate.captured_diagram_args == args


def test_non_diagrammable_subop():
    qbits = qubitron.LineQubit.range(2)

    class UndiagrammableGate(qubitron.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    undiagrammable_op = UndiagrammableGate()(qbits[1])

    c_op = qubitron.ControlledOperation(qbits[:1], undiagrammable_op)
    assert qubitron.circuit_diagram_info(c_op, default=None) is None


@pytest.mark.parametrize(
    'gate, should_decompose_to_target',
    [
        (qubitron.X(qubitron.NamedQubit('q1')), True),
        (qubitron.X(qubitron.NamedQubit('q1')) ** 0.5, True),
        (qubitron.rx(np.pi)(qubitron.NamedQubit('q1')), True),
        (qubitron.rx(np.pi / 2)(qubitron.NamedQubit('q1')), True),
        (qubitron.Z(qubitron.NamedQubit('q1')), True),
        (qubitron.H(qubitron.NamedQubit('q1')), True),
        (qubitron.CNOT(qubitron.NamedQubit('q1'), qubitron.NamedQubit('q2')), True),
        (qubitron.SWAP(qubitron.NamedQubit('q1'), qubitron.NamedQubit('q2')), True),
        (qubitron.CCZ(qubitron.NamedQubit('q1'), qubitron.NamedQubit('q2'), qubitron.NamedQubit('q3')), True),
        (qubitron.ControlledGate(qubitron.ControlledGate(qubitron.CCZ))(*qubitron.LineQubit.range(5)), True),
        (GateUsingWorkspaceForApplyUnitary()(qubitron.NamedQubit('q1')), True),
        (GateAllocatingNewSpaceForResult()(qubitron.NamedQubit('q1')), True),
        (
            qubitron.MatrixGate(np.kron(*(qubitron.unitary(qubitron.H),) * 2), qid_shape=(4,)).on(
                qubitron.NamedQid("q", 4)
            ),
            False,
        ),
        (
            qubitron.MatrixGate(qubitron.testing.random_unitary(4, random_state=1234)).on(
                qubitron.NamedQubit('q1'), qubitron.NamedQubit('q2')
            ),
            False,
        ),
        (qubitron.XX(qubitron.NamedQubit('q1'), qubitron.NamedQubit('q2')) ** sympy.Symbol("s"), True),
        (qubitron.DiagonalGate(sympy.symbols("s1, s2")).on(qubitron.NamedQubit("q")), False),
    ],
)
def test_controlled_operation_is_consistent(
    gate: qubitron.GateOperation, should_decompose_to_target: bool
):
    cb = qubitron.NamedQubit('ctr')
    cgate = qubitron.ControlledOperation([cb], gate)
    qubitron.testing.assert_implements_consistent_protocols(cgate)
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=not should_decompose_to_target
    )

    cgate = qubitron.ControlledOperation([cb], gate, control_values=[0])
    qubitron.testing.assert_implements_consistent_protocols(cgate)
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=(not should_decompose_to_target or qubitron.is_parameterized(gate))
    )

    cgate = qubitron.ControlledOperation([cb], gate, control_values=[(0, 1)])
    qubitron.testing.assert_implements_consistent_protocols(cgate)
    qubitron.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=(not should_decompose_to_target or qubitron.is_parameterized(gate))
    )

    cb3 = cb.with_dimension(3)
    cgate = qubitron.ControlledOperation([cb3], gate, control_values=[(0, 2)])
    qubitron.testing.assert_implements_consistent_protocols(cgate)
    qubitron.testing.assert_decompose_ends_at_default_gateset(cgate)


def test_controlled_circuit_operation_is_consistent():
    op = qubitron.CircuitOperation(
        qubitron.FrozenCircuit(
            qubitron.XXPowGate(exponent=0.25, global_shift=-0.5).on(*qubitron.LineQubit.range(2))
        )
    )
    cb = qubitron.NamedQubit('ctr')
    cop = qubitron.ControlledOperation([cb], op)
    qubitron.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    qubitron.testing.assert_decompose_ends_at_default_gateset(cop)

    cop = qubitron.ControlledOperation([cb], op, control_values=[0])
    qubitron.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    qubitron.testing.assert_decompose_ends_at_default_gateset(cop)

    cop = qubitron.ControlledOperation([cb], op, control_values=[(0, 1)])
    qubitron.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    qubitron.testing.assert_decompose_ends_at_default_gateset(cop)


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    a = sympy.Symbol('a')
    qubits = qubitron.LineQubit.range(3)

    cz = qubitron.ControlledOperation(qubits[:1], qubitron.Z(qubits[1]))
    cza = qubitron.ControlledOperation(qubits[:1], qubitron.ZPowGate(exponent=a)(qubits[1]))
    assert qubitron.is_parameterized(cza)
    assert not qubitron.is_parameterized(cz)
    assert resolve_fn(cza, qubitron.ParamResolver({'a': 1})) == cz

    cchan = qubitron.ControlledOperation(
        [qubits[0]],
        qubitron.RandomGateChannel(sub_gate=qubitron.PhaseDampingChannel(0.1), probability=a)(qubits[1]),
    )
    with pytest.raises(ValueError, match='Cannot control channel'):
        resolve_fn(cchan, qubitron.ParamResolver({'a': 0.1}))


def test_bounded_effect():
    qubits = qubitron.LineQubit.range(3)
    cy = qubitron.ControlledOperation(qubits[:1], qubitron.Y(qubits[1]))
    assert qubitron.trace_distance_bound(cy**0.001) < 0.01
    foo = sympy.Symbol('foo')
    scy = qubitron.ControlledOperation(qubits[:1], qubitron.Y(qubits[1]) ** foo)
    assert qubitron.trace_distance_bound(scy) == 1.0
    assert qubitron.approx_eq(qubitron.trace_distance_bound(cy), 1.0)


def test_controlled_operation_gate():
    gate = qubitron.X.controlled(control_values=[0, 1], control_qid_shape=[2, 3])
    op = gate.on(qubitron.LineQubit(0), qubitron.LineQid(1, 3), qubitron.LineQubit(2))
    assert op.gate == gate

    class Gateless(qubitron.Operation):
        @property
        def qubits(self):
            return ()  # pragma: no cover

        def with_qubits(self, *new_qubits):
            return self  # pragma: no cover

        def _has_mixture_(self):
            return True

    op = Gateless().controlled_by(qubitron.LineQubit(0))
    assert op.gate is None


def test_controlled_mixture():
    a, b = qubitron.LineQubit.range(2)
    c_yes = qubitron.ControlledOperation(controls=[b], sub_operation=qubitron.phase_flip(0.25).on(a))
    assert qubitron.has_mixture(c_yes)
    assert qubitron.approx_eq(qubitron.mixture(c_yes), [(0.75, np.eye(4)), (0.25, qubitron.unitary(qubitron.CZ))])
