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

import qubitron


def test_align_basic_no_context():
    q1 = qubitron.NamedQubit('q1')
    q2 = qubitron.NamedQubit('q2')
    c = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.X(q1)]),
            qubitron.Moment([qubitron.Y(q1), qubitron.X(q2)]),
            qubitron.Moment([qubitron.X(q1)]),
        ]
    )
    qubitron.testing.assert_same_circuits(
        qubitron.align_left(c),
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(q1), qubitron.X(q2)]),
            qubitron.Moment([qubitron.Y(q1)]),
            qubitron.Moment([qubitron.X(q1)]),
        ),
    )
    qubitron.testing.assert_same_circuits(
        qubitron.align_right(c),
        qubitron.Circuit(
            qubitron.Moment([qubitron.X(q1)]),
            qubitron.Moment([qubitron.Y(q1)]),
            qubitron.Moment([qubitron.X(q1), qubitron.X(q2)]),
        ),
    )


def test_align_left_no_compile_context():
    q1 = qubitron.NamedQubit('q1')
    q2 = qubitron.NamedQubit('q2')
    qubitron.testing.assert_same_circuits(
        qubitron.align_left(
            qubitron.Circuit(
                [
                    qubitron.Moment([qubitron.X(q1)]),
                    qubitron.Moment([qubitron.Y(q1), qubitron.X(q2)]),
                    qubitron.Moment([qubitron.X(q1), qubitron.Y(q2).with_tags("nocompile")]),
                    qubitron.Moment([qubitron.Y(q1)]),
                    qubitron.measure(*[q1, q2], key='a'),
                ]
            ),
            context=qubitron.TransformerContext(tags_to_ignore=["nocompile"]),
        ),
        qubitron.Circuit(
            [
                qubitron.Moment([qubitron.X(q1), qubitron.X(q2)]),
                qubitron.Moment([qubitron.Y(q1)]),
                qubitron.Moment([qubitron.X(q1), qubitron.Y(q2).with_tags("nocompile")]),
                qubitron.Moment([qubitron.Y(q1)]),
                qubitron.measure(*[q1, q2], key='a'),
            ]
        ),
    )


def test_align_left_deep():
    q1, q2 = qubitron.LineQubit.range(2)
    c_nested = qubitron.FrozenCircuit(
        [
            qubitron.Moment([qubitron.X(q1)]),
            qubitron.Moment([qubitron.Y(q2)]),
            qubitron.Moment([qubitron.Z(q1), qubitron.Y(q2).with_tags("nocompile")]),
            qubitron.Moment([qubitron.Y(q1)]),
            qubitron.measure(q2, key='a'),
            qubitron.Z(q1).with_classical_controls('a'),
        ]
    )
    c_nested_aligned = qubitron.FrozenCircuit(
        qubitron.Moment(qubitron.X(q1), qubitron.Y(q2)),
        qubitron.Moment(qubitron.Z(q1)),
        qubitron.Moment([qubitron.Y(q1), qubitron.Y(q2).with_tags("nocompile")]),
        qubitron.measure(q2, key='a'),
        qubitron.Z(q1).with_classical_controls('a'),
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
    )
    c_expected = qubitron.Circuit(
        c_nested_aligned,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested_aligned,
        qubitron.CircuitOperation(c_nested_aligned).repeat(5).with_tags("preserve_tag"),
    )
    context = qubitron.TransformerContext(tags_to_ignore=["nocompile"], deep=True)
    qubitron.testing.assert_same_circuits(qubitron.align_left(c_orig, context=context), c_expected)


def test_align_left_subset_of_operations():
    q1 = qubitron.NamedQubit('q1')
    q2 = qubitron.NamedQubit('q2')
    tag = "op_to_align"
    c_orig = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.Y(q1)]),
            qubitron.Moment([qubitron.X(q2)]),
            qubitron.Moment([qubitron.X(q1).with_tags(tag)]),
            qubitron.Moment([qubitron.Y(q2)]),
            qubitron.measure(*[q1, q2], key='a'),
        ]
    )
    c_exp = qubitron.Circuit(
        [
            qubitron.Moment([qubitron.Y(q1)]),
            qubitron.Moment([qubitron.X(q1).with_tags(tag), qubitron.X(q2)]),
            qubitron.Moment(),
            qubitron.Moment([qubitron.Y(q2)]),
            qubitron.measure(*[q1, q2], key='a'),
        ]
    )
    qubitron.testing.assert_same_circuits(
        qubitron.toggle_tags(
            qubitron.align_left(
                qubitron.toggle_tags(c_orig, [tag]),
                context=qubitron.TransformerContext(tags_to_ignore=[tag]),
            ),
            [tag],
        ),
        c_exp,
    )


def test_align_right_no_compile_context():
    q1 = qubitron.NamedQubit('q1')
    q2 = qubitron.NamedQubit('q2')
    qubitron.testing.assert_same_circuits(
        qubitron.align_right(
            qubitron.Circuit(
                [
                    qubitron.Moment([qubitron.X(q1)]),
                    qubitron.Moment([qubitron.Y(q1), qubitron.X(q2).with_tags("nocompile")]),
                    qubitron.Moment([qubitron.X(q1), qubitron.Y(q2)]),
                    qubitron.Moment([qubitron.Y(q1)]),
                    qubitron.measure(*[q1, q2], key='a'),
                ]
            ),
            context=qubitron.TransformerContext(tags_to_ignore=["nocompile"]),
        ),
        qubitron.Circuit(
            [
                qubitron.Moment([qubitron.X(q1)]),
                qubitron.Moment([qubitron.Y(q1), qubitron.X(q2).with_tags("nocompile")]),
                qubitron.Moment([qubitron.X(q1)]),
                qubitron.Moment([qubitron.Y(q1), qubitron.Y(q2)]),
                qubitron.measure(*[q1, q2], key='a'),
            ]
        ),
    )


def test_align_right_deep():
    q1, q2 = qubitron.LineQubit.range(2)
    c_nested = qubitron.FrozenCircuit(
        qubitron.Moment([qubitron.X(q1)]),
        qubitron.Moment([qubitron.Y(q1), qubitron.X(q2).with_tags("nocompile")]),
        qubitron.Moment([qubitron.X(q2)]),
        qubitron.Moment([qubitron.Y(q1)]),
        qubitron.measure(q1, key='a'),
        qubitron.Z(q2).with_classical_controls('a'),
    )
    c_nested_aligned = qubitron.FrozenCircuit(
        qubitron.Moment([qubitron.X(q1), qubitron.X(q2).with_tags("nocompile")]),
        [qubitron.Y(q1), qubitron.Y(q1)],
        qubitron.Moment(qubitron.measure(q1, key='a'), qubitron.X(q2)),
        qubitron.Z(q2).with_classical_controls('a'),
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
    )
    c_expected = qubitron.Circuit(
        c_nested_aligned,
        qubitron.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        qubitron.Moment(),
        c_nested_aligned,
        qubitron.CircuitOperation(c_nested_aligned).repeat(5).with_tags("preserve_tag"),
    )
    context = qubitron.TransformerContext(tags_to_ignore=["nocompile"], deep=True)
    qubitron.testing.assert_same_circuits(qubitron.align_right(c_orig, context=context), c_expected)


def test_classical_control():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.H(q0), qubitron.measure(q0, key='m'), qubitron.X(q1).with_classical_controls('m')
    )
    qubitron.testing.assert_same_circuits(qubitron.align_left(circuit), circuit)
    qubitron.testing.assert_same_circuits(qubitron.align_right(circuit), circuit)


def test_measurement_and_classical_control_same_moment_preserve_order():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit()
    op_measure = qubitron.measure(q0, key='m')
    op_controlled = qubitron.X(q1).with_classical_controls('m')
    circuit.append(op_measure)
    circuit.append(op_controlled, qubitron.InsertStrategy.INLINE)
    circuit = qubitron.align_right(circuit)
    ops_in_order = list(circuit.all_operations())
    assert ops_in_order[0] == op_measure
    assert ops_in_order[1] == op_controlled
