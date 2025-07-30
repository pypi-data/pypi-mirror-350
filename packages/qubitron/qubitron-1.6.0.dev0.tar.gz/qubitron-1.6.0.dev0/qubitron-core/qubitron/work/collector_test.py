# Copyright 2019 The Qubitron Developers
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

import duet
import pytest

import qubitron


def test_circuit_sample_job_equality() -> None:
    eq = qubitron.testing.EqualsTester()
    c1 = qubitron.Circuit()
    c2 = qubitron.Circuit(qubitron.measure(qubitron.LineQubit(0)))

    eq.add_equality_group(
        qubitron.CircuitSampleJob(c1, repetitions=10),
        qubitron.CircuitSampleJob(c1, repetitions=10, tag=None),
    )
    eq.add_equality_group(qubitron.CircuitSampleJob(c2, repetitions=10))
    eq.add_equality_group(qubitron.CircuitSampleJob(c1, repetitions=100))
    eq.add_equality_group(qubitron.CircuitSampleJob(c1, repetitions=10, tag='test'))


def test_circuit_sample_job_repr() -> None:
    qubitron.testing.assert_equivalent_repr(
        qubitron.CircuitSampleJob(qubitron.Circuit(qubitron.H(qubitron.LineQubit(0))), repetitions=10, tag='guess')
    )


@duet.sync
async def test_async_collect() -> None:
    received = []

    class TestCollector(qubitron.Collector):
        def next_job(self):
            q = qubitron.LineQubit(0)
            circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
            return qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag='test')

        def on_job_result(self, job, result):
            received.append(job.tag)

    await TestCollector().collect_async(
        sampler=qubitron.Simulator(), max_total_samples=100, concurrency=5
    )
    assert received == ['test'] * 10


def test_collect() -> None:
    received = []

    class TestCollector(qubitron.Collector):
        def next_job(self):
            q = qubitron.LineQubit(0)
            circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
            return qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag='test')

        def on_job_result(self, job, result):
            received.append(job.tag)

    TestCollector().collect(sampler=qubitron.Simulator(), max_total_samples=100, concurrency=5)
    assert received == ['test'] * 10


def test_failed_job() -> None:
    class FailingSampler:
        async def run_async(self, circuit, repetitions):
            await duet.completed_future(None)
            raise Exception('job failed!')

    class TestCollector(qubitron.Collector):
        def next_job(self):
            q = qubitron.LineQubit(0)
            circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
            return qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag='test')

        def on_job_result(self, job, result):
            pass

    with pytest.raises(Exception, match='job failed!'):
        TestCollector().collect(
            sampler=FailingSampler(),  # type:ignore
            max_total_samples=100,
            concurrency=5,
        )


def test_collect_with_reaction() -> None:
    events = [0]
    sent = 0
    received = 0

    class TestCollector(qubitron.Collector):
        def next_job(self):
            nonlocal sent
            if sent >= received + 3:
                return None
            sent += 1
            events.append(sent)
            q = qubitron.LineQubit(0)
            circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
            return qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag=sent)

        def on_job_result(self, job, result):
            nonlocal received
            received += 1
            events.append(-job.tag)

    TestCollector().collect(sampler=qubitron.Simulator(), max_total_samples=100, concurrency=5)
    # Expected sends and receives are present.
    assert sorted(events) == list(range(-10, 1 + 10))
    # Sends are in order.
    assert [e for e in events if e > 0] == list(range(1, 11))
    # Every receive comes after the corresponding send.
    assert all(events.index(-k) > events.index(k) for k in range(1, 11))


def test_flatten_jobs_terminate_from_collector() -> None:
    sent = False
    received = []

    class TestCollector(qubitron.Collector):
        def next_job(self):
            nonlocal sent
            if sent:
                return
            sent = True
            q = qubitron.LineQubit(0)
            circuit = qubitron.Circuit(qubitron.H(q), qubitron.measure(q))
            a = qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag='test')
            b = qubitron.CircuitSampleJob(circuit=circuit, repetitions=10, tag='test')
            return [[a, None], [[[None]]], [[[]]], b]

        def on_job_result(self, job, result):
            received.append(job.tag)

    TestCollector().collect(sampler=qubitron.Simulator(), concurrency=5)
    assert received == ['test'] * 2
