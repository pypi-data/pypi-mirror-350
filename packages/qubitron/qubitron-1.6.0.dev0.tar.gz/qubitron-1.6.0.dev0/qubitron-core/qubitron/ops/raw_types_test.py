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

from typing import AbstractSet, Any, Iterator

import numpy as np
import pytest
import sympy

import qubitron


class ValidQubit(qubitron.Qid):
    def __init__(self, name):
        self._name = name

    @property
    def dimension(self):
        return 2

    def _comparison_key(self):
        return self._name

    def __repr__(self):
        return f'ValidQubit({self._name!r})'

    def __str__(self):
        return f'TQ_{self._name!s}'


class ValidQid(qubitron.Qid):
    def __init__(self, name, dimension):
        self._name = name
        self._dimension = dimension
        self.validate_dimension(dimension)

    @property
    def dimension(self):
        return self._dimension

    def with_dimension(self, dimension):
        return ValidQid(self._name, dimension)

    def _comparison_key(self):
        return self._name


def test_wrapped_qid():
    assert type(ValidQubit('a').with_dimension(3)) is not ValidQubit
    assert type(ValidQubit('a').with_dimension(2)) is ValidQubit
    assert type(ValidQubit('a').with_dimension(5).with_dimension(2)) is ValidQubit
    assert ValidQubit('a').with_dimension(3).with_dimension(4) == ValidQubit('a').with_dimension(4)
    assert ValidQubit('a').with_dimension(3).qubit == ValidQubit('a')
    assert ValidQubit('a').with_dimension(3) == ValidQubit('a').with_dimension(3)
    assert ValidQubit('a').with_dimension(3) < ValidQubit('a').with_dimension(4)
    assert ValidQubit('a').with_dimension(3) < ValidQubit('b').with_dimension(3)
    assert ValidQubit('a').with_dimension(4) < ValidQubit('b').with_dimension(3)

    qubitron.testing.assert_equivalent_repr(
        ValidQubit('a').with_dimension(3), global_vals={'ValidQubit': ValidQubit}
    )
    assert str(ValidQubit('a').with_dimension(3)) == 'TQ_a (d=3)'

    assert ValidQubit('zz').with_dimension(3)._json_dict_() == {
        'qubit': ValidQubit('zz'),
        'dimension': 3,
    }

    assert not ValidQubit('zz') == 4
    assert ValidQubit('zz') != 4
    assert ValidQubit('zz') > ValidQubit('aa')
    assert ValidQubit('zz') <= ValidQubit('zz')
    assert ValidQubit('zz') >= ValidQubit('zz')
    assert ValidQubit('zz') >= ValidQubit('aa')


def test_qid_dimension():
    assert ValidQubit('a').dimension == 2
    assert ValidQubit('a').with_dimension(3).dimension == 3
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQubit('a').with_dimension(0)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQubit('a').with_dimension(-3)

    assert ValidQid('a', 3).dimension == 3
    assert ValidQid('a', 3).with_dimension(2).dimension == 2
    assert ValidQid('a', 3).with_dimension(4) == ValidQid('a', 4)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQid('a', 3).with_dimension(0)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQid('a', 3).with_dimension(-3)


class ValiGate(qubitron.Gate):
    def _num_qubits_(self):
        return 2

    def validate_args(self, qubits):
        if len(qubits) == 1:
            return  # Bypass check for some tests
        super().validate_args(qubits)

    def _has_mixture_(self):
        return True


def test_gate():
    a, b, c = qubitron.LineQubit.range(3)

    g = ValiGate()
    assert qubitron.num_qubits(g) == 2

    _ = g.on(a, c)
    with pytest.raises(ValueError, match='Wrong number'):
        _ = g.on(a, c, b)

    _ = g(a)  # Bypassing validate_args
    _ = g(a, c)
    with pytest.raises(ValueError, match='Wrong number'):
        _ = g(c, b, a)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = g(a, b.with_dimension(3))

    assert g.controlled(0) is g


def test_op():
    a, b, c, d = qubitron.LineQubit.range(4)
    g = ValiGate()
    op = g(a, b)
    assert op.controlled_by() is op
    controlled_op = op.controlled_by(c, d)
    assert controlled_op.sub_operation == op
    assert controlled_op.controls == (c, d)


def test_op_validate():
    op = qubitron.X(qubitron.LineQid(0, 2))
    op2 = qubitron.CNOT(*qubitron.LineQid.range(2, dimension=2))
    op.validate_args([qubitron.LineQid(1, 2)])  # Valid
    op2.validate_args(qubitron.LineQid.range(1, 3, dimension=2))  # Valid
    with pytest.raises(ValueError, match='Wrong shape'):
        op.validate_args([qubitron.LineQid(1, 9)])
    with pytest.raises(ValueError, match='Wrong number'):
        op.validate_args([qubitron.LineQid(1, 2), qubitron.LineQid(2, 2)])
    with pytest.raises(ValueError, match='Duplicate'):
        op2.validate_args([qubitron.LineQid(1, 2), qubitron.LineQid(1, 2)])


def test_disable_op_validation():
    q0, q1 = qubitron.LineQubit.range(2)
    h_op = qubitron.H(q0)

    # Fails normally.
    with pytest.raises(ValueError, match='Wrong number'):
        _ = qubitron.H(q0, q1)
    with pytest.raises(ValueError, match='Wrong number'):
        h_op.validate_args([q0, q1])

    # Passes, skipping validation.
    with qubitron.with_debug(False):
        op = qubitron.H(q0, q1)
        assert op.qubits == (q0, q1)
        h_op.validate_args([q0, q1])

    # Fails again when validation is re-enabled.
    with pytest.raises(ValueError, match='Wrong number'):
        _ = qubitron.H(q0, q1)
    with pytest.raises(ValueError, match='Wrong number'):
        h_op.validate_args([q0, q1])


def test_default_validation_and_inverse():
    class TestGate(qubitron.Gate):
        def _num_qubits_(self):
            return 2

        def _decompose_(self, qubits):
            a, b = qubits
            yield qubitron.Z(a)
            yield qubitron.S(b)
            yield qubitron.X(a)

        def __eq__(self, other):
            return isinstance(other, TestGate)

        def __repr__(self):
            return 'TestGate()'

    a, b = qubitron.LineQubit.range(2)

    with pytest.raises(ValueError, match='number of qubits'):
        TestGate().on(a)

    t = TestGate().on(a, b)
    i = t**-1
    assert i**-1 == t
    assert t**-1 == i
    assert qubitron.decompose(i) == [qubitron.X(a), qubitron.S(b) ** -1, qubitron.Z(a)]
    assert [*i._decompose_()] == [qubitron.X(a), qubitron.S(b) ** -1, qubitron.Z(a)]
    assert [*i.gate._decompose_([a, b])] == [qubitron.X(a), qubitron.S(b) ** -1, qubitron.Z(a)]
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(i), qubitron.unitary(t).conj().T, atol=1e-8
    )

    qubitron.testing.assert_implements_consistent_protocols(i, local_vals={'TestGate': TestGate})


def test_default_no_qubits():
    class TestOp(qubitron.Operation):
        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            pass

    op = TestOp()
    assert op.controlled_by(*[]) is op
    op = TestOp().with_tags("abc")
    assert op.classical_controls == frozenset()


def test_default_inverse():
    class TestGate(qubitron.Gate):
        def _num_qubits_(self):
            return 3

        def _decompose_(self, qubits):
            return (qubitron.X**0.1).on_each(*qubits)

    assert qubitron.inverse(TestGate(), None) is not None
    qubitron.testing.assert_has_consistent_qid_shape(qubitron.inverse(TestGate()))
    qubitron.testing.assert_has_consistent_qid_shape(
        qubitron.inverse(TestGate().on(*qubitron.LineQubit.range(3)))
    )


def test_no_inverse_if_not_unitary():
    class TestGate(qubitron.Gate):
        def _num_qubits_(self):
            return 1

        def _decompose_(self, qubits):
            return qubitron.amplitude_damp(0.5).on(qubits[0])

    assert qubitron.inverse(TestGate(), None) is None


def test_default_qudit_inverse():
    class TestGate(qubitron.Gate):
        def _qid_shape_(self):
            return (1, 2, 3)

        def _decompose_(self, qubits):
            return (qubitron.X**0.1).on(qubits[1])

    assert qubitron.qid_shape(qubitron.inverse(TestGate(), None)) == (1, 2, 3)
    qubitron.testing.assert_has_consistent_qid_shape(qubitron.inverse(TestGate()))


@pytest.mark.parametrize(
    'expression, expected_result',
    (
        (qubitron.X * 2, 2 * qubitron.X),
        (qubitron.Y * 2, qubitron.Y + qubitron.Y),
        (qubitron.Z - qubitron.Z + qubitron.Z, qubitron.Z.wrap_in_linear_combination()),
        (1j * qubitron.S * 1j, -qubitron.S),
        (qubitron.CZ * 1, qubitron.CZ / 1),
        (-qubitron.CSWAP * 1j, qubitron.CSWAP / 1j),
        (qubitron.TOFFOLI * 0.5, qubitron.TOFFOLI / 2),
        (-qubitron.X * sympy.Symbol('s'), -sympy.Symbol('s') * qubitron.X),
    ),
)
def test_gate_algebra(expression, expected_result):
    assert expression == expected_result


def test_gate_shape():
    class ShapeGate(qubitron.Gate):
        def _qid_shape_(self):
            return (1, 2, 3, 4)

    class QubitGate(qubitron.Gate):
        def _num_qubits_(self):
            return 3

    class DeprecatedGate(qubitron.Gate):
        def num_qubits(self):
            return 3

    shape_gate = ShapeGate()
    assert qubitron.qid_shape(shape_gate) == (1, 2, 3, 4)
    assert qubitron.num_qubits(shape_gate) == 4
    assert shape_gate.num_qubits() == 4

    qubit_gate = QubitGate()
    assert qubitron.qid_shape(qubit_gate) == (2, 2, 2)
    assert qubitron.num_qubits(qubit_gate) == 3
    assert qubit_gate.num_qubits() == 3

    dep_gate = DeprecatedGate()
    assert qubitron.qid_shape(dep_gate) == (2, 2, 2)
    assert qubitron.num_qubits(dep_gate) == 3
    assert dep_gate.num_qubits() == 3


def test_gate_shape_protocol():
    """This test is only needed while the `_num_qubits_` and `_qid_shape_`
    methods are implemented as alternatives.  This can be removed once the
    deprecated `num_qubits` method is removed."""

    class NotImplementedGate1(qubitron.Gate):
        def _num_qubits_(self):
            return NotImplemented

        def _qid_shape_(self):
            return NotImplemented

    class NotImplementedGate2(qubitron.Gate):
        def _num_qubits_(self):
            return NotImplemented

    class NotImplementedGate3(qubitron.Gate):
        def _qid_shape_(self):
            return NotImplemented

    class ShapeGate(qubitron.Gate):
        def _num_qubits_(self):
            return NotImplemented

        def _qid_shape_(self):
            return (1, 2, 3)

    class QubitGate(qubitron.Gate):
        def _num_qubits_(self):
            return 2

        def _qid_shape_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.qid_shape(NotImplementedGate1())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.num_qubits(NotImplementedGate1())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate1().num_qubits()  # Deprecated
    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.qid_shape(NotImplementedGate2())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.num_qubits(NotImplementedGate2())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate2().num_qubits()  # Deprecated
    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.qid_shape(NotImplementedGate3())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        qubitron.num_qubits(NotImplementedGate3())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate3().num_qubits()  # Deprecated
    assert qubitron.qid_shape(ShapeGate()) == (1, 2, 3)
    assert qubitron.num_qubits(ShapeGate()) == 3
    assert ShapeGate().num_qubits() == 3  # Deprecated
    assert qubitron.qid_shape(QubitGate()) == (2, 2)
    assert qubitron.num_qubits(QubitGate()) == 2
    assert QubitGate().num_qubits() == 2  # Deprecated


def test_operation_shape():
    class FixedQids(qubitron.Operation):
        def with_qubits(self, *new_qids):
            raise NotImplementedError

    class QubitOp(FixedQids):
        @property
        def qubits(self):
            return qubitron.LineQubit.range(2)

    class NumQubitOp(FixedQids):
        @property
        def qubits(self):
            return qubitron.LineQubit.range(3)

        def _num_qubits_(self):
            return 3

    class ShapeOp(FixedQids):
        @property
        def qubits(self):
            return qubitron.LineQubit.range(4)

        def _qid_shape_(self):
            return (1, 2, 3, 4)

    qubit_op = QubitOp()
    assert len(qubit_op.qubits) == 2
    assert qubitron.qid_shape(qubit_op) == (2, 2)
    assert qubitron.num_qubits(qubit_op) == 2

    num_qubit_op = NumQubitOp()
    assert len(num_qubit_op.qubits) == 3
    assert qubitron.qid_shape(num_qubit_op) == (2, 2, 2)
    assert qubitron.num_qubits(num_qubit_op) == 3

    shape_op = ShapeOp()
    assert len(shape_op.qubits) == 4
    assert qubitron.qid_shape(shape_op) == (1, 2, 3, 4)
    assert qubitron.num_qubits(shape_op) == 4


def test_gate_json_dict():
    g = qubitron.CSWAP  # not an eigen gate (which has its own _json_dict_)
    assert g._json_dict_() == {}


def test_inverse_composite_diagram_info():
    class Gate(qubitron.Gate):
        def _decompose_(self, qubits):
            return qubitron.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

    c = qubitron.inverse(Gate())
    assert qubitron.circuit_diagram_info(c, default=None) is None

    class Gate2(qubitron.Gate):
        def _decompose_(self, qubits):
            return qubitron.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

        def _circuit_diagram_info_(self, args):
            return 's!'

    c = qubitron.inverse(Gate2())
    assert qubitron.circuit_diagram_info(c) == qubitron.CircuitDiagramInfo(
        wire_symbols=('s!',), exponent=-1
    )


def test_tagged_operation_equality():
    eq = qubitron.testing.EqualsTester()
    q1 = qubitron.GridQubit(1, 1)
    op = qubitron.X(q1)
    op2 = qubitron.Y(q1)

    eq.add_equality_group(op)
    eq.add_equality_group(op.with_tags('tag1'), qubitron.TaggedOperation(op, 'tag1'))
    eq.add_equality_group(op2.with_tags('tag1'), qubitron.TaggedOperation(op2, 'tag1'))
    eq.add_equality_group(op.with_tags('tag2'), qubitron.TaggedOperation(op, 'tag2'))
    eq.add_equality_group(
        op.with_tags('tag1', 'tag2'),
        op.with_tags('tag1').with_tags('tag2'),
        qubitron.TaggedOperation(op, 'tag1', 'tag2'),
    )


def test_tagged_operation():
    q1 = qubitron.GridQubit(1, 1)
    q2 = qubitron.GridQubit(2, 2)
    op = qubitron.X(q1).with_tags('tag1')
    op_repr = "qubitron.X(qubitron.GridQubit(1, 1))"
    assert repr(op) == f"qubitron.TaggedOperation({op_repr}, 'tag1')"

    assert op.qubits == (q1,)
    assert op.tags == ('tag1',)
    assert op.gate == qubitron.X
    assert op.with_qubits(q2) == qubitron.X(q2).with_tags('tag1')
    assert op.with_qubits(q2).qubits == (q2,)
    assert not qubitron.is_measurement(op)

    # Tags can't be types
    # This is to prevent typos of qubitron.X(q1).with_tags(TagType)
    # when you meant qubitron.X(q1).with_tags(TagType())
    with pytest.raises(ValueError, match="cannot be types"):
        _ = qubitron.X(q1).with_tags(qubitron.Circuit)


def test_with_tags_returns_same_instance_if_possible():
    untagged = qubitron.X(qubitron.GridQubit(1, 1))
    assert untagged.with_tags() is untagged

    tagged = untagged.with_tags('foo')
    assert tagged.with_tags() is tagged


def test_tagged_measurement():
    assert not qubitron.is_measurement(qubitron.global_phase_operation(coefficient=-1.0).with_tags('tag0'))

    a = qubitron.LineQubit(0)
    op = qubitron.measure(a, key='m').with_tags('tag')
    assert qubitron.is_measurement(op)

    remap_op = qubitron.with_measurement_key_mapping(op, {'m': 'k'})
    assert remap_op.tags == ('tag',)
    assert qubitron.is_measurement(remap_op)
    assert qubitron.measurement_key_names(remap_op) == {'k'}
    assert qubitron.with_measurement_key_mapping(op, {'x': 'k'}) == op


def test_cannot_remap_non_measurement_gate():
    a = qubitron.LineQubit(0)
    op = qubitron.X(a).with_tags('tag')

    assert qubitron.with_measurement_key_mapping(op, {'m': 'k'}) is NotImplemented


def test_circuit_diagram():
    class TaggyTag:
        """Tag with a custom str function to test circuit diagrams."""

        def __str__(self):
            return '<taggy>'

    h = qubitron.H(qubitron.GridQubit(1, 1))
    tagged_h = h.with_tags('tag1')
    non_string_tag_h = h.with_tags(TaggyTag())

    expected = qubitron.CircuitDiagramInfo(
        wire_symbols=("H[tag1]",),
        exponent=1.0,
        connected=True,
        exponent_qubit_index=None,
        auto_exponent_parens=True,
    )
    args = qubitron.CircuitDiagramInfoArgs(None, None, None, None, None, False)
    assert qubitron.circuit_diagram_info(tagged_h) == expected
    assert qubitron.circuit_diagram_info(tagged_h, args) == qubitron.circuit_diagram_info(h)

    c = qubitron.Circuit(tagged_h)
    diagram_with_tags = "(1, 1): ───H[tag1]───"
    diagram_without_tags = "(1, 1): ───H───"
    assert str(qubitron.Circuit(tagged_h)) == diagram_with_tags
    assert c.to_text_diagram() == diagram_with_tags
    assert c.to_text_diagram(include_tags=False) == diagram_without_tags

    c = qubitron.Circuit(non_string_tag_h)
    diagram_with_non_string_tag = "(1, 1): ───H[<taggy>]───"
    assert c.to_text_diagram() == diagram_with_non_string_tag
    assert c.to_text_diagram(include_tags=False) == diagram_without_tags


def test_circuit_diagram_tagged_global_phase():
    # Tests global phase operation
    q = qubitron.NamedQubit('a')
    global_phase = qubitron.global_phase_operation(coefficient=-1.0).with_tags('tag0')

    # Just global phase in a circuit
    assert qubitron.circuit_diagram_info(global_phase, default='default') == 'default'
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(global_phase), "\n\nglobal phase:   π[tag0]", use_unicode_characters=True
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(global_phase),
        "\n\nglobal phase:   π",
        use_unicode_characters=True,
        include_tags=False,
    )

    expected = qubitron.CircuitDiagramInfo(
        wire_symbols=(),
        exponent=1.0,
        connected=True,
        exponent_qubit_index=None,
        auto_exponent_parens=True,
    )

    # Operation with no qubits and returns diagram info with no wire symbols
    class NoWireSymbols(qubitron.GlobalPhaseGate):
        def _circuit_diagram_info_(
            self, args: qubitron.CircuitDiagramInfoArgs
        ) -> qubitron.CircuitDiagramInfo:
            return expected

    no_wire_symbol_op = NoWireSymbols(coefficient=-1.0)().with_tags('tag0')
    assert qubitron.circuit_diagram_info(no_wire_symbol_op, default='default') == expected
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(no_wire_symbol_op), "\n\nglobal phase:   π[tag0]", use_unicode_characters=True
    )

    # Two global phases in one moment
    tag1 = qubitron.global_phase_operation(coefficient=1j).with_tags('tag1')
    tag2 = qubitron.global_phase_operation(coefficient=1j).with_tags('tag2')
    c = qubitron.Circuit([qubitron.X(q), tag1, tag2])
    qubitron.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X───────────────

global phase:   π[tag1, tag2]""",
        use_unicode_characters=True,
        precision=2,
    )

    # Two moments with global phase, one with another tagged gate
    c = qubitron.Circuit([qubitron.X(q).with_tags('x_tag'), tag1])
    c.append(qubitron.Moment([qubitron.X(q), tag2]))
    qubitron.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X[x_tag]─────X────────────

global phase:   0.5π[tag1]   0.5π[tag2]
""",
        use_unicode_characters=True,
        include_tags=True,
    )


def test_circuit_diagram_no_circuit_diagram():
    class NoCircuitDiagram(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def __repr__(self):
            return 'guess-i-will-repr'

    q = qubitron.GridQubit(1, 1)
    expected = "(1, 1): ───guess-i-will-repr───"
    assert qubitron.Circuit(NoCircuitDiagram()(q)).to_text_diagram() == expected
    expected = "(1, 1): ───guess-i-will-repr[taggy]───"
    assert qubitron.Circuit(NoCircuitDiagram()(q).with_tags('taggy')).to_text_diagram() == expected


def test_tagged_operation_forwards_protocols():
    """The results of all protocols applied to an operation with a tag should
    be equivalent to the result without tags.
    """
    q1 = qubitron.GridQubit(1, 1)
    q2 = qubitron.GridQubit(1, 2)
    h = qubitron.H(q1)
    tag = 'tag1'
    tagged_h = qubitron.H(q1).with_tags(tag)

    np.testing.assert_equal(qubitron.unitary(tagged_h), qubitron.unitary(h))
    assert qubitron.has_unitary(tagged_h)
    assert qubitron.decompose(tagged_h) == qubitron.decompose(h)
    assert [*tagged_h._decompose_()] == qubitron.decompose(h)
    assert qubitron.pauli_expansion(tagged_h) == qubitron.pauli_expansion(h)
    assert qubitron.equal_up_to_global_phase(h, tagged_h)
    assert np.isclose(qubitron.kraus(h), qubitron.kraus(tagged_h)).all()

    assert qubitron.measurement_key_name(qubitron.measure(q1, key='blah').with_tags(tag)) == 'blah'
    assert qubitron.measurement_key_obj(
        qubitron.measure(q1, key='blah').with_tags(tag)
    ) == qubitron.MeasurementKey('blah')

    parameterized_op = qubitron.XPowGate(exponent=sympy.Symbol('t'))(q1).with_tags(tag)
    assert qubitron.is_parameterized(parameterized_op)
    resolver = qubitron.study.ParamResolver({'t': 0.25})
    assert qubitron.resolve_parameters(parameterized_op, resolver) == qubitron.XPowGate(exponent=0.25)(
        q1
    ).with_tags(tag)
    assert qubitron.resolve_parameters_once(parameterized_op, resolver) == qubitron.XPowGate(exponent=0.25)(
        q1
    ).with_tags(tag)
    assert parameterized_op._unitary_() is NotImplemented
    assert parameterized_op._mixture_() is NotImplemented
    assert parameterized_op._kraus_() is NotImplemented

    y = qubitron.Y(q1)
    tagged_y = qubitron.Y(q1).with_tags(tag)
    assert tagged_y**0.5 == qubitron.YPowGate(exponent=0.5)(q1)
    assert tagged_y * 2 == (y * 2)
    assert 3 * tagged_y == (3 * y)
    assert qubitron.phase_by(y, 0.125, 0) == qubitron.phase_by(tagged_y, 0.125, 0)
    controlled_y = tagged_y.controlled_by(q2)
    assert controlled_y.qubits == (q2, q1)
    assert isinstance(controlled_y, qubitron.Operation)
    assert not isinstance(controlled_y, qubitron.TaggedOperation)
    classically_controlled_y = tagged_y.with_classical_controls("a")
    assert classically_controlled_y.classical_controls == frozenset(
        {qubitron.KeyCondition(qubitron.MeasurementKey(name='a'))}
    )
    assert classically_controlled_y == y.with_classical_controls("a")
    assert isinstance(classically_controlled_y, qubitron.Operation)
    assert not isinstance(classically_controlled_y, qubitron.TaggedOperation)

    clifford_x = qubitron.SingleQubitCliffordGate.X(q1)
    tagged_x = qubitron.SingleQubitCliffordGate.X(q1).with_tags(tag)
    assert qubitron.commutes(clifford_x, clifford_x)
    assert qubitron.commutes(tagged_x, clifford_x)
    assert qubitron.commutes(clifford_x, tagged_x)
    assert qubitron.commutes(tagged_x, tagged_x)
    assert qubitron.phase_by(clifford_x, 0.125, 0, default=None) is None
    assert qubitron.phase_by(tagged_x, 0.125, 0, default=None) is None

    assert qubitron.trace_distance_bound(y**0.001) == qubitron.trace_distance_bound(
        (y**0.001).with_tags(tag)
    )

    flip = qubitron.bit_flip(0.5)(q1)
    tagged_flip = qubitron.bit_flip(0.5)(q1).with_tags(tag)
    assert qubitron.has_mixture(tagged_flip)
    assert qubitron.has_kraus(tagged_flip)

    flip_mixture = qubitron.mixture(flip)
    tagged_mixture = qubitron.mixture(tagged_flip)
    assert len(tagged_mixture) == 2
    assert len(tagged_mixture[0]) == 2
    assert len(tagged_mixture[1]) == 2
    assert tagged_mixture[0][0] == flip_mixture[0][0]
    assert np.isclose(tagged_mixture[0][1], flip_mixture[0][1]).all()
    assert tagged_mixture[1][0] == flip_mixture[1][0]
    assert np.isclose(tagged_mixture[1][1], flip_mixture[1][1]).all()

    qubit_map = {q1: 'q1'}
    qasm_args = qubitron.QasmArgs(qubit_id_map=qubit_map)
    assert qubitron.qasm(h, args=qasm_args) == qubitron.qasm(tagged_h, args=qasm_args)

    qubitron.testing.assert_has_consistent_apply_unitary(tagged_h)


class ParameterizableTag:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def _is_parameterized_(self) -> bool:
        return qubitron.is_parameterized(self.value)

    def _parameter_names_(self) -> AbstractSet[str]:
        return qubitron.parameter_names(self.value)

    def _resolve_parameters_(
        self, resolver: qubitron.ParamResolver, recursive: bool
    ) -> ParameterizableTag:
        return ParameterizableTag(qubitron.resolve_parameters(self.value, resolver, recursive))


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_tagged_operation_resolves_parameterized_tags(resolve_fn):
    q = qubitron.GridQubit(0, 0)
    tag = ParameterizableTag(sympy.Symbol('t'))
    assert qubitron.is_parameterized(tag)
    assert qubitron.parameter_names(tag) == {'t'}
    op = qubitron.Z(q).with_tags(tag)
    assert qubitron.is_parameterized(op)
    assert qubitron.parameter_names(op) == {'t'}
    resolved_op = resolve_fn(op, {'t': 10})
    assert resolved_op == qubitron.Z(q).with_tags(ParameterizableTag(10))
    assert not qubitron.is_parameterized(resolved_op)
    assert qubitron.parameter_names(resolved_op) == set()


def test_inverse_composite_standards():
    @qubitron.value_equality
    class Gate(qubitron.Gate):
        def __init__(self, param: qubitron.TParamVal):
            self._param = param

        def _decompose_(self, qubits):
            return qubitron.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

        def _has_unitary_(self):
            return True

        def _value_equality_values_(self):
            return (self._param,)

        def _parameter_names_(self) -> AbstractSet[str]:
            return qubitron.parameter_names(self._param)

        def _is_parameterized_(self) -> bool:
            return qubitron.is_parameterized(self._param)

        def _resolve_parameters_(
            self, resolver: qubitron.ParamResolver, recursive: bool
        ) -> Gate:  # pylint: disable=undefined-variable
            return Gate(qubitron.resolve_parameters(self._param, resolver, recursive))

        def __repr__(self):
            return f'C({self._param})'

    a = sympy.Symbol("a")
    g = qubitron.inverse(Gate(a))
    assert qubitron.is_parameterized(g)
    assert qubitron.parameter_names(g) == {'a'}
    assert qubitron.resolve_parameters(g, {a: 0}) == Gate(0) ** -1
    qubitron.testing.assert_implements_consistent_protocols(g, global_vals={'C': Gate, 'a': a})
    assert str(g) == 'C(a)†'


def test_tagged_act_on():
    class YesActOn(qubitron.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _act_on_(self, sim_state, qubits):
            return True

    class NoActOn(qubitron.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _act_on_(self, sim_state, qubits):
            return NotImplemented

    class MissingActOn(qubitron.Operation):
        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            pass

    q = qubitron.LineQubit(1)
    from qubitron.protocols.act_on_protocol_test import ExampleSimulationState

    args = ExampleSimulationState()
    qubitron.act_on(YesActOn()(q).with_tags("test"), args)
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(NoActOn()(q).with_tags("test"), args)
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(MissingActOn().with_tags("test"), args)


def test_single_qubit_gate_validates_on_each():
    class Example(qubitron.testing.SingleQubitGate):
        def matrix(self):
            pass

    g = Example()
    assert g.num_qubits() == 1

    test_qubits = [qubitron.NamedQubit(str(i)) for i in range(3)]

    _ = g.on_each(*test_qubits)
    _ = g.on_each(test_qubits)

    test_non_qubits = [str(i) for i in range(3)]
    with pytest.raises(ValueError):
        _ = g.on_each(*test_non_qubits)

    with qubitron.with_debug(False):
        assert g.on_each(*test_non_qubits)[0].qubits == ('0',)

    with pytest.raises(ValueError):
        _ = g.on_each(*test_non_qubits)


def test_on_each():
    class CustomGate(qubitron.testing.SingleQubitGate):
        pass

    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = CustomGate()

    assert c.on_each() == []
    assert c.on_each(a) == [c(a)]
    assert c.on_each(a, b) == [c(a), c(b)]
    assert c.on_each(b, a) == [c(b), c(a)]

    assert c.on_each([]) == []
    assert c.on_each([a]) == [c(a)]
    assert c.on_each([a, b]) == [c(a), c(b)]
    assert c.on_each([b, a]) == [c(b), c(a)]
    assert c.on_each([a, [b, a], b]) == [c(a), c(b), c(a), c(b)]

    with pytest.raises(ValueError):
        c.on_each('abcd')
    with pytest.raises(ValueError):
        c.on_each(['abcd'])
    with pytest.raises(ValueError):
        c.on_each([a, 'abcd'])

    qubit_iterator = (q for q in [a, b, a, b])
    assert isinstance(qubit_iterator, Iterator)
    assert c.on_each(qubit_iterator) == [c(a), c(b), c(a), c(b)]


def test_on_each_two_qubits():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    g = qubitron.testing.TwoQubitGate()

    assert g.on_each([]) == []
    assert g.on_each([(a, b)]) == [g(a, b)]
    assert g.on_each([[a, b]]) == [g(a, b)]
    assert g.on_each([(b, a)]) == [g(b, a)]
    assert g.on_each([(a, b), (b, a)]) == [g(a, b), g(b, a)]
    assert g.on_each(zip([a, b], [b, a])) == [g(a, b), g(b, a)]
    assert g.on_each() == []
    assert g.on_each((b, a)) == [g(b, a)]
    assert g.on_each((a, b), (a, b)) == [g(a, b), g(a, b)]
    assert g.on_each(*zip([a, b], [b, a])) == [g(a, b), g(b, a)]
    with pytest.raises(TypeError, match='object is not iterable'):
        g.on_each(a)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each(a, b)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([12])
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([(a, b), 12])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, b), [(a, b)]])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([()])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([(a,)])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([(a, b, a)])

    with qubitron.with_debug(False):
        assert g.on_each([(a, b, a)])[0].qubits == (a, b, a)

    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each(zip([a, a]))
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each(zip([a, a], [b, b], [a, a]))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each('ab')
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each(('ab',))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([('ab',)])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'ab')])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'b')])

    qubit_iterator = (qs for qs in [[a, b], [a, b]])
    assert isinstance(qubit_iterator, Iterator)
    assert g.on_each(qubit_iterator) == [g(a, b), g(a, b)]


def test_on_each_three_qubits():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    g = qubitron.testing.ThreeQubitGate()

    assert g.on_each([]) == []
    assert g.on_each([(a, b, c)]) == [g(a, b, c)]
    assert g.on_each([[a, b, c]]) == [g(a, b, c)]
    assert g.on_each([(c, b, a)]) == [g(c, b, a)]
    assert g.on_each([(a, b, c), (c, b, a)]) == [g(a, b, c), g(c, b, a)]
    assert g.on_each(zip([a, c], [b, b], [c, a])) == [g(a, b, c), g(c, b, a)]
    assert g.on_each() == []
    assert g.on_each((c, b, a)) == [g(c, b, a)]
    assert g.on_each((a, b, c), (c, b, a)) == [g(a, b, c), g(c, b, a)]
    assert g.on_each(*zip([a, c], [b, b], [c, a])) == [g(a, b, c), g(c, b, a)]
    with pytest.raises(TypeError, match='object is not iterable'):
        g.on_each(a)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each(a, b, c)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([12])
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([(a, b, c), 12])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, b, c), [(a, b, c)]])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a,)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a, b)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a, b, c, a)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each(zip([a, a], [b, b]))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each('abc')
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each(('abc',))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([('abc',)])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'abc')])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'bc')])

    qubit_iterator = (qs for qs in [[a, b, c], [a, b, c]])
    assert isinstance(qubit_iterator, Iterator)
    assert g.on_each(qubit_iterator) == [g(a, b, c), g(a, b, c)]


def test_on_each_iterable_qid():
    class QidIter(qubitron.Qid):
        @property
        def dimension(self) -> int:
            return 2

        def _comparison_key(self) -> Any:
            return 1

        def __iter__(self):
            raise NotImplementedError()

    assert qubitron.H.on_each(QidIter())[0] == qubitron.H.on(QidIter())


@pytest.mark.parametrize(
    'op', [qubitron.X(qubitron.NamedQubit("q")), qubitron.X(qubitron.NamedQubit("q")).with_tags("tagged_op")]
)
def test_with_methods_return_self_on_empty_conditions(op):
    assert op is op.with_tags(*[])
    assert op is op.with_classical_controls(*[])
    assert op is op.controlled_by(*[])
