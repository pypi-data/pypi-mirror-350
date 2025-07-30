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

import collections

import numpy as np
import pytest
import sympy
import sympy.parsing.sympy_parser as sympy_parser

import qubitron
import qubitron.testing

_ = 0.0  # Make matrices readable by visually hiding off-diagonal elements.
q0, q1, q2, q3 = qubitron.LineQubit.range(4)


@pytest.mark.parametrize(
    'terms',
    (
        {qubitron.X: -2, qubitron.H: 2},
        {qubitron.XX: 1, qubitron.YY: 1j, qubitron.ZZ: -1},
        {qubitron.TOFFOLI: 0.5j, qubitron.FREDKIN: 0.5},
    ),
)
def test_linear_combination_of_gates_accepts_consistent_gates(terms):
    combination_1 = qubitron.LinearCombinationOfGates(terms)

    combination_2 = qubitron.LinearCombinationOfGates({})
    combination_2.update(terms)

    combination_3 = qubitron.LinearCombinationOfGates({})
    for gate, coefficient in terms.items():
        combination_3[gate] += coefficient

    assert combination_1 == combination_2 == combination_3


@pytest.mark.parametrize(
    'terms',
    (
        {qubitron.X: -2, qubitron.CZ: 2},
        {qubitron.X: 1, qubitron.YY: 1j, qubitron.ZZ: -1},
        {qubitron.TOFFOLI: 0.5j, qubitron.S: 0.5},
    ),
)
def test_linear_combination_of_gates_rejects_inconsistent_gates(terms):
    with pytest.raises(ValueError):
        qubitron.LinearCombinationOfGates(terms)

    combination = qubitron.LinearCombinationOfGates({})
    with pytest.raises(ValueError):
        combination.update(terms)

    combination = qubitron.LinearCombinationOfGates({})
    with pytest.raises(ValueError):
        for gate, coefficient in terms.items():
            combination[gate] += coefficient


@pytest.mark.parametrize('gate', (qubitron.X, qubitron.Y, qubitron.XX, qubitron.CZ, qubitron.CSWAP, qubitron.FREDKIN))
def test_empty_linear_combination_of_gates_accepts_all_gates(gate):
    combination = qubitron.LinearCombinationOfGates({})
    combination[gate] = -0.5j
    assert len(combination) == 1


@pytest.mark.parametrize(
    'terms, expected_num_qubits',
    (
        ({qubitron.X: 1}, 1),
        ({qubitron.H: 10, qubitron.S: -10j}, 1),
        ({qubitron.XX: 1, qubitron.YY: 2, qubitron.ZZ: 3}, 2),
        ({qubitron.CCZ: 0.1, qubitron.CSWAP: 0.2}, 3),
    ),
)
def test_linear_combination_of_gates_has_correct_num_qubits(terms, expected_num_qubits):
    combination = qubitron.LinearCombinationOfGates(terms)
    assert combination.num_qubits() == expected_num_qubits


def test_empty_linear_combination_of_gates_has_no_matrix():
    empty = qubitron.LinearCombinationOfGates({})
    assert empty.num_qubits() is None
    with pytest.raises(ValueError):
        empty.matrix()


@pytest.mark.parametrize(
    'terms, expected_matrix',
    (
        (
            {qubitron.I: 2, qubitron.X: 3, qubitron.Y: 4, qubitron.Z: 5j},
            np.array([[2 + 5j, 3 - 4j], [3 + 4j, 2 - 5j]]),
        ),
        ({qubitron.XX: 0.5, qubitron.YY: -0.5}, np.rot90(np.diag([1, 0, 0, 1]))),
        ({qubitron.CCZ: 3j}, np.diag([3j, 3j, 3j, 3j, 3j, 3j, 3j, -3j])),
    ),
)
def test_linear_combination_of_gates_has_correct_matrix(terms, expected_matrix):
    combination = qubitron.LinearCombinationOfGates(terms)
    assert np.all(combination.matrix() == expected_matrix)


@pytest.mark.parametrize(
    'terms, expected_unitary',
    (
        (
            {qubitron.X: np.sqrt(0.5), qubitron.Y: np.sqrt(0.5)},
            np.array([[0, np.sqrt(-1j)], [np.sqrt(1j), 0]]),
        ),
        (
            {qubitron.IdentityGate(2): np.sqrt(0.5), qubitron.YY: -1j * np.sqrt(0.5)},
            np.sqrt(0.5) * np.array([[1, 0, 0, 1j], [0, 1, -1j, 0], [0, -1j, 1, 0], [1j, 0, 0, 1]]),
        ),
    ),
)
def test_unitary_linear_combination_of_gates_has_correct_unitary(terms, expected_unitary):
    combination = qubitron.LinearCombinationOfGates(terms)
    assert qubitron.has_unitary(combination)
    assert np.allclose(qubitron.unitary(combination), expected_unitary)


@pytest.mark.parametrize(
    'terms', ({qubitron.X: 2}, {qubitron.Y ** sympy.Symbol('t'): 1}, {qubitron.X: 1, qubitron.S: 1})
)
def test_non_unitary_linear_combination_of_gates_has_no_unitary(terms):
    combination = qubitron.LinearCombinationOfGates(terms)
    assert not qubitron.has_unitary(combination)
    with pytest.raises((TypeError, ValueError)):
        _ = qubitron.unitary(combination)


@pytest.mark.parametrize(
    'terms, expected_expansion',
    (
        ({qubitron.X: 10, qubitron.Y: -20}, {'X': 10, 'Y': -20}),
        (
            {qubitron.Y: np.sqrt(0.5), qubitron.H: 1},
            {'X': np.sqrt(0.5), 'Y': np.sqrt(0.5), 'Z': np.sqrt(0.5)},
        ),
        ({qubitron.X: 2, qubitron.H: 1}, {'X': 2 + np.sqrt(0.5), 'Z': np.sqrt(0.5)}),
        ({qubitron.XX: -2, qubitron.YY: 3j, qubitron.ZZ: 4}, {'XX': -2, 'YY': 3j, 'ZZ': 4}),
        (
            {qubitron.X: sympy.Symbol('x'), qubitron.Y: -sympy.Symbol('y')},
            {'X': sympy.Symbol('x'), 'Y': -sympy.Symbol('y')},
        ),
    ),
)
def test_linear_combination_of_gates_has_correct_pauli_expansion(terms, expected_expansion):
    combination = qubitron.LinearCombinationOfGates(terms)
    actual_expansion = qubitron.pauli_expansion(combination)
    assert set(actual_expansion.keys()) == set(expected_expansion.keys())
    for name in actual_expansion.keys():
        assert abs(actual_expansion[name] - expected_expansion[name]) < 1e-12


@pytest.mark.parametrize(
    'terms, exponent, expected_terms',
    (
        ({qubitron.X: 1}, 2, {qubitron.I: 1}),
        ({qubitron.X: 1}, 3, {qubitron.X: 1}),
        ({qubitron.Y: 0.5}, 10, {qubitron.I: 2**-10}),
        ({qubitron.Y: 0.5}, 11, {qubitron.Y: 2**-11}),
        (
            {qubitron.I: 1, qubitron.X: 2, qubitron.Y: 3, qubitron.Z: 4},
            2,
            {qubitron.I: 30, qubitron.X: 4, qubitron.Y: 6, qubitron.Z: 8},
        ),
        ({qubitron.X: 1, qubitron.Y: 1j}, 2, {}),
        ({qubitron.X: 0.4, qubitron.Y: 0.4}, 0, {qubitron.I: 1}),
    ),
)
def test_linear_combinations_of_gates_valid_powers(terms, exponent, expected_terms):
    combination = qubitron.LinearCombinationOfGates(terms)
    actual_result = combination**exponent
    expected_result = qubitron.LinearCombinationOfGates(expected_terms)
    assert qubitron.approx_eq(actual_result, expected_result)
    assert len(actual_result) == len(expected_terms)


@pytest.mark.parametrize(
    'terms, exponent',
    (
        ({}, 2),
        ({qubitron.H: 1}, 2),
        ({qubitron.CNOT: 2}, 2),
        ({qubitron.X: 1, qubitron.S: -1}, 2),
        ({qubitron.X: 1}, -1),
        ({qubitron.Y: 1}, sympy.Symbol('k')),
    ),
)
def test_linear_combinations_of_gates_invalid_powers(terms, exponent):
    combination = qubitron.LinearCombinationOfGates(terms)
    with pytest.raises(TypeError):
        _ = combination**exponent


@pytest.mark.parametrize(
    'terms, is_parameterized, parameter_names',
    [
        ({qubitron.H: 1}, False, set()),
        ({qubitron.X ** sympy.Symbol('t'): 1}, True, {'t'}),
        ({qubitron.X: sympy.Symbol('t')}, True, {'t'}),
    ],
)
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterized_linear_combination_of_gates(
    terms, is_parameterized, parameter_names, resolve_fn
):
    gate = qubitron.LinearCombinationOfGates(terms)
    assert qubitron.is_parameterized(gate) == is_parameterized
    assert qubitron.parameter_names(gate) == parameter_names
    resolved = resolve_fn(gate, {p: 1 for p in parameter_names})
    assert not qubitron.is_parameterized(resolved)


def get_matrix(
    operator: (
        qubitron.Gate
        | qubitron.GateOperation
        | qubitron.LinearCombinationOfGates
        | qubitron.LinearCombinationOfOperations
    ),
) -> np.ndarray:
    if isinstance(operator, (qubitron.LinearCombinationOfGates, qubitron.LinearCombinationOfOperations)):
        return operator.matrix()
    return qubitron.unitary(operator)


def assert_linear_combinations_are_equal(
    actual: qubitron.LinearCombinationOfGates | qubitron.LinearCombinationOfOperations,
    expected: qubitron.LinearCombinationOfGates | qubitron.LinearCombinationOfOperations,
) -> None:
    if not actual and not expected:
        assert len(actual) == 0
        assert len(expected) == 0
        return

    actual_matrix = get_matrix(actual)
    expected_matrix = get_matrix(expected)
    assert qubitron.approx_eq(actual_matrix, expected_matrix)

    actual_expansion = qubitron.pauli_expansion(actual)
    expected_expansion = qubitron.pauli_expansion(expected)
    assert set(actual_expansion.keys()) == set(expected_expansion.keys())
    for name in actual_expansion.keys():
        assert qubitron.approx_eq(actual_expansion[name], expected_expansion[name])


@pytest.mark.parametrize(
    'expression, expected_result',
    (
        ((qubitron.X + qubitron.Z) / np.sqrt(2), qubitron.H),
        (qubitron.X - qubitron.Y, -qubitron.Y + qubitron.X),
        (qubitron.X + qubitron.S - qubitron.X, qubitron.S),
        (qubitron.Y - 2 * qubitron.Y, -qubitron.Y),
        (qubitron.rx(0.2), np.cos(0.1) * qubitron.I - 1j * np.sin(0.1) * qubitron.X),
        (1j * qubitron.H * 1j, -qubitron.H),
        (-1j * qubitron.Y, qubitron.ry(np.pi)),
        (np.sqrt(-1j) * qubitron.S, qubitron.rz(np.pi / 2)),
        (0.5 * (qubitron.IdentityGate(2) + qubitron.XX + qubitron.YY + qubitron.ZZ), qubitron.SWAP),
        ((qubitron.IdentityGate(2) + 1j * (qubitron.XX + qubitron.YY) + qubitron.ZZ) / 2, qubitron.ISWAP),
        (qubitron.CNOT + 0 * qubitron.SWAP, qubitron.CNOT),
        (0.5 * qubitron.FREDKIN, qubitron.FREDKIN / 2),
        (qubitron.FREDKIN * 0.5, qubitron.FREDKIN / 2),
        (((qubitron.X + qubitron.Y) / np.sqrt(2)) ** 2, qubitron.I),
        ((qubitron.X + qubitron.Z) ** 3, 2 * (qubitron.X + qubitron.Z)),
        ((qubitron.X + 1j * qubitron.Y) ** 2, qubitron.LinearCombinationOfGates({})),
        ((qubitron.X - 1j * qubitron.Y) ** 2, qubitron.LinearCombinationOfGates({})),
        (((3 * qubitron.X - 4 * qubitron.Y + 12 * qubitron.Z) / 13) ** 24, qubitron.I),
        (
            ((3 * qubitron.X - 4 * qubitron.Y + 12 * qubitron.Z) / 13) ** 25,
            (3 * qubitron.X - 4 * qubitron.Y + 12 * qubitron.Z) / 13,
        ),
        ((qubitron.X + qubitron.Y + qubitron.Z) ** 0, qubitron.I),
        ((qubitron.X - 1j * qubitron.Y) ** 0, qubitron.I),
        (qubitron.Y - sympy.Symbol('s') * qubitron.Y, (1 - sympy.Symbol('s')) * qubitron.Y),
        ((qubitron.X + qubitron.Z) * sympy.Symbol('s') / np.sqrt(2), qubitron.H * sympy.Symbol('s')),
    ),
)
def test_gate_expressions(expression, expected_result):
    assert_linear_combinations_are_equal(expression, expected_result)


@pytest.mark.parametrize(
    'gates',
    (
        (qubitron.X, qubitron.T, qubitron.T, qubitron.X, qubitron.Z),
        (qubitron.CZ, qubitron.XX, qubitron.YY, qubitron.ZZ),
        (qubitron.TOFFOLI, qubitron.TOFFOLI, qubitron.FREDKIN),
    ),
)
def test_in_place_manipulations_of_linear_combination_of_gates(gates):
    a = qubitron.LinearCombinationOfGates({})
    b = qubitron.LinearCombinationOfGates({})

    for i, gate in enumerate(gates):
        a += gate
        b -= gate

        prefix = gates[: i + 1]
        expected_a = qubitron.LinearCombinationOfGates(collections.Counter(prefix))
        expected_b = -expected_a

        assert_linear_combinations_are_equal(a, expected_a)
        assert_linear_combinations_are_equal(b, expected_b)


@pytest.mark.parametrize(
    'op',
    (
        qubitron.X(q0),
        qubitron.Y(q1),
        qubitron.XX(q0, q1),
        qubitron.CZ(q0, q1),
        qubitron.FREDKIN(q0, q1, q2),
        qubitron.ControlledOperation((q0, q1), qubitron.H(q2)),
        qubitron.ParallelGate(qubitron.X, 3).on(q0, q1, q2),
        qubitron.PauliString({q0: qubitron.X, q1: qubitron.Y, q2: qubitron.Z}),
    ),
)
def test_empty_linear_combination_of_operations_accepts_all_operations(op):
    combination = qubitron.LinearCombinationOfOperations({})
    combination[op] = -0.5j
    assert len(combination) == 1


@pytest.mark.parametrize(
    'terms',
    (
        {qubitron.X(q0): -2, qubitron.H(q0): 2},
        {qubitron.X(q0): -2, qubitron.H(q1): 2j},
        {qubitron.X(q0): 1, qubitron.CZ(q0, q1): 3},
        {qubitron.X(q0): 1 + 1j, qubitron.CZ(q1, q2): 0.5},
    ),
)
def test_linear_combination_of_operations_is_consistent(terms):
    combination_1 = qubitron.LinearCombinationOfOperations(terms)

    combination_2 = qubitron.LinearCombinationOfOperations({})
    combination_2.update(terms)

    combination_3 = qubitron.LinearCombinationOfOperations({})
    for gate, coefficient in terms.items():
        combination_3[gate] += coefficient

    assert combination_1 == combination_2 == combination_3


@pytest.mark.parametrize(
    'terms, expected_qubits',
    (
        ({}, ()),
        ({qubitron.I(q0): 1, qubitron.H(q0): 1e-3j}, (q0,)),
        ({qubitron.X(q0): 1j, qubitron.H(q1): 2j}, (q0, q1)),
        ({qubitron.Y(q0): -1, qubitron.CZ(q0, q1): 3e3}, (q0, q1)),
        ({qubitron.Z(q0): -1j, qubitron.CNOT(q1, q2): 0.25}, (q0, q1, q2)),
    ),
)
def test_linear_combination_of_operations_has_correct_qubits(terms, expected_qubits):
    combination = qubitron.LinearCombinationOfOperations(terms)
    assert combination.qubits == expected_qubits


@pytest.mark.parametrize(
    'terms, expected_matrix',
    (
        ({}, np.array([0])),
        (
            {qubitron.I(q0): 2, qubitron.X(q0): 3, qubitron.Y(q0): 4, qubitron.Z(q0): 5j},
            # fmt: off
            np.array(
                [
                    [2 + 5j, 3 - 4j],
                    [3 + 4j, 2 - 5j],
                ]
            ),
            # fmt: on
        ),
        (
            {qubitron.X(q0): 2, qubitron.Y(q1): 3},
            # fmt: off
            np.array(
                [
                    [0, -3j, 2, 0],
                    [3j, 0, 0, 2],
                    [2, 0, 0, -3j],
                    [0, 2, 3j, 0],
                ]
            ),
            # fmt: on
        ),
        ({qubitron.XX(q0, q1): 0.5, qubitron.YY(q0, q1): -0.5}, np.rot90(np.diag([1, 0, 0, 1]))),
        ({qubitron.CCZ(q0, q1, q2): 3j}, np.diag([3j, 3j, 3j, 3j, 3j, 3j, 3j, -3j])),
        (
            {qubitron.I(q0): 0.1, qubitron.CNOT(q1, q2): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 0.1, 1, _, _, _, _],
                    [_, _, 1, 0.1, _, _, _, _],
                    [_, _, _, _, 1.1, _, _, _],
                    [_, _, _, _, _, 1.1, _, _],
                    [_, _, _, _, _, _, 0.1, 1],
                    [_, _, _, _, _, _, 1, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q1): 0.1, qubitron.CNOT(q0, q2): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, 0.1, 1, _, _],
                    [_, _, _, _, 1, 0.1, _, _],
                    [_, _, _, _, _, _, 0.1, 1],
                    [_, _, _, _, _, _, 1, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q2): 0.1, qubitron.CNOT(q0, q1): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, 0.1, _, 1, _],
                    [_, _, _, _, _, 0.1, _, 1],
                    [_, _, _, _, 1, _, 0.1, _],
                    [_, _, _, _, _, 1, _, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q0): 0.1, qubitron.ControlledGate(qubitron.Y).on(q1, q2): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 0.1, -1j, _, _, _, _],
                    [_, _, 1j, 0.1, _, _, _, _],
                    [_, _, _, _, 1.1, _, _, _],
                    [_, _, _, _, _, 1.1, _, _],
                    [_, _, _, _, _, _, 0.1, -1j],
                    [_, _, _, _, _, _, 1j, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q1): 0.1, qubitron.ControlledGate(qubitron.Y).on(q0, q2): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, 0.1, -1j, _, _],
                    [_, _, _, _, 1j, 0.1, _, _],
                    [_, _, _, _, _, _, 0.1, -1j],
                    [_, _, _, _, _, _, 1j, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q2): 0.1, qubitron.ControlledGate(qubitron.Y).on(q0, q1): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, 0.1, _, -1j, _],
                    [_, _, _, _, _, 0.1, _, -1j],
                    [_, _, _, _, 1j, _, 0.1, _],
                    [_, _, _, _, _, 1j, _, 0.1],
                ]
            ),
        ),
        (
            {qubitron.I(q0): 0.1, qubitron.FREDKIN(q1, q2, q3): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, 0.1, 1, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, 1, 0.1, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, 1.1, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, 1.1, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, 1.1, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, 0.1, 1, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, 1, 0.1, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1.1],
                ]
            ),
        ),
        (
            {qubitron.I(q1): 0.1, qubitron.FREDKIN(q0, q2, q3): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, 1.1, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, 1.1, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, 0.1, 1, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, 1, 0.1, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 1.1, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, 1.1, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, 0.1, 1, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, 1, 0.1, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1.1],
                ]
            ),
        ),
        (
            {qubitron.I(q2): 0.1, qubitron.FREDKIN(q0, q1, q3): 1},
            np.array(
                [
                    [1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, 1.1, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, 1.1, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, 1.1, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, 1.1, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, 0.1, _, _, 1, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, 1.1, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 0.1, _, _, 1, _],
                    [_, _, _, _, _, _, _, _, _, 1, _, _, 0.1, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, 0, 1.1, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 1, _, _, 0.1, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1.1],
                ]
            ),
        ),
        (
            {qubitron.I(q3): 2j, qubitron.FREDKIN(q0, q1, q2): 1j},
            np.array(
                [
                    [3j, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, 3j, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, 3j, _, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, 3j, _, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, 3j, _, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, 3j, _, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, 3j, _, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, 3j, _, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, 3j, _, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, 3j, _, _, _, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, 2j, _, 1j, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 2j, _, 1j, _, _],
                    [_, _, _, _, _, _, _, _, _, _, 1j, _, 2j, _, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, 1j, _, 2j, _, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, 3j, _],
                    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3j],
                ]
            ),
        ),
    ),
)
def test_linear_combination_of_operations_has_correct_matrix(terms, expected_matrix):
    combination = qubitron.LinearCombinationOfOperations(terms)
    assert np.allclose(combination.matrix(), expected_matrix)


@pytest.mark.parametrize(
    'terms, expected_unitary',
    (
        (
            {qubitron.X(q0): np.sqrt(0.5), qubitron.Z(q0): np.sqrt(0.5)},
            np.sqrt(0.5) * np.array([[1, 1], [1, -1]]),
        ),
        (
            {
                qubitron.IdentityGate(3).on(q0, q1, q2): np.sqrt(0.5),
                qubitron.CCZ(q0, q1, q2): 1j * np.sqrt(0.5),
            },
            np.diag(
                [
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(1j),
                    np.sqrt(-1j),
                ]
            ),
        ),
    ),
)
def test_unitary_linear_combination_of_operations_has_correct_unitary(terms, expected_unitary):
    combination = qubitron.LinearCombinationOfOperations(terms)
    assert qubitron.has_unitary(combination)
    assert np.allclose(qubitron.unitary(combination), expected_unitary)


@pytest.mark.parametrize(
    'terms',
    (
        {qubitron.CNOT(q0, q1): 1.1},
        {qubitron.CZ(q0, q1) ** sympy.Symbol('t'): 1},
        {qubitron.X(q0): 1, qubitron.S(q0): 1},
    ),
)
def test_non_unitary_linear_combination_of_operations_has_no_unitary(terms):
    combination = qubitron.LinearCombinationOfOperations(terms)
    assert not qubitron.has_unitary(combination)
    with pytest.raises((TypeError, ValueError)):
        _ = qubitron.unitary(combination)


@pytest.mark.parametrize(
    'terms, expected_expansion',
    (
        ({}, {}),
        ({qubitron.X(q0): -10, qubitron.Y(q0): 20}, {'X': -10, 'Y': 20}),
        ({qubitron.X(q0): -10, qubitron.Y(q1): 20}, {'XI': -10, 'IY': 20}),
        (
            {qubitron.Y(q0): np.sqrt(0.5), qubitron.H(q0): 1},
            {'X': np.sqrt(0.5), 'Y': np.sqrt(0.5), 'Z': np.sqrt(0.5)},
        ),
        (
            {qubitron.Y(q0): np.sqrt(0.5), qubitron.H(q2): 1},
            {'IX': np.sqrt(0.5), 'YI': np.sqrt(0.5), 'IZ': np.sqrt(0.5)},
        ),
        (
            {qubitron.XX(q0, q1): -2, qubitron.YY(q0, q1): 3j, qubitron.ZZ(q0, q1): 4},
            {'XX': -2, 'YY': 3j, 'ZZ': 4},
        ),
        (
            {qubitron.XX(q0, q1): -2, qubitron.YY(q0, q2): 3j, qubitron.ZZ(q1, q2): 4},
            {'XXI': -2, 'YIY': 3j, 'IZZ': 4},
        ),
        (
            {qubitron.IdentityGate(2).on(q0, q3): -1, qubitron.CZ(q1, q2): 2},
            {'IIZI': 1, 'IZII': 1, 'IZZI': -1},
        ),
        ({qubitron.CNOT(q0, q1): 2, qubitron.Z(q0): -1, qubitron.X(q1): -1}, {'II': 1, 'ZX': -1}),
        (
            {qubitron.X(q0): -sympy.Symbol('x'), qubitron.Y(q0): sympy.Symbol('y')},
            {'X': -sympy.Symbol('x'), 'Y': sympy.Symbol('y')},
        ),
    ),
)
def test_linear_combination_of_operations_has_correct_pauli_expansion(terms, expected_expansion):
    combination = qubitron.LinearCombinationOfOperations(terms)
    actual_expansion = qubitron.pauli_expansion(combination)
    assert set(actual_expansion.keys()) == set(expected_expansion.keys())
    for name in actual_expansion.keys():
        assert abs(actual_expansion[name] - expected_expansion[name]) < 1e-12


@pytest.mark.parametrize(
    'terms, exponent, expected_terms',
    (
        ({qubitron.X(q0): 1}, 2, {qubitron.I(q0): 1}),
        ({qubitron.X(q0): 1}, 3, {qubitron.X(q0): 1}),
        ({qubitron.Y(q0): 0.5}, 10, {qubitron.I(q0): 2**-10}),
        ({qubitron.Y(q0): 0.5}, 11, {qubitron.Y(q0): 2**-11}),
        (
            {qubitron.I(q0): 1, qubitron.X(q0): 2, qubitron.Y(q0): 3, qubitron.Z(q0): 4},
            2,
            {qubitron.I(q0): 30, qubitron.X(q0): 4, qubitron.Y(q0): 6, qubitron.Z(q0): 8},
        ),
        ({qubitron.X(q0): 1, qubitron.Y(q0): 1j}, 2, {}),
        ({qubitron.Y(q1): 2, qubitron.Z(q1): 3}, 0, {qubitron.I(q1): 1}),
    ),
)
def test_linear_combinations_of_operations_valid_powers(terms, exponent, expected_terms):
    combination = qubitron.LinearCombinationOfOperations(terms)
    actual_result = combination**exponent
    expected_result = qubitron.LinearCombinationOfOperations(expected_terms)
    assert qubitron.approx_eq(actual_result, expected_result)
    assert len(actual_result) == len(expected_terms)


@pytest.mark.parametrize(
    'terms, exponent',
    (
        ({}, 2),
        ({qubitron.H(q0): 1}, 2),
        ({qubitron.CNOT(q0, q1): 2}, 2),
        ({qubitron.X(q0): 1, qubitron.S(q0): -1}, 2),
        ({qubitron.X(q0): 1, qubitron.Y(q1): 1}, 2),
        ({qubitron.Z(q0): 1}, -1),
        ({qubitron.X(q0): 1}, sympy.Symbol('k')),
    ),
)
def test_linear_combinations_of_operations_invalid_powers(terms, exponent):
    combination = qubitron.LinearCombinationOfOperations(terms)
    with pytest.raises(TypeError):
        _ = combination**exponent


@pytest.mark.parametrize(
    'terms, is_parameterized, parameter_names',
    [
        ({qubitron.H(qubitron.LineQubit(0)): 1}, False, set()),
        ({qubitron.X(qubitron.LineQubit(0)) ** sympy.Symbol('t'): 1}, True, {'t'}),
        ({qubitron.X(qubitron.LineQubit(0)): sympy.Symbol('t')}, True, {'t'}),
    ],
)
@pytest.mark.parametrize('resolve_fn', [qubitron.resolve_parameters, qubitron.resolve_parameters_once])
def test_parameterized_linear_combination_of_ops(
    terms, is_parameterized, parameter_names, resolve_fn
):
    op = qubitron.LinearCombinationOfOperations(terms)
    assert qubitron.is_parameterized(op) == is_parameterized
    assert qubitron.parameter_names(op) == parameter_names
    resolved = resolve_fn(op, {p: 1 for p in parameter_names})
    assert not qubitron.is_parameterized(resolved)


@pytest.mark.parametrize(
    'expression, expected_result',
    (
        (
            qubitron.LinearCombinationOfOperations({qubitron.XX(q0, q1): 2}),
            qubitron.LinearCombinationOfOperations({qubitron.ParallelGate(qubitron.X, 2).on(q0, q1): 2}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.CNOT(q0, q1): 2}),
            qubitron.LinearCombinationOfOperations(
                {
                    qubitron.IdentityGate(2).on(q0, q1): 1,
                    qubitron.PauliString({q1: qubitron.X}): 1,
                    qubitron.PauliString({q0: qubitron.Z}): 1,
                    qubitron.PauliString({q0: qubitron.Z, q1: qubitron.X}): -1,
                }
            ),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): 1}) ** 2,
            qubitron.LinearCombinationOfOperations({qubitron.I(q0): 1}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): np.sqrt(0.5), qubitron.Y(q0): np.sqrt(0.5)})
            ** 2,
            qubitron.LinearCombinationOfOperations({qubitron.I(q0): 1}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): 1, qubitron.Z(q0): 1}) ** 3,
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): 2, qubitron.Z(q0): 2}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): 1j, qubitron.Y(q0): 1}) ** 2,
            qubitron.LinearCombinationOfOperations({}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): -1j, qubitron.Y(q0): 1}) ** 2,
            qubitron.LinearCombinationOfOperations({}),
        ),
        (
            qubitron.LinearCombinationOfOperations(
                {qubitron.X(q0): 3 / 13, qubitron.Y(q0): -4 / 13, qubitron.Z(q0): 12 / 13}
            )
            ** 24,
            qubitron.LinearCombinationOfOperations({qubitron.I(q0): 1}),
        ),
        (
            qubitron.LinearCombinationOfOperations(
                {qubitron.X(q0): 3 / 13, qubitron.Y(q0): -4 / 13, qubitron.Z(q0): 12 / 13}
            )
            ** 25,
            qubitron.LinearCombinationOfOperations(
                {qubitron.X(q0): 3 / 13, qubitron.Y(q0): -4 / 13, qubitron.Z(q0): 12 / 13}
            ),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q1): 2, qubitron.Z(q1): 3}) ** 0,
            qubitron.LinearCombinationOfOperations({qubitron.I(q1): 1}),
        ),
        (
            qubitron.LinearCombinationOfOperations({qubitron.X(q0): sympy.Symbol('s')}) ** 2,
            qubitron.LinearCombinationOfOperations({qubitron.I(q0): sympy.Symbol('s') ** 2}),
        ),
    ),
)
def test_operation_expressions(expression, expected_result):
    assert_linear_combinations_are_equal(expression, expected_result)


def test_pauli_sum_construction():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    psum = pstr1 + pstr2
    assert psum  # should be truthy
    assert list(psum) == [pstr1, pstr2]

    psum2 = qubitron.PauliSum.from_pauli_strings([pstr1, pstr2])
    assert psum == psum2

    zero = qubitron.PauliSum()
    assert len(zero) == 0


@pytest.mark.parametrize(
    'psum, expected_unitary',
    (
        (np.sqrt(0.5) * (qubitron.X(q0) + qubitron.Z(q0)), np.sqrt(0.5) * np.array([[1, 1], [1, -1]])),
        (
            np.sqrt(0.5) * (qubitron.X(q0) * qubitron.X(q1) + qubitron.Z(q1)),
            np.sqrt(0.5) * np.array([[1, 0, 0, 1], [0, -1, 1, 0], [0, 1, 1, 0], [1, 0, 0, -1]]),
        ),
    ),
)
def test_unitary_pauli_sum_has_correct_unitary(psum, expected_unitary):
    assert qubitron.has_unitary(psum)
    assert np.allclose(qubitron.unitary(psum), expected_unitary)


@pytest.mark.parametrize(
    'psum',
    (
        qubitron.X(q0) + qubitron.Z(q0),
        2 * qubitron.Z(q0) * qubitron.X(q1) + qubitron.Y(q2),
        qubitron.X(q0) * qubitron.Z(q1) - qubitron.Z(q1) * qubitron.X(q0),
    ),
)
def test_non_pauli_sum_has_no_unitary(psum):
    assert isinstance(psum, qubitron.PauliSum)
    assert not qubitron.has_unitary(psum)
    with pytest.raises(ValueError):
        _ = qubitron.unitary(psum)


@pytest.mark.parametrize(
    'psum, expected_qubits',
    (
        (qubitron.Z(q1), (q1,)),
        (qubitron.X(q0) + qubitron.Y(q0), (q0,)),
        (qubitron.X(q0) + qubitron.Y(q2), (q0, q2)),
        (qubitron.X(q2) + qubitron.Y(q0), (q0, q2)),
        (qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q1) * qubitron.Z(q3), (q0, q1, q3)),
    ),
)
def test_pauli_sum_qubits(psum, expected_qubits):
    assert psum.qubits == expected_qubits


@pytest.mark.parametrize(
    'psum, expected_psum',
    (
        (qubitron.Z(q0) + qubitron.Y(q0), qubitron.Z(q1) + qubitron.Y(q0)),
        (2 * qubitron.X(q0) + 3 * qubitron.Y(q2), 2 * qubitron.X(q1) + 3 * qubitron.Y(q3)),
        (
            qubitron.X(q0) * qubitron.Y(q1) + qubitron.Y(q1) * qubitron.Z(q3),
            qubitron.X(q1) * qubitron.Y(q2) + qubitron.Y(q2) * qubitron.Z(q3),
        ),
    ),
)
def test_pauli_sum_with_qubits(psum, expected_psum):
    if len(expected_psum.qubits) == len(psum.qubits):
        assert psum.with_qubits(*expected_psum.qubits) == expected_psum
    else:
        with pytest.raises(ValueError, match='number'):
            psum.with_qubits(*expected_psum.qubits)


def test_pauli_sum_from_single_pauli():
    q = qubitron.LineQubit.range(2)
    psum1 = qubitron.X(q[0]) + qubitron.Y(q[1])
    assert psum1 == qubitron.PauliSum.from_pauli_strings([qubitron.X(q[0]) * 1, qubitron.Y(q[1]) * 1])

    psum2 = qubitron.X(q[0]) * qubitron.X(q[1]) + qubitron.Y(q[1])
    assert psum2 == qubitron.PauliSum.from_pauli_strings(
        [qubitron.X(q[0]) * qubitron.X(q[1]), qubitron.Y(q[1]) * 1]
    )

    psum3 = qubitron.Y(q[1]) + qubitron.X(q[0]) * qubitron.X(q[1])
    assert psum3 == psum2


def test_pauli_sub():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    psum = pstr1 - pstr2

    psum2 = qubitron.PauliSum.from_pauli_strings([pstr1, -1 * pstr2])
    assert psum == psum2


def test_pauli_sub_simplify():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.X(q[0]) * qubitron.X(q[1])
    psum = pstr1 - pstr2

    psum2 = qubitron.PauliSum.from_pauli_strings([])
    assert psum == psum2


def test_pauli_sum_neg():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    psum1 = pstr1 + pstr2
    psum2 = -1 * pstr1 - pstr2

    assert -psum1 == psum2
    psum1 *= -1
    assert psum1 == psum2

    psum2 = psum1 * -1
    assert psum1 == -psum2


def test_paulisum_validation():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    with pytest.raises(ValueError) as e:
        qubitron.PauliSum([pstr1, pstr2])
    assert e.match("Consider using")

    with pytest.raises(ValueError):
        ld = qubitron.LinearDict({pstr1: 2.0})
        qubitron.PauliSum(ld)

    with pytest.raises(ValueError):
        key = frozenset([('q0', qubitron.X)])
        ld = qubitron.LinearDict({key: 2.0})
        qubitron.PauliSum(ld)

    with pytest.raises(ValueError):
        key = frozenset([(q[0], qubitron.H)])
        ld = qubitron.LinearDict({key: 2.0})
        qubitron.PauliSum(ld)

    key = frozenset([(q[0], qubitron.X)])
    ld = qubitron.LinearDict({key: 2.0})
    assert qubitron.PauliSum(ld) == qubitron.PauliSum.from_pauli_strings([2 * qubitron.X(q[0])])

    ps = qubitron.PauliSum()
    ps += qubitron.I(qubitron.LineQubit(0))
    assert ps == qubitron.PauliSum(qubitron.LinearDict({frozenset(): complex(1)}))


def test_add_number_paulisum():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    psum = qubitron.PauliSum.from_pauli_strings([pstr1]) + 1.3
    assert psum == qubitron.PauliSum.from_pauli_strings([pstr1, qubitron.PauliString({}, 1.3)])


def test_add_number_paulistring():
    a, b = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(a) * qubitron.X(b)
    psum = pstr1 + 1.3
    assert psum == qubitron.PauliSum.from_pauli_strings([pstr1, qubitron.PauliString({}, 1.3)])
    assert psum == 1.3 + pstr1

    psum = pstr1 - 1.3
    assert psum == psum + 0 == psum - 0 == 0 + psum == -(0 - psum)
    assert psum + 1 == 1 + psum
    assert psum - 1 == -(1 - psum)
    assert psum == qubitron.PauliSum.from_pauli_strings([pstr1, qubitron.PauliString({}, -1.3)])
    assert psum == -1.3 + pstr1
    assert psum == -1.3 - -pstr1

    assert (
        qubitron.X(a) + 2
        == 2 + qubitron.X(a)
        == qubitron.PauliSum.from_pauli_strings([qubitron.PauliString() * 2, qubitron.PauliString({a: qubitron.X})])
    )


def test_pauli_sum_formatting():
    q = qubitron.LineQubit.range(2)
    pauli = qubitron.X(q[0])
    assert str(pauli) == 'X(q(0))'
    paulistr = qubitron.X(q[0]) * qubitron.X(q[1])
    assert str(paulistr) == 'X(q(0))*X(q(1))'
    paulisum1 = qubitron.X(q[0]) * qubitron.X(q[1]) + 4
    assert str(paulisum1) == '1.000*X(q(0))*X(q(1))+4.000*I'
    paulisum2 = qubitron.X(q[0]) * qubitron.X(q[1]) + qubitron.Z(q[0])
    assert str(paulisum2) == '1.000*X(q(0))*X(q(1))+1.000*Z(q(0))'
    paulisum3 = qubitron.X(q[0]) * qubitron.X(q[1]) + qubitron.Z(q[0]) * qubitron.Z(q[1])
    assert str(paulisum3) == '1.000*X(q(0))*X(q(1))+1.000*Z(q(0))*Z(q(1))'
    assert f"{paulisum3:.0f}" == '1*X(q(0))*X(q(1))+1*Z(q(0))*Z(q(1))'

    empty = qubitron.PauliSum.from_pauli_strings([])
    assert str(empty) == "0.000"


def test_pauli_sum_matrix():
    q = qubitron.LineQubit.range(3)
    paulisum = qubitron.X(q[0]) * qubitron.X(q[1]) + qubitron.Z(q[0])
    H1 = np.array(
        [[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0], [0.0, 1.0, -1.0, 0.0], [1.0, 0.0, 0.0, -1.0]]
    )
    assert np.allclose(H1, paulisum.matrix())
    assert np.allclose(H1, paulisum.matrix([q[0], q[1]]))
    # Expects a different matrix when change qubits order.
    H2 = np.array(
        [[1.0, 0.0, 0.0, 1.0], [0.0, -1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 0.0, -1.0]]
    )
    assert np.allclose(H2, paulisum.matrix([q[1], q[0]]))
    # Expects matrix with a different size when add a new qubit.
    H3 = np.array(
        [
            [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        ]
    )
    assert np.allclose(H3, paulisum.matrix([q[1], q[2], q[0]]))


def test_pauli_sum_repr():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    psum = pstr1 + 2 * pstr2 + 1
    qubitron.testing.assert_equivalent_repr(psum)


def test_bad_arithmetic():
    q = qubitron.LineQubit.range(2)
    pstr1 = qubitron.X(q[0]) * qubitron.X(q[1])
    pstr2 = qubitron.Y(q[0]) * qubitron.Y(q[1])
    psum = pstr1 + 2 * pstr2 + 1

    with pytest.raises(TypeError):
        psum += 'hi mom'

    with pytest.raises(TypeError):
        _ = psum + 'hi mom'

    with pytest.raises(TypeError):
        psum -= 'hi mom'

    with pytest.raises(TypeError):
        _ = psum - 'hi mom'
    with pytest.raises(TypeError):
        psum *= [1, 2, 3]

    with pytest.raises(TypeError):
        _ = psum * [1, 2, 3]

    with pytest.raises(TypeError):
        _ = [1, 2, 3] * psum

    with pytest.raises(TypeError):
        _ = psum / [1, 2, 3]

    with pytest.raises(TypeError):
        _ = psum**1.2

    with pytest.raises(TypeError):
        _ = psum**-2

    with pytest.raises(TypeError):
        _ = psum ** "string"


def test_paulisum_mul_paulistring():
    q0, q1 = qubitron.LineQubit.range(2)

    psum1 = qubitron.X(q0) + 2 * qubitron.Y(q0) + 3 * qubitron.Z(q0)
    x0 = qubitron.PauliString(qubitron.X(q0))
    y1 = qubitron.PauliString(qubitron.Y(q1))
    assert x0 * psum1 == qubitron.PauliString(qubitron.I(q0)) + 2j * qubitron.PauliString(
        qubitron.Z(q0)
    ) - 3j * qubitron.PauliString(qubitron.Y(q0))
    assert y1 * psum1 == qubitron.PauliString(qubitron.X(q0) * qubitron.Y(q1)) + 2 * qubitron.PauliString(
        qubitron.Y(q0) * qubitron.Y(q1)
    ) + 3 * qubitron.PauliString(qubitron.Z(q0) * qubitron.Y(q1))
    assert qubitron.PauliString(qubitron.I(q0)) * psum1 == psum1
    assert psum1 * x0 == qubitron.PauliString(qubitron.I(q0)) - 2j * qubitron.PauliString(
        qubitron.Z(q0)
    ) + 3j * qubitron.PauliString(qubitron.Y(q0))
    assert psum1 * y1 == y1 * psum1

    psum1 *= qubitron.Z(q0)
    assert psum1 == -1j * qubitron.Y(q0) + 2j * qubitron.X(q0) + 3


def test_paulisum_mul_paulisum():
    q0, q1, q2 = qubitron.LineQubit.range(3)

    psum1 = qubitron.X(q0) + 2 * qubitron.Y(q0) * qubitron.Y(q1)
    psum2 = qubitron.X(q0) * qubitron.Y(q1) + 3 * qubitron.Z(q2)
    assert psum1 * psum2 == qubitron.Y(q1) + 3 * qubitron.X(q0) * qubitron.Z(q2) - 2j * qubitron.Z(q0) + 6 * qubitron.Y(
        q0
    ) * qubitron.Y(q1) * qubitron.Z(q2)
    assert psum2 * psum1 == qubitron.Y(q1) + 3 * qubitron.X(q0) * qubitron.Z(q2) + 2j * qubitron.Z(q0) + 6 * qubitron.Y(
        q0
    ) * qubitron.Y(q1) * qubitron.Z(q2)
    psum3 = qubitron.X(q1) + qubitron.X(q2)
    psum1 *= psum3
    assert psum1 == qubitron.X(q0) * qubitron.X(q1) - 2j * qubitron.Y(q0) * qubitron.Z(q1) + qubitron.X(q0) * qubitron.X(
        q2
    ) + 2 * qubitron.Y(q0) * qubitron.Y(q1) * qubitron.X(q2)

    psum4 = qubitron.X(q0) + qubitron.Y(q0) + qubitron.Z(q1)
    psum5 = qubitron.Z(q0) + qubitron.Y(q0) + qubitron.PauliString(coefficient=1.2)
    assert (
        psum4 * psum5
        == -1j * qubitron.Y(q0)
        + 1j * (qubitron.X(q0) + qubitron.Z(q0))
        + (qubitron.Z(q0) + qubitron.Y(q0)) * qubitron.Z(q1)
        + 1
        + 1.2 * psum4
    )
    assert (
        psum5 * psum4
        == 1j * qubitron.Y(q0)
        + -1j * (qubitron.X(q0) + qubitron.Z(q0))
        + (qubitron.Z(q0) + qubitron.Y(q0)) * qubitron.Z(q1)
        + 1
        + 1.2 * psum4
    )


def test_pauli_sum_pow():
    identity = qubitron.PauliSum.from_pauli_strings([qubitron.PauliString(coefficient=1)])
    psum1 = qubitron.X(q0) + qubitron.Y(q0)
    assert psum1**2 == psum1 * psum1
    assert psum1**2 == 2 * identity

    psum2 = qubitron.X(q0) + qubitron.Y(q1)
    assert psum2**2 == qubitron.PauliString(qubitron.I(q0)) + 2 * qubitron.X(q0) * qubitron.Y(
        q1
    ) + qubitron.PauliString(qubitron.I(q1))

    psum3 = qubitron.X(q0) * qubitron.Z(q1) + 1.3 * qubitron.Z(q0)
    sqd = qubitron.PauliSum.from_pauli_strings([2.69 * qubitron.PauliString(qubitron.I(q0))])
    assert qubitron.approx_eq(psum3**2, sqd, atol=1e-8)

    psum4 = qubitron.X(q0) * qubitron.Z(q1) + 1.3 * qubitron.Z(q1)
    sqd2 = qubitron.PauliSum.from_pauli_strings([2.69 * qubitron.PauliString(qubitron.I(q0)), 2.6 * qubitron.X(q0)])
    assert qubitron.approx_eq(psum4**2, sqd2, atol=1e-8)

    for psum in [psum1, psum2, psum3, psum4]:
        assert qubitron.approx_eq(psum**0, identity)

    # tests for exponents greater than two for both even and odd
    psum5 = qubitron.Z(q0) * qubitron.Z(q1) + qubitron.Z(q2) + qubitron.Z(q3)
    correctresult = psum5.copy()
    for e in range(1, 9):
        assert correctresult == psum5**e
        correctresult *= psum5

    psum6 = qubitron.X(q0) * qubitron.Y(q1) + qubitron.Z(q2) + qubitron.X(q3)
    assert psum6 * psum6 * psum6 * psum6 * psum6 * psum6 * psum6 * psum6 == psum6**8

    # test to ensure pow doesn't make any change to the original value
    psum7 = qubitron.X(q0) * qubitron.Y(q1) + qubitron.Z(q2)
    psum7copy = psum7.copy()
    assert psum7**5 == psum7 * psum7 * psum7 * psum7 * psum7
    assert psum7copy == psum7


# Using the entries of table 1 of https://arxiv.org/abs/1804.09130 as golden values.
@pytest.mark.parametrize(
    'boolean_expr,expected_pauli_sum',
    [
        ('x', ['(-0.5+0j)*Z(x)', '(0.5+0j)*I']),
        ('~x', ['(0.5+0j)*I', '(0.5+0j)*Z(x)']),
        ('x0 ^ x1', ['(-0.5+0j)*Z(x0)*Z(x1)', '(0.5+0j)*I']),
        (
            'x0 & x1',
            ['(-0.25+0j)*Z(x0)', '(-0.25+0j)*Z(x1)', '(0.25+0j)*I', '(0.25+0j)*Z(x0)*Z(x1)'],
        ),
        (
            'x0 | x1',
            ['(-0.25+0j)*Z(x0)', '(-0.25+0j)*Z(x0)*Z(x1)', '(-0.25+0j)*Z(x1)', '(0.75+0j)*I'],
        ),
        ('x0 ^ x1 ^ x2', ['(-0.5+0j)*Z(x0)*Z(x1)*Z(x2)', '(0.5+0j)*I']),
    ],
)
def test_from_boolean_expression(boolean_expr, expected_pauli_sum):
    boolean = sympy_parser.parse_expr(boolean_expr)
    qubit_map = {name: qubitron.NamedQubit(name) for name in sorted(qubitron.parameter_names(boolean))}
    actual = qubitron.PauliSum.from_boolean_expression(boolean, qubit_map)
    # Instead of calling str() directly, first make sure that the items are sorted. This is to make
    # the unit test more robut in case Sympy would result in a different parsing order. By sorting
    # the individual items, we would have a canonical representation.
    actual_items = list(sorted(str(pauli_string) for pauli_string in actual))
    assert expected_pauli_sum == actual_items


def test_unsupported_op():
    not_a_boolean = sympy_parser.parse_expr('x * x')
    qubit_map = {name: qubitron.NamedQubit(name) for name in qubitron.parameter_names(not_a_boolean)}
    with pytest.raises(ValueError, match='Unsupported type'):
        qubitron.PauliSum.from_boolean_expression(not_a_boolean, qubit_map)


def test_imul_aliasing():
    q0, q1, q2 = qubitron.LineQubit.range(3)
    psum1 = qubitron.X(q0) + qubitron.Y(q1)
    psum2 = psum1
    psum2 *= qubitron.X(q0) * qubitron.Y(q2)
    assert psum1 is psum2
    assert psum1 == psum2


def test_expectation_from_state_vector_invalid_input():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    psum = qubitron.X(q0) + 2 * qubitron.Y(q1) + 3 * qubitron.Z(q3)
    q_map = {q0: 0, q1: 1, q3: 2}
    wf = np.array([1, 0, 0, 0, 0, 0, 0], dtype=np.complex64)

    im_psum = (1j + 1) * psum
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_psum.expectation_from_state_vector(wf, q_map)

    with pytest.raises(TypeError, match='dtype'):
        psum.expectation_from_state_vector(np.array([1, 0], dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_state_vector(wf, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_state_vector(wf, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_state_vector(wf, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        psum.expectation_from_state_vector(wf, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        psum.expectation_from_state_vector(wf, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_state_vector(wf, {q0: -1, q1: 1, q3: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_state_vector(wf, {q0: 0, q1: 3, q3: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_state_vector(wf, {q0: 0, q1: 0, q3: 2})

    with pytest.raises(ValueError, match='9'):
        psum.expectation_from_state_vector(np.arange(9, dtype=np.complex64), q_map)
    q_map_2 = {q0: 0, q1: 1, q2: 2, q3: 3}
    with pytest.raises(ValueError, match='normalized'):
        psum.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map_2)

    wf = np.arange(16, dtype=np.complex64) / np.linalg.norm(np.arange(16))
    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_state_vector(wf.reshape((16, 1)), q_map_2)
    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_state_vector(wf.reshape((4, 4, 1)), q_map_2)


def test_expectation_from_state_vector_check_preconditions():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    psum = qubitron.X(q0) + 2 * qubitron.Y(q1) + 3 * qubitron.Z(q3)
    q_map = {q0: 0, q1: 1, q2: 2, q3: 3}

    with pytest.raises(ValueError, match='normalized'):
        psum.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map)

    _ = psum.expectation_from_state_vector(
        np.arange(16, dtype=np.complex64), q_map, check_preconditions=False
    )


def test_expectation_from_state_vector_basis_states():
    q = qubitron.LineQubit.range(2)
    psum = qubitron.X(q[0]) + 2 * qubitron.Y(q[0]) + 3 * qubitron.Z(q[0])
    q_map = {x: i for i, x in enumerate(q)}

    np.testing.assert_allclose(
        psum.expectation_from_state_vector(
            np.array([1, 1], dtype=complex) / np.sqrt(2), qubit_map=q_map
        ),
        1,
    )
    np.testing.assert_allclose(
        psum.expectation_from_state_vector(
            np.array([1, -1], dtype=complex) / np.sqrt(2), qubit_map=q_map
        ),
        -1,
    )
    np.testing.assert_allclose(
        psum.expectation_from_state_vector(
            np.array([1, 1j], dtype=complex) / np.sqrt(2), qubit_map=q_map
        ),
        2,
    )
    np.testing.assert_allclose(
        psum.expectation_from_state_vector(
            np.array([1, -1j], dtype=complex) / np.sqrt(2), qubit_map=q_map
        ),
        -2,
    )
    np.testing.assert_allclose(
        psum.expectation_from_state_vector(np.array([1, 0], dtype=complex), qubit_map=q_map), 3
    )
    np.testing.assert_allclose(
        psum.expectation_from_state_vector(np.array([0, 1], dtype=complex), qubit_map=q_map), -3
    )


def test_expectation_from_state_vector_two_qubit_states():
    q = qubitron.LineQubit.range(2)
    q_map = {x: i for i, x in enumerate(q)}

    psum1 = qubitron.Z(q[0]) + 3.2 * qubitron.Z(q[1])
    psum2 = -1 * qubitron.X(q[0]) + 2 * qubitron.X(q[1])
    wf1 = np.array([0, 1, 0, 0], dtype=complex)
    for state in [wf1, wf1.reshape((2, 2))]:
        np.testing.assert_allclose(
            psum1.expectation_from_state_vector(state, qubit_map=q_map), -2.2, atol=1e-7
        )
        np.testing.assert_allclose(
            psum2.expectation_from_state_vector(state, qubit_map=q_map), 0, atol=1e-7
        )

    wf2 = np.array([1, 1, 1, 1], dtype=complex) / 2
    for state in [wf2, wf2.reshape((2, 2))]:
        np.testing.assert_allclose(
            psum1.expectation_from_state_vector(state, qubit_map=q_map), 0, atol=1e-7
        )
        np.testing.assert_allclose(
            psum2.expectation_from_state_vector(state, qubit_map=q_map), 1, atol=1e-7
        )

    psum3 = qubitron.Z(q[0]) + qubitron.X(q[1])
    wf3 = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)
    q_map_2 = {q0: 1, q1: 0}
    for state in [wf3, wf3.reshape((2, 2))]:
        np.testing.assert_allclose(
            psum3.expectation_from_state_vector(state, qubit_map=q_map), 2, atol=1e-7
        )
        np.testing.assert_allclose(
            psum3.expectation_from_state_vector(state, qubit_map=q_map_2), 0, atol=1e-7
        )


def test_expectation_from_density_matrix_invalid_input():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    psum = qubitron.X(q0) + 2 * qubitron.Y(q1) + 3 * qubitron.Z(q3)
    q_map = {q0: 0, q1: 1, q3: 2}
    wf = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.complex64)
    rho = np.kron(wf.conjugate().T, wf).reshape((8, 8))

    im_psum = (1j + 1) * psum
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_psum.expectation_from_density_matrix(rho, q_map)

    with pytest.raises(TypeError, match='dtype'):
        psum.expectation_from_density_matrix(0.5 * np.eye(2, dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_density_matrix(rho, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_density_matrix(rho, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        psum.expectation_from_density_matrix(rho, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        psum.expectation_from_density_matrix(rho, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        psum.expectation_from_density_matrix(rho, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_density_matrix(rho, {q0: -1, q1: 1, q3: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_density_matrix(rho, {q0: 0, q1: 3, q3: 2})
    with pytest.raises(ValueError, match='indices'):
        psum.expectation_from_density_matrix(rho, {q0: 0, q1: 0, q3: 2})

    with pytest.raises(ValueError, match='hermitian'):
        psum.expectation_from_density_matrix(1j * np.eye(8), q_map)
    with pytest.raises(ValueError, match='trace'):
        psum.expectation_from_density_matrix(np.eye(8, dtype=np.complex64), q_map)

    not_psd = np.zeros((8, 8), dtype=np.complex64)
    not_psd[0, 0] = 1.1
    not_psd[1, 1] = -0.1
    with pytest.raises(ValueError, match='semidefinite'):
        psum.expectation_from_density_matrix(not_psd, q_map)

    not_square = np.ones((8, 9), dtype=np.complex64)
    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_density_matrix(not_square, q_map)
    bad_wf = np.zeros(128, dtype=np.complex64)
    bad_wf[0] = 1
    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_density_matrix(bad_wf, q_map)

    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_density_matrix(rho.reshape((8, 8, 1)), q_map)
    with pytest.raises(ValueError, match='shape'):
        psum.expectation_from_density_matrix(rho.reshape((-1)), q_map)


def test_expectation_from_density_matrix_check_preconditions():
    q0, q1, _, q3 = qubitron.LineQubit.range(4)
    psum = qubitron.X(q0) + 2 * qubitron.Y(q1) + 3 * qubitron.Z(q3)
    q_map = {q0: 0, q1: 1, q3: 2}
    not_psd = np.zeros((8, 8), dtype=np.complex64)
    not_psd[0, 0] = 1.1
    not_psd[1, 1] = -0.1

    with pytest.raises(ValueError, match='semidefinite'):
        psum.expectation_from_density_matrix(not_psd, q_map)

    _ = psum.expectation_from_density_matrix(not_psd, q_map, check_preconditions=False)


def test_expectation_from_density_matrix_basis_states():
    q = qubitron.LineQubit.range(2)
    psum = qubitron.X(q[0]) + 2 * qubitron.Y(q[0]) + 3 * qubitron.Z(q[0])
    q_map = {x: i for i, x in enumerate(q)}

    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(np.array([[1, 1], [1, 1]], dtype=complex) / 2, q_map),
        1,
    )
    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(
            np.array([[1, -1], [-1, 1]], dtype=complex) / 2, q_map
        ),
        -1,
    )
    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(
            np.array([[1, -1j], [1j, 1]], dtype=complex) / 2, qubit_map=q_map
        ),
        2,
    )
    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(
            np.array([[1, 1j], [-1j, 1]], dtype=complex) / 2, qubit_map=q_map
        ),
        -2,
    )
    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(np.array([[1, 0], [0, 0]], dtype=complex), q_map), 3
    )
    np.testing.assert_allclose(
        psum.expectation_from_density_matrix(np.array([[0, 0], [0, 1]], dtype=complex), q_map), -3
    )


def test_expectation_from_density_matrix_two_qubit_states():
    q = qubitron.LineQubit.range(2)
    q_map = {x: i for i, x in enumerate(q)}

    psum1 = qubitron.Z(q[0]) + 3.2 * qubitron.Z(q[1])
    psum2 = -1 * qubitron.X(q[0]) + 2 * qubitron.X(q[1])
    wf1 = np.array([0, 1, 0, 0], dtype=complex)
    rho1 = np.kron(wf1, wf1).reshape((4, 4))
    for state in [rho1, rho1.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(
            psum1.expectation_from_density_matrix(state, qubit_map=q_map), -2.2
        )
        np.testing.assert_allclose(psum2.expectation_from_density_matrix(state, qubit_map=q_map), 0)

    wf2 = np.array([1, 1, 1, 1], dtype=complex) / 2
    rho2 = np.kron(wf2, wf2).reshape((4, 4))
    for state in [rho2, rho2.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(psum1.expectation_from_density_matrix(state, qubit_map=q_map), 0)
        np.testing.assert_allclose(psum2.expectation_from_density_matrix(state, qubit_map=q_map), 1)

    psum3 = qubitron.Z(q[0]) + qubitron.X(q[1])
    wf3 = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)
    rho3 = np.kron(wf3, wf3).reshape((4, 4))
    q_map_2 = {q0: 1, q1: 0}
    for state in [rho3, rho3.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(psum3.expectation_from_density_matrix(state, qubit_map=q_map), 2)
        np.testing.assert_allclose(
            psum3.expectation_from_density_matrix(state, qubit_map=q_map_2), 0
        )


def test_projector_sum_expectations_matrix():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 0}, coefficient=0.2016)
    )
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 1}, coefficient=0.0913)
    )
    proj_sum = 0.6 * zero_projector_sum + 0.4 * one_projector_sum

    np.testing.assert_allclose(
        proj_sum.matrix().toarray(),
        0.6 * zero_projector_sum.matrix().toarray() + 0.4 * one_projector_sum.matrix().toarray(),
    )


def test_projector_sum_expectations_from_state_vector():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 0}, coefficient=0.2016)
    )
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 1}, coefficient=0.0913)
    )
    proj_sum = 0.6 * zero_projector_sum + 0.4 * one_projector_sum

    random_state_vector = qubitron.testing.random_superposition(2)

    np.testing.assert_allclose(
        proj_sum.expectation_from_state_vector(random_state_vector, qid_map={q0: 0}),
        0.6 * zero_projector_sum.expectation_from_state_vector(random_state_vector, qid_map={q0: 0})
        + 0.4
        * one_projector_sum.expectation_from_state_vector(random_state_vector, qid_map={q0: 0}),
    )


def test_projector_sum_expectations_from_density_matrix():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 0}, coefficient=0.2016)
    )
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        qubitron.ProjectorString({q0: 1}, coefficient=0.0913)
    )
    proj_sum = 0.6 * zero_projector_sum + 0.4 * one_projector_sum

    ranom_density_matrix = qubitron.testing.random_density_matrix(2)

    np.testing.assert_allclose(
        proj_sum.expectation_from_density_matrix(ranom_density_matrix, qid_map={q0: 0}),
        0.6
        * zero_projector_sum.expectation_from_density_matrix(ranom_density_matrix, qid_map={q0: 0})
        + 0.4
        * one_projector_sum.expectation_from_density_matrix(ranom_density_matrix, qid_map={q0: 0}),
    )


def test_projector_sum_accessor():
    q0 = qubitron.NamedQubit('q0')

    projector_string_1 = qubitron.ProjectorString({q0: 0}, 0.2016)
    projector_string_2 = qubitron.ProjectorString({q0: 1}, 0.0913)

    projector_sum = qubitron.ProjectorSum.from_projector_strings(
        [projector_string_1, projector_string_2]
    )

    assert len(projector_sum) == 2
    expanded_projector_strings = list(projector_sum)
    assert expanded_projector_strings == [projector_string_1, projector_string_2]


def test_projector_bool_operation():
    q0 = qubitron.NamedQubit('q0')

    empty_projector_sum = qubitron.ProjectorSum.from_projector_strings([])
    non_empty_projector_sum = qubitron.ProjectorSum.from_projector_strings(
        [qubitron.ProjectorString({q0: 0})]
    )

    assert not empty_projector_sum
    assert non_empty_projector_sum


def test_projector_sum_addition():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))
    one_projector_string = qubitron.ProjectorString({q0: 1})
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(one_projector_string)

    simple_addition = zero_projector_sum + one_projector_sum
    np.testing.assert_allclose(simple_addition.matrix().toarray(), [[1.0, 0.0], [0.0, 1.0]])

    simple_addition = zero_projector_sum + one_projector_string
    np.testing.assert_allclose(simple_addition.matrix().toarray(), [[1.0, 0.0], [0.0, 1.0]])

    # Check that the inputs are not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(one_projector_sum.matrix().toarray(), [[0.0, 0.0], [0.0, 1.0]])

    with pytest.raises(TypeError):
        _ = zero_projector_sum + 0.20160913


def test_projector_sum_subtraction():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))
    one_projector_string = qubitron.ProjectorString({q0: 1})
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(one_projector_string)

    simple_subtraction = zero_projector_sum - one_projector_sum
    np.testing.assert_allclose(simple_subtraction.matrix().toarray(), [[1.0, 0.0], [0.0, -1.0]])

    simple_subtraction = zero_projector_sum - one_projector_string
    np.testing.assert_allclose(simple_subtraction.matrix().toarray(), [[1.0, 0.0], [0.0, -1.0]])

    # Check that the inputs are not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(one_projector_sum.matrix().toarray(), [[0.0, 0.0], [0.0, 1.0]])

    with pytest.raises(TypeError):
        _ = zero_projector_sum - 0.87539319


def test_projector_sum_negation():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))

    negation = -zero_projector_sum.copy()
    np.testing.assert_allclose(negation.matrix().toarray(), [[-1.0, 0.0], [0.0, 0.0]])

    # Check that the input is not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])


def test_projector_sum_incrementation():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))
    one_projector_string = qubitron.ProjectorString({q0: 1})
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(one_projector_string)

    incrementation = zero_projector_sum.copy()
    incrementation += one_projector_sum
    np.testing.assert_allclose(incrementation.matrix().toarray(), [[1.0, 0.0], [0.0, 1.0]])

    incrementation = zero_projector_sum.copy()
    incrementation += one_projector_string
    np.testing.assert_allclose(incrementation.matrix().toarray(), [[1.0, 0.0], [0.0, 1.0]])

    # Check that the inputs are not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(one_projector_sum.matrix().toarray(), [[0.0, 0.0], [0.0, 1.0]])

    with pytest.raises(TypeError):
        zero_projector_sum += 0.6963472309248


def test_projector_sum_decrementation():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))
    one_projector_string = qubitron.ProjectorString({q0: 1})
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(one_projector_string)

    decrementation = zero_projector_sum.copy()
    decrementation -= one_projector_sum
    np.testing.assert_allclose(decrementation.matrix().toarray(), [[1.0, 0.0], [0.0, -1.0]])

    decrementation = zero_projector_sum.copy()
    decrementation -= one_projector_string
    np.testing.assert_allclose(decrementation.matrix().toarray(), [[1.0, 0.0], [0.0, -1.0]])

    # Check that the inputs are not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(one_projector_sum.matrix().toarray(), [[0.0, 0.0], [0.0, 1.0]])

    with pytest.raises(TypeError):
        zero_projector_sum -= 0.12345


def test_projector_sum_multiplication_left():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))

    multiplication_float = 2.0 * zero_projector_sum
    np.testing.assert_allclose(multiplication_float.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_int = 2 * zero_projector_sum
    np.testing.assert_allclose(multiplication_int.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_complex = 2j * zero_projector_sum
    np.testing.assert_allclose(multiplication_complex.matrix().toarray(), [[2.0j, 0.0], [0.0, 0.0]])

    # Check that the input is not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])

    with pytest.raises(TypeError):
        _ = 'not_the_correct_type' * zero_projector_sum


def test_projector_sum_multiplication_right():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))

    multiplication_float = zero_projector_sum * 2.0
    np.testing.assert_allclose(multiplication_float.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_int = zero_projector_sum * 2
    np.testing.assert_allclose(multiplication_int.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_complex = zero_projector_sum * 2j
    np.testing.assert_allclose(multiplication_complex.matrix().toarray(), [[2.0j, 0.0], [0.0, 0.0]])

    # Check that the input is not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])

    with pytest.raises(TypeError):
        _ = zero_projector_sum * 'not_the_correct_type'


def test_projector_sum_self_multiplication():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))

    multiplication_float = zero_projector_sum.copy()
    multiplication_float *= 2.0
    np.testing.assert_allclose(multiplication_float.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_int = zero_projector_sum.copy()
    multiplication_int *= 2
    np.testing.assert_allclose(multiplication_int.matrix().toarray(), [[2.0, 0.0], [0.0, 0.0]])

    multiplication_complex = zero_projector_sum.copy()
    multiplication_complex *= 2j
    np.testing.assert_allclose(multiplication_complex.matrix().toarray(), [[2.0j, 0.0], [0.0, 0.0]])

    with pytest.raises(TypeError):
        zero_projector_sum *= 'not_the_correct_type'


def test_projector_sum_weighted_sum():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))
    one_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 1}))

    weighted_sum = 0.6 * zero_projector_sum + 0.4 * one_projector_sum
    np.testing.assert_allclose(weighted_sum.matrix().toarray(), [[0.6, 0.0], [0.0, 0.4]])

    # Check that the inputs are not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])
    np.testing.assert_allclose(one_projector_sum.matrix().toarray(), [[0.0, 0.0], [0.0, 1.0]])


def test_projector_sum_division():
    q0 = qubitron.NamedQubit('q0')

    zero_projector_sum = qubitron.ProjectorSum.from_projector_strings(qubitron.ProjectorString({q0: 0}))

    true_division_float = zero_projector_sum / 2.0
    np.testing.assert_allclose(true_division_float.matrix().toarray(), [[0.5, 0.0], [0.0, 0.0]])

    true_division_int = zero_projector_sum / 2
    np.testing.assert_allclose(true_division_int.matrix().toarray(), [[0.5, 0.0], [0.0, 0.0]])

    true_division_complex = zero_projector_sum / 2j
    np.testing.assert_allclose(true_division_complex.matrix().toarray(), [[-0.5j, 0.0], [0.0, 0.0]])

    # Check that the input is not changed:
    np.testing.assert_allclose(zero_projector_sum.matrix().toarray(), [[1.0, 0.0], [0.0, 0.0]])

    with pytest.raises(TypeError):
        _ = zero_projector_sum / 'not_the_correct_type'


@pytest.mark.parametrize(
    'terms, expected_qubits',
    (
        ([], ()),
        ([qubitron.ProjectorString({q0: 0})], (q0,)),
        ([qubitron.ProjectorString({q0: 0}), qubitron.ProjectorString({q1: 0})], (q0, q1)),
        ([qubitron.ProjectorString({q0: 0, q1: 1})], (q0, q1)),
    ),
)
def test_projector_sum_has_correct_qubits(terms, expected_qubits):
    combination = qubitron.ProjectorSum.from_projector_strings(terms)
    assert combination.qubits == expected_qubits
