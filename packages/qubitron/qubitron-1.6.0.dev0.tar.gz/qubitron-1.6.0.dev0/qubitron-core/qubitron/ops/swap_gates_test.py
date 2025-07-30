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
from scipy import linalg

import qubitron


@pytest.mark.parametrize('eigen_gate_type', [qubitron.ISwapPowGate, qubitron.SwapPowGate])
def test_phase_sensitive_eigen_gates_consistent_protocols(eigen_gate_type) -> None:
    qubitron.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


def test_interchangeable_qubit_eq() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    c = qubitron.NamedQubit('c')
    eq = qubitron.testing.EqualsTester()

    eq.add_equality_group(qubitron.SWAP(a, b), qubitron.SWAP(b, a))
    eq.add_equality_group(qubitron.SWAP(a, c))

    eq.add_equality_group(qubitron.SWAP(a, b) ** 0.3, qubitron.SWAP(b, a) ** 0.3)
    eq.add_equality_group(qubitron.SWAP(a, c) ** 0.3)

    eq.add_equality_group(qubitron.ISWAP(a, b), qubitron.ISWAP(b, a))
    eq.add_equality_group(qubitron.ISWAP(a, c))

    eq.add_equality_group(qubitron.ISWAP(a, b) ** 0.3, qubitron.ISWAP(b, a) ** 0.3)
    eq.add_equality_group(qubitron.ISWAP(a, c) ** 0.3)


def test_text_diagrams() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')
    circuit = qubitron.Circuit(qubitron.SWAP(a, b), qubitron.ISWAP(a, b) ** -1)

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ───×───iSwap──────
      │   │
b: ───×───iSwap^-1───
""",
    )

    qubitron.testing.assert_has_diagram(
        circuit,
        """
a: ---Swap---iSwap------
      |      |
b: ---Swap---iSwap^-1---
""",
        use_unicode_characters=False,
    )


def test_swap_has_stabilizer_effect() -> None:
    assert qubitron.has_stabilizer_effect(qubitron.SWAP)
    assert qubitron.has_stabilizer_effect(qubitron.SWAP**2)
    assert not qubitron.has_stabilizer_effect(qubitron.SWAP**0.5)
    assert not qubitron.has_stabilizer_effect(qubitron.SWAP ** sympy.Symbol('foo'))


def test_swap_unitary() -> None:
    # yapf: disable
    np.testing.assert_almost_equal(
        qubitron.unitary(qubitron.SWAP**0.5),
        np.array([
            [1, 0, 0, 0],
            [0, 0.5 + 0.5j, 0.5 - 0.5j, 0],
            [0, 0.5 - 0.5j, 0.5 + 0.5j, 0],
            [0, 0, 0, 1]
        ]))
    # yapf: enable


def test_iswap_unitary() -> None:
    # yapf: disable
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(qubitron.ISWAP),
        # Reference for the iswap gate's matrix using +i instead of -i:
        # https://quantumcomputing.stackexchange.com/questions/2594/
        np.array([[1, 0, 0, 0],
                   [0, 0, 1j, 0],
                   [0, 1j, 0, 0],
                   [0, 0, 0, 1]]),
        atol=1e-8)
    # yapf: enable


def test_iswap_inv_unitary() -> None:
    # yapf: disable
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(qubitron.ISWAP_INV),
        # Reference for the iswap gate's matrix using +i instead of -i:
        # https://quantumcomputing.stackexchange.com/questions/2594/
        np.array([[1, 0, 0, 0],
                  [0, 0, -1j, 0],
                  [0, -1j, 0, 0],
                  [0, 0, 0, 1]]),
        atol=1e-8)
    # yapf: enable


def test_sqrt_iswap_unitary() -> None:
    # yapf: disable
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(qubitron.SQRT_ISWAP),
        # Reference for the sqrt-iSWAP gate's matrix:
        # https://arxiv.org/abs/2105.06074
        np.array([[1, 0,         0,         0],
                  [0, 1/2**0.5,  1j/2**0.5, 0],
                  [0, 1j/2**0.5, 1/2**0.5,  0],
                  [0, 0,         0,         1]]),
        atol=1e-8)
    # yapf: enable


def test_sqrt_iswap_inv_unitary() -> None:
    # yapf: disable
    qubitron.testing.assert_allclose_up_to_global_phase(
        qubitron.unitary(qubitron.SQRT_ISWAP_INV),
        # Reference for the inv-sqrt-iSWAP gate's matrix:
        # https://arxiv.org/abs/2105.06074
        np.array([[1, 0,          0,          0],
                  [0, 1/2**0.5,   -1j/2**0.5, 0],
                  [0, -1j/2**0.5, 1/2**0.5,   0],
                  [0, 0,          0,          1]]),
        atol=1e-8)
    # yapf: enable


def test_repr() -> None:
    assert repr(qubitron.SWAP) == 'qubitron.SWAP'
    assert repr(qubitron.SWAP**0.5) == '(qubitron.SWAP**0.5)'

    assert repr(qubitron.ISWAP) == 'qubitron.ISWAP'
    assert repr(qubitron.ISWAP**0.5) == '(qubitron.ISWAP**0.5)'

    assert repr(qubitron.ISWAP_INV) == 'qubitron.ISWAP_INV'
    assert repr(qubitron.ISWAP_INV**0.5) == '(qubitron.ISWAP**-0.5)'


def test_str() -> None:
    assert str(qubitron.SWAP) == 'SWAP'
    assert str(qubitron.SWAP**0.5) == 'SWAP**0.5'

    assert str(qubitron.ISWAP) == 'ISWAP'
    assert str(qubitron.ISWAP**0.5) == 'ISWAP**0.5'

    assert str(qubitron.ISWAP_INV) == 'ISWAP_INV'
    assert str(qubitron.ISWAP_INV**0.5) == 'ISWAP**-0.5'


def test_iswap_decompose_diagram() -> None:
    a = qubitron.NamedQubit('a')
    b = qubitron.NamedQubit('b')

    decomposed = qubitron.Circuit(qubitron.decompose_once(qubitron.ISWAP(a, b) ** 0.5))
    qubitron.testing.assert_has_diagram(
        decomposed,
        """
a: ───@───H───X───T───X───T^-1───H───@───
      │       │       │              │
b: ───X───────@───────@──────────────X───
""",
    )


def test_trace_distance() -> None:
    foo = sympy.Symbol('foo')
    sswap = qubitron.SWAP**foo
    siswap = qubitron.ISWAP**foo
    # These values should have 1.0 or 0.0 directly returned
    assert qubitron.trace_distance_bound(sswap) == 1.0
    assert qubitron.trace_distance_bound(siswap) == 1.0
    # These values are calculated, so we use approx_eq
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.SWAP**0.3), np.sin(0.3 * np.pi / 2))
    assert qubitron.approx_eq(qubitron.trace_distance_bound(qubitron.ISWAP**0), 0.0)


def test_trace_distance_over_range_of_exponents() -> None:
    for exp in np.linspace(0, 4, 20):
        qubitron.testing.assert_has_consistent_trace_distance_bound(qubitron.SWAP**exp)
        qubitron.testing.assert_has_consistent_trace_distance_bound(qubitron.ISWAP**exp)


@pytest.mark.parametrize('angle_rads', (-np.pi, -np.pi / 3, -0.1, np.pi / 5))
def test_riswap_unitary(angle_rads) -> None:
    actual = qubitron.unitary(qubitron.riswap(angle_rads))
    c = np.cos(angle_rads)
    s = 1j * np.sin(angle_rads)
    # yapf: disable
    expected = np.array([[1, 0, 0, 0],
                         [0, c, s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]])
    # yapf: enable
    assert np.allclose(actual, expected)


@pytest.mark.parametrize('angle_rads', (-2 * np.pi / 3, -0.2, 0.4, np.pi / 4))
def test_riswap_hamiltonian(angle_rads) -> None:
    actual = qubitron.unitary(qubitron.riswap(angle_rads))
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    xx = np.kron(x, x)
    yy = np.kron(y, y)
    expected = linalg.expm(+0.5j * angle_rads * (xx + yy))
    assert np.allclose(actual, expected)


@pytest.mark.parametrize('angle_rads', (-np.pi / 5, 0.4, 2, np.pi))
def test_riswap_has_consistent_protocols(angle_rads) -> None:
    qubitron.testing.assert_implements_consistent_protocols(qubitron.riswap(angle_rads))
