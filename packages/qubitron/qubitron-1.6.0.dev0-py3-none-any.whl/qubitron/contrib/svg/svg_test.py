# pylint: disable=wrong-or-nonexistent-copyright-notice

from __future__ import annotations

import IPython.display
import numpy as np
import pytest

import qubitron
from qubitron.contrib.svg import circuit_to_svg, SVGCircuit


def test_svg() -> None:
    a, b, c = qubitron.LineQubit.range(3)

    svg_text = circuit_to_svg(
        qubitron.Circuit(
            qubitron.CNOT(a, b),
            qubitron.CZ(b, c),
            qubitron.SWAP(a, c),
            qubitron.PhasedXPowGate(exponent=0.123, phase_exponent=0.456).on(c),
            qubitron.Z(a),
            qubitron.measure(a, b, c, key='z'),
            qubitron.MatrixGate(np.eye(2)).on(a),
        )
    )
    assert '?' in svg_text
    assert '<svg' in svg_text
    assert '</svg>' in svg_text


def test_svg_noise() -> None:
    noise_model = qubitron.ConstantQubitNoiseModel(qubitron.DepolarizingChannel(p=1e-3))
    q = qubitron.LineQubit(0)
    circuit = qubitron.Circuit(qubitron.X(q))
    circuit = qubitron.Circuit(noise_model.noisy_moments(circuit.moments, [q]))
    svg = circuit_to_svg(circuit)
    assert '>D(0.001)</text>' in svg


def test_validation() -> None:
    with pytest.raises(ValueError):
        circuit_to_svg(qubitron.Circuit())


def test_empty_moments() -> None:
    a, b = qubitron.LineQubit.range(2)
    svg_1 = circuit_to_svg(
        qubitron.Circuit(
            qubitron.Moment(),
            qubitron.Moment(qubitron.CNOT(a, b)),
            qubitron.Moment(),
            qubitron.Moment(qubitron.SWAP(a, b)),
            qubitron.Moment(qubitron.Z(a)),
            qubitron.Moment(qubitron.measure(a, b, key='z')),
            qubitron.Moment(),
        )
    )
    assert '<svg' in svg_1
    assert '</svg>' in svg_1

    svg_2 = circuit_to_svg(qubitron.Circuit(qubitron.Moment()))
    assert '<svg' in svg_2
    assert '</svg>' in svg_2


@pytest.mark.parametrize(
    'symbol,svg_symbol',
    [
        ('<a', '&lt;a'),
        ('<a&', '&lt;a&amp;'),
        ('<=b', '&lt;=b'),
        ('>c', '&gt;c'),
        ('>=d', '&gt;=d'),
        ('>e<', '&gt;e&lt;'),
        ('A[<virtual>]B[qubitron.VirtualTag()]C>D<E', 'ABC&gt;D&lt;E'),
    ],
)
def test_gate_with_less_greater_str(symbol, svg_symbol) -> None:
    class CustomGate(qubitron.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _circuit_diagram_info_(self, _) -> qubitron.CircuitDiagramInfo:
            return qubitron.CircuitDiagramInfo(wire_symbols=[symbol])

    circuit = qubitron.Circuit(CustomGate().on(qubitron.LineQubit(0)))
    svg_circuit = SVGCircuit(circuit)
    svg = svg_circuit._repr_svg_()

    _ = IPython.display.SVG(svg)
    assert svg_symbol in svg
