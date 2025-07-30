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

import collections.abc
import pathlib

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


def test_gate_operation_init():
    q = qubitron.NamedQubit('q')
    g = qubitron.testing.SingleQubitGate()
    v = qubitron.GateOperation(g, (q,))
    assert v.gate == g
    assert v.qubits == (q,)


def test_invalid_gate_operation():
    three_qubit_gate = qubitron.testing.ThreeQubitGate()
    single_qubit = [qubitron.GridQubit(0, 0)]
    with pytest.raises(ValueError, match="number of qubits"):
        qubitron.GateOperation(three_qubit_gate, single_qubit)


def test_immutable():
    a, b = qubitron.LineQubit.range(2)
    op = qubitron.X(a)

    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|"
        "(property 'gate' of 'SingleQubitPauliStringGateOperation' object has no setter)",
    ):
        op.gate = qubitron.Y

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|"
        "(property 'qubits' of 'SingleQubitPauliStringGateOperation' object has no setter)",
    ):
        op.qubits = [b]


def test_gate_operation_eq():
    g1 = qubitron.testing.SingleQubitGate()
    g2 = qubitron.testing.SingleQubitGate()
    g3 = qubitron.testing.TwoQubitGate()
    r1 = [qubitron.NamedQubit('r1')]
    r2 = [qubitron.NamedQubit('r2')]
    r12 = r1 + r2
    r21 = r2 + r1

    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(lambda: qubitron.GateOperation(g1, r1))
    eq.make_equality_group(lambda: qubitron.GateOperation(g2, r1))
    eq.make_equality_group(lambda: qubitron.GateOperation(g1, r2))
    eq.make_equality_group(lambda: qubitron.GateOperation(g3, r12))
    eq.make_equality_group(lambda: qubitron.GateOperation(g3, r21))
    eq.add_equality_group(qubitron.GateOperation(qubitron.CZ, r21), qubitron.GateOperation(qubitron.CZ, r12))

    @qubitron.value_equality
    class PairGate(qubitron.Gate, qubitron.InterchangeableQubitsGate):
        """Interchangeable subsets."""

        def __init__(self, num_qubits):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def qubit_index_to_equivalence_group_key(self, index: int):
            return index // 2

        def _value_equality_values_(self):
            return (self.num_qubits(),)

    def p(*q):
        return PairGate(len(q)).on(*q)

    a0, a1, b0, b1, c0 = qubitron.LineQubit.range(5)
    eq.add_equality_group(p(a0, a1, b0, b1), p(a1, a0, b1, b0))
    eq.add_equality_group(p(b0, b1, a0, a1))
    eq.add_equality_group(p(a0, a1, b0, b1, c0), p(a1, a0, b1, b0, c0))
    eq.add_equality_group(p(a0, b0, a1, b1, c0))
    eq.add_equality_group(p(a0, c0, b0, b1, a1))
    eq.add_equality_group(p(b0, a1, a0, b1, c0))


def test_gate_operation_approx_eq():
    a = [qubitron.NamedQubit('r1')]
    b = [qubitron.NamedQubit('r2')]

    assert qubitron.approx_eq(
        qubitron.GateOperation(qubitron.XPowGate(), a), qubitron.GateOperation(qubitron.XPowGate(), a)
    )
    assert not qubitron.approx_eq(
        qubitron.GateOperation(qubitron.XPowGate(), a), qubitron.GateOperation(qubitron.XPowGate(), b)
    )

    assert qubitron.approx_eq(
        qubitron.GateOperation(qubitron.XPowGate(exponent=0), a),
        qubitron.GateOperation(qubitron.XPowGate(exponent=1e-9), a),
    )
    assert not qubitron.approx_eq(
        qubitron.GateOperation(qubitron.XPowGate(exponent=0), a),
        qubitron.GateOperation(qubitron.XPowGate(exponent=1e-7), a),
    )
    assert qubitron.approx_eq(
        qubitron.GateOperation(qubitron.XPowGate(exponent=0), a),
        qubitron.GateOperation(qubitron.XPowGate(exponent=1e-7), a),
        atol=1e-6,
    )


def test_gate_operation_qid_shape():
    class ShapeGate(qubitron.Gate):
        def _qid_shape_(self):
            return (1, 2, 3, 4)

    op = ShapeGate().on(*qubitron.LineQid.for_qid_shape((1, 2, 3, 4)))
    assert qubitron.qid_shape(op) == (1, 2, 3, 4)
    assert qubitron.num_qubits(op) == 4


def test_gate_operation_num_qubits():
    class NumQubitsGate(qubitron.Gate):
        def _num_qubits_(self):
            return 4

    op = NumQubitsGate().on(*qubitron.LineQubit.range(4))
    assert qubitron.qid_shape(op) == (2, 2, 2, 2)
    assert qubitron.num_qubits(op) == 4


def test_gate_operation_pow():
    Y = qubitron.Y
    q = qubitron.NamedQubit('q')
    assert (Y**0.5)(q) == Y(q) ** 0.5


def test_with_qubits_and_transform_qubits():
    g = qubitron.testing.ThreeQubitGate()
    g = qubitron.testing.ThreeQubitGate()
    op = qubitron.GateOperation(g, qubitron.LineQubit.range(3))
    assert op.with_qubits(*qubitron.LineQubit.range(3, 0, -1)) == qubitron.GateOperation(
        g, qubitron.LineQubit.range(3, 0, -1)
    )
    assert op.transform_qubits(lambda e: qubitron.LineQubit(-e.x)) == qubitron.GateOperation(
        g, [qubitron.LineQubit(0), qubitron.LineQubit(-1), qubitron.LineQubit(-2)]
    )


def test_extrapolate():
    q = qubitron.NamedQubit('q')

    # If the gate isn't extrapolatable, you get a type error.
    op0 = qubitron.GateOperation(qubitron.testing.SingleQubitGate(), [q])
    with pytest.raises(TypeError):
        _ = op0**0.5

    op1 = qubitron.GateOperation(qubitron.Y, [q])
    assert op1**0.5 == qubitron.GateOperation(qubitron.Y**0.5, [q])
    assert (qubitron.Y**0.5).on(q) == qubitron.Y(q) ** 0.5


def test_inverse():
    q = qubitron.NamedQubit('q')

    # If the gate isn't reversible, you get a type error.
    op0 = qubitron.GateOperation(qubitron.testing.SingleQubitGate(), [q])
    assert qubitron.inverse(op0, None) is None

    op1 = qubitron.GateOperation(qubitron.S, [q])
    assert qubitron.inverse(op1) == op1**-1 == qubitron.GateOperation(qubitron.S**-1, [q])
    assert qubitron.inverse(qubitron.S).on(q) == qubitron.inverse(qubitron.S.on(q))


def test_text_diagrammable():
    q = qubitron.NamedQubit('q')

    # If the gate isn't diagrammable, you get a type error.
    op0 = qubitron.GateOperation(qubitron.testing.SingleQubitGate(), [q])
    with pytest.raises(TypeError):
        _ = qubitron.circuit_diagram_info(op0)

    op1 = qubitron.GateOperation(qubitron.S, [q])
    actual = qubitron.circuit_diagram_info(op1)
    expected = qubitron.circuit_diagram_info(qubitron.S)
    assert actual == expected


def test_bounded_effect():
    q = qubitron.NamedQubit('q')

    # If the gate isn't bounded, you get a type error.
    op0 = qubitron.GateOperation(qubitron.testing.SingleQubitGate(), [q])
    assert qubitron.trace_distance_bound(op0) >= 1
    op1 = qubitron.GateOperation(qubitron.Z**0.000001, [q])
    op1_bound = qubitron.trace_distance_bound(op1)
    assert op1_bound == qubitron.trace_distance_bound(qubitron.Z**0.000001)


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterizable_effect(resolve_fn):
    q = qubitron.NamedQubit('q')
    r = qubitron.ParamResolver({'a': 0.5})

    op1 = qubitron.GateOperation(qubitron.Z ** sympy.Symbol('a'), [q])
    assert qubitron.is_parameterized(op1)
    op2 = resolve_fn(op1, r)
    assert not qubitron.is_parameterized(op2)
    assert op2 == qubitron.S.on(q)


def test_pauli_expansion():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert qubitron.pauli_expansion(qubitron.X(a)) == qubitron.LinearDict({'X': 1})
    assert qubitron.pauli_expansion(qubitron.CNOT(a, b)) == qubitron.pauli_expansion(qubitron.CNOT)

    class No(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

    class Yes(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _pauli_expansion_(self):
            return qubitron.LinearDict({'X': 0.5})

    assert qubitron.pauli_expansion(No().on(a), default=None) is None
    assert qubitron.pauli_expansion(Yes().on(a)) == qubitron.LinearDict({'X': 0.5})


def test_unitary():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    assert not qubitron.has_unitary(qubitron.measure(a))
    assert qubitron.unitary(qubitron.measure(a), None) is None
    np.testing.assert_allclose(qubitron.unitary(qubitron.X(a)), np.array([[0, 1], [1, 0]]), atol=1e-8)
    np.testing.assert_allclose(qubitron.unitary(qubitron.CNOT(a, b)), qubitron.unitary(qubitron.CNOT), atol=1e-8)


def test_channel():
    a = qubitron.NamedQubit('a')
    op = qubitron.bit_flip(0.5).on(a)
    np.testing.assert_allclose(qubitron.kraus(op), qubitron.kraus(op.gate))
    assert qubitron.has_kraus(op)

    assert qubitron.kraus(qubitron.testing.SingleQubitGate()(a), None) is None
    assert not qubitron.has_kraus(qubitron.testing.SingleQubitGate()(a))


def test_measurement_key():
    a = qubitron.NamedQubit('a')
    assert qubitron.measurement_key_name(qubitron.measure(a, key='lock')) == 'lock'


def assert_mixtures_equal(actual, expected):
    """Assert equal for tuple of mixed scalar and array types."""
    for a, e in zip(actual, expected):
        np.testing.assert_almost_equal(a[0], e[0])
        np.testing.assert_almost_equal(a[1], e[1])


def test_mixture():
    a = qubitron.NamedQubit('a')
    op = qubitron.bit_flip(0.5).on(a)
    assert_mixtures_equal(qubitron.mixture(op), qubitron.mixture(op.gate))
    assert qubitron.has_mixture(op)

    assert qubitron.has_mixture(qubitron.X(a))
    m = qubitron.mixture(qubitron.X(a))
    assert len(m) == 1
    assert m[0][0] == 1
    np.testing.assert_allclose(m[0][1], qubitron.unitary(qubitron.X))


def test_repr():
    a, b = qubitron.LineQubit.range(2)
    assert (
        repr(qubitron.GateOperation(qubitron.CZ, (a, b))) == 'qubitron.CZ(qubitron.LineQubit(0), qubitron.LineQubit(1))'
    )

    class Inconsistent(qubitron.testing.SingleQubitGate):
        def __repr__(self):
            return 'Inconsistent'

        def on(self, *qubits):
            return qubitron.GateOperation(Inconsistent(), qubits)

    assert (
        repr(qubitron.GateOperation(Inconsistent(), [a]))
        == 'qubitron.GateOperation(gate=Inconsistent, qubits=[qubitron.LineQubit(0)])'
    )


@pytest.mark.parametrize(
    'gate1,gate2,eq_up_to_global_phase',
    [
        (qubitron.rz(0.3 * np.pi), qubitron.Z**0.3, True),
        (qubitron.rz(0.3), qubitron.Z**0.3, False),
        (qubitron.ZZPowGate(global_shift=0.5), qubitron.ZZ, True),
        (qubitron.ZPowGate(global_shift=0.5) ** sympy.Symbol('e'), qubitron.Z, False),
        (qubitron.Z ** sympy.Symbol('e'), qubitron.Z ** sympy.Symbol('f'), False),
    ],
)
def test_equal_up_to_global_phase_on_gates(gate1, gate2, eq_up_to_global_phase):
    num_qubits1, num_qubits2 = (qubitron.num_qubits(g) for g in (gate1, gate2))
    qubits = qubitron.LineQubit.range(max(num_qubits1, num_qubits2) + 1)
    op1, op2 = gate1(*qubits[:num_qubits1]), gate2(*qubits[:num_qubits2])
    assert qubitron.equal_up_to_global_phase(op1, op2) == eq_up_to_global_phase
    op2_on_diff_qubits = gate2(*qubits[1 : num_qubits2 + 1])
    assert not qubitron.equal_up_to_global_phase(op1, op2_on_diff_qubits)


def test_equal_up_to_global_phase_on_diff_types():
    op = qubitron.X(qubitron.LineQubit(0))
    assert not qubitron.equal_up_to_global_phase(op, 3)


def test_gate_on_operation_besides_gate_operation():
    a, b = qubitron.LineQubit.range(2)

    op = -1j * qubitron.X(a) * qubitron.Y(b)
    assert isinstance(op.gate, qubitron.DensePauliString)
    assert op.gate == -1j * qubitron.DensePauliString('XY')
    assert not isinstance(op.gate, qubitron.XPowGate)


def test_mul():
    class GateRMul(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _rmul_with_qubits(self, qubits, other):
            if other == 2:
                return 3
            if isinstance(other, qubitron.Operation) and isinstance(other.gate, GateRMul):
                return 4
            raise NotImplementedError()

    class GateMul(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _mul_with_qubits(self, qubits, other):
            if other == 2:
                return 5
            if isinstance(other, qubitron.Operation) and isinstance(other.gate, GateMul):
                return 6
            raise NotImplementedError()

    # Delegates right multiplication.
    q = qubitron.LineQubit(0)
    r = GateRMul().on(q)
    assert 2 * r == 3
    with pytest.raises(TypeError):
        _ = r * 2

    # Delegates left multiplication.
    m = GateMul().on(q)
    assert m * 2 == 5
    with pytest.raises(TypeError):
        _ = 2 * m

    # Handles the symmetric type case correctly.
    assert m * m == 6
    assert r * r == 4


def test_with_gate():
    g1 = qubitron.GateOperation(qubitron.X, qubitron.LineQubit.range(1))
    g2 = qubitron.GateOperation(qubitron.Y, qubitron.LineQubit.range(1))
    assert g1.with_gate(qubitron.X) is g1
    assert g1.with_gate(qubitron.Y) == g2


def test_with_measurement_key_mapping():
    a = qubitron.LineQubit(0)
    op = qubitron.measure(a, key='m')

    remap_op = qubitron.with_measurement_key_mapping(op, {'m': 'k'})
    assert qubitron.measurement_key_names(remap_op) == {'k'}
    assert qubitron.with_measurement_key_mapping(op, {'x': 'k'}) is op


def test_with_key_path():
    a = qubitron.LineQubit(0)
    op = qubitron.measure(a, key='m')

    remap_op = qubitron.with_key_path(op, ('a', 'b'))
    assert qubitron.measurement_key_names(remap_op) == {'a:b:m'}
    assert qubitron.with_key_path(remap_op, ('a', 'b')) is remap_op

    assert qubitron.with_key_path(op, tuple()) is op

    assert qubitron.with_key_path(qubitron.X(a), ('a', 'b')) is NotImplemented


def test_with_key_path_prefix():
    a = qubitron.LineQubit(0)
    op = qubitron.measure(a, key='m')
    remap_op = qubitron.with_key_path_prefix(op, ('a', 'b'))
    assert qubitron.measurement_key_names(remap_op) == {'a:b:m'}
    assert qubitron.with_key_path_prefix(remap_op, tuple()) is remap_op
    assert qubitron.with_key_path_prefix(op, tuple()) is op
    assert qubitron.with_key_path_prefix(qubitron.X(a), ('a', 'b')) is NotImplemented


def test_cannot_remap_non_measurement_gate():
    a = qubitron.LineQubit(0)
    op = qubitron.X(a)

    assert qubitron.with_measurement_key_mapping(op, {'m': 'k'}) is NotImplemented


def test_is_parameterized():
    class No1(qubitron.testing.SingleQubitGate):
        def num_qubits(self) -> int:
            return 1

    class No2(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _is_parameterized_(self):
            return False

    class Yes(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _is_parameterized_(self):
            return True

    q = qubitron.LineQubit(0)
    assert No1().num_qubits() == 1
    assert not qubitron.is_parameterized(No1().on(q))
    assert not qubitron.is_parameterized(No2().on(q))
    assert qubitron.is_parameterized(Yes().on(q))


def test_group_interchangeable_qubits_creates_tuples_with_unique_keys():
    class MyGate(qubitron.Gate, qubitron.InterchangeableQubitsGate):
        def __init__(self, num_qubits) -> None:
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def qubit_index_to_equivalence_group_key(self, index: int) -> int:
            if index % 2 == 0:
                return index
            return 0

    qubits = qubitron.LineQubit.range(4)
    gate = MyGate(len(qubits))

    assert gate(qubits[0], qubits[1], qubits[2], qubits[3]) == gate(
        qubits[3], qubits[1], qubits[2], qubits[0]
    )


def test_gate_to_operation_to_gate_round_trips():
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    # Only test gate subclasses in qubitron-core.
    gate_subclasses = {
        g
        for g in all_subclasses(qubitron.Gate)
        if g.__module__.startswith("qubitron.")
        and "contrib" not in g.__module__
        and "test" not in g.__module__
    }

    test_module_spec = qubitron.testing.json.spec_for("qubitron.protocols")

    skip_classes = {
        # Abstract or private parent classes.
        qubitron.ArithmeticGate,
        qubitron.BaseDensePauliString,
        qubitron.EigenGate,
        qubitron.Pauli,
        # Private gates.
        qubitron.transformers.analytical_decompositions.two_qubit_to_fsim._BGate,
        qubitron.transformers.measurement_transformers._ConfusionChannel,
        qubitron.transformers.measurement_transformers._ModAdd,
        qubitron.transformers.routing.visualize_routed_circuit._SwapPrintGate,
        qubitron.circuits.qasm_output.QasmTwoQubitGate,
        qubitron.ops.MSGate,
        # Interop gates
        qubitron.interop.quirk.QuirkQubitPermutationGate,
        qubitron.interop.quirk.QuirkArithmeticGate,
    }

    skipped = set()
    for gate_cls in gate_subclasses:
        filename = test_module_spec.test_data_path.joinpath(f"{gate_cls.__name__}.json")
        if pathlib.Path(filename).is_file():
            gates = qubitron.read_json(filename)
        else:
            if gate_cls in skip_classes:
                skipped.add(gate_cls)
                continue
            raise AssertionError(  # pragma: no cover
                f"{gate_cls} has no json file, please add a json file or add to the list of "
                "classes to be skipped if there is a reason this gate should not round trip "
                "to a gate via creating an operation."
            )

        if not isinstance(gates, collections.abc.Iterable):
            gates = [gates]
        for gate in gates:
            if gate.num_qubits():
                qudits = [qubitron.LineQid(i, d) for i, d in enumerate(qubitron.qid_shape(gate))]
                assert gate.on(*qudits).gate == gate

    assert (
        skipped == skip_classes
    ), "A gate that was supposed to be skipped was not, please update the list of skipped gates."
