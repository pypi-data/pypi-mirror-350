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

import pytest
import sympy

import qubitron
from qubitron.work import _MeasurementSpec, InitObsSetting, observables_to_settings
from qubitron.work.observable_settings import _hashable_param, _max_weight_observable, _max_weight_state


def test_init_obs_setting() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    setting = InitObsSetting(
        init_state=qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1), observable=qubitron.X(q0) * qubitron.Y(q1)
    )
    assert str(setting) == '+Z(q(0)) * +Z(q(1)) → X(q(0))*Y(q(1))'
    assert eval(repr(setting)) == setting

    with pytest.raises(ValueError):
        setting = InitObsSetting(init_state=qubitron.KET_ZERO(q0), observable=qubitron.X(q0) * qubitron.Y(q1))


def test_max_weight_observable() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    observables = [qubitron.X(q0), qubitron.X(q1)]
    assert _max_weight_observable(observables) == qubitron.X(q0) * qubitron.X(q1)

    observables = [qubitron.X(q0), qubitron.X(q1), qubitron.Z(q1)]
    assert _max_weight_observable(observables) is None


def test_max_weight_state() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    states = [qubitron.KET_PLUS(q0), qubitron.KET_PLUS(q1)]
    assert _max_weight_state(states) == qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1)

    states = [qubitron.KET_PLUS(q0), qubitron.KET_PLUS(q1), qubitron.KET_MINUS(q1)]
    assert _max_weight_state(states) is None


def test_observable_to_setting() -> None:
    q0, q1, q2 = qubitron.LineQubit.range(3)
    observables = [qubitron.X(q0) * qubitron.Y(q1), qubitron.Z(q2) * 1]

    zero_state = qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1) * qubitron.KET_ZERO(q2)
    settings_should_be = [
        InitObsSetting(zero_state, observables[0]),
        InitObsSetting(zero_state, observables[1]),
    ]
    assert list(observables_to_settings(observables, qubits=[q0, q1, q2])) == settings_should_be


def test_param_hash() -> None:
    params1 = [('beta', 1.23), ('gamma', 4.56)]
    params2 = [('beta', 1.23), ('gamma', 4.56)]
    params3 = [('beta', 1.24), ('gamma', 4.57)]
    params4 = [('beta', 1.23 + 0.01j), ('gamma', 4.56 + 0.01j)]
    params5 = [('beta', 1.23 + 0.01j), ('gamma', 4.56 + 0.01j)]
    params3 = [('beta', 1.24), ('gamma', 4.57)]
    assert _hashable_param(params1) == _hashable_param(params1)
    assert hash(_hashable_param(params1)) == hash(_hashable_param(params1))
    assert _hashable_param(params1) == _hashable_param(params2)
    assert hash(_hashable_param(params1)) == hash(_hashable_param(params2))
    assert _hashable_param(params1) != _hashable_param(params3)
    assert hash(_hashable_param(params1)) != hash(_hashable_param(params3))
    assert _hashable_param(params1) != _hashable_param(params4)
    assert hash(_hashable_param(params1)) != hash(_hashable_param(params4))
    assert _hashable_param(params4) == _hashable_param(params5)
    assert hash(_hashable_param(params4)) == hash(_hashable_param(params5))


def test_measurement_spec() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    setting = InitObsSetting(
        init_state=qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1), observable=qubitron.X(q0) * qubitron.Y(q1)
    )
    meas_spec = _MeasurementSpec(
        max_setting=setting, circuit_params={'beta': 0.123, 'gamma': 0.456}
    )
    meas_spec2 = _MeasurementSpec(
        max_setting=setting, circuit_params={'beta': 0.123, 'gamma': 0.456}
    )
    assert hash(meas_spec) == hash(meas_spec2)
    qubitron.testing.assert_equivalent_repr(meas_spec)


def test_measurement_spec_no_symbols() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    setting = InitObsSetting(
        init_state=qubitron.KET_ZERO(q0) * qubitron.KET_ZERO(q1), observable=qubitron.X(q0) * qubitron.Y(q1)
    )
    meas_spec = _MeasurementSpec(max_setting=setting, circuit_params={'beta': sympy.Symbol('t')})
    with pytest.raises(ValueError, match='Cannot convert'):
        _ = hash(meas_spec)
