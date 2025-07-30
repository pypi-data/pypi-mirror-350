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

import pickle

import pytest

import qubitron


def test_repr() -> None:
    assert repr(qubitron.InsertStrategy.NEW) == 'qubitron.InsertStrategy.NEW'
    assert str(qubitron.InsertStrategy.NEW) == 'NEW'


@pytest.mark.parametrize(
    'strategy',
    [
        qubitron.InsertStrategy.NEW,
        qubitron.InsertStrategy.NEW_THEN_INLINE,
        qubitron.InsertStrategy.INLINE,
        qubitron.InsertStrategy.EARLIEST,
    ],
    ids=lambda strategy: strategy.name,
)
def test_identity_after_pickling(strategy: qubitron.InsertStrategy) -> None:
    unpickled_strategy = pickle.loads(pickle.dumps(strategy))
    assert unpickled_strategy is strategy
