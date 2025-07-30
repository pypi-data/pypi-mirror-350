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
import sympy

import qubitron


def all_gates_of_type(m: qubitron.Moment, g: qubitron.Gateset):
    for op in m:
        if op not in g:
            return False
    return True


def assert_optimizes(before: qubitron.Circuit, expected: qubitron.Circuit, **kwargs):
    qubitron.testing.assert_same_circuits(
        qubitron.optimize_for_target_gateset(
            before, gateset=qubitron.SqrtIswapTargetGateset(**kwargs), ignore_failures=False
        ),
        expected,
    )


def assert_optimization_not_broken(
    circuit: qubitron.Circuit, required_sqrt_iswap_count: int | None = None
):
    c_new = qubitron.optimize_for_target_gateset(
        circuit,
        gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=required_sqrt_iswap_count),
        ignore_failures=False,
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )
    c_new = qubitron.optimize_for_target_gateset(
        circuit,
        gateset=qubitron.SqrtIswapTargetGateset(
            use_sqrt_iswap_inv=True, required_sqrt_iswap_count=required_sqrt_iswap_count
        ),
        ignore_failures=False,
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )


def test_convert_to_sqrt_iswap_preserving_moment_structure() -> None:
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
        c_orig, gateset=qubitron.SqrtIswapTargetGateset(), ignore_failures=True
    )

    assert c_orig[-2:] == c_new[-2:]
    c_orig, c_new = c_orig[:-2], c_new[:-2]

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, qubitron.Gateset(qubitron.PhasedXZGate))
            or all_gates_of_type(m, qubitron.Gateset(qubitron.SQRT_ISWAP))
        )
        for m in c_new
    )

    c_new = qubitron.optimize_for_target_gateset(
        c_orig, gateset=qubitron.SqrtIswapTargetGateset(use_sqrt_iswap_inv=True), ignore_failures=False
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, qubitron.Gateset(qubitron.PhasedXZGate))
            or all_gates_of_type(m, qubitron.Gateset(qubitron.SQRT_ISWAP_INV))
        )
        for m in c_new
    )


@pytest.mark.parametrize(
    'gate',
    [
        qubitron.CNotPowGate(exponent=sympy.Symbol('t')),
        qubitron.PhasedFSimGate(theta=sympy.Symbol('t'), chi=sympy.Symbol('t'), phi=sympy.Symbol('t')),
    ],
)
@pytest.mark.parametrize('use_sqrt_iswap_inv', [True, False])
def test_two_qubit_gates_with_symbols(gate: qubitron.Gate, use_sqrt_iswap_inv: bool) -> None:
    # Note that even though these gates are not natively supported by
    # `qubitron.parameterized_2q_op_to_sqrt_iswap_operations`, the transformation succeeds because
    # `qubitron.optimize_for_target_gateset` also relies on `qubitron.decompose` as a fallback.

    c_orig = qubitron.Circuit(gate(*qubitron.LineQubit.range(2)))
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=qubitron.SqrtIswapTargetGateset(
            use_sqrt_iswap_inv=use_sqrt_iswap_inv,
            additional_gates=[qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate],
        ),
        ignore_failures=False,
    )

    # Check that `c_new` only contains sqrt iswap as the 2q entangling gate.
    sqrt_iswap_gate = qubitron.SQRT_ISWAP_INV if use_sqrt_iswap_inv else qubitron.SQRT_ISWAP
    for op in c_new.all_operations():
        if qubitron.num_qubits(op) == 2:
            assert op.gate == sqrt_iswap_gate

    # Check if unitaries are the same
    for val in np.linspace(0, 2 * np.pi, 10):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.resolve_parameters(c_orig, {'t': val}),
            qubitron.resolve_parameters(c_new, {'t': val}),
            atol=1e-6,
        )


def test_sqrt_iswap_gateset_raises() -> None:
    with pytest.raises(ValueError, match="`required_sqrt_iswap_count` must be 0, 1, 2, or 3"):
        _ = qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=4)


def test_sqrt_iswap_gateset_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.SqrtIswapTargetGateset(), qubitron.SqrtIswapTargetGateset(use_sqrt_iswap_inv=False)
    )
    eq.add_equality_group(
        qubitron.SqrtIswapTargetGateset(atol=1e-6, required_sqrt_iswap_count=0, use_sqrt_iswap_inv=True)
    )
    eq.add_equality_group(
        qubitron.SqrtIswapTargetGateset(atol=1e-6, required_sqrt_iswap_count=3, use_sqrt_iswap_inv=True)
    )
    eq.add_equality_group(qubitron.SqrtIswapTargetGateset(additional_gates=[qubitron.XPowGate]))


@pytest.mark.parametrize(
    'gateset',
    [
        qubitron.SqrtIswapTargetGateset(),
        qubitron.SqrtIswapTargetGateset(
            atol=1e-6,
            required_sqrt_iswap_count=2,
            use_sqrt_iswap_inv=True,
            additional_gates=[
                qubitron.CZ,
                qubitron.XPowGate,
                qubitron.YPowGate,
                qubitron.GateFamily(qubitron.ZPowGate, tags_to_accept=['test_tag']),
            ],
        ),
        qubitron.SqrtIswapTargetGateset(additional_gates=()),
    ],
)
def test_sqrt_iswap_gateset_repr(gateset) -> None:
    qubitron.testing.assert_equivalent_repr(gateset)


def test_simplifies_sqrt_iswap() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimizes(
        before=qubitron.Circuit(
            [
                # SQRT_ISWAP**8 == Identity
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
            ]
        ),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.SQRT_ISWAP(a, b)])]),
    )


def test_simplifies_sqrt_iswap_inv() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimizes(
        use_sqrt_iswap_inv=True,
        before=qubitron.Circuit(
            [
                # SQRT_ISWAP**8 == Identity
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP_INV(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b)]),
            ]
        ),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.SQRT_ISWAP_INV(a, b)])]),
    )


def test_works_with_tags() -> None:
    a, b = qubitron.LineQubit.range(2)
    assert_optimizes(
        before=qubitron.Circuit(
            [
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b).with_tags('mytag1')]),
                qubitron.Moment([qubitron.SQRT_ISWAP(a, b).with_tags('mytag2')]),
                qubitron.Moment([qubitron.SQRT_ISWAP_INV(a, b).with_tags('mytag3')]),
            ]
        ),
        expected=qubitron.Circuit([qubitron.Moment([qubitron.SQRT_ISWAP(a, b)])]),
    )


def test_no_touch_single_sqrt_iswap() -> None:
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment(
                [qubitron.ISwapPowGate(exponent=0.5, global_shift=-0.5).on(a, b).with_tags('mytag')]
            )
        ]
    )
    assert_optimizes(before=circuit, expected=circuit)


def test_no_touch_single_sqrt_iswap_inv() -> None:
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment(
                [qubitron.ISwapPowGate(exponent=-0.5, global_shift=-0.5).on(a, b).with_tags('mytag')]
            )
        ]
    )
    assert_optimizes(before=circuit, expected=circuit, use_sqrt_iswap_inv=True)


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
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_single_inv_sqrt_iswap() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SQRT_ISWAP_INV(a, b))
    assert_optimization_not_broken(c)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 1


def test_optimizes_single_iswap_require0() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.CNOT(a, b), qubitron.CNOT(a, b))  # Minimum 0 sqrt-iSWAP
    assert_optimization_not_broken(c, required_sqrt_iswap_count=0)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=0), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 0


def test_optimizes_single_iswap_require0_raises() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.CNOT(a, b))  # Minimum 2 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 0 sqrt-iSWAP gates'):
        _ = qubitron.optimize_for_target_gateset(
            c,
            gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=0),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require1() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SQRT_ISWAP_INV(a, b))  # Minimum 1 sqrt-iSWAP
    assert_optimization_not_broken(c, required_sqrt_iswap_count=1)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=1), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 1


def test_optimizes_single_iswap_require1_raises() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.CNOT(a, b))  # Minimum 2 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 1 sqrt-iSWAP gates'):
        c = qubitron.optimize_for_target_gateset(
            c,
            gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=1),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require2() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SQRT_ISWAP_INV(a, b))  # Minimum 1 sqrt-iSWAP but 2 possible
    assert_optimization_not_broken(c, required_sqrt_iswap_count=2)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=2), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_single_iswap_require2_raises() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SWAP(a, b))  # Minimum 3 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 2 sqrt-iSWAP gates'):
        c = qubitron.optimize_for_target_gateset(
            c,
            gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=2),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require3() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.ISWAP(a, b))  # Minimum 2 sqrt-iSWAP but 3 possible
    assert_optimization_not_broken(c, required_sqrt_iswap_count=3)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=3), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 3


def test_optimizes_single_inv_sqrt_iswap_require3() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(qubitron.SQRT_ISWAP_INV(a, b))
    assert_optimization_not_broken(c, required_sqrt_iswap_count=3)
    c = qubitron.optimize_for_target_gateset(
        c, gateset=qubitron.SqrtIswapTargetGateset(required_sqrt_iswap_count=3), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 3
