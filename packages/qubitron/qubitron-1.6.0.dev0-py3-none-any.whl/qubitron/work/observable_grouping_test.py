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


def test_group_settings_greedy_one_group() -> None:
    qubits = qubitron.LineQubit.range(2)
    q0, q1 = qubits
    terms = [qubitron.X(q0), qubitron.Y(q1)]
    settings = list(qubitron.work.observables_to_settings(terms, qubits))
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 1

    group_max_obs_should_be = [qubitron.X(q0) * qubitron.Y(q1)]
    group_max_settings_should_be = list(
        qubitron.work.observables_to_settings(group_max_obs_should_be, qubits)
    )
    assert set(grouped_settings.keys()) == set(group_max_settings_should_be)

    the_group = grouped_settings[group_max_settings_should_be[0]]
    assert set(the_group) == set(settings)


def test_group_settings_greedy_two_groups() -> None:
    qubits = qubitron.LineQubit.range(2)
    q0, q1 = qubits
    terms = [qubitron.X(q0) * qubitron.X(q1), qubitron.Y(q0) * qubitron.Y(q1)]
    settings = list(qubitron.work.observables_to_settings(terms, qubits))
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 2

    group_max_obs_should_be = terms.copy()
    group_max_settings_should_be = list(
        qubitron.work.observables_to_settings(group_max_obs_should_be, qubits)
    )
    assert set(grouped_settings.keys()) == set(group_max_settings_should_be)


def test_group_settings_greedy_single_item() -> None:
    qubits = qubitron.LineQubit.range(2)
    q0, q1 = qubits
    term = qubitron.X(q0) * qubitron.X(q1)

    settings = list(qubitron.work.observables_to_settings([term], qubits))
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 1
    assert list(grouped_settings.keys())[0] == settings[0]
    assert list(grouped_settings.values())[0][0] == settings[0]


def test_group_settings_greedy_empty() -> None:
    assert qubitron.work.group_settings_greedy([]) == dict()


def test_group_settings_greedy_init_state_compat() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    settings = [
        qubitron.work.InitObsSetting(
            init_state=qubitron.KET_PLUS(q0) * qubitron.KET_ZERO(q1), observable=qubitron.X(q0)
        ),
        qubitron.work.InitObsSetting(
            init_state=qubitron.KET_PLUS(q0) * qubitron.KET_ZERO(q1), observable=qubitron.Z(q1)
        ),
    ]
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 1


def test_group_settings_greedy_init_state_compat_sparse() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    settings = [
        qubitron.work.InitObsSetting(init_state=qubitron.KET_PLUS(q0), observable=qubitron.X(q0)),
        qubitron.work.InitObsSetting(init_state=qubitron.KET_ZERO(q1), observable=qubitron.Z(q1)),
    ]
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    # pylint: disable=line-too-long
    grouped_settings_should_be = {
        qubitron.work.InitObsSetting(
            init_state=qubitron.KET_PLUS(q0) * qubitron.KET_ZERO(q1), observable=qubitron.X(q0) * qubitron.Z(q1)
        ): settings
    }
    assert grouped_settings == grouped_settings_should_be


def test_group_settings_greedy_init_state_incompat() -> None:
    q0, q1 = qubitron.LineQubit.range(2)
    settings = [
        qubitron.work.InitObsSetting(
            init_state=qubitron.KET_PLUS(q0) * qubitron.KET_PLUS(q1), observable=qubitron.X(q0)
        ),
        qubitron.work.InitObsSetting(init_state=qubitron.KET_ZERO(q1), observable=qubitron.Z(q1)),
    ]
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 2


def test_group_settings_greedy_hydrogen() -> None:
    qubits = qubitron.LineQubit.range(4)
    q0, q1, q2, q3 = qubits
    terms = [
        0.1711977489805745 * qubitron.Z(q0),
        0.17119774898057447 * qubitron.Z(q1),
        -0.2227859302428765 * qubitron.Z(q2),
        -0.22278593024287646 * qubitron.Z(q3),
        0.16862219157249939 * qubitron.Z(q0) * qubitron.Z(q1),
        0.04532220205777764 * qubitron.Y(q0) * qubitron.X(q1) * qubitron.X(q2) * qubitron.Y(q3),
        -0.0453222020577776 * qubitron.Y(q0) * qubitron.Y(q1) * qubitron.X(q2) * qubitron.X(q3),
        -0.0453222020577776 * qubitron.X(q0) * qubitron.X(q1) * qubitron.Y(q2) * qubitron.Y(q3),
        0.04532220205777764 * qubitron.X(q0) * qubitron.Y(q1) * qubitron.Y(q2) * qubitron.X(q3),
        0.12054482203290037 * qubitron.Z(q0) * qubitron.Z(q2),
        0.16586702409067802 * qubitron.Z(q0) * qubitron.Z(q3),
        0.16586702409067802 * qubitron.Z(q1) * qubitron.Z(q2),
        0.12054482203290037 * qubitron.Z(q1) * qubitron.Z(q3),
        0.1743484418396392 * qubitron.Z(q2) * qubitron.Z(q3),
    ]
    settings = qubitron.work.observables_to_settings(terms, qubits)
    grouped_settings = qubitron.work.group_settings_greedy(settings)
    assert len(grouped_settings) == 5

    group_max_obs_should_be = [
        qubitron.Y(q0) * qubitron.X(q1) * qubitron.X(q2) * qubitron.Y(q3),
        qubitron.Y(q0) * qubitron.Y(q1) * qubitron.X(q2) * qubitron.X(q3),
        qubitron.X(q0) * qubitron.X(q1) * qubitron.Y(q2) * qubitron.Y(q3),
        qubitron.X(q0) * qubitron.Y(q1) * qubitron.Y(q2) * qubitron.X(q3),
        qubitron.Z(q0) * qubitron.Z(q1) * qubitron.Z(q2) * qubitron.Z(q3),
    ]
    group_max_settings_should_be = qubitron.work.observables_to_settings(
        group_max_obs_should_be, qubits
    )

    assert set(grouped_settings.keys()) == set(group_max_settings_should_be)
    groups = list(grouped_settings.values())
    assert len(groups[0]) == 1
    assert len(groups[1]) == 1
    assert len(groups[2]) == 1
    assert len(groups[3]) == 1
    assert len(groups[4]) == len(terms) - 4
