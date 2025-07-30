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

import random

import pytest

import qubitron
import qubitron.contrib.acquaintance as cca
import qubitron.testing as ct


def test_swap_permutation_gate():
    no_decomp = lambda op: (isinstance(op, qubitron.GateOperation) and op.gate == qubitron.SWAP)
    a, b = qubitron.NamedQubit('a'), qubitron.NamedQubit('b')
    gate = cca.SwapPermutationGate()
    assert gate.num_qubits() == 2
    circuit = qubitron.Circuit(gate(a, b))
    circuit = qubitron.expand_composite(circuit, no_decomp=no_decomp)
    assert tuple(circuit.all_operations()) == (qubitron.SWAP(a, b),)

    no_decomp = lambda op: (isinstance(op, qubitron.GateOperation) and op.gate == qubitron.CZ)
    circuit = qubitron.Circuit(cca.SwapPermutationGate(qubitron.CZ)(a, b))
    circuit = qubitron.expand_composite(circuit, no_decomp=no_decomp)
    assert tuple(circuit.all_operations()) == (qubitron.CZ(a, b),)

    assert qubitron.commutes(gate, qubitron.ZZ)
    with pytest.raises(TypeError):
        qubitron.commutes(gate, qubitron.CCZ)


def test_validate_permutation_errors():
    validate_permutation = cca.PermutationGate.validate_permutation
    validate_permutation({})

    with pytest.raises(IndexError, match=r'key and value sets must be the same\.'):
        validate_permutation({0: 2, 1: 3})

    with pytest.raises(IndexError, match=r'keys of the permutation must be non-negative\.'):
        validate_permutation({-1: 0, 0: -1})

    with pytest.raises(IndexError, match=r'key is out of bounds\.'):
        validate_permutation({0: 3, 3: 0}, 2)

    gate = cca.SwapPermutationGate()
    assert qubitron.circuit_diagram_info(gate, default=None) is None


def test_diagram():
    gate = cca.SwapPermutationGate()
    a, b = qubitron.NamedQubit('a'), qubitron.NamedQubit('b')
    circuit = qubitron.Circuit([gate(a, b)])
    actual_text_diagram = circuit.to_text_diagram()
    expected_text_diagram = """
a: ───0↦1───
      │
b: ───1↦0───
    """.strip()
    assert actual_text_diagram == expected_text_diagram


def test_update_mapping():
    gate = cca.SwapPermutationGate()
    a, b, c = (qubitron.NamedQubit(s) for s in 'abc')
    mapping = {s: i for i, s in enumerate((a, b, c))}
    ops = [gate(a, b), gate(b, c)]
    cca.update_mapping(mapping, ops)
    assert mapping == {a: 1, b: 2, c: 0}


def test_get_logical_operations():
    a, b, c, d = qubits = qubitron.LineQubit.range(4)
    mapping = dict(zip(qubits, qubits))
    operations = [
        qubitron.ZZ(a, b),
        cca.SwapPermutationGate()(b, c),
        qubitron.SWAP(a, b),
        cca.SwapPermutationGate()(c, d),
        cca.SwapPermutationGate()(b, c),
        qubitron.ZZ(a, b),
    ]
    assert list(cca.get_logical_operations(operations, mapping)) == [
        qubitron.ZZ(a, b),
        qubitron.SWAP(a, c),
        qubitron.ZZ(a, d),
    ]


@pytest.mark.parametrize(
    'n_elements,n_permuted',
    (
        (n_elements, random.randint(0, n_elements))
        for n_elements in (random.randint(5, 20) for _ in range(20))
    ),
)
def test_linear_permutation_gate(n_elements, n_permuted):
    qubits = qubitron.LineQubit.range(n_elements)
    elements = tuple(range(n_elements))
    elements_to_permute = random.sample(elements, n_permuted)
    permuted_elements = random.sample(elements_to_permute, n_permuted)
    permutation = {e: p for e, p in zip(elements_to_permute, permuted_elements)}
    cca.PermutationGate.validate_permutation(permutation, n_elements)
    gate = cca.LinearPermutationGate(n_elements, permutation)
    ct.assert_equivalent_repr(gate)
    assert gate.permutation() == permutation
    mapping = dict(zip(qubits, elements))
    for swap in qubitron.flatten_op_tree(qubitron.decompose_once_with_qubits(gate, qubits)):
        assert isinstance(swap, qubitron.GateOperation)
        swap.gate.update_mapping(mapping, swap.qubits)
    for i in range(n_elements):
        p = permutation.get(elements[i], i)
        assert mapping.get(qubits[p], elements[i]) == i


def random_equal_permutations(n_perms, n_items, prob):
    indices_to_permute = [i for i in range(n_items) if random.random() <= prob]
    permuted_indices = random.sample(indices_to_permute, len(indices_to_permute))
    base_permutation = dict(zip(indices_to_permute, permuted_indices))
    fixed_indices = [i for i in range(n_items) if i not in base_permutation]
    permutations = []
    for _ in range(n_perms):
        permutation = base_permutation.copy()
        permutation.update({i: i for i in fixed_indices if random.random() <= prob})
        permutations.append(permutation)
    return permutations


def random_permutation_equality_groups(n_groups, n_perms_per_group, n_items, prob):
    fingerprints = set()
    for _ in range(n_groups):
        perms = random_equal_permutations(n_perms_per_group, n_items, prob)
        perm = perms[0]
        fingerprint = tuple(perm.get(i, i) for i in range(n_items))
        if fingerprint not in fingerprints:
            yield perms
            fingerprints.add(fingerprint)


@pytest.mark.parametrize('permutation_sets', [random_permutation_equality_groups(5, 3, 10, 0.5)])
def test_linear_permutation_gate_equality(permutation_sets):
    swap_gates = [qubitron.SWAP, qubitron.CNOT]
    equals_tester = ct.EqualsTester()
    for swap_gate in swap_gates:
        for permutation_set in permutation_sets:
            equals_tester.add_equality_group(
                *(
                    cca.LinearPermutationGate(10, permutation, swap_gate)
                    for permutation in permutation_set
                )
            )


def test_linear_permutation_gate_pow_not_implemented():
    permutation_gate = cca.LinearPermutationGate(3, {0: 1, 1: 2, 2: 0})

    assert permutation_gate.__pow__(0) is NotImplemented
    assert permutation_gate.__pow__(2) is NotImplemented
    assert permutation_gate.__pow__(-2) is NotImplemented
    assert permutation_gate.__pow__(0.5) is NotImplemented
    assert permutation_gate.__pow__(-0.5) is NotImplemented


@pytest.mark.parametrize(
    'num_qubits,permutation',
    [
        (2, {0: 1, 1: 0}),
        (3, {0: 0, 1: 1, 2: 2}),
        (3, {0: 1, 1: 2, 2: 0}),
        (3, {0: 2, 1: 0, 2: 1}),
        (4, {0: 3, 1: 2, 2: 1, 3: 0}),
    ],
)
def test_linear_permutation_gate_pow_identity(num_qubits, permutation):
    permutation_gate = cca.LinearPermutationGate(num_qubits, permutation)

    assert permutation_gate**1 == permutation_gate


@pytest.mark.parametrize(
    'num_qubits,permutation,inverse',
    [
        (2, {0: 1, 1: 0}, {0: 1, 1: 0}),
        (3, {0: 0, 1: 1, 2: 2}, {0: 0, 1: 1, 2: 2}),
        (3, {0: 1, 1: 2, 2: 0}, {0: 2, 1: 0, 2: 1}),
        (3, {0: 2, 1: 0, 2: 1}, {0: 1, 1: 2, 2: 0}),
        (4, {0: 3, 1: 2, 2: 1, 3: 0}, {0: 3, 1: 2, 2: 1, 3: 0}),
    ],
)
def test_linear_permutation_gate_pow_inverse(num_qubits, permutation, inverse):
    permutation_gate = cca.LinearPermutationGate(num_qubits, permutation)
    inverse_gate = cca.LinearPermutationGate(num_qubits, inverse)

    assert permutation_gate**-1 == inverse_gate
    assert qubitron.inverse(permutation_gate) == inverse_gate


def test_display_mapping():
    indices = [4, 2, 0, 1, 3]
    qubits = qubitron.LineQubit.range(len(indices))
    circuit = cca.complete_acquaintance_strategy(qubits, 2)
    cca.expose_acquaintance_gates(circuit)
    initial_mapping = dict(zip(qubits, indices))
    cca.display_mapping(circuit, initial_mapping)
    expected_diagram = """
0: ───4───█───4───╲0╱───2───────2─────────2───█───2───╲0╱───1───────1─────────1───█───1───╲0╱───3───
          │       │                           │       │                           │       │
1: ───2───█───2───╱1╲───4───█───4───╲0╱───1───█───1───╱1╲───2───█───2───╲0╱───3───█───3───╱1╲───1───
                            │       │                           │       │
2: ───0───█───0───╲0╱───1───█───1───╱1╲───4───█───4───╲0╱───3───█───3───╱1╲───2───█───2───╲0╱───0───
          │       │                           │       │                           │       │
3: ───1───█───1───╱1╲───0───█───0───╲0╱───3───█───3───╱1╲───4───█───4───╲0╱───0───█───0───╱1╲───2───
                            │       │                           │       │
4: ───3───────3─────────3───█───3───╱1╲───0───────0─────────0───█───0───╱1╲───4───────4─────────4───
"""
    qubitron.testing.assert_has_diagram(circuit, expected_diagram)


@pytest.mark.parametrize(
    'circuit',
    [
        qubitron.Circuit(
            cca.SwapPermutationGate()(*qubit_pair)
            for qubit_pair in [random.sample(qubitron.LineQubit.range(10), 2) for _ in range(20)]
        )
        for _ in range(4)
    ],
)
def test_return_to_initial_mapping(circuit):
    qubits = sorted(circuit.all_qubits())
    cca.return_to_initial_mapping(circuit)
    initial_mapping = {q: i for i, q in enumerate(qubits)}
    mapping = dict(initial_mapping)
    cca.update_mapping(mapping, circuit.all_operations())
    assert mapping == initial_mapping


def test_uses_consistent_swap_gate():
    a, b = qubitron.LineQubit.range(2)
    circuit = qubitron.Circuit([cca.SwapPermutationGate()(a, b), cca.SwapPermutationGate()(a, b)])
    assert cca.uses_consistent_swap_gate(circuit, qubitron.SWAP)
    assert not cca.uses_consistent_swap_gate(circuit, qubitron.CZ)
    circuit = qubitron.Circuit(
        [cca.SwapPermutationGate(qubitron.CZ)(a, b), cca.SwapPermutationGate(qubitron.CZ)(a, b)]
    )
    assert cca.uses_consistent_swap_gate(circuit, qubitron.CZ)
    assert not cca.uses_consistent_swap_gate(circuit, qubitron.SWAP)
    circuit = qubitron.Circuit(
        [cca.SwapPermutationGate()(a, b), cca.SwapPermutationGate(qubitron.CZ)(a, b)]
    )
    assert not cca.uses_consistent_swap_gate(circuit, qubitron.SWAP)
    assert not cca.uses_consistent_swap_gate(circuit, qubitron.CZ)


def test_swap_gate_eq():
    assert cca.SwapPermutationGate() == cca.SwapPermutationGate(qubitron.SWAP)
    assert cca.SwapPermutationGate() != cca.SwapPermutationGate(qubitron.CZ)
    assert cca.SwapPermutationGate(qubitron.CZ) == cca.SwapPermutationGate(qubitron.CZ)


@pytest.mark.parametrize(
    'gate',
    [
        cca.SwapPermutationGate(),
        cca.SwapPermutationGate(qubitron.SWAP),
        cca.SwapPermutationGate(qubitron.CZ),
    ],
)
def test_swap_gate_repr(gate):
    qubitron.testing.assert_equivalent_repr(gate)
