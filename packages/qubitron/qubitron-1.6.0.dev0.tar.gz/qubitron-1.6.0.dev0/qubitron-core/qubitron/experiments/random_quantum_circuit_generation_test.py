# Copyright 2020 The Qubitron Developers
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

import itertools
from typing import Callable, cast, Iterable, Sequence

import networkx as nx
import numpy as np
import pytest

import qubitron
from qubitron.experiments import (
    GridInteractionLayer,
    random_rotations_between_grid_interaction_layers_circuit,
)
from qubitron.experiments.random_quantum_circuit_generation import (
    generate_library_of_2q_circuits,
    get_grid_interaction_layer_circuit,
    get_random_combinations_for_device,
    get_random_combinations_for_layer_circuit,
    get_random_combinations_for_pairs,
    random_rotations_between_two_qubit_circuit,
)

SINGLE_QUBIT_LAYER = dict[qubitron.GridQubit, qubitron.Gate | None]


def test_random_rotation_between_two_qubit_circuit():
    q0, q1 = qubitron.LineQubit.range(2)
    circuit = random_rotations_between_two_qubit_circuit(q0, q1, 4, seed=52)
    assert len(circuit) == 4 * 2 + 1
    assert circuit.all_qubits() == {q0, q1}

    circuit = random_rotations_between_two_qubit_circuit(
        q0, q1, 4, seed=52, add_final_single_qubit_layer=False
    )
    assert len(circuit) == 4 * 2
    assert circuit.all_qubits() == {q0, q1}

    qubitron.testing.assert_has_diagram(
        circuit,
        """\
0             1
│             │
Y^0.5         X^0.5
│             │
@─────────────@
│             │
PhX(0.25)^0.5 Y^0.5
│             │
@─────────────@
│             │
Y^0.5         X^0.5
│             │
@─────────────@
│             │
X^0.5         PhX(0.25)^0.5
│             │
@─────────────@
│             │""",
        transpose=True,
    )


def test_generate_library_of_2q_circuits():
    circuits = generate_library_of_2q_circuits(
        n_library_circuits=5, two_qubit_gate=qubitron.CNOT, max_cycle_depth=13, random_state=9
    )
    assert len(circuits) == 5
    for circuit in circuits:
        assert len(circuit.all_qubits()) == 2
        assert sorted(circuit.all_qubits()) == qubitron.LineQubit.range(2)
        for m1, m2 in zip(circuit.moments[::2], circuit.moments[1::2]):
            assert len(m1.operations) == 2  # single qubit layer
            assert len(m2.operations) == 1
            assert m2.operations[0].gate == qubitron.CNOT


def test_generate_library_of_2q_circuits_custom_qubits():
    circuits = generate_library_of_2q_circuits(
        n_library_circuits=5,
        two_qubit_gate=qubitron.ISWAP**0.5,
        max_cycle_depth=13,
        q0=qubitron.GridQubit(9, 9),
        q1=qubitron.NamedQubit('hi mom'),
        random_state=9,
    )
    assert len(circuits) == 5
    for circuit in circuits:
        assert sorted(circuit.all_qubits()) == [qubitron.GridQubit(9, 9), qubitron.NamedQubit('hi mom')]
        for m1, m2 in zip(circuit.moments[::2], circuit.moments[1::2]):
            assert len(m1.operations) == 2  # single qubit layer
            assert len(m2.operations) == 1
            assert m2.operations[0].gate == qubitron.ISWAP**0.5


def _gridqubits_to_graph_device(qubits: Iterable[qubitron.GridQubit]):
    # qubitron contrib: routing.gridqubits_to_graph_device
    def _manhattan_distance(qubit1: qubitron.GridQubit, qubit2: qubitron.GridQubit) -> int:
        return abs(qubit1.row - qubit2.row) + abs(qubit1.col - qubit2.col)

    return nx.Graph(
        pair for pair in itertools.combinations(qubits, 2) if _manhattan_distance(*pair) == 1
    )


def test_get_random_combinations_for_device():
    graph = _gridqubits_to_graph_device(qubitron.GridQubit.rect(3, 3))
    n_combinations = 4
    combinations = get_random_combinations_for_device(
        n_library_circuits=3, n_combinations=n_combinations, device_graph=graph, random_state=99
    )
    assert len(combinations) == 4  # degree-four graph
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in qubitron.GridQubit.rect(3, 3)
            assert q1 in qubitron.GridQubit.rect(3, 3)

        assert qubitron.experiments.HALF_GRID_STAGGERED_PATTERN[i] == comb.layer


def test_get_random_combinations_for_small_device():
    graph = _gridqubits_to_graph_device(qubitron.GridQubit.rect(3, 1))
    n_combinations = 4
    combinations = get_random_combinations_for_device(
        n_library_circuits=3, n_combinations=n_combinations, device_graph=graph, random_state=99
    )
    assert len(combinations) == 2  # 3x1 device only fits two layers


def test_get_random_combinations_for_pairs():
    all_pairs = [
        [(qubitron.LineQubit(0), qubitron.LineQubit(1)), (qubitron.LineQubit(2), qubitron.LineQubit(3))],
        [(qubitron.LineQubit(1), qubitron.LineQubit(2))],
    ]
    combinations = get_random_combinations_for_pairs(
        n_library_circuits=3, n_combinations=4, all_pairs=all_pairs, random_state=99
    )
    assert len(combinations) == len(all_pairs)
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == 4  # n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in qubitron.LineQubit.range(4)
            assert q1 in qubitron.LineQubit.range(4)

        assert comb.layer is None
        assert comb.pairs == all_pairs[i]


def test_get_random_combinations_for_layer_circuit():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(qubitron.CNOT(q0, q1), qubitron.CNOT(q2, q3), qubitron.CNOT(q1, q2))
    combinations = get_random_combinations_for_layer_circuit(
        n_library_circuits=3, n_combinations=4, layer_circuit=circuit, random_state=99
    )
    assert len(combinations) == 2  # operations pack into two layers
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == 4  # n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in qubitron.LineQubit.range(4)
            assert q1 in qubitron.LineQubit.range(4)

        assert comb.layer == circuit.moments[i]


def test_get_random_combinations_for_bad_layer_circuit():
    q0, q1, q2, q3 = qubitron.LineQubit.range(4)
    circuit = qubitron.Circuit(
        qubitron.H.on_each(q0, q1, q2, q3), qubitron.CNOT(q0, q1), qubitron.CNOT(q2, q3), qubitron.CNOT(q1, q2)
    )

    with pytest.raises(ValueError, match=r'non-2-qubit operation'):
        _ = get_random_combinations_for_layer_circuit(
            n_library_circuits=3, n_combinations=4, layer_circuit=circuit, random_state=99
        )


def test_get_grid_interaction_layer_circuit():
    graph = _gridqubits_to_graph_device(qubitron.GridQubit.rect(3, 3))
    layer_circuit = get_grid_interaction_layer_circuit(graph)

    sqrtisw = qubitron.ISWAP**0.5
    gq = qubitron.GridQubit
    should_be = qubitron.Circuit(
        # Vertical
        sqrtisw(gq(0, 0), gq(1, 0)),
        sqrtisw(gq(1, 1), gq(2, 1)),
        sqrtisw(gq(0, 2), gq(1, 2)),
        # Vertical, offset
        sqrtisw(gq(0, 1), gq(1, 1)),
        sqrtisw(gq(1, 2), gq(2, 2)),
        sqrtisw(gq(1, 0), gq(2, 0)),
        # Horizontal, offset
        sqrtisw(gq(0, 1), gq(0, 2)),
        sqrtisw(gq(1, 0), gq(1, 1)),
        sqrtisw(gq(2, 1), gq(2, 2)),
        # Horizontal
        sqrtisw(gq(0, 0), gq(0, 1)),
        sqrtisw(gq(1, 1), gq(1, 2)),
        sqrtisw(gq(2, 0), gq(2, 1)),
    )
    assert layer_circuit == should_be


def test_random_combinations_layer_circuit_vs_device():
    # Random combinations from layer circuit is the same as getting it directly from graph
    graph = _gridqubits_to_graph_device(qubitron.GridQubit.rect(3, 3))
    layer_circuit = get_grid_interaction_layer_circuit(graph)
    combs1 = get_random_combinations_for_layer_circuit(
        n_library_circuits=10, n_combinations=10, layer_circuit=layer_circuit, random_state=1
    )
    combs2 = get_random_combinations_for_device(
        n_library_circuits=10, n_combinations=10, device_graph=graph, random_state=1
    )
    for comb1, comb2 in zip(combs1, combs2):
        assert comb1.pairs == comb2.pairs
        assert np.all(comb1.combinations == comb2.combinations)


def _cz_with_adjacent_z_rotations(
    a: qubitron.GridQubit, b: qubitron.GridQubit, prng: np.random.RandomState
):
    z_exponents = [prng.uniform(0, 1) for _ in range(4)]
    yield qubitron.Z(a) ** z_exponents[0]
    yield qubitron.Z(b) ** z_exponents[1]
    yield qubitron.CZ(a, b)
    yield qubitron.Z(a) ** z_exponents[2]
    yield qubitron.Z(b) ** z_exponents[3]


class FakeSycamoreGate(qubitron.FSimGate):
    def __init__(self):
        super().__init__(theta=np.pi / 2, phi=np.pi / 6)


@pytest.mark.parametrize(
    'qubits, depth, two_qubit_op_factory, pattern, '
    'single_qubit_gates, add_final_single_qubit_layer, '
    'seed, expected_circuit_length, single_qubit_layers_slice, '
    'two_qubit_layers_slice',
    (
        (
            (qubitron.q(0, 0), qubitron.q(0, 1), qubitron.q(0, 2)),
            4,
            lambda a, b, _: qubitron.CZ(a, b),
            [[(qubitron.q(0, 0), qubitron.q(0, 1))], [(qubitron.q(0, 1), qubitron.q(0, 2))]],
            (qubitron.X**0.5,),
            True,
            1234,
            9,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            (qubitron.q(0, 0), qubitron.q(0, 1), qubitron.q(0, 2)),
            4,
            lambda a, b, _: qubitron.CZ(a, b),
            [[(qubitron.q(0, 1), qubitron.q(0, 0))], [(qubitron.q(0, 1), qubitron.q(0, 2))]],
            (qubitron.X**0.5,),
            True,
            1234,
            9,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            qubitron.GridQubit.rect(4, 3),
            20,
            lambda a, b, _: qubitron.CZ(a, b),
            qubitron.experiments.GRID_STAGGERED_PATTERN,
            (qubitron.X**0.5, qubitron.Y**0.5, qubitron.Z**0.5),
            True,
            1234,
            41,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            qubitron.GridQubit.rect(4, 3),
            20,
            lambda a, b, _: FakeSycamoreGate()(a, b),
            qubitron.experiments.HALF_GRID_STAGGERED_PATTERN,
            (qubitron.X**0.5, qubitron.Y**0.5, qubitron.Z**0.5),
            True,
            1234,
            41,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            qubitron.GridQubit.rect(4, 5),
            21,
            lambda a, b, _: qubitron.CZ(a, b),
            qubitron.experiments.GRID_ALIGNED_PATTERN,
            (qubitron.X**0.5, qubitron.Y**0.5, qubitron.Z**0.5),
            True,
            1234,
            43,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            qubitron.GridQubit.rect(5, 4),
            22,
            _cz_with_adjacent_z_rotations,
            qubitron.experiments.GRID_STAGGERED_PATTERN,
            (qubitron.X**0.5, qubitron.Y**0.5, qubitron.Z**0.5),
            True,
            1234,
            89,
            slice(None, None, 4),
            slice(2, None, 4),
        ),
        (
            qubitron.GridQubit.rect(5, 5),
            23,
            lambda a, b, _: qubitron.CZ(a, b),
            qubitron.experiments.GRID_ALIGNED_PATTERN,
            (qubitron.X**0.5, qubitron.Y**0.5, qubitron.Z**0.5),
            False,
            1234,
            46,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
        (
            qubitron.GridQubit.rect(5, 5),
            24,
            lambda a, b, _: qubitron.CZ(a, b),
            qubitron.experiments.GRID_ALIGNED_PATTERN,
            (qubitron.X**0.5, qubitron.X**0.5),
            True,
            1234,
            49,
            slice(None, None, 2),
            slice(1, None, 2),
        ),
    ),
)
def test_random_rotations_between_grid_interaction_layers(
    qubits: Iterable[qubitron.GridQubit],
    depth: int,
    two_qubit_op_factory: Callable[
        [qubitron.GridQubit, qubitron.GridQubit, np.random.RandomState], qubitron.OP_TREE
    ],
    pattern: Sequence[GridInteractionLayer],
    single_qubit_gates: Sequence[qubitron.Gate],
    add_final_single_qubit_layer: bool,
    seed: qubitron.RANDOM_STATE_OR_SEED_LIKE,
    expected_circuit_length: int,
    single_qubit_layers_slice: slice,
    two_qubit_layers_slice: slice,
):
    qubits = set(qubits)
    circuit = random_rotations_between_grid_interaction_layers_circuit(
        qubits,
        depth,
        two_qubit_op_factory=two_qubit_op_factory,
        pattern=pattern,
        single_qubit_gates=single_qubit_gates,
        add_final_single_qubit_layer=add_final_single_qubit_layer,
        seed=seed,
    )

    assert len(circuit) == expected_circuit_length
    _validate_single_qubit_layers(
        qubits,
        cast(Sequence[qubitron.Moment], circuit[single_qubit_layers_slice]),
        non_repeating_layers=len(set(single_qubit_gates)) > 1,
    )
    _validate_two_qubit_layers(
        qubits, cast(Sequence[qubitron.Moment], circuit[two_qubit_layers_slice]), pattern
    )


def test_grid_interaction_layer_repr():
    layer = GridInteractionLayer(col_offset=0, vertical=True, stagger=False)
    assert repr(layer) == (
        'qubitron.experiments.GridInteractionLayer(col_offset=0, vertical=True, stagger=False)'
    )


def _validate_single_qubit_layers(
    qubits: set[qubitron.GridQubit], moments: Sequence[qubitron.Moment], non_repeating_layers: bool = True
) -> None:
    previous_single_qubit_gates: SINGLE_QUBIT_LAYER = {q: None for q in qubits}

    for moment in moments:
        # All qubits are acted upon
        assert moment.qubits == qubits
        for op in moment:
            # Operation is single-qubit
            assert qubitron.num_qubits(op) == 1
            if non_repeating_layers:
                # Gate differs from previous single-qubit gate on this qubit
                q = cast(qubitron.GridQubit, op.qubits[0])
                assert op.gate != previous_single_qubit_gates[q]
                previous_single_qubit_gates[q] = op.gate


def _validate_two_qubit_layers(
    qubits: set[qubitron.GridQubit],
    moments: Sequence[qubitron.Moment],
    pattern: Sequence[qubitron.experiments.GridInteractionLayer],
) -> None:
    coupled_qubit_pairs = _coupled_qubit_pairs(qubits)
    for i, moment in enumerate(moments):
        active_pairs = set()
        for op in moment:
            # Operation is two-qubit
            assert qubitron.num_qubits(op) == 2
            # Operation fits pattern
            assert (
                op.qubits in pattern[i % len(pattern)]
                or op.qubits[::-1] in pattern[i % len(pattern)]
            )
            active_pairs.add(op.qubits)
        # All interactions that should be in this layer are present
        assert all(
            pair in active_pairs
            for pair in coupled_qubit_pairs
            if pair in pattern[i % len(pattern)]
        )


def _coupled_qubit_pairs(
    qubits: set[qubitron.GridQubit],
) -> list[tuple[qubitron.GridQubit, qubitron.GridQubit]]:
    pairs = []
    for qubit in qubits:

        def add_pair(neighbor: qubitron.GridQubit):
            if neighbor in qubits:
                pairs.append((qubit, neighbor))

        add_pair(qubitron.GridQubit(qubit.row, qubit.col + 1))
        add_pair(qubitron.GridQubit(qubit.row + 1, qubit.col))

    return pairs


def test_generate_library_of_2q_circuits_with_tags():
    circuits = generate_library_of_2q_circuits(
        n_library_circuits=5,
        two_qubit_gate=qubitron.FSimGate(3, 4),
        max_cycle_depth=13,
        random_state=9,
        tags=('test_tag',),
    )
    assert len(circuits) == 5
    for circuit in circuits:
        for op in circuit.all_operations():
            if qubitron.num_qubits(op) == 1:
                continue
            assert op.tags == ('test_tag',)
            assert op.gate == qubitron.FSimGate(3, 4)
