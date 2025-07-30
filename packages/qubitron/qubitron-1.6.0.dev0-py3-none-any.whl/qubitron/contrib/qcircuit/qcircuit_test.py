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

import qubitron
import qubitron.contrib.qcircuit as ccq
import qubitron.testing as ct


def assert_has_qcircuit_diagram(actual: qubitron.Circuit, desired: str, **kwargs) -> None:
    """Determines if a given circuit has the desired qcircuit diagram.

    Args:
        actual: The circuit that was actually computed by some process.
        desired: The desired qcircuit diagram as a string. Newlines at the
            beginning and whitespace at the end are ignored.
        **kwargs: Keyword arguments to be passed to
            circuit_to_latex_using_qcircuit.
    """
    actual_diagram = ccq.circuit_to_latex_using_qcircuit(actual, **kwargs).lstrip('\n').rstrip()
    desired_diagram = desired.lstrip("\n").rstrip()
    assert actual_diagram == desired_diagram, (
        "Circuit's qcircuit diagram differs from the desired diagram.\n"
        '\n'
        'Diagram of actual circuit:\n'
        f'{actual_diagram}\n'
        '\n'
        'Desired qcircuit diagram:\n'
        f'{desired_diagram}\n'
        '\n'
        'Highlighted differences:\n'
        f'{ct.highlight_text_differences(actual_diagram, desired_diagram)}\n'
    )


def test_fallback_diagram() -> None:
    class MagicGate(qubitron.testing.ThreeQubitGate):
        def __str__(self):
            return 'MagicGate'

    class MagicOp(qubitron.Operation):
        def __init__(self, *qubits):
            self._qubits = qubits

        def with_qubits(self, *new_qubits):
            return MagicOp(*new_qubits)  # pragma: no cover

        @property
        def qubits(self):
            return self._qubits

        def __str__(self):
            return 'MagicOperate'

    circuit = qubitron.Circuit(
        MagicOp(qubitron.NamedQubit('b')),
        MagicGate().on(qubitron.NamedQubit('b'), qubitron.NamedQubit('a'), qubitron.NamedQubit('c')),
    )
    expected_diagram = r"""
\Qcircuit @R=1em @C=0.75em {
 \\
 &\lstick{\text{a}}& \qw&                           \qw&\gate{\text{\#2}}       \qw    &\qw\\
 &\lstick{\text{b}}& \qw&\gate{\text{MagicOperate}} \qw&\gate{\text{MagicGate}} \qw\qwx&\qw\\
 &\lstick{\text{c}}& \qw&                           \qw&\gate{\text{\#3}}       \qw\qwx&\qw\\
 \\
}""".strip()
    assert_has_qcircuit_diagram(circuit, expected_diagram)


def test_teleportation_diagram() -> None:
    ali = qubitron.NamedQubit('alice')
    car = qubitron.NamedQubit('carrier')
    bob = qubitron.NamedQubit('bob')

    circuit = qubitron.Circuit(
        qubitron.H(car),
        qubitron.CNOT(car, bob),
        qubitron.X(ali) ** 0.5,
        qubitron.CNOT(ali, car),
        qubitron.H(ali),
        [qubitron.measure(ali), qubitron.measure(car)],
        qubitron.CNOT(car, bob),
        qubitron.CZ(ali, bob),
    )

    expected_diagram = r"""
\Qcircuit @R=1em @C=0.75em {
 \\
 &\lstick{\text{alice}}&   \qw&\gate{\text{X}^{0.5}} \qw&         \qw    &\control \qw    &\gate{\text{H}} \qw&\meter   \qw    &\control \qw    &\qw\\
 &\lstick{\text{carrier}}& \qw&\gate{\text{H}}       \qw&\control \qw    &\targ    \qw\qwx&\meter          \qw&\control \qw    &         \qw\qwx&\qw\\
 &\lstick{\text{bob}}&     \qw&                      \qw&\targ    \qw\qwx&         \qw    &                \qw&\targ    \qw\qwx&\control \qw\qwx&\qw\\
 \\
}""".strip()
    assert_has_qcircuit_diagram(
        circuit, expected_diagram, qubit_order=qubitron.QubitOrder.explicit([ali, car, bob])
    )


def test_other_diagram() -> None:
    a, b, c = qubitron.LineQubit.range(3)

    circuit = qubitron.Circuit(qubitron.X(a), qubitron.Y(b), qubitron.Z(c))

    expected_diagram = r"""
\Qcircuit @R=1em @C=0.75em {
 \\
 &\lstick{\text{q(0)}}& \qw&\targ           \qw&\qw\\
 &\lstick{\text{q(1)}}& \qw&\gate{\text{Y}} \qw&\qw\\
 &\lstick{\text{q(2)}}& \qw&\gate{\text{Z}} \qw&\qw\\
 \\
}""".strip()
    assert_has_qcircuit_diagram(circuit, expected_diagram)


def test_qcircuit_qubit_namer() -> None:
    from qubitron.contrib.qcircuit import qcircuit_diagram

    assert qcircuit_diagram.qcircuit_qubit_namer(qubitron.NamedQubit('q')) == r'\lstick{\text{q}}&'
    assert qcircuit_diagram.qcircuit_qubit_namer(qubitron.NamedQubit('q_1')) == r'\lstick{\text{q\_1}}&'
    assert (
        qcircuit_diagram.qcircuit_qubit_namer(qubitron.NamedQubit('q^1'))
        == r'\lstick{\text{q\textasciicircum{}1}}&'
    )
    assert (
        qcircuit_diagram.qcircuit_qubit_namer(qubitron.NamedQubit('q_{1}'))
        == r'\lstick{\text{q\_\{1\}}}&'
    )


def test_two_cx_diagram() -> None:
    # test for no moment indication
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(qubitron.CX(q0, q2), qubitron.CX(q1, q3), qubitron.CX(q0, q2), qubitron.CX(q1, q3))
    expected_diagram = r"""
\Qcircuit @R=1em @C=0.75em {
 \\
 &\lstick{\text{q(0)}}& \qw&\control \qw    &         \qw    &\control \qw    &         \qw    &\qw\\
 &\lstick{\text{q(1)}}& \qw&         \qw\qwx&\control \qw    &         \qw\qwx&\control \qw    &\qw\\
 &\lstick{\text{q(2)}}& \qw&\targ    \qw\qwx&         \qw\qwx&\targ    \qw\qwx&         \qw\qwx&\qw\\
 &\lstick{\text{q(3)}}& \qw&         \qw    &\targ    \qw\qwx&         \qw    &\targ    \qw\qwx&\qw\\
 \\
}""".strip()
    assert_has_qcircuit_diagram(circuit, expected_diagram)


def test_sqrt_iswap_diagram() -> None:
    # test for proper rendering of ISWAP^{0.5}
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.ISWAP(q0, q1) ** 0.5)
    expected_diagram = r"""
\Qcircuit @R=1em @C=0.75em {
 \\
 &\lstick{\text{q(0)}}& \qw&\multigate{1}{\text{ISWAP}^{0.5}} \qw&\qw\\
 &\lstick{\text{q(1)}}& \qw&\ghost{\text{ISWAP}^{0.5}}        \qw&\qw\\
 \\
}""".strip()
    assert_has_qcircuit_diagram(circuit, expected_diagram)
