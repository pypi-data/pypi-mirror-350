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

"""Tests for GridDevicemetadata."""

from __future__ import annotations

import networkx as nx
import pytest

import qubitron


def test_griddevice_metadata():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    isolated_qubits = [qubitron.GridQubit(9, 9), qubitron.GridQubit(10, 10)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ)
    gate_durations = {
        qubitron.GateFamily(qubitron.XPowGate): 1_000,
        qubitron.GateFamily(qubitron.YPowGate): 1_000,
        qubitron.GateFamily(qubitron.ZPowGate): 1_000,
        # omitting qubitron.CZ
    }
    target_gatesets = (qubitron.CZTargetGateset(),)
    metadata = qubitron.GridDeviceMetadata(
        qubit_pairs,
        gateset,
        gate_durations=gate_durations,
        all_qubits=qubits + isolated_qubits,
        compilation_target_gatesets=target_gatesets,
    )
    expected_pairings = frozenset(
        {
            frozenset((qubitron.GridQubit(0, 0), qubitron.GridQubit(0, 1))),
            frozenset((qubitron.GridQubit(0, 1), qubitron.GridQubit(0, 2))),
            frozenset((qubitron.GridQubit(0, 1), qubitron.GridQubit(1, 1))),
            frozenset((qubitron.GridQubit(0, 2), qubitron.GridQubit(1, 2))),
            frozenset((qubitron.GridQubit(1, 0), qubitron.GridQubit(1, 1))),
            frozenset((qubitron.GridQubit(1, 1), qubitron.GridQubit(1, 2))),
            frozenset((qubitron.GridQubit(0, 0), qubitron.GridQubit(1, 0))),
        }
    )
    assert metadata.qubit_set == frozenset(qubits + isolated_qubits)
    assert metadata.qubit_pairs == expected_pairings
    assert metadata.gateset == gateset
    expected_graph = nx.Graph()
    expected_graph.add_nodes_from(sorted(list(qubits + isolated_qubits)))
    expected_graph.add_edges_from(sorted(list(expected_pairings)), directed=False)
    assert metadata.nx_graph.edges() == expected_graph.edges()
    assert metadata.nx_graph.nodes() == expected_graph.nodes()
    assert metadata.gate_durations == gate_durations
    assert metadata.isolated_qubits == frozenset(isolated_qubits)
    assert metadata.compilation_target_gatesets == target_gatesets


def test_griddevice_metadata_bad_durations():
    qubits = tuple(qubitron.GridQubit.rect(1, 2))

    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate)
    invalid_duration = {
        qubitron.GateFamily(qubitron.XPowGate): qubitron.Duration(nanos=1),
        qubitron.GateFamily(qubitron.ZPowGate): qubitron.Duration(picos=1),
    }
    with pytest.raises(ValueError, match="ZPowGate"):
        qubitron.GridDeviceMetadata([qubits], gateset, gate_durations=invalid_duration)


def test_griddevice_metadata_bad_isolated():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    fewer_qubits = [qubitron.GridQubit(0, 0)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ)
    with pytest.raises(ValueError, match='node_set'):
        _ = qubitron.GridDeviceMetadata(qubit_pairs, gateset, all_qubits=fewer_qubits)


def test_griddevice_self_loop():
    bad_pairs = [
        (qubitron.GridQubit(0, 0), qubitron.GridQubit(0, 0)),
        (qubitron.GridQubit(1, 0), qubitron.GridQubit(1, 1)),
    ]
    with pytest.raises(ValueError, match='Self loop'):
        _ = qubitron.GridDeviceMetadata(bad_pairs, qubitron.Gateset(qubitron.XPowGate))


def test_griddevice_json_load():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ)
    duration = {
        qubitron.GateFamily(qubitron.XPowGate): qubitron.Duration(nanos=1),
        qubitron.GateFamily(qubitron.YPowGate): qubitron.Duration(picos=2),
        qubitron.GateFamily(qubitron.ZPowGate): qubitron.Duration(picos=3),
        qubitron.GateFamily(qubitron.CZ): qubitron.Duration(nanos=4),
    }
    isolated_qubits = [qubitron.GridQubit(9, 9), qubitron.GridQubit(10, 10)]
    target_gatesets = [qubitron.CZTargetGateset()]
    metadata = qubitron.GridDeviceMetadata(
        qubit_pairs,
        gateset,
        gate_durations=duration,
        all_qubits=qubits + isolated_qubits,
        compilation_target_gatesets=target_gatesets,
    )
    rep_str = qubitron.to_json(metadata)
    assert metadata == qubitron.read_json(json_text=rep_str)


def test_griddevice_json_load_with_defaults():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ)

    # Don't set parameters with default values
    metadata = qubitron.GridDeviceMetadata(qubit_pairs, gateset)
    rep_str = qubitron.to_json(metadata)

    assert metadata == qubitron.read_json(json_text=rep_str)


def test_griddevice_metadata_equality():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ, qubitron.SQRT_ISWAP)
    duration = {
        qubitron.GateFamily(qubitron.XPowGate): qubitron.Duration(nanos=1),
        qubitron.GateFamily(qubitron.YPowGate): qubitron.Duration(picos=3),
        qubitron.GateFamily(qubitron.ZPowGate): qubitron.Duration(picos=2),
        qubitron.GateFamily(qubitron.CZ): qubitron.Duration(nanos=4),
        qubitron.GateFamily(qubitron.SQRT_ISWAP): qubitron.Duration(nanos=5),
    }
    duration2 = {
        qubitron.GateFamily(qubitron.XPowGate): qubitron.Duration(nanos=10),
        qubitron.GateFamily(qubitron.YPowGate): qubitron.Duration(picos=13),
        qubitron.GateFamily(qubitron.ZPowGate): qubitron.Duration(picos=12),
        qubitron.GateFamily(qubitron.CZ): qubitron.Duration(nanos=14),
        qubitron.GateFamily(qubitron.SQRT_ISWAP): qubitron.Duration(nanos=15),
    }
    isolated_qubits = [qubitron.GridQubit(9, 9)]
    target_gatesets = [qubitron.CZTargetGateset(), qubitron.SqrtIswapTargetGateset()]
    metadata = qubitron.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=duration)
    metadata2 = qubitron.GridDeviceMetadata(qubit_pairs[:2], gateset, gate_durations=duration)
    metadata3 = qubitron.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=None)
    metadata4 = qubitron.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=duration2)
    metadata5 = qubitron.GridDeviceMetadata(reversed(qubit_pairs), gateset, gate_durations=duration)
    metadata6 = qubitron.GridDeviceMetadata(
        qubit_pairs, gateset, gate_durations=duration, all_qubits=qubits + isolated_qubits
    )
    metadata7 = qubitron.GridDeviceMetadata(
        qubit_pairs, gateset, compilation_target_gatesets=target_gatesets
    )
    metadata8 = qubitron.GridDeviceMetadata(
        qubit_pairs, gateset, compilation_target_gatesets=target_gatesets[::-1]
    )
    metadata9 = qubitron.GridDeviceMetadata(
        qubit_pairs, gateset, compilation_target_gatesets=tuple(target_gatesets)
    )
    metadata10 = qubitron.GridDeviceMetadata(
        qubit_pairs, gateset, compilation_target_gatesets=set(target_gatesets)
    )

    eq = qubitron.testing.EqualsTester()
    eq.add_equality_group(metadata)
    eq.add_equality_group(metadata2)
    eq.add_equality_group(metadata3)
    eq.add_equality_group(metadata4)
    eq.add_equality_group(metadata6)
    eq.add_equality_group(metadata7, metadata8, metadata9, metadata10)

    assert metadata == metadata5


def test_repr():
    qubits = qubitron.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = qubitron.Gateset(qubitron.XPowGate, qubitron.YPowGate, qubitron.ZPowGate, qubitron.CZ)
    duration = {
        qubitron.GateFamily(qubitron.XPowGate): qubitron.Duration(nanos=1),
        qubitron.GateFamily(qubitron.YPowGate): qubitron.Duration(picos=3),
        qubitron.GateFamily(qubitron.ZPowGate): qubitron.Duration(picos=2),
        qubitron.GateFamily(qubitron.CZ): qubitron.Duration(nanos=4),
    }
    isolated_qubits = [qubitron.GridQubit(9, 9)]
    target_gatesets = [qubitron.CZTargetGateset()]
    metadata = qubitron.GridDeviceMetadata(
        qubit_pairs,
        gateset,
        gate_durations=duration,
        all_qubits=qubits + isolated_qubits,
        compilation_target_gatesets=target_gatesets,
    )
    qubitron.testing.assert_equivalent_repr(metadata)
