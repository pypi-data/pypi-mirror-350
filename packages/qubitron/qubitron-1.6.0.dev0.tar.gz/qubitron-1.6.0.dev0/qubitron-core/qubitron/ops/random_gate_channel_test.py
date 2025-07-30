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

import numpy as np
import pytest
import sympy

import qubitron


def test_init() -> None:
    p = qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=0.5)
    assert p.sub_gate is qubitron.X
    assert p.probability == 0.5

    with pytest.raises(ValueError, match='probability'):
        _ = qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=2)
    with pytest.raises(ValueError, match='probability'):
        _ = qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=-1)


def test_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    q = qubitron.LineQubit(0)

    eq.add_equality_group(
        qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=0.5), qubitron.X.with_probability(0.5)
    )

    # Each field matters for equality.
    eq.add_equality_group(qubitron.Y.with_probability(0.5))
    eq.add_equality_group(qubitron.X.with_probability(0.25))

    # `with_probability(1)` doesn't wrap
    eq.add_equality_group(qubitron.X, qubitron.X.with_probability(1))
    eq.add_equality_group(
        qubitron.X.with_probability(1).on(q), qubitron.X.on(q).with_probability(1), qubitron.X(q)
    )

    # `with_probability` with `on`.
    eq.add_equality_group(qubitron.X.with_probability(0.5).on(q), qubitron.X.on(q).with_probability(0.5))

    # Flattening.
    eq.add_equality_group(
        qubitron.RandomGateChannel(sub_gate=qubitron.Z, probability=0.25),
        qubitron.RandomGateChannel(
            sub_gate=qubitron.RandomGateChannel(sub_gate=qubitron.Z, probability=0.5), probability=0.5
        ),
        qubitron.Z.with_probability(0.5).with_probability(0.5),
        qubitron.Z.with_probability(0.25),
    )

    # Supports approximate equality.
    assert qubitron.approx_eq(qubitron.X.with_probability(0.5), qubitron.X.with_probability(0.50001), atol=1e-2)
    assert not qubitron.approx_eq(
        qubitron.X.with_probability(0.5), qubitron.X.with_probability(0.50001), atol=1e-8
    )


def test_consistent_protocols() -> None:
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=1),
        ignore_decompose_to_default_gateset=True,
    )
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=0),
        ignore_decompose_to_default_gateset=True,
    )
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=sympy.Symbol('x') / 2),
        ignore_decompose_to_default_gateset=True,
    )
    qubitron.testing.assert_implements_consistent_protocols(
        qubitron.RandomGateChannel(sub_gate=qubitron.X, probability=0.5),
        ignore_decompose_to_default_gateset=True,
    )


def test_diagram() -> None:
    class NoDetailsGate(qubitron.Gate):
        def num_qubits(self) -> int:
            raise NotImplementedError()

    assert qubitron.circuit_diagram_info(NoDetailsGate().with_probability(0.5), None) is None

    a, b = qubitron.LineQubit.range(2)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.CNOT(a, b).with_probability(0.125)),
        """
0: ───@[prob=0.125]───
      │
1: ───X───────────────
        """,
    )

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.CNOT(a, b).with_probability(0.125)),
        """
0: ───@[prob=0.1]───
      │
1: ───X─────────────
        """,
        precision=1,
    )


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterized(resolve_fn) -> None:
    op = qubitron.X.with_probability(sympy.Symbol('x'))
    assert qubitron.is_parameterized(op)
    assert not qubitron.has_kraus(op)
    assert not qubitron.has_mixture(op)

    op2 = resolve_fn(op, {'x': 0.5})
    assert op2 == qubitron.X.with_probability(0.5)
    assert not qubitron.is_parameterized(op2)
    assert qubitron.has_kraus(op2)
    assert qubitron.has_mixture(op2)


def test_mixture() -> None:
    class NoDetailsGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

    assert not qubitron.has_mixture(NoDetailsGate().with_probability(0.5))
    assert qubitron.mixture(NoDetailsGate().with_probability(0.5), None) is None

    assert qubitron.mixture(qubitron.X.with_probability(sympy.Symbol('x')), None) is None

    m = qubitron.mixture(qubitron.X.with_probability(0.25))
    assert len(m) == 2
    assert m[0][0] == 0.25
    np.testing.assert_allclose(qubitron.unitary(qubitron.X), m[0][1])
    assert m[1][0] == 0.75
    np.testing.assert_allclose(qubitron.unitary(qubitron.I), m[1][1])

    m = qubitron.mixture(qubitron.bit_flip(1 / 4).with_probability(1 / 8))
    assert len(m) == 3
    assert {p for p, _ in m} == {7 / 8, 1 / 32, 3 / 32}


def test_channel() -> None:
    class NoDetailsGate(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

    assert not qubitron.has_kraus(NoDetailsGate().with_probability(0.5))
    assert qubitron.kraus(NoDetailsGate().with_probability(0.5), None) is None
    assert qubitron.kraus(qubitron.X.with_probability(sympy.Symbol('x')), None) is None
    qubitron.testing.assert_consistent_channel(qubitron.X.with_probability(0.25))
    qubitron.testing.assert_consistent_channel(qubitron.bit_flip(0.75).with_probability(0.25))
    qubitron.testing.assert_consistent_channel(qubitron.amplitude_damp(0.75).with_probability(0.25))

    qubitron.testing.assert_consistent_mixture(qubitron.X.with_probability(0.25))
    qubitron.testing.assert_consistent_mixture(qubitron.bit_flip(0.75).with_probability(0.25))
    assert not qubitron.has_mixture(qubitron.amplitude_damp(0.75).with_probability(0.25))

    m = qubitron.kraus(qubitron.X.with_probability(0.25))
    assert len(m) == 2
    np.testing.assert_allclose(m[0], qubitron.unitary(qubitron.X) * np.sqrt(0.25), atol=1e-8)
    np.testing.assert_allclose(m[1], qubitron.unitary(qubitron.I) * np.sqrt(0.75), atol=1e-8)

    m = qubitron.kraus(qubitron.bit_flip(0.75).with_probability(0.25))
    assert len(m) == 3
    np.testing.assert_allclose(
        m[0], qubitron.unitary(qubitron.I) * np.sqrt(0.25) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(
        m[1], qubitron.unitary(qubitron.X) * np.sqrt(0.25) * np.sqrt(0.75), atol=1e-8
    )
    np.testing.assert_allclose(m[2], qubitron.unitary(qubitron.I) * np.sqrt(0.75), atol=1e-8)

    m = qubitron.kraus(qubitron.amplitude_damp(0.75).with_probability(0.25))
    assert len(m) == 3
    np.testing.assert_allclose(
        m[0], np.array([[1, 0], [0, np.sqrt(1 - 0.75)]]) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(
        m[1], np.array([[0, np.sqrt(0.75)], [0, 0]]) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(m[2], qubitron.unitary(qubitron.I) * np.sqrt(0.75), atol=1e-8)


def test_trace_distance() -> None:
    t = qubitron.trace_distance_bound
    assert 0.999 <= t(qubitron.X.with_probability(sympy.Symbol('x')))
    assert t(qubitron.X.with_probability(0)) == 0
    assert 0.49 <= t(qubitron.X.with_probability(0.5)) <= 0.51
    assert 0.7 <= t(qubitron.S.with_probability(sympy.Symbol('x'))) <= 0.71
    assert 0.35 <= t(qubitron.S.with_probability(0.5)) <= 0.36


def test_str() -> None:
    assert str(qubitron.X.with_probability(0.5)) == 'X[prob=0.5]'


def test_stabilizer_supports_probability() -> None:
    q = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.X(q).with_probability(0.5), qubitron.measure(q, key='m'))
    m = np.sum(qubitron.StabilizerSampler().sample(c, repetitions=100)['m'])
    assert 5 < m < 95


def test_unsupported_stabilizer_safety() -> None:
    from qubitron.protocols.act_on_protocol_test import ExampleSimulationState

    with pytest.raises(TypeError, match="act_on"):
        for _ in range(100):
            qubitron.act_on(qubitron.X.with_probability(0.5), ExampleSimulationState(), qubits=())
    with pytest.raises(TypeError, match="act_on"):
        qubitron.act_on(qubitron.X.with_probability(sympy.Symbol('x')), ExampleSimulationState(), qubits=())

    q = qubitron.LineQubit(0)
    c = qubitron.Circuit((qubitron.X(q) ** 0.25).with_probability(0.5), qubitron.measure(q, key='m'))
    with pytest.raises(TypeError, match='Failed to act'):
        qubitron.StabilizerSampler().sample(c, repetitions=100)
