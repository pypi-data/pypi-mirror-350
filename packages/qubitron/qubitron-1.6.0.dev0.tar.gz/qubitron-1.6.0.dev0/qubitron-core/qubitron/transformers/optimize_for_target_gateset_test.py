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

from typing import TYPE_CHECKING

import pytest

import qubitron
from qubitron.transformers.optimize_for_target_gateset import _decompose_operations_to_target_gateset

if TYPE_CHECKING:
    from qubitron.protocols.decompose_protocol import DecomposeResult


def test_decompose_operations_raises_on_stuck():
    c_orig = qubitron.Circuit(qubitron.X(qubitron.NamedQubit("q")).with_tags("ignore"))
    gateset = qubitron.Gateset(qubitron.Y)
    with pytest.raises(ValueError, match="Unable to convert"):
        _ = _decompose_operations_to_target_gateset(c_orig, gateset=gateset, ignore_failures=False)

    # Gates marked with a no-compile tag are completely ignored.
    c_new = _decompose_operations_to_target_gateset(
        c_orig,
        context=qubitron.TransformerContext(tags_to_ignore=("ignore",)),
        gateset=gateset,
        ignore_failures=False,
    )
    qubitron.testing.assert_same_circuits(c_orig, c_new)


# pylint: disable=line-too-long
def test_decompose_operations_to_target_gateset_default():
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.T(q[0]),
        qubitron.SWAP(*q),
        qubitron.T(q[0]),
        qubitron.SWAP(*q).with_tags("ignore"),
        qubitron.measure(q[0], key="m"),
        qubitron.X(q[1]).with_classical_controls("m"),
        qubitron.Moment(qubitron.T.on_each(*q)),
        qubitron.SWAP(*q),
        qubitron.T.on_each(*q),
    )
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───T───×───T───×[ignore]───M───────T───×───T───
          │       │           ║           │
1: ───────×───────×───────────╫───X───T───×───T───
                              ║   ║
m: ═══════════════════════════@═══^═══════════════''',
    )
    context = qubitron.TransformerContext(tags_to_ignore=("ignore",))
    c_new = _decompose_operations_to_target_gateset(c_orig, context=context)
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───T────────────@───Y^-0.5───@───Y^0.5────@───────────T───×[ignore]───M───────T────────────@───Y^-0.5───@───Y^0.5────@───────────T───
                   │            │            │               │           ║                    │            │            │
1: ───────Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───────×───────────╫───X───T───Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───T───
                                                                         ║   ║
m: ══════════════════════════════════════════════════════════════════════@═══^══════════════════════════════════════════════════════════
''',
    )


def test_decompose_operations_to_target_gateset():
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.T(q[0]),
        qubitron.SWAP(*q),
        qubitron.T(q[0]),
        qubitron.SWAP(*q).with_tags("ignore"),
        qubitron.measure(q[0], key="m"),
        qubitron.X(q[1]).with_classical_controls("m"),
        qubitron.Moment(qubitron.T.on_each(*q)),
        qubitron.SWAP(*q),
        qubitron.T.on_each(*q),
    )
    gateset = qubitron.Gateset(qubitron.H, qubitron.CNOT)
    decomposer = lambda op, _: (
        qubitron.H(op.qubits[0])
        if qubitron.has_unitary(op) and qubitron.num_qubits(op) == 1
        else NotImplemented
    )
    context = qubitron.TransformerContext(tags_to_ignore=("ignore",))
    c_new = _decompose_operations_to_target_gateset(
        c_orig, gateset=gateset, decomposer=decomposer, context=context
    )
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───H───@───X───@───H───×[ignore]───M───────H───@───X───@───H───
          │   │   │       │           ║           │   │   │
1: ───────X───@───X───────×───────────╫───X───H───X───@───X───H───
                                      ║   ║
m: ═══════════════════════════════════@═══^═══════════════════════''',
    )

    with pytest.raises(ValueError, match="Unable to convert"):
        _ = _decompose_operations_to_target_gateset(
            c_orig, gateset=gateset, decomposer=decomposer, context=context, ignore_failures=False
        )


class MatrixGateTargetGateset(qubitron.CompilationTargetGateset):
    def __init__(self):
        super().__init__(qubitron.MatrixGate)

    @property
    def num_qubits(self) -> int:
        return 2

    def decompose_to_target_gateset(self, op: qubitron.Operation, _) -> DecomposeResult:
        if qubitron.num_qubits(op) != 2 or not qubitron.has_unitary(op):
            return NotImplemented
        return qubitron.MatrixGate(qubitron.unitary(op), name="M").on(*op.qubits)


def test_optimize_for_target_gateset_default():
    q = qubitron.LineQubit.range(2)
    c_orig = qubitron.Circuit(
        qubitron.T(q[0]), qubitron.SWAP(*q), qubitron.T(q[0]), qubitron.SWAP(*q).with_tags("ignore")
    )
    context = qubitron.TransformerContext(tags_to_ignore=("ignore",))
    c_new = qubitron.optimize_for_target_gateset(c_orig, context=context)
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
0: ───T────────────@───Y^-0.5───@───Y^0.5────@───────────T───×[ignore]───
                   │            │            │               │
1: ───────Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───────×───────────
''',
    )
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)


def test_optimize_for_target_gateset():
    q = qubitron.LineQubit.range(4)
    c_orig = qubitron.Circuit(
        qubitron.QuantumFourierTransformGate(4).on(*q),
        qubitron.Y(q[0]).with_tags("ignore"),
        qubitron.Y(q[1]).with_tags("ignore"),
        qubitron.CNOT(*q[2:]).with_tags("ignore"),
        qubitron.measure(*q[:2], key="m"),
        qubitron.CZ(*q[2:]).with_classical_controls("m"),
        qubitron.inverse(qubitron.QuantumFourierTransformGate(4).on(*q)),
    )

    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
0: ───qft───Y[ignore]───M───────qft^-1───
      │                 ║       │
1: ───#2────Y[ignore]───M───────#2───────
      │                 ║       │
2: ───#3────@[ignore]───╫───@───#3───────
      │     │           ║   ║   │
3: ───#4────X───────────╫───@───#4───────
                        ║   ║
m: ═════════════════════@═══^════════════
''',
    )
    gateset = MatrixGateTargetGateset()
    context = qubitron.TransformerContext(tags_to_ignore=("ignore",))
    c_new = qubitron.optimize_for_target_gateset(c_orig, gateset=gateset, context=context)
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
                                         ┌────────┐                       ┌────────┐                 ┌────────┐
0: ───M[1]──────────M[1]──────────────────────M[1]────Y[ignore]───M────────────M[1]───────────────────M[1]────────M[1]───M[1]───
      │             │                         │                   ║            │                      │           │      │
1: ───M[2]───M[1]───┼─────────────M[1]────M[1]┼───────Y[ignore]───M────────M[1]┼──────────────M[1]────┼───M[1]────┼──────M[2]───
             │      │             │       │   │                   ║        │   │              │       │   │       │
2: ──────────M[2]───M[2]───M[1]───┼───────M[2]┼───────@[ignore]───╫───@────M[2]┼───────M[1]───┼───────┼───M[2]────M[2]──────────
                           │      │           │       │           ║   ║        │       │      │       │
3: ────────────────────────M[2]───M[2]────────M[2]────X───────────╫───@────────M[2]────M[2]───M[2]────M[2]──────────────────────
                                                                  ║   ║
m: ═══════════════════════════════════════════════════════════════@═══^═════════════════════════════════════════════════════════
                                         └────────┘                       └────────┘                 └────────┘
       ''',
    )

    with pytest.raises(ValueError, match="Unable to convert"):
        # Raises an error due to CCO and Measurement gate, which are not part of the gateset.
        _ = qubitron.optimize_for_target_gateset(
            c_orig, gateset=gateset, context=context, ignore_failures=False
        )


def test_optimize_for_target_gateset_deep():
    q0, q1 = qubitron.LineQubit.range(2)
    c_nested = qubitron.FrozenCircuit(qubitron.CX(q0, q1))
    c_orig = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.H(q0), qubitron.CircuitOperation(c_nested).repeat(3))
        ).repeat(5)
    )
    c_expected = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(
                qubitron.single_qubit_matrix_to_phxz(qubitron.unitary(qubitron.H(q0))).on(q0),
                qubitron.CircuitOperation(
                    qubitron.FrozenCircuit(
                        qubitron.MatrixGate(c_nested.unitary(qubit_order=[q0, q1]), name="M").on(q0, q1)
                    )
                ).repeat(3),
            )
        ).repeat(5)
    )
    gateset = MatrixGateTargetGateset()
    context = qubitron.TransformerContext(deep=True)
    c_new = qubitron.optimize_for_target_gateset(c_orig, gateset=gateset, context=context)
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_new, c_expected)
    qubitron.testing.assert_has_diagram(
        c_orig,
        '''
      [           [ 0: ───@─── ]             ]
      [ 0: ───H───[       │    ]──────────── ]
0: ───[           [ 1: ───X─── ](loops=3)    ]────────────
      [           │                          ]
      [ 1: ───────#2──────────────────────── ](loops=5)
      │
1: ───#2──────────────────────────────────────────────────
''',
    )
    qubitron.testing.assert_has_diagram(
        c_new,
        '''
      [                                 [ 0: ───M[1]─── ]             ]
      [ 0: ───PhXZ(a=-0.5,x=0.5,z=-1)───[       │       ]──────────── ]
0: ───[                                 [ 1: ───M[2]─── ](loops=3)    ]────────────
      [                                 │                             ]
      [ 1: ─────────────────────────────#2─────────────────────────── ](loops=5)
      │
1: ───#2───────────────────────────────────────────────────────────────────────────
''',
    )


@pytest.mark.parametrize('max_num_passes', [2, None])
def test_optimize_for_target_gateset_multiple_passes(max_num_passes: int | None):
    gateset = qubitron.CZTargetGateset()

    input_circuit = qubitron.Circuit(
        [
            qubitron.Moment(
                qubitron.X(qubitron.LineQubit(1)),
                qubitron.X(qubitron.LineQubit(2)),
                qubitron.X(qubitron.LineQubit(3)),
                qubitron.X(qubitron.LineQubit(6)),
            ),
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(0)),
                qubitron.H(qubitron.LineQubit(1)),
                qubitron.H(qubitron.LineQubit(2)),
                qubitron.H(qubitron.LineQubit(3)),
                qubitron.H(qubitron.LineQubit(4)),
                qubitron.H(qubitron.LineQubit(5)),
                qubitron.H(qubitron.LineQubit(6)),
            ),
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(1)), qubitron.H(qubitron.LineQubit(3)), qubitron.H(qubitron.LineQubit(5))
            ),
            qubitron.Moment(
                qubitron.CZ(qubitron.LineQubit(0), qubitron.LineQubit(1)),
                qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(3)),
                qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(5)),
            ),
            qubitron.Moment(
                qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(1)),
                qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(3)),
                qubitron.CZ(qubitron.LineQubit(6), qubitron.LineQubit(5)),
            ),
        ]
    )
    desired_circuit = qubitron.Circuit.from_moments(
        qubitron.Moment(
            qubitron.PhasedXZGate(axis_phase_exponent=0.5, x_exponent=-0.5, z_exponent=1.0).on(
                qubitron.LineQubit(4)
            )
        ),
        qubitron.Moment(qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(5))),
        qubitron.Moment(
            qubitron.PhasedXZGate(axis_phase_exponent=-1.0, x_exponent=1, z_exponent=0).on(
                qubitron.LineQubit(1)
            ),
            qubitron.PhasedXZGate(axis_phase_exponent=0.5, x_exponent=-0.5, z_exponent=1.0).on(
                qubitron.LineQubit(0)
            ),
            qubitron.PhasedXZGate(axis_phase_exponent=-1.0, x_exponent=1, z_exponent=0).on(
                qubitron.LineQubit(3)
            ),
            qubitron.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0.5, z_exponent=0.0).on(
                qubitron.LineQubit(2)
            ),
        ),
        qubitron.Moment(
            qubitron.CZ(qubitron.LineQubit(0), qubitron.LineQubit(1)),
            qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(3)),
        ),
        qubitron.Moment(
            qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(1)),
            qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(3)),
        ),
        qubitron.Moment(
            qubitron.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0.5, z_exponent=0.0).on(
                qubitron.LineQubit(6)
            )
        ),
        qubitron.Moment(qubitron.CZ(qubitron.LineQubit(6), qubitron.LineQubit(5))),
    )
    got = qubitron.optimize_for_target_gateset(
        input_circuit, gateset=gateset, max_num_passes=max_num_passes
    )
    qubitron.testing.assert_same_circuits(got, desired_circuit)


@pytest.mark.parametrize('max_num_passes', [2, None])
def test_optimize_for_target_gateset_multiple_passes_dont_preserve_moment_structure(
    max_num_passes: int | None,
):
    gateset = qubitron.CZTargetGateset(preserve_moment_structure=False)

    input_circuit = qubitron.Circuit(
        [
            qubitron.Moment(
                qubitron.X(qubitron.LineQubit(1)),
                qubitron.X(qubitron.LineQubit(2)),
                qubitron.X(qubitron.LineQubit(3)),
                qubitron.X(qubitron.LineQubit(6)),
            ),
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(0)),
                qubitron.H(qubitron.LineQubit(1)),
                qubitron.H(qubitron.LineQubit(2)),
                qubitron.H(qubitron.LineQubit(3)),
                qubitron.H(qubitron.LineQubit(4)),
                qubitron.H(qubitron.LineQubit(5)),
                qubitron.H(qubitron.LineQubit(6)),
            ),
            qubitron.Moment(
                qubitron.H(qubitron.LineQubit(1)), qubitron.H(qubitron.LineQubit(3)), qubitron.H(qubitron.LineQubit(5))
            ),
            qubitron.Moment(
                qubitron.CZ(qubitron.LineQubit(0), qubitron.LineQubit(1)),
                qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(3)),
                qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(5)),
            ),
            qubitron.Moment(
                qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(1)),
                qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(3)),
                qubitron.CZ(qubitron.LineQubit(6), qubitron.LineQubit(5)),
            ),
        ]
    )
    desired_circuit = qubitron.Circuit(
        qubitron.PhasedXZGate(axis_phase_exponent=0.5, x_exponent=-0.5, z_exponent=1.0).on(
            qubitron.LineQubit(4)
        ),
        qubitron.PhasedXZGate(axis_phase_exponent=-1.0, x_exponent=1, z_exponent=0).on(
            qubitron.LineQubit(1)
        ),
        qubitron.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0.5, z_exponent=0.0).on(
            qubitron.LineQubit(2)
        ),
        qubitron.PhasedXZGate(axis_phase_exponent=0.5, x_exponent=-0.5, z_exponent=1.0).on(
            qubitron.LineQubit(0)
        ),
        qubitron.PhasedXZGate(axis_phase_exponent=-1.0, x_exponent=1, z_exponent=0).on(
            qubitron.LineQubit(3)
        ),
        qubitron.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0.5, z_exponent=0.0).on(
            qubitron.LineQubit(6)
        ),
        qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(5)),
        qubitron.CZ(qubitron.LineQubit(0), qubitron.LineQubit(1)),
        qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(3)),
        qubitron.CZ(qubitron.LineQubit(2), qubitron.LineQubit(1)),
        qubitron.CZ(qubitron.LineQubit(4), qubitron.LineQubit(3)),
        qubitron.CZ(qubitron.LineQubit(6), qubitron.LineQubit(5)),
    )
    got = qubitron.optimize_for_target_gateset(
        input_circuit, gateset=gateset, max_num_passes=max_num_passes
    )
    qubitron.testing.assert_same_circuits(got, desired_circuit)
