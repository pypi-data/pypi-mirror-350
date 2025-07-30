# Copyright 2021 The Qubitron Developers
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

import qubitron


def test_control_key() -> None:
    class Named:
        def _control_keys_(self):
            return frozenset([qubitron.MeasurementKey('key')])

    class NoImpl:
        def _control_keys_(self):
            return NotImplemented

    assert qubitron.control_keys(Named()) == {qubitron.MeasurementKey('key')}
    assert not qubitron.control_keys(NoImpl())
    assert not qubitron.control_keys(5)
