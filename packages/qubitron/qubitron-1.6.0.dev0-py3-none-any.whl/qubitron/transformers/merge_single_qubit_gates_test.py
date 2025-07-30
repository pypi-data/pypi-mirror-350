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


def assert_optimizes(optimized: qubitron.AbstractCircuit, expected: qubitron.AbstractCircuit):
    # Ignore differences that would be caught by follow-up optimizations.
    followup_transformers: list[qubitron.TRANSFORMER] = [
        qubitron.drop_negligible_operations,
        qubitron.drop_empty_moments,
    ]
    for transform in followup_transformers:
        optimized = transform(optimized)
        expected = transform(expected)

    qubitron.testing.assert_same_circuits(optimized, expected)


def test_merge_single_qubit_gates_to_phased_x_and_z():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        qubitron.X(a),
        qubitron.Y(b) ** 0.5,
        qubitron.CZ(a, b),
        qubitron.H(a),
        qubitron.Z(a),
        qubitron.measure(b, key="m"),
        qubitron.H(a).with_classical_controls("m"),
    )
    assert_optimizes(
        optimized=qubitron.merge_single_qubit_gates_to_phased_x_and_z(c),
        expected=qubitron.Circuit(
            qubitron.PhasedXPowGate(phase_exponent=1)(a),
            qubitron.PhasedXPowGate(phase_exponent=0.5)(b) ** 0.5,
            qubitron.CZ(a, b),
            (qubitron.PhasedXPowGate(phase_exponent=-0.5)(a)) ** 0.5,
            qubitron.measure(b, key="m"),
            qubitron.H(a).with_classical_controls("m"),
        ),
    )


def test_merge_single_qubit_gates_to_phased_x_and_z_deep():
    a = qubitron.NamedQubit("a")
    c_nested = qubitron.FrozenCircuit(qubitron.H(a), qubitron.Z(a), qubitron.H(a).with_tags("ignore"))
    c_nested_merged = qubitron.FrozenCircuit(
        qubitron.PhasedXPowGate(phase_exponent=-0.5, exponent=0.5).on(a), qubitron.H(a).with_tags("ignore")
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = qubitron.Circuit(
        c_nested_merged,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = qubitron.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = qubitron.merge_single_qubit_gates_to_phased_x_and_z(c_orig, context=context)
    qubitron.testing.assert_same_circuits(c_new, c_expected)


def _phxz(a: float, x: float, z: float):
    return qubitron.PhasedXZGate(axis_phase_exponent=a, x_exponent=x, z_exponent=z)


def test_merge_single_qubit_gates_to_phxz():
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        qubitron.X(a),
        qubitron.Y(b) ** 0.5,
        qubitron.CZ(a, b),
        qubitron.H(a),
        qubitron.Z(a),
        qubitron.measure(b, key="m"),
        qubitron.H(a).with_classical_controls("m"),
    )
    assert_optimizes(
        optimized=qubitron.merge_single_qubit_gates_to_phxz(c),
        expected=qubitron.Circuit(
            _phxz(-1, 1, 0).on(a),
            _phxz(0.5, 0.5, 0).on(b),
            qubitron.CZ(a, b),
            _phxz(-0.5, 0.5, 0).on(a),
            qubitron.measure(b, key="m"),
            qubitron.H(a).with_classical_controls("m"),
        ),
    )


def test_merge_single_qubit_gates_to_phxz_deep():
    a = qubitron.NamedQubit("a")
    c_nested = qubitron.FrozenCircuit(qubitron.H(a), qubitron.Z(a), qubitron.H(a).with_tags("ignore"))
    c_nested_merged = qubitron.FrozenCircuit(_phxz(-0.5, 0.5, 0).on(a), qubitron.H(a).with_tags("ignore"))
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = qubitron.Circuit(
        c_nested_merged,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = qubitron.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = qubitron.merge_single_qubit_gates_to_phxz(c_orig, context=context)
    qubitron.testing.assert_same_circuits(c_new, c_expected)


def test_merge_single_qubit_moments_to_phxz():
    q = qubitron.LineQubit.range(3)
    c_orig = qubitron.Circuit(
        qubitron.Moment(qubitron.X.on_each(*q[:2])),
        qubitron.Moment(qubitron.T.on_each(*q[1:])),
        qubitron.Moment(qubitron.Y.on_each(*q[:2])),
        qubitron.Moment(qubitron.CZ(*q[:2]), qubitron.Y(q[2])),
        qubitron.Moment(qubitron.X.on_each(*q[:2])),
        qubitron.Moment(qubitron.T.on_each(*q[1:])),
        qubitron.Moment(qubitron.Y.on_each(*q[:2])),
        qubitron.Moment(qubitron.Y(q[0]).with_tags("nocompile"), qubitron.Z.on_each(*q[1:])),
        qubitron.Moment(qubitron.X.on_each(q[0])),
        qubitron.Moment(qubitron.measure(q[0], key="a")),
        qubitron.Moment(qubitron.X(q[1]).with_classical_controls("a")),
        qubitron.Moment(qubitron.X.on_each(q[1])),
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───────Y───@───X───────Y───Y[nocompile]───X───M───────────
                  │                                  ║
1: ───X───T───Y───@───X───T───Y───Z──────────────────╫───X───X───
                                                     ║   ║
2: ───────T───────Y───────T───────Z──────────────────╫───╫───────
                                                     ║   ║
a: ══════════════════════════════════════════════════@═══^═══════
''',
    )
    context = qubitron.TransformerContext(tags_to_ignore=("nocompile",))
    c_new = qubitron.merge_single_qubit_moments_to_phxz(c_orig, context=context)
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───PhXZ(a=-0.5,x=0,z=-1)──────@───PhXZ(a=-0.5,x=0,z=-1)──────Y[nocompile]───X───M───────────
                                 │                                                 ║
1: ───PhXZ(a=-0.25,x=0,z=0.75)───@───PhXZ(a=-0.25,x=0,z=0.75)───Z──────────────────╫───X───X───
                                                                                   ║   ║
2: ───PhXZ(a=0.25,x=0,z=0.25)────Y───PhXZ(a=0.25,x=0,z=0.25)────Z──────────────────╫───╫───────
                                                                                   ║   ║
a: ════════════════════════════════════════════════════════════════════════════════@═══^═══════
''',
    )


def test_merge_single_qubit_moments_to_phxz_deep():
    q = qubitron.LineQubit.range(3)
    x_t_y = qubitron.FrozenCircuit(
        qubitron.Moment(qubitron.X.on_each(*q[:2])),
        qubitron.Moment(qubitron.T.on_each(*q[1:])),
        qubitron.Moment(qubitron.Y.on_each(*q[:2])),
    )
    c_nested = qubitron.FrozenCircuit(
        x_t_y,
        qubitron.Moment(qubitron.CZ(*q[:2]), qubitron.Y(q[2])),
        x_t_y,
        qubitron.Moment(qubitron.Y(q[0]).with_tags("ignore"), qubitron.Z.on_each(*q[1:])),
    )

    c_nested_merged = qubitron.FrozenCircuit(
        [_phxz(-0.25, 0.0, 0.75)(q[1]), _phxz(0.25, 0.0, 0.25)(q[2]), _phxz(-0.5, 0.0, -1.0)(q[0])],
        [qubitron.CZ(q[0], q[1]), qubitron.Y(q[2])],
        [_phxz(-0.25, 0.0, 0.75)(q[1]), _phxz(0.25, 0.0, 0.25)(q[2]), _phxz(-0.5, 0.0, -1.0)(q[0])],
        qubitron.Moment(qubitron.Y(q[0]).with_tags("ignore"), qubitron.Z.on_each(*q[1:])),
    )
    c_orig = qubitron.Circuit(
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        qubitron.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = qubitron.Circuit(
        c_nested_merged,
        qubitron.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        qubitron.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = qubitron.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = qubitron.merge_single_qubit_moments_to_phxz(c_orig, context=context)
    qubitron.testing.assert_allclose_up_to_global_phase(
        c_new.unitary(), c_expected.unitary(), atol=1e-7
    )


def test_merge_single_qubit_moments_to_phxz_global_phase():
    c = qubitron.Circuit(qubitron.GlobalPhaseGate(1j).on())
    c2 = qubitron.merge_single_qubit_gates_to_phxz(c)
    assert c == c2


def test_merge_single_qubit_moments_to_phased_x_and_z_global_phase():
    c = qubitron.Circuit(qubitron.GlobalPhaseGate(1j).on())
    c2 = qubitron.merge_single_qubit_gates_to_phased_x_and_z(c)
    assert c == c2
