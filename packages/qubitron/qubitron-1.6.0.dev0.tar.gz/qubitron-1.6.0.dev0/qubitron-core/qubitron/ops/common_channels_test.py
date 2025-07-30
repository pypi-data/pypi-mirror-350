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

import re

import numpy as np
import pytest

import qubitron
from qubitron.protocols.act_on_protocol_test import ExampleSimulationState

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])

no_precision = qubitron.CircuitDiagramInfoArgs(
    known_qubits=None,
    known_qubit_count=None,
    use_unicode_characters=True,
    precision=None,
    label_map=None,
)

round_to_6_prec = qubitron.CircuitDiagramInfoArgs(
    known_qubits=None,
    known_qubit_count=None,
    use_unicode_characters=True,
    precision=6,
    label_map=None,
)

round_to_2_prec = qubitron.CircuitDiagramInfoArgs(
    known_qubits=None,
    known_qubit_count=None,
    use_unicode_characters=True,
    precision=2,
    label_map=None,
)


def assert_mixtures_equal(actual, expected):
    """Assert equal for tuple of mixed scalar and array types."""
    for a, e in zip(actual, expected):
        np.testing.assert_almost_equal(a[0], e[0])
        np.testing.assert_almost_equal(a[1], e[1])


def test_asymmetric_depolarizing_channel() -> None:
    d = qubitron.asymmetric_depolarize(0.1, 0.2, 0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (np.sqrt(0.4) * np.eye(2), np.sqrt(0.1) * X, np.sqrt(0.2) * Y, np.sqrt(0.3) * Z),
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)

    assert qubitron.AsymmetricDepolarizingChannel(p_x=0, p_y=0.1, p_z=0).num_qubits() == 1


def test_asymmetric_depolarizing_mixture() -> None:
    d = qubitron.asymmetric_depolarize(0.1, 0.2, 0.3)
    assert_mixtures_equal(qubitron.mixture(d), ((0.4, np.eye(2)), (0.1, X), (0.2, Y), (0.3, Z)))
    assert qubitron.has_mixture(d)


def test_asymmetric_depolarizing_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.AsymmetricDepolarizingChannel(0.1, 0.2, 0.3))


def test_asymmetric_depolarizing_channel_str() -> None:
    assert (
        str(qubitron.asymmetric_depolarize(0.1, 0.2, 0.3))
        == "asymmetric_depolarize(error_probabilities={'I': 0.3999999999999999, "
        + "'X': 0.1, 'Y': 0.2, 'Z': 0.3})"
    )


def test_asymmetric_depolarizing_channel_eq() -> None:
    a = qubitron.asymmetric_depolarize(0.0099999, 0.01)
    b = qubitron.asymmetric_depolarize(0.01, 0.0099999)
    c = qubitron.asymmetric_depolarize(0.0, 0.0, 0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.asymmetric_depolarize(0.0, 0.0, 0.1))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.0, 0.1, 0.0))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.1, 0.0, 0.0))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.1, 0.2, 0.3))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.3, 0.4, 0.3))
    et.add_equality_group(qubitron.asymmetric_depolarize(1.0, 0.0, 0.0))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.0, 1.0, 0.0))
    et.add_equality_group(qubitron.asymmetric_depolarize(0.0, 0.0, 1.0))


@pytest.mark.parametrize(
    'p_x,p_y,p_z', ((-0.1, 0.0, 0.0), (0.0, -0.1, 0.0), (0.0, 0.0, -0.1), (0.1, -0.1, 0.1))
)
def test_asymmetric_depolarizing_channel_negative_probability(p_x, p_y, p_z) -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.asymmetric_depolarize(p_x, p_y, p_z)


@pytest.mark.parametrize(
    'p_x,p_y,p_z', ((1.1, 0.0, 0.0), (0.0, 1.1, 0.0), (0.0, 0.0, 1.1), (0.1, 0.9, 0.1))
)
def test_asymmetric_depolarizing_channel_bigly_probability(p_x, p_y, p_z) -> None:
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.asymmetric_depolarize(p_x, p_y, p_z)


def test_asymmetric_depolarizing_channel_text_diagram() -> None:
    a = qubitron.asymmetric_depolarize(1 / 9, 2 / 9, 3 / 9)
    assert qubitron.circuit_diagram_info(a, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(0.1111111111111111,0.2222222222222222,' + '0.3333333333333333)',)
    )
    assert qubitron.circuit_diagram_info(a, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(0.111111,0.222222,0.333333)',)
    )
    assert qubitron.circuit_diagram_info(a, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(0.11,0.22,0.33)',)
    )


def test_depolarizing_channel() -> None:
    d = qubitron.depolarize(0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (np.sqrt(0.7) * np.eye(2), np.sqrt(0.1) * X, np.sqrt(0.1) * Y, np.sqrt(0.1) * Z),
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)


def test_depolarizing_channel_two_qubits() -> None:
    d = qubitron.depolarize(0.15, n_qubits=2)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (
            np.sqrt(0.85) * np.eye(4),
            np.sqrt(0.01) * np.kron(np.eye(2), X),
            np.sqrt(0.01) * np.kron(np.eye(2), Y),
            np.sqrt(0.01) * np.kron(np.eye(2), Z),
            np.sqrt(0.01) * np.kron(X, np.eye(2)),
            np.sqrt(0.01) * np.kron(X, X),
            np.sqrt(0.01) * np.kron(X, Y),
            np.sqrt(0.01) * np.kron(X, Z),
            np.sqrt(0.01) * np.kron(Y, np.eye(2)),
            np.sqrt(0.01) * np.kron(Y, X),
            np.sqrt(0.01) * np.kron(Y, Y),
            np.sqrt(0.01) * np.kron(Y, Z),
            np.sqrt(0.01) * np.kron(Z, np.eye(2)),
            np.sqrt(0.01) * np.kron(Z, X),
            np.sqrt(0.01) * np.kron(Z, Y),
            np.sqrt(0.01) * np.kron(Z, Z),
        ),
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)

    assert d.num_qubits() == 2
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(d(*qubitron.LineQubit.range(2))),
        """
0: ───D(0.15)───
      │
1: ───#2────────
        """,
    )


def test_depolarizing_mixture() -> None:
    d = qubitron.depolarize(0.3)
    assert_mixtures_equal(qubitron.mixture(d), ((0.7, np.eye(2)), (0.1, X), (0.1, Y), (0.1, Z)))
    assert qubitron.has_mixture(d)


def test_depolarizing_mixture_two_qubits() -> None:
    d = qubitron.depolarize(0.15, n_qubits=2)
    assert_mixtures_equal(
        qubitron.mixture(d),
        (
            (0.85, np.eye(4)),
            (0.01, np.kron(np.eye(2), X)),
            (0.01, np.kron(np.eye(2), Y)),
            (0.01, np.kron(np.eye(2), Z)),
            (0.01, np.kron(X, np.eye(2))),
            (0.01, np.kron(X, X)),
            (0.01, np.kron(X, Y)),
            (0.01, np.kron(X, Z)),
            (0.01, np.kron(Y, np.eye(2))),
            (0.01, np.kron(Y, X)),
            (0.01, np.kron(Y, Y)),
            (0.01, np.kron(Y, Z)),
            (0.01, np.kron(Z, np.eye(2))),
            (0.01, np.kron(Z, X)),
            (0.01, np.kron(Z, Y)),
            (0.01, np.kron(Z, Z)),
        ),
    )
    assert qubitron.has_mixture(d)


def test_depolarizing_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.DepolarizingChannel(0.3))


def test_depolarizing_channel_repr_two_qubits() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.DepolarizingChannel(0.3, n_qubits=2))


def test_depolarizing_channel_str() -> None:
    assert str(qubitron.depolarize(0.3)) == 'depolarize(p=0.3)'


def test_depolarizing_channel_str_two_qubits() -> None:
    assert str(qubitron.depolarize(0.3, n_qubits=2)) == 'depolarize(p=0.3,n_qubits=2)'


def test_deprecated_on_each_for_depolarizing_channel_one_qubit() -> None:
    q0 = qubitron.LineQubit.range(1)
    op = qubitron.DepolarizingChannel(p=0.1, n_qubits=1)

    op.on_each(q0)
    op.on_each([q0])
    with pytest.raises(ValueError, match="Gate was called with type different than Qid"):
        op.on_each('bogus object')


def test_deprecated_on_each_for_depolarizing_channel_two_qubits() -> None:
    q0, q1, q2, q3, q4, q5 = qubitron.LineQubit.range(6)
    op = qubitron.DepolarizingChannel(p=0.1, n_qubits=2)

    op.on_each([(q0, q1)])
    op.on_each([(q0, q1), (q2, q3)])
    op.on_each(zip([q0, q2, q4], [q1, q3, q5]))
    op.on_each((q0, q1))
    op.on_each([q0, q1])
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        op.on_each(q0, q1)
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        op.on_each([('bogus object 0', 'bogus object 1')])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        op.on_each(['01'])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        op.on_each([(False, None)])


def test_depolarizing_channel_apply_two_qubits() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    op = qubitron.DepolarizingChannel(p=0.1, n_qubits=2)
    op(q0, q1)


def test_asymmetric_depolarizing_channel_apply_two_qubits() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    op = qubitron.AsymmetricDepolarizingChannel(error_probabilities={'XX': 0.1})
    op(q0, q1)


def test_depolarizing_channel_eq() -> None:
    a = qubitron.depolarize(p=0.0099999)
    b = qubitron.depolarize(p=0.01)
    c = qubitron.depolarize(0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()

    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.depolarize(0.1))
    et.add_equality_group(qubitron.depolarize(0.9))
    et.add_equality_group(qubitron.depolarize(1.0))
    et.add_equality_group(qubitron.depolarize(1.0, n_qubits=2))


def test_depolarizing_channel_invalid_probability() -> None:
    with pytest.raises(ValueError, match=re.escape('p(I) was greater than 1.')):
        qubitron.depolarize(-0.1)
    with pytest.raises(ValueError, match=re.escape('p(I) was less than 0.')):
        qubitron.depolarize(1.1)


def test_depolarizing_channel_text_diagram() -> None:
    d = qubitron.depolarize(0.1234567)
    assert qubitron.circuit_diagram_info(d, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.123457)',)
    )
    assert qubitron.circuit_diagram_info(d, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.12)',)
    )
    assert qubitron.circuit_diagram_info(d, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.1234567)',)
    )


def test_depolarizing_channel_text_diagram_two_qubits() -> None:
    d = qubitron.depolarize(0.1234567, n_qubits=2)
    assert qubitron.circuit_diagram_info(d, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.123457)', '#2')
    )
    assert qubitron.circuit_diagram_info(d, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.12)', '#2')
    )
    assert qubitron.circuit_diagram_info(d, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('D(0.1234567)', '#2')
    )


def test_generalized_amplitude_damping_channel() -> None:
    d = qubitron.generalized_amplitude_damp(0.1, 0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (
            np.sqrt(0.1) * np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - 0.3)]]),
            np.sqrt(0.1) * np.array([[0.0, np.sqrt(0.3)], [0.0, 0.0]]),
            np.sqrt(0.9) * np.array([[np.sqrt(1.0 - 0.3), 0.0], [0.0, 1.0]]),
            np.sqrt(0.9) * np.array([[0.0, 0.0], [np.sqrt(0.3), 0.0]]),
        ),
    )
    qubitron.testing.assert_consistent_channel(d)
    assert not qubitron.has_mixture(d)


def test_generalized_amplitude_damping_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.GeneralizedAmplitudeDampingChannel(0.1, 0.3))


def test_generalized_amplitude_damping_str() -> None:
    assert (
        str(qubitron.generalized_amplitude_damp(0.1, 0.3))
        == 'generalized_amplitude_damp(p=0.1,gamma=0.3)'
    )


def test_generalized_amplitude_damping_channel_eq() -> None:
    a = qubitron.generalized_amplitude_damp(0.0099999, 0.01)
    b = qubitron.generalized_amplitude_damp(0.01, 0.0099999)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    c = qubitron.generalized_amplitude_damp(0.0, 0.0)
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.generalized_amplitude_damp(0.1, 0.0))
    et.add_equality_group(qubitron.generalized_amplitude_damp(0.0, 0.1))
    et.add_equality_group(qubitron.generalized_amplitude_damp(0.6, 0.4))
    et.add_equality_group(qubitron.generalized_amplitude_damp(0.8, 0.2))


@pytest.mark.parametrize('p, gamma', ((-0.1, 0.0), (0.0, -0.1), (0.1, -0.1), (-0.1, 0.1)))
def test_generalized_amplitude_damping_channel_negative_probability(p, gamma) -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.generalized_amplitude_damp(p, gamma)


@pytest.mark.parametrize('p,gamma', ((1.1, 0.0), (0.0, 1.1), (1.1, 1.1)))
def test_generalized_amplitude_damping_channel_bigly_probability(p, gamma) -> None:
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.generalized_amplitude_damp(p, gamma)


def test_generalized_amplitude_damping_channel_text_diagram() -> None:
    a = qubitron.generalized_amplitude_damp(0.1, 0.39558391)
    assert qubitron.circuit_diagram_info(a, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('GAD(0.1,0.395584)',)
    )
    assert qubitron.circuit_diagram_info(a, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('GAD(0.1,0.4)',)
    )
    assert qubitron.circuit_diagram_info(a, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('GAD(0.1,0.39558391)',)
    )


def test_amplitude_damping_channel() -> None:
    d = qubitron.amplitude_damp(0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (
            np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - 0.3)]]),
            np.array([[0.0, np.sqrt(0.3)], [0.0, 0.0]]),
        ),
    )
    qubitron.testing.assert_consistent_channel(d)
    assert not qubitron.has_mixture(d)


def test_amplitude_damping_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.AmplitudeDampingChannel(0.3))


def test_amplitude_damping_channel_str() -> None:
    assert str(qubitron.amplitude_damp(0.3)) == 'amplitude_damp(gamma=0.3)'


def test_amplitude_damping_channel_eq() -> None:
    a = qubitron.amplitude_damp(0.0099999)
    b = qubitron.amplitude_damp(0.01)
    c = qubitron.amplitude_damp(0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.amplitude_damp(0.1))
    et.add_equality_group(qubitron.amplitude_damp(0.4))
    et.add_equality_group(qubitron.amplitude_damp(0.6))
    et.add_equality_group(qubitron.amplitude_damp(0.8))


def test_amplitude_damping_channel_invalid_probability() -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.amplitude_damp(-0.1)
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.amplitude_damp(1.1)


def test_amplitude_damping_channel_text_diagram() -> None:
    ad = qubitron.amplitude_damp(0.38059322)
    assert qubitron.circuit_diagram_info(ad, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('AD(0.380593)',)
    )
    assert qubitron.circuit_diagram_info(ad, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('AD(0.38)',)
    )
    assert qubitron.circuit_diagram_info(ad, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('AD(0.38059322)',)
    )


def test_reset_channel() -> None:
    r = qubitron.reset(qubitron.LineQubit(0))
    np.testing.assert_almost_equal(
        qubitron.kraus(r), (np.array([[1.0, 0.0], [0.0, 0]]), np.array([[0.0, 1.0], [0.0, 0.0]]))
    )
    qubitron.testing.assert_consistent_channel(r)
    assert not qubitron.has_mixture(r)

    assert qubitron.num_qubits(r) == 1
    assert qubitron.qid_shape(r) == (2,)

    r = qubitron.reset(qubitron.LineQid(0, dimension=3))
    np.testing.assert_almost_equal(
        qubitron.kraus(r),
        (
            np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]]),
        ),
    )  # yapf: disable
    qubitron.testing.assert_consistent_channel(r)
    assert not qubitron.has_mixture(r)
    assert qubitron.qid_shape(r) == (3,)


def test_reset_channel_equality() -> None:
    assert qubitron.reset(qubitron.LineQubit(0)).gate == qubitron.ResetChannel()
    assert qubitron.reset(qubitron.LineQid(0, 3)).gate == qubitron.ResetChannel(3)


def test_reset_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.ResetChannel())
    qubitron.testing.assert_equivalent_repr(qubitron.ResetChannel(3))


def test_reset_channel_str() -> None:
    assert str(qubitron.ResetChannel()) == 'reset'
    assert str(qubitron.ResetChannel(3)) == 'reset'


def test_reset_channel_text_diagram() -> None:
    assert qubitron.circuit_diagram_info(qubitron.ResetChannel()) == qubitron.CircuitDiagramInfo(
        wire_symbols=('R',)
    )
    assert qubitron.circuit_diagram_info(qubitron.ResetChannel(3)) == qubitron.CircuitDiagramInfo(
        wire_symbols=('R',)
    )


def test_reset_act_on() -> None:
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.ResetChannel(), ExampleSimulationState(), qubits=())

    args = qubitron.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2), dtype=np.complex64),
        qubits=qubitron.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=qubitron.one_hot(
            index=(1, 1, 1, 1, 1), shape=(2, 2, 2, 2, 2), dtype=np.complex64
        ),
        dtype=np.complex64,
    )

    qubitron.act_on(qubitron.ResetChannel(), args, [qubitron.LineQubit(1)])
    assert args.log_of_measurement_results == {}
    np.testing.assert_allclose(
        args.target_tensor,
        qubitron.one_hot(index=(1, 0, 1, 1, 1), shape=(2, 2, 2, 2, 2), dtype=np.complex64),
    )

    qubitron.act_on(qubitron.ResetChannel(), args, [qubitron.LineQubit(1)])
    assert args.log_of_measurement_results == {}
    np.testing.assert_allclose(
        args.target_tensor,
        qubitron.one_hot(index=(1, 0, 1, 1, 1), shape=(2, 2, 2, 2, 2), dtype=np.complex64),
    )


def test_reset_each() -> None:
    qubits = qubitron.LineQubit.range(8)
    for n in range(len(qubits) + 1):
        ops = qubitron.reset_each(*qubits[:n])
        assert len(ops) == n
        for i, op in enumerate(ops):
            assert isinstance(op.gate, qubitron.ResetChannel)
            assert op.qubits == (qubits[i],)


def test_reset_consistency() -> None:
    two_d_chan = qubitron.ResetChannel()
    qubitron.testing.assert_has_consistent_apply_channel(two_d_chan)
    three_d_chan = qubitron.ResetChannel(dimension=3)
    qubitron.testing.assert_has_consistent_apply_channel(three_d_chan)


def test_phase_damping_channel() -> None:
    d = qubitron.phase_damp(0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d),
        (
            np.array([[1.0, 0.0], [0.0, np.sqrt(1 - 0.3)]]),
            np.array([[0.0, 0.0], [0.0, np.sqrt(0.3)]]),
        ),
    )
    qubitron.testing.assert_consistent_channel(d)
    assert not qubitron.has_mixture(d)


def test_phase_damping_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.PhaseDampingChannel(0.3))


def test_phase_damping_channel_str() -> None:
    assert str(qubitron.phase_damp(0.3)) == 'phase_damp(gamma=0.3)'


def test_phase_damping_channel_eq() -> None:
    a = qubitron.phase_damp(0.0099999)
    b = qubitron.phase_damp(0.01)
    c = qubitron.phase_damp(0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.phase_damp(0.1))
    et.add_equality_group(qubitron.phase_damp(0.4))
    et.add_equality_group(qubitron.phase_damp(0.6))
    et.add_equality_group(qubitron.phase_damp(0.8))


def test_phase_damping_channel_invalid_probability() -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.phase_damp(-0.1)
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.phase_damp(1.1)


def test_phase_damping_channel_text_diagram() -> None:
    pd = qubitron.phase_damp(0.1000009)
    assert qubitron.circuit_diagram_info(pd, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PD(0.100001)',)
    )
    assert qubitron.circuit_diagram_info(pd, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PD(0.1)',)
    )
    assert qubitron.circuit_diagram_info(pd, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PD(0.1000009)',)
    )


def test_phase_damp_consistency() -> None:
    full_damp = qubitron.PhaseDampingChannel(gamma=1)
    qubitron.testing.assert_has_consistent_apply_channel(full_damp)
    partial_damp = qubitron.PhaseDampingChannel(gamma=0.5)
    qubitron.testing.assert_has_consistent_apply_channel(partial_damp)
    no_damp = qubitron.PhaseDampingChannel(gamma=0)
    qubitron.testing.assert_has_consistent_apply_channel(no_damp)


def test_phase_flip_channel() -> None:
    d = qubitron.phase_flip(0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d), (np.sqrt(1.0 - 0.3) * np.eye(2), np.sqrt(0.3) * Z)
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)


def test_phase_flip_mixture() -> None:
    d = qubitron.phase_flip(0.3)
    assert_mixtures_equal(qubitron.mixture(d), ((0.7, np.eye(2)), (0.3, Z)))
    assert qubitron.has_mixture(d)


def test_phase_flip_overload() -> None:
    d = qubitron.phase_flip()
    d2 = qubitron.phase_flip(0.3)
    assert str(d) == 'Z'
    assert str(d2) == 'phase_flip(p=0.3)'


def test_phase_flip_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.PhaseFlipChannel(0.3))


def test_phase_flip_channel_str() -> None:
    assert str(qubitron.phase_flip(0.3)) == 'phase_flip(p=0.3)'


def test_phase_flip_channel_eq() -> None:
    a = qubitron.phase_flip(0.0099999)
    b = qubitron.phase_flip(0.01)
    c = qubitron.phase_flip(0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.phase_flip(0.1))
    et.add_equality_group(qubitron.phase_flip(0.4))
    et.add_equality_group(qubitron.phase_flip(0.6))
    et.add_equality_group(qubitron.phase_flip(0.8))


def test_phase_flip_channel_invalid_probability() -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.phase_flip(-0.1)
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.phase_flip(1.1)


def test_phase_flip_channel_text_diagram() -> None:
    pf = qubitron.phase_flip(0.987654)
    assert qubitron.circuit_diagram_info(pf, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PF(0.987654)',)
    )
    assert qubitron.circuit_diagram_info(pf, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PF(0.99)',)
    )
    assert qubitron.circuit_diagram_info(pf, no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('PF(0.987654)',)
    )


def test_bit_flip_channel() -> None:
    d = qubitron.bit_flip(0.3)
    np.testing.assert_almost_equal(
        qubitron.kraus(d), (np.sqrt(1.0 - 0.3) * np.eye(2), np.sqrt(0.3) * X)
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)


def test_bit_flip_mixture() -> None:
    d = qubitron.bit_flip(0.3)
    assert_mixtures_equal(qubitron.mixture(d), ((0.7, np.eye(2)), (0.3, X)))
    assert qubitron.has_mixture(d)


def test_bit_flip_overload() -> None:
    d = qubitron.bit_flip()
    d2 = qubitron.bit_flip(0.3)
    assert str(d) == 'X'
    assert str(d2) == 'bit_flip(p=0.3)'


def test_bit_flip_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.BitFlipChannel(0.3))


def test_bit_flip_channel_str() -> None:
    assert str(qubitron.bit_flip(0.3)) == 'bit_flip(p=0.3)'


def test_bit_flip_channel_eq() -> None:
    a = qubitron.bit_flip(0.0099999)
    b = qubitron.bit_flip(0.01)
    c = qubitron.bit_flip(0.0)

    assert qubitron.approx_eq(a, b, atol=1e-2)
    assert not qubitron.approx_eq(a, qubitron.X)

    et = qubitron.testing.EqualsTester()
    et.make_equality_group(lambda: c)
    et.add_equality_group(qubitron.bit_flip(0.1))
    et.add_equality_group(qubitron.bit_flip(0.4))
    et.add_equality_group(qubitron.bit_flip(0.6))
    et.add_equality_group(qubitron.bit_flip(0.8))


def test_bit_flip_channel_invalid_probability() -> None:
    with pytest.raises(ValueError, match='was less than 0'):
        qubitron.bit_flip(-0.1)
    with pytest.raises(ValueError, match='was greater than 1'):
        qubitron.bit_flip(1.1)


def test_bit_flip_channel_text_diagram() -> None:
    bf = qubitron.bit_flip(0.1234567)
    assert qubitron.circuit_diagram_info(bf, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('BF(0.123457)',)
    )
    assert qubitron.circuit_diagram_info(bf, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('BF(0.12)',)
    )
    assert qubitron.circuit_diagram_info(bf, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('BF(0.1234567)',)
    )


def test_stabilizer_supports_depolarize() -> None:
    with pytest.raises(TypeError, match="act_on"):
        for _ in range(100):
            qubitron.act_on(qubitron.depolarize(3 / 4), ExampleSimulationState(), qubits=())

    q = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.depolarize(3 / 4).on(q), qubitron.measure(q, key='m'))
    m = np.sum(qubitron.StabilizerSampler().sample(c, repetitions=100)['m'])
    assert 5 < m < 95


def test_default_asymmetric_depolarizing_channel() -> None:
    d = qubitron.asymmetric_depolarize()
    assert d.p_i == 1.0
    assert d.p_x == 0.0
    assert d.p_y == 0.0
    assert d.p_z == 0.0
    assert d.num_qubits() == 1


def test_bad_error_probabilities_gate() -> None:
    with pytest.raises(ValueError, match='AB is not made solely of I, X, Y, Z.'):
        qubitron.asymmetric_depolarize(error_probabilities={'AB': 1.0})
    with pytest.raises(ValueError, match='Y must have 2 Pauli gates.'):
        qubitron.asymmetric_depolarize(error_probabilities={'IX': 0.8, 'Y': 0.2})


def test_bad_probs() -> None:
    with pytest.raises(ValueError, match=re.escape('p(X) was greater than 1.')):
        qubitron.asymmetric_depolarize(error_probabilities={'X': 1.1, 'Y': -0.1})
    with pytest.raises(ValueError, match=re.escape('Probabilities do not add up to 1')):
        qubitron.asymmetric_depolarize(error_probabilities={'X': 0.7, 'Y': 0.6})


def test_missing_prob_mass() -> None:
    with pytest.raises(ValueError, match='Probabilities do not add up to 1'):
        qubitron.asymmetric_depolarize(error_probabilities={'X': 0.1, 'I': 0.2})
    d = qubitron.asymmetric_depolarize(error_probabilities={'X': 0.1})
    np.testing.assert_almost_equal(d.error_probabilities['I'], 0.9)


def test_multi_asymmetric_depolarizing_channel() -> None:
    d = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})
    np.testing.assert_almost_equal(
        qubitron.kraus(d), (np.sqrt(0.8) * np.eye(4), np.sqrt(0.2) * np.kron(X, X))
    )
    qubitron.testing.assert_consistent_channel(d)
    qubitron.testing.assert_consistent_mixture(d)
    np.testing.assert_equal(d._num_qubits_(), 2)

    with pytest.raises(ValueError, match="num_qubits should be 1"):
        assert d.p_i == 1.0
    with pytest.raises(ValueError, match="num_qubits should be 1"):
        assert d.p_x == 0.0
    with pytest.raises(ValueError, match="num_qubits should be 1"):
        assert d.p_y == 0.0
    with pytest.raises(ValueError, match="num_qubits should be 1"):
        assert d.p_z == 0.0


def test_multi_asymmetric_depolarizing_mixture() -> None:
    d = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})
    assert_mixtures_equal(qubitron.mixture(d), ((0.8, np.eye(4)), (0.2, np.kron(X, X))))
    assert qubitron.has_mixture(d)
    np.testing.assert_equal(d._num_qubits_(), 2)


def test_multi_asymmetric_depolarizing_channel_repr() -> None:
    qubitron.testing.assert_equivalent_repr(
        qubitron.AsymmetricDepolarizingChannel(error_probabilities={'II': 0.8, 'XX': 0.2})
    )


def test_multi_asymmetric_depolarizing_eq() -> None:
    a = qubitron.asymmetric_depolarize(error_probabilities={'I': 0.8, 'X': 0.2})
    b = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})

    assert not qubitron.approx_eq(a, b)

    a = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})
    b = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'XX': 1 / 3})

    assert not qubitron.approx_eq(a, b)

    a = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'ZZ': 1 / 3})
    b = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'XX': 1 / 3})

    assert not qubitron.approx_eq(a, b)

    a = qubitron.asymmetric_depolarize(0.1, 0.2)
    b = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'XX': 1 / 3})

    assert not qubitron.approx_eq(a, b)

    a = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.667, 'XX': 0.333})
    b = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'XX': 1 / 3})

    assert qubitron.approx_eq(a, b, atol=1e-3)

    a = qubitron.asymmetric_depolarize(error_probabilities={'II': 0.667, 'XX': 0.333})
    b = qubitron.asymmetric_depolarize(error_probabilities={'XX': 1 / 3, 'II': 2 / 3})

    assert qubitron.approx_eq(a, b, atol=1e-3)

    assert not qubitron.approx_eq(a, qubitron.X)


def test_multi_asymmetric_depolarizing_channel_str() -> None:
    assert str(qubitron.asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})) == (
        "asymmetric_depolarize(error_probabilities={'II': 0.8, 'XX': 0.2})"
    )


def test_multi_asymmetric_depolarizing_channel_text_diagram() -> None:
    a = qubitron.asymmetric_depolarize(error_probabilities={'II': 2 / 3, 'XX': 1 / 3})
    assert qubitron.circuit_diagram_info(a, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(II:0.6666666666666666, XX:0.3333333333333333)', '(1)')
    )
    assert qubitron.circuit_diagram_info(a, args=round_to_6_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(II:0.666667, XX:0.333333)', '(1)')
    )
    assert qubitron.circuit_diagram_info(a, args=round_to_2_prec) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(II:0.67, XX:0.33)', '(1)')
    )
    assert qubitron.circuit_diagram_info(a, args=no_precision) == qubitron.CircuitDiagramInfo(
        wire_symbols=('A(II:0.6666666666666666, XX:0.3333333333333333)', '(1)')
    )


def test_reset_stabilizer() -> None:
    assert qubitron.has_stabilizer_effect(qubitron.reset(qubitron.LineQubit(0)))
