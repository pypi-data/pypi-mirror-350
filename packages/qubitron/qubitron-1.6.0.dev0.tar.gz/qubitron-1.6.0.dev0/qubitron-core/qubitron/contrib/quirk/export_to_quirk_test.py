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

import pytest
import sympy

import qubitron
from qubitron.contrib.quirk.export_to_quirk import circuit_to_quirk_url


def assert_links_to(circuit: qubitron.Circuit, expected: str, **kwargs):
    actual = circuit_to_quirk_url(circuit, **kwargs)
    actual = actual.replace('\n', '').replace(' ', '').strip()
    expected = expected.replace('],[', '],\n[').strip()
    expected = expected.replace('\n', '').replace(' ', '')
    assert actual == expected


def test_x_z_same_col():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.X(a), qubitron.Z(b))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["X","Z"]]}
    """,
        escape_url=False,
    )
    assert_links_to(
        circuit,
        'http://algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22X%22%2C%22Z%22%5D%5D%7D',
    )


def test_x_cnot_split_cols():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    circuit = qubitron.Circuit(qubitron.CNOT(a, b), qubitron.X(c))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","X"],[1,1,"X"]]}
    """,
        escape_url=False,
    )


def test_cz_cnot_split_cols():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    circuit = qubitron.Circuit(qubitron.CNOT(a, b), qubitron.CZ(b, c))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","X"],[1,"•","Z"]]}
    """,
        escape_url=False,
    )


def test_various_known_gate_types():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(
        qubitron.X(a),
        qubitron.X(a) ** 0.25,
        qubitron.X(a) ** -0.5,
        qubitron.Z(a),
        qubitron.Z(a) ** 0.5,
        qubitron.Y(a),
        qubitron.Y(a) ** -0.25,
        qubitron.Y(a) ** sympy.Symbol('t'),
        qubitron.H(a),
        qubitron.measure(a),
        qubitron.measure(a, b, key='not-relevant'),
        qubitron.SWAP(a, b),
        qubitron.CNOT(a, b),
        qubitron.CNOT(b, a),
        qubitron.CZ(a, b),
    )
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["X"],
            ["X^¼"],
            ["X^-½"],
            ["Z"],
            ["Z^½"],
            ["Y"],
            ["Y^-¼"],
            ["Y^t"],
            ["H"],
            ["Measure"],
            ["Measure","Measure"],
            ["Swap","Swap"],
            ["•","X"],
            ["X","•"],
            ["•","Z"]]}
    """,
        escape_url=False,
    )


def test_parameterized_gates():
    a = qubitron.LineQubit(0)
    s = sympy.Symbol('s')
    t = sympy.Symbol('t')

    assert_links_to(
        qubitron.Circuit(qubitron.X(a) ** t),
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["X^t"]
        ]}
    """,
        escape_url=False,
    )

    assert_links_to(
        qubitron.Circuit(qubitron.Y(a) ** t),
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["Y^t"]
        ]}
    """,
        escape_url=False,
    )

    assert_links_to(
        qubitron.Circuit(qubitron.Z(a) ** t),
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["Z^t"]
        ]}
    """,
        escape_url=False,
    )

    assert_links_to(
        qubitron.Circuit(qubitron.Z(a) ** (2 * t)),
        """
        http://algassert.com/quirk#circuit={"cols":[
            [{"arg":"2*t","id":"Z^ft"}]
        ]}
    """,
        escape_url=False,
    )

    with pytest.raises(ValueError, match='Symbol other than "t"'):
        _ = circuit_to_quirk_url(qubitron.Circuit(qubitron.X(a) ** s))


class MysteryOperation(qubitron.Operation):
    def __init__(self, *qubits):
        self._qubits = qubits

    @property
    def qubits(self):
        return self._qubits

    def with_qubits(self, *new_qubits):
        return MysteryOperation(*new_qubits)


class MysteryGate(qubitron.testing.SingleQubitGate):
    def _has_mixture_(self):
        return True


def test_various_unknown_gate_types():
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(
        MysteryOperation(b),
        qubitron.SWAP(a, b) ** 0.5,
        qubitron.H(a) ** 0.5,
        qubitron.SingleQubitCliffordGate.X_sqrt.merged_with(qubitron.SingleQubitCliffordGate.Z_sqrt).on(a),
        qubitron.X(a) ** (1 / 5),
        qubitron.Y(a) ** (1 / 5),
        qubitron.Z(a) ** (1 / 5),
        qubitron.CZ(a, b) ** (1 / 5),
        qubitron.PhasedXPowGate(phase_exponent=0.25)(a),
        qubitron.PhasedXPowGate(exponent=1, phase_exponent=sympy.Symbol('r'))(a),
        qubitron.PhasedXPowGate(exponent=0.001, phase_exponent=0.1)(a),
    )
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            [1,"UNKNOWN"],
            ["UNKNOWN", "UNKNOWN"],
            [{"id":"?","matrix":"{{0.853553+0.146447i,0.353553-0.353553i},
                                  {0.353553-0.353553i,0.146447+0.853553i}}"}],
            [{"id":"?","matrix":"{{0.5+0.5i,0.5+0.5i},{0.5-0.5i,-0.5+0.5i}}"}],
            [{"arg":"0.2000","id":"X^ft"}],
            [{"arg":"0.2000","id":"Y^ft"}],
            [{"arg":"0.2000","id":"Z^ft"}],
            ["•",{"arg":"0.2000","id":"Z^ft"}],
            [{"id":"?",
              "matrix":"{{0, 0.707107+0.707107i},
                         {0.707107-0.707107i, 0}}"}],
            ["UNKNOWN"],
            [{"id":"?",
              "matrix":"{{0.999998+0.001571i,0.000488-0.001493i},
                         {-0.000483-0.001495i,0.999998+0.001571i}}"}]
        ]}
    """,
        escape_url=False,
        prefer_unknown_gate_to_failure=True,
    )


def test_formulaic_exponent_export():
    a = qubitron.LineQubit(0)
    t = sympy.Symbol('t')
    assert_links_to(
        qubitron.Circuit(qubitron.X(a) ** t, qubitron.Y(a) ** -t, qubitron.Z(a) ** (t * 2 + 1)),
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["X^t"],
            ["Y^-t"],
            [{"arg":"2*t+1","id":"Z^ft"}]
        ]}
    """,
        escape_url=False,
    )


def test_formulaic_rotation_xyz_export():
    a = qubitron.LineQubit(0)
    t = sympy.Symbol('t')
    assert_links_to(
        qubitron.Circuit(
            qubitron.rx(sympy.pi / 2).on(a), qubitron.ry(sympy.pi * t).on(a), qubitron.rz(-sympy.pi * t).on(a)
        ),
        """
        http://algassert.com/quirk#circuit={"cols":[
            [{"arg":"(1/2)pi","id":"Rxft"}],
            [{"arg":"(t)pi","id":"Ryft"}],
            [{"arg":"(-t)pi","id":"Rzft"}]
        ]}
    """,
        escape_url=False,
    )

    with pytest.raises(ValueError, match='unsupported'):
        _ = circuit_to_quirk_url(qubitron.Circuit(qubitron.rx(sympy.FallingFactorial(t, t)).on(a)))


def test_unrecognized_single_qubit_gate_with_matrix():
    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(qubitron.PhasedXPowGate(phase_exponent=0).on(a) ** 0.2731)
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[[{
            "id":"?",
            "matrix":"{
                {0.826988+0.378258i, 0.173012-0.378258i},
                {0.173012-0.378258i, 0.826988+0.378258i}
            }"}]]}
    """,
        escape_url=False,
    )


def test_unknown_gate():
    class UnknownGate(qubitron.testing.SingleQubitGate):
        pass

    a = qubitron.NamedQubit('a')
    circuit = qubitron.Circuit(UnknownGate()(a))
    with pytest.raises(TypeError):
        _ = circuit_to_quirk_url(circuit)
    with pytest.raises(TypeError):
        _ = circuit_to_quirk_url(circuit, escape_url=False)
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["UNKNOWN"]]}
    """,
        prefer_unknown_gate_to_failure=True,
        escape_url=False,
    )


def test_controlled_gate():
    a, b, c, d = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(qubitron.ControlledGate(qubitron.ControlledGate(qubitron.CZ)).on(a, d, c, b))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","Z","•", "•"]]}
    """,
        escape_url=False,
    )

    # Doesn't merge.
    circuit = qubitron.Circuit(
        qubitron.ControlledGate(qubitron.X).on(a, b), qubitron.ControlledGate(qubitron.Z).on(c, d)
    )
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","X"],[1,1,"•", "Z"]]}
    """,
        escape_url=False,
    )

    # Unknown sub-gate.
    circuit = qubitron.Circuit(qubitron.ControlledGate(MysteryGate()).on(a, b))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["UNKNOWN","UNKNOWN"]]}
    """,
        escape_url=False,
        prefer_unknown_gate_to_failure=True,
    )


def test_toffoli():
    a, b, c, d = qubitron.LineQubit.range(4)

    # Raw.
    circuit = qubitron.Circuit(qubitron.TOFFOLI(a, b, c))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","•","X"]]}
    """,
        escape_url=False,
    )

    # With exponent. Doesn't merge with other operation.
    circuit = qubitron.Circuit(qubitron.CCX(a, b, c) ** 0.5, qubitron.H(d))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["•","•","X^½"],[1,1,1,"H"]]}
    """,
        escape_url=False,
    )

    # Unknown exponent.
    circuit = qubitron.Circuit(qubitron.CCX(a, b, c) ** 0.01)
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["UNKNOWN","UNKNOWN","UNKNOWN"]
        ]}
    """,
        escape_url=False,
        prefer_unknown_gate_to_failure=True,
    )


def test_fredkin():
    a, b, c = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.FREDKIN(a, b, c))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","Swap","Swap"]]}
    """,
        escape_url=False,
    )

    # Doesn't merge.
    x, y, z = qubitron.LineQubit.range(3, 6)
    circuit = qubitron.Circuit(qubitron.CSWAP(a, b, c), qubitron.CSWAP(x, y, z))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["•","Swap","Swap"],
            [1,1,1,"•","Swap","Swap"]
        ]}
    """,
        escape_url=False,
    )


def test_ccz():
    a, b, c, d = qubitron.LineQubit.range(4)

    # Raw.
    circuit = qubitron.Circuit(qubitron.CCZ(a, b, c))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","•","Z"]]}
    """,
        escape_url=False,
    )

    # Symbolic exponent.
    circuit = qubitron.Circuit(qubitron.CCZ(a, b, c) ** sympy.Symbol('t'))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[["•","•","Z^t"]]}
    """,
        escape_url=False,
    )

    # Unknown exponent.
    circuit = qubitron.Circuit(qubitron.CCZ(a, b, c) ** 0.01)
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["UNKNOWN","UNKNOWN","UNKNOWN"]
        ]}
    """,
        escape_url=False,
        prefer_unknown_gate_to_failure=True,
    )

    # With exponent. Doesn't merge with other operation.
    circuit = qubitron.Circuit(qubitron.CCZ(a, b, c) ** 0.5, qubitron.H(d))
    assert_links_to(
        circuit,
        """
        http://algassert.com/quirk#circuit={"cols":[
            ["•","•","Z^½"],[1,1,1,"H"]]}
    """,
        escape_url=False,
    )
