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

from typing import cast

import numpy as np
import pytest

import qubitron


@pytest.mark.parametrize(
    'key',
    ['q0_1_0', qubitron.MeasurementKey(name='q0_1_0'), qubitron.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_eval_repr(key):
    # Basic safeguard against repr-inequality.
    op = qubitron.GateOperation(gate=qubitron.MeasurementGate(1, key), qubits=[qubitron.GridQubit(0, 1)])
    qubitron.testing.assert_equivalent_repr(op)


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_measure_init(num_qubits):
    assert qubitron.MeasurementGate(num_qubits, 'a').num_qubits() == num_qubits
    assert qubitron.MeasurementGate(num_qubits, key='a').key == 'a'
    assert qubitron.MeasurementGate(num_qubits, key='a').mkey == qubitron.MeasurementKey('a')
    assert qubitron.MeasurementGate(num_qubits, key=qubitron.MeasurementKey('a')).key == 'a'
    assert qubitron.MeasurementGate(num_qubits, key=qubitron.MeasurementKey('a')) == qubitron.MeasurementGate(
        num_qubits, key='a'
    )
    assert qubitron.MeasurementGate(num_qubits, 'a', invert_mask=(True,)).invert_mask == (True,)
    assert qubitron.qid_shape(qubitron.MeasurementGate(num_qubits, 'a')) == (2,) * num_qubits
    cmap = {(0,): np.array([[0, 1], [1, 0]])}
    assert qubitron.MeasurementGate(num_qubits, 'a', confusion_map=cmap).confusion_map == cmap


def test_measure_init_num_qubit_agnostic():
    assert qubitron.qid_shape(qubitron.MeasurementGate(3, 'a', qid_shape=(1, 2, 3))) == (1, 2, 3)
    assert qubitron.qid_shape(qubitron.MeasurementGate(key='a', qid_shape=(1, 2, 3))) == (1, 2, 3)
    with pytest.raises(ValueError, match='len.* >'):
        qubitron.MeasurementGate(5, 'a', invert_mask=(True,) * 6)
    with pytest.raises(ValueError, match='len.* !='):
        qubitron.MeasurementGate(5, 'a', qid_shape=(1, 2))
    with pytest.raises(ValueError, match='valid string'):
        qubitron.MeasurementGate(2, qid_shape=(1, 2), key=None)
    with pytest.raises(ValueError, match='Confusion matrices have index out of bounds'):
        qubitron.MeasurementGate(1, 'a', confusion_map={(1,): np.array([[0, 1], [1, 0]])})
    with pytest.raises(ValueError, match='Specify either'):
        qubitron.MeasurementGate()


def test_measurement_has_unitary_returns_false():
    gate = qubitron.MeasurementGate(1, 'a')
    assert not qubitron.has_unitary(gate)


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_has_stabilizer_effect(num_qubits):
    assert qubitron.has_stabilizer_effect(qubitron.MeasurementGate(num_qubits, 'a'))


def test_measurement_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(
        lambda: qubitron.MeasurementGate(1, 'a'),
        lambda: qubitron.MeasurementGate(1, 'a', invert_mask=()),
        lambda: qubitron.MeasurementGate(1, 'a', invert_mask=(False,)),
        lambda: qubitron.MeasurementGate(1, 'a', qid_shape=(2,)),
        lambda: qubitron.MeasurementGate(1, 'a', confusion_map={}),
    )
    eq.add_equality_group(qubitron.MeasurementGate(1, 'a', invert_mask=(True,)))
    eq.add_equality_group(
        qubitron.MeasurementGate(1, 'a', confusion_map={(0,): np.array([[0, 1], [1, 0]])})
    )
    eq.add_equality_group(qubitron.MeasurementGate(1, 'b'))
    eq.add_equality_group(qubitron.MeasurementGate(2, 'a'))
    eq.add_equality_group(
        qubitron.MeasurementGate(3, 'a'), qubitron.MeasurementGate(3, 'a', qid_shape=(2, 2, 2))
    )
    eq.add_equality_group(qubitron.MeasurementGate(3, 'a', qid_shape=(1, 2, 3)))


def test_measurement_full_invert_mask():
    assert qubitron.MeasurementGate(1, 'a').full_invert_mask() == (False,)
    assert qubitron.MeasurementGate(2, 'a', invert_mask=(False, True)).full_invert_mask() == (
        False,
        True,
    )
    assert qubitron.MeasurementGate(2, 'a', invert_mask=(True,)).full_invert_mask() == (True, False)


@pytest.mark.parametrize('use_protocol', [False, True])
@pytest.mark.parametrize(
    'gate',
    [
        qubitron.MeasurementGate(1, 'a'),
        qubitron.MeasurementGate(1, 'a', invert_mask=(True,)),
        qubitron.MeasurementGate(1, 'a', qid_shape=(3,)),
        qubitron.MeasurementGate(2, 'a', invert_mask=(True, False), qid_shape=(2, 3)),
    ],
)
def test_measurement_with_key(use_protocol, gate):
    if use_protocol:
        gate1 = qubitron.with_measurement_key_mapping(gate, {'a': 'b'})
    else:
        gate1 = gate.with_key('b')
    assert gate1.key == 'b'
    assert gate1.num_qubits() == gate.num_qubits()
    assert gate1.invert_mask == gate.invert_mask
    assert qubitron.qid_shape(gate1) == qubitron.qid_shape(gate)
    if use_protocol:
        gate2 = qubitron.with_measurement_key_mapping(gate, {'a': 'a'})
    else:
        gate2 = gate.with_key('a')
    assert gate2 == gate


@pytest.mark.parametrize(
    'num_qubits, mask, bits, flipped',
    [
        (1, (), [0], (True,)),
        (3, (False,), [1], (False, True)),
        (3, (False, False), [0, 2], (True, False, True)),
    ],
)
def test_measurement_with_bits_flipped(num_qubits, mask, bits, flipped):
    gate = qubitron.MeasurementGate(num_qubits, key='a', invert_mask=mask, qid_shape=(3,) * num_qubits)

    gate1 = gate.with_bits_flipped(*bits)
    assert gate1.key == gate.key
    assert gate1.num_qubits() == gate.num_qubits()
    assert gate1.invert_mask == flipped
    assert qubitron.qid_shape(gate1) == qubitron.qid_shape(gate)

    # Flipping bits again restores the mask (but may have extended it).
    gate2 = gate1.with_bits_flipped(*bits)
    assert gate2.full_invert_mask() == gate.full_invert_mask()


def test_qudit_measure_qasm():
    assert (
        qubitron.qasm(
            qubitron.measure(qubitron.LineQid(0, 3), key='a'),
            args=qubitron.QasmArgs(),
            default='not implemented',
        )
        == 'not implemented'
    )


def test_confused_measure_qasm():
    q0 = qubitron.LineQubit(0)
    assert (
        qubitron.qasm(
            qubitron.measure(q0, key='a', confusion_map={(0,): np.array([[0, 1], [1, 0]])}),
            args=qubitron.QasmArgs(),
            default='not implemented',
        )
        == 'not implemented'
    )


def test_measurement_gate_diagram():
    # Shows key.
    assert qubitron.circuit_diagram_info(
        qubitron.MeasurementGate(1, key='test')
    ) == qubitron.CircuitDiagramInfo(("M('test')",))

    # Uses known qubit count.
    assert qubitron.circuit_diagram_info(
        qubitron.MeasurementGate(3, 'a'),
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=None,
            known_qubit_count=3,
            use_unicode_characters=True,
            precision=None,
            label_map=None,
        ),
    ) == qubitron.CircuitDiagramInfo(("M('a')", 'M', 'M'))

    # Shows invert mask.
    assert qubitron.circuit_diagram_info(
        qubitron.MeasurementGate(2, 'a', invert_mask=(False, True))
    ) == qubitron.CircuitDiagramInfo(("M('a')", "!M"))

    # Omits key when it is the default.
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure(a, b)),
        """
a: ───M───
      │
b: ───M───
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure(a, b, invert_mask=(True,))),
        """
a: ───!M───
      │
b: ───M────
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure(a, b, confusion_map={(1,): np.array([[0, 1], [1, 0]])})),
        """
a: ───M────
      │
b: ───?M───
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(
            qubitron.measure(
                a, b, invert_mask=(False, True), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
            )
        ),
        """
a: ───M─────
      │
b: ───!?M───
""",
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.measure(a, b, key='test')),
        """
a: ───M('test')───
      │
b: ───M───────────
""",
    )


def test_measurement_channel():
    np.testing.assert_allclose(
        qubitron.kraus(qubitron.MeasurementGate(1, 'a')),
        (np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])),
    )
    qubitron.testing.assert_consistent_channel(qubitron.MeasurementGate(1, 'a'))
    assert not qubitron.has_mixture(qubitron.MeasurementGate(1, 'a'))
    # yapf: disable
    np.testing.assert_allclose(
            qubitron.kraus(qubitron.MeasurementGate(2, 'a')),
            (np.array([[1, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])))
    np.testing.assert_allclose(
            qubitron.kraus(qubitron.MeasurementGate(2, 'a', qid_shape=(2, 3))),
            (np.diag([1, 0, 0, 0, 0, 0]),
             np.diag([0, 1, 0, 0, 0, 0]),
             np.diag([0, 0, 1, 0, 0, 0]),
             np.diag([0, 0, 0, 1, 0, 0]),
             np.diag([0, 0, 0, 0, 1, 0]),
             np.diag([0, 0, 0, 0, 0, 1])))
    # yapf: enable


def test_measurement_qubit_count_vs_mask_length():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')

    _ = qubitron.MeasurementGate(num_qubits=1, key='a', invert_mask=(True,)).on(a)
    _ = qubitron.MeasurementGate(num_qubits=2, key='a', invert_mask=(True, False)).on(a, b)
    _ = qubitron.MeasurementGate(num_qubits=3, key='a', invert_mask=(True, False, True)).on(a, b, c)
    with pytest.raises(ValueError):
        _ = qubitron.MeasurementGate(num_qubits=1, key='a', invert_mask=(True, False)).on(a)
    with pytest.raises(ValueError):
        _ = qubitron.MeasurementGate(num_qubits=3, key='a', invert_mask=(True, False, True)).on(a, b)


def test_consistent_protocols():
    for n in range(1, 5):
        gate = qubitron.MeasurementGate(num_qubits=n, key='a')
        qubitron.testing.assert_implements_consistent_protocols(gate)

        gate = qubitron.MeasurementGate(num_qubits=n, key='a', qid_shape=(3,) * n)
        qubitron.testing.assert_implements_consistent_protocols(gate)


def test_op_repr():
    a, b = qubitron.LineQubit.range(2)
    assert repr(qubitron.measure(a)) == 'qubitron.measure(qubitron.LineQubit(0))'
    assert repr(qubitron.measure(a, b)) == ('qubitron.measure(qubitron.LineQubit(0), qubitron.LineQubit(1))')
    assert repr(qubitron.measure(a, b, key='out', invert_mask=(False, True))) == (
        "qubitron.measure(qubitron.LineQubit(0), qubitron.LineQubit(1), "
        "key=qubitron.MeasurementKey(name='out'), "
        "invert_mask=(False, True))"
    )
    assert repr(
        qubitron.measure(
            a,
            b,
            key='out',
            invert_mask=(False, True),
            confusion_map={(0,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))},
        )
    ) == (
        "qubitron.measure(qubitron.LineQubit(0), qubitron.LineQubit(1), "
        "key=qubitron.MeasurementKey(name='out'), "
        "invert_mask=(False, True), "
        "confusion_map={(0,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))})"
    )


def test_repr():
    gate = qubitron.MeasurementGate(
        3,
        'a',
        (True, False),
        (1, 2, 3),
        {(2,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))},
    )
    assert repr(gate) == (
        "qubitron.MeasurementGate(3, qubitron.MeasurementKey(name='a'), (True, False), "
        "qid_shape=(1, 2, 3), "
        "confusion_map={(2,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))})"
    )


def test_act_on_state_vector():
    a, b = [qubitron.LineQubit(3), qubitron.LineQubit(1)]
    m = qubitron.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(shape=(2, 2, 2, 2, 2), dtype=np.complex64),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(0, 1, 0, 0, 0), shape=(2, 2, 2, 2, 2), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(0, 1, 0, 1, 0), shape=(2, 2, 2, 2, 2), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    datastore = cast(qubitron.ClassicalDataDictionaryStore, args.classical_data)
    out = qubitron.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_clifford_tableau():
    a, b = [qubitron.LineQubit(3), qubitron.LineQubit(1)]
    m = qubitron.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )
    # The below assertion does not fail since it ignores non-unitary operations
    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(m)

    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=5, initial_state=0),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=5, initial_state=8),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=5, initial_state=10),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(m, args)
    datastore = cast(qubitron.ClassicalDataDictionaryStore, args.classical_data)
    out = qubitron.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_stabilizer_ch_form():
    a, b = [qubitron.LineQubit(3), qubitron.LineQubit(1)]
    m = qubitron.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )
    # The below assertion does not fail since it ignores non-unitary operations
    qubitron.testing.assert_all_implemented_act_on_effects_match_unitary(m)

    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(5), prng=np.random.RandomState(), initial_state=0
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(5), prng=np.random.RandomState(), initial_state=8
    )

    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = qubitron.StabilizerChFormSimulationState(
        qubits=qubitron.LineQubit.range(5), prng=np.random.RandomState(), initial_state=10
    )
    qubitron.act_on(m, args)
    datastore = cast(qubitron.ClassicalDataDictionaryStore, args.classical_data)
    out = qubitron.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_qutrit():
    a, b = [qubitron.LineQid(3, dimension=3), qubitron.LineQid(1, dimension=3)]
    m = qubitron.measure(
        a,
        b,
        key='out',
        invert_mask=(True,),
        confusion_map={(1,): np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])},
    )

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=qubitron.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(0, 2, 0, 2, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [2, 0]}

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=qubitron.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(0, 1, 0, 2, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [2, 2]}

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=qubitron.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(0, 2, 0, 1, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    qubitron.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
