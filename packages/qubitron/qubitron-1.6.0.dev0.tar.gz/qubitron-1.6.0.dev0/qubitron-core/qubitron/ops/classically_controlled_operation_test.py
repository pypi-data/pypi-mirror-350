# Copyright 2021 The Qubitron Developers
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
from sympy.parsing import sympy_parser

import qubitron

ALL_SIMULATORS = (qubitron.Simulator(), qubitron.DensityMatrixSimulator(), qubitron.CliffordSimulator())


def test_diagram():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('a'))

    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───────
      ║
1: ───╫───X───
      ║   ║
a: ═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_pauli():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure_single_paulistring(qubitron.X(q0), key='a'),
        qubitron.X(q1).with_classical_controls('a'),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M(X)───────
      ║
1: ───╫──────X───
      ║      ║
a: ═══@══════^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_measurements():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q0, key='b'),
        qubitron.X(q1).with_classical_controls('a'),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───M('b')───
      ║
1: ───╫───X────────
      ║   ║
a: ═══@═══^════════
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_controlled_bits():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.measure(q0, key='a'), qubitron.CX(q0, q1).with_classical_controls('a'))

    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───@───
      ║   ║
1: ───╫───X───
      ║   ║
a: ═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_control_bits():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q0, key='b'),
        qubitron.X(q1).with_classical_controls('a', 'b'),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───M───────
      ║   ║
1: ───╫───╫───X───
      ║   ║   ║
a: ═══@═══╬═══^═══
          ║   ║
b: ═══════@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_multiple_ops_single_moment():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q1, key='b'),
        qubitron.X(q0).with_classical_controls('a'),
        qubitron.X(q1).with_classical_controls('b'),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
      ┌──┐   ┌──┐
0: ────M──────X─────
       ║      ║
1: ────╫M─────╫X────
       ║║     ║║
a: ════@╬═════^╬════
        ║      ║
b: ═════@══════^════
      └──┘   └──┘
""",
        use_unicode_characters=True,
    )


def test_diagram_subcircuit():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('a'))
        )
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
      [ 0: ───M─────── ]
      [       ║        ]
0: ───[ 1: ───╫───X─── ]───
      [       ║   ║    ]
      [ a: ═══@═══^═══ ]
      │
1: ───#2───────────────────
""",
        use_unicode_characters=True,
    )


def test_diagram_subcircuit_layered():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.CircuitOperation(
            qubitron.FrozenCircuit(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('a'))
        ),
        qubitron.X(q1).with_classical_controls('a'),
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
          [ 0: ───M─────── ]
          [       ║        ]
0: ───M───[ 1: ───╫───X─── ]───────
      ║   [       ║   ║    ]
      ║   [ a: ═══@═══^═══ ]
      ║   ║
1: ───╫───#2───────────────────X───
      ║   ║                    ║
a: ═══@═══╩════════════════════^═══
""",
        use_unicode_characters=True,
    )


def test_qasm_sympy_condition():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls(sympy.Eq(sympy.Symbol('a'), 0)),
    )
    qasm = qubitron.qasm(circuit)
    assert (
        qasm
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];
creg m_a[1];


measure q[0] -> m_a[0];
if (m_a==0) x q[1];
"""
    )


def test_qasm_key_condition():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('a'))
    qasm = qubitron.qasm(circuit)
    assert (
        qasm
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];
creg m_a[1];


measure q[0] -> m_a[0];
if (m_a==1) x q[1];
"""
    )


def test_qasm_no_conditions():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'), qubitron.ClassicallyControlledOperation(qubitron.X(q1), [])
    )
    qasm = qubitron.qasm(circuit)
    assert (
        qasm
        == f"""// Generated from Qubitron v{qubitron.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];
creg m_a[1];


measure q[0] -> m_a[0];
x q[1];
"""
    )


def test_qasm_multiple_conditions():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.measure(q0, key='b'),
        qubitron.X(q1).with_classical_controls(
            sympy.Eq(sympy.Symbol('a'), 0), sympy.Eq(sympy.Symbol('b'), 0)
        ),
    )
    with pytest.raises(ValueError, match='QASM does not support multiple conditions'):
        _ = qubitron.qasm(circuit)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_key_unset(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    result = sim.run(circuit)
    assert result.measurements['a'] == 0
    assert result.measurements['b'] == 0


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_key_set(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls('a'),
        qubitron.measure(q1, key='b'),
    )
    result = sim.run(circuit)
    assert result.measurements['a'] == 1
    assert result.measurements['b'] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeated_measurement_unset(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls(qubitron.KeyCondition(qubitron.MeasurementKey('a'), index=-2)),
        qubitron.measure(q1, key='b'),
        qubitron.X(q1).with_classical_controls(qubitron.KeyCondition(qubitron.MeasurementKey('a'), index=-1)),
        qubitron.measure(q1, key='c'),
    )
    result = sim.run(circuit)
    assert result.records['a'][0][0][0] == 0
    assert result.records['a'][0][1][0] == 1
    assert result.records['b'][0][0][0] == 0
    assert result.records['c'][0][0][0] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeated_measurement_set(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),
        qubitron.X(q1).with_classical_controls(qubitron.KeyCondition(qubitron.MeasurementKey('a'), index=-2)),
        qubitron.measure(q1, key='b'),
        qubitron.X(q1).with_classical_controls(qubitron.KeyCondition(qubitron.MeasurementKey('a'), index=-1)),
        qubitron.measure(q1, key='c'),
    )
    result = sim.run(circuit)
    assert result.records['a'][0][0][0] == 1
    assert result.records['a'][0][1][0] == 0
    assert result.records['b'][0][0][0] == 1
    assert result.records['c'][0][0][0] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_subcircuit_key_unset(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    inner = qubitron.Circuit(
        qubitron.measure(q0, key='c'),
        qubitron.X(q1).with_classical_controls('c'),
        qubitron.measure(q1, key='b'),
    )
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            inner.freeze(), repetitions=2, use_repetition_ids=True, measurement_key_map={'c': 'a'}
        )
    )
    result = sim.run(circuit)
    assert result.measurements['0:a'] == 0
    assert result.measurements['0:b'] == 0
    assert result.measurements['1:a'] == 0
    assert result.measurements['1:b'] == 0


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_subcircuit_key_set(sim):
    q0, q1 = qubitron.LineQubit.range(2)
    inner = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.measure(q0, key='c'),
        qubitron.X(q1).with_classical_controls('c'),
        qubitron.measure(q1, key='b'),
    )
    circuit = qubitron.Circuit(
        qubitron.CircuitOperation(
            inner.freeze(), repetitions=4, use_repetition_ids=True, measurement_key_map={'c': 'a'}
        )
    )
    result = sim.run(circuit)
    assert result.measurements['0:a'] == 1
    assert result.measurements['0:b'] == 1
    assert result.measurements['1:a'] == 0
    assert result.measurements['1:b'] == 1
    assert result.measurements['2:a'] == 1
    assert result.measurements['2:b'] == 0
    assert result.measurements['3:a'] == 0
    assert result.measurements['3:b'] == 0


def test_key_unset_in_subcircuit_outer_scope():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='a'),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.X(q1).with_classical_controls('a'))),
    )
    circuit.append(qubitron.measure(q1, key='b'))
    result = qubitron.Simulator().run(circuit)
    assert result.measurements['a'] == 0
    assert result.measurements['b'] == 0


def test_key_set_in_subcircuit_outer_scope():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.X(q0),
        qubitron.measure(q0, key='a'),
        qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.X(q1).with_classical_controls('a'))),
    )
    circuit.append(qubitron.measure(q1, key='b'))
    result = qubitron.Simulator().run(circuit)
    assert result.measurements['a'] == 1
    assert result.measurements['b'] == 1


def test_condition_types():
    q0 = qubitron.LineQubit(0)
    sympy_cond = sympy_parser.parse_expr('a >= 2')
    op = qubitron.X(q0).with_classical_controls(qubitron.MeasurementKey('a'), 'b', 'a > b', sympy_cond)
    assert set(map(str, op.classical_controls)) == {'a', 'b', 'a > b', 'a >= 2'}


def test_condition_flattening():
    q0 = qubitron.LineQubit(0)
    op = qubitron.X(q0).with_classical_controls('a').with_classical_controls('b')
    assert set(map(str, op.classical_controls)) == {'a', 'b'}
    assert isinstance(op._sub_operation, qubitron.GateOperation)


def test_condition_stacking():
    q0 = qubitron.LineQubit(0)
    op = qubitron.X(q0).with_classical_controls('a').with_tags('t').with_classical_controls('b')
    assert set(map(str, qubitron.control_keys(op))) == {'a', 'b'}
    assert set(map(str, op.classical_controls)) == {'a', 'b'}
    assert not op.tags


def test_condition_removal():
    q0 = qubitron.LineQubit(0)
    op = (
        qubitron.X(q0)
        .with_tags('t1')
        .with_classical_controls('a')
        .with_tags('t2')
        .with_classical_controls('b')
    )
    op = op.without_classical_controls()
    assert not qubitron.control_keys(op)
    assert not op.classical_controls
    assert not op.tags


def test_qubit_mapping():
    q0, q1 = qubitron.LineQubit.range(2)
    op = qubitron.X(q0).with_classical_controls('a')
    assert op.with_qubits(q1).qubits == (q1,)


def test_parameterizable():
    s = sympy.Symbol('s')
    q0 = qubitron.LineQubit(0)
    op = qubitron.X(q0).with_classical_controls('a')
    opa = qubitron.XPowGate(exponent=s).on(q0).with_classical_controls('a')
    assert qubitron.is_parameterized(opa)
    assert not qubitron.is_parameterized(op)
    assert qubitron.resolve_parameters(opa, qubitron.ParamResolver({'s': 1})) == op


def test_decompose():
    q0 = qubitron.LineQubit(0)
    op = qubitron.H(q0).with_classical_controls('a')
    assert qubitron.decompose(op) == [
        (qubitron.Y(q0) ** 0.5).with_classical_controls('a'),
        qubitron.XPowGate(exponent=1.0, global_shift=-0.25).on(q0).with_classical_controls('a'),
    ]


def test_str():
    q0 = qubitron.LineQubit(0)
    op = qubitron.X(q0).with_classical_controls('a')
    assert str(op) == 'X(q(0)).with_classical_controls(a)'


def test_scope_local():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('a'))
    middle = qubitron.Circuit(
        qubitron.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=True)
    )
    outer_subcircuit = qubitron.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=True
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['0:0:a', '0:1:a', '1:0:a', '1:1:a']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    # pylint: disable=line-too-long
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]                                      ]
0: ───[ 0: ───[       ║   ║    ]───────────────────────────────────── ]─────────────────────────────────────
      [       [ a: ═══@═══^═══ ](loops=2, use_repetition_ids=True)    ](loops=2, use_repetition_ids=True)
""",
        use_unicode_characters=True,
    )
    # pylint: enable=line-too-long
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───────M───X───M───X───M───X───M───X───
          ║   ║   ║   ║   ║   ║   ║   ║
0:0:a: ═══@═══^═══╬═══╬═══╬═══╬═══╬═══╬═══
                  ║   ║   ║   ║   ║   ║
0:1:a: ═══════════@═══^═══╬═══╬═══╬═══╬═══
                          ║   ║   ║   ║
1:0:a: ═══════════════════@═══^═══╬═══╬═══
                                  ║   ║
1:1:a: ═══════════════════════════@═══^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))


def test_scope_flatten_both():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('a'))
    middle = qubitron.Circuit(
        qubitron.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=False)
    )
    outer_subcircuit = qubitron.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=False
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['a', 'a', 'a', 'a']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]             ]
0: ───[ 0: ───[       ║   ║    ]──────────── ]────────────
      [       [ a: ═══@═══^═══ ](loops=2)    ](loops=2)
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───X───M───X───M───X───M───X───
      ║   ║   ║   ║   ║   ║   ║   ║
a: ═══@═══^═══@═══^═══@═══^═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_flatten_inner():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('a'))
    middle = qubitron.Circuit(qubitron.CircuitOperation(inner.freeze(), repetitions=2))
    outer_subcircuit = qubitron.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=True
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['0:a', '0:a', '1:a', '1:a']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]             ]
0: ───[ 0: ───[       ║   ║    ]──────────── ]─────────────────────────────────────
      [       [ a: ═══@═══^═══ ](loops=2)    ](loops=2, use_repetition_ids=True)
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───X───M───X───M───X───M───X───
        ║   ║   ║   ║   ║   ║   ║   ║
0:a: ═══@═══^═══@═══^═══╬═══╬═══╬═══╬═══
                        ║   ║   ║   ║
1:a: ═══════════════════@═══^═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_flatten_outer():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('a'))
    middle = qubitron.Circuit(
        qubitron.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=True)
    )
    outer_subcircuit = qubitron.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['0:a', '1:a', '0:a', '1:a']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]                                      ]
0: ───[ 0: ───[       ║   ║    ]───────────────────────────────────── ]────────────
      [       [ a: ═══@═══^═══ ](loops=2, use_repetition_ids=True)    ](loops=2)
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───X───M───X───M───X───M───X───
        ║   ║   ║   ║   ║   ║   ║   ║
0:a: ═══@═══^═══╬═══╬═══@═══^═══╬═══╬═══
                ║   ║           ║   ║
1:a: ═══════════@═══^═══════════@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_extern():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('b'))
    middle = qubitron.Circuit(
        qubitron.measure(q, key=qubitron.MeasurementKey('b')),
        qubitron.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=True),
    )
    outer_subcircuit = qubitron.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=True
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['0:b', '0:b', '1:b', '1:b']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    # pylint: disable=line-too-long
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [           [ 0: ───M('a')───X─── ]                                      ]
      [ 0: ───M───[                ║    ]───────────────────────────────────── ]
0: ───[       ║   [ b: ════════════^═══ ](loops=2, use_repetition_ids=True)    ]─────────────────────────────────────
      [       ║   ║                                                            ]
      [ b: ═══@═══╩═══════════════════════════════════════════════════════════ ](loops=2, use_repetition_ids=True)
""",
        use_unicode_characters=True,
    )
    # pylint: enable=line-too-long
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───M('0:0:a')───X───M('0:1:a')───X───M───M('1:0:a')───X───M('1:1:a')───X───
        ║                ║                ║   ║                ║                ║
0:b: ═══@════════════════^════════════════^═══╬════════════════╬════════════════╬═══
                                              ║                ║                ║
1:b: ═════════════════════════════════════════@════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))


def test_scope_extern_wrapping_with_non_repeating_subcircuits():
    def wrap(*ops):
        return qubitron.CircuitOperation(qubitron.FrozenCircuit(*ops))

    def wrap_frozen(*ops):
        return qubitron.FrozenCircuit(wrap(*ops))

    q = qubitron.LineQubit(0)
    inner = wrap_frozen(
        wrap(qubitron.measure(q, key='a')), wrap(qubitron.X(q).with_classical_controls('b'))
    )
    middle = wrap_frozen(
        wrap(qubitron.measure(q, key=qubitron.MeasurementKey('b'))),
        wrap(qubitron.CircuitOperation(inner, repetitions=2, use_repetition_ids=True)),
    )
    outer_subcircuit = qubitron.CircuitOperation(middle, repetitions=2, use_repetition_ids=True)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['0:b', '0:b', '1:b', '1:b']
    assert not qubitron.control_keys(outer_subcircuit)
    assert not qubitron.control_keys(circuit)
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───M('0:0:a')───X───M('0:1:a')───X───M───M('1:0:a')───X───M('1:1:a')───X───
        ║                ║                ║   ║                ║                ║
0:b: ═══@════════════════^════════════════^═══╬════════════════╬════════════════╬═══
                                              ║                ║                ║
1:b: ═════════════════════════════════════════@════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))


def test_scope_root():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('b'))
    middle = qubitron.Circuit(
        qubitron.measure(q, key=qubitron.MeasurementKey('c')),
        qubitron.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = qubitron.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['b', 'b', 'b', 'b']
    assert qubitron.control_keys(outer_subcircuit) == {qubitron.MeasurementKey('b')}
    assert qubitron.control_keys(circuit) == {qubitron.MeasurementKey('b')}
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [                [ 0: ───M('a')───X─── ]             ]
      [ 0: ───M('c')───[                ║    ]──────────── ]
0: ───[                [ b: ════════════^═══ ](loops=2)    ]────────────
      [                ║                                   ]
      [ b: ════════════╩══════════════════════════════════ ](loops=2)
      ║
b: ═══╩═════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M('c')───M('a')───X───M('a')───X───M('c')───M('a')───X───M('a')───X───
                        ║            ║                     ║            ║
b: ═════════════════════^════════════^═════════════════════^════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))


def test_scope_extern_mismatch():
    q = qubitron.LineQubit(0)
    inner = qubitron.Circuit(qubitron.measure(q, key='a'), qubitron.X(q).with_classical_controls('b'))
    middle = qubitron.Circuit(
        qubitron.measure(q, key=qubitron.MeasurementKey('b', ('0',))),
        qubitron.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=True),
    )
    outer_subcircuit = qubitron.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=True
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in qubitron.control_keys(op)
    ]
    assert internal_control_keys == ['b', 'b', 'b', 'b']
    assert qubitron.control_keys(outer_subcircuit) == {qubitron.MeasurementKey('b')}
    assert qubitron.control_keys(circuit) == {qubitron.MeasurementKey('b')}
    # pylint: disable=line-too-long
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [                  [ 0: ───M('a')───X─── ]                                      ]
      [ 0: ───M('0:b')───[                ║    ]───────────────────────────────────── ]
0: ───[                  [ b: ════════════^═══ ](loops=2, use_repetition_ids=True)    ]─────────────────────────────────────
      [                  ║                                                            ]
      [ b: ══════════════╩═══════════════════════════════════════════════════════════ ](loops=2, use_repetition_ids=True)
      ║
b: ═══╩═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    # pylint: enable=line-too-long
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M('0:0:b')───M('0:0:a')───X───M('0:1:a')───X───M('1:0:b')───M('1:0:a')───X───M('1:1:a')───X───
                                ║                ║                             ║                ║
b: ═════════════════════════════^════════════════^═════════════════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))


def test_repr():
    q0 = qubitron.LineQubit(0)
    op = qubitron.X(q0).with_classical_controls('a')
    assert repr(op) == (
        "qubitron.ClassicallyControlledOperation("
        "qubitron.X(qubitron.LineQubit(0)), [qubitron.KeyCondition(qubitron.MeasurementKey(name='a'))]"
        ")"
    )


def test_no_measurement_gates():
    q0 = qubitron.LineQubit(0)
    with pytest.raises(ValueError, match='with measurements'):
        _ = qubitron.measure(q0).with_classical_controls('a')


def test_unmeasured_condition():
    q0 = qubitron.LineQubit(0)
    bad_circuit = qubitron.Circuit(qubitron.X(q0).with_classical_controls('a'))
    with pytest.raises(
        ValueError, match='Measurement key a missing when testing classical control'
    ):
        _ = qubitron.Simulator().simulate(bad_circuit)


def test_layered_circuit_operations_with_controls_in_between():
    q = qubitron.LineQubit(0)
    outer_subcircuit = qubitron.CircuitOperation(
        qubitron.Circuit(
            qubitron.CircuitOperation(qubitron.FrozenCircuit(qubitron.X(q), qubitron.Y(q))).with_classical_controls(
                'm'
            )
        ).freeze()
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [ 0: ───[ 0: ───X───Y─── ].with_classical_controls(m)─── ]
0: ───[       ║                                                ]───
      [ m: ═══╩═══════════════════════════════════════════════ ]
      ║
m: ═══╩════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───[ 0: ───X───Y─── ].with_classical_controls(m)───
      ║
m: ═══╩═══════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(qubitron.decompose(outer_subcircuit)),
        """
0: ───X───Y───
      ║   ║
m: ═══^═══^═══
""",
        use_unicode_characters=True,
    )


def test_sympy():
    q0, q1, q2, q3, q_result = qubitron.LineQubit.range(5)
    for i in range(4):
        for j in range(4):
            # Put first two qubits into a state representing bitstring(i), next two qubits into a
            # state representing bitstring(j) and measure those into m_i and m_j respectively. Then
            # add a conditional X(q_result) based on m_i > m_j and measure that.
            bitstring_i = qubitron.big_endian_int_to_bits(i, bit_count=2)
            bitstring_j = qubitron.big_endian_int_to_bits(j, bit_count=2)
            circuit = qubitron.Circuit(
                qubitron.X(q0) ** bitstring_i[0],
                qubitron.X(q1) ** bitstring_i[1],
                qubitron.X(q2) ** bitstring_j[0],
                qubitron.X(q3) ** bitstring_j[1],
                qubitron.measure(q0, q1, key='m_i'),
                qubitron.measure(q2, q3, key='m_j'),
                qubitron.X(q_result).with_classical_controls(sympy_parser.parse_expr('m_j > m_i')),
                qubitron.measure(q_result, key='m_result'),
            )

            # m_result should now be set iff j > i.
            result = qubitron.Simulator().run(circuit)
            assert result.measurements['m_result'][0][0] == (j > i)


def test_sympy_qudits():
    q0 = qubitron.LineQid(0, 3)
    q1 = qubitron.LineQid(1, 5)
    q_result = qubitron.LineQubit(2)

    class PlusGate(qubitron.Gate):
        def __init__(self, dimension, increment=1):
            self.dimension = dimension
            self.increment = increment % dimension

        def _qid_shape_(self):
            return (self.dimension,)

        def _unitary_(self):
            inc = (self.increment - 1) % self.dimension + 1
            u = np.empty((self.dimension, self.dimension))
            u[inc:] = np.eye(self.dimension)[:-inc]
            u[:inc] = np.eye(self.dimension)[-inc:]
            return u

    for i in range(15):
        digits = qubitron.big_endian_int_to_digits(i, digit_count=2, base=(3, 5))
        circuit = qubitron.Circuit(
            PlusGate(3, digits[0]).on(q0),
            PlusGate(5, digits[1]).on(q1),
            qubitron.measure(q0, q1, key='m'),
            qubitron.X(q_result).with_classical_controls(sympy_parser.parse_expr('m % 4 <= 1')),
            qubitron.measure(q_result, key='m_result'),
        )

        result = qubitron.Simulator().run(circuit)
        assert result.measurements['m_result'][0][0] == (i % 4 <= 1)


def test_sympy_path_prefix():
    q = qubitron.LineQubit(0)
    op = qubitron.X(q).with_classical_controls(sympy.Symbol('b'))
    prefixed = qubitron.with_key_path_prefix(op, ('0',))
    assert qubitron.control_keys(prefixed) == {'0:b'}


def test_sympy_scope():
    q = qubitron.LineQubit(0)
    a, b, c, d = sympy.symbols('a b c d')
    inner = qubitron.Circuit(
        qubitron.measure(q, key='a'),
        qubitron.X(q).with_classical_controls(a & b).with_classical_controls(c | d),
    )
    middle = qubitron.Circuit(
        qubitron.measure(q, key='b'),
        qubitron.measure(q, key=qubitron.MeasurementKey('c', ('0',))),
        qubitron.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = qubitron.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_controls = [str(k) for op in circuit.all_operations() for k in qubitron.control_keys(op)]
    assert set(internal_controls) == {'a', 'b', 'c', 'd'}
    assert qubitron.control_keys(outer_subcircuit) == {'c', 'd'}
    assert qubitron.control_keys(circuit) == {'c', 'd'}
    assert circuit == qubitron.Circuit(qubitron.decompose(outer_subcircuit))
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(outer_subcircuit),
        """
      [                      [ 0: ───M───X(conditions=[c | d, a & b])─── ]             ]
      [                      [       ║   ║                               ]             ]
      [                      [ a: ═══@═══^══════════════════════════════ ]             ]
      [                      [           ║                               ]             ]
      [ 0: ───M───M('0:c')───[ b: ═══════^══════════════════════════════ ]──────────── ]
      [       ║              [           ║                               ]             ]
      [       ║              [ c: ═══════^══════════════════════════════ ]             ]
0: ───[       ║              [           ║                               ]             ]────────────
      [       ║              [ d: ═══════^══════════════════════════════ ](loops=2)    ]
      [       ║              ║                                                         ]
      [ b: ═══@══════════════╬════════════════════════════════════════════════════════ ]
      [                      ║                                                         ]
      [ c: ══════════════════╬════════════════════════════════════════════════════════ ]
      [                      ║                                                         ]
      [ d: ══════════════════╩════════════════════════════════════════════════════════ ](loops=2)
      ║
c: ═══╬═════════════════════════════════════════════════════════════════════════════════════════════
      ║
d: ═══╩═════════════════════════════════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )

    # pylint: disable=line-too-long
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───M('0:c')───M───X(conditions=[c | d, a & b])───M───X(conditions=[c | d, a & b])───M───M('0:c')───M───X(conditions=[c | d, a & b])───M───X(conditions=[c | d, a & b])───
      ║              ║   ║                              ║   ║                              ║              ║   ║                              ║   ║
a: ═══╬══════════════@═══^══════════════════════════════@═══^══════════════════════════════╬══════════════@═══^══════════════════════════════@═══^══════════════════════════════
      ║                  ║                                  ║                              ║                  ║                                  ║
b: ═══@══════════════════^══════════════════════════════════^══════════════════════════════@══════════════════^══════════════════════════════════^══════════════════════════════
                         ║                                  ║                                                 ║                                  ║
c: ══════════════════════^══════════════════════════════════^═════════════════════════════════════════════════^══════════════════════════════════^══════════════════════════════
                         ║                                  ║                                                 ║                                  ║
d: ══════════════════════^══════════════════════════════════^═════════════════════════════════════════════════^══════════════════════════════════^══════════════════════════════
""",
        use_unicode_characters=True,
    )
    # pylint: enable=line-too-long


def test_sympy_scope_simulation():
    q0, q1, q2, q3, q_ignored, q_result = qubitron.LineQubit.range(6)
    condition = sympy_parser.parse_expr('a & b | c & d')
    # We set up condition (a & b | c & d) plus an ignored measurement key, and run through the
    # combinations of possible values of those (by doing X(q_i)**bits[i] on each), then verify
    # that the final measurement into m_result is True iff that condition was met.
    for i in range(32):
        bits = qubitron.big_endian_int_to_bits(i, bit_count=5)
        inner = qubitron.Circuit(
            qubitron.X(q0) ** bits[0],
            qubitron.measure(q0, key='a'),
            qubitron.X(q_result).with_classical_controls(condition),
            qubitron.measure(q_result, key='m_result'),
        )
        middle = qubitron.Circuit(
            qubitron.X(q1) ** bits[1],
            qubitron.measure(q1, key='b'),
            qubitron.X(q_ignored) ** bits[4],
            qubitron.measure(q_ignored, key=qubitron.MeasurementKey('c', ('0',))),
            qubitron.CircuitOperation(inner.freeze(), repetition_ids=['0']),
        )
        circuit = qubitron.Circuit(
            qubitron.X(q2) ** bits[2],
            qubitron.measure(q2, key='c'),
            qubitron.X(q3) ** bits[3],
            qubitron.measure(q3, key='d'),
            qubitron.CircuitOperation(middle.freeze(), repetition_ids=['0']),
        )
        result = qubitron.CliffordSimulator().run(circuit)
        assert result.measurements['0:0:m_result'][0][0] == (
            bits[0] and bits[1] or bits[2] and bits[3]  # bits[4] irrelevant
        )


def test_commutes():
    q0, q1 = qubitron.LineQubit.range(2)
    assert qubitron.commutes(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('b'))
    assert qubitron.commutes(qubitron.X(q1).with_classical_controls('b'), qubitron.measure(q0, key='a'))
    assert qubitron.commutes(
        qubitron.X(q0).with_classical_controls('a'), qubitron.H(q1).with_classical_controls('a')
    )
    assert qubitron.commutes(
        qubitron.X(q0).with_classical_controls('a'), qubitron.X(q0).with_classical_controls('a')
    )
    assert not qubitron.commutes(qubitron.measure(q0, key='a'), qubitron.X(q1).with_classical_controls('a'))
    assert not qubitron.commutes(qubitron.X(q1).with_classical_controls('a'), qubitron.measure(q0, key='a'))
    assert not qubitron.commutes(
        qubitron.X(q0).with_classical_controls('a'), qubitron.H(q0).with_classical_controls('a')
    )


def test_moment_diagram():
    a, _, c, d = qubitron.GridQubit.rect(2, 2)
    m = qubitron.Moment(qubitron.CZ(a, d), qubitron.X(c).with_classical_controls('m'))
    assert (
        str(m).strip()
        == """
  ╷ 0                 1
╶─┼─────────────────────
0 │ @─────────────────┐
  │                   │
1 │ X(conditions=[m]) @
  │
    """.strip()
    )


def test_diagram_exponents():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='m'), (qubitron.X(q1) ** 0.5).with_classical_controls('m')
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───────────
      ║
1: ───╫───X^0.5───
      ║   ║
m: ═══@═══^═══════
""",
    )


def test_diagram_exponents_cx():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='m'), (qubitron.CX(q2, q1) ** 0.5).with_classical_controls('m')
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M───────────
      ║
1: ───╫───X^0.5───
      ║   ║
2: ───╫───@───────
      ║   ║
m: ═══@═══^═══════
""",
    )


def test_diagram_exponents_multiple_keys():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        qubitron.measure(q0, key='m0'),
        qubitron.measure(q1, key='m1'),
        (qubitron.X(q2) ** 0.5).with_classical_controls('m0', 'm1'),
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
       ┌──┐
0: ─────M─────────────
        ║
1: ─────╫M────────────
        ║║
2: ─────╫╫────X^0.5───
        ║║    ║
m0: ════@╬════^═══════
         ║    ║
m1: ═════@════^═══════
       └──┘
""",
    )


def test_sympy_indexed_condition_circuit():
    a = sympy.IndexedBase('a')
    # XOR the 2nd and 3rd bits of the measurement (big-endian)
    cond = qubitron.SympyCondition(sympy.Xor(a[1], a[2]))
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    sim = qubitron.Simulator()
    circuit = qubitron.Circuit(
        qubitron.measure(q0, q1, q2, key='a'),
        qubitron.X(q3).with_classical_controls(cond),
        qubitron.measure(q3, key='b'),
    )
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───M──────────────────────────────────────────
      ║
1: ───M──────────────────────────────────────────
      ║
2: ───M──────────────────────────────────────────
      ║
3: ───╫───X(conditions=[a[1] ^ a[2]])───M('b')───
      ║   ║
a: ═══@═══^══════════════════════════════════════
""",
    )
    result = sim.sample(circuit)
    assert result['a'][0] == 0b000
    assert result['b'][0] == 0
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b001
    assert result['b'][0] == 1
    circuit.insert(0, qubitron.X(q1))
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b010
    assert result['b'][0] == 1
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b011
    assert result['b'][0] == 0
    circuit.insert(0, qubitron.X(q0))
    circuit.insert(0, qubitron.X(q1))
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b100
    assert result['b'][0] == 0
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b101
    assert result['b'][0] == 1
    circuit.insert(0, qubitron.X(q1))
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b110
    assert result['b'][0] == 1
    circuit.insert(0, qubitron.X(q2))
    result = sim.sample(circuit)
    assert result['a'][0] == 0b111
    assert result['b'][0] == 0
