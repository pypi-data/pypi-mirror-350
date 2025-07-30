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
"""Methods for resolving JSON types during serialization."""

from __future__ import annotations

import datetime
import functools
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    import qubitron
    import qubitron.devices.unconstrained_device
    import qubitron.ops.pauli_gates
    from qubitron.protocols.json_serialization import ObjectFactory


# Needed for backwards compatible named tuples of CrossEntropyResult
CrossEntropyPair = NamedTuple('CrossEntropyPair', [('num_cycle', int), ('xeb_fidelity', float)])
SpecklePurityPair = NamedTuple('SpecklePurityPair', [('num_cycle', int), ('purity', float)])
CrossEntropyResult = NamedTuple(
    'CrossEntropyResult',
    [
        ('data', list[CrossEntropyPair]),
        ('repetitions', int),
        ('purity_data', list[SpecklePurityPair] | None),
    ],
)
CrossEntropyResultDict = NamedTuple(
    'CrossEntropyResultDict', [('results', dict[tuple['qubitron.Qid', ...], CrossEntropyResult])]
)


@functools.lru_cache()
def _class_resolver_dictionary() -> dict[str, ObjectFactory]:
    import numpy as np
    import pandas as pd

    import qubitron
    from qubitron.devices import InsertionNoiseModel
    from qubitron.devices.noise_model import _NoNoiseModel
    from qubitron.experiments import GridInteractionLayer
    from qubitron.ops import raw_types

    def _boolean_hamiltonian_gate_op(qubit_map, boolean_strs, theta):
        return qubitron.BooleanHamiltonianGate(
            parameter_names=list(qubit_map.keys()), boolean_strs=boolean_strs, theta=theta
        ).on(*qubit_map.values())

    def _identity_operation_from_dict(qubits, **kwargs):
        return qubitron.identity_each(*qubits)

    def single_qubit_matrix_gate(matrix):
        if not isinstance(matrix, np.ndarray):
            matrix = np.array(matrix, dtype=np.complex128)
        return qubitron.MatrixGate(matrix, qid_shape=(matrix.shape[0],))

    def two_qubit_matrix_gate(matrix):
        if not isinstance(matrix, np.ndarray):
            matrix = np.array(matrix, dtype=np.complex128)
        return qubitron.MatrixGate(matrix, qid_shape=(2, 2))

    def _cross_entropy_result(data, repetitions, **kwargs) -> CrossEntropyResult:
        purity_data = kwargs.get('purity_data', None)
        if purity_data is not None:
            purity_data = [SpecklePurityPair(d, f) for d, f in purity_data]
        return CrossEntropyResult(
            data=[CrossEntropyPair(d, f) for d, f in data],
            repetitions=repetitions,
            purity_data=purity_data,
        )

    def _cross_entropy_result_dict(
        results: list[tuple[list[qubitron.Qid], CrossEntropyResult]], **kwargs
    ) -> CrossEntropyResultDict:
        return CrossEntropyResultDict(results={tuple(qubits): result for qubits, result in results})

    def _parallel_gate_op(gate, qubits):
        return qubitron.parallel_gate_op(gate, *qubits)

    def _datetime(timestamp: float) -> datetime.datetime:
        # We serialize datetimes (both with ("aware") and without ("naive") timezone information)
        # as unix timestamps. The deserialized datetime will always refer to the
        # same point in time, but will be re-constructed as a timezone-aware object.
        #
        # If `o` is a naive datetime,  o != read_json(to_json(o)) because Python doesn't
        # let you compare aware and naive datetimes.
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    def _symmetricalqidpair(qids):
        return frozenset(qids)

    import sympy

    return {
        'AmplitudeDampingChannel': qubitron.AmplitudeDampingChannel,
        'AnyIntegerPowerGateFamily': qubitron.AnyIntegerPowerGateFamily,
        'AnyUnitaryGateFamily': qubitron.AnyUnitaryGateFamily,
        'AsymmetricDepolarizingChannel': qubitron.AsymmetricDepolarizingChannel,
        'BitFlipChannel': qubitron.BitFlipChannel,
        'BitMaskKeyCondition': qubitron.BitMaskKeyCondition,
        'BitstringAccumulator': qubitron.work.BitstringAccumulator,
        'BooleanHamiltonianGate': qubitron.BooleanHamiltonianGate,
        'CCNotPowGate': qubitron.CCNotPowGate,
        'CCXPowGate': qubitron.CCXPowGate,
        'CCZPowGate': qubitron.CCZPowGate,
        'Circuit': qubitron.Circuit,
        'CircuitOperation': qubitron.CircuitOperation,
        'ClassicallyControlledOperation': qubitron.ClassicallyControlledOperation,
        'ClassicalDataDictionaryStore': qubitron.ClassicalDataDictionaryStore,
        'CliffordGate': qubitron.CliffordGate,
        'CliffordState': qubitron.CliffordState,
        'CliffordTableau': qubitron.CliffordTableau,
        'CNotPowGate': qubitron.CNotPowGate,
        'Concat': qubitron.Concat,
        'ConstantQubitNoiseModel': qubitron.ConstantQubitNoiseModel,
        'ControlledGate': qubitron.ControlledGate,
        'ControlledOperation': qubitron.ControlledOperation,
        'CSwapGate': qubitron.CSwapGate,
        'CXPowGate': qubitron.CXPowGate,
        'CZPowGate': qubitron.CZPowGate,
        'CZTargetGateset': qubitron.CZTargetGateset,
        'DiagonalGate': qubitron.DiagonalGate,
        'DensePauliString': qubitron.DensePauliString,
        'DepolarizingChannel': qubitron.DepolarizingChannel,
        'DeviceMetadata': qubitron.DeviceMetadata,
        'Duration': qubitron.Duration,
        'FrozenCircuit': qubitron.FrozenCircuit,
        'FSimGate': qubitron.FSimGate,
        'GateFamily': qubitron.GateFamily,
        'GateOperation': qubitron.GateOperation,
        'Gateset': qubitron.Gateset,
        'GeneralizedAmplitudeDampingChannel': qubitron.GeneralizedAmplitudeDampingChannel,
        'GlobalPhaseGate': qubitron.GlobalPhaseGate,
        'GridDeviceMetadata': qubitron.GridDeviceMetadata,
        'GridInteractionLayer': GridInteractionLayer,
        'GridQid': qubitron.GridQid,
        'GridQubit': qubitron.GridQubit,
        'HPowGate': qubitron.HPowGate,
        'ISwapPowGate': qubitron.ISwapPowGate,
        'IdentityGate': qubitron.IdentityGate,
        'InitObsSetting': qubitron.work.InitObsSetting,
        'InsertionNoiseModel': InsertionNoiseModel,
        '_InverseCompositeGate': raw_types._InverseCompositeGate,
        'KeyCondition': qubitron.KeyCondition,
        'KrausChannel': qubitron.KrausChannel,
        'LinearDict': qubitron.LinearDict,
        'LineQubit': qubitron.LineQubit,
        'LineQid': qubitron.LineQid,
        'LineTopology': qubitron.LineTopology,
        'Linspace': qubitron.Linspace,
        'ListSweep': qubitron.ListSweep,
        'qubitron.MSGate': qubitron.MSGate,
        'MatrixGate': qubitron.MatrixGate,
        'MixedUnitaryChannel': qubitron.MixedUnitaryChannel,
        'MeasurementKey': qubitron.MeasurementKey,
        'MeasurementGate': qubitron.MeasurementGate,
        'MeasurementType': qubitron.MeasurementType,
        '_MeasurementSpec': qubitron.work._MeasurementSpec,
        'Moment': qubitron.Moment,
        'MutableDensePauliString': qubitron.MutableDensePauliString,
        'MutablePauliString': qubitron.MutablePauliString,
        '_NoNoiseModel': _NoNoiseModel,
        'NamedQubit': qubitron.NamedQubit,
        'NamedQid': qubitron.NamedQid,
        'NoIdentifierQubit': qubitron.testing.NoIdentifierQubit,
        'ObservableMeasuredResult': qubitron.work.ObservableMeasuredResult,
        'OpIdentifier': qubitron.OpIdentifier,
        'ParamResolver': qubitron.ParamResolver,
        'ParallelGate': qubitron.ParallelGate,
        'ParallelGateFamily': qubitron.ParallelGateFamily,
        'PauliInteractionGate': qubitron.PauliInteractionGate,
        'PauliMeasurementGate': qubitron.PauliMeasurementGate,
        'PauliString': qubitron.PauliString,
        'PauliStringPhasor': qubitron.PauliStringPhasor,
        'PauliStringPhasorGate': qubitron.PauliStringPhasorGate,
        'PauliSum': qubitron.PauliSum,
        '_PauliX': qubitron.ops.pauli_gates._PauliX,
        '_PauliY': qubitron.ops.pauli_gates._PauliY,
        '_PauliZ': qubitron.ops.pauli_gates._PauliZ,
        'PhaseDampingChannel': qubitron.PhaseDampingChannel,
        'PhaseFlipChannel': qubitron.PhaseFlipChannel,
        'PhaseGradientGate': qubitron.PhaseGradientGate,
        'PhasedFSimGate': qubitron.PhasedFSimGate,
        'PhasedISwapPowGate': qubitron.PhasedISwapPowGate,
        'PhasedXPowGate': qubitron.PhasedXPowGate,
        'PhasedXZGate': qubitron.PhasedXZGate,
        'Points': qubitron.Points,
        'Product': qubitron.Product,
        'ProductState': qubitron.ProductState,
        'ProductOfSums': qubitron.ProductOfSums,
        'ProjectorString': qubitron.ProjectorString,
        'ProjectorSum': qubitron.ProjectorSum,
        'QasmUGate': qubitron.circuits.qasm_output.QasmUGate,
        '_QubitAsQid': raw_types._QubitAsQid,
        'QuantumFourierTransformGate': qubitron.QuantumFourierTransformGate,
        'QubitPermutationGate': qubitron.QubitPermutationGate,
        'RandomGateChannel': qubitron.RandomGateChannel,
        'RepetitionsStoppingCriteria': qubitron.work.RepetitionsStoppingCriteria,
        'ResetChannel': qubitron.ResetChannel,
        'Result': qubitron.ResultDict,  # Keep support for Qubitron < 0.14.
        'ResultDict': qubitron.ResultDict,
        'RoutingSwapTag': qubitron.RoutingSwapTag,
        'Rx': qubitron.Rx,
        'Ry': qubitron.Ry,
        'Rz': qubitron.Rz,
        'SingleQubitCliffordGate': qubitron.SingleQubitCliffordGate,
        'SingleQubitPauliStringGateOperation': qubitron.SingleQubitPauliStringGateOperation,
        'SingleQubitReadoutCalibrationResult': qubitron.experiments.SingleQubitReadoutCalibrationResult,
        'SqrtIswapTargetGateset': qubitron.SqrtIswapTargetGateset,
        'StabilizerStateChForm': qubitron.StabilizerStateChForm,
        'StatePreparationChannel': qubitron.StatePreparationChannel,
        'SumOfProducts': qubitron.SumOfProducts,
        'SwapPowGate': qubitron.SwapPowGate,
        'SympyCondition': qubitron.SympyCondition,
        'TaggedOperation': qubitron.TaggedOperation,
        'TensoredConfusionMatrices': qubitron.TensoredConfusionMatrices,
        'TiltedSquareLattice': qubitron.TiltedSquareLattice,
        'ThreeQubitDiagonalGate': qubitron.ThreeQubitDiagonalGate,
        'TrialResult': qubitron.ResultDict,  # keep support for Qubitron < 0.11.
        'TwoQubitDiagonalGate': qubitron.TwoQubitDiagonalGate,
        'TwoQubitGateTabulation': qubitron.TwoQubitGateTabulation,
        '_UnconstrainedDevice': qubitron.devices.unconstrained_device._UnconstrainedDevice,
        '_Unit': qubitron.study.sweeps._Unit,
        'VarianceStoppingCriteria': qubitron.work.VarianceStoppingCriteria,
        'VirtualTag': qubitron.VirtualTag,
        'WaitGate': qubitron.WaitGate,
        # The formatter keeps putting this back
        # pylint: disable=line-too-long
        'XEBPhasedFSimCharacterizationOptions': qubitron.experiments.XEBPhasedFSimCharacterizationOptions,
        # pylint: enable=line-too-long
        '_XEigenState': qubitron.value.product_state._XEigenState,
        'XPowGate': qubitron.XPowGate,
        'XXPowGate': qubitron.XXPowGate,
        '_YEigenState': qubitron.value.product_state._YEigenState,
        'YPowGate': qubitron.YPowGate,
        'YYPowGate': qubitron.YYPowGate,
        '_ZEigenState': qubitron.value.product_state._ZEigenState,
        'Zip': qubitron.Zip,
        'ZipLongest': qubitron.ZipLongest,
        'ZPowGate': qubitron.ZPowGate,
        'ZZPowGate': qubitron.ZZPowGate,
        'UniformSuperpositionGate': qubitron.UniformSuperpositionGate,
        # Old types, only supported for backwards-compatibility
        'BooleanHamiltonian': _boolean_hamiltonian_gate_op,  # Removed in v0.15
        'CrossEntropyResult': _cross_entropy_result,  # Removed in v0.16
        'CrossEntropyResultDict': _cross_entropy_result_dict,  # Removed in v0.16
        'IdentityOperation': _identity_operation_from_dict,
        'ParallelGateOperation': _parallel_gate_op,  # Removed in v0.14
        'SingleQubitMatrixGate': single_qubit_matrix_gate,
        'SymmetricalQidPair': _symmetricalqidpair,  # Removed in v0.15
        'TwoQubitMatrixGate': two_qubit_matrix_gate,
        'GlobalPhaseOperation': qubitron.global_phase_operation,  # Removed in v0.16
        # not a qubitron class, but treated as one:
        'pandas.DataFrame': pd.DataFrame,
        'pandas.Index': pd.Index,
        'pandas.MultiIndex': pd.MultiIndex.from_tuples,
        'sympy.Symbol': sympy.Symbol,
        'sympy.Add': lambda args: sympy.Add(*args),
        'sympy.Mul': lambda args: sympy.Mul(*args),
        'sympy.Pow': lambda args: sympy.Pow(*args),
        'sympy.GreaterThan': lambda args: sympy.GreaterThan(*args),
        'sympy.StrictGreaterThan': lambda args: sympy.StrictGreaterThan(*args),
        'sympy.LessThan': lambda args: sympy.LessThan(*args),
        'sympy.StrictLessThan': lambda args: sympy.StrictLessThan(*args),
        'sympy.Equality': lambda args: sympy.Equality(*args),
        'sympy.Unequality': lambda args: sympy.Unequality(*args),
        'sympy.And': lambda args: sympy.And(*args),
        'sympy.Or': lambda args: sympy.Or(*args),
        'sympy.Not': lambda args: sympy.Not(*args),
        'sympy.Xor': lambda args: sympy.Xor(*args),
        'sympy.Indexed': lambda args: sympy.Indexed(*args),
        'sympy.IndexedBase': lambda args: sympy.IndexedBase(*args),
        'sympy.Float': lambda approx: sympy.Float(approx),
        'sympy.Integer': sympy.Integer,
        'sympy.Rational': sympy.Rational,
        'sympy.pi': lambda: sympy.pi,
        'sympy.E': lambda: sympy.E,
        'sympy.EulerGamma': lambda: sympy.EulerGamma,
        'complex': complex,
        'datetime.datetime': _datetime,
    }
