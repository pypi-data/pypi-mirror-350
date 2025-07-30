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
from sympy.parsing import sympy_parser

import qubitron
from qubitron.transformers.measurement_transformers import _ConfusionChannel, _MeasurementQid, _mod_add


def assert_equivalent_to_deferred(circuit: qubitron.Circuit):
    qubits = list(circuit.all_qubits())
    sim = qubitron.Simulator()
    num_qubits = len(qubits)
    dimensions = [q.dimension for q in qubits]
    for i in range(np.prod(dimensions)):
        bits = qubitron.big_endian_int_to_digits(i, base=dimensions)
        modified = qubitron.Circuit()
        for j in range(num_qubits):
            modified.append(qubitron.XPowGate(dimension=qubits[j].dimension)(qubits[j]) ** bits[j])
        modified.append(circuit)
        deferred = qubitron.defer_measurements(modified)
        result = sim.simulate(modified)
        result1 = sim.simulate(deferred)
        np.testing.assert_equal(result.measurements, result1.measurements)


def test_basic():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q_ma, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_qudits():
    q0, q1 = qubitron.LineQid.range(2, dimension=3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.XPowGate(dimension=3).on(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            _mod_add(q0, q_ma),
            qubitron.XPowGate(dimension=3).on(q1).controlled_by(q_ma, control_values=[[1, 2]]),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_sympy_control():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls(sympy.Symbol('a')),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q_ma, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_sympy_qudits():
    q0, q1 = qubitron.LineQid.range(2, dimension=3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.XPowGate(dimension=3).on(q1).with_classical_controls(sympy.Symbol('a')),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            _mod_add(q0, q_ma),
            qubitron.XPowGate(dimension=3).on(q1).controlled_by(q_ma, control_values=[[1, 2]]),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_sympy_control_complex():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, key='b'),
        qubitron.X(q2).with_classical_controls(sympy_parser.parse_expr('a >= b')),
        qubitron.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q1, q_mb),
            qubitron.ControlledOperation(
                [q_ma, q_mb], qubitron.X(q2), qubitron.SumOfProducts([[0, 0], [1, 0], [1, 1]])
            ),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q_mb, key='b'),
            qubitron.measure(q2, key='c'),
        ),
    )


def test_sympy_control_complex_qudit():
    q0, q1, q2 = qubitron.LineQid.for_qid_shape((4, 2, 2))
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, key='b'),
        qubitron.X(q2).with_classical_controls(sympy_parser.parse_expr('a > b')),
        qubitron.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            _mod_add(q0, q_ma),
            qubitron.CX(q1, q_mb),
            qubitron.ControlledOperation(
                [q_ma, q_mb],
                qubitron.X(q2),
                qubitron.SumOfProducts([[1, 0], [2, 0], [3, 0], [2, 1], [3, 1]]),
            ),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q_mb, key='b'),
            qubitron.measure(q2, key='c'),
        ),
    )


def test_multiple_sympy_control_complex():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, key='b'),
        qubitron.X(q2)
        .with_classical_controls(sympy_parser.parse_expr('a >= b'))
        .with_classical_controls(sympy_parser.parse_expr('a <= b')),
        qubitron.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q1, q_mb),
            qubitron.ControlledOperation(
                [q_ma, q_mb], qubitron.X(q2), qubitron.SumOfProducts([[0, 0], [1, 1]])
            ),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q_mb, key='b'),
            qubitron.measure(q2, key='c'),
        ),
    )


def test_sympy_and_key_control():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls(sympy.Symbol('a')).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q_ma, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_sympy_control_multiqubit():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, q1, key='a'),
        qubitron.X(q2).with_classical_controls(sympy_parser.parse_expr('a >= 2')),
        qubitron.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma0),
            qubitron.CX(q1, q_ma1),
            qubitron.ControlledOperation(
                [q_ma0, q_ma1], qubitron.X(q2), qubitron.SumOfProducts([[1, 0], [1, 1]])
            ),
            qubitron.measure(q_ma0, q_ma1, key='a'),
            qubitron.measure(q2, key='c'),
        ),
    )


def test_nocompile_context():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a').with_tags('nocompile'),
        qubitron.X(q1).with_classical_controls('a').with_tags('nocompile'),
        qubitron.measure(q1, key='b'),
    )
    deferred = qubitron.defer_measurements(
        circuit, context=qubitron.TransformerContext(tags_to_ignore=('nocompile',))
    )
    qubitron.testing.assert_same_circuits(deferred, circuit)


def test_nocompile_context_leaves_invalid_circuit():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a').with_tags('nocompile'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    with pytest.raises(ValueError, match='Deferred measurement for key=a not found'):
        _ = qubitron.defer_measurements(
            circuit, context=qubitron.TransformerContext(tags_to_ignore=('nocompile',))
        )


def test_pauli():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.PauliMeasurementGate(qubitron.DensePauliString('Y'), key='a').on(q0),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        qubitron.unroll_circuit_op(deferred),
        qubitron.Circuit(
            qubitron.SingleQubitCliffordGate.X_sqrt(q0),
            qubitron.CX(q0, q_ma),
            (qubitron.SingleQubitCliffordGate.X_sqrt(q0) ** -1),
            qubitron.Moment(qubitron.CX(q_ma, q1)),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_extra_measurements():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q0, key='b'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q_ma, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q0, key='b'),
            qubitron.measure(q1, key='c'),
        ),
    )


def test_extra_controlled_bits():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.CX(q0, q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CCX(q_ma, q0, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_extra_control_bits():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q0, key='b'),
        qubitron.X(q1).with_classical_controls('a', 'b'),
        qubitron.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.CX(q0, q_mb),
            qubitron.CCX(q_ma, q_mb, q1),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q_mb, key='b'),
            qubitron.measure(q1, key='c'),
        ),
    )


def test_subcircuit():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.measure(q0, key='a'),
                qubitron.X(q1).with_classical_controls('a'),
                qubitron.measure(q1, key='b'),
            )
        )
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_m = _MeasurementQid('a', q0)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_m),
            qubitron.CX(q_m, q1),
            qubitron.measure(q_m, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_multi_qubit_measurements():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, q1, key='a'),
        qubitron.X(q0),
        qubitron.measure(q0, key='b'),
        qubitron.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma0),
            qubitron.CX(q1, q_ma1),
            qubitron.X(q0),
            qubitron.measure(q_ma0, q_ma1, key='a'),
            qubitron.measure(q0, key='b'),
            qubitron.measure(q1, key='c'),
        ),
    )


def test_multi_qubit_control():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, q1, key='a'),
        qubitron.X(q2).with_classical_controls('a'),
        qubitron.measure(q2, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma0),
            qubitron.CX(q1, q_ma1),
            qubitron.X(q2).controlled_by(
                q_ma0, q_ma1, control_values=qubitron.SumOfProducts(((0, 1), (1, 0), (1, 1)))
            ),
            qubitron.measure(q_ma0, q_ma1, key='a'),
            qubitron.measure(q2, key='b'),
        ),
    )


@pytest.mark.parametrize('index', [-3, -2, -1, 0, 1, 2])
def test_repeated(index: int):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),  # The control measurement when `index` is 0 or -2
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),  # The control measurement when `index` is 1 or -1
        qubitron.X(q1).with_classical_controls(qubitron.KeyCondition(qubitron.MeasurementKey('a'), index)),
        qubitron.measure(q1, key='b'),
    )
    if index in [-3, 2]:
        with pytest.raises(ValueError, match='Invalid index'):
            _ = qubitron.defer_measurements(circuit)
        return
    assert_equivalent_to_deferred(circuit)
    deferred = qubitron.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)  # The ancilla qubit created for the first `a` measurement
    q_ma1 = _MeasurementQid('a', q0, 1)  # The ancilla qubit created for the second `a` measurement
    # The ancilla used for control should match the measurement used for control above.
    q_expected_control = q_ma if index in [0, -2] else q_ma1
    qubitron.testing.assert_same_circuits(
        deferred,
        qubitron.Circuit(
            qubitron.CX(q0, q_ma),
            qubitron.X(q0),
            qubitron.CX(q0, q_ma1),
            qubitron.Moment(qubitron.CX(q_expected_control, q1)),
            qubitron.measure(q_ma, key='a'),
            qubitron.measure(q_ma1, key='a'),
            qubitron.measure(q1, key='b'),
        ),
    )


def test_diagram():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, q2, key='a'),
        qubitron.measure(q1, q3, key='b'),
        qubitron.X(q0),
        qubitron.measure(q0, q1, q2, q3, key='c'),
    )
    deferred = qubitron.defer_measurements(circuit)
    qubitron.testing.assert_has_diagram(
        deferred,
        """
                      ┌────┐
0: ────────────────────@───────X────────M('c')───
                       │                │
1: ────────────────────┼─@──────────────M────────
                       │ │              │
2: ────────────────────┼@┼──────────────M────────
                       │││              │
3: ────────────────────┼┼┼@─────────────M────────
                       ││││
M('a[0]', q=q(0)): ────X┼┼┼────M('a')────────────
                        │││    │
M('a[0]', q=q(2)): ─────X┼┼────M─────────────────
                         ││
M('b[0]', q=q(1)): ──────X┼────M('b')────────────
                          │    │
M('b[0]', q=q(3)): ───────X────M─────────────────
                      └────┘
""",
        use_unicode_characters=True,
    )


def test_repr():
    def test_repr(qid: _MeasurementQid):
        qubitron.testing.assert_equivalent_repr(qid, global_vals={'_MeasurementQid': _MeasurementQid})

    test_repr(_MeasurementQid('a', qubitron.LineQubit(0)))
    test_repr(_MeasurementQid('a', qubitron.NamedQubit('x')))
    test_repr(_MeasurementQid('a', qubitron.NamedQid('x', 4)))
    test_repr(_MeasurementQid('a', qubitron.GridQubit(2, 3)))
    test_repr(_MeasurementQid('0:1:a', qubitron.LineQid(9, 4)))


def test_confusion_map():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.H(q0),
        qubitron.measure(q0, key='a', confusion_map={(0,): np.array([[0.8, 0.2], [0.1, 0.9]])}),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    deferred = qubitron.defer_measurements(circuit)

    # We use DM simulator because the deferred circuit has channels
    sim = qubitron.DensityMatrixSimulator()

    # 10K samples would take a long time if we had not deferred the measurements, as we'd have to
    # run 10K simulations. Here with DM simulator it's 100ms.
    result = sim.sample(deferred, repetitions=10_000)

    # This should be 5_000 due to the H, then 1_000 more due to 0's flipping to 1's with p=0.2, and
    # then 500 less due to 1's flipping to 0's with p=0.1, so 5_500.
    assert 5_100 <= np.sum(result['a']) <= 5_900
    assert np.all(result['a'] == result['b'])


def test_confusion_map_density_matrix():
    q0, q1 = qubitron.LineQubit.range(2)
    p_q0 = 0.3  # probability to measure 1 for q0
    confusion = np.array([[0.8, 0.2], [0.1, 0.9]])
    circuit = qubitron.Circuit(
        # Rotate q0 such that the probability to measure 1 is p_q0
        qubitron.X(q0) ** (np.arcsin(np.sqrt(p_q0)) * 2 / np.pi),
        qubitron.measure(q0, key='a', confusion_map={(0,): confusion}),
        qubitron.X(q1).with_classical_controls('a'),
    )
    deferred = qubitron.defer_measurements(circuit)
    q_order = (q0, q1, _MeasurementQid('a', q0))
    rho = qubitron.final_density_matrix(deferred, qubit_order=q_order).reshape((2,) * 6)

    # q0 density matrix should be a diagonal with the probabilities [1-p, p].
    q0_probs = [1 - p_q0, p_q0]
    assert np.allclose(qubitron.partial_trace(rho, [0]), np.diag(q0_probs))

    # q1 and the ancilla should both be the q1 probs matmul the confusion matrix.
    expected = np.diag(q0_probs @ confusion)
    assert np.allclose(qubitron.partial_trace(rho, [1]), expected)
    assert np.allclose(qubitron.partial_trace(rho, [2]), expected)


def test_confusion_map_invert_mask_ordering():
    q0 = qubitron.LineQubit(0)
    # Confusion map sets the measurement to zero, and the invert mask changes it to one.
    # If these are run out of order then the result would be zero.
    circuit = qubitron.Circuit(
        qubitron.measure(
            q0, key='a', confusion_map={(0,): np.array([[1, 0], [1, 0]])}, invert_mask=(1,)
        ),
        qubitron.I(q0),
    )
    assert_equivalent_to_deferred(circuit)


def test_confusion_map_qudits():
    q0 = qubitron.LineQid(0, dimension=3)
    # First op takes q0 to superposed state, then confusion map measures 2 regardless.
    circuit = qubitron.Circuit(
        qubitron.XPowGate(dimension=3).on(q0) ** 1.3,
        qubitron.measure(
            q0, key='a', confusion_map={(0,): np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]])}
        ),
        qubitron.IdentityGate(qid_shape=(3,)).on(q0),
    )
    assert_equivalent_to_deferred(circuit)


def test_multi_qubit_confusion_map():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(
            q0,
            q1,
            key='a',
            confusion_map={
                (0, 1): np.array(
                    [
                        [0.7, 0.1, 0.1, 0.1],
                        [0.1, 0.6, 0.1, 0.2],
                        [0.2, 0.2, 0.5, 0.1],
                        [0.0, 0.0, 1.0, 0.0],
                    ]
                )
            },
        ),
        qubitron.X(q2).with_classical_controls('a'),
        qubitron.measure(q2, key='b'),
    )
    deferred = qubitron.defer_measurements(circuit)
    sim = qubitron.DensityMatrixSimulator()
    result = sim.sample(deferred, repetitions=10_000)

    # The initial state is zero, so the first measurement will confuse by the first line in the
    # map, giving 7000 0's, 1000 1's, 1000 2's, and 1000 3's, for a sum of 6000 on average.
    assert 5_600 <= np.sum(result['a']) <= 6_400

    # The measurement will be non-zero 3000 times on average.
    assert 2_600 <= np.sum(result['b']) <= 3_400

    # Try a deterministic one: initial state is 3, which the confusion map sends to 2 with p=1.
    deferred.insert(0, qubitron.X.on_each(q0, q1))
    result = sim.sample(deferred, repetitions=100)
    assert np.sum(result['a']) == 200
    assert np.sum(result['b']) == 100


def test_confusion_map_errors():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a', confusion_map={(0,): np.array([1])}),
        qubitron.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='map must be 2D'):
        _ = qubitron.defer_measurements(circuit)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a', confusion_map={(0,): np.array([[0.7, 0.3]])}),
        qubitron.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='map must be square'):
        _ = qubitron.defer_measurements(circuit)
    circuit = qubitron.Circuit(
        qubitron.measure(
            q0,
            key='a',
            confusion_map={(0,): np.array([[0.7, 0.1, 0.2], [0.1, 0.6, 0.3], [0.2, 0.2, 0.6]])},
        ),
        qubitron.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='size does not match'):
        _ = qubitron.defer_measurements(circuit)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a', confusion_map={(0,): np.array([[-1, 2], [0, 1]])}),
        qubitron.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='negative probabilities'):
        _ = qubitron.defer_measurements(circuit)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a', confusion_map={(0,): np.array([[0.3, 0.3], [0.3, 0.3]])}),
        qubitron.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='invalid probabilities'):
        _ = qubitron.defer_measurements(circuit)


def test_dephase():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.CX(q1, q0),
                qubitron.measure(q0, key='a'),
                qubitron.CX(q0, q1),
                qubitron.measure(q1, key='b'),
            )
        )
    )
    dephased = qubitron.dephase_measurements(circuit)
    qubitron.testing.assert_same_circuits(
        dephased,
        qubitron.Circuit(
            qubitron.CircuitOperation(
                qubitron.FrozenCircuit(
                    qubitron.CX(q1, q0),
                    qubitron.KrausChannel.from_channel(qubitron.phase_damp(1), key='a')(q0),
                    qubitron.CX(q0, q1),
                    qubitron.KrausChannel.from_channel(qubitron.phase_damp(1), key='b')(q1),
                )
            )
        ),
    )


def test_dephase_classical_conditions():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    with pytest.raises(ValueError, match='defer_measurements first to remove classical controls'):
        _ = qubitron.dephase_measurements(circuit)


def test_dephase_nocompile_context():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.CX(q1, q0),
                qubitron.measure(q0, key='a').with_tags('nocompile'),
                qubitron.CX(q0, q1),
                qubitron.measure(q1, key='b'),
            )
        )
    )
    dephased = qubitron.dephase_measurements(
        circuit, context=qubitron.TransformerContext(deep=True, tags_to_ignore=('nocompile',))
    )
    qubitron.testing.assert_same_circuits(
        dephased,
        qubitron.Circuit(
            qubitron.CircuitOperation(
                qubitron.FrozenCircuit(
                    qubitron.CX(q1, q0),
                    qubitron.measure(q0, key='a').with_tags('nocompile'),
                    qubitron.CX(q0, q1),
                    qubitron.KrausChannel.from_channel(qubitron.phase_damp(1), key='b')(q1),
                )
            )
        ),
    )


def test_drop_terminal():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.CX(q0, q1), qubitron.measure(q0, q1, key='a~b', invert_mask=[0, 1]))
        )
    )
    dropped = qubitron.drop_terminal_measurements(circuit)
    qubitron.testing.assert_same_circuits(
        dropped,
        qubitron.Circuit(
            qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.CX(q0, q1), qubitron.I(q0), qubitron.X(q1)))
        ),
    )


def test_drop_terminal_qudit():
    q0, q1 = qubitron.LineQid.range(2, dimension=3)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.measure(q0, q1, key='m', invert_mask=[0, 1])))
    )
    dropped = qubitron.drop_terminal_measurements(circuit)
    expected_inversion_matrix = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    qubitron.testing.assert_same_circuits(
        dropped,
        qubitron.Circuit(
            qubitron.CircuitOperation(
                qubitron.FrozenCircuit(
                    qubitron.IdentityGate(qid_shape=(3,)).on(q0),
                    qubitron.MatrixGate(expected_inversion_matrix, qid_shape=(3,)).on(q1),
                )
            )
        ),
    )
    # Verify behavior equivalent to simulator (invert_mask swaps 0,1 but leaves 2 alone)
    dropped.append(qubitron.measure(q0, q1, key='m'))
    sim = qubitron.Simulator()
    c0 = sim.simulate(circuit, initial_state=[0, 0])
    d0 = sim.simulate(dropped, initial_state=[0, 0])
    assert np.all(c0.measurements['m'] == [0, 1])
    assert np.all(d0.measurements['m'] == [0, 1])
    c1 = sim.simulate(circuit, initial_state=[1, 1])
    d1 = sim.simulate(dropped, initial_state=[1, 1])
    assert np.all(c1.measurements['m'] == [1, 0])
    assert np.all(d1.measurements['m'] == [1, 0])
    c2 = sim.simulate(circuit, initial_state=[2, 2])
    d2 = sim.simulate(dropped, initial_state=[2, 2])
    assert np.all(c2.measurements['m'] == [2, 2])
    assert np.all(d2.measurements['m'] == [2, 2])


def test_drop_terminal_nonterminal_error():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.measure(q0, q1, key='a~b', invert_mask=[0, 1]), qubitron.CX(q0, q1))
        )
    )
    with pytest.raises(ValueError, match='Circuit contains a non-terminal measurement'):
        _ = qubitron.drop_terminal_measurements(circuit)

    with pytest.raises(ValueError, match='Context has `deep=False`'):
        _ = qubitron.drop_terminal_measurements(circuit, context=qubitron.TransformerContext(deep=False))

    with pytest.raises(ValueError, match='Context has `deep=False`'):
        _ = qubitron.drop_terminal_measurements(circuit, context=None)


def test_confusion_channel_consistency():
    two_d_chan = _ConfusionChannel(np.array([[0.5, 0.5], [0.4, 0.6]]), shape=(2,))
    qubitron.testing.assert_has_consistent_apply_channel(two_d_chan)
    three_d_chan = _ConfusionChannel(
        np.array([[0.5, 0.3, 0.2], [0.4, 0.5, 0.1], [0, 0, 1]]), shape=(3,)
    )
    qubitron.testing.assert_has_consistent_apply_channel(three_d_chan)
    two_q_chan = _ConfusionChannel(
        np.array([[0.5, 0.3, 0.1, 0.1], [0.4, 0.5, 0.1, 0], [0, 0, 1, 0], [0, 0, 0.5, 0.5]]),
        shape=(2, 2),
    )
    qubitron.testing.assert_has_consistent_apply_channel(two_q_chan)
