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

import numpy as np
import pytest
import sympy

import qubitron


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [
        (qubitron.testing.SingleQubitGate(), 2, qubitron.LineQubit.range(2)),
        (qubitron.X**0.5, 4, qubitron.LineQubit.range(4)),
    ],
)
def test_parallel_gate_operation_init(gate, num_copies, qubits) -> None:
    v = qubitron.ParallelGate(gate, num_copies)
    assert v.sub_gate == gate
    assert v.num_copies == num_copies
    assert v.on(*qubits).qubits == tuple(qubits)


@pytest.mark.parametrize(
    'gate, num_copies, qubits, error_msg',
    [
        (qubitron.testing.SingleQubitGate(), 3, qubitron.LineQubit.range(2), "Wrong number of qubits"),
        (
            qubitron.testing.SingleQubitGate(),
            0,
            qubitron.LineQubit.range(4),
            "gate must be applied at least once",
        ),
        (
            qubitron.testing.SingleQubitGate(),
            2,
            [qubitron.NamedQubit("a"), qubitron.NamedQubit("a")],
            "Duplicate",
        ),
        (qubitron.testing.TwoQubitGate(), 2, qubitron.LineQubit.range(4), "must be a single qubit gate"),
    ],
)
def test_invalid_parallel_gate_operation(gate, num_copies, qubits, error_msg) -> None:
    with pytest.raises(ValueError, match=error_msg):
        qubitron.ParallelGate(gate, num_copies)(*qubits)


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [(qubitron.X, 2, qubitron.LineQubit.range(2)), (qubitron.H**0.5, 4, qubitron.LineQubit.range(4))],
)
def test_decompose(gate, num_copies, qubits) -> None:
    g = qubitron.ParallelGate(gate, num_copies)
    step = gate.num_qubits()
    qubit_lists = [qubits[i * step : (i + 1) * step] for i in range(num_copies)]
    assert set(qubitron.decompose_once(g(*qubits))) == set(gate.on_each(qubit_lists))


def test_decompose_raises() -> None:
    g = qubitron.ParallelGate(qubitron.X, 2)
    qubits = qubitron.LineQubit.range(4)
    with pytest.raises(ValueError, match=r'len\(qubits\)=4 should be 2'):
        qubitron.decompose_once_with_qubits(g, qubits)


def test_with_num_copies() -> None:
    g = qubitron.testing.SingleQubitGate()
    pg = qubitron.ParallelGate(g, 3)
    assert pg.with_num_copies(5) == qubitron.ParallelGate(g, 5)


def test_extrapolate() -> None:
    # If the gate isn't extrapolatable, you get a type error.
    g = qubitron.ParallelGate(qubitron.testing.SingleQubitGate(), 2)
    with pytest.raises(TypeError):
        _ = g**0.5
    # If the gate is extrapolatable, the effect is applied on the underlying gate.
    g = qubitron.ParallelGate(qubitron.Y, 2)
    assert g**0.5 == qubitron.ParallelGate(qubitron.Y**0.5, 2)
    assert qubitron.inverse(g) == g**-1 == qubitron.ParallelGate(qubitron.Y**-1, 2)


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterizable_gates(resolve_fn) -> None:
    r = qubitron.ParamResolver({'a': 0.5})
    g1 = qubitron.ParallelGate(qubitron.Z ** sympy.Symbol('a'), 2)
    assert qubitron.is_parameterized(g1)
    g2 = resolve_fn(g1, r)
    assert not qubitron.is_parameterized(g2)


@pytest.mark.parametrize('gate', [qubitron.X ** sympy.Symbol("a"), qubitron.testing.SingleQubitGate()])
def test_no_unitary(gate) -> None:
    g = qubitron.ParallelGate(gate, 2)
    assert not qubitron.has_unitary(g)
    assert qubitron.unitary(g, None) is None


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [
        (qubitron.X**0.5, 2, qubitron.LineQubit.range(2)),
        (qubitron.MatrixGate(qubitron.unitary(qubitron.H**0.25)), 6, qubitron.LineQubit.range(6)),
    ],
)
def test_unitary(gate, num_copies, qubits) -> None:
    g = qubitron.ParallelGate(gate, num_copies)
    step = gate.num_qubits()
    qubit_lists = [qubits[i * step : (i + 1) * step] for i in range(num_copies)]
    np.testing.assert_allclose(
        qubitron.unitary(g), qubitron.unitary(qubitron.Circuit(gate.on_each(qubit_lists))), atol=1e-8
    )


def test_not_implemented_diagram() -> None:
    q = qubitron.LineQubit.range(2)
    g = qubitron.testing.SingleQubitGate()
    c = qubitron.Circuit()
    c.append(qubitron.ParallelGate(g, 2)(*q))
    assert 'qubitron.testing.gate_features.SingleQubitGate ' in str(c)


def test_repr() -> None:
    assert repr(qubitron.ParallelGate(qubitron.X, 2)) == 'qubitron.ParallelGate(sub_gate=qubitron.X, num_copies=2)'


def test_str() -> None:
    assert str(qubitron.ParallelGate(qubitron.X**0.5, 10)) == 'X**0.5 x 10'


def test_equivalent_circuit() -> None:
    qreg = qubitron.LineQubit.range(4)
    oldc = qubitron.Circuit()
    newc = qubitron.Circuit()
    single_qubit_gates = [qubitron.X ** (1 / 2), qubitron.Y ** (1 / 3), qubitron.Z**-1]
    for gate in single_qubit_gates:
        for qubit in qreg:
            oldc.append(gate.on(qubit))
        newc.append(qubitron.ParallelGate(gate, 4)(*qreg))
    qubitron.testing.assert_has_diagram(newc, oldc.to_text_diagram())
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(oldc, newc, atol=1e-6)


@pytest.mark.parametrize('gate, num_copies', [(qubitron.X, 1), (qubitron.Y, 2), (qubitron.Z, 3), (qubitron.H, 4)])
def test_parallel_gate_operation_is_consistent(gate, num_copies) -> None:
    qubitron.testing.assert_implements_consistent_protocols(qubitron.ParallelGate(gate, num_copies))


def test_trace_distance() -> None:
    s = qubitron.X**0.25
    two_g = qubitron.ParallelGate(s, 2)
    three_g = qubitron.ParallelGate(s, 3)
    four_g = qubitron.ParallelGate(s, 4)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(two_g), np.sin(np.pi / 4))
    assert qubitron.approx_eq(qubitron.trace_distance_bound(three_g), np.sin(3 * np.pi / 8))
    assert qubitron.approx_eq(qubitron.trace_distance_bound(four_g), 1.0)
    spg = qubitron.ParallelGate(qubitron.X ** sympy.Symbol('a'), 4)
    assert qubitron.approx_eq(qubitron.trace_distance_bound(spg), 1.0)


@pytest.mark.parametrize('gate, num_copies', [(qubitron.X, 1), (qubitron.Y, 2), (qubitron.Z, 3), (qubitron.H, 4)])
def test_parallel_gate_op(gate, num_copies) -> None:
    qubits = qubitron.LineQubit.range(num_copies * gate.num_qubits())
    assert qubitron.parallel_gate_op(gate, *qubits) == qubitron.ParallelGate(gate, num_copies).on(*qubits)
