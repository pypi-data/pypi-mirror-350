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

import numpy as np
import pytest

import qubitron


def test_external() -> None:
    for t in ['a', 1j]:
        qubitron.testing.assert_equivalent_repr(t)
        qubitron.testing.assert_equivalent_repr(t, setup_code='')

    qubitron.testing.assert_equivalent_repr(np.array([5]), setup_code='from numpy import array')

    with pytest.raises(AssertionError, match='not defined'):
        qubitron.testing.assert_equivalent_repr(np.array([5]))


def test_custom_class_repr() -> None:
    class CustomRepr:  # pragma: no cover
        setup_code = """class CustomRepr:
            def __init__(self, eq_val):
                self.eq_val = eq_val
            def __pow__(self, exponent):
                return self
        """

        def __init__(self, eq_val, repr_str: str):
            self.eq_val = eq_val
            self.repr_str = repr_str

        def __eq__(self, other):
            return self.eq_val == getattr(other, 'eq_val', None)

        def __ne__(self, other):
            return not self == other

        def __repr__(self):
            return self.repr_str

    qubitron.testing.assert_equivalent_repr(
        CustomRepr('b', "CustomRepr('b')"), setup_code=CustomRepr.setup_code
    )
    qubitron.testing.assert_equivalent_repr(
        CustomRepr('a', "CustomRepr('a')"), setup_code=CustomRepr.setup_code
    )

    # Non-equal values.
    with pytest.raises(AssertionError, match=r'eval\(repr\(value\)\): a'):
        qubitron.testing.assert_equivalent_repr(CustomRepr('a', "'a'"))
    with pytest.raises(AssertionError, match=r'eval\(repr\(value\)\): 1'):
        qubitron.testing.assert_equivalent_repr(CustomRepr('a', "1"))

    # Single failure out of many.
    with pytest.raises(AssertionError, match=r'eval\(repr\(value\)\): a'):
        qubitron.testing.assert_equivalent_repr(CustomRepr('a', "'a'"))

    # Syntax errors.
    with pytest.raises(AssertionError, match='SyntaxError'):
        qubitron.testing.assert_equivalent_repr(CustomRepr('a', "("))
    with pytest.raises(AssertionError, match='SyntaxError'):
        qubitron.testing.assert_equivalent_repr(CustomRepr('a', "return 1"))

    # Not dottable.
    with pytest.raises(AssertionError, match=r'dottable'):
        qubitron.testing.assert_equivalent_repr(
            CustomRepr(5, "CustomRepr(5)**1"), setup_code=CustomRepr.setup_code
        )


def test_imports_qubitron_by_default() -> None:
    qubitron.testing.assert_equivalent_repr(qubitron.NamedQubit('a'))
