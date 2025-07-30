# Copyright 2024 The Qubitron Developers
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

from unittest.mock import patch

import numpy as np
import pytest

import qubitron
from qubitron.transformers.gauge_compiling import GaugeSelector, GaugeTransformer


class GaugeTester:

    two_qubit_gate: qubitron.Gate
    gauge_transformer: GaugeTransformer
    must_fail: bool = False

    @pytest.mark.parametrize(
        ['generation_seed', 'transformation_seed'],
        np.random.RandomState(0).randint(2**31, size=(5, 2)).tolist(),
    )
    def test_gauge_transformer(self, generation_seed, transformation_seed):
        c = qubitron.Circuit()
        while not any(op.gate == self.two_qubit_gate for op in c.all_operations()):
            c = qubitron.testing.random_circuit(
                qubits=3,
                n_moments=3,
                op_density=1,
                gate_domain={self.two_qubit_gate: 2, qubitron.X: 1, qubitron.Y: 1, qubitron.H: 1, qubitron.Z: 1},
                random_state=generation_seed,
            )
            generation_seed += 1
        nc = self.gauge_transformer(c, prng=np.random.default_rng(transformation_seed))
        if self.must_fail:
            with pytest.raises(AssertionError):
                qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
                    nc, c, qubit_map={q: q for q in c.all_qubits()}
                )
        else:
            qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
                nc, c, qubit_map={q: q for q in c.all_qubits()}
            )

    @patch('qubitron.transformers.gauge_compiling.gauge_compiling._select', autospec=True)
    @pytest.mark.parametrize('seed', range(5))
    def test_all_gauges(self, mock_select, seed):
        assert isinstance(
            self.gauge_transformer.gauge_selector, GaugeSelector
        ), 'When using a custom selector, please override this method to properly test all gauges'
        c = qubitron.Circuit(self.two_qubit_gate(qubitron.LineQubit(0), qubitron.LineQubit(1)))
        prng = np.random.default_rng(seed)
        for gauge in self.gauge_transformer.gauge_selector.gauges:
            mock_select.return_value = gauge
            assert self.gauge_transformer.gauge_selector(prng) == gauge
            nc = self.gauge_transformer(c, prng=prng)

            if self.must_fail:
                with pytest.raises(AssertionError):
                    _check_equivalent_with_error_message(c, nc, gauge)
            else:
                _check_equivalent_with_error_message(c, nc, gauge)

    def test_sweep(self):
        qubits = qubitron.LineQubit.range(3)

        input_circuit = qubitron.Circuit(
            qubitron.Moment(qubitron.H(qubits[0])),
            qubitron.Moment(self.two_qubit_gate(*qubits[:2])),
            qubitron.Moment(self.two_qubit_gate(*qubits[1:])),
            qubitron.Moment([qubitron.H(q) for q in qubits]),
            qubitron.Moment([qubitron.measure(q) for q in qubits]),
        )

        n_samples = 5
        parameterized_circuit, sweeps = self.gauge_transformer.as_sweep(input_circuit, N=n_samples)

        # Check the parameterized circuit and N set of parameters.
        assert qubitron.is_parameterized(parameterized_circuit)
        simulator = qubitron.Simulator()
        results = simulator.run_sweep(parameterized_circuit, sweeps)
        assert len(results) == n_samples

        # Check compilied circuits have the same unitary as the orig circuit.
        for params in sweeps:
            compiled_circuit = qubitron.resolve_parameters(parameterized_circuit, params)
            if self.must_fail:
                with pytest.raises(AssertionError):
                    qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
                        input_circuit[:-1],
                        compiled_circuit[:-1],
                        qubit_map={q: q for q in input_circuit.all_qubits()},
                    )
                break
            qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
                input_circuit[:-1],
                compiled_circuit[:-1],
                qubit_map={q: q for q in input_circuit.all_qubits()},
            )


def _check_equivalent_with_error_message(c: qubitron.AbstractCircuit, nc: qubitron.AbstractCircuit, gauge):
    try:
        qubitron.testing.assert_circuits_have_same_unitary_given_final_permutation(
            nc, c, qubit_map={q: q for q in c.all_qubits()}
        )
    except AssertionError as ex:
        raise AssertionError(f"{gauge=} didn't result in an equivalent circuit") from ex
