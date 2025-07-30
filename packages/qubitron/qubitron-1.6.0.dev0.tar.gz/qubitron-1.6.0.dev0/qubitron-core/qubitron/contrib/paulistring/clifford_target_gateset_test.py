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

import pytest
import sympy

import qubitron
from qubitron.contrib.paulistring.clifford_target_gateset import CliffordTargetGateset


@pytest.mark.parametrize(
    'op,expected_ops',
    (
        lambda q0, q1: (
            (qubitron.X(q0), qubitron.SingleQubitCliffordGate.X(q0)),
            (qubitron.Y(q0), qubitron.SingleQubitCliffordGate.Y(q0)),
            (qubitron.Z(q0), qubitron.SingleQubitCliffordGate.Z(q0)),
            (qubitron.X(q0) ** 0.5, qubitron.SingleQubitCliffordGate.X_sqrt(q0)),
            (qubitron.Y(q0) ** 0.5, qubitron.SingleQubitCliffordGate.Y_sqrt(q0)),
            (qubitron.Z(q0) ** 0.5, qubitron.SingleQubitCliffordGate.Z_sqrt(q0)),
            (qubitron.X(q0) ** -0.5, qubitron.SingleQubitCliffordGate.X_nsqrt(q0)),
            (qubitron.Y(q0) ** -0.5, qubitron.SingleQubitCliffordGate.Y_nsqrt(q0)),
            (qubitron.Z(q0) ** -0.5, qubitron.SingleQubitCliffordGate.Z_nsqrt(q0)),
            (qubitron.X(q0) ** 0.25, qubitron.PauliStringPhasor(qubitron.PauliString([qubitron.X.on(q0)])) ** 0.25),
            (qubitron.Y(q0) ** 0.25, qubitron.PauliStringPhasor(qubitron.PauliString([qubitron.Y.on(q0)])) ** 0.25),
            (qubitron.Z(q0) ** 0.25, qubitron.PauliStringPhasor(qubitron.PauliString([qubitron.Z.on(q0)])) ** 0.25),
            (qubitron.X(q0) ** 0, ()),
            (qubitron.CZ(q0, q1), qubitron.CZ(q0, q1)),
            (qubitron.measure(q0, q1, key='key'), qubitron.measure(q0, q1, key='key')),
        )
    )(qubitron.LineQubit(0), qubitron.LineQubit(1)),
)
def test_converts_various_ops(op, expected_ops) -> None:
    before = qubitron.Circuit(op)
    expected = qubitron.Circuit(expected_ops, strategy=qubitron.InsertStrategy.EARLIEST)
    after = qubitron.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    assert after == expected
    qubitron.testing.assert_allclose_up_to_global_phase(
        before.unitary(), after.unitary(qubits_that_should_be_present=op.qubits), atol=1e-7
    )
    qubitron.testing.assert_allclose_up_to_global_phase(
        after.unitary(qubits_that_should_be_present=op.qubits),
        expected.unitary(qubits_that_should_be_present=op.qubits),
        atol=1e-7,
    )


def test_degenerate_single_qubit_decompose() -> None:
    q0 = qubitron.LineQubit(0)

    before = qubitron.Circuit(qubitron.Z(q0) ** 0.1, qubitron.X(q0) ** 1.0000000001, qubitron.Z(q0) ** 0.1)
    expected = qubitron.Circuit(qubitron.SingleQubitCliffordGate.X(q0))

    after = qubitron.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    assert after == expected
    qubitron.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)
    qubitron.testing.assert_allclose_up_to_global_phase(after.unitary(), expected.unitary(), atol=1e-7)


def test_converts_single_qubit_series() -> None:
    q0 = qubitron.LineQubit(0)

    before = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.Y(q0),
        qubitron.Z(q0),
        qubitron.X(q0) ** 0.5,
        qubitron.Y(q0) ** 0.5,
        qubitron.Z(q0) ** 0.5,
        qubitron.X(q0) ** -0.5,
        qubitron.Y(q0) ** -0.5,
        qubitron.Z(q0) ** -0.5,
        qubitron.X(q0) ** 0.25,
        qubitron.Y(q0) ** 0.25,
        qubitron.Z(q0) ** 0.25,
    )

    after = qubitron.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    qubitron.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)


def test_converts_single_qubit_then_two() -> None:
    q0, q1 = qubitron.LineQubit.range(2)

    before = qubitron.Circuit(qubitron.X(q0), qubitron.Y(q0), qubitron.CZ(q0, q1))

    after = qubitron.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    qubitron.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)


def test_converts_large_circuit() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)

    before = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.Y(q0),
        qubitron.Z(q0),
        qubitron.X(q0) ** 0.5,
        qubitron.Y(q0) ** 0.5,
        qubitron.Z(q0) ** 0.5,
        qubitron.X(q0) ** -0.5,
        qubitron.Y(q0) ** -0.5,
        qubitron.Z(q0) ** -0.5,
        qubitron.H(q0),
        qubitron.CZ(q0, q1),
        qubitron.CZ(q1, q2),
        qubitron.X(q0) ** 0.25,
        qubitron.Y(q0) ** 0.25,
        qubitron.Z(q0) ** 0.25,
        qubitron.CZ(q0, q1),
    )

    after = qubitron.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )

    qubitron.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)

    qubitron.testing.assert_has_diagram(
        after,
        '''
0: ───Y^0.5───@───[Z]^-0.304───[X]^(1/3)───[Z]^0.446───────@───
              │                                            │
1: ───────────@────────────────────────────────────────@───@───
                                                       │
2: ────────────────────────────────────────────────────@───────
''',
    )


def test_convert_to_pauli_string_phasors() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(qubitron.X(q0), qubitron.Y(q1) ** 0.25, qubitron.Z(q0) ** 0.125, qubitron.H(q1))
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.PAULI_STRING_PHASORS
        ),
    )

    qubitron.testing.assert_allclose_up_to_global_phase(c_new.unitary(), c_orig.unitary(), atol=1e-7)
    qubitron.testing.assert_has_diagram(
        c_new,
        """
0: ───[X]─────────[Z]^(1/8)───

1: ───[Y]^-0.25───[Z]─────────
""",
    )


def test_already_converted() -> None:
    q0 = qubitron.LineQubit(0)
    c_orig = qubitron.Circuit(qubitron.PauliStringPhasor(qubitron.X.on(q0)))
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.PAULI_STRING_PHASORS
        ),
        ignore_failures=False,
    )
    assert c_new == c_orig


def test_ignore_unsupported_gate() -> None:
    class UnsupportedGate(qubitron.testing.TwoQubitGate):
        pass

    q0, q1 = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(UnsupportedGate()(q0, q1), qubitron.X(q0) ** sympy.Symbol("theta"))
    c_new = qubitron.optimize_for_target_gateset(
        c_orig, gateset=CliffordTargetGateset(), ignore_failures=True
    )
    assert c_new == c_orig


def test_fail_unsupported_gate() -> None:
    class UnsupportedGate(qubitron.testing.TwoQubitGate):
        pass

    q0, q1 = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(UnsupportedGate()(q0, q1))
    with pytest.raises(ValueError):
        _ = qubitron.optimize_for_target_gateset(
            c_orig, gateset=CliffordTargetGateset(), ignore_failures=False
        )


def test_convert_to_single_qubit_cliffords() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.X(q0), qubitron.Y(q1) ** 0.5, qubitron.Z(q0) ** -0.5, qubitron.Z(q1) ** 0, qubitron.H(q0)
    )
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.SINGLE_QUBIT_CLIFFORDS
        ),
        ignore_failures=True,
    )

    assert all(isinstance(op.gate, qubitron.SingleQubitCliffordGate) for op in c_new.all_operations())

    qubitron.testing.assert_allclose_up_to_global_phase(c_new.unitary(), c_orig.unitary(), atol=1e-7)

    qubitron.testing.assert_has_diagram(
        c_new,
        """
0: ───(X^-0.5-Z^0.5)───

1: ───Y^0.5────────────
""",
    )


def test_convert_to_single_qubit_cliffords_ignores_non_clifford() -> None:
    q0 = qubitron.LineQubit(0)
    c_orig = qubitron.Circuit(qubitron.Z(q0) ** 0.25)
    c_new = qubitron.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.SINGLE_QUBIT_CLIFFORDS
        ),
        ignore_failures=True,
    )
    assert c_orig == c_new
