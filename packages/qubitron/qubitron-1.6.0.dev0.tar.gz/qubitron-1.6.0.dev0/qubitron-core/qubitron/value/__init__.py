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

"""Value conversion utilities and classes for time and quantum states."""
from qubitron.value.abc_alt import (
    ABCMetaImplementAnyOneOf as ABCMetaImplementAnyOneOf,
    alternative as alternative,
)

from qubitron.value.angle import (
    canonicalize_half_turns as canonicalize_half_turns,
    chosen_angle_to_canonical_half_turns as chosen_angle_to_canonical_half_turns,
    chosen_angle_to_half_turns as chosen_angle_to_half_turns,
)

from qubitron.value.classical_data import (
    ClassicalDataDictionaryStore as ClassicalDataDictionaryStore,
    ClassicalDataStore as ClassicalDataStore,
    ClassicalDataStoreReader as ClassicalDataStoreReader,
    MeasurementType as MeasurementType,
)

from qubitron.value.condition import (
    Condition as Condition,
    KeyCondition as KeyCondition,
    SympyCondition as SympyCondition,
    BitMaskKeyCondition as BitMaskKeyCondition,
)

from qubitron.value.digits import (
    big_endian_bits_to_int as big_endian_bits_to_int,
    big_endian_digits_to_int as big_endian_digits_to_int,
    big_endian_int_to_bits as big_endian_int_to_bits,
    big_endian_int_to_digits as big_endian_int_to_digits,
)

from qubitron.value.duration import Duration as Duration, DURATION_LIKE as DURATION_LIKE

from qubitron.value.linear_dict import LinearDict as LinearDict, Scalar as Scalar

from qubitron.value.measurement_key import (
    MEASUREMENT_KEY_SEPARATOR as MEASUREMENT_KEY_SEPARATOR,
    MeasurementKey as MeasurementKey,
)

from qubitron.value.probability import (
    state_vector_to_probabilities as state_vector_to_probabilities,
    validate_probability as validate_probability,
)

from qubitron.value.product_state import (
    ProductState as ProductState,
    KET_PLUS as KET_PLUS,
    KET_MINUS as KET_MINUS,
    KET_IMAG as KET_IMAG,
    KET_MINUS_IMAG as KET_MINUS_IMAG,
    KET_ZERO as KET_ZERO,
    KET_ONE as KET_ONE,
    PAULI_STATES as PAULI_STATES,
)

from qubitron.value.periodic_value import PeriodicValue as PeriodicValue

from qubitron.value.random_state import (
    parse_random_state as parse_random_state,
    RANDOM_STATE_OR_SEED_LIKE as RANDOM_STATE_OR_SEED_LIKE,
)

from qubitron.value.timestamp import Timestamp as Timestamp

from qubitron.value.type_alias import (
    TParamKey as TParamKey,
    TParamVal as TParamVal,
    TParamValComplex as TParamValComplex,
)

from qubitron.value.value_equality_attr import value_equality as value_equality
