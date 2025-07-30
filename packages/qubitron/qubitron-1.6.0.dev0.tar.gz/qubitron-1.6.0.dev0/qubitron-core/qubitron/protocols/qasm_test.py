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


class NoMethod:
    pass


class ReturnsNotImplemented:
    def _qasm_(self):
        return NotImplemented


class ReturnsText:
    def _qasm_(self):
        return 'text'


class ExpectsArgs:
    def _qasm_(self, args):
        return 'text'


class ExpectsArgsQubits:
    def _qasm_(self, args, qubits):
        return 'text'


def test_qasm() -> None:
    assert qubitron.qasm(NoMethod(), default=None) is None
    assert qubitron.qasm(NoMethod(), default=5) == 5
    assert qubitron.qasm(ReturnsText()) == 'text'

    with pytest.raises(TypeError, match='no _qasm_ method'):
        _ = qubitron.qasm(NoMethod())
    with pytest.raises(TypeError, match='returned NotImplemented or None'):
        _ = qubitron.qasm(ReturnsNotImplemented())

    assert qubitron.qasm(ExpectsArgs(), args=qubitron.QasmArgs()) == 'text'
    assert qubitron.qasm(ExpectsArgsQubits(), args=qubitron.QasmArgs(), qubits=()) == 'text'


def test_qasm_qubits_improperly_supplied() -> None:
    with pytest.raises(TypeError, match="does not expect qubits or args to be specified"):
        _ = qubitron.qasm(qubitron.Circuit(), qubits=[qubitron.LineQubit(1)])


def test_qasm_args_formatting() -> None:
    args = qubitron.QasmArgs()
    assert args.format_field(0.01, '') == '0.01'
    assert args.format_field(0.01, 'half_turns') == 'pi*0.01'
    assert args.format_field(0.00001, '') == '1.0e-05'
    assert args.format_field(0.00001, 'half_turns') == 'pi*1.0e-05'
    assert args.format_field(1e-10, 'half_turns') == 'pi*1.0e-10'
    args = qubitron.QasmArgs(precision=6)
    assert args.format_field(0.00001234, '') == '1.2e-05'
    assert args.format_field(0.00001234, 'half_turns') == 'pi*1.2e-05'
