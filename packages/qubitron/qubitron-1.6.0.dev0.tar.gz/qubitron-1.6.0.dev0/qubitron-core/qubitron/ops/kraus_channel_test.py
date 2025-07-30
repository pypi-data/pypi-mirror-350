# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import numpy as np
import pytest

import qubitron


def test_kraus_channel_from_channel():
    q0 = qubitron.LineQubit(0)
    dp = qubitron.depolarize(0.1)
    kc = qubitron.KrausChannel.from_channel(dp, key='dp')
    assert qubitron.measurement_key_name(kc) == 'dp'
    qubitron.testing.assert_consistent_channel(kc)

    circuit = qubitron.Circuit(kc.on(q0))
    sim = qubitron.Simulator(seed=0)

    results = sim.simulate(circuit)
    assert 'dp' in results.measurements
    # The depolarizing channel has four Kraus operators.
    assert results.measurements['dp'] in range(4)


def test_kraus_channel_equality():
    dp_pt1 = qubitron.depolarize(0.1)
    dp_pt2 = qubitron.depolarize(0.2)
    kc_a1 = qubitron.KrausChannel.from_channel(dp_pt1, key='a')
    kc_a2 = qubitron.KrausChannel.from_channel(dp_pt2, key='a')
    kc_b1 = qubitron.KrausChannel.from_channel(dp_pt1, key='b')

    # Even if their effect is the same, KrausChannels are not treated as equal
    # to other channels defined in Qubitron.
    assert kc_a1 != dp_pt1
    assert kc_a1 != kc_a2
    assert kc_a1 != kc_b1
    assert kc_a2 != kc_b1

    ops = [np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])]
    x_meas = qubitron.KrausChannel(ops)
    ops_inv = list(reversed(ops))
    x_meas_inv = qubitron.KrausChannel(ops_inv)
    # Even though these have the same effect on the circuit, their measurement
    # behavior differs, so they are considered non-equal.
    assert x_meas != x_meas_inv


def test_kraus_channel_remap_keys():
    dp = qubitron.depolarize(0.1)
    kc = qubitron.KrausChannel.from_channel(dp)
    with pytest.raises(TypeError):
        _ = qubitron.measurement_key_name(kc)
    assert qubitron.with_measurement_key_mapping(kc, {'a': 'b'}) is NotImplemented

    kc_x = qubitron.KrausChannel.from_channel(dp, key='x')
    assert qubitron.with_measurement_key_mapping(kc_x, {'a': 'b'}) is kc_x
    assert qubitron.measurement_key_name(qubitron.with_key_path(kc_x, ('path',))) == 'path:x'
    assert qubitron.measurement_key_name(qubitron.with_key_path_prefix(kc_x, ('path',))) == 'path:x'

    kc_a = qubitron.KrausChannel.from_channel(dp, key='a')
    kc_b = qubitron.KrausChannel.from_channel(dp, key='b')
    assert kc_a != kc_b
    assert qubitron.with_measurement_key_mapping(kc_a, {'a': 'b'}) == kc_b


def test_kraus_channel_from_kraus():
    q0 = qubitron.LineQubit(0)
    # This is equivalent to an X-basis measurement.
    ops = [np.array([[1, 1], [1, 1]]) * 0.5, np.array([[1, -1], [-1, 1]]) * 0.5]
    x_meas = qubitron.KrausChannel(ops, key='x_meas')
    assert qubitron.measurement_key_name(x_meas) == 'x_meas'

    circuit = qubitron.Circuit(qubitron.H(q0), x_meas.on(q0))
    sim = qubitron.Simulator(seed=0)

    results = sim.simulate(circuit)
    assert 'x_meas' in results.measurements
    assert results.measurements['x_meas'] == 0


def test_kraus_channel_str():
    # This is equivalent to an X-basis measurement.
    ops = [np.array([[1, 1], [1, 1]]) * 0.5, np.array([[1, -1], [-1, 1]]) * 0.5]
    x_meas = qubitron.KrausChannel(ops)
    assert (
        str(x_meas)
        == """KrausChannel([array([[0.5, 0.5],
       [0.5, 0.5]]), array([[ 0.5, -0.5],
       [-0.5,  0.5]])])"""
    )
    x_meas_keyed = qubitron.KrausChannel(ops, key='x_meas')
    assert (
        str(x_meas_keyed)
        == """KrausChannel([array([[0.5, 0.5],
       [0.5, 0.5]]), array([[ 0.5, -0.5],
       [-0.5,  0.5]])], key=x_meas)"""
    )


def test_kraus_channel_repr():
    # This is equivalent to an X-basis measurement.
    ops = [
        np.array([[1, 1], [1, 1]], dtype=np.complex64) * 0.5,
        np.array([[1, -1], [-1, 1]], dtype=np.complex64) * 0.5,
    ]
    x_meas = qubitron.KrausChannel(ops, key='x_meas')
    assert (
        repr(x_meas)
        == """\
qubitron.KrausChannel(kraus_ops=[\
np.array([[(0.5+0j), (0.5+0j)], [(0.5+0j), (0.5+0j)]], dtype=np.dtype('complex64')), \
np.array([[(0.5+0j), (-0.5+0j)], [(-0.5+0j), (0.5+0j)]], dtype=np.dtype('complex64'))], \
key='x_meas')"""
    )


def test_empty_ops_fails():
    ops = []

    with pytest.raises(ValueError, match='must have at least one operation'):
        _ = qubitron.KrausChannel(kraus_ops=ops, key='m')


def test_ops_mismatch_fails():
    op2 = np.zeros((4, 4))
    op2[1][1] = 1
    ops = [np.array([[1, 0], [0, 0]]), op2]

    with pytest.raises(ValueError, match='Inconsistent Kraus operator shapes'):
        _ = qubitron.KrausChannel(kraus_ops=ops, key='m')


def test_nonqubit_kraus_ops_fails():
    ops = [np.array([[1, 0, 0], [0, 0, 0]]), np.array([[0, 0, 0], [0, 1, 0]])]

    with pytest.raises(ValueError, match='Input Kraus ops'):
        _ = qubitron.KrausChannel(kraus_ops=ops, key='m')


def test_validate():
    # Not quite CPTP.
    ops = [np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 0.9]])]
    with pytest.raises(ValueError, match='CPTP map'):
        _ = qubitron.KrausChannel(kraus_ops=ops, key='m', validate=True)
