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

import functools
import itertools

import numpy as np
import pytest

import qubitron
from qubitron.protocols.act_on_protocol_test import ExampleSimulationState
from qubitron.testing import assert_allclose_up_to_global_phase, EqualsTester

_bools = (False, True)
_paulis = (qubitron.X, qubitron.Y, qubitron.Z)


def _assert_not_mirror(gate) -> None:
    trans_x = gate.pauli_tuple(qubitron.X)
    trans_y = gate.pauli_tuple(qubitron.Y)
    trans_z = gate.pauli_tuple(qubitron.Z)
    right_handed = (
        trans_x[1] ^ trans_y[1] ^ trans_z[1] ^ (trans_x[0].relative_index(trans_y[0]) != 1)
    )
    assert right_handed, 'Mirrors'


def _assert_no_collision(gate) -> None:
    trans_x = gate.pauli_tuple(qubitron.X)
    trans_y = gate.pauli_tuple(qubitron.Y)
    trans_z = gate.pauli_tuple(qubitron.Z)
    assert trans_x[0] != trans_y[0], 'Collision'
    assert trans_y[0] != trans_z[0], 'Collision'
    assert trans_z[0] != trans_x[0], 'Collision'


def _all_rotations():
    for pauli, flip in itertools.product(_paulis, _bools):
        yield (pauli, flip)


def _all_rotation_pairs():
    for px, flip_x, pz, flip_z in itertools.product(_paulis, _bools, _paulis, _bools):
        if px == pz:
            continue
        yield (px, flip_x), (pz, flip_z)


@functools.lru_cache()
def _all_clifford_gates() -> tuple[qubitron.SingleQubitCliffordGate, ...]:
    return tuple(
        qubitron.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
        for trans_x, trans_z in _all_rotation_pairs()
    )


@pytest.mark.parametrize('pauli,flip_x,flip_z', itertools.product(_paulis, _bools, _bools))
def test_init_value_error(pauli, flip_x, flip_z):
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_xz_map((pauli, flip_x), (pauli, flip_z))


@pytest.mark.parametrize('trans_x,trans_z', _all_rotation_pairs())
def test_init_from_xz(trans_x, trans_z):
    gate = qubitron.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
    assert gate.pauli_tuple(qubitron.X) == trans_x
    assert gate.pauli_tuple(qubitron.Z) == trans_z
    _assert_not_mirror(gate)
    _assert_no_collision(gate)


def test_dense_pauli_string():
    gate = qubitron.SingleQubitCliffordGate.from_xz_map((qubitron.X, True), (qubitron.Y, False))
    assert gate.dense_pauli_string(qubitron.X) == qubitron.DensePauliString('X', coefficient=-1)
    assert gate.dense_pauli_string(qubitron.Z) == qubitron.DensePauliString('Y')


@pytest.mark.parametrize(
    'trans1,trans2,from1',
    (
        (trans1, trans2, from1)
        for trans1, trans2, from1 in itertools.product(_all_rotations(), _all_rotations(), _paulis)
        if trans1[0] != trans2[0]
    ),
)
def test_init_from_double_map_vs_kwargs(trans1, trans2, from1):
    from2 = qubitron.Pauli.by_relative_index(from1, 1)
    from1_str, from2_str = (str(frm).lower() + '_to' for frm in (from1, from2))
    gate_kw = qubitron.SingleQubitCliffordGate.from_double_map(**{from1_str: trans1, from2_str: trans2})
    gate_map = qubitron.SingleQubitCliffordGate.from_double_map({from1: trans1, from2: trans2})
    # Test initializes the same gate
    assert gate_kw == gate_map

    # Test initializes what was expected
    assert gate_map.pauli_tuple(from1) == trans1
    assert gate_map.pauli_tuple(from2) == trans2
    _assert_not_mirror(gate_map)
    _assert_no_collision(gate_map)


@pytest.mark.parametrize(
    'trans1,from1',
    ((trans1, from1) for trans1, from1 in itertools.product(_all_rotations(), _paulis)),
)
def test_init_from_double_invalid(trans1, from1):
    from2 = qubitron.Pauli.by_relative_index(from1, 1)
    # Test throws on invalid arguments
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_double_map({from1: trans1, from2: trans1})


@pytest.mark.parametrize('trans,frm', itertools.product(_all_rotations(), _paulis))
def test_init_from_single_map_vs_kwargs(trans, frm):
    from_str = str(frm).lower() + '_to'
    # pylint: disable=unexpected-keyword-arg
    gate_kw = qubitron.SingleQubitCliffordGate.from_single_map(**{from_str: trans})
    gate_map = qubitron.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate_kw == gate_map


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] != frm
    ),
)
def test_init_90rot_from_single(trans, frm):
    gate = qubitron.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to one gate
    assert len(gate.decompose_rotation()) == 1
    # Check that this is a 90 degree rotation gate
    assert (
        gate.merged_with(gate).merged_with(gate).merged_with(gate) == qubitron.SingleQubitCliffordGate.I
    )
    # Check that flipping the transform produces the inverse rotation
    trans_rev = (trans[0], not trans[1])
    gate_rev = qubitron.SingleQubitCliffordGate.from_single_map({frm: trans_rev})
    assert gate**-1 == gate_rev


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] == frm and trans[1]
    ),
)
def test_init_180rot_from_single(trans, frm):
    gate = qubitron.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to one gate
    assert len(gate.decompose_rotation()) == 1
    # Check that this is a 180 degree rotation gate
    assert gate.merged_with(gate) == qubitron.SingleQubitCliffordGate.I


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] == frm and not trans[1]
    ),
)
def test_init_ident_from_single(trans, frm):
    gate = qubitron.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to zero gates
    assert len(gate.decompose_rotation()) == 0
    # Check that this is an identity gate
    assert gate == qubitron.SingleQubitCliffordGate.I


@pytest.mark.parametrize(
    'pauli,sqrt,expected',
    (
        (qubitron.X, False, qubitron.SingleQubitCliffordGate.X),
        (qubitron.Y, False, qubitron.SingleQubitCliffordGate.Y),
        (qubitron.Z, False, qubitron.SingleQubitCliffordGate.Z),
        (qubitron.X, True, qubitron.SingleQubitCliffordGate.X_sqrt),
        (qubitron.Y, True, qubitron.SingleQubitCliffordGate.Y_sqrt),
        (qubitron.Z, True, qubitron.SingleQubitCliffordGate.Z_sqrt),
    ),
)
def test_init_from_pauli(pauli, sqrt, expected):
    gate = qubitron.SingleQubitCliffordGate.from_pauli(pauli, sqrt=sqrt)
    assert gate == expected


def test_pow():
    assert qubitron.SingleQubitCliffordGate.X**-1 == qubitron.SingleQubitCliffordGate.X
    assert qubitron.SingleQubitCliffordGate.H**-1 == qubitron.SingleQubitCliffordGate.H
    assert qubitron.SingleQubitCliffordGate.X_sqrt == qubitron.SingleQubitCliffordGate.X**0.5
    assert qubitron.SingleQubitCliffordGate.Y_sqrt == qubitron.SingleQubitCliffordGate.Y**0.5
    assert qubitron.SingleQubitCliffordGate.Z_sqrt == qubitron.SingleQubitCliffordGate.Z**0.5
    assert qubitron.SingleQubitCliffordGate.X_nsqrt == qubitron.SingleQubitCliffordGate.X**-0.5
    assert qubitron.SingleQubitCliffordGate.Y_nsqrt == qubitron.SingleQubitCliffordGate.Y**-0.5
    assert qubitron.SingleQubitCliffordGate.Z_nsqrt == qubitron.SingleQubitCliffordGate.Z**-0.5
    assert qubitron.SingleQubitCliffordGate.X_sqrt**-1 == qubitron.SingleQubitCliffordGate.X_nsqrt
    assert qubitron.SingleQubitCliffordGate.X_sqrt**3 == qubitron.SingleQubitCliffordGate.X**1.5
    assert qubitron.SingleQubitCliffordGate.Z**2.0 == qubitron.SingleQubitCliffordGate.I
    assert qubitron.inverse(qubitron.SingleQubitCliffordGate.X_nsqrt) == (
        qubitron.SingleQubitCliffordGate.X_sqrt
    )
    with pytest.raises(TypeError):
        _ = qubitron.SingleQubitCliffordGate.Z**0.25


def test_init_from_quarter_turns():
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 0),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 0),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 0),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 4),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 4),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 4),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 8),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 8),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 8),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, -4),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, -4),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, -4),
    )
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 1),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 5),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 9),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, -3),
    )
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 1),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 5),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, 9),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Y, -3),
    )
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 1),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 5),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, 9),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.Z, -3),
    )
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 2),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 6),
    )
    eq.add_equality_group(
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 3),
        qubitron.SingleQubitCliffordGate.from_quarter_turns(qubitron.X, 7),
    )


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_init_from_quarter_turns_reconstruct(gate):
    new_gate = functools.reduce(
        qubitron.SingleQubitCliffordGate.merged_with,
        (
            qubitron.SingleQubitCliffordGate.from_quarter_turns(pauli, qt)
            for pauli, qt in gate.decompose_rotation()
        ),
        qubitron.SingleQubitCliffordGate.I,
    )
    assert gate == new_gate


def test_init_invalid():
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map()
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map({})
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map(
            {qubitron.X: (qubitron.X, False)}, y_to=(qubitron.Y, False)
        )
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map(
            {qubitron.X: (qubitron.X, False), qubitron.Y: (qubitron.Y, False)}
        )
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_double_map()
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_double_map({})
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_double_map({qubitron.X: (qubitron.X, False)})
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_double_map(x_to=(qubitron.X, False))
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map(
            {qubitron.X: (qubitron.Y, False), qubitron.Y: (qubitron.Z, False), qubitron.Z: (qubitron.X, False)}
        )
    with pytest.raises(ValueError):
        qubitron.SingleQubitCliffordGate.from_single_map(
            {qubitron.X: (qubitron.X, False), qubitron.Y: (qubitron.X, False)}
        )


def test_eq_ne_and_hash():
    eq = EqualsTester()
    for trans_x, trans_z in _all_rotation_pairs():
        gate_gen = lambda: qubitron.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
        eq.make_equality_group(gate_gen)


@pytest.mark.parametrize(
    'gate',
    (
        qubitron.SingleQubitCliffordGate.I,
        qubitron.SingleQubitCliffordGate.H,
        qubitron.SingleQubitCliffordGate.X,
        qubitron.SingleQubitCliffordGate.X_sqrt,
    ),
)
def test_repr_gate(gate):
    qubitron.testing.assert_equivalent_repr(gate)


def test_repr_operation():
    qubitron.testing.assert_equivalent_repr(
        qubitron.SingleQubitCliffordGate.from_pauli(qubitron.Z).on(qubitron.LineQubit(2))
    )


@pytest.mark.parametrize(
    'gate,trans_y',
    (
        (qubitron.SingleQubitCliffordGate.I, (qubitron.Y, False)),
        (qubitron.SingleQubitCliffordGate.H, (qubitron.Y, True)),
        (qubitron.SingleQubitCliffordGate.X, (qubitron.Y, True)),
        (qubitron.SingleQubitCliffordGate.Y, (qubitron.Y, False)),
        (qubitron.SingleQubitCliffordGate.Z, (qubitron.Y, True)),
        (qubitron.SingleQubitCliffordGate.X_sqrt, (qubitron.Z, False)),
        (qubitron.SingleQubitCliffordGate.X_nsqrt, (qubitron.Z, True)),
        (qubitron.SingleQubitCliffordGate.Y_sqrt, (qubitron.Y, False)),
        (qubitron.SingleQubitCliffordGate.Y_nsqrt, (qubitron.Y, False)),
        (qubitron.SingleQubitCliffordGate.Z_sqrt, (qubitron.X, True)),
        (qubitron.SingleQubitCliffordGate.Z_nsqrt, (qubitron.X, False)),
    ),
)
def test_y_rotation(gate, trans_y):
    assert gate.pauli_tuple(qubitron.Y) == trans_y


@pytest.mark.parametrize(
    'gate,gate_equiv',
    (
        (qubitron.SingleQubitCliffordGate.I, qubitron.X**0),
        (qubitron.SingleQubitCliffordGate.H, qubitron.H),
        (qubitron.SingleQubitCliffordGate.X, qubitron.X),
        (qubitron.SingleQubitCliffordGate.Y, qubitron.Y),
        (qubitron.SingleQubitCliffordGate.Z, qubitron.Z),
        (qubitron.SingleQubitCliffordGate.X_sqrt, qubitron.X**0.5),
        (qubitron.SingleQubitCliffordGate.X_nsqrt, qubitron.X**-0.5),
        (qubitron.SingleQubitCliffordGate.Y_sqrt, qubitron.Y**0.5),
        (qubitron.SingleQubitCliffordGate.Y_nsqrt, qubitron.Y**-0.5),
        (qubitron.SingleQubitCliffordGate.Z_sqrt, qubitron.Z**0.5),
        (qubitron.SingleQubitCliffordGate.Z_nsqrt, qubitron.Z**-0.5),
    ),
)
def test_decompose(gate, gate_equiv):
    q0 = qubitron.NamedQubit('q0')
    mat = qubitron.Circuit(gate(q0)).unitary()
    mat_check = qubitron.Circuit(gate_equiv(q0)).unitary()
    assert_allclose_up_to_global_phase(mat, mat_check, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize(
    'gate,gate_equiv',
    (
        (qubitron.SingleQubitCliffordGate.I, qubitron.X**0),
        (qubitron.SingleQubitCliffordGate.H, qubitron.H),
        (qubitron.SingleQubitCliffordGate.X, qubitron.X),
        (qubitron.SingleQubitCliffordGate.Y, qubitron.Y),
        (qubitron.SingleQubitCliffordGate.Z, qubitron.Z),
        (qubitron.SingleQubitCliffordGate.X_sqrt, qubitron.X**0.5),
        (qubitron.SingleQubitCliffordGate.X_nsqrt, qubitron.X**-0.5),
        (qubitron.SingleQubitCliffordGate.Y_sqrt, qubitron.Y**0.5),
        (qubitron.SingleQubitCliffordGate.Y_nsqrt, qubitron.Y**-0.5),
        (qubitron.SingleQubitCliffordGate.Z_sqrt, qubitron.Z**0.5),
        (qubitron.SingleQubitCliffordGate.Z_nsqrt, qubitron.Z**-0.5),
    ),
)
def test_known_matrix(gate, gate_equiv):
    assert qubitron.has_unitary(gate)
    mat = qubitron.unitary(gate)
    mat_check = qubitron.unitary(gate_equiv)
    assert_allclose_up_to_global_phase(mat, mat_check, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize(
    'name, expected_cls',
    [
        ('I', qubitron.SingleQubitCliffordGate),
        ('H', qubitron.SingleQubitCliffordGate),
        ('X', qubitron.SingleQubitCliffordGate),
        ('Y', qubitron.SingleQubitCliffordGate),
        ('Z', qubitron.SingleQubitCliffordGate),
        ('S', qubitron.SingleQubitCliffordGate),
        ('X_sqrt', qubitron.SingleQubitCliffordGate),
        ('X_nsqrt', qubitron.SingleQubitCliffordGate),
        ('Y_sqrt', qubitron.SingleQubitCliffordGate),
        ('Y_nsqrt', qubitron.SingleQubitCliffordGate),
        ('Z_sqrt', qubitron.SingleQubitCliffordGate),
        ('Z_nsqrt', qubitron.SingleQubitCliffordGate),
        ('CNOT', qubitron.CliffordGate),
        ('CZ', qubitron.CliffordGate),
        ('SWAP', qubitron.CliffordGate),
    ],
)
def test_common_clifford_types(name: str, expected_cls: type) -> None:
    assert isinstance(getattr(qubitron.CliffordGate, name), expected_cls)
    assert isinstance(getattr(qubitron.SingleQubitCliffordGate, name), expected_cls)


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_inverse(gate):
    assert gate == qubitron.inverse(qubitron.inverse(gate))


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_inverse_matrix(gate):
    q0 = qubitron.NamedQubit('q0')
    mat = qubitron.Circuit(gate(q0)).unitary()
    mat_inv = qubitron.Circuit(qubitron.inverse(gate)(q0)).unitary()
    assert_allclose_up_to_global_phase(mat, mat_inv.T.conj(), rtol=1e-7, atol=1e-7)


def test_commutes_notimplemented_type():
    with pytest.raises(TypeError):
        qubitron.commutes(qubitron.SingleQubitCliffordGate.X, 'X')
    assert qubitron.commutes(qubitron.SingleQubitCliffordGate.X, 'X', default='default') == 'default'

    with pytest.raises(TypeError):
        qubitron.commutes(qubitron.CliffordGate.X, 'X')
    assert qubitron.commutes(qubitron.CliffordGate.X, 'X', default='default') == 'default'


@pytest.mark.parametrize('gate,other', itertools.combinations(_all_clifford_gates(), r=2))
def test_commutes_single_qubit_gate(gate, other):
    q0 = qubitron.NamedQubit('q0')
    gate_op = gate(q0)
    other_op = other(q0)
    mat = qubitron.Circuit(gate_op, other_op).unitary()
    mat_swap = qubitron.Circuit(other_op, gate_op).unitary()
    commutes = qubitron.commutes(gate, other)
    commutes_check = qubitron.allclose_up_to_global_phase(mat, mat_swap)
    assert commutes == commutes_check

    # Test after switching order
    mat_swap = qubitron.Circuit(gate.equivalent_gate_before(other)(q0), gate_op).unitary()
    assert_allclose_up_to_global_phase(mat, mat_swap, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_parses_single_qubit_gate(gate):
    assert gate == qubitron.read_json(json_text=(qubitron.to_json(gate)))


@pytest.mark.parametrize(
    'gate,pauli,half_turns',
    itertools.product(_all_clifford_gates(), _paulis, (1.0, 0.25, 0.5, -0.5)),
)
def test_commutes_pauli(gate, pauli, half_turns):
    pauli_gate = pauli if half_turns == 1 else pauli**half_turns
    q0 = qubitron.NamedQubit('q0')
    mat = qubitron.Circuit(gate(q0), pauli_gate(q0)).unitary()
    mat_swap = qubitron.Circuit(pauli_gate(q0), gate(q0)).unitary()
    commutes = qubitron.commutes(gate, pauli_gate)
    commutes_check = np.allclose(mat, mat_swap)
    assert commutes == commutes_check, f"gate: {gate}, pauli {pauli}"


def test_to_clifford_tableau_util_function():
    tableau = qubitron.ops.clifford_gate._to_clifford_tableau(
        x_to=(qubitron.X, False), z_to=(qubitron.Z, False)
    )
    assert tableau == qubitron.CliffordTableau(num_qubits=1, initial_state=0)

    tableau = qubitron.ops.clifford_gate._to_clifford_tableau(x_to=(qubitron.X, False), z_to=(qubitron.Z, True))
    assert tableau == qubitron.CliffordTableau(num_qubits=1, initial_state=1)

    tableau = qubitron.ops.clifford_gate._to_clifford_tableau(
        rotation_map={qubitron.X: (qubitron.X, False), qubitron.Z: (qubitron.Z, False)}
    )
    assert tableau == qubitron.CliffordTableau(num_qubits=1, initial_state=0)

    tableau = qubitron.ops.clifford_gate._to_clifford_tableau(
        rotation_map={qubitron.X: (qubitron.X, False), qubitron.Z: (qubitron.Z, True)}
    )
    assert tableau == qubitron.CliffordTableau(num_qubits=1, initial_state=1)

    with pytest.raises(ValueError):
        qubitron.ops.clifford_gate._to_clifford_tableau()


@pytest.mark.parametrize(
    'gate,sym,exp',
    (
        (qubitron.SingleQubitCliffordGate.I, 'I', 1),
        (qubitron.SingleQubitCliffordGate.H, 'H', 1),
        (qubitron.SingleQubitCliffordGate.X, 'X', 1),
        (qubitron.SingleQubitCliffordGate.X_sqrt, 'X', 0.5),
        (qubitron.SingleQubitCliffordGate.X_nsqrt, 'X', -0.5),
        (
            qubitron.SingleQubitCliffordGate.from_xz_map((qubitron.Y, False), (qubitron.X, True)),
            '(X^-0.5-Z^0.5)',
            1,
        ),
    ),
)
def test_text_diagram_info(gate, sym, exp):
    assert qubitron.circuit_diagram_info(gate) == qubitron.CircuitDiagramInfo(
        wire_symbols=(sym,), exponent=exp
    )


@pytest.mark.parametrize("clifford_gate", qubitron.SingleQubitCliffordGate.all_single_qubit_cliffords)
def test_from_unitary(clifford_gate):
    u = qubitron.unitary(clifford_gate)
    result_gate = qubitron.SingleQubitCliffordGate.from_unitary(u)
    assert result_gate == clifford_gate

    result_gate2, global_phase = qubitron.SingleQubitCliffordGate.from_unitary_with_global_phase(u)
    assert result_gate2 == result_gate
    assert np.allclose(qubitron.unitary(result_gate2) * global_phase, u)


def test_from_unitary_with_phase_shift():
    u = np.exp(0.42j) * qubitron.unitary(qubitron.SingleQubitCliffordGate.Y_sqrt)
    gate = qubitron.SingleQubitCliffordGate.from_unitary(u)

    assert gate == qubitron.SingleQubitCliffordGate.Y_sqrt

    gate2, global_phase = qubitron.SingleQubitCliffordGate.from_unitary_with_global_phase(u)
    assert gate2 == gate
    assert np.allclose(qubitron.unitary(gate2) * global_phase, u)


def test_from_unitary_not_clifford():
    # Not a single-qubit gate.
    u = qubitron.unitary(qubitron.CNOT)
    assert qubitron.SingleQubitCliffordGate.from_unitary(u) is None
    assert qubitron.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None

    # Not an unitary matrix.
    u = 2 * qubitron.unitary(qubitron.X)
    assert qubitron.SingleQubitCliffordGate.from_unitary(u) is None
    assert qubitron.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None

    # Not a Clifford gate.
    u = qubitron.unitary(qubitron.T)
    assert qubitron.SingleQubitCliffordGate.from_unitary(u) is None
    assert qubitron.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None


@pytest.mark.parametrize("clifford_gate", qubitron.SingleQubitCliffordGate.all_single_qubit_cliffords)
def test_decompose_gate(clifford_gate):
    gates = clifford_gate.decompose_gate()
    u = functools.reduce(np.dot, [np.eye(2), *(qubitron.unitary(gate) for gate in reversed(gates))])
    assert np.allclose(u, qubitron.unitary(clifford_gate))  # No global phase difference.


@pytest.mark.parametrize('trans_x,trans_z', _all_rotation_pairs())
def test_to_phased_xz_gate(trans_x, trans_z):
    gate = qubitron.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
    actual_phased_xz_gate = gate.to_phased_xz_gate()._canonical()
    expect_phased_xz_gates = qubitron.PhasedXZGate.from_matrix(qubitron.unitary(gate))

    assert np.isclose(actual_phased_xz_gate.x_exponent, expect_phased_xz_gates.x_exponent)
    assert np.isclose(actual_phased_xz_gate.z_exponent, expect_phased_xz_gates.z_exponent)
    assert np.isclose(
        actual_phased_xz_gate.axis_phase_exponent, expect_phased_xz_gates.axis_phase_exponent
    )


def test_from_xz_to_clifford_tableau():
    seen_tableau = []
    for trans_x, trans_z in _all_rotation_pairs():
        tableau = qubitron.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z).clifford_tableau
        tableau_number = sum(2**i * t for i, t in enumerate(tableau.matrix().ravel()))
        tableau_number = tableau_number * 4 + 2 * tableau.rs[0] + tableau.rs[1]
        seen_tableau.append(tableau_number)
        # Satisfy the symplectic property
        assert sum(tableau.matrix()[0, :2] * tableau.matrix()[1, 1::-1]) % 2 == 1

    # Should not have any duplication.
    assert len(set(seen_tableau)) == 24


@pytest.mark.parametrize(
    'clifford_gate,standard_gate',
    [
        (qubitron.CliffordGate.I, qubitron.I),
        (qubitron.CliffordGate.X, qubitron.X),
        (qubitron.CliffordGate.Y, qubitron.Y),
        (qubitron.CliffordGate.Z, qubitron.Z),
        (qubitron.CliffordGate.H, qubitron.H),
        (qubitron.CliffordGate.S, qubitron.S),
        (qubitron.CliffordGate.CNOT, qubitron.CNOT),
        (qubitron.CliffordGate.CZ, qubitron.CZ),
        (qubitron.CliffordGate.SWAP, qubitron.SWAP),
    ],
)
def test_common_clifford_gate(clifford_gate, standard_gate):
    # qubitron.unitary is relied on the _decompose_ methods.
    u_c = qubitron.unitary(clifford_gate)
    u_s = qubitron.unitary(standard_gate)
    qubitron.testing.assert_allclose_up_to_global_phase(u_c, u_s, atol=1e-8)


@pytest.mark.parametrize('property_name', ("all_single_qubit_cliffords", "CNOT", "CZ", "SWAP"))
def test_common_clifford_gate_caching(property_name):
    cache_name = f"_{property_name}"
    delattr(qubitron.CliffordGate, cache_name)
    assert not hasattr(qubitron.CliffordGate, cache_name)
    _ = getattr(qubitron.CliffordGate, property_name)
    assert hasattr(qubitron.CliffordGate, cache_name)


def test_multi_qubit_clifford_pow():
    assert qubitron.CliffordGate.X**-1 == qubitron.CliffordGate.X
    assert qubitron.CliffordGate.H**-1 == qubitron.CliffordGate.H
    assert qubitron.CliffordGate.S**2 == qubitron.CliffordGate.Z
    assert qubitron.CliffordGate.S**-1 == qubitron.CliffordGate.S**3
    assert qubitron.CliffordGate.S**-3 == qubitron.CliffordGate.S
    assert qubitron.CliffordGate.CNOT**3 == qubitron.CliffordGate.CNOT
    assert qubitron.CliffordGate.CNOT**-3 == qubitron.CliffordGate.CNOT
    with pytest.raises(TypeError):
        _ = qubitron.CliffordGate.Z**0.25


def test_stabilizer_effec():
    assert qubitron.has_stabilizer_effect(qubitron.CliffordGate.X)
    assert qubitron.has_stabilizer_effect(qubitron.CliffordGate.H)
    assert qubitron.has_stabilizer_effect(qubitron.CliffordGate.S)
    assert qubitron.has_stabilizer_effect(qubitron.CliffordGate.CNOT)
    assert qubitron.has_stabilizer_effect(qubitron.CliffordGate.CZ)
    qubits = qubitron.LineQubit.range(2)
    gate = qubitron.CliffordGate.from_op_list(
        [qubitron.H(qubits[1]), qubitron.CZ(*qubits), qubitron.H(qubits[1])], qubits
    )
    assert qubitron.has_stabilizer_effect(gate)


def test_clifford_gate_from_op_list():
    # Since from_op_list() ==> _act_on_() ==> tableau.then() and then() has already covered
    # lots of random circuit cases, here we just test a few well-known relationships.
    qubit = qubitron.NamedQubit('test')
    gate = qubitron.CliffordGate.from_op_list([qubitron.X(qubit), qubitron.Z(qubit)], [qubit])
    assert gate == qubitron.CliffordGate.Y  # The tableau ignores the global phase

    gate = qubitron.CliffordGate.from_op_list([qubitron.Z(qubit), qubitron.X(qubit)], [qubit])
    assert gate == qubitron.CliffordGate.Y  # The tableau ignores the global phase

    gate = qubitron.CliffordGate.from_op_list([qubitron.X(qubit), qubitron.Y(qubit)], [qubit])
    assert gate == qubitron.CliffordGate.Z  # The tableau ignores the global phase

    gate = qubitron.CliffordGate.from_op_list([qubitron.Z(qubit), qubitron.X(qubit)], [qubit])
    assert gate == qubitron.CliffordGate.Y  # The tableau ignores the global phase

    # Two qubits gates
    qubits = qubitron.LineQubit.range(2)
    gate = qubitron.CliffordGate.from_op_list(
        [qubitron.H(qubits[1]), qubitron.CZ(*qubits), qubitron.H(qubits[1])], qubits
    )
    assert gate == qubitron.CliffordGate.CNOT

    gate = qubitron.CliffordGate.from_op_list(
        [qubitron.H(qubits[1]), qubitron.CNOT(*qubits), qubitron.H(qubits[1])], qubits
    )
    assert gate == qubitron.CliffordGate.CZ

    # Note the order of qubits matters
    gate = qubitron.CliffordGate.from_op_list(
        [qubitron.H(qubits[0]), qubitron.CZ(qubits[1], qubits[0]), qubitron.H(qubits[0])], qubits
    )
    assert gate != qubitron.CliffordGate.CNOT
    # But if we reverse the qubit_order, they will equal again.
    gate = qubitron.CliffordGate.from_op_list(
        [qubitron.H(qubits[0]), qubitron.CZ(qubits[1], qubits[0]), qubitron.H(qubits[0])], qubits[::-1]
    )
    assert gate == qubitron.CliffordGate.CNOT

    with pytest.raises(
        ValueError, match="only be constructed from the operations that has stabilizer effect"
    ):
        qubitron.CliffordGate.from_op_list([qubitron.T(qubit)], [qubit])


def test_clifford_gate_from_tableau():
    t = qubitron.CliffordGate.X.clifford_tableau
    assert qubitron.CliffordGate.from_clifford_tableau(t) == qubitron.CliffordGate.X

    t = qubitron.CliffordGate.H.clifford_tableau
    assert qubitron.CliffordGate.from_clifford_tableau(t) == qubitron.CliffordGate.H

    t = qubitron.CliffordGate.CNOT.clifford_tableau
    assert qubitron.CliffordGate.from_clifford_tableau(t) == qubitron.CliffordGate.CNOT

    with pytest.raises(ValueError, match='Input argument has to be a CliffordTableau instance.'):
        qubitron.SingleQubitCliffordGate.from_clifford_tableau(123)

    with pytest.raises(ValueError, match="The number of qubit of input tableau should be 1"):
        t = qubitron.CliffordTableau(num_qubits=2)
        qubitron.SingleQubitCliffordGate.from_clifford_tableau(t)

    with pytest.raises(ValueError):
        t = qubitron.CliffordTableau(num_qubits=1)
        t.xs = np.array([1, 1]).reshape(2, 1)
        t.zs = np.array([1, 1]).reshape(2, 1)  # This violates the sympletic property.
        qubitron.CliffordGate.from_clifford_tableau(t)

    with pytest.raises(ValueError, match="Input argument has to be a CliffordTableau instance."):
        qubitron.CliffordGate.from_clifford_tableau(1)


def test_multi_clifford_decompose_by_unitary():
    # Construct a random clifford gate:
    n, num_ops = 5, 20  # because we relied on unitary cannot test large-scale qubits
    gate_candidate = [qubitron.X, qubitron.Y, qubitron.Z, qubitron.H, qubitron.S, qubitron.CNOT, qubitron.CZ]
    for _ in range(10):
        qubits = qubitron.LineQubit.range(n)
        ops = []
        for _ in range(num_ops):
            g = np.random.randint(len(gate_candidate))
            indices = (np.random.randint(n),) if g < 5 else np.random.choice(n, 2, replace=False)
            ops.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        gate = qubitron.CliffordGate.from_op_list(ops, qubits)
        decomposed_ops = qubitron.decompose(gate.on(*qubits))
        circ = qubitron.Circuit(decomposed_ops)
        circ.append(qubitron.I.on_each(qubits))  # make sure the dimension aligned.
        qubitron.testing.assert_allclose_up_to_global_phase(
            qubitron.unitary(gate), qubitron.unitary(circ), atol=1e-7
        )


def test_pad_tableau_bad_input():
    with pytest.raises(
        ValueError, match="Input axes of padding should match with the number of qubits"
    ):
        tableau = qubitron.CliffordTableau(num_qubits=3)
        qubitron.ops.clifford_gate._pad_tableau(tableau, num_qubits_after_padding=4, axes=[1, 2])

    with pytest.raises(
        ValueError, match='The number of qubits in the input tableau should not be larger than'
    ):
        tableau = qubitron.CliffordTableau(num_qubits=3)
        qubitron.ops.clifford_gate._pad_tableau(tableau, num_qubits_after_padding=2, axes=[0, 1, 2])


def test_pad_tableau():
    tableau = qubitron.CliffordTableau(num_qubits=1)
    padded_tableau = qubitron.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[0]
    )
    assert padded_tableau == qubitron.CliffordTableau(num_qubits=2)

    tableau = qubitron.CliffordTableau(num_qubits=1, initial_state=1)
    padded_tableau = qubitron.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=1, axes=[0]
    )
    assert padded_tableau == qubitron.CliffordGate.X.clifford_tableau

    # Tableau for H
    # [0 1 0]
    # [1 0 0]
    tableau = qubitron.CliffordGate.H.clifford_tableau
    padded_tableau = qubitron.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[0]
    )
    # fmt: off
    np.testing.assert_equal(
        padded_tableau.matrix().astype(np.int64),
        np.array([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]]),
    )
    # fmt: on
    np.testing.assert_equal(padded_tableau.rs.astype(np.int64), np.zeros(4))
    # The tableau of H again but pad for another ax
    tableau = qubitron.CliffordGate.H.clifford_tableau
    padded_tableau = qubitron.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[1]
    )
    # fmt: off
    np.testing.assert_equal(
        padded_tableau.matrix().astype(np.int64),
        np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]),
    )
    # fmt: on
    np.testing.assert_equal(padded_tableau.rs.astype(np.int64), np.zeros(4))


def test_clifford_gate_act_on_small_case():
    # Note this is also covered by the `from_op_list` one, etc.

    qubits = qubitron.LineQubit.range(5)
    args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=5), qubits=qubits, prng=np.random.RandomState()
    )
    expected_args = qubitron.CliffordTableauSimulationState(
        tableau=qubitron.CliffordTableau(num_qubits=5), qubits=qubits, prng=np.random.RandomState()
    )
    qubitron.act_on(qubitron.H, expected_args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.CliffordGate.H, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    qubitron.act_on(qubitron.CNOT, expected_args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    qubitron.act_on(qubitron.CliffordGate.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    qubitron.act_on(qubitron.H, expected_args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.CliffordGate.H, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    qubitron.act_on(qubitron.S, expected_args, qubits=[qubits[0]], allow_decompose=False)
    qubitron.act_on(qubitron.CliffordGate.S, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    qubitron.act_on(qubitron.X, expected_args, qubits=[qubits[2]], allow_decompose=False)
    qubitron.act_on(qubitron.CliffordGate.X, args, qubits=[qubits[2]], allow_decompose=False)
    assert args.tableau == expected_args.tableau


def test_clifford_gate_act_on_large_case():
    n, num_ops = 50, 1000  # because we don't need unitary, it is fast.
    gate_candidate = [qubitron.X, qubitron.Y, qubitron.Z, qubitron.H, qubitron.S, qubitron.CNOT, qubitron.CZ]
    for seed in range(10):
        prng = np.random.RandomState(seed)
        t1 = qubitron.CliffordTableau(num_qubits=n)
        t2 = qubitron.CliffordTableau(num_qubits=n)
        qubits = qubitron.LineQubit.range(n)
        args1 = qubitron.CliffordTableauSimulationState(tableau=t1, qubits=qubits, prng=prng)
        args2 = qubitron.CliffordTableauSimulationState(tableau=t2, qubits=qubits, prng=prng)
        ops = []
        for _ in range(0, num_ops, 100):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            qubitron.act_on(
                gate_candidate[g], args1, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            ops.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        compiled_gate = qubitron.CliffordGate.from_op_list(ops, qubits)
        qubitron.act_on(compiled_gate, args2, qubits)

        assert args1.tableau == args2.tableau


def test_clifford_gate_act_on_ch_form():
    # Although we don't support CH_form from the _act_on_, it will fall back
    # to the decomposititon method and apply it through decomposed ops.
    # Here we run it for the coverage only.
    args = qubitron.StabilizerChFormSimulationState(
        initial_state=qubitron.StabilizerStateChForm(num_qubits=2, initial_state=1),
        qubits=qubitron.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    qubitron.act_on(qubitron.CliffordGate.X, args, qubits=qubitron.LineQubit.range(1))
    np.testing.assert_allclose(args.state.state_vector(), np.array([0, 0, 0, 1]))


def test_clifford_gate_act_on_fail():
    with pytest.raises(TypeError, match="Failed to act"):
        qubitron.act_on(qubitron.CliffordGate.X, ExampleSimulationState(), qubits=())


def test_all_single_qubit_clifford_unitaries():
    i = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])

    cs = [qubitron.unitary(c) for c in qubitron.CliffordGate.all_single_qubit_cliffords]

    # Identity
    assert qubitron.equal_up_to_global_phase(cs[0], i)
    # Paulis
    assert qubitron.equal_up_to_global_phase(cs[1], x)
    assert qubitron.equal_up_to_global_phase(cs[2], y)
    assert qubitron.equal_up_to_global_phase(cs[3], z)
    # Square roots of Paulis
    assert qubitron.equal_up_to_global_phase(cs[4], (i - 1j * x) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[5], (i - 1j * y) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[6], (i - 1j * z) / np.sqrt(2))
    # Negative square roots of Paulis
    assert qubitron.equal_up_to_global_phase(cs[7], (i + 1j * x) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[8], (i + 1j * y) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[9], (i + 1j * z) / np.sqrt(2))
    # Hadamards
    assert qubitron.equal_up_to_global_phase(cs[10], (z + x) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[11], (x + y) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[12], (y + z) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[13], (z - x) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[14], (x - y) / np.sqrt(2))
    assert qubitron.equal_up_to_global_phase(cs[15], (y - z) / np.sqrt(2))
    # Order-3 Cliffords
    assert qubitron.equal_up_to_global_phase(cs[16], (i - 1j * (x + y + z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[17], (i - 1j * (x + y - z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[18], (i - 1j * (x - y + z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[19], (i - 1j * (x - y - z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[20], (i - 1j * (-x + y + z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[21], (i - 1j * (-x + y - z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[22], (i - 1j * (-x - y + z)) / 2)
    assert qubitron.equal_up_to_global_phase(cs[23], (i - 1j * (-x - y - z)) / 2)


def test_clifford_gate_repr():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    assert (
        repr(qubitron.ops.CliffordGate.from_op_list([qubitron.ops.X(q0), qubitron.CZ(q1, q2)], [q0, q1, q2]))
        == """Clifford Gate with Tableau:
stable   | destable
---------+----------
- Z0     | + X0
+   Z1   | +   X1Z2
+     Z2 | +   Z1X2
"""
    )
    assert (
        repr(qubitron.ops.CliffordGate.CNOT)
        == """Clifford Gate with Tableau:
stable | destable
-------+----------
+ Z0   | + X0X1
+ Z0Z1 | +   X1
"""
    )


def test_single_qubit_clifford_gate_repr():
    # Common gates
    assert repr(qubitron.ops.SingleQubitCliffordGate.X) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([False, True]), xs=np.array([[True], [False]]), '
        'zs=np.array([[False], [True]])))'
    )
    assert repr(qubitron.ops.SingleQubitCliffordGate.Y) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([True, True]), xs=np.array([[True], [False]]), '
        'zs=np.array([[False], [True]])))'
    )
    assert repr(qubitron.ops.SingleQubitCliffordGate.Z) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([True, False]), xs=np.array([[True], [False]]), '
        'zs=np.array([[False], [True]])))'
    )
    assert repr(qubitron.ops.SingleQubitCliffordGate.I) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([False, False]), xs=np.array([[True], [False]]), '
        'zs=np.array([[False], [True]])))'
    )
    assert repr(qubitron.ops.SingleQubitCliffordGate.X_sqrt) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([False, True]), xs=np.array([[True], [True]]), '
        'zs=np.array([[False], [True]])))'
    )

    assert repr(qubitron.ops.SingleQubitCliffordGate.X) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([False, True]), xs=np.array([[True], [False]]), '
        'zs=np.array([[False], [True]])))'
    )

    # Other gates
    qa = qubitron.NamedQubit('a')
    gate = qubitron.ops.SingleQubitCliffordGate.from_clifford_tableau(
        qubitron.ops.CliffordGate.from_op_list(
            [qubitron.ops.PhasedXZGate(axis_phase_exponent=0.25, x_exponent=-1, z_exponent=0).on(qa)],
            [qa],
        ).clifford_tableau
    )
    assert repr(gate) == (
        'qubitron.ops.SingleQubitCliffordGate(_clifford_tableau=qubitron.CliffordTableau(1, '
        'rs=np.array([False, True]), xs=np.array([[True], [False]]), '
        'zs=np.array([[True], [True]])))'
    )


def test_cxswap_czswap():

    # qubitron unitary for CNOT then SWAP (big endian)
    cxswap_expected = np.asarray([[1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0]])
    print(qubitron.unitary(qubitron.CXSWAP))
    assert np.allclose(qubitron.unitary(qubitron.CXSWAP), cxswap_expected)

    czswap_expected = np.asarray([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, -1]])
    assert np.allclose(qubitron.unitary(qubitron.CZSWAP), czswap_expected)
