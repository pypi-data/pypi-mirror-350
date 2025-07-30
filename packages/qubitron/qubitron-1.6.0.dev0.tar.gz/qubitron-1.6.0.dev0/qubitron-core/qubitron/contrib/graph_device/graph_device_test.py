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

import pytest

import qubitron
import qubitron.contrib.graph_device as ccgd
import qubitron.contrib.graph_device.graph_device as ccgdgd


def test_fixed_duration_undirected_graph_device_edge_eq():
    e = ccgd.FixedDurationUndirectedGraphDeviceEdge(qubitron.Duration(picos=4))
    f = ccgd.FixedDurationUndirectedGraphDeviceEdge(qubitron.Duration(picos=4))
    g = ccgd.FixedDurationUndirectedGraphDeviceEdge(qubitron.Duration(picos=5))
    assert e == f
    assert e != g
    assert e != 4


def test_unconstrained_undirected_graph_device_edge_eq():
    e = ccgdgd._UnconstrainedUndirectedGraphDeviceEdge()
    f = ccgd.UnconstrainedUndirectedGraphDeviceEdge
    assert e == f
    assert e != 3


def test_is_undirected_device_graph():
    assert not ccgd.is_undirected_device_graph('abc')
    graph = ccgd.UndirectedHypergraph()
    assert ccgd.is_undirected_device_graph(graph)
    a, b, c, d, e = qubitron.LineQubit.range(5)
    graph.add_edge((a, b))
    assert ccgd.is_undirected_device_graph(graph)
    graph.add_edge((b, c), ccgd.UnconstrainedUndirectedGraphDeviceEdge)
    assert ccgd.is_undirected_device_graph(graph)
    graph.add_edge((d, e), 'abc')
    assert not ccgd.is_undirected_device_graph(graph)
    graph = ccgd.UndirectedHypergraph(vertices=(0, 1))
    assert not ccgd.is_undirected_device_graph(graph)


def test_is_crosstalk_graph():
    a, b, c, d, e, f = qubitron.LineQubit.range(6)
    assert not ccgd.is_crosstalk_graph('abc')
    graph = ccgd.UndirectedHypergraph()
    graph.add_vertex('abc')
    assert not ccgd.is_crosstalk_graph(graph)
    graph = ccgd.UndirectedHypergraph()
    graph.add_edge((frozenset((a, b)), frozenset((c, d))), 'abc')
    assert not ccgd.is_crosstalk_graph(graph)
    graph = ccgd.UndirectedHypergraph()
    graph.add_edge((frozenset((a, b)), frozenset((c, d))), None)
    graph.add_edge((frozenset((e, f)), frozenset((c, d))), lambda _: None)
    assert ccgd.is_crosstalk_graph(graph)
    graph = ccgd.UndirectedHypergraph()
    graph.add_edge((frozenset((a, b)), frozenset((c, d))), 'abc')
    assert not ccgd.is_crosstalk_graph(graph)
    graph = ccgd.UndirectedHypergraph()
    graph.add_edge((frozenset((a, b)),), None)
    assert not ccgd.is_crosstalk_graph(graph)
    graph = ccgd.UndirectedHypergraph()
    graph.add_edge((frozenset((0, 1)), frozenset((2, 3))), None)
    assert not ccgd.is_crosstalk_graph(graph)


def test_unconstrained_undirected_graph_device_edge():
    edge = ccgd.UnconstrainedUndirectedGraphDeviceEdge
    qubits = qubitron.LineQubit.range(2)
    assert edge.duration_of(qubitron.X(qubits[0])) == qubitron.Duration(picos=0)
    assert edge.duration_of(qubitron.CZ(*qubits[:2])) == qubitron.Duration(picos=0)


def test_graph_device():
    one_qubit_duration = qubitron.Duration(picos=10)
    two_qubit_duration = qubitron.Duration(picos=1)
    one_qubit_edge = ccgd.FixedDurationUndirectedGraphDeviceEdge(one_qubit_duration)
    two_qubit_edge = ccgd.FixedDurationUndirectedGraphDeviceEdge(two_qubit_duration)

    empty_device = ccgd.UndirectedGraphDevice()
    assert not empty_device.qubits
    assert not empty_device.edges

    n_qubits = 4
    qubits = qubitron.LineQubit.range(n_qubits)
    edges = {
        (qubitron.LineQubit(i), qubitron.LineQubit((i + 1) % n_qubits)): two_qubit_edge
        for i in range(n_qubits)
    }
    edges.update({(qubitron.LineQubit(i),): one_qubit_edge for i in range(n_qubits)})
    device_graph = ccgd.UndirectedHypergraph(labelled_edges=edges)

    def not_cnots(first_op, second_op):
        if all(
            isinstance(op, qubitron.GateOperation) and op.gate == qubitron.CNOT
            for op in (first_op, second_op)
        ):
            raise ValueError('Simultaneous CNOTs')

    assert ccgd.is_undirected_device_graph(device_graph)
    with pytest.raises(TypeError):
        ccgd.UndirectedGraphDevice('abc')
    constraint_edges = {
        (frozenset(qubitron.LineQubit.range(2)), frozenset(qubitron.LineQubit.range(2, 4))): None,
        (
            frozenset(qubitron.LineQubit.range(1, 3)),
            frozenset((qubitron.LineQubit(0), qubitron.LineQubit(3))),
        ): not_cnots,
    }
    crosstalk_graph = ccgd.UndirectedHypergraph(labelled_edges=constraint_edges)
    assert ccgd.is_crosstalk_graph(crosstalk_graph)

    with pytest.raises(TypeError):
        ccgd.UndirectedGraphDevice(device_graph, crosstalk_graph='abc')

    graph_device = ccgd.UndirectedGraphDevice(device_graph)
    assert graph_device.crosstalk_graph == ccgd.UndirectedHypergraph()

    graph_device = ccgd.UndirectedGraphDevice(device_graph, crosstalk_graph=crosstalk_graph)
    assert sorted(graph_device.edges) == sorted(device_graph.edges)
    assert graph_device.qubits == tuple(qubits)
    assert graph_device.device_graph == device_graph
    assert graph_device.labelled_edges == device_graph.labelled_edges

    assert graph_device.duration_of(qubitron.X(qubits[2])) == one_qubit_duration
    assert graph_device.duration_of(qubitron.CNOT(*qubits[:2])) == two_qubit_duration
    with pytest.raises(KeyError):
        graph_device.duration_of(qubitron.CNOT(qubits[0], qubits[2]))
    with pytest.raises(ValueError):
        graph_device.validate_operation(qubitron.CNOT(qubits[0], qubits[2]))
    with pytest.raises(AttributeError):
        graph_device.validate_operation(list((2, 3)))

    moment = qubitron.Moment([qubitron.CNOT(*qubits[:2]), qubitron.CNOT(*qubits[2:])])
    with pytest.raises(ValueError):
        graph_device.validate_moment(moment)

    moment = qubitron.Moment([qubitron.CNOT(qubits[0], qubits[3]), qubitron.CZ(qubits[1], qubits[2])])
    graph_device.validate_moment(moment)

    moment = qubitron.Moment([qubitron.CNOT(qubits[0], qubits[3]), qubitron.CNOT(qubits[1], qubits[2])])
    with pytest.raises(ValueError):
        graph_device.validate_moment(moment)


def test_graph_device_copy_and_add():
    a, b, c, d, e, f = qubitron.LineQubit.range(6)
    device_graph = ccgd.UndirectedHypergraph(labelled_edges={(a, b): None, (c, d): None})
    crosstalk_graph = ccgd.UndirectedHypergraph(
        labelled_edges={(frozenset((a, b)), frozenset((c, d))): None}
    )
    device = ccgd.UndirectedGraphDevice(device_graph=device_graph, crosstalk_graph=crosstalk_graph)
    device_graph_addend = ccgd.UndirectedHypergraph(labelled_edges={(a, b): None, (e, f): None})
    crosstalk_graph_addend = ccgd.UndirectedHypergraph(
        labelled_edges={(frozenset((a, b)), frozenset((e, f))): None}
    )
    device_addend = ccgd.UndirectedGraphDevice(
        device_graph=device_graph_addend, crosstalk_graph=crosstalk_graph_addend
    )
    device_sum = device + device_addend
    device_copy = device.__copy__()
    device_copy += device_addend
    assert device != device_copy
    assert device_copy == device_sum
