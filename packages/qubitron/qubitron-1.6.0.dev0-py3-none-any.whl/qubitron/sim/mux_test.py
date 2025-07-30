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

"""Tests sampling/simulation methods that delegate to appropriate simulators."""

from __future__ import annotations

import collections

import numpy as np
import pytest
import sympy

import qubitron
import qubitron.testing


def test_sample():
    q = qubitron.NamedQubit('q')

    with pytest.raises(ValueError, match="no measurements"):
        qubitron.sample(qubitron.Circuit(qubitron.X(q)))
    # Unitary.
    results = qubitron.sample(qubitron.Circuit(qubitron.X(q), qubitron.measure(q)))
    assert results.histogram(key=q) == collections.Counter({1: 1})

    # Intermediate measurements.
    results = qubitron.sample(qubitron.Circuit(qubitron.measure(q, key='drop'), qubitron.X(q), qubitron.measure(q)))
    assert results.histogram(key='drop') == collections.Counter({0: 1})
    assert results.histogram(key=q) == collections.Counter({1: 1})

    # Overdamped everywhere.
    results = qubitron.sample(
        qubitron.Circuit(qubitron.measure(q, key='drop'), qubitron.X(q), qubitron.measure(q)),
        noise=qubitron.ConstantQubitNoiseModel(qubitron.amplitude_damp(1)),
    )
    assert results.histogram(key='drop') == collections.Counter({0: 1})
    assert results.histogram(key=q) == collections.Counter({0: 1})


def test_sample_seed_unitary():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit(qubitron.X(q) ** 0.2, qubitron.measure(q))
    result = qubitron.sample(circuit, repetitions=10, seed=1234)
    measurements = result.measurements['q']
    assert np.all(
        measurements
        == [[False], [False], [False], [False], [False], [False], [False], [False], [True], [False]]
    )


def test_sample_seed_non_unitary():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit(qubitron.depolarize(0.5).on(q), qubitron.measure(q))
    result = qubitron.sample(circuit, repetitions=10, seed=1234)
    assert np.all(
        result.measurements['q']
        == [[False], [False], [False], [True], [True], [False], [False], [True], [True], [True]]
    )


def test_sample_sweep():
    q = qubitron.NamedQubit('q')
    c = qubitron.Circuit(qubitron.X(q), qubitron.Y(q) ** sympy.Symbol('t'), qubitron.measure(q))

    # Unitary.
    results = qubitron.sample_sweep(c, qubitron.Linspace('t', 0, 1, 2), repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({1: 3})
    assert results[1].histogram(key=q) == collections.Counter({0: 3})

    # Overdamped.
    c = qubitron.Circuit(
        qubitron.X(q), qubitron.amplitude_damp(1).on(q), qubitron.Y(q) ** sympy.Symbol('t'), qubitron.measure(q)
    )
    results = qubitron.sample_sweep(c, qubitron.Linspace('t', 0, 1, 2), repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({0: 3})
    assert results[1].histogram(key=q) == collections.Counter({1: 3})

    # Overdamped everywhere.
    c = qubitron.Circuit(qubitron.X(q), qubitron.Y(q) ** sympy.Symbol('t'), qubitron.measure(q))
    results = qubitron.sample_sweep(
        c,
        qubitron.Linspace('t', 0, 1, 2),
        noise=qubitron.ConstantQubitNoiseModel(qubitron.amplitude_damp(1)),
        repetitions=3,
    )
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({0: 3})
    assert results[1].histogram(key=q) == collections.Counter({0: 3})


def test_sample_sweep_seed():
    q = qubitron.NamedQubit('q')
    circuit = qubitron.Circuit(qubitron.X(q) ** sympy.Symbol('t'), qubitron.measure(q))

    results = qubitron.sample_sweep(
        circuit, [qubitron.ParamResolver({'t': 0.5})] * 3, repetitions=2, seed=1234
    )
    assert np.all(results[0].measurements['q'] == [[False], [True]])
    assert np.all(results[1].measurements['q'] == [[False], [True]])
    assert np.all(results[2].measurements['q'] == [[True], [False]])

    results = qubitron.sample_sweep(
        circuit,
        [qubitron.ParamResolver({'t': 0.5})] * 3,
        repetitions=2,
        seed=np.random.RandomState(1234),
    )
    assert np.all(results[0].measurements['q'] == [[False], [True]])
    assert np.all(results[1].measurements['q'] == [[False], [True]])
    assert np.all(results[2].measurements['q'] == [[True], [False]])


def test_final_state_vector_different_program_types():
    a, b = qubitron.LineQubit.range(2)

    np.testing.assert_allclose(qubitron.final_state_vector(qubitron.X), [0, 1], atol=1e-8)

    ops = [qubitron.H(a), qubitron.CNOT(a, b)]

    np.testing.assert_allclose(
        qubitron.final_state_vector(ops), [np.sqrt(0.5), 0, 0, np.sqrt(0.5)], atol=1e-8
    )

    np.testing.assert_allclose(
        qubitron.final_state_vector(qubitron.Circuit(ops)), [np.sqrt(0.5), 0, 0, np.sqrt(0.5)], atol=1e-8
    )


def test_final_state_vector_initial_state():
    np.testing.assert_allclose(qubitron.final_state_vector(qubitron.X, initial_state=0), [0, 1], atol=1e-8)

    np.testing.assert_allclose(qubitron.final_state_vector(qubitron.X, initial_state=1), [1, 0], atol=1e-8)

    np.testing.assert_allclose(
        qubitron.final_state_vector(qubitron.X, initial_state=[np.sqrt(0.5), 1j * np.sqrt(0.5)]),
        [1j * np.sqrt(0.5), np.sqrt(0.5)],
        atol=1e-8,
    )


def test_final_state_vector_dtype_insensitive_to_initial_state():
    assert qubitron.final_state_vector(qubitron.X).dtype == np.complex64

    assert qubitron.final_state_vector(qubitron.X, initial_state=0).dtype == np.complex64

    assert (
        qubitron.final_state_vector(qubitron.X, initial_state=[np.sqrt(0.5), np.sqrt(0.5)]).dtype
        == np.complex64
    )

    assert (
        qubitron.final_state_vector(qubitron.X, initial_state=np.array([np.sqrt(0.5), np.sqrt(0.5)])).dtype
        == np.complex64
    )

    for t in [np.int32, np.float32, np.float64, np.complex64]:
        assert (
            qubitron.final_state_vector(qubitron.X, initial_state=np.array([1, 0], dtype=t)).dtype
            == np.complex64
        )

        assert (
            qubitron.final_state_vector(
                qubitron.X, initial_state=np.array([1, 0], dtype=t), dtype=np.complex128
            ).dtype
            == np.complex128
        )


def test_final_state_vector_param_resolver():
    s = sympy.Symbol('s')

    with pytest.raises(ValueError, match='not unitary'):
        _ = qubitron.final_state_vector(qubitron.X**s)

    np.testing.assert_allclose(
        qubitron.final_state_vector(qubitron.X**s, param_resolver={s: 0.5}), [0.5 + 0.5j, 0.5 - 0.5j]
    )


def test_final_state_vector_qubit_order():
    a, b = qubitron.LineQubit.range(2)

    np.testing.assert_allclose(
        qubitron.final_state_vector([qubitron.X(a), qubitron.X(b) ** 0.5], qubit_order=[a, b]),
        [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
    )

    np.testing.assert_allclose(
        qubitron.final_state_vector([qubitron.X(a), qubitron.X(b) ** 0.5], qubit_order=[b, a]),
        [0, 0.5 + 0.5j, 0, 0.5 - 0.5j],
    )


def test_final_state_vector_ignore_terminal_measurement():
    a, b = qubitron.LineQubit.range(2)

    np.testing.assert_allclose(
        qubitron.final_state_vector(
            [qubitron.X(a), qubitron.X(b) ** 0.5, qubitron.measure(a, b, key='m')],
            ignore_terminal_measurements=True,
        ),
        [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
    )
    with pytest.raises(ValueError, match='is not unitary'):
        _ = (
            qubitron.final_state_vector(
                [qubitron.X(a), qubitron.amplitude_damp(0.1).on(b), qubitron.measure(a, b, key='m')],
                ignore_terminal_measurements=True,
            ),
        )


@pytest.mark.parametrize('repetitions', (0, 1, 100))
def test_repetitions(repetitions):
    a = qubitron.LineQubit(0)
    c = qubitron.Circuit(qubitron.H(a), qubitron.measure(a, key='m'))
    r = qubitron.sample(c, repetitions=repetitions)
    samples = r.data['m'].to_numpy()
    assert samples.shape == (repetitions,)
    assert np.issubdtype(samples.dtype, np.integer)


def test_final_density_matrix_different_program_types():
    a, b = qubitron.LineQubit.range(2)

    np.testing.assert_allclose(qubitron.final_density_matrix(qubitron.X), [[0, 0], [0, 1]], atol=1e-8)

    ops = [qubitron.H(a), qubitron.CNOT(a, b)]

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.Circuit(ops)),
        [[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]],
        atol=1e-8,
    )


def test_final_density_matrix_initial_state():
    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.X, initial_state=0), [[0, 0], [0, 1]], atol=1e-8
    )

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.X, initial_state=1), [[1, 0], [0, 0]], atol=1e-8
    )

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.X, initial_state=[np.sqrt(0.5), 1j * np.sqrt(0.5)]),
        [[0.5, 0.5j], [-0.5j, 0.5]],
        atol=1e-8,
    )


def test_final_density_matrix_dtype_insensitive_to_initial_state():
    assert qubitron.final_density_matrix(qubitron.X).dtype == np.complex64

    assert qubitron.final_density_matrix(qubitron.X, initial_state=0).dtype == np.complex64

    assert (
        qubitron.final_density_matrix(qubitron.X, initial_state=[np.sqrt(0.5), np.sqrt(0.5)]).dtype
        == np.complex64
    )

    assert (
        qubitron.final_density_matrix(
            qubitron.X, initial_state=np.array([np.sqrt(0.5), np.sqrt(0.5)])
        ).dtype
        == np.complex64
    )

    for t in [np.int32, np.float32, np.float64, np.complex64]:
        assert (
            qubitron.final_density_matrix(qubitron.X, initial_state=np.array([1, 0], dtype=t)).dtype
            == np.complex64
        )

        assert (
            qubitron.final_density_matrix(
                qubitron.X, initial_state=np.array([1, 0], dtype=t), dtype=np.complex128
            ).dtype
            == np.complex128
        )


def test_final_density_matrix_param_resolver():
    s = sympy.Symbol('s')

    with pytest.raises(ValueError, match='not specified in parameter sweep'):
        _ = qubitron.final_density_matrix(qubitron.X**s)

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.X**s, param_resolver={s: 0.5}),
        [[0.5 - 0.0j, 0.0 + 0.5j], [0.0 - 0.5j, 0.5 - 0.0j]],
    )


def test_final_density_matrix_qubit_order():
    a, b = qubitron.LineQubit.range(2)

    np.testing.assert_allclose(
        qubitron.final_density_matrix([qubitron.X(a), qubitron.X(b) ** 0.5], qubit_order=[a, b]),
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0.5, 0.5j], [0, 0, -0.5j, 0.5]],
    )

    np.testing.assert_allclose(
        qubitron.final_density_matrix([qubitron.X(a), qubitron.X(b) ** 0.5], qubit_order=[b, a]),
        [[0, 0, 0, 0], [0, 0.5, 0, 0.5j], [0, 0, 0, 0], [0, -0.5j, 0, 0.5]],
    )

    np.testing.assert_allclose(
        qubitron.final_density_matrix(
            [qubitron.X(a), qubitron.X(b) ** 0.5],
            qubit_order=[b, a],
            noise=qubitron.ConstantQubitNoiseModel(qubitron.amplitude_damp(1.0)),
        ),
        [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    )


def test_final_density_matrix_seed_with_dephasing():
    a = qubitron.LineQubit(0)
    np.testing.assert_allclose(
        qubitron.final_density_matrix([qubitron.X(a) ** 0.5, qubitron.measure(a)], seed=123),
        [[0.5 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.5 + 0.0j]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        qubitron.final_density_matrix([qubitron.X(a) ** 0.5, qubitron.measure(a)], seed=124),
        [[0.5 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.5 + 0.0j]],
        atol=1e-4,
    )


def test_final_density_matrix_seed_with_collapsing():
    a = qubitron.LineQubit(0)
    np.testing.assert_allclose(
        qubitron.final_density_matrix(
            [qubitron.X(a) ** 0.5, qubitron.measure(a)], seed=123, ignore_measurement_results=False
        ),
        [[0, 0], [0, 1]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        qubitron.final_density_matrix(
            [qubitron.X(a) ** 0.5, qubitron.measure(a)], seed=124, ignore_measurement_results=False
        ),
        [[1, 0], [0, 0]],
        atol=1e-4,
    )


def test_final_density_matrix_noise():
    a = qubitron.LineQubit(0)
    np.testing.assert_allclose(
        qubitron.final_density_matrix([qubitron.H(a), qubitron.Z(a), qubitron.H(a), qubitron.measure(a)]),
        [[0, 0], [0, 1]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        qubitron.final_density_matrix(
            [qubitron.H(a), qubitron.Z(a), qubitron.H(a), qubitron.measure(a)],
            noise=qubitron.ConstantQubitNoiseModel(qubitron.amplitude_damp(1.0)),
        ),
        [[1, 0], [0, 0]],
        atol=1e-4,
    )


def test_ps_initial_state_wfn():
    q0, q1 = qubitron.LineQubit.range(2)
    s00 = qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1)
    sp0 = qubitron.KET_PLUS(q0) * qubitron.KET_ZERO(q1)

    np.testing.assert_allclose(
        qubitron.final_state_vector(qubitron.Circuit(qubitron.I.on_each(q0, q1))),
        qubitron.final_state_vector(qubitron.Circuit(qubitron.I.on_each(q0, q1)), initial_state=s00),
    )

    np.testing.assert_allclose(
        qubitron.final_state_vector(qubitron.Circuit(qubitron.H(q0), qubitron.I(q1))),
        qubitron.final_state_vector(qubitron.Circuit(qubitron.I.on_each(q0, q1)), initial_state=sp0),
    )


def test_ps_initial_state_dmat():
    q0, q1 = qubitron.LineQubit.range(2)
    s00 = qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1)
    sp0 = qubitron.KET_PLUS(q0) * qubitron.KET_ZERO(q1)

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.Circuit(qubitron.I.on_each(q0, q1))),
        qubitron.final_density_matrix(qubitron.Circuit(qubitron.I.on_each(q0, q1)), initial_state=s00),
    )

    np.testing.assert_allclose(
        qubitron.final_density_matrix(qubitron.Circuit(qubitron.H(q0), qubitron.I(q1))),
        qubitron.final_density_matrix(qubitron.Circuit(qubitron.I.on_each(q0, q1)), initial_state=sp0),
    )
