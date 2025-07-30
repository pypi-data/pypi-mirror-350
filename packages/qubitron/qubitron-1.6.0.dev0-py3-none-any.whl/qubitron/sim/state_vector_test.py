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

"""Tests for state_vector.py"""

from __future__ import annotations

import itertools
from typing import Iterator
from unittest import mock

import numpy as np
import pytest

import qubitron
import qubitron.testing
from qubitron import linalg


@pytest.fixture
def use_np_transpose(request) -> Iterator[bool]:
    value: bool = request.param
    with mock.patch.object(linalg, 'can_numpy_support_shape', lambda shape: value):
        yield value


def test_state_mixin():
    class TestClass(qubitron.StateVectorMixin):
        def state_vector(self, copy: bool | None = None) -> np.ndarray:
            return np.array([0, 0, 1, 0])

    qubits = qubitron.LineQubit.range(2)
    test = TestClass(qubit_map={qubits[i]: i for i in range(2)})
    assert test.dirac_notation() == '|10⟩'
    np.testing.assert_almost_equal(test.bloch_vector_of(qubits[0]), np.array([0, 0, -1]))
    np.testing.assert_almost_equal(test.density_matrix_of(qubits[0:1]), np.array([[0, 0], [0, 1]]))

    assert qubitron.qid_shape(TestClass({qubits[i]: 1 - i for i in range(2)})) == (2, 2)
    assert qubitron.qid_shape(TestClass({qubitron.LineQid(i, i + 1): 2 - i for i in range(3)})) == (3, 2, 1)
    assert qubitron.qid_shape(TestClass(), 'no shape') == 'no shape'

    with pytest.raises(ValueError, match='Qubit index out of bounds'):
        _ = TestClass({qubits[0]: 1})
    with pytest.raises(ValueError, match='Duplicate qubit index'):
        _ = TestClass({qubits[0]: 0, qubits[1]: 0})
    with pytest.raises(ValueError, match='Duplicate qubit index'):
        _ = TestClass({qubits[0]: 1, qubits[1]: 1})
    with pytest.raises(ValueError, match='Duplicate qubit index'):
        _ = TestClass({qubits[0]: -1, qubits[1]: 1})


def test_sample_state_big_endian():
    results = []
    for x in range(8):
        state = qubitron.to_valid_state_vector(x, 3)
        sample = qubitron.sample_state_vector(state, [2, 1, 0])
        results.append(sample)
    expecteds = [[list(reversed(x))] for x in list(itertools.product([False, True], repeat=3))]
    for result, expected in zip(results, expecteds):
        np.testing.assert_equal(result, expected)


def test_sample_state_partial_indices():
    for index in range(3):
        for x in range(8):
            state = qubitron.to_valid_state_vector(x, 3)
            np.testing.assert_equal(
                qubitron.sample_state_vector(state, [index]), [[bool(1 & (x >> (2 - index)))]]
            )


def test_sample_state_partial_indices_oder():
    for x in range(8):
        state = qubitron.to_valid_state_vector(x, 3)
        expected = [[bool(1 & (x >> 0)), bool(1 & (x >> 1))]]
        np.testing.assert_equal(qubitron.sample_state_vector(state, [2, 1]), expected)


def test_sample_state_partial_indices_all_orders():
    for perm in itertools.permutations([0, 1, 2]):
        for x in range(8):
            state = qubitron.to_valid_state_vector(x, 3)
            expected = [[bool(1 & (x >> (2 - p))) for p in perm]]
            np.testing.assert_equal(qubitron.sample_state_vector(state, perm), expected)


def test_sample_state():
    state = np.zeros(8, dtype=np.complex64)
    state[0] = 1 / np.sqrt(2)
    state[2] = 1 / np.sqrt(2)
    for _ in range(10):
        sample = qubitron.sample_state_vector(state, [2, 1, 0])
        assert np.array_equal(sample, [[False, False, False]]) or np.array_equal(
            sample, [[False, True, False]]
        )
    # Partial sample is correct.
    for _ in range(10):
        np.testing.assert_equal(qubitron.sample_state_vector(state, [2]), [[False]])
        np.testing.assert_equal(qubitron.sample_state_vector(state, [0]), [[False]])


def test_sample_empty_state():
    state = np.array([1.0])
    np.testing.assert_almost_equal(qubitron.sample_state_vector(state, []), np.zeros(shape=(1, 0)))


def test_sample_no_repetitions():
    state = qubitron.to_valid_state_vector(0, 3)
    np.testing.assert_almost_equal(
        qubitron.sample_state_vector(state, [1], repetitions=0), np.zeros(shape=(0, 1))
    )
    np.testing.assert_almost_equal(
        qubitron.sample_state_vector(state, [1, 2], repetitions=0), np.zeros(shape=(0, 2))
    )


def test_sample_state_repetitions():
    for perm in itertools.permutations([0, 1, 2]):
        for x in range(8):
            state = qubitron.to_valid_state_vector(x, 3)
            expected = [[bool(1 & (x >> (2 - p))) for p in perm]] * 3

            result = qubitron.sample_state_vector(state, perm, repetitions=3)
            np.testing.assert_equal(result, expected)


def test_sample_state_seed():
    state = np.ones(2) / np.sqrt(2)

    samples = qubitron.sample_state_vector(state, [0], repetitions=10, seed=1234)
    assert np.array_equal(
        samples,
        [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]],
    )

    samples = qubitron.sample_state_vector(state, [0], repetitions=10, seed=np.random.RandomState(1234))
    assert np.array_equal(
        samples,
        [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]],
    )


def test_sample_state_negative_repetitions():
    state = qubitron.to_valid_state_vector(0, 3)
    with pytest.raises(ValueError, match='-1'):
        qubitron.sample_state_vector(state, [1], repetitions=-1)


def test_sample_state_not_power_of_two():
    with pytest.raises(ValueError, match='3'):
        qubitron.sample_state_vector(np.array([1, 0, 0]), [1])
    with pytest.raises(ValueError, match='5'):
        qubitron.sample_state_vector(np.array([0, 1, 0, 0, 0]), [1])


def test_sample_state_index_out_of_range():
    state = qubitron.to_valid_state_vector(0, 3)
    with pytest.raises(IndexError, match='-2'):
        qubitron.sample_state_vector(state, [-2])
    with pytest.raises(IndexError, match='3'):
        qubitron.sample_state_vector(state, [3])


def test_sample_no_indices():
    state = qubitron.to_valid_state_vector(0, 3)
    np.testing.assert_almost_equal(qubitron.sample_state_vector(state, []), np.zeros(shape=(1, 0)))


def test_sample_no_indices_repetitions():
    state = qubitron.to_valid_state_vector(0, 3)
    np.testing.assert_almost_equal(
        qubitron.sample_state_vector(state, [], repetitions=2), np.zeros(shape=(2, 0))
    )


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_computational_basis(use_np_transpose: bool):
    # verify patching of can_numpy_support_shape in the use_np_transpose fixture
    assert linalg.can_numpy_support_shape([1]) is use_np_transpose
    results = []
    for x in range(8):
        initial_state = qubitron.to_valid_state_vector(x, 3)
        bits, state = qubitron.measure_state_vector(initial_state, [2, 1, 0])
        results.append(bits)
        np.testing.assert_almost_equal(state, initial_state)
    expected = [list(reversed(x)) for x in list(itertools.product([False, True], repeat=3))]
    assert results == expected


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_reshape(use_np_transpose: bool):
    results = []
    for x in range(8):
        initial_state = np.reshape(qubitron.to_valid_state_vector(x, 3), [2] * 3)
        bits, state = qubitron.measure_state_vector(initial_state, [2, 1, 0])
        results.append(bits)
        np.testing.assert_almost_equal(state, initial_state)
    expected = [list(reversed(x)) for x in list(itertools.product([False, True], repeat=3))]
    assert results == expected


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_partial_indices(use_np_transpose: bool):
    for index in range(3):
        for x in range(8):
            initial_state = qubitron.to_valid_state_vector(x, 3)
            bits, state = qubitron.measure_state_vector(initial_state, [index])
            np.testing.assert_almost_equal(state, initial_state)
            assert bits == [bool(1 & (x >> (2 - index)))]


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_partial_indices_order(use_np_transpose: bool):
    for x in range(8):
        initial_state = qubitron.to_valid_state_vector(x, 3)
        bits, state = qubitron.measure_state_vector(initial_state, [2, 1])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [bool(1 & (x >> 0)), bool(1 & (x >> 1))]


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_partial_indices_all_orders(use_np_transpose: bool):
    for perm in itertools.permutations([0, 1, 2]):
        for x in range(8):
            initial_state = qubitron.to_valid_state_vector(x, 3)
            bits, state = qubitron.measure_state_vector(initial_state, perm)
            np.testing.assert_almost_equal(state, initial_state)
            assert bits == [bool(1 & (x >> (2 - p))) for p in perm]


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_collapse(use_np_transpose: bool):
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    for _ in range(10):
        bits, state = qubitron.measure_state_vector(initial_state, [2, 1, 0])
        assert bits in [[False, False, False], [False, True, False]]
        expected = np.zeros(8, dtype=np.complex64)
        expected[2 if bits[1] else 0] = 1.0
        np.testing.assert_almost_equal(state, expected)
        assert state is not initial_state

    # Partial sample is correct.
    for _ in range(10):
        bits, state = qubitron.measure_state_vector(initial_state, [2])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [False]

        bits, state = qubitron.measure_state_vector(initial_state, [0])
        np.testing.assert_almost_equal(state, initial_state)
        assert bits == [False]


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_seed(use_np_transpose: bool):
    n = 10
    initial_state = np.ones(2**n) / 2 ** (n / 2)

    bits, state1 = qubitron.measure_state_vector(initial_state, range(n), seed=1234)
    np.testing.assert_equal(
        bits, [False, False, True, True, False, False, False, True, False, False]
    )

    bits, state2 = qubitron.measure_state_vector(
        initial_state, range(n), seed=np.random.RandomState(1234)
    )
    np.testing.assert_equal(
        bits, [False, False, True, True, False, False, False, True, False, False]
    )

    np.testing.assert_allclose(state1, state2)


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_out_is_state(use_np_transpose: bool):
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    bits, state = qubitron.measure_state_vector(initial_state, [2, 1, 0], out=initial_state)
    expected = np.zeros(8, dtype=np.complex64)
    expected[2 if bits[1] else 0] = 1.0
    np.testing.assert_array_almost_equal(initial_state, expected)
    assert state is initial_state


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_out_is_not_state(use_np_transpose: bool):
    initial_state = np.zeros(8, dtype=np.complex64)
    initial_state[0] = 1 / np.sqrt(2)
    initial_state[2] = 1 / np.sqrt(2)
    out = np.zeros_like(initial_state)
    _, state = qubitron.measure_state_vector(initial_state, [2, 1, 0], out=out)
    assert out is not initial_state
    assert out is state


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_not_power_of_two(use_np_transpose: bool):
    with pytest.raises(ValueError, match='3'):
        _, _ = qubitron.measure_state_vector(np.array([1, 0, 0]), [1])
    with pytest.raises(ValueError, match='5'):
        qubitron.measure_state_vector(np.array([0, 1, 0, 0, 0]), [1])


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_index_out_of_range(use_np_transpose: bool):
    state = qubitron.to_valid_state_vector(0, 3)
    with pytest.raises(IndexError, match='-2'):
        qubitron.measure_state_vector(state, [-2])
    with pytest.raises(IndexError, match='3'):
        qubitron.measure_state_vector(state, [3])


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_no_indices(use_np_transpose: bool):
    initial_state = qubitron.to_valid_state_vector(0, 3)
    bits, state = qubitron.measure_state_vector(initial_state, [])
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_no_indices_out_is_state(use_np_transpose: bool):
    initial_state = qubitron.to_valid_state_vector(0, 3)
    bits, state = qubitron.measure_state_vector(initial_state, [], out=initial_state)
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)
    assert state is initial_state


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_no_indices_out_is_not_state(use_np_transpose: bool):
    initial_state = qubitron.to_valid_state_vector(0, 3)
    out = np.zeros_like(initial_state)
    bits, state = qubitron.measure_state_vector(initial_state, [], out=out)
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)
    assert state is out
    assert out is not initial_state


@pytest.mark.parametrize('use_np_transpose', [False, True], indirect=True)
def test_measure_state_empty_state(use_np_transpose: bool):
    initial_state = np.array([1.0])
    bits, state = qubitron.measure_state_vector(initial_state, [])
    assert [] == bits
    np.testing.assert_almost_equal(state, initial_state)


class BasicStateVector(qubitron.StateVectorMixin):
    def state_vector(self, copy: bool | None = None) -> np.ndarray:
        return np.array([0, 1, 0, 0])


def test_step_result_pretty_state():
    step_result = BasicStateVector()
    assert step_result.dirac_notation() == '|01⟩'


def test_step_result_density_matrix():
    q0, q1 = qubitron.LineQubit.range(2)

    step_result = BasicStateVector({q0: 0, q1: 1})
    rho = np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(rho, step_result.density_matrix_of([q0, q1]))

    np.testing.assert_array_almost_equal(rho, step_result.density_matrix_of())

    rho_ind_rev = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(rho_ind_rev, step_result.density_matrix_of([q1, q0]))

    single_rho = np.array([[0, 0], [0, 1]])
    np.testing.assert_array_almost_equal(single_rho, step_result.density_matrix_of([q1]))


def test_step_result_density_matrix_invalid():
    q0, q1 = qubitron.LineQubit.range(2)

    step_result = BasicStateVector({q0: 0})

    with pytest.raises(KeyError):
        step_result.density_matrix_of([q1])
    with pytest.raises(KeyError):
        step_result.density_matrix_of('junk')
    with pytest.raises(TypeError):
        step_result.density_matrix_of(0)


def test_step_result_bloch_vector():
    q0, q1 = qubitron.LineQubit.range(2)
    step_result = BasicStateVector({q0: 0, q1: 1})
    bloch1 = np.array([0, 0, -1])
    bloch0 = np.array([0, 0, 1])
    np.testing.assert_array_almost_equal(bloch1, step_result.bloch_vector_of(q1))
    np.testing.assert_array_almost_equal(bloch0, step_result.bloch_vector_of(q0))


def test_factor_validation():
    args = qubitron.Simulator()._create_simulation_state(0, qubits=qubitron.LineQubit.range(2))
    args.apply_operation(qubitron.H(qubitron.LineQubit(0)) ** 0.7)
    t = args.create_merged_state().target_tensor
    qubitron.linalg.transformations.factor_state_vector(t, [0])
    qubitron.linalg.transformations.factor_state_vector(t, [1])
    args.apply_operation(qubitron.CNOT(qubitron.LineQubit(0), qubitron.LineQubit(1)))
    t = args.create_merged_state().target_tensor
    with pytest.raises(qubitron.linalg.transformations.EntangledStateError):
        qubitron.linalg.transformations.factor_state_vector(t, [0])
    with pytest.raises(qubitron.linalg.transformations.EntangledStateError):
        qubitron.linalg.transformations.factor_state_vector(t, [1])
