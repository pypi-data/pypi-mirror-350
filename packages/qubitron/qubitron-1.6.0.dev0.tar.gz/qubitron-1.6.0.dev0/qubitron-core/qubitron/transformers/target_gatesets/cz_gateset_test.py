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

from typing import Sequence

import numpy as np
import pytest
import sympy

import qubitron


def all_gates_of_type(m: qubitron.Moment, g: qubitron.Gateset):
    for op in m:
        if op not in g:
            return False
    return True


def assert_optimizes(
    before: qubitron.Circuit,
    expected: qubitron.Circuit,
    additional_gates: Sequence[type[qubitron.Gate]] | None = None,
):
    if additional_gates is None:
        gateset = qubitron.CZTargetGateset()
    else:
        gateset = qubitron.CZTargetGateset(additional_gates=additional_gates)

    qubitron.testing.assert_same_circuits(
        qubitron.optimize_for_target_gateset(before, gateset=gateset, ignore_failures=False), expected
    )


def assert_optimization_not_broken(circuit: qubitron.Circuit):
    c_new = qubitron.optimize_for_target_gateset(circuit, gateset=qubitron.CZTargetGateset())
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )
    c_new = qubitron.optimize_for_target_gateset(
        circuit, gateset=qubitron.CZTargetGateset(allow_partial_czs=True), ignore_failures=False
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )


def test_convert_to_cz_preserving_moment_structure() -> None:
    q = qubitron.LineQubit.range(5)
    op = lambda q0, q1: qubitron.H(q1).controlled_by(q0)
    c_orig = qubitron.Circuit(
        qubitron.Moment(qubitron.X(q[2])),
        qubitron.Moment(op(q[0], q[1]), op(q[2], q[3])),
        qubitron.Moment(op(q[2], q[1]), op(q[4], q[3])),
        qubitron.Moment(op(q[1], q[2]), op(q[3], q[4])),
        qubitron.Moment(op(q[3], q[2]), op(q[1], q[0])),
        qubitron.measure(*q[:2], key="m"),
        qubitron.X(q[2]).with_classical_controls("m"),
        qubitron.CZ(*q[3:]).with_classical_controls("m"),
    )
    # Classically controlled operations are not part of the gateset, so failures should be ignored
    # during compilation.
    c_new = qubitron.optimize_for_target_gateset(
        c_orig, gateset=qubitron.CZTargetGateset(), ignore_failures=True
    )

    assert c_orig[-2:] == c_new[-2:]
    c_orig, c_new = c_orig[:-2], c_new[:-2]

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, qubitron.Gateset(qubitron.PhasedXZGate))
            or all_gates_of_type(m, qubitron.Gateset(qubitron.CZ))
        )
        for m in c_new
    )

    c_new = qubitron.optimize_for_target_gateset(
        c_orig, gateset=qubitron.CZTargetGateset(allow_partial_czs=True), ignore_failures=False
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, qubitron.Gateset(qubitron.PhasedXZGate))
            or all_gates_of_type(m, qubitron.Gateset(qubitron.CZPowGate))
        )
        for m in c_new
    )


def test_clears_paired_cnot() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimizes(
        before=qubitron.Circuit(qubitron.Moment(qubitron.CNOT(a, b)), qubitron.Moment(qubitron.CNOT(a, b))),
        expected=qubitron.Circuit(),
    )


def test_ignores_czs_separated_by_parameterized() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment(qubitron.CZ(a, b)),
                qubitron.Moment(qubitron.Z(a) ** sympy.Symbol('boo')),
                qubitron.Moment(qubitron.CZ(a, b)),
            ]
        ),
        expected=qubitron.Circuit(
            [
                qubitron.Moment(qubitron.CZ(a, b)),
                qubitron.Moment(qubitron.Z(a) ** sympy.Symbol('boo')),
                qubitron.Moment(qubitron.CZ(a, b)),
            ]
        ),
        additional_gates=[qubitron.ZPowGate],
    )


def test_cnots_separated_by_single_gates_correct() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimization_not_broken(qubitron.Circuit(qubitron.CNOT(a, b), qubitron.H(b), qubitron.CNOT(a, b)))


def test_czs_separated_by_single_gates_correct() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimization_not_broken(
        qubitron.Circuit(qubitron.CZ(a, b), qubitron.X(b), qubitron.X(b), qubitron.X(b), qubitron.CZ(a, b))
    )


def test_inefficient_circuit_correct() -> None:
    t = 0.1
    v = 0.11
    a, b = qubitron.LineQubit.range(2)
    assert_optimization_not_broken(
        qubitron.Circuit(
            qubitron.H(b),
            qubitron.CNOT(a, b),
            qubitron.H(b),
            qubitron.CNOT(a, b),
            qubitron.CNOT(b, a),
            qubitron.H(a),
            qubitron.CNOT(a, b),
            qubitron.Z(a) ** t,
            qubitron.Z(b) ** -t,
            qubitron.CNOT(a, b),
            qubitron.H(a),
            qubitron.Z(b) ** v,
            qubitron.CNOT(a, b),
            qubitron.Z(a) ** -v,
            qubitron.Z(b) ** -v,
        )
    )


def test_optimizes_single_iswap() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.ISWAP(a, b))
    assert_optimization_not_broken(c)
    c = qubitron.optimize_for_target_gateset(c, gateset=qubitron.CZTargetGateset(), ignore_failures=False)
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_tagged_partial_cz() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit((qubitron.CZ**0.5)(a, b).with_tags('mytag'))
    assert_optimization_not_broken(c)
    c = qubitron.optimize_for_target_gateset(c, gateset=qubitron.CZTargetGateset(), ignore_failures=False)
    assert (
        len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2
    ), 'It should take 2 CZ gates to decompose a CZ**0.5 gate'


def test_not_decompose_czs() -> None:
    circuit = qubitron.Circuit(
        qubitron.CZPowGate(exponent=1, global_shift=-0.5).on(*qubitron.LineQubit.range(2))
    )
    assert_optimizes(before=circuit, expected=circuit)


@pytest.mark.parametrize(
    'circuit',
    (
        qubitron.Circuit(qubitron.CZPowGate(exponent=0.1)(*qubitron.LineQubit.range(2))),
        qubitron.Circuit(
            qubitron.CZPowGate(exponent=0.2)(*qubitron.LineQubit.range(2)),
            qubitron.CZPowGate(exponent=0.3, global_shift=-0.5)(*qubitron.LineQubit.range(2)),
        ),
    ),
)
def test_decompose_partial_czs(circuit) -> None:
    circuit = qubitron.optimize_for_target_gateset(
        circuit, gateset=qubitron.CZTargetGateset(), ignore_failures=False
    )
    cz_gates = [
        op.gate
        for op in circuit.all_operations()
        if isinstance(op, qubitron.GateOperation) and isinstance(op.gate, qubitron.CZPowGate)
    ]
    num_full_cz = sum(1 for cz in cz_gates if cz.exponent % 2 == 1)
    num_part_cz = sum(1 for cz in cz_gates if cz.exponent % 2 != 1)
    assert num_full_cz == 2
    assert num_part_cz == 0


def test_not_decompose_partial_czs() -> None:
    circuit = qubitron.Circuit(
        qubitron.CZPowGate(exponent=0.1, global_shift=-0.5)(*qubitron.LineQubit.range(2))
    )
    qubitron.optimize_for_target_gateset(circuit, gateset=qubitron.CZTargetGateset(), ignore_failures=False)
    cz_gates = [
        op.gate
        for op in circuit.all_operations()
        if isinstance(op, qubitron.GateOperation) and isinstance(op.gate, qubitron.CZPowGate)
    ]
    num_full_cz = sum(1 for cz in cz_gates if cz.exponent % 2 == 1)
    num_part_cz = sum(1 for cz in cz_gates if cz.exponent % 2 != 1)
    assert num_full_cz == 0
    assert num_part_cz == 1


def test_avoids_decompose_when_matrix_available() -> None:
    class OtherXX(qubitron.testing.TwoQubitGate):  # pragma: no cover
        def _has_unitary_(self) -> bool:
            return True

        def _unitary_(self) -> np.ndarray:
            m = np.array([[0, 1], [1, 0]])
            return np.kron(m, m)

        def _decompose_(self, qubits):
            assert False

    class OtherOtherXX(qubitron.testing.TwoQubitGate):  # pragma: no cover
        def _has_unitary_(self) -> bool:
            return True

        def _unitary_(self) -> np.ndarray:
            m = np.array([[0, 1], [1, 0]])
            return np.kron(m, m)

        def _decompose_(self, qubits):
            assert False

    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(OtherXX()(a, b), OtherOtherXX()(a, b))
    c = qubitron.optimize_for_target_gateset(c, gateset=qubitron.CZTargetGateset(), ignore_failures=False)
    assert len(c) == 0


def test_composite_gates_without_matrix() -> None:
    class CompositeExample(qubitron.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            yield qubitron.X(qubits[0])
            yield qubitron.Y(qubits[0]) ** 0.5

    class CompositeExample2(qubitron.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            yield qubitron.CZ(qubits[0], qubits[1])
            yield CompositeExample()(qubits[1])

    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(CompositeExample()(q0), CompositeExample2()(q0, q1))
    expected = qubitron.Circuit(
        qubitron.X(q0), qubitron.Y(q0) ** 0.5, qubitron.CZ(q0, q1), qubitron.X(q1), qubitron.Y(q1) ** 0.5
    )
    c_new = qubitron.optimize_for_target_gateset(
        circuit, gateset=qubitron.CZTargetGateset(), ignore_failures=False
    )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_new, expected, atol=1e-6
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_new, circuit, atol=1e-6
    )


def test_unsupported_gate() -> None:
    class UnsupportedExample(qubitron.testing.TwoQubitGate):
        pass

    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(UnsupportedExample()(q0, q1))
    assert circuit == qubitron.optimize_for_target_gateset(circuit, gateset=qubitron.CZTargetGateset())
    with pytest.raises(ValueError, match='Unable to convert'):
        _ = qubitron.optimize_for_target_gateset(
            circuit, gateset=qubitron.CZTargetGateset(), ignore_failures=False
        )


@pytest.mark.parametrize(
    'gateset',
    [
        qubitron.CZTargetGateset(),
        qubitron.CZTargetGateset(
            atol=1e-6,
            allow_partial_czs=True,
            additional_gates=[
                qubitron.SQRT_ISWAP,
                qubitron.XPowGate,
                qubitron.YPowGate,
                qubitron.GateFamily(qubitron.ZPowGate, tags_to_accept=['test_tag']),
            ],
        ),
        qubitron.CZTargetGateset(additional_gates=()),
    ],
)
def test_repr(gateset) -> None:
    qubitron.testing.assert_equivalent_repr(gateset)


def test_with_commutation() -> None:
    c = qubitron.Circuit(
        qubitron.CZ(qubitron.q(0), qubitron.q(1)), qubitron.CZ(qubitron.q(1), qubitron.q(2)), qubitron.CZ(qubitron.q(0), qubitron.q(1))
    )
    got = qubitron.optimize_for_target_gateset(
        c,
        gateset=qubitron.CZTargetGateset(preserve_moment_structure=False, reorder_operations=True),
        max_num_passes=1,
    )
    assert got == qubitron.Circuit(qubitron.CZ(qubitron.q(1), qubitron.q(2)))


def test_reorder_operations_and_preserve_moment_structure_raises() -> None:
    with pytest.raises(
        ValueError, match='reorder_operations and preserve_moment_structure can not both be True'
    ):
        _ = qubitron.CZTargetGateset(preserve_moment_structure=True, reorder_operations=True)
