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

import qubitron


def test_default_parameter() -> None:
    qid_shape = (2,)
    tensor = qubitron.to_valid_density_matrix(
        0, len(qid_shape), qid_shape=qid_shape, dtype=np.complex64
    )
    args = qubitron.DensityMatrixSimulationState(qubits=qubitron.LineQubit.range(1), initial_state=0)
    np.testing.assert_almost_equal(args.target_tensor, tensor)
    assert len(args.available_buffer) == 3
    for buffer in args.available_buffer:
        assert buffer.shape == tensor.shape
        assert buffer.dtype == tensor.dtype
    assert args.qid_shape == qid_shape


def test_shallow_copy_buffers() -> None:
    args = qubitron.DensityMatrixSimulationState(qubits=qubitron.LineQubit.range(1), initial_state=0)
    copy = args.copy(deep_copy_buffers=False)
    assert copy.available_buffer is args.available_buffer


def test_decomposed_fallback() -> None:
    class Composite(qubitron.Gate):
        def num_qubits(self) -> int:
            return 1

        def _decompose_(self, qubits):
            yield qubitron.X(*qubits)

    args = qubitron.DensityMatrixSimulationState(
        qubits=qubitron.LineQubit.range(1),
        prng=np.random.RandomState(),
        initial_state=0,
        dtype=np.complex64,
    )

    qubitron.act_on(Composite(), args, qubitron.LineQubit.range(1))
    np.testing.assert_allclose(
        args.target_tensor, qubitron.one_hot(index=(1, 1), shape=(2, 2), dtype=np.complex64)
    )


def test_cannot_act() -> None:
    class NoDetails:
        pass

    args = qubitron.DensityMatrixSimulationState(
        qubits=qubitron.LineQubit.range(1),
        prng=np.random.RandomState(),
        initial_state=0,
        dtype=np.complex64,
    )
    with pytest.raises(TypeError, match="Can't simulate operations"):
        qubitron.act_on(NoDetails(), args, qubits=())


def test_qid_shape_error() -> None:
    with pytest.raises(ValueError, match="qid_shape must be provided"):
        qubitron.sim.density_matrix_simulation_state._BufferedDensityMatrix.create(initial_state=0)


def test_initial_state_vector() -> None:
    qubits = qubitron.LineQubit.range(3)
    args = qubitron.DensityMatrixSimulationState(
        qubits=qubits, initial_state=np.full((8,), 1 / np.sqrt(8)), dtype=np.complex64
    )
    assert args.target_tensor.shape == (2, 2, 2, 2, 2, 2)

    args2 = qubitron.DensityMatrixSimulationState(
        qubits=qubits, initial_state=np.full((2, 2, 2), 1 / np.sqrt(8)), dtype=np.complex64
    )
    assert args2.target_tensor.shape == (2, 2, 2, 2, 2, 2)


def test_initial_state_matrix() -> None:
    qubits = qubitron.LineQubit.range(3)
    args = qubitron.DensityMatrixSimulationState(
        qubits=qubits, initial_state=np.full((8, 8), 1 / 8), dtype=np.complex64
    )
    assert args.target_tensor.shape == (2, 2, 2, 2, 2, 2)

    args2 = qubitron.DensityMatrixSimulationState(
        qubits=qubits, initial_state=np.full((2, 2, 2, 2, 2, 2), 1 / 8), dtype=np.complex64
    )
    assert args2.target_tensor.shape == (2, 2, 2, 2, 2, 2)


def test_initial_state_bad_shape() -> None:
    qubits = qubitron.LineQubit.range(3)
    with pytest.raises(ValueError, match="Invalid quantum state"):
        qubitron.DensityMatrixSimulationState(
            qubits=qubits, initial_state=np.full((4,), 1 / 2), dtype=np.complex64
        )
    with pytest.raises(ValueError, match="Invalid quantum state"):
        qubitron.DensityMatrixSimulationState(
            qubits=qubits, initial_state=np.full((2, 2), 1 / 2), dtype=np.complex64
        )

    with pytest.raises(ValueError, match="Invalid quantum state"):
        qubitron.DensityMatrixSimulationState(
            qubits=qubits, initial_state=np.full((4, 4), 1 / 4), dtype=np.complex64
        )
    with pytest.raises(ValueError, match="Invalid quantum state"):
        qubitron.DensityMatrixSimulationState(
            qubits=qubits, initial_state=np.full((2, 2, 2, 2), 1 / 4), dtype=np.complex64
        )
