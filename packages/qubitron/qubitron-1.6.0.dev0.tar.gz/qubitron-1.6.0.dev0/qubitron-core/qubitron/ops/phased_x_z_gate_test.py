# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import random

import numpy as np
import pytest
import sympy

import qubitron


def test_init_properties():
    g = qubitron.PhasedXZGate(x_exponent=0.125, z_exponent=0.25, axis_phase_exponent=0.375)
    assert g.x_exponent == 0.125
    assert g.z_exponent == 0.25
    assert g.axis_phase_exponent == 0.375


def test_eq():
    eq = qubitron.testing.EqualsTester()
    eq.make_equality_group(
        lambda: qubitron.PhasedXZGate(x_exponent=0.25, z_exponent=0.5, axis_phase_exponent=0.75)
    )

    # Sensitive to each parameter.
    eq.add_equality_group(qubitron.PhasedXZGate(x_exponent=0, z_exponent=0.5, axis_phase_exponent=0.75))
    eq.add_equality_group(
        qubitron.PhasedXZGate(x_exponent=0.25, z_exponent=0, axis_phase_exponent=0.75)
    )
    eq.add_equality_group(qubitron.PhasedXZGate(x_exponent=0.25, z_exponent=0.5, axis_phase_exponent=0))

    # Different from other gates.
    eq.add_equality_group(qubitron.PhasedXPowGate(exponent=0.25, phase_exponent=0.75))
    eq.add_equality_group(qubitron.X)
    eq.add_equality_group(qubitron.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0))


@pytest.mark.parametrize('z0_rad', [-np.pi / 5, 0, np.pi / 5, np.pi / 4, np.pi / 2, np.pi])
@pytest.mark.parametrize('y_rad', [0, np.pi / 5, np.pi / 4, np.pi / 2, np.pi])
@pytest.mark.parametrize('z1_rad', [-np.pi / 5, 0, np.pi / 5, np.pi / 4, np.pi / 2, np.pi])
def test_from_zyz_angles(z0_rad: float, y_rad: float, z1_rad: float) -> None:
    q = qubitron.q(0)
    phxz = qubitron.PhasedXZGate.from_zyz_angles(z0_rad, y_rad, z1_rad)
    zyz = qubitron.Circuit(qubitron.rz(z0_rad).on(q), qubitron.ry(y_rad).on(q), qubitron.rz(z1_rad).on(q))
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(phxz), qubitron.unitary(zyz), atol=1e-8
    )


@pytest.mark.parametrize('z0', [-0.2, 0, 0.2, 0.25, 0.5, 1])
@pytest.mark.parametrize('y', [0, 0.2, 0.25, 0.5, 1])
@pytest.mark.parametrize('z1', [-0.2, 0, 0.2, 0.25, 0.5, 1])
def test_from_zyz_exponents(z0: float, y: float, z1: float) -> None:
    q = qubitron.q(0)
    phxz = qubitron.PhasedXZGate.from_zyz_exponents(z0, y, z1)
    zyz = qubitron.Circuit(qubitron.Z(q) ** z0, qubitron.Y(q) ** y, qubitron.Z(q) ** z1)
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(phxz), qubitron.unitary(zyz), atol=1e-8
    )


def test_canonicalization():
    def f(x, z, a):
        return qubitron.PhasedXZGate(x_exponent=x, z_exponent=z, axis_phase_exponent=a)

    # Canonicalizations are equivalent.
    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(f(-1, 0, 0), f(-3, 0, 0), f(1, 1, 0.5))
    """
    # Canonicalize X exponent (-1, +1].
    if isinstance(x, numbers.Real):
        x %= 2
        if x > 1:
            x -= 2
    # Axis phase exponent is irrelevant if there is no X exponent.
    # Canonicalize Z exponent (-1, +1].
    if isinstance(z, numbers.Real):
        z %= 2
        if z > 1:
            z -= 2

    # Canonicalize axis phase exponent into (-0.5, +0.5].
    if isinstance(a, numbers.Real):
        a %= 2
        if a > 1:
            a -= 2
        if a <= -0.5:
            a += 1
            x = -x
        elif a > 0.5:
            a -= 1
            x = -x
    """

    # X rotation gets canonicalized.
    t = f(3, 0, 0)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0
    t = f(1.5, 0, 0)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0

    # Z rotation gets canonicalized.
    t = f(0, 3, 0)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == 1
    assert t.axis_phase_exponent == 0
    t = f(0, 1.5, 0)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == -0.5
    assert t.axis_phase_exponent == 0

    # Axis phase gets canonicalized.
    t = f(0.5, 0, 2.25)._canonical()
    assert t.x_exponent == 0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0.25
    t = f(0.5, 0, 1.25)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0.25
    t = f(0.5, 0, 0.75)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == -0.25

    # 180 degree rotations don't need a virtual Z.
    t = f(1, 1, 0.5)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0
    t = f(1, 0.25, 0.5)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == -0.375
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(t), qubitron.unitary(f(1, 0.25, 0.5)), atol=1e-8
    )

    # Axis phase is irrelevant when not rotating.
    t = f(0, 0.25, 0.5)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == 0.25
    assert t.axis_phase_exponent == 0


def test_from_matrix():
    # Axis rotations.
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.X**0.1)),
        qubitron.PhasedXZGate(x_exponent=0.1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.X**-0.1)),
        qubitron.PhasedXZGate(x_exponent=-0.1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Y**0.1)),
        qubitron.PhasedXZGate(x_exponent=0.1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Y**-0.1)),
        qubitron.PhasedXZGate(x_exponent=-0.1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Z**-0.1)),
        qubitron.PhasedXZGate(x_exponent=0, z_exponent=-0.1, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Z**0.1)),
        qubitron.PhasedXZGate(x_exponent=0, z_exponent=0.1, axis_phase_exponent=0),
        atol=1e-8,
    )

    # Pauli matrices.
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(np.eye(2)),
        qubitron.PhasedXZGate(x_exponent=0, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.X)),
        qubitron.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Y)),
        qubitron.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert qubitron.approx_eq(
        qubitron.PhasedXZGate.from_matrix(qubitron.unitary(qubitron.Z)),
        qubitron.PhasedXZGate(x_exponent=0, z_exponent=1, axis_phase_exponent=0),
        atol=1e-8,
    )

    # Round trips.
    a = random.random()
    b = random.random()
    c = random.random()
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    assert qubitron.approx_eq(qubitron.PhasedXZGate.from_matrix(qubitron.unitary(g)), g, atol=1e-8)


@pytest.mark.parametrize(
    'unitary',
    [
        qubitron.testing.random_unitary(2),
        qubitron.testing.random_unitary(2),
        qubitron.testing.random_unitary(2),
        np.array([[0, 1], [1j, 0]]),
    ],
)
def test_from_matrix_close_unitary(unitary: np.ndarray):
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(qubitron.PhasedXZGate.from_matrix(unitary)), unitary, atol=1e-8
    )


@pytest.mark.parametrize(
    'unitary',
    [
        qubitron.testing.random_unitary(2),
        qubitron.testing.random_unitary(2),
        qubitron.testing.random_unitary(2),
        np.array([[0, 1], [1j, 0]]),
    ],
)
def test_from_matrix_close_kraus(unitary: np.ndarray):
    gate = qubitron.PhasedXZGate.from_matrix(unitary)
    kraus = qubitron.kraus(gate)
    assert len(kraus) == 1
    qubitron.testing.assert_allclose_up_to_global_phase(kraus[0], unitary, atol=1e-8)


def test_protocols():
    a = random.random()
    b = random.random()
    c = random.random()
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    qubitron.testing.assert_implements_consistent_protocols(g)

    # Symbolic.
    t = sympy.Symbol('t')
    g = qubitron.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c)
    qubitron.testing.assert_implements_consistent_protocols(g)
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c)
    qubitron.testing.assert_implements_consistent_protocols(g)
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t)
    qubitron.testing.assert_implements_consistent_protocols(g)


def test_inverse():
    a = random.random()
    b = random.random()
    c = random.random()
    q = qubitron.LineQubit(0)
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c).on(q)

    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(g**-1), np.transpose(np.conjugate(qubitron.unitary(g))), atol=1e-8
    )


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterized(resolve_fn):
    a = random.random()
    b = random.random()
    c = random.random()
    g = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    assert not qubitron.is_parameterized(g)

    t = sympy.Symbol('t')
    gt = qubitron.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c)
    assert qubitron.is_parameterized(gt)
    assert resolve_fn(gt, {'t': a}) == g
    gt = qubitron.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c)
    assert qubitron.is_parameterized(gt)
    assert resolve_fn(gt, {'t': b}) == g
    gt = qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t)
    assert qubitron.is_parameterized(gt)
    assert resolve_fn(gt, {'t': c}) == g

    resolver = {'t': 0.5j}
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(qubitron.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c), resolver)
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(qubitron.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c), resolver)
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(qubitron.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t), resolver)


def test_str_diagram():
    g = qubitron.PhasedXZGate(x_exponent=0.5, z_exponent=0.25, axis_phase_exponent=0.125)

    assert str(g) == "PhXZ(a=0.125,x=0.5,z=0.25)"

    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(g.on(qubitron.LineQubit(0))),
        """
0: ───PhXZ(a=0.125,x=0.5,z=0.25)───
    """,
    )
