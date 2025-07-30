# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import networkx as nx

import qubitron


def test_device_metadata() -> None:
    class RawDevice(qubitron.Device):
        pass

    assert RawDevice().metadata is None


def test_metadata() -> None:
    qubits = qubitron.LineQubit.range(4)
    graph = nx.star_graph(3)
    metadata = qubitron.DeviceMetadata(qubits, graph)
    assert metadata.qubit_set == frozenset(qubits)
    assert metadata.nx_graph == graph


def test_metadata_json_load_logic() -> None:
    qubits = qubitron.LineQubit.range(4)
    graph = nx.star_graph(3)
    metadata = qubitron.DeviceMetadata(qubits, graph)
    str_rep = qubitron.to_json(metadata)
    assert metadata == qubitron.read_json(json_text=str_rep)


def test_metadata_equality() -> None:
    qubits = qubitron.LineQubit.range(4)
    graph = nx.star_graph(3)
    graph2 = nx.star_graph(3)
    graph.add_edge(1, 2, directed=False)
    graph2.add_edge(1, 2, directed=True)

    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(qubitron.DeviceMetadata(qubits, graph))
    eq.add_equality_group(qubitron.DeviceMetadata(qubits, graph2))
    eq.add_equality_group(qubitron.DeviceMetadata(qubits[1:], graph))
