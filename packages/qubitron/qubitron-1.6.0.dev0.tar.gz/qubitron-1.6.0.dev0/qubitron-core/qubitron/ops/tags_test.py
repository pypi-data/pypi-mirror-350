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

import qubitron


def test_virtual_tag() -> None:
    tag1 = qubitron.ops.VirtualTag()
    tag2 = qubitron.ops.VirtualTag()

    assert tag1 == tag2
    assert str(tag1) == str(tag2) == '<virtual>'

    qubitron.testing.assert_equivalent_repr(tag1)
    qubitron.testing.assert_equivalent_repr(tag2)


def test_routing_swap_tag() -> None:
    tag1 = qubitron.ops.RoutingSwapTag()
    tag2 = qubitron.ops.RoutingSwapTag()

    assert tag1 == tag2
    assert str(tag1) == str(tag2) == '<r>'
    assert hash(tag1) == hash(tag2)

    qubitron.testing.assert_equivalent_repr(tag1)
    qubitron.testing.assert_equivalent_repr(tag2)
