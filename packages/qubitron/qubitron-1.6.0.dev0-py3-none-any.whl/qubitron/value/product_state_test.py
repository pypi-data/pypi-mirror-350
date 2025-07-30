# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import numpy as np
import pytest

import qubitron


def test_name():
    names = [str(state) for state in qubitron.PAULI_STATES]
    assert names == ['+X', '-X', '+Y', '-Y', '+Z', '-Z']


def test_repr():
    for o in qubitron.PAULI_STATES:
        assert o == eval(repr(o))


def test_equality():
    assert qubitron.KET_PLUS == qubitron.KET_PLUS
    assert qubitron.KET_PLUS != qubitron.KET_MINUS
    assert qubitron.KET_PLUS != qubitron.KET_ZERO

    assert hash(qubitron.KET_PLUS) == hash(qubitron.KET_PLUS)


def test_basis_construction():
    states = []
    for gate in [qubitron.X, qubitron.Y, qubitron.Z]:
        for e_val in [+1, -1]:
            states.append(gate.basis[e_val])

    assert states == qubitron.PAULI_STATES


def test_stabilized():
    for state in qubitron.PAULI_STATES:
        val, gate = state.stabilized_by()
        matrix = qubitron.unitary(gate)
        vec = state.state_vector()

        np.testing.assert_allclose(matrix @ vec, val * vec)


def test_projector():
    np.testing.assert_equal(qubitron.KET_ZERO.projector(), [[1, 0], [0, 0]])
    np.testing.assert_equal(qubitron.KET_ONE.projector(), [[0, 0], [0, 1]])
    np.testing.assert_allclose(qubitron.KET_PLUS.projector(), np.array([[1, 1], [1, 1]]) / 2)
    np.testing.assert_allclose(qubitron.KET_MINUS.projector(), np.array([[1, -1], [-1, 1]]) / 2)


def test_projector_2():
    for gate in [qubitron.X, qubitron.Y, qubitron.Z]:
        for eigen_index in [0, 1]:
            eigenvalue = {0: +1, 1: -1}[eigen_index]
            np.testing.assert_allclose(
                gate.basis[eigenvalue].projector(), gate._eigen_components()[eigen_index][1]
            )


def test_oneq_state():
    q0, q1 = qubitron.LineQubit.range(2)
    st0 = qubitron.KET_PLUS(q0)
    assert str(st0) == '+X(q(0))'

    st1 = qubitron.KET_PLUS(q1)
    assert st0 != st1

    assert st0 == qubitron.KET_PLUS.on(q0)


def test_product_state():
    q0, q1, q2 = qubitron.LineQubit.range(3)

    plus0 = qubitron.KET_PLUS(q0)
    plus1 = qubitron.KET_PLUS(q1)

    ps = plus0 * plus1
    assert str(plus0) == "+X(q(0))"
    assert str(plus1) == "+X(q(1))"
    assert str(ps) == "+X(q(0)) * +X(q(1))"

    ps *= qubitron.KET_ONE(q2)
    assert str(ps) == "+X(q(0)) * +X(q(1)) * -Z(q(2))"

    with pytest.raises(ValueError) as e:
        # Re-use q2
        ps *= qubitron.KET_PLUS(q2)
    assert e.match(r'.*both contain factors for these qubits: ' r'\[qubitron.LineQubit\(2\)\]')

    ps2 = eval(repr(ps))
    assert ps == ps2


def test_product_state_2():
    q0, q1 = qubitron.LineQubit.range(2)

    with pytest.raises(ValueError):
        # No coefficient
        _ = qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1) * -1
    with pytest.raises(ValueError):
        # Not a state
        _ = qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1) * qubitron.KET_ZERO


def test_product_qubits():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    ps = qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1) * qubitron.KET_ZERO(q2)
    assert ps.qubits == [q0, q1, q2]
    assert ps[q0] == qubitron.KET_PLUS


def test_product_iter():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    ps = qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1) * qubitron.KET_ZERO(q2)

    should_be = [(q0, qubitron.KET_PLUS), (q1, qubitron.KET_PLUS), (q2, qubitron.KET_ZERO)]
    assert list(ps) == should_be
    assert len(ps) == 3


def test_product_state_equality():
    q0, q1, q2 = qubitron.LineQubit.range(3)

    assert qubitron.KET_PLUS(q0) == qubitron.KET_PLUS(q0)
    assert qubitron.KET_PLUS(q0) != qubitron.KET_PLUS(q1)
    assert qubitron.KET_PLUS(q0) != qubitron.KET_MINUS(q0)

    assert qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1) == qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1)
    assert qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1) != qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q2)

    assert hash(qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1)) == hash(
        qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1)
    )
    assert hash(qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1)) != hash(
        qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q2)
    )
    assert qubitron.KET_PLUS(q0) != '+X(0)'


def test_tp_state_vector():
    q0, q1 = qubitron.LineQubit.range(2)
    s00 = qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1)
    np.testing.assert_equal(s00.state_vector(), [1, 0, 0, 0])
    np.testing.assert_equal(s00.state_vector(qubit_order=(q1, q0)), [1, 0, 0, 0])

    s01 = qubitron.KET_ZERO(q0) * qubitron.KET_ONE(q1)
    np.testing.assert_equal(s01.state_vector(), [0, 1, 0, 0])
    np.testing.assert_equal(s01.state_vector(qubit_order=(q1, q0)), [0, 0, 1, 0])


def test_tp_initial_state():
    q0, q1 = qubitron.LineQubit.range(2)
    psi1 = qubitron.final_state_vector(qubitron.Circuit([qubitron.I.on_each(q0, q1), qubitron.X(q1)]))

    s01 = qubitron.KET_ZERO(q0) * qubitron.KET_ONE(q1)
    psi2 = qubitron.final_state_vector(qubitron.Circuit([qubitron.I.on_each(q0, q1)]), initial_state=s01)

    np.testing.assert_allclose(psi1, psi2)


def test_tp_projector():
    q0, q1 = qubitron.LineQubit.range(2)
    p00 = (qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit(qubitron.I.on_each(q0, q1)))
    np.testing.assert_allclose(rho, p00)

    p01 = (qubitron.KET_ZERO(q0) * qubitron.KET_ONE(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit([qubitron.I.on_each(q0, q1), qubitron.X(q1)]))
    np.testing.assert_allclose(rho, p01)

    ppp = (qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit([qubitron.H.on_each(q0, q1)]))
    np.testing.assert_allclose(rho, ppp, atol=1e-7)

    ppm = (qubitron.KET_PLUS(q0) * qubitron.KET_MINUS(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit([qubitron.H.on_each(q0, q1), qubitron.Z(q1)]))
    np.testing.assert_allclose(rho, ppm, atol=1e-7)

    pii = (qubitron.KET_IMAG(q0) * qubitron.KET_IMAG(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit(qubitron.rx(-np.pi / 2).on_each(q0, q1)))
    np.testing.assert_allclose(rho, pii, atol=1e-7)

    pij = (qubitron.KET_IMAG(q0) * qubitron.KET_MINUS_IMAG(q1)).projector()
    rho = qubitron.final_density_matrix(qubitron.Circuit(qubitron.rx(-np.pi / 2)(q0), qubitron.rx(np.pi / 2)(q1)))
    np.testing.assert_allclose(rho, pij, atol=1e-7)
