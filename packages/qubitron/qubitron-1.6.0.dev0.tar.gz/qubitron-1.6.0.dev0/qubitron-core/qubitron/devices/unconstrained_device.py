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

from typing import Any, TYPE_CHECKING

from qubitron import protocols, value
from qubitron._doc import document
from qubitron.devices import device

if TYPE_CHECKING:
    import qubitron


@value.value_equality()
class _UnconstrainedDevice(device.Device):
    """A device that allows everything, infinitely fast."""

    def duration_of(self, operation: qubitron.Operation) -> qubitron.Duration:
        return value.Duration(picos=0)

    def validate_moment(self, moment) -> None:
        pass

    def validate_circuit(self, circuit) -> None:
        pass

    def __repr__(self) -> str:
        return 'qubitron.UNCONSTRAINED_DEVICE'

    def _value_equality_values_(self) -> Any:
        return ()

    def _json_dict_(self) -> dict[str, Any]:
        return protocols.obj_to_dict_helper(self, [])


UNCONSTRAINED_DEVICE: device.Device = _UnconstrainedDevice()
document(UNCONSTRAINED_DEVICE, """A device with no constraints on operations or qubits.""")
