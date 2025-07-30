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

"""Device classes, qubits, and topologies, as well as noise models."""


from qubitron.devices.device import Device as Device, DeviceMetadata as DeviceMetadata

from qubitron.devices.grid_device_metadata import GridDeviceMetadata as GridDeviceMetadata

from qubitron.devices.grid_qubit import GridQid as GridQid, GridQubit as GridQubit

from qubitron.devices.line_qubit import LineQubit as LineQubit, LineQid as LineQid

from qubitron.devices.unconstrained_device import UNCONSTRAINED_DEVICE as UNCONSTRAINED_DEVICE

from qubitron.devices.noise_model import (
    NO_NOISE as NO_NOISE,
    NOISE_MODEL_LIKE as NOISE_MODEL_LIKE,
    NoiseModel as NoiseModel,
    ConstantQubitNoiseModel as ConstantQubitNoiseModel,
)

from qubitron.devices.named_topologies import (
    NamedTopology as NamedTopology,
    draw_gridlike as draw_gridlike,
    LineTopology as LineTopology,
    TiltedSquareLattice as TiltedSquareLattice,
    get_placements as get_placements,
    is_valid_placement as is_valid_placement,
    draw_placements as draw_placements,
)

from qubitron.devices.insertion_noise_model import InsertionNoiseModel as InsertionNoiseModel

from qubitron.devices.thermal_noise_model import ThermalNoiseModel as ThermalNoiseModel

from qubitron.devices.noise_properties import (
    NoiseModelFromNoiseProperties as NoiseModelFromNoiseProperties,
    NoiseProperties as NoiseProperties,
)

from qubitron.devices.superconducting_qubits_noise_properties import (
    SuperconductingQubitsNoiseProperties as SuperconductingQubitsNoiseProperties,
)

from qubitron.devices.noise_utils import (
    OpIdentifier as OpIdentifier,
    decay_constant_to_xeb_fidelity as decay_constant_to_xeb_fidelity,
    decay_constant_to_pauli_error as decay_constant_to_pauli_error,
    pauli_error_to_decay_constant as pauli_error_to_decay_constant,
    xeb_fidelity_to_decay_constant as xeb_fidelity_to_decay_constant,
    pauli_error_from_t1 as pauli_error_from_t1,
    average_error as average_error,
    decoherence_pauli_error as decoherence_pauli_error,
)
