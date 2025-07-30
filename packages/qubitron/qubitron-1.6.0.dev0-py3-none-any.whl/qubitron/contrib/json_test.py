# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import qubitron
from qubitron.contrib.acquaintance import SwapPermutationGate
from qubitron.contrib.bayesian_network import BayesianNetworkGate
from qubitron.contrib.json import DEFAULT_CONTRIB_RESOLVERS
from qubitron.contrib.quantum_volume import QuantumVolumeResult
from qubitron.testing import assert_json_roundtrip_works


def test_bayesian_network_gate() -> None:
    gate = BayesianNetworkGate(
        init_probs=[('q0', 0.125), ('q1', None)], arc_probs=[('q1', ('q0',), [0.25, 0.5])]
    )
    assert_json_roundtrip_works(gate, resolvers=DEFAULT_CONTRIB_RESOLVERS)


def test_quantum_volume() -> None:
    qubits = qubitron.LineQubit.range(5)
    qvr = QuantumVolumeResult(
        model_circuit=qubitron.Circuit(qubitron.H.on_each(qubits)),
        heavy_set=[1, 2, 3],
        compiled_circuit=qubitron.Circuit(qubitron.H.on_each(qubits)),
        sampler_result=0.1,
    )
    assert_json_roundtrip_works(qvr, resolvers=DEFAULT_CONTRIB_RESOLVERS)


def test_swap_permutation_gate() -> None:
    gate = SwapPermutationGate(swap_gate=qubitron.SWAP)
    assert_json_roundtrip_works(gate, resolvers=DEFAULT_CONTRIB_RESOLVERS)
