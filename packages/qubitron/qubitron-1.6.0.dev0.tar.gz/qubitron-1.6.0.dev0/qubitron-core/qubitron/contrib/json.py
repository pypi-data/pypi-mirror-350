# pylint: disable=wrong-or-nonexistent-copyright-notice
"""Functions for JSON serialization and de-serialization for classes in Contrib."""

from __future__ import annotations

from qubitron.protocols.json_serialization import DEFAULT_RESOLVERS


def contrib_class_resolver(qubitron_type: str):
    """Extend qubitron's JSON API with resolvers for qubitron contrib classes."""
    from qubitron.contrib.acquaintance import SwapPermutationGate
    from qubitron.contrib.bayesian_network import BayesianNetworkGate
    from qubitron.contrib.quantum_volume import QuantumVolumeResult

    classes = [BayesianNetworkGate, QuantumVolumeResult, SwapPermutationGate]
    d = {cls.__name__: cls for cls in classes}
    return d.get(qubitron_type, None)


DEFAULT_CONTRIB_RESOLVERS = [contrib_class_resolver] + DEFAULT_RESOLVERS
