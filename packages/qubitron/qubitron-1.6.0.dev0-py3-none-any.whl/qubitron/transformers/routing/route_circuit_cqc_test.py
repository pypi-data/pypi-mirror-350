# Copyright 2022 The Qubitron Developers
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

import pytest

import qubitron


def test_directed_device() -> None:
    device = qubitron.testing.construct_ring_device(10, directed=True)
    device_graph = device.metadata.nx_graph
    with pytest.raises(ValueError, match="Device graph must be undirected."):
        qubitron.RouteCQC(device_graph)


@pytest.mark.parametrize(
    "n_qubits, n_moments, op_density, seed",
    [
        (8, size, op_density, seed)
        for size in [50, 100]
        for seed in range(3)
        for op_density in [0.3, 0.5, 0.7]
    ],
)
def test_route_small_circuit_random(n_qubits, n_moments, op_density, seed) -> None:
    c_orig = qubitron.testing.random_circuit(
        qubits=n_qubits, n_moments=n_moments, op_density=op_density, random_state=seed
    )
    device = qubitron.testing.construct_grid_device(4, 4)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    c_routed, imap, swap_map = router.route_circuit(c_orig, tag_inserted_swaps=True)
    device.validate_circuit(c_routed)
    qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
        c_routed, c_orig.transform_qubits(imap), swap_map
    )


def test_high_qubit_count() -> None:
    c_orig = qubitron.testing.random_circuit(qubits=40, n_moments=350, op_density=0.4, random_state=0)
    device = qubitron.testing.construct_grid_device(7, 7)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    c_routed = router(c_orig)
    device.validate_circuit(c_routed)


def test_multi_qubit_gate_inputs() -> None:
    device = qubitron.testing.construct_grid_device(4, 4)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    q = qubitron.LineQubit.range(5)

    invalid_subcircuit_op = qubitron.CircuitOperation(
        qubitron.Circuit(qubitron.X(q[1]), qubitron.CCZ(q[0], q[1], q[2]), qubitron.Y(q[1])).freeze()
    ).with_tags('<mapped_circuit_op>')
    invalid_circuit = qubitron.Circuit(qubitron.H(q[0]), qubitron.H(q[2]), invalid_subcircuit_op)
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=qubitron.TransformerContext(deep=True))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=qubitron.TransformerContext(deep=False))

    invalid_circuit = qubitron.Circuit(qubitron.CCX(q[0], q[1], q[2]))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=qubitron.TransformerContext(deep=True))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=qubitron.TransformerContext(deep=False))

    valid_subcircuit_op = qubitron.CircuitOperation(
        qubitron.Circuit(qubitron.X(q[1]), qubitron.CZ(q[0], q[1]), qubitron.CZ(q[1], q[2]), qubitron.Y(q[1])).freeze()
    ).with_tags('<mapped_circuit_op>')
    valid_circuit = qubitron.Circuit(qubitron.H(q[0]), qubitron.H(q[2]), valid_subcircuit_op)
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=qubitron.TransformerContext(deep=False))
    c_routed = router(valid_circuit, context=qubitron.TransformerContext(deep=True))
    device.validate_circuit(c_routed)


def test_circuit_with_measurement_gates() -> None:
    device = qubitron.testing.construct_ring_device(3)
    device_graph = device.metadata.nx_graph
    q = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(qubitron.MeasurementGate(2).on(q[0], q[2]), qubitron.MeasurementGate(3).on(*q))
    hard_coded_mapper = qubitron.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = qubitron.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    qubitron.testing.assert_same_circuits(routed_circuit, circuit)


def test_circuit_with_two_qubit_intermediate_measurement_gate() -> None:
    device = qubitron.testing.construct_ring_device(2)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    qs = qubitron.LineQubit.range(2)
    hard_coded_mapper = qubitron.HardCodedInitialMapper({qs[i]: qs[i] for i in range(2)})
    circuit = qubitron.Circuit([qubitron.Moment(qubitron.measure(qs)), qubitron.Moment(qubitron.H.on_each(qs))])
    routed_circuit = router(
        circuit, initial_mapper=hard_coded_mapper, context=qubitron.TransformerContext(deep=True)
    )
    device.validate_circuit(routed_circuit)


def test_circuit_with_multi_qubit_intermediate_measurement_gate_and_with_default_key() -> None:
    device = qubitron.testing.construct_ring_device(3)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    qs = qubitron.LineQubit.range(3)
    hard_coded_mapper = qubitron.HardCodedInitialMapper({qs[i]: qs[i] for i in range(3)})
    circuit = qubitron.Circuit([qubitron.Moment(qubitron.measure(qs)), qubitron.Moment(qubitron.H.on_each(qs))])
    routed_circuit = router(
        circuit, initial_mapper=hard_coded_mapper, context=qubitron.TransformerContext(deep=True)
    )
    expected = qubitron.Circuit([qubitron.Moment(qubitron.measure_each(qs)), qubitron.Moment(qubitron.H.on_each(qs))])
    qubitron.testing.assert_same_circuits(routed_circuit, expected)


def test_circuit_with_multi_qubit_intermediate_measurement_gate_with_custom_key() -> None:
    device = qubitron.testing.construct_ring_device(3)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    qs = qubitron.LineQubit.range(3)
    hard_coded_mapper = qubitron.HardCodedInitialMapper({qs[i]: qs[i] for i in range(3)})
    circuit = qubitron.Circuit(
        [qubitron.Moment(qubitron.measure(qs, key="test")), qubitron.Moment(qubitron.H.on_each(qs))]
    )
    with pytest.raises(ValueError):
        _ = router(
            circuit, initial_mapper=hard_coded_mapper, context=qubitron.TransformerContext(deep=True)
        )


def test_circuit_with_non_unitary_and_global_phase() -> None:
    device = qubitron.testing.construct_ring_device(4)
    device_graph = device.metadata.nx_graph
    q = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.CNOT(q[0], q[1]), qubitron.global_phase_operation(-1)),
            qubitron.Moment(qubitron.CNOT(q[1], q[2])),
            qubitron.Moment(qubitron.depolarize(0.1, 2).on(q[0], q[2]), qubitron.depolarize(0.1).on(q[1])),
        ]
    )
    hard_coded_mapper = qubitron.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = qubitron.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    expected = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.CNOT(q[0], q[1]), qubitron.global_phase_operation(-1)),
            qubitron.Moment(qubitron.CNOT(q[1], q[2])),
            qubitron.Moment(qubitron.depolarize(0.1).on(q[1])),
            qubitron.Moment(qubitron.SWAP(q[0], q[1])),
            qubitron.Moment(qubitron.depolarize(0.1, 2).on(q[1], q[2])),
        ]
    )
    qubitron.testing.assert_same_circuits(routed_circuit, expected)


def test_circuit_with_tagged_ops() -> None:
    device = qubitron.testing.construct_ring_device(4)
    device_graph = device.metadata.nx_graph
    q = qubitron.LineQubit.range(3)
    circuit = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.CNOT(q[0], q[1]).with_tags("u")),
            qubitron.Moment(qubitron.CNOT(q[1], q[2])),
            qubitron.Moment(qubitron.CNOT(q[0], q[2]).with_tags("u")),
            qubitron.Moment(qubitron.X(q[0]).with_tags("u")),
            qubitron.Moment(qubitron.X(q[0]).with_tags("u")),
        ]
    )
    hard_coded_mapper = qubitron.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = qubitron.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    expected = qubitron.Circuit(
        [
            qubitron.Moment(qubitron.TaggedOperation(qubitron.CNOT(q[0], q[1]), 'u')),
            qubitron.Moment(qubitron.CNOT(q[1], q[2])),
            qubitron.Moment(qubitron.SWAP(q[0], q[1])),
            qubitron.Moment(qubitron.TaggedOperation(qubitron.CNOT(q[1], q[2]), 'u')),
            qubitron.Moment(qubitron.TaggedOperation(qubitron.X(q[1]), 'u')),
            qubitron.Moment(qubitron.TaggedOperation(qubitron.X(q[1]), 'u')),
        ]
    )
    qubitron.testing.assert_same_circuits(routed_circuit, expected)


def test_already_valid_circuit() -> None:
    device = qubitron.testing.construct_ring_device(10)
    device_graph = device.metadata.nx_graph
    circuit = qubitron.Circuit(
        [qubitron.Moment(qubitron.CNOT(qubitron.LineQubit(i), qubitron.LineQubit(i + 1))) for i in range(9)],
        qubitron.X(qubitron.LineQubit(1)),
    )
    hard_coded_mapper = qubitron.HardCodedInitialMapper(
        {qubitron.LineQubit(i): qubitron.LineQubit(i) for i in range(10)}
    )
    router = qubitron.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)

    device.validate_circuit(routed_circuit)
    qubitron.testing.assert_same_circuits(routed_circuit, circuit)


def test_empty_circuit() -> None:
    device = qubitron.testing.construct_grid_device(5, 5)
    device_graph = device.metadata.nx_graph
    empty_circuit = qubitron.Circuit()
    router = qubitron.RouteCQC(device_graph)
    empty_circuit_routed = router(empty_circuit)

    device.validate_circuit(empty_circuit_routed)
    assert len(list(empty_circuit.all_operations())) == len(
        list(empty_circuit_routed.all_operations())
    )


def test_repr() -> None:
    device = qubitron.testing.construct_ring_device(10)
    device_graph = device.metadata.nx_graph
    router = qubitron.RouteCQC(device_graph)
    qubitron.testing.assert_equivalent_repr(router, setup_code='import qubitron\nimport networkx as nx')
