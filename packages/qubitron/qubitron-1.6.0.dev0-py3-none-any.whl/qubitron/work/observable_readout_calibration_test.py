# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

from typing import Sequence

import numpy as np

import qubitron
import qubitron.work as cw


class DepolarizingWithDampedReadoutNoiseModel(qubitron.NoiseModel):
    """This simulates asymmetric readout error.

    The noise is structured so the T1 decay is applied, then the readout bitflip, then measurement.
    If a circuit contains measurements, they must be in moments that don't also contain gates.
    """

    def __init__(self, depol_prob: float, bitflip_prob: float, decay_prob: float):
        self.qubit_noise_gate = qubitron.DepolarizingChannel(depol_prob)
        self.readout_noise_gate = qubitron.BitFlipChannel(bitflip_prob)
        self.readout_decay_gate = qubitron.AmplitudeDampingChannel(decay_prob)

    def noisy_moment(self, moment: qubitron.Moment, system_qubits: Sequence[qubitron.Qid]):
        if qubitron.devices.noise_model.validate_all_measurements(moment):
            return [
                qubitron.Moment(self.readout_decay_gate(q) for q in system_qubits),
                qubitron.Moment(self.readout_noise_gate(q) for q in system_qubits),
                moment,
            ]
        else:
            return [moment, qubitron.Moment(self.qubit_noise_gate(q) for q in system_qubits)]


def test_calibrate_readout_error() -> None:
    sampler = qubitron.DensityMatrixSimulator(
        noise=DepolarizingWithDampedReadoutNoiseModel(
            depol_prob=1e-3, bitflip_prob=0.03, decay_prob=0.03
        ),
        seed=10,
    )
    readout_calibration = cw.calibrate_readout_error(
        qubits=qubitron.LineQubit.range(2),
        sampler=sampler,
        stopping_criteria=cw.RepetitionsStoppingCriteria(100_000),
    )
    means = readout_calibration.means()
    assert len(means) == 2, 'Two qubits'
    assert np.all(means > 0.89)
    assert np.all(means < 0.91)
