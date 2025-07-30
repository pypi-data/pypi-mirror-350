# Copyright 2019 The Qubitron Developers
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


def test_fsim_init() -> None:
    f = qubitron.FSimGate(1, 2)
    assert f.theta == 1
    assert f.phi == 2

    f2 = qubitron.FSimGate(theta=1, phi=2)
    assert f2.theta == 1
    assert f2.phi == 2

    f3 = qubitron.FSimGate(theta=4, phi=-5)
    assert f3.theta == 4 - 2 * np.pi
    assert f3.phi == -5 + 2 * np.pi


def test_fsim_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    a, b = qubitron.LineQubit.range(2)

    eq.add_equality_group(qubitron.FSimGate(1, 2), qubitron.FSimGate(1, 2))
    eq.add_equality_group(qubitron.FSimGate(2, 1))
    eq.add_equality_group(qubitron.FSimGate(0, 0))
    eq.add_equality_group(qubitron.FSimGate(1, 1))
    eq.add_equality_group(qubitron.FSimGate(1, 2).on(a, b), qubitron.FSimGate(1, 2).on(b, a))
    eq.add_equality_group(qubitron.FSimGate(np.pi, np.pi), qubitron.FSimGate(-np.pi, -np.pi))


def test_fsim_approx_eq() -> None:
    assert qubitron.approx_eq(qubitron.FSimGate(1, 2), qubitron.FSimGate(1.00001, 2.00001), atol=0.01)


@pytest.mark.parametrize(
    'theta, phi',
    [
        (0, 0),
        (np.pi / 3, np.pi / 5),
        (-np.pi / 3, np.pi / 5),
        (np.pi / 3, -np.pi / 5),
        (-np.pi / 3, -np.pi / 5),
        (np.pi / 2, 0.5),
    ],
)
def test_fsim_consistent(theta, phi) -> None:
    gate = qubitron.FSimGate(theta=theta, phi=phi)
    qubitron.testing.assert_implements_consistent_protocols(gate)


def test_fsim_circuit() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        qubitron.FSimGate(np.pi / 2, np.pi).on(a, b), qubitron.FSimGate(-np.pi, np.pi / 2).on(a, b)
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───FSim(0.5π, -π)───FSim(-π, 0.5π)───
      │                │
1: ───FSim(0.5π, -π)───FSim(-π, 0.5π)───
    """,
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ---FSim(0.5pi, -pi)---FSim(-pi, 0.5pi)---
      |                  |
1: ---FSim(0.5pi, -pi)---FSim(-pi, 0.5pi)---
        """,
        use_unicode_characters=False,
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ---FSim(1.5707963267948966, -pi)---FSim(-pi, 1.5707963267948966)---
      |                               |
1: ---FSim(1.5707963267948966, -pi)---FSim(-pi, 1.5707963267948966)---
""",
        use_unicode_characters=False,
        precision=None,
    )
    c = qubitron.Circuit(qubitron.FSimGate(sympy.Symbol('a') + sympy.Symbol('b'), 0).on(a, b))
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───FSim(a + b, 0)───
      │
1: ───FSim(a + b, 0)───
    """,
    )


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_fsim_resolve(resolve_fn) -> None:
    f = qubitron.FSimGate(sympy.Symbol('a'), sympy.Symbol('b'))
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'a': 2})
    assert f == qubitron.FSimGate(2, sympy.Symbol('b'))
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'b': 1})
    assert f == qubitron.FSimGate(2, 1)
    assert not qubitron.is_parameterized(f)


def test_fsim_unitary() -> None:
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )

    # Theta
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=np.pi / 2, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 0, -1j, 0],
                [0, -1j, 0, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=-np.pi / 2, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 0, 1j, 0],
                [0, 1j, 0, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=np.pi, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=2 * np.pi, phi=0)),
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=0)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=-np.pi / 2, phi=0)),
        qubitron.unitary(qubitron.FSimGate(theta=3 / 2 * np.pi, phi=0)),
        atol=1e-8,
    )

    # Phi
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=np.pi / 2)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, -1j],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=-np.pi / 2)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1j],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=np.pi)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, -1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=0)),
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=2 * np.pi)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=-np.pi / 2)),
        qubitron.unitary(qubitron.FSimGate(theta=0, phi=3 / 2 * np.pi)),
        atol=1e-8,
    )

    # Both.
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.FSimGate(theta=np.pi / 4, phi=np.pi / 3)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, s, -1j * s, 0],
                [0, -1j * s, s, 0],
                [0, 0, 0, 0.5 - 1j * np.sqrt(0.75)],
            ]
        ),
        atol=1e-8,
    )


@pytest.mark.parametrize(
    'theta, phi',
    (
        (0, 0),
        (0.1, 0.1),
        (-0.1, 0.1),
        (0.1, -0.1),
        (-0.1, -0.1),
        (np.pi / 2, np.pi / 6),
        (np.pi, np.pi),
        (3.5 * np.pi, 4 * np.pi),
    ),
)
def test_fsim_iswap_cphase(theta, phi) -> None:
    q0, q1 = qubitron.NamedQubit('q0'), qubitron.NamedQubit('q1')
    iswap = qubitron.ISWAP ** (-theta * 2 / np.pi)
    cphase = qubitron.CZPowGate(exponent=-phi / np.pi)
    iswap_cphase = qubitron.Circuit((iswap.on(q0, q1), cphase.on(q0, q1)))
    fsim = qubitron.FSimGate(theta=theta, phi=phi)
    assert np.allclose(qubitron.unitary(iswap_cphase), qubitron.unitary(fsim))


def test_fsim_repr() -> None:
    f = qubitron.FSimGate(sympy.Symbol('a'), sympy.Symbol('b'))
    qubitron.testing.assert_equivalent_repr(f)


def test_fsim_json_dict() -> None:
    assert qubitron.FSimGate(theta=0.123, phi=0.456)._json_dict_() == {'theta': 0.123, 'phi': 0.456}


def test_phased_fsim_init() -> None:
    f = qubitron.PhasedFSimGate(1, 2, 3, 4, 5)
    assert f.theta == 1
    assert f.zeta == 2
    assert f.chi == 3
    assert f.gamma == 4 - 2 * np.pi
    assert f.phi == 5 - 2 * np.pi

    f2 = qubitron.PhasedFSimGate(theta=1, zeta=2, chi=3, gamma=4, phi=5)
    assert f2.theta == 1
    assert f2.zeta == 2
    assert f2.chi == 3
    assert f2.gamma == 4 - 2 * np.pi
    assert f2.phi == 5 - 2 * np.pi


@pytest.mark.parametrize(
    'theta, phi, rz_angles_before, rz_angles_after',
    (
        (0, 0, (0, 0), (0, 0)),
        (1, 2, (3, 4), (5, 7)),
        (np.pi / 5, np.pi / 6, (0.1, 0.2), (0.3, 0.5)),
    ),
)
def test_phased_fsim_from_fsim_rz(theta, phi, rz_angles_before, rz_angles_after) -> None:
    f = qubitron.PhasedFSimGate.from_fsim_rz(theta, phi, rz_angles_before, rz_angles_after)
    q0, q1 = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        qubitron.rz(rz_angles_before[0]).on(q0),
        qubitron.rz(rz_angles_before[1]).on(q1),
        qubitron.FSimGate(theta, phi).on(q0, q1),
        qubitron.rz(rz_angles_after[0]).on(q0),
        qubitron.rz(rz_angles_after[1]).on(q1),
    )
    qubitron.testing.assert_allclose_up_to_global_phase(qubitron.unitary(f), qubitron.unitary(c), atol=1e-8)


@pytest.mark.parametrize(
    'rz_angles_before, rz_angles_after',
    (
        ((0, 0), (0, 0)),
        ((0.1, 0.2), (0.3, 0.7)),
        ((0.1, 0.2), (0.3, -0.8)),
        ((-0.1, -0.2), (-0.3, -0.9)),
        ((np.pi / 5, -np.pi / 3), (0, np.pi / 2)),
    ),
)
def test_phased_fsim_recreate_from_phase_angles(rz_angles_before, rz_angles_after) -> None:
    f = qubitron.PhasedFSimGate.from_fsim_rz(np.pi / 3, np.pi / 5, rz_angles_before, rz_angles_after)
    f2 = qubitron.PhasedFSimGate.from_fsim_rz(f.theta, f.phi, f.rz_angles_before, f.rz_angles_after)
    assert qubitron.approx_eq(f, f2)


@pytest.mark.parametrize(
    'rz_angles_before, rz_angles_after',
    (
        ((0, 0), (0, 0)),
        ((0.1, 0.2), (0.3, 0.7)),
        ((-0.1, 0.2), (0.3, 0.8)),
        ((-0.1, -0.2), (0.3, -0.9)),
        ((np.pi, np.pi / 6), (-np.pi / 2, 0)),
    ),
)
def test_phased_fsim_phase_angle_symmetry(rz_angles_before, rz_angles_after) -> None:
    f = qubitron.PhasedFSimGate.from_fsim_rz(np.pi / 3, np.pi / 5, rz_angles_before, rz_angles_after)
    for d in (-10, -7, -2 * np.pi, -0.2, 0, 0.1, 0.2, np.pi, 8, 20):
        rz_angles_before2 = (rz_angles_before[0] + d, rz_angles_before[1] + d)
        rz_angles_after2 = (rz_angles_after[0] - d, rz_angles_after[1] - d)
        f2 = qubitron.PhasedFSimGate.from_fsim_rz(
            np.pi / 3, np.pi / 5, rz_angles_before2, rz_angles_after2
        )
        assert qubitron.approx_eq(f, f2)


def test_phased_fsim_eq() -> None:
    eq = qubitron.testing.EqualsTester()
    a, b = qubitron.LineQubit.range(2)
    r, s = sympy.Symbol('r'), sympy.Symbol('s')

    eq.add_equality_group(qubitron.PhasedFSimGate(1, 2, 3, 4, 5), qubitron.PhasedFSimGate(1, 2, 3, 4, 5))
    eq.add_equality_group(qubitron.PhasedFSimGate(2, 1, 3, 4, 5))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 0, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(0, 1, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(0, 0, 0, 1, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(0, 0, 0, 0, 1))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, 0, 0, r))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, 0, 0, s))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, 0, r, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, 0, s, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, r, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 1, s, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, r, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, s, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(r, 1, 0, 0, 0))
    eq.add_equality_group(qubitron.PhasedFSimGate(s, 1, 0, 0, 0))
    eq.add_equality_group(
        qubitron.PhasedFSimGate(np.pi, np.pi, np.pi, np.pi, np.pi),
        qubitron.PhasedFSimGate(-np.pi, -np.pi, -np.pi, -np.pi, -np.pi),
    )

    # Regions of insensitivity to zeta and chi
    eq.add_equality_group(
        qubitron.PhasedFSimGate(np.pi / 2, 0, 0, 4, 5), qubitron.PhasedFSimGate(np.pi / 2, 2, 0, 4, 5)
    )
    eq.add_equality_group(qubitron.PhasedFSimGate(0, 0, 0, 0, 0), qubitron.PhasedFSimGate(0, 0, 1, 0, 0))
    eq.add_equality_group(
        qubitron.PhasedFSimGate(np.pi, 0, 0, 4, 5), qubitron.PhasedFSimGate(np.pi, 0, 3, 4, 5)
    )
    eq.add_equality_group(
        qubitron.PhasedFSimGate(sympy.pi / 2, 0, 0, 4, 5), qubitron.PhasedFSimGate(sympy.pi / 2, 2, 0, 4, 5)
    )
    eq.add_equality_group(
        qubitron.PhasedFSimGate(-sympy.pi, 0, 0, 4, 5), qubitron.PhasedFSimGate(-sympy.pi, 0, 3, 4, 5)
    )

    # Symmetries under qubit exchange
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 2, 3, 4, 5).on(a, b))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 2, 3, 4, 5).on(b, a))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 0, 3, 4, 5).on(a, b))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 0, 3, 4, 5).on(b, a))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 2, 0, 4, 5).on(a, b))
    eq.add_equality_group(qubitron.PhasedFSimGate(1, 2, 0, 4, 5).on(b, a))
    eq.add_equality_group(
        qubitron.PhasedFSimGate(1, 0, 0, 4, 5).on(a, b), qubitron.PhasedFSimGate(1, 0, 0, 4, 5).on(b, a)
    )
    eq.add_equality_group(
        qubitron.PhasedFSimGate(1, -np.pi, np.pi, 4, 5).on(a, b),
        qubitron.PhasedFSimGate(1, -np.pi, np.pi, 4, 5).on(b, a),
    )
    eq.add_equality_group(
        qubitron.PhasedFSimGate(1, -sympy.pi, -sympy.pi, r, 5).on(a, b),
        qubitron.PhasedFSimGate(1, -sympy.pi, -sympy.pi, r, 5).on(b, a),
    )
    eq.add_equality_group(qubitron.PhasedFSimGate(sympy.pi / 3, 2, 0, 4, 5).on(a, b))
    eq.add_equality_group(qubitron.PhasedFSimGate(sympy.pi / 3, 2, 0, 4, 5).on(b, a))


@pytest.mark.parametrize(
    'gate, interchangeable',
    (
        (qubitron.PhasedFSimGate(1, 2, 3, 4, 5), False),
        (qubitron.PhasedFSimGate(1, 2, 0, 4, 5), False),
        (qubitron.PhasedFSimGate(1, 0, 3, 4, 5), False),
        (qubitron.PhasedFSimGate(1, 0, 0, 4, 5), True),
        (qubitron.PhasedFSimGate(np.pi / 2, 2, 0, 4, 5), True),
        (qubitron.PhasedFSimGate(np.pi, 0, 3, 4, 5), True),
        (qubitron.PhasedFSimGate(1, -np.pi, 0, 4, 5), True),
        (qubitron.PhasedFSimGate(1, 0, np.pi, 4, 5), True),
        (qubitron.PhasedFSimGate(1, np.pi / 2, 0, 4, 5), False),
    ),
)
def test_qubit_interchangeability(gate, interchangeable) -> None:
    a, b = qubitron.LineQubit.range(2)
    c1 = qubitron.Circuit(gate.on(a, b))
    c2 = qubitron.Circuit(qubitron.SWAP(a, b), gate.on(a, b), qubitron.SWAP(a, b))
    u1 = qubitron.unitary(c1)
    u2 = qubitron.unitary(c2)
    assert np.all(u1 == u2) == interchangeable


def test_phased_fsim_approx_eq() -> None:
    assert qubitron.approx_eq(
        qubitron.PhasedFSimGate(1, 2, 3, 4, 5),
        qubitron.PhasedFSimGate(1.00001, 2.00001, 3.00001, 4.00004, 5.00005),
        atol=0.01,
    )


@pytest.mark.parametrize(
    'theta, zeta, chi, gamma, phi',
    [
        (0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (np.pi / 3, 0, 0, 0, np.pi / 5),
        (np.pi / 3, 1, 0, 0, np.pi / 5),
        (np.pi / 3, 0, 1, 0, np.pi / 5),
        (np.pi / 3, 0, 0, 1, np.pi / 5),
        (-np.pi / 3, 1, 0, 0, np.pi / 5),
        (np.pi / 3, 0, 1, 0, -np.pi / 5),
        (-np.pi / 3, 0, 0, 1, -np.pi / 5),
        (np.pi, 0, 0, sympy.Symbol('a'), 0),
    ],
)
def test_phased_fsim_consistent(theta, zeta, chi, gamma, phi) -> None:
    gate = qubitron.PhasedFSimGate(theta=theta, zeta=zeta, chi=chi, gamma=gamma, phi=phi)
    qubitron.testing.assert_implements_consistent_protocols(gate)


def test_phased_fsim_circuit() -> None:
    a, b = qubitron.LineQubit.range(2)
    c = qubitron.Circuit(
        qubitron.PhasedFSimGate(np.pi / 2, np.pi, np.pi / 2, 0, -np.pi / 4).on(a, b),
        qubitron.PhasedFSimGate(-np.pi, np.pi / 2, np.pi / 10, np.pi / 5, 3 * np.pi / 10).on(a, b),
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───PhFSim(0.5π, -π, 0.5π, 0, -0.25π)───PhFSim(-π, 0.5π, 0.1π, 0.2π, 0.3π)───
      │                                   │
1: ───PhFSim(0.5π, -π, 0.5π, 0, -0.25π)───PhFSim(-π, 0.5π, 0.1π, 0.2π, 0.3π)───
    """,
    )
    # pylint: disable=line-too-long
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ---PhFSim(0.5pi, -pi, 0.5pi, 0, -0.25pi)---PhFSim(-pi, 0.5pi, 0.1pi, 0.2pi, 0.3pi)---
      |                                       |
1: ---PhFSim(0.5pi, -pi, 0.5pi, 0, -0.25pi)---PhFSim(-pi, 0.5pi, 0.1pi, 0.2pi, 0.3pi)---
        """,
        use_unicode_characters=False,
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ---PhFSim(1.5707963267948966, -pi, 1.5707963267948966, 0, -0.7853981633974483)---PhFSim(-pi, 1.5707963267948966, 0.3141592653589793, 0.6283185307179586, 0.9424777960769379)---
      |                                                                             |
1: ---PhFSim(1.5707963267948966, -pi, 1.5707963267948966, 0, -0.7853981633974483)---PhFSim(-pi, 1.5707963267948966, 0.3141592653589793, 0.6283185307179586, 0.9424777960769379)---
""",
        use_unicode_characters=False,
        precision=None,
    )
    # pylint: enable=line-too-long
    c = qubitron.Circuit(
        qubitron.PhasedFSimGate(
            sympy.Symbol('a') + sympy.Symbol('b'),
            0,
            sympy.Symbol('c'),
            sympy.Symbol('d'),
            sympy.Symbol('a') - sympy.Symbol('b'),
        ).on(a, b)
    )
    qubitron.testing.assert_has_diagram(
        c,
        """
0: ───PhFSim(a + b, 0, c, d, a - b)───
      │
1: ───PhFSim(a + b, 0, c, d, a - b)───
    """,
    )


@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_phased_fsim_resolve(resolve_fn) -> None:
    f = qubitron.PhasedFSimGate(
        sympy.Symbol('a'),
        sympy.Symbol('b'),
        sympy.Symbol('c'),
        sympy.Symbol('d'),
        sympy.Symbol('e'),
    )
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'a': 1})
    assert f == qubitron.PhasedFSimGate(
        1, sympy.Symbol('b'), sympy.Symbol('c'), sympy.Symbol('d'), sympy.Symbol('e')
    )
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'b': 2})
    assert f == qubitron.PhasedFSimGate(1, 2, sympy.Symbol('c'), sympy.Symbol('d'), sympy.Symbol('e'))
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'c': 3})
    assert f == qubitron.PhasedFSimGate(1, 2, 3, sympy.Symbol('d'), sympy.Symbol('e'))
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'d': 4})
    assert f == qubitron.PhasedFSimGate(1, 2, 3, 4, sympy.Symbol('e'))
    assert qubitron.is_parameterized(f)

    f = resolve_fn(f, {'e': 5})
    assert f == qubitron.PhasedFSimGate(1, 2, 3, 4, 5)
    assert not qubitron.is_parameterized(f)


def test_phased_fsim_unitary() -> None:
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )

    # Theta
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi / 2, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 0, -1j, 0],
                [0, -1j, 0, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=-np.pi / 2, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 0, 1j, 0],
                [0, 1j, 0, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi, phi=0)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=2 * np.pi, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=0)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=-np.pi / 2, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=3 / 2 * np.pi, phi=0)),
        atol=1e-8,
    )

    # Phi
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=np.pi / 2)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, -1j],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=-np.pi / 2)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1j],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=np.pi)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, -1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=2 * np.pi)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=-np.pi / 2)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=3 / 2 * np.pi)),
        atol=1e-8,
    )

    # Theta and phi
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi / 4, phi=np.pi / 3)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, s, -1j * s, 0],
                [0, -1j * s, s, 0],
                [0, 0, 0, 0.5 - 1j * np.sqrt(0.75)],
            ]
        ),
        atol=1e-8,
    )

    # Zeta, gamma, chi
    w6 = np.exp(-1j * np.pi / 6)
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, gamma=np.pi / 2, zeta=np.pi / 3)),
        np.array([[1, 0, 0, 0], [0, -w6.conjugate(), 0, 0], [0, 0, w6, 0], [0, 0, 0, -1]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=0, phi=0, chi=0.2)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi, chi=0.2)),
        atol=1e-8,
    )
    # fmt: off
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=-np.pi / 2, gamma=np.pi / 2, chi=np.pi / 3)),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 0, 1j * w6, 0],
                [0, 1j * -w6.conjugate(), 0, 0],
                [0, 0, 0, -1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi / 2, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=np.pi / 2, zeta=0.2, phi=0)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(theta=-np.pi / 2, phi=0)),
        qubitron.unitary(qubitron.PhasedFSimGate(theta=-np.pi / 2, zeta=0.2)),
        atol=1e-8,
    )

    # Zeta insensitivity region
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(-np.pi / 2, 0, 1, 2, 3)),
        qubitron.unitary(qubitron.PhasedFSimGate(-np.pi / 2, 0.1, 1, 2, 3)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(np.pi / 2, 1, 1, 2, 3)),
        qubitron.unitary(qubitron.PhasedFSimGate(np.pi / 2, 2, 1, 2, 3)),
        atol=1e-8,
    )

    # Chi insensitivity region
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(-np.pi, 1, 0, 2, 3)),
        qubitron.unitary(qubitron.PhasedFSimGate(-np.pi, 1, 0.1, 2, 3)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(0, 1, 1, 2, 3)),
        qubitron.unitary(qubitron.PhasedFSimGate(0, 1, 2, 2, 3)),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        qubitron.unitary(qubitron.PhasedFSimGate(np.pi / 2, -0.5, 1, 2, 3)),
        qubitron.unitary(qubitron.PhasedFSimGate(np.pi / 2, -0.2, 1, 2, 3)),
        atol=1e-8,
    )


@pytest.mark.parametrize(
    'theta, phi',
    (
        (0, 0),
        (0.1, 0.1),
        (-0.1, 0.1),
        (0.1, -0.1),
        (-0.1, -0.1),
        (np.pi / 2, np.pi / 6),
        (np.pi, np.pi),
        (3.5 * np.pi, 4 * np.pi),
    ),
)
def test_phased_fsim_vs_fsim(theta, phi) -> None:
    g1 = qubitron.FSimGate(theta, phi)
    g2 = qubitron.PhasedFSimGate(theta, 0, 0, 0, phi)
    assert np.allclose(qubitron.unitary(g1), qubitron.unitary(g2))


def test_phased_fsim_repr() -> None:
    f = qubitron.PhasedFSimGate(
        sympy.Symbol('a'),
        sympy.Symbol('b'),
        sympy.Symbol('c'),
        sympy.Symbol('d'),
        sympy.Symbol('e'),
    )
    qubitron.testing.assert_equivalent_repr(f)


def test_phased_fsim_json_dict() -> None:
    assert qubitron.PhasedFSimGate(
        theta=0.12, zeta=0.34, chi=0.56, gamma=0.78, phi=0.9
    )._json_dict_() == {'theta': 0.12, 'zeta': 0.34, 'chi': 0.56, 'gamma': 0.78, 'phi': 0.9}


@pytest.mark.parametrize(
    'gate',
    [
        qubitron.CZ,
        qubitron.SQRT_ISWAP,
        qubitron.SQRT_ISWAP_INV,
        qubitron.ISWAP,
        qubitron.ISWAP_INV,
        qubitron.cphase(0.1),
        qubitron.CZ**0.2,
    ],
)
def test_phase_fsim_from_matrix(gate) -> None:
    u = qubitron.unitary(gate)
    np.testing.assert_allclose(qubitron.unitary(qubitron.PhasedFSimGate.from_matrix(u)), u, atol=1e-8)


def test_phase_fsim_from_matrix_not_fsim_returns_none() -> None:
    assert qubitron.PhasedFSimGate.from_matrix(np.ones((4, 4))) is None
