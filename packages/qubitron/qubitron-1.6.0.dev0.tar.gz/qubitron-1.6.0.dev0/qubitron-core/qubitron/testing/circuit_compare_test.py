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

from __future__ import annotations

import numpy as np
import pytest

import qubitron
from qubitron.testing.circuit_compare import _assert_apply_unitary_works_when_axes_transposed


def test_sensitive_to_phase():
    q = qubitron.NamedQubit('q')

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([])]), qubitron.Circuit(), atol=0
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.0001])]), qubitron.Circuit(), atol=0
        )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.Z(q) ** 0.0001])]), qubitron.Circuit(), atol=0.01
    )


def test_sensitive_to_measurement_but_not_measured_phase():
    q = qubitron.NamedQubit('q')

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.measure(q)])]), qubitron.Circuit()
        )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(q)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.Z(q)]), qubitron.Moment([qubitron.measure(q)])]),
    )

    a, b = qubitron.LineQubit.range(2)

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a, b)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.Z(a)]), qubitron.Moment([qubitron.measure(a, b)])]),
    )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.Z(a)]), qubitron.Moment([qubitron.measure(a)])]),
    )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a, b)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.T(a), qubitron.S(b)]), qubitron.Moment([qubitron.measure(a, b)])]),
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.measure(a)])]),
            qubitron.Circuit([qubitron.Moment([qubitron.T(a), qubitron.S(b)]), qubitron.Moment([qubitron.measure(a)])]),
        )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a, b)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.CZ(a, b)]), qubitron.Moment([qubitron.measure(a, b)])]),
    )


def test_sensitive_to_measurement_toggle():
    q = qubitron.NamedQubit('q')

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.measure(q)])]),
            qubitron.Circuit([qubitron.Moment([qubitron.X(q)]), qubitron.Moment([qubitron.measure(q)])]),
        )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.measure(q)])]),
            qubitron.Circuit([qubitron.Moment([qubitron.measure(q, invert_mask=(True,))])]),
        )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(q)])]),
        qubitron.Circuit(
            [qubitron.Moment([qubitron.X(q)]), qubitron.Moment([qubitron.measure(q, invert_mask=(True,))])]
        ),
    )


def test_measuring_qubits():
    a, b = qubitron.LineQubit.range(2)

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit([qubitron.Moment([qubitron.measure(a)])]),
            qubitron.Circuit([qubitron.Moment([qubitron.measure(b)])]),
        )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a, b, invert_mask=(True,))])]),
        qubitron.Circuit([qubitron.Moment([qubitron.measure(b, a, invert_mask=(False, True))])]),
    )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a)]), qubitron.Moment([qubitron.measure(b)])]),
        qubitron.Circuit([qubitron.Moment([qubitron.measure(a, b)])]),
    )


@pytest.mark.parametrize(
    'circuit', [qubitron.testing.random_circuit(qubitron.LineQubit.range(2), 4, 0.5) for _ in range(5)]
)
def test_random_same_matrix(circuit):
    a, b = qubitron.LineQubit.range(2)
    same = qubitron.Circuit(
        qubitron.MatrixGate(circuit.unitary(qubits_that_should_be_present=[a, b])).on(a, b)
    )

    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(circuit, same)

    mutable_circuit = circuit.copy()
    mutable_circuit.append(qubitron.measure(a))
    same.append(qubitron.measure(a))
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(mutable_circuit, same)


def test_correct_qubit_ordering():
    a, b = qubitron.LineQubit.range(2)
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        qubitron.Circuit(qubitron.Z(a), qubitron.Z(b), qubitron.measure(b)),
        qubitron.Circuit(qubitron.Z(a), qubitron.measure(b)),
    )

    with pytest.raises(AssertionError):
        qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            qubitron.Circuit(qubitron.Z(a), qubitron.Z(b), qubitron.measure(b)),
            qubitron.Circuit(qubitron.Z(b), qubitron.measure(b)),
        )


def test_known_old_failure():
    a, b = qubitron.LineQubit.range(2)
    qubitron.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        actual=qubitron.Circuit(
            qubitron.PhasedXPowGate(exponent=0.61351656, phase_exponent=0.8034575038876517).on(b),
            qubitron.measure(a, b),
        ),
        reference=qubitron.Circuit(
            qubitron.PhasedXPowGate(exponent=0.61351656, phase_exponent=0.8034575038876517).on(b),
            qubitron.Z(a) ** 0.5,
            qubitron.Z(b) ** 0.1,
            qubitron.measure(a, b),
        ),
    )


def test_assert_same_circuits():
    a, b = qubitron.LineQubit.range(2)

    qubitron.testing.assert_same_circuits(qubitron.Circuit(qubitron.H(a)), qubitron.Circuit(qubitron.H(a)))

    with pytest.raises(AssertionError) as exc_info:
        qubitron.testing.assert_same_circuits(qubitron.Circuit(qubitron.H(a)), qubitron.Circuit())
    assert 'differing moment:\n0\n' in exc_info.value.args[0]

    with pytest.raises(AssertionError) as exc_info:
        qubitron.testing.assert_same_circuits(
            qubitron.Circuit(qubitron.H(a), qubitron.H(a)), qubitron.Circuit(qubitron.H(a), qubitron.CZ(a, b))
        )
    assert 'differing moment:\n1\n' in exc_info.value.args[0]

    with pytest.raises(AssertionError):
        qubitron.testing.assert_same_circuits(
            qubitron.Circuit(qubitron.CNOT(a, b)), qubitron.Circuit(qubitron.ControlledGate(qubitron.X).on(a, b))
        )


def test_assert_circuits_have_same_unitary_given_final_permutation():
    q = qubitron.LineQubit.range(5)
    expected = qubitron.Circuit([qubitron.Moment(qubitron.CNOT(q[2], q[1]), qubitron.CNOT(q[3], q[0]))])
    actual = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.CNOT(q[2], q[1])),
            qubitron.Moment(qubitron.SWAP(q[0], q[2])),
            qubitron.Moment(qubitron.SWAP(q[0], q[1])),
            qubitron.Moment(qubitron.CNOT(q[3], q[2])),
        ]
    )
    qubit_map = {q[0]: q[2], q[2]: q[1], q[1]: q[0]}
    qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
        actual, expected, qubit_map
    )

    qubit_map.update({q[2]: q[3]})
    with pytest.raises(ValueError, match="'qubit_map' must have the same set"):
        qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
            actual, expected, qubit_map=qubit_map
        )

    bad_qubit_map = {q[0]: q[2], q[2]: q[4], q[4]: q[0]}
    with pytest.raises(ValueError, match="'qubit_map' must be a mapping"):
        qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
            actual, expected, qubit_map=bad_qubit_map
        )


def test_assert_has_diagram():
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit(qubitron.CNOT(a, b))
    qubitron.testing.assert_has_diagram(
        circuit,
        """
0: ───@───
      │
1: ───X───
""",
    )

    expected_error = """Circuit's text diagram differs from the desired diagram.

Diagram of actual circuit:
0: ───@───
      │
1: ───X───

Desired text diagram:
0: ───@───
      │
1: ───Z───

Highlighted differences:
0: ───@───
      │
1: ───█───

"""

    with pytest.raises(AssertionError) as ex_info:
        qubitron.testing.assert_has_diagram(
            circuit,
            """
0: ───@───
      │
1: ───Z───
""",
        )
    assert expected_error in ex_info.value.args[0]


def test_assert_has_consistent_apply_channel():
    class Correct:
        def _apply_channel_(self, args: qubitron.ApplyChannelArgs):
            args.target_tensor[...] = 0
            return args.target_tensor

        def _kraus_(self):
            return [np.array([[0, 0], [0, 0]])]

        def _num_qubits_(self):
            return 1

    qubitron.testing.assert_has_consistent_apply_channel(Correct())

    class Wrong:
        def _apply_channel_(self, args: qubitron.ApplyChannelArgs):
            args.target_tensor[...] = 0
            return args.target_tensor

        def _kraus_(self):
            return [np.array([[1, 0], [0, 0]])]

        def _num_qubits_(self):
            return 1

    with pytest.raises(AssertionError):
        qubitron.testing.assert_has_consistent_apply_channel(Wrong())

    class NoNothing:
        def _apply_channel_(self, args: qubitron.ApplyChannelArgs):
            return NotImplemented

        def _kraus_(self):
            return NotImplemented

        def _num_qubits_(self):
            return 1

    qubitron.testing.assert_has_consistent_apply_channel(NoNothing())

    class NoKraus:
        def _apply_channel_(self, args: qubitron.ApplyChannelArgs):
            return args.target_tensor

        def _kraus_(self):
            return NotImplemented

        def _num_qubits_(self):
            return 1

    with pytest.raises(AssertionError):
        qubitron.testing.assert_has_consistent_apply_channel(NoKraus())

    class NoApply:
        def _apply_channel_(self, args: qubitron.ApplyChannelArgs):
            return NotImplemented

        def _kraus_(self):
            return [np.array([[0, 0], [0, 0]])]

        def _num_qubits_(self):
            return 1

    qubitron.testing.assert_has_consistent_apply_channel(NoApply())


def test_assert_has_consistent_apply_unitary():
    class IdentityReturningUnalteredWorkspace:
        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            return args.available_buffer

        def _unitary_(self):
            return np.eye(2)  # pragma: no cover

        def _num_qubits_(self):
            return 1

    with pytest.raises(AssertionError):
        qubitron.testing.assert_has_consistent_apply_unitary(IdentityReturningUnalteredWorkspace())

    class DifferentEffect:
        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            o = args.subspace_index(0)
            i = args.subspace_index(1)
            args.available_buffer[o] = args.target_tensor[i]
            args.available_buffer[i] = args.target_tensor[o]
            return args.available_buffer

        def _unitary_(self):
            return np.eye(2, dtype=np.complex128)

        def _num_qubits_(self):
            return 1

    with pytest.raises(AssertionError):
        qubitron.testing.assert_has_consistent_apply_unitary(DifferentEffect())

    class IgnoreAxisEffect:
        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            if args.target_tensor.shape[0] > 1:
                args.available_buffer[0] = args.target_tensor[1]
                args.available_buffer[1] = args.target_tensor[0]
            return args.available_buffer

        def _unitary_(self):
            return np.array([[0, 1], [1, 0]])  # pragma: no cover

        def _num_qubits_(self):
            return 1

    with pytest.raises(AssertionError, match='Not equal|acted differently'):
        qubitron.testing.assert_has_consistent_apply_unitary(IgnoreAxisEffect())

    class SameEffect:
        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            o = args.subspace_index(0)
            i = args.subspace_index(1)
            args.available_buffer[o] = args.target_tensor[i]
            args.available_buffer[i] = args.target_tensor[o]
            return args.available_buffer

        def _unitary_(self):
            return np.array([[0, 1], [1, 0]])

        def _num_qubits_(self):
            return 1

    qubitron.testing.assert_has_consistent_apply_unitary(SameEffect())

    class SameQuditEffect:
        def _qid_shape_(self):
            return (3,)

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            args.available_buffer[..., 0] = args.target_tensor[..., 2]
            args.available_buffer[..., 1] = args.target_tensor[..., 0]
            args.available_buffer[..., 2] = args.target_tensor[..., 1]
            return args.available_buffer

        def _unitary_(self):
            return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])

    qubitron.testing.assert_has_consistent_apply_unitary(SameQuditEffect())

    class BadExponent:
        def __init__(self, power):
            self.power = power

        def __pow__(self, power):
            return BadExponent(self.power * power)

        def _num_qubits_(self):
            return 1

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            i = args.subspace_index(1)
            args.target_tensor[i] *= self.power * 2
            return args.target_tensor

        def _unitary_(self):
            return np.array([[1, 0], [0, 2]])

    qubitron.testing.assert_has_consistent_apply_unitary(BadExponent(1))

    with pytest.raises(AssertionError):
        qubitron.testing.assert_has_consistent_apply_unitary_for_various_exponents(
            BadExponent(1), exponents=[1, 2]
        )

    class EffectWithoutUnitary:
        def _num_qubits_(self):
            return 1

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            return args.target_tensor

    qubitron.testing.assert_has_consistent_apply_unitary(EffectWithoutUnitary())

    class NoEffect:
        def _num_qubits_(self):
            return 1

        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs) -> np.ndarray:
            return NotImplemented

    qubitron.testing.assert_has_consistent_apply_unitary(NoEffect())

    class UnknownCountEffect:
        pass

    with pytest.raises(TypeError, match="no _num_qubits_ or _qid_shape_"):
        qubitron.testing.assert_has_consistent_apply_unitary(UnknownCountEffect())

    qubitron.testing.assert_has_consistent_apply_unitary(qubitron.X)

    qubitron.testing.assert_has_consistent_apply_unitary(qubitron.X.on(qubitron.NamedQubit('q')))


def test_assert_has_consistent_qid_shape():
    class ConsistentGate(qubitron.Gate):
        def _num_qubits_(self):
            return 4

        def _qid_shape_(self):
            return 1, 2, 3, 4

    class InconsistentGate(qubitron.Gate):
        def _num_qubits_(self):
            return 2

        def _qid_shape_(self):
            return 1, 2, 3, 4

    class BadShapeGate(qubitron.Gate):
        def _num_qubits_(self):
            return 4

        def _qid_shape_(self):
            return 1, 2, 0, 4

    class ConsistentOp(qubitron.Operation):
        def with_qubits(self, *qubits):
            raise NotImplementedError

        @property
        def qubits(self):
            return qubitron.LineQubit.range(4)

        def _num_qubits_(self):
            return 4

        def _qid_shape_(self):
            return (1, 2, 3, 4)

    # The 'pragma: no cover' comments in the InconsistentOp classes is needed
    # because test_assert_has_consistent_qid_shape may only need to check two of
    # the three methods before finding an inconsistency and throwing an error.
    class InconsistentOp1(qubitron.Operation):
        def with_qubits(self, *qubits):
            raise NotImplementedError

        @property
        def qubits(self):
            return qubitron.LineQubit.range(2)

        def _num_qubits_(self):
            return 4  # pragma: no cover

        def _qid_shape_(self):
            return (1, 2, 3, 4)  # pragma: no cover

    class InconsistentOp2(qubitron.Operation):
        def with_qubits(self, *qubits):
            raise NotImplementedError

        @property
        def qubits(self):
            return qubitron.LineQubit.range(4)  # pragma: no cover

        def _num_qubits_(self):
            return 2

        def _qid_shape_(self):
            return (1, 2, 3, 4)  # pragma: no cover

    class InconsistentOp3(qubitron.Operation):
        def with_qubits(self, *qubits):
            raise NotImplementedError

        @property
        def qubits(self):
            return qubitron.LineQubit.range(4)  # pragma: no cover

        def _num_qubits_(self):
            return 4  # pragma: no cover

        def _qid_shape_(self):
            return 1, 2

    class NoProtocol:
        pass

    qubitron.testing.assert_has_consistent_qid_shape(ConsistentGate())
    with pytest.raises(AssertionError, match='disagree'):
        qubitron.testing.assert_has_consistent_qid_shape(InconsistentGate())
    with pytest.raises(AssertionError, match='positive'):
        qubitron.testing.assert_has_consistent_qid_shape(BadShapeGate())
    qubitron.testing.assert_has_consistent_qid_shape(ConsistentOp())
    with pytest.raises(AssertionError, match='disagree'):
        qubitron.testing.assert_has_consistent_qid_shape(InconsistentOp1())
    with pytest.raises(AssertionError, match='disagree'):
        qubitron.testing.assert_has_consistent_qid_shape(InconsistentOp2())
    with pytest.raises(AssertionError, match='disagree'):
        qubitron.testing.assert_has_consistent_qid_shape(InconsistentOp3())
    qubitron.testing.assert_has_consistent_qid_shape(NoProtocol())


def test_assert_apply_unitary_works_when_axes_transposed_failure():
    class BadOp:
        def _apply_unitary_(self, args: qubitron.ApplyUnitaryArgs):
            # Get a more convenient view of the data.
            a, b = args.axes
            rest = list(range(len(args.target_tensor.shape)))
            rest.remove(a)
            rest.remove(b)
            size = args.target_tensor.size
            view = args.target_tensor.transpose([a, b, *rest])
            view = view.reshape((4, size // 4))  # Oops. Reshape might copy.

            # Apply phase gradient.
            view[1, ...] *= 1j
            view[2, ...] *= -1
            view[3, ...] *= -1j
            return args.target_tensor

        def _num_qubits_(self):
            return 2

    bad_op = BadOp()
    assert qubitron.has_unitary(bad_op)

    # Appears to work.
    np.testing.assert_allclose(qubitron.unitary(bad_op), np.diag([1, 1j, -1, -1j]))
    # But fails the more discerning test.
    with pytest.raises(AssertionError, match='acted differently on out-of-order axes'):
        for _ in range(100):  # Axis orders chosen at random. Brute force a hit.
            _assert_apply_unitary_works_when_axes_transposed(bad_op)
