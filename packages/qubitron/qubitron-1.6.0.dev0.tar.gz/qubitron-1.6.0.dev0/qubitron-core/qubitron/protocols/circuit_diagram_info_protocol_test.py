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


def test_circuit_diagram_info_value_wrapping() -> None:
    single_info = qubitron.CircuitDiagramInfo(('Single',))

    class ReturnInfo:
        def _circuit_diagram_info_(self, args):
            return single_info

    class ReturnTuple:
        def _circuit_diagram_info_(self, args):
            return ('Single',)

    class ReturnList:
        def _circuit_diagram_info_(self, args):
            return ('Single' for _ in range(1))

    class ReturnGenerator:
        def _circuit_diagram_info_(self, args):
            return ['Single']

    class ReturnString:
        def _circuit_diagram_info_(self, args):
            return 'Single'

    assert (
        qubitron.circuit_diagram_info(ReturnInfo())
        == qubitron.circuit_diagram_info(ReturnTuple())
        == qubitron.circuit_diagram_info(ReturnString())
        == qubitron.circuit_diagram_info(ReturnList())
        == qubitron.circuit_diagram_info(ReturnGenerator())
        == single_info
    )

    double_info = qubitron.CircuitDiagramInfo(('Single', 'Double'))

    class ReturnDoubleInfo:
        def _circuit_diagram_info_(self, args):
            return double_info

    class ReturnDoubleTuple:
        def _circuit_diagram_info_(self, args):
            return 'Single', 'Double'

    assert (
        qubitron.circuit_diagram_info(ReturnDoubleInfo())
        == qubitron.circuit_diagram_info(ReturnDoubleTuple())
        == double_info
    )


def test_circuit_diagram_info_init() -> None:
    assert qubitron.CircuitDiagramInfo(['a', 'b']).wire_symbols == ('a', 'b')


def test_circuit_diagram_info_validate() -> None:
    with pytest.raises(ValueError):
        _ = qubitron.CircuitDiagramInfo('X')


def test_circuit_diagram_info_repr() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.CircuitDiagramInfo(('X', 'Y'), 2))


def test_circuit_diagram_info_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(lambda: qubitron.CircuitDiagramInfo(('X',)))
    eq.add_equality_group(
        qubitron.CircuitDiagramInfo(('X', 'Y')), qubitron.CircuitDiagramInfo(('X', 'Y'), 1)
    )
    eq.add_equality_group(qubitron.CircuitDiagramInfo(('Z',), 2))
    eq.add_equality_group(qubitron.CircuitDiagramInfo(('Z', 'Z'), 2))
    eq.add_equality_group(qubitron.CircuitDiagramInfo(('Z',), 3))
    eq.add_equality_group(qubitron.CircuitDiagramInfo(('Z',), 3, auto_exponent_parens=False))


def test_circuit_diagram_info_pass_fail() -> None:
    class C:
        pass

    class D:
        def _circuit_diagram_info_(self, args):
            return NotImplemented

    class E:
        def _circuit_diagram_info_(self, args):
            return qubitron.CircuitDiagramInfo(('X',))

    assert qubitron.circuit_diagram_info(C(), default=None) is None
    assert qubitron.circuit_diagram_info(D(), default=None) is None
    assert qubitron.circuit_diagram_info(E(), default=None) == qubitron.CircuitDiagramInfo(('X',))

    with pytest.raises(TypeError, match='no _circuit_diagram_info'):
        _ = qubitron.circuit_diagram_info(C())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = qubitron.circuit_diagram_info(D())
    assert qubitron.circuit_diagram_info(E()) == qubitron.CircuitDiagramInfo(('X',))


def test_controlled_1x1_matrixgate_diagram_error() -> None:
    q = qubitron.LineQubit(0)
    g = qubitron.MatrixGate(np.array([[1j]])).controlled()
    c = qubitron.Circuit(g(q))
    assert str(c) == "0: ───C[[0.+1.j]]───"


def test_circuit_diagram_info_args_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT)
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=None,
            known_qubit_count=None,
            use_unicode_characters=False,
            precision=None,
            label_map=None,
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=None,
            known_qubit_count=None,
            use_unicode_characters=True,
            precision=None,
            label_map=None,
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(3),
            known_qubit_count=3,
            use_unicode_characters=False,
            precision=None,
            label_map=None,
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=False,
            precision=None,
            label_map=None,
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=False,
            precision=None,
            label_map=None,
            include_tags=False,
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=False,
            precision=None,
            label_map={qubitron.LineQubit(0): 5, qubitron.LineQubit(1): 7},
        )
    )
    eq.add_equality_group(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=False,
            precision=None,
            label_map={qubitron.LineQubit(0): 5, qubitron.LineQubit(1): 7},
            transpose=True,
        )
    )


def test_circuit_diagram_info_args_repr() -> None:
    qubitron.testing.assert_equivalent_repr(
        qubitron.CircuitDiagramInfoArgs(
            known_qubits=qubitron.LineQubit.range(2),
            known_qubit_count=2,
            use_unicode_characters=True,
            precision=5,
            label_map={qubitron.LineQubit(0): 5, qubitron.LineQubit(1): 7},
            include_tags=False,
            transpose=True,
        )
    )


def test_format_real() -> None:
    args = qubitron.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT.copy()
    assert args.format_real(1) == '1'
    assert args.format_real(1.1) == '1.1'
    assert args.format_real(1.234567) == '1.23'
    assert args.format_real(1 / 7) == '0.143'
    assert args.format_real(sympy.Symbol('t')) == 't'
    assert args.format_real(sympy.Symbol('t') * 2 + 1) == '2*t + 1'

    assert args.format_real(np.float64(1.1)) == '1.1'
    assert args.format_real(np.int32(1)) == '1'

    args.precision = None
    assert args.format_real(1) == '1'
    assert args.format_real(1.1) == '1.1'
    assert args.format_real(1.234567) == '1.234567'
    assert args.format_real(1 / 7) == repr(1 / 7)
    assert args.format_real(sympy.Symbol('t')) == 't'
    assert args.format_real(sympy.Symbol('t') * 2 + 1) == '2*t + 1'


def test_format_complex() -> None:
    args = qubitron.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT.copy()
    assert args.format_complex(1) == '1+0i'
    assert args.format_complex(1.1) == '1.1+0i'
    assert args.format_complex(1.1 + 1j) == '1.1+i'
    assert args.format_complex(1.1 - 1j) == '1.1-i'
    assert args.format_complex(1.1 - 2j) == '1.1-2i'
    assert args.format_complex(-2.2j) == '0-2.2i'
    assert args.format_complex(1.234567) == '1.23+0i'
    assert args.format_complex(1 / 7) == '0.143+0i'
    assert args.format_complex(sympy.Symbol('t')) == 't'
    assert args.format_complex(sympy.Symbol('t') * 2 + 1) == '2*t + 1'

    args.precision = None
    assert args.format_complex(1) == '1+0i'
    assert args.format_complex(1.1) == '1.1+0i'
    assert args.format_complex(1.234567) == '1.234567+0i'
    assert args.format_complex(1.234567 + 5.5j) == '1.234567+5.5i'
    assert args.format_complex(1 / 7) == repr(1 / 7) + '+0i'
    assert args.format_complex(sympy.Symbol('t')) == 't'
    assert args.format_complex(sympy.Symbol('t') * 2 + 1) == '2*t + 1'


def test_format_radians_without_precision() -> None:
    args = qubitron.CircuitDiagramInfoArgs(
        known_qubits=None,
        known_qubit_count=None,
        use_unicode_characters=False,
        precision=None,
        label_map=None,
    )
    assert args.format_radians(np.pi) == 'pi'
    assert args.format_radians(-np.pi) == '-pi'
    assert args.format_radians(1.1) == '1.1'
    assert args.format_radians(1.234567) == '1.234567'
    assert args.format_radians(np.float32(1.234567)) == '1.234567'
    assert args.format_radians(1 / 7) == repr(1 / 7)
    assert args.format_radians(sympy.Symbol('t')) == 't'
    assert args.format_radians(sympy.Symbol('t') * 2 + 1) == '2*t + 1'

    args.use_unicode_characters = True
    assert args.format_radians(np.pi) == 'π'
    assert args.format_radians(-np.pi) == '-π'
    assert args.format_radians(1.1) == '1.1'
    assert args.format_radians(1.234567) == '1.234567'
    assert args.format_radians(np.float32(1.234567)) == '1.234567'
    assert args.format_radians(1 / 7) == repr(1 / 7)
    assert args.format_radians(sympy.Symbol('t')) == 't'
    assert args.format_radians(sympy.Symbol('t') * 2 + 1) == '2*t + 1'


def test_format_radians_with_precision() -> None:
    args = qubitron.CircuitDiagramInfoArgs(
        known_qubits=None,
        known_qubit_count=None,
        use_unicode_characters=False,
        precision=3,
        label_map=None,
    )
    assert args.format_radians(np.pi) == 'pi'
    assert args.format_radians(-np.pi) == '-pi'
    assert args.format_radians(np.pi / 2) == '0.5pi'
    assert args.format_radians(-3 * np.pi / 4) == '-0.75pi'
    assert args.format_radians(1.1) == '0.35pi'
    assert args.format_radians(1.234567) == '0.393pi'
    assert args.format_radians(sympy.Symbol('t')) == 't'
    assert args.format_radians(sympy.Symbol('t') * 2 + 1) == '2*t + 1'

    args.use_unicode_characters = True
    assert args.format_radians(np.pi) == 'π'
    assert args.format_radians(-np.pi) == '-π'
    assert args.format_radians(np.pi / 2) == '0.5π'
    assert args.format_radians(-3 * np.pi / 4) == '-0.75π'
    assert args.format_radians(1.1) == '0.35π'
    assert args.format_radians(1.234567) == '0.393π'
    assert args.format_radians(sympy.Symbol('t')) == 't'
    assert args.format_radians(sympy.Symbol('t') * 2 + 1) == '2*t + 1'
