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

from typing import Sequence

import numpy as np
import pytest

import qubitron
from qubitron import ops
from qubitron.devices.noise_model import validate_all_measurements
from qubitron.testing import assert_equivalent_op_tree


def assert_equivalent_op_tree_sequence(x: Sequence[qubitron.OP_TREE], y: Sequence[qubitron.OP_TREE]):
    assert len(x) == len(y)
    for a, b in zip(x, y):
        assert_equivalent_op_tree(a, b)


def test_requires_one_override():
    class C(qubitron.NoiseModel):
        pass

    with pytest.raises(TypeError, match='abstract'):
        _ = C()


def test_infers_other_methods():
    q = qubitron.LineQubit(0)

    class NoiseModelWithNoisyMomentListMethod(qubitron.NoiseModel):
        def noisy_moments(self, moments, system_qubits):
            result = []
            for moment in moments:
                if moment.operations:
                    result.append(
                        qubitron.X(moment.operations[0].qubits[0]).with_tags(ops.VirtualTag())
                    )
                else:
                    result.append([])
            return result

    a = NoiseModelWithNoisyMomentListMethod()
    assert_equivalent_op_tree(a.noisy_operation(qubitron.H(q)), qubitron.X(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        a.noisy_moment(qubitron.Moment([qubitron.H(q)]), [q]), qubitron.X(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        a.noisy_moments([qubitron.Moment(), qubitron.Moment([qubitron.H(q)])], [q]),
        [[], qubitron.X(q).with_tags(ops.VirtualTag())],
    )

    class NoiseModelWithNoisyMomentMethod(qubitron.NoiseModel):
        def noisy_moment(self, moment, system_qubits):
            return [y.with_tags(ops.VirtualTag()) for y in qubitron.Y.on_each(*moment.qubits)]

    b = NoiseModelWithNoisyMomentMethod()
    assert_equivalent_op_tree(b.noisy_operation(qubitron.H(q)), qubitron.Y(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        b.noisy_moment(qubitron.Moment([qubitron.H(q)]), [q]), qubitron.Y(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        b.noisy_moments([qubitron.Moment(), qubitron.Moment([qubitron.H(q)])], [q]),
        [[], qubitron.Y(q).with_tags(ops.VirtualTag())],
    )

    class NoiseModelWithNoisyOperationMethod(qubitron.NoiseModel):
        def noisy_operation(self, operation: qubitron.Operation):
            return qubitron.Z(operation.qubits[0]).with_tags(ops.VirtualTag())

    c = NoiseModelWithNoisyOperationMethod()
    assert_equivalent_op_tree(c.noisy_operation(qubitron.H(q)), qubitron.Z(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        c.noisy_moment(qubitron.Moment([qubitron.H(q)]), [q]), qubitron.Z(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        c.noisy_moments([qubitron.Moment(), qubitron.Moment([qubitron.H(q)])], [q]),
        [[], qubitron.Z(q).with_tags(ops.VirtualTag())],
    )


def test_no_noise():
    q = qubitron.LineQubit(0)
    m = qubitron.Moment([qubitron.X(q)])
    assert qubitron.NO_NOISE.noisy_operation(qubitron.X(q)) == qubitron.X(q)
    assert qubitron.NO_NOISE.noisy_moment(m, [q]) is m
    assert qubitron.NO_NOISE.noisy_moments([m, m], [q]) == [m, m]
    assert qubitron.NO_NOISE == qubitron.NO_NOISE
    assert str(qubitron.NO_NOISE) == '(no noise)'
    qubitron.testing.assert_equivalent_repr(qubitron.NO_NOISE)


def test_constant_qubit_noise():
    a, b, c = qubitron.LineQubit.range(3)
    damp = qubitron.amplitude_damp(0.5)
    damp_all = qubitron.ConstantQubitNoiseModel(damp)
    actual = damp_all.noisy_moments([qubitron.Moment([qubitron.X(a)]), qubitron.Moment()], [a, b, c])
    expected = [
        [
            qubitron.Moment([qubitron.X(a)]),
            qubitron.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
        ],
        [
            qubitron.Moment(),
            qubitron.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
        ],
    ]
    assert actual == expected
    qubitron.testing.assert_equivalent_repr(damp_all)

    with pytest.raises(ValueError, match='num_qubits'):
        _ = qubitron.ConstantQubitNoiseModel(qubitron.CNOT**0.01)


def test_constant_qubit_noise_prepend():
    a, b, c = qubitron.LineQubit.range(3)
    damp = qubitron.amplitude_damp(0.5)
    damp_all = qubitron.ConstantQubitNoiseModel(damp, prepend=True)
    actual = damp_all.noisy_moments([qubitron.Moment([qubitron.X(a)]), qubitron.Moment()], [a, b, c])
    expected = [
        [
            qubitron.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
            qubitron.Moment([qubitron.X(a)]),
        ],
        [
            qubitron.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
            qubitron.Moment(),
        ],
    ]
    assert actual == expected
    qubitron.testing.assert_equivalent_repr(damp_all)


def test_noise_composition():
    # Verify that noise models can be composed without regard to ordering, as
    # long as the noise operators commute with one another.
    a, b, c = qubitron.LineQubit.range(3)
    noise_z = qubitron.ConstantQubitNoiseModel(qubitron.Z)
    noise_inv_s = qubitron.ConstantQubitNoiseModel(qubitron.S**-1)
    base_moments = [qubitron.Moment([qubitron.X(a)]), qubitron.Moment([qubitron.Y(b)]), qubitron.Moment([qubitron.H(c)])]
    circuit_z = qubitron.Circuit(noise_z.noisy_moments(base_moments, [a, b, c]))
    circuit_s = qubitron.Circuit(noise_inv_s.noisy_moments(base_moments, [a, b, c]))
    actual_zs = qubitron.Circuit(noise_inv_s.noisy_moments(circuit_z.moments, [a, b, c]))
    actual_sz = qubitron.Circuit(noise_z.noisy_moments(circuit_s.moments, [a, b, c]))

    expected_circuit = qubitron.Circuit(
        qubitron.Moment([qubitron.X(a)]),
        qubitron.Moment([qubitron.S(a), qubitron.S(b), qubitron.S(c)]),
        qubitron.Moment([qubitron.Y(b)]),
        qubitron.Moment([qubitron.S(a), qubitron.S(b), qubitron.S(c)]),
        qubitron.Moment([qubitron.H(c)]),
        qubitron.Moment([qubitron.S(a), qubitron.S(b), qubitron.S(c)]),
    )

    # All of the gates will be the same, just out of order. Merging fixes this.
    actual_zs = qubitron.merge_single_qubit_gates_to_phased_x_and_z(actual_zs)
    actual_sz = qubitron.merge_single_qubit_gates_to_phased_x_and_z(actual_sz)
    expected_circuit = qubitron.merge_single_qubit_gates_to_phased_x_and_z(expected_circuit)
    assert_equivalent_op_tree(actual_zs, actual_sz)
    assert_equivalent_op_tree(actual_zs, expected_circuit)


def test_constant_qubit_noise_repr():
    qubitron.testing.assert_equivalent_repr(qubitron.ConstantQubitNoiseModel(qubitron.X**0.01))


def test_wrap():
    class Forget(qubitron.NoiseModel):
        def noisy_operation(self, operation):
            raise NotImplementedError()

    forget = Forget()

    assert qubitron.NoiseModel.from_noise_model_like(None) is qubitron.NO_NOISE
    assert qubitron.NoiseModel.from_noise_model_like(
        qubitron.depolarize(0.1)
    ) == qubitron.ConstantQubitNoiseModel(qubitron.depolarize(0.1))
    assert qubitron.NoiseModel.from_noise_model_like(qubitron.Z**0.01) == qubitron.ConstantQubitNoiseModel(
        qubitron.Z**0.01
    )
    assert qubitron.NoiseModel.from_noise_model_like(forget) is forget

    with pytest.raises(TypeError, match='Expected a NOISE_MODEL_LIKE'):
        _ = qubitron.NoiseModel.from_noise_model_like('test')

    with pytest.raises(ValueError, match='Multi-qubit gate'):
        _ = qubitron.NoiseModel.from_noise_model_like(qubitron.CZ**0.01)


def test_gate_substitution_noise_model():
    def _overrotation(op):
        if isinstance(op.gate, qubitron.XPowGate):
            return qubitron.XPowGate(exponent=op.gate.exponent + 0.1).on(*op.qubits)
        return op

    noise = qubitron.devices.noise_model.GateSubstitutionNoiseModel(_overrotation)

    q0 = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.X(q0) ** 0.5, qubitron.Y(q0))
    circuit2 = qubitron.Circuit(qubitron.X(q0) ** 0.6, qubitron.Y(q0))
    rho1 = qubitron.final_density_matrix(circuit, noise=noise)
    rho2 = qubitron.final_density_matrix(circuit2)
    np.testing.assert_allclose(rho1, rho2)


def test_moment_is_measurements():
    q = qubitron.LineQubit.range(2)
    circ = qubitron.Circuit([qubitron.X(q[0]), qubitron.X(q[1]), qubitron.measure(*q, key='z')])
    assert not validate_all_measurements(circ[0])
    assert validate_all_measurements(circ[1])


def test_moment_is_measurements_mixed1():
    q = qubitron.LineQubit.range(2)
    circ = qubitron.Circuit([qubitron.X(q[0]), qubitron.X(q[1]), qubitron.measure(q[0], key='z'), qubitron.Z(q[1])])
    assert not validate_all_measurements(circ[0])
    with pytest.raises(ValueError) as e:
        validate_all_measurements(circ[1])
    assert e.match(".*must be homogeneous: all measurements.*")


def test_moment_is_measurements_mixed2():
    q = qubitron.LineQubit.range(2)
    circ = qubitron.Circuit([qubitron.X(q[0]), qubitron.X(q[1]), qubitron.Z(q[0]), qubitron.measure(q[1], key='z')])
    assert not validate_all_measurements(circ[0])
    with pytest.raises(ValueError) as e:
        validate_all_measurements(circ[1])
    assert e.match(".*must be homogeneous: all measurements.*")
