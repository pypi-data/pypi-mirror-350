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
"""Gates (unitary and non-unitary), operations, base types, and gate sets."""

from qubitron.ops.arithmetic_operation import ArithmeticGate as ArithmeticGate

from qubitron.ops.clifford_gate import (
    CliffordGate as CliffordGate,
    CXSWAP as CXSWAP,
    CZSWAP as CZSWAP,
    SingleQubitCliffordGate as SingleQubitCliffordGate,
)

from qubitron.ops.dense_pauli_string import (
    BaseDensePauliString as BaseDensePauliString,
    DensePauliString as DensePauliString,
    MutableDensePauliString as MutableDensePauliString,
)

from qubitron.ops.boolean_hamiltonian import BooleanHamiltonianGate as BooleanHamiltonianGate

from qubitron.ops.common_channels import (
    amplitude_damp as amplitude_damp,
    AmplitudeDampingChannel as AmplitudeDampingChannel,
    asymmetric_depolarize as asymmetric_depolarize,
    AsymmetricDepolarizingChannel as AsymmetricDepolarizingChannel,
    bit_flip as bit_flip,
    BitFlipChannel as BitFlipChannel,
    depolarize as depolarize,
    DepolarizingChannel as DepolarizingChannel,
    generalized_amplitude_damp as generalized_amplitude_damp,
    GeneralizedAmplitudeDampingChannel as GeneralizedAmplitudeDampingChannel,
    phase_damp as phase_damp,
    phase_flip as phase_flip,
    PhaseDampingChannel as PhaseDampingChannel,
    PhaseFlipChannel as PhaseFlipChannel,
    R as R,
    reset as reset,
    reset_each as reset_each,
    ResetChannel as ResetChannel,
)

from qubitron.ops.common_gates import (
    CNOT as CNOT,
    CNotPowGate as CNotPowGate,
    cphase as cphase,
    CX as CX,
    CXPowGate as CXPowGate,
    CZ as CZ,
    CZPowGate as CZPowGate,
    H as H,
    HPowGate as HPowGate,
    Rx as Rx,
    Ry as Ry,
    Rz as Rz,
    rx as rx,
    ry as ry,
    rz as rz,
    S as S,
    T as T,
    XPowGate as XPowGate,
    YPowGate as YPowGate,
    ZPowGate as ZPowGate,
)

from qubitron.ops.common_gate_families import (
    AnyUnitaryGateFamily as AnyUnitaryGateFamily,
    AnyIntegerPowerGateFamily as AnyIntegerPowerGateFamily,
    ParallelGateFamily as ParallelGateFamily,
)

from qubitron.ops.classically_controlled_operation import (
    ClassicallyControlledOperation as ClassicallyControlledOperation,
)

from qubitron.ops.controlled_gate import ControlledGate as ControlledGate

from qubitron.ops.diagonal_gate import DiagonalGate as DiagonalGate

from qubitron.ops.eigen_gate import EigenGate as EigenGate

from qubitron.ops.fourier_transform import (
    PhaseGradientGate as PhaseGradientGate,
    qft as qft,
    QuantumFourierTransformGate as QuantumFourierTransformGate,
)

from qubitron.ops.fsim_gate import FSimGate as FSimGate, PhasedFSimGate as PhasedFSimGate

from qubitron.ops.gate_features import InterchangeableQubitsGate as InterchangeableQubitsGate

from qubitron.ops.gate_operation import GateOperation as GateOperation

from qubitron.ops.gateset import GateFamily as GateFamily, Gateset as Gateset

from qubitron.ops.identity import I as I, identity_each as identity_each, IdentityGate as IdentityGate

from qubitron.ops.global_phase_op import (
    GlobalPhaseGate as GlobalPhaseGate,
    global_phase_operation as global_phase_operation,
)

from qubitron.ops.kraus_channel import KrausChannel as KrausChannel

from qubitron.ops.linear_combinations import (
    LinearCombinationOfGates as LinearCombinationOfGates,
    LinearCombinationOfOperations as LinearCombinationOfOperations,
    PauliSum as PauliSum,
    PauliSumLike as PauliSumLike,
    ProjectorSum as ProjectorSum,
)

from qubitron.ops.mixed_unitary_channel import MixedUnitaryChannel as MixedUnitaryChannel

from qubitron.ops.pauli_sum_exponential import PauliSumExponential as PauliSumExponential

from qubitron.ops.pauli_measurement_gate import PauliMeasurementGate as PauliMeasurementGate

from qubitron.ops.parallel_gate import (
    ParallelGate as ParallelGate,
    parallel_gate_op as parallel_gate_op,
)

from qubitron.ops.projector import ProjectorString as ProjectorString

from qubitron.ops.controlled_operation import ControlledOperation as ControlledOperation

from qubitron.ops.qubit_manager import (
    BorrowableQubit as BorrowableQubit,
    CleanQubit as CleanQubit,
    QubitManager as QubitManager,
    SimpleQubitManager as SimpleQubitManager,
)

from qubitron.ops.greedy_qubit_manager import GreedyQubitManager as GreedyQubitManager

from qubitron.ops.qubit_order import QubitOrder as QubitOrder

from qubitron.ops.qubit_order_or_list import QubitOrderOrList as QubitOrderOrList

from qubitron.ops.matrix_gates import MatrixGate as MatrixGate

from qubitron.ops.measure_util import (
    M as M,
    measure as measure,
    measure_each as measure_each,
    measure_paulistring_terms as measure_paulistring_terms,
    measure_single_paulistring as measure_single_paulistring,
)

from qubitron.ops.measurement_gate import MeasurementGate as MeasurementGate

from qubitron.ops.named_qubit import NamedQubit as NamedQubit, NamedQid as NamedQid

from qubitron.ops.op_tree import (
    flatten_op_tree as flatten_op_tree,
    freeze_op_tree as freeze_op_tree,
    flatten_to_ops as flatten_to_ops,
    flatten_to_ops_or_moments as flatten_to_ops_or_moments,
    OP_TREE as OP_TREE,
    transform_op_tree as transform_op_tree,
)

from qubitron.ops.parity_gates import (
    XX as XX,
    XXPowGate as XXPowGate,
    YY as YY,
    YYPowGate as YYPowGate,
    ZZ as ZZ,
    ZZPowGate as ZZPowGate,
    MSGate as MSGate,
    ms as ms,
)

from qubitron.ops.pauli_gates import Pauli as Pauli, X as X, Y as Y, Z as Z

from qubitron.ops.pauli_interaction_gate import PauliInteractionGate as PauliInteractionGate

from qubitron.ops.pauli_string import (
    MutablePauliString as MutablePauliString,
    PAULI_GATE_LIKE as PAULI_GATE_LIKE,
    PAULI_STRING_LIKE as PAULI_STRING_LIKE,
    PauliString as PauliString,
    SingleQubitPauliStringGateOperation as SingleQubitPauliStringGateOperation,
)

from qubitron.ops.pauli_string_phasor import (
    PauliStringPhasor as PauliStringPhasor,
    PauliStringPhasorGate as PauliStringPhasorGate,
)

from qubitron.ops.pauli_string_raw_types import PauliStringGateOperation as PauliStringGateOperation

from qubitron.ops.permutation_gate import QubitPermutationGate as QubitPermutationGate

from qubitron.ops.phased_iswap_gate import givens as givens, PhasedISwapPowGate as PhasedISwapPowGate

from qubitron.ops.phased_x_gate import PhasedXPowGate as PhasedXPowGate

from qubitron.ops.phased_x_z_gate import PhasedXZGate as PhasedXZGate

from qubitron.ops.qid_util import q as q

from qubitron.ops.random_gate_channel import RandomGateChannel as RandomGateChannel

from qubitron.ops.raw_types import (
    Gate as Gate,
    Operation as Operation,
    Qid as Qid,
    TaggedOperation as TaggedOperation,
)

from qubitron.ops.swap_gates import (
    ISWAP as ISWAP,
    ISwapPowGate as ISwapPowGate,
    ISWAP_INV as ISWAP_INV,
    riswap as riswap,
    SQRT_ISWAP as SQRT_ISWAP,
    SQRT_ISWAP_INV as SQRT_ISWAP_INV,
    SWAP as SWAP,
    SwapPowGate as SwapPowGate,
)

from qubitron.ops.tags import RoutingSwapTag as RoutingSwapTag, VirtualTag as VirtualTag

from qubitron.ops.three_qubit_gates import (
    CCNOT as CCNOT,
    CCNotPowGate as CCNotPowGate,
    CCX as CCX,
    CCXPowGate as CCXPowGate,
    CCZ as CCZ,
    CCZPowGate as CCZPowGate,
    CSWAP as CSWAP,
    CSwapGate as CSwapGate,
    FREDKIN as FREDKIN,
    ThreeQubitDiagonalGate as ThreeQubitDiagonalGate,
    TOFFOLI as TOFFOLI,
)

from qubitron.ops.two_qubit_diagonal_gate import TwoQubitDiagonalGate as TwoQubitDiagonalGate

from qubitron.ops.wait_gate import wait as wait, WaitGate as WaitGate

from qubitron.ops.state_preparation_channel import StatePreparationChannel as StatePreparationChannel

from qubitron.ops.control_values import (
    AbstractControlValues as AbstractControlValues,
    ProductOfSums as ProductOfSums,
    SumOfProducts as SumOfProducts,
)

from qubitron.ops.uniform_superposition_gate import UniformSuperpositionGate as UniformSuperpositionGate
