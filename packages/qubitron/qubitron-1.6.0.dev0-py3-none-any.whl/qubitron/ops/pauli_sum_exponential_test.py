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

import qubitron
import qubitron.testing

q0, q1, q2, q3 = qubitron.LineQubit.range(4)


def test_raises_for_non_commuting_paulis() -> None:
    with pytest.raises(ValueError, match='commuting'):
        qubitron.PauliSumExponential(qubitron.X(q0) + qubitron.Z(q0), np.pi / 2)


def test_raises_for_non_hermitian_pauli() -> None:
    with pytest.raises(ValueError, match='hermitian'):
        qubitron.PauliSumExponential(qubitron.X(q0) + 1j * qubitron.Z(q1), np.pi / 2)


@pytest.mark.parametrize(
    'psum_exp, expected_qubits',
    (
        (qubitron.PauliSumExponential(qubitron.Z(q1), np.pi / 2), (q1,)),
        (
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Y(q2), sympy.Symbol("theta")),
            (q0, q2),
        ),
        (
            qubitron.PauliSumExponential(qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q2) * qubitron.Z(q3), np.pi),
            (q0, q1, q2, q3),
        ),
    ),
)
def test_pauli_sum_exponential_qubits(psum_exp, expected_qubits) -> None:
    assert psum_exp.qubits == expected_qubits


@pytest.mark.parametrize(
    'psum_exp, expected_psum_exp',
    (
        (
            qubitron.PauliSumExponential(qubitron.Z(q0), np.pi / 2),
            qubitron.PauliSumExponential(qubitron.Z(q1), np.pi / 2),
        ),
        (
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Y(q2), sympy.Symbol("theta")),
            qubitron.PauliSumExponential(2j * qubitron.X(q1) + 3j * qubitron.Y(q3), sympy.Symbol("theta")),
        ),
        (
            qubitron.PauliSumExponential(qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q1) * qubitron.Z(q3), np.pi),
            qubitron.PauliSumExponential(qubitron.X(q1) * qubitron.Y(q2) + qubitron.Y(q2) * qubitron.Z(q3), np.pi),
        ),
    ),
)
def test_pauli_sum_exponential_with_qubits(psum_exp, expected_psum_exp) -> None:
    assert psum_exp.with_qubits(*expected_psum_exp.qubits) == expected_psum_exp


@pytest.mark.parametrize(
    'psum, exp',
    (
        (qubitron.Z(q0), np.pi / 2),
        (2 * qubitron.X(q0) + 3 * qubitron.Y(q2), 1),
        (qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q1) * qubitron.Z(q3), np.pi),
    ),
)
def test_with_parameters_resolved_by(psum, exp) -> None:
    psum_exp = qubitron.PauliSumExponential(psum, sympy.Symbol("theta"))
    resolver = qubitron.ParamResolver({"theta": exp})
    actual = qubitron.resolve_parameters(psum_exp, resolver)
    expected = qubitron.PauliSumExponential(psum, exp)
    assert actual == expected


def test_pauli_sum_exponential_parameterized_matrix_raises() -> None:
    with pytest.raises(ValueError, match='parameterized'):
        qubitron.PauliSumExponential(qubitron.X(q0) + qubitron.Z(q1), sympy.Symbol("theta")).matrix()


@pytest.mark.parametrize(
    'psum_exp, expected_unitary',
    (
        (qubitron.PauliSumExponential(qubitron.X(q0), np.pi / 2), np.array([[0, 1j], [1j, 0]])),
        (
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Z(q1), np.pi / 2),
            np.array([[1j, 0, 0, 0], [0, -1j, 0, 0], [0, 0, 1j, 0], [0, 0, 0, -1j]]),
        ),
    ),
)
def test_pauli_sum_exponential_has_correct_unitary(psum_exp, expected_unitary) -> None:
    assert qubitron.has_unitary(psum_exp)
    assert np.allclose(qubitron.unitary(psum_exp), expected_unitary)


@pytest.mark.parametrize(
    'psum_exp, power, expected_psum',
    (
        (
            qubitron.PauliSumExponential(qubitron.Z(q1), np.pi / 2),
            5,
            qubitron.PauliSumExponential(qubitron.Z(q1), 5 * np.pi / 2),
        ),
        (
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Y(q2), sympy.Symbol("theta")),
            5,
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Y(q2), 5 * sympy.Symbol("theta")),
        ),
        (
            qubitron.PauliSumExponential(qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q2) * qubitron.Z(q3), np.pi),
            5,
            qubitron.PauliSumExponential(qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q2) * qubitron.Z(q3), 5 * np.pi),
        ),
    ),
)
def test_pauli_sum_exponential_pow(psum_exp, power, expected_psum) -> None:
    assert psum_exp**power == expected_psum


@pytest.mark.parametrize(
    'psum_exp',
    (
        (qubitron.PauliSumExponential(0, np.pi / 2)),
        (qubitron.PauliSumExponential(2j * qubitron.X(q0) + 3j * qubitron.Z(q1), np.pi / 2)),
    ),
)
def test_pauli_sum_exponential_repr(psum_exp) -> None:
    qubitron.testing.assert_equivalent_repr(psum_exp)


@pytest.mark.parametrize(
    'psum_exp, expected_str',
    (
        (qubitron.PauliSumExponential(0, np.pi / 2), 'exp(j * 1.5707963267948966 * (0.000))'),
        (
            qubitron.PauliSumExponential(2j * qubitron.X(q0) + 4j * qubitron.Y(q1), 2),
            'exp(2 * (2.000j*X(q(0))+4.000j*Y(q(1))))',
        ),
        (
            qubitron.PauliSumExponential(0.5 * qubitron.X(q0) + 0.6 * qubitron.Y(q1), sympy.Symbol("theta")),
            'exp(j * theta * (0.500*X(q(0))+0.600*Y(q(1))))',
        ),
    ),
)
def test_pauli_sum_exponential_formatting(psum_exp, expected_str) -> None:
    assert str(psum_exp) == expected_str
