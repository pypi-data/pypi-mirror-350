# Copyright 2022 The Qubitron Developers
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

from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    import qubitron


@overload
def q(__x: int) -> qubitron.LineQubit: ...


@overload
def q(__row: int, __col: int) -> qubitron.GridQubit: ...


@overload
def q(__name: str) -> qubitron.NamedQubit: ...


def q(*args: int | str) -> qubitron.LineQubit | qubitron.GridQubit | qubitron.NamedQubit:
    """Constructs a qubit id of the appropriate type based on args.

    This is shorthand for constructing qubit ids of common types:
    >>> qubitron.q(1) == qubitron.LineQubit(1)
    True
    >>> qubitron.q(1, 2) == qubitron.GridQubit(1, 2)
    True
    >>> qubitron.q("foo") == qubitron.NamedQubit("foo")
    True

    Note that arguments should be treated as positional only.

    Args:
        *args: One or two ints, or a single str, as described above.

    Returns:
        qubitron.LineQubit if called with one integer arg.
        qubitron.GridQubit if called with two integer args.
        qubitron.NamedQubit if called with one string arg.

    Raises:
        ValueError: if called with invalid arguments.
    """
    import qubitron  # avoid circular import

    if len(args) == 1:
        if isinstance(args[0], int):
            return qubitron.LineQubit(args[0])
        elif isinstance(args[0], str):
            return qubitron.NamedQubit(args[0])
    elif len(args) == 2:
        if isinstance(args[0], int) and isinstance(args[1], int):
            return qubitron.GridQubit(args[0], args[1])
    raise ValueError(f"Could not construct qubit: args={args}")
