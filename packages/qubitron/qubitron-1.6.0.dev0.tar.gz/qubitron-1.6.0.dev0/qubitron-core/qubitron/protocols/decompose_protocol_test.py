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

import itertools
from unittest import mock

import pytest

import qubitron


class NoMethod:
    pass


class DecomposeNotImplemented:
    def _decompose_(self, qubits=None):
        return NotImplemented


class DecomposeNone:
    def _decompose_(self, qubits=None):
        return None


class DecomposeGiven:
    def __init__(self, val):
        self.val = val

    def _decompose_(self):
        return self.val


class DecomposeWithQubitsGiven:
    def __init__(self, func):
        self.func = func

    def _decompose_(self, qubits):
        return self.func(*qubits)


class DecomposeGenerated:
    def _decompose_(self):
        yield qubitron.X(qubitron.LineQubit(0))
        yield qubitron.Y(qubitron.LineQubit(1))


class DecomposeQuditGate:
    def _decompose_(self, qids):
        yield qubitron.identity_each(*qids)


def test_decompose_once() -> None:
    # No default value results in descriptive error.
    with pytest.raises(TypeError, match='no _decompose_with_context_ or _decompose_ method'):
        _ = qubitron.decompose_once(NoMethod())
    with pytest.raises(TypeError, match='returned NotImplemented or None'):
        _ = qubitron.decompose_once(DecomposeNotImplemented())
    with pytest.raises(TypeError, match='returned NotImplemented or None'):
        _ = qubitron.decompose_once(DecomposeNone())

    # Default value works.
    assert qubitron.decompose_once(NoMethod(), 5) == 5
    assert qubitron.decompose_once(DecomposeNotImplemented(), None) is None
    assert qubitron.decompose_once(NoMethod(), NotImplemented) is NotImplemented
    assert qubitron.decompose_once(DecomposeNone(), 0) == 0

    # Flattens into a list.
    op = qubitron.X(qubitron.NamedQubit('q'))
    assert qubitron.decompose_once(DecomposeGiven(op)) == [op]
    assert qubitron.decompose_once(DecomposeGiven([[[op]], []])) == [op]
    assert qubitron.decompose_once(DecomposeGiven(op for _ in range(2))) == [op, op]
    assert type(qubitron.decompose_once(DecomposeGiven(op for _ in range(2)))) == list
    assert qubitron.decompose_once(DecomposeGenerated()) == [
        qubitron.X(qubitron.LineQubit(0)),
        qubitron.Y(qubitron.LineQubit(1)),
    ]


def test_decompose_once_with_qubits() -> None:
    qs = qubitron.LineQubit.range(3)

    # No default value results in descriptive error.
    with pytest.raises(TypeError, match='no _decompose_with_context_ or _decompose_ method'):
        _ = qubitron.decompose_once_with_qubits(NoMethod(), qs)
    with pytest.raises(TypeError, match='returned NotImplemented or None'):
        _ = qubitron.decompose_once_with_qubits(DecomposeNotImplemented(), qs)
    with pytest.raises(TypeError, match='returned NotImplemented or None'):
        _ = qubitron.decompose_once_with_qubits(DecomposeNone(), qs)

    # Default value works.
    assert qubitron.decompose_once_with_qubits(NoMethod(), qs, 5) == 5
    assert qubitron.decompose_once_with_qubits(DecomposeNotImplemented(), qs, None) is None
    assert qubitron.decompose_once_with_qubits(NoMethod(), qs, NotImplemented) is NotImplemented

    # Flattens into a list.
    assert qubitron.decompose_once_with_qubits(DecomposeWithQubitsGiven(qubitron.X.on_each), qs) == [
        qubitron.X(qubitron.LineQubit(0)),
        qubitron.X(qubitron.LineQubit(1)),
        qubitron.X(qubitron.LineQubit(2)),
    ]
    assert qubitron.decompose_once_with_qubits(
        DecomposeWithQubitsGiven(lambda *qubits: qubitron.Y(qubits[0])), qs
    ) == [qubitron.Y(qubitron.LineQubit(0))]
    assert qubitron.decompose_once_with_qubits(
        DecomposeWithQubitsGiven(lambda *qubits: (qubitron.Y(q) for q in qubits)), qs
    ) == [qubitron.Y(qubitron.LineQubit(0)), qubitron.Y(qubitron.LineQubit(1)), qubitron.Y(qubitron.LineQubit(2))]

    # Qudits, _decompose_ argument name is not 'qubits'.
    assert qubitron.decompose_once_with_qubits(
        DecomposeQuditGate(), qubitron.LineQid.for_qid_shape((1, 2, 3))
    ) == [qubitron.identity_each(*qubitron.LineQid.for_qid_shape((1, 2, 3)))]

    # Works when qubits are generated.
    def use_qubits_twice(*qubits):
        a = list(qubits)
        b = list(qubits)
        yield qubitron.X.on_each(*a)
        yield qubitron.Y.on_each(*b)

    assert qubitron.decompose_once_with_qubits(
        DecomposeWithQubitsGiven(use_qubits_twice), (q for q in qs)
    ) == list(qubitron.X.on_each(*qs)) + list(qubitron.Y.on_each(*qs))


def test_decompose_general() -> None:
    a, b, c = qubitron.LineQubit.range(3)
    no_method = NoMethod()
    assert qubitron.decompose(no_method) == [no_method]

    # Flattens iterables.
    assert qubitron.decompose([qubitron.SWAP(a, b), qubitron.SWAP(a, b)]) == 2 * qubitron.decompose(qubitron.SWAP(a, b))

    # Decomposed circuit should be equivalent. The ordering should be correct.
    ops = qubitron.TOFFOLI(a, b, c), qubitron.H(a), qubitron.CZ(a, c)
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit(ops), qubitron.Circuit(qubitron.decompose(ops)), atol=1e-8
    )


def test_decompose_keep() -> None:
    a, b = qubitron.LineQubit.range(2)

    # Recursion can be stopped.
    assert qubitron.decompose(qubitron.SWAP(a, b), keep=lambda e: isinstance(e.gate, qubitron.CNotPowGate)) == [
        qubitron.CNOT(a, b),
        qubitron.CNOT(b, a),
        qubitron.CNOT(a, b),
    ]

    # Recursion continues down to CZ + single-qubit gates.
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.decompose(qubitron.SWAP(a, b))),
        """
0: ────────────@───Y^-0.5───@───Y^0.5────@───────────
               │            │            │
1: ───Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───
""",
    )

    # If you're happy with everything, no decomposition happens.
    assert qubitron.decompose(qubitron.SWAP(a, b), keep=lambda _: True) == [qubitron.SWAP(a, b)]
    # Unless it's not an operation.
    assert qubitron.decompose(DecomposeGiven(qubitron.SWAP(b, a)), keep=lambda _: True) == [qubitron.SWAP(b, a)]
    # E.g. lists still get flattened.
    assert qubitron.decompose([[[qubitron.SWAP(a, b)]]], keep=lambda _: True) == [qubitron.SWAP(a, b)]


def test_decompose_on_stuck_raise() -> None:
    a, b = qubitron.LineQubit.range(2)
    no_method = NoMethod()

    # If you're not happy with anything, you're going to get an error.
    with pytest.raises(ValueError, match="but can't be decomposed"):
        _ = qubitron.decompose(NoMethod(), keep=lambda _: False)
    # Unless there's no operations to be unhappy about.
    assert qubitron.decompose([], keep=lambda _: False) == []
    assert qubitron.decompose([], on_stuck_raise=None) == []
    # Or you say you're fine.
    assert qubitron.decompose(no_method, keep=lambda _: False, on_stuck_raise=None) == [no_method]
    assert qubitron.decompose(no_method, keep=lambda _: False, on_stuck_raise=lambda _: None) == [
        no_method
    ]
    # You can customize the error.
    with pytest.raises(TypeError, match='test'):
        _ = qubitron.decompose(no_method, keep=lambda _: False, on_stuck_raise=TypeError('test'))
    with pytest.raises(NotImplementedError, match='op qubitron.CZ'):
        _ = qubitron.decompose(
            qubitron.CZ(a, b),
            keep=lambda _: False,
            on_stuck_raise=lambda op: NotImplementedError(f'op {op!r}'),
        )

    # There's a nice warning if you specify `on_stuck_raise` but not `keep`.
    with pytest.raises(ValueError, match='on_stuck_raise'):
        assert qubitron.decompose([], on_stuck_raise=TypeError('x'))


def test_decompose_intercept() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    # Runs instead of normal decomposition.
    actual = qubitron.decompose(
        qubitron.SWAP(a, b),
        intercepting_decomposer=lambda op: (qubitron.X(a) if op == qubitron.SWAP(a, b) else NotImplemented),
    )
    assert actual == [qubitron.X(a)]

    # Falls back to normal decomposition when NotImplemented.
    actual = qubitron.decompose(
        qubitron.SWAP(a, b),
        keep=lambda op: isinstance(op.gate, qubitron.CNotPowGate),
        intercepting_decomposer=lambda _: NotImplemented,
    )
    assert actual == [qubitron.CNOT(a, b), qubitron.CNOT(b, a), qubitron.CNOT(a, b)]

    # Accepts a context, when provided.
    def _intercept_with_context(
        op: qubitron.Operation, context: qubitron.DecompositionContext | None = None
    ):
        assert context is not None
        if op.gate == qubitron.SWAP:
            q = context.qubit_manager.qalloc(1)
            a, b = op.qubits
            return [qubitron.X(a), qubitron.X(*q), qubitron.X(b)]
        return NotImplemented

    context = qubitron.DecompositionContext(qubitron.ops.SimpleQubitManager())
    actual = qubitron.decompose(
        qubitron.SWAP(a, b), intercepting_decomposer=_intercept_with_context, context=context
    )
    assert actual == [qubitron.X(a), qubitron.X(qubitron.ops.CleanQubit(0)), qubitron.X(b)]


def test_decompose_preserving_structure() -> None:
    a, b = qubitron.LineQubit.range(2)
    fc1 = qubitron.FrozenCircuit(qubitron.SWAP(a, b), qubitron.FSimGate(0.1, 0.2).on(a, b))
    cop1_1 = qubitron.CircuitOperation(fc1).with_tags('test_tag')
    cop1_2 = qubitron.CircuitOperation(fc1).with_qubit_mapping({a: b, b: a})
    fc2 = qubitron.FrozenCircuit(qubitron.X(a), cop1_1, cop1_2)
    cop2 = qubitron.CircuitOperation(fc2)

    circuit = qubitron.Circuit(cop2, qubitron.measure(a, b, key='m'))
    actual = qubitron.Circuit(qubitron.decompose(circuit, preserve_structure=True))

    # This should keep the CircuitOperations but decompose their SWAPs.
    fc1_decomp = qubitron.FrozenCircuit(qubitron.decompose(fc1))
    expected = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.X(a),
                qubitron.CircuitOperation(fc1_decomp).with_tags('test_tag'),
                qubitron.CircuitOperation(fc1_decomp).with_qubit_mapping({a: b, b: a}),
            )
        ),
        qubitron.measure(a, b, key='m'),
    )
    assert actual == expected


# Test both intercepting and fallback decomposers.
@pytest.mark.parametrize('decompose_mode', ['intercept', 'fallback'])
def test_decompose_preserving_structure_forwards_args(decompose_mode) -> None:
    a, b = qubitron.LineQubit.range(2)
    fc1 = qubitron.FrozenCircuit(qubitron.SWAP(a, b), qubitron.FSimGate(0.1, 0.2).on(a, b))
    cop1_1 = qubitron.CircuitOperation(fc1).with_tags('test_tag')
    cop1_2 = qubitron.CircuitOperation(fc1).with_qubit_mapping({a: b, b: a})
    fc2 = qubitron.FrozenCircuit(qubitron.X(a), cop1_1, cop1_2)
    cop2 = qubitron.CircuitOperation(fc2)

    circuit = qubitron.Circuit(cop2, qubitron.measure(a, b, key='m'))

    def keep_func(op: qubitron.Operation):
        # Only decompose SWAP and X.
        return not isinstance(op.gate, (qubitron.SwapPowGate, qubitron.XPowGate))

    def x_to_hzh(op: qubitron.Operation):
        if isinstance(op.gate, qubitron.XPowGate) and op.gate.exponent == 1:
            return [qubitron.H(*op.qubits), qubitron.Z(*op.qubits), qubitron.H(*op.qubits)]

    actual = qubitron.Circuit(
        qubitron.decompose(
            circuit,
            keep=keep_func,
            intercepting_decomposer=x_to_hzh if decompose_mode == 'intercept' else None,
            fallback_decomposer=x_to_hzh if decompose_mode == 'fallback' else None,
            preserve_structure=True,
        )
    )

    # This should keep the CircuitOperations but decompose their SWAPs.
    fc1_decomp = qubitron.FrozenCircuit(
        qubitron.decompose(fc1, keep=keep_func, fallback_decomposer=x_to_hzh)
    )
    expected = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.H(a),
                qubitron.Z(a),
                qubitron.H(a),
                qubitron.CircuitOperation(fc1_decomp).with_tags('test_tag'),
                qubitron.CircuitOperation(fc1_decomp).with_qubit_mapping({a: b, b: a}),
            )
        ),
        qubitron.measure(a, b, key='m'),
    )
    assert actual == expected


def test_decompose_tagged_operation() -> None:
    op = qubitron.TaggedOperation(
        qubitron.CircuitOperation(
            circuit=qubitron.FrozenCircuit(
                [qubitron.Moment(qubitron.SWAP(qubitron.LineQubit(0), qubitron.LineQubit(1)))]
            )
        ),
        'tag',
    )
    assert qubitron.decompose_once(op) == qubitron.decompose_once(op.untagged)


class RecursiveDecompose(qubitron.Gate):
    def __init__(
        self,
        recurse: bool = True,
        mock_qm=mock.Mock(spec=qubitron.QubitManager),
        with_context: bool = False,
    ):
        self.recurse = recurse
        self.mock_qm = mock_qm
        self.with_context = with_context

    def _num_qubits_(self) -> int:
        return 2

    def _decompose_impl(self, qubits, mock_qm: mock.Mock):
        mock_qm.qalloc(self.recurse)
        yield (
            RecursiveDecompose(
                recurse=False, mock_qm=self.mock_qm, with_context=self.with_context
            ).on(*qubits)
            if self.recurse
            else qubitron.Z.on_each(*qubits)
        )
        mock_qm.qfree(self.recurse)

    def _decompose_(self, qubits):
        if self.with_context:
            assert False  # pragma: no cover
        else:
            return self._decompose_impl(qubits, self.mock_qm)

    def _decompose_with_context_(self, qubits, context):
        if self.with_context:
            qm = self.mock_qm if context is None else context.qubit_manager
            return self._decompose_impl(qubits, qm)
        else:
            return NotImplemented

    def _has_unitary_(self):
        return True


@pytest.mark.parametrize('with_context', [True, False])
def test_decompose_recursive_dfs(with_context: bool) -> None:
    expected_calls = [
        mock.call.qalloc(True),
        mock.call.qalloc(False),
        mock.call.qfree(False),
        mock.call.qfree(True),
    ]
    mock_qm = mock.Mock(spec=qubitron.QubitManager)
    context_qm = mock.Mock(spec=qubitron.QubitManager)
    gate = RecursiveDecompose(mock_qm=mock_qm, with_context=with_context)
    q = qubitron.LineQubit.range(3)
    gate_op = gate.on(*q[:2])
    tagged_op = gate_op.with_tags("custom tag")
    controlled_op = gate_op.controlled_by(q[2])
    classically_controlled_op = gate_op.with_classical_controls('key')
    moment = qubitron.Moment(gate_op)
    circuit = qubitron.Circuit(moment)
    for val in [gate_op, tagged_op, controlled_op, classically_controlled_op, moment, circuit]:
        mock_qm.reset_mock()
        _ = qubitron.decompose(val, context=qubitron.DecompositionContext(qubit_manager=mock_qm))
        assert mock_qm.method_calls == expected_calls

        mock_qm.reset_mock()
        context_qm.reset_mock()
        _ = qubitron.decompose(val, context=qubitron.DecompositionContext(context_qm))
        assert (
            context_qm.method_calls == expected_calls
            if with_context
            else mock_qm.method_calls == expected_calls
        )


class G1(qubitron.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _decompose_with_context_(self, qubits, context):
        yield qubitron.CNOT(qubits[0], context.qubit_manager.qalloc(1)[0])


class G2(qubitron.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _decompose_with_context_(self, qubits, context):
        yield G1()(*context.qubit_manager.qalloc(1))


@mock.patch('qubitron.protocols.decompose_protocol._CONTEXT_COUNTER', itertools.count())
def test_successive_decompose_once_succeed() -> None:
    op = G2()(qubitron.NamedQubit('q'))
    d1 = qubitron.decompose_once(op)
    d2 = qubitron.decompose_once(d1[0])
    assert d2 == [
        qubitron.CNOT(
            qubitron.ops.CleanQubit(0, prefix='_decompose_protocol_0'),
            qubitron.ops.CleanQubit(0, prefix='_decompose_protocol_1'),
        )
    ]


def test_decompose_without_context_succeed() -> None:
    op = G2()(qubitron.NamedQubit('q'))
    assert qubitron.decompose(op, keep=lambda op: op.gate is qubitron.CNOT) == [
        qubitron.CNOT(
            qubitron.ops.CleanQubit(0, prefix='_decompose_protocol'),
            qubitron.ops.CleanQubit(1, prefix='_decompose_protocol'),
        )
    ]
