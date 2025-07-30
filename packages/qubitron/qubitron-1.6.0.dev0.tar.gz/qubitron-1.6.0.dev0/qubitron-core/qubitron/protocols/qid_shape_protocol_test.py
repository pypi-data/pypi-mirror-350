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

import pytest

import qubitron


def test_qid_shape() -> None:
    class ShapeObj:
        def _qid_shape_(self):
            return (1, 2, 3)

    class NumObj:
        def _num_qubits_(self):
            return 2

    class NotImplShape:
        def _qid_shape_(self):
            return NotImplemented

    class NotImplNum:
        def _num_qubits_(self):
            return NotImplemented

    class NotImplBoth:
        def _num_qubits_(self):
            return NotImplemented

        def _qid_shape_(self):
            return NotImplemented

    class NoProtocol:
        pass

    assert qubitron.qid_shape(ShapeObj()) == (1, 2, 3)
    assert qubitron.num_qubits(ShapeObj()) == 3
    assert qubitron.qid_shape(NumObj()) == (2, 2)
    assert qubitron.num_qubits(NumObj()) == 2
    with pytest.raises(TypeError, match='_qid_shape_.*NotImplemented'):
        qubitron.qid_shape(NotImplShape())
    with pytest.raises(TypeError, match='_qid_shape_.*NotImplemented'):
        qubitron.num_qubits(NotImplShape())
    with pytest.raises(TypeError, match='_num_qubits_.*NotImplemented'):
        qubitron.qid_shape(NotImplNum())
    with pytest.raises(TypeError, match='_num_qubits_.*NotImplemented'):
        qubitron.num_qubits(NotImplNum())
    with pytest.raises(TypeError, match='_qid_shape_.*NotImplemented'):
        qubitron.qid_shape(NotImplBoth())
    with pytest.raises(TypeError, match='_num_qubits_.*NotImplemented'):
        qubitron.num_qubits(NotImplBoth())
    with pytest.raises(TypeError):
        qubitron.qid_shape(NoProtocol())
    with pytest.raises(TypeError):
        qubitron.num_qubits(NoProtocol())
    assert qubitron.qid_shape(qubitron.LineQid.for_qid_shape((1, 2, 3))) == (1, 2, 3)
    assert qubitron.num_qubits(qubitron.LineQid.for_qid_shape((1, 2, 3))) == 3
