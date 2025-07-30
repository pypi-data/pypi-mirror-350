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

import abc
import numbers
from types import NotImplementedType
from typing import (
    AbstractSet,
    Any,
    Callable,
    cast,
    Iterable,
    Iterator,
    overload,
    Sequence,
    TYPE_CHECKING,
)

import numpy as np
import sympy
from typing_extensions import Self

from qubitron import linalg, protocols, value
from qubitron._compat import proper_repr
from qubitron.ops import global_phase_op, identity, pauli_gates, pauli_string, raw_types

if TYPE_CHECKING:
    import qubitron

# Order is important! Index equals numeric value.
PAULI_CHARS = 'IXYZ'
PAULI_GATES: list[qubitron.Pauli | qubitron.IdentityGate] = [
    identity.I,
    pauli_gates.X,
    pauli_gates.Y,
    pauli_gates.Z,
]


@value.value_equality(approximate=True, distinct_child_types=True)
class BaseDensePauliString(raw_types.Gate, metaclass=abc.ABCMeta):
    """Parent class for `qubitron.DensePauliString` and `qubitron.MutableDensePauliString`.

    `qubitron.BaseDensePauliString` is an abstract base class, which is used to implement
    `qubitron.DensePauliString` and `qubitron.MutableDensePauliString`. The non-mutable version
    is used as the corresponding gate for `qubitron.PauliString` operation and the mutable
    version is mainly used for efficiently manipulating dense pauli strings.

    See the docstrings of `qubitron.DensePauliString` and `qubitron.MutableDensePauliString` for more
    details.

    Examples:
    >>> print(qubitron.DensePauliString('XXIY'))
    +XXIY

    >>> print(qubitron.MutableDensePauliString('IZII', coefficient=-1))
    -IZII (mutable)

    >>> print(qubitron.DensePauliString([0, 1, 2, 3],
    ...                             coefficient=sympy.Symbol('t')))
    t*IXYZ
    """

    I_VAL = 0
    X_VAL = 1
    Y_VAL = 2
    Z_VAL = 3

    def __init__(
        self,
        pauli_mask: Iterable[qubitron.PAULI_GATE_LIKE] | np.ndarray,
        *,
        coefficient: qubitron.TParamValComplex = 1,
    ):
        """Initializes a new dense pauli string.

        Args:
            pauli_mask: A specification of the Pauli gates to use. This argument
                can be a string like "IXYYZ", or a numeric list like
                [0, 1, 3, 2] with I=0, X=1, Y=2, Z=3=X|Y.

                The internal representation is a 1-dimensional uint8 numpy array
                containing numeric values. If such a numpy array is given, and
                the pauli string is mutable, the argument will be used directly
                instead of being copied.
            coefficient: A complex number. Usually +1, -1, 1j, or -1j but other
                values are supported.
        """
        self._pauli_mask = _as_pauli_mask(pauli_mask)
        self._coefficient: complex | sympy.Expr = (
            coefficient if isinstance(coefficient, sympy.Expr) else complex(coefficient)
        )
        if type(self) != MutableDensePauliString:
            self._pauli_mask = np.copy(self.pauli_mask)
            self._pauli_mask.flags.writeable = False

    @property
    def pauli_mask(self) -> np.ndarray:
        """A 1-dimensional uint8 numpy array giving a specification of Pauli gates to use."""
        return self._pauli_mask

    @property
    def coefficient(self) -> qubitron.TParamValComplex:
        """A complex coefficient or symbol."""
        return self._coefficient

    def _json_dict_(self) -> dict[str, Any]:
        return protocols.obj_to_dict_helper(self, ['pauli_mask', 'coefficient'])

    def _value_equality_values_(self):
        # Note: can't use pauli_mask directly.
        # Would cause approx_eq to false positive when atol > 1.
        return self.coefficient, tuple(PAULI_CHARS[p] for p in self.pauli_mask)

    @classmethod
    def one_hot(cls, *, index: int, length: int, pauli: qubitron.PAULI_GATE_LIKE) -> Self:
        """Creates a dense pauli string with only one non-identity Pauli.

        Args:
            index: The index of the Pauli that is not an identity.
            length: The total length of the string to create.
            pauli: The pauli gate to put at the hot index. Can be set to either
                a string ('X', 'Y', 'Z', 'I'), a qubitron gate (`qubitron.X`,
                `qubitron.Y`, `qubitron.Z`, or `qubitron.I`), or an integer (0=I, 1=X, 2=Y,
                3=Z).
        """
        mask = np.zeros(length, dtype=np.uint8)
        mask[index] = _pauli_index(pauli)
        concrete_cls = cast(Callable, DensePauliString if cls is BaseDensePauliString else cls)
        return concrete_cls(pauli_mask=mask)

    @classmethod
    def eye(cls, length: int) -> Self:
        """Creates a dense pauli string containing only identity gates.

        Args:
            length: The length of the dense pauli string.
        """
        concrete_cls = cast(Callable, DensePauliString if cls is BaseDensePauliString else cls)
        return concrete_cls(pauli_mask=np.zeros(length, dtype=np.uint8))

    def _num_qubits_(self) -> int:
        return len(self)

    def _has_unitary_(self) -> bool:
        if self._is_parameterized_():
            return False
        return abs(1 - abs(cast(complex, self.coefficient))) < 1e-8

    def _unitary_(self) -> np.ndarray | NotImplementedType:
        if not self._has_unitary_():
            return NotImplemented
        return self.coefficient * linalg.kron(
            *[protocols.unitary(PAULI_GATES[p]) for p in self.pauli_mask]
        )

    def _apply_unitary_(self, args) -> np.ndarray | None | NotImplementedType:
        if not self._has_unitary_():
            return NotImplemented
        from qubitron import devices

        qubits = devices.LineQubit.range(len(self))
        decomposed_ops = cast(Iterable['qubitron.OP_TREE'], self._decompose_(qubits))
        return protocols.apply_unitaries(decomposed_ops, qubits, args)

    def _decompose_(self, qubits: Sequence[qubitron.Qid]) -> NotImplementedType | qubitron.OP_TREE:
        if not self._has_unitary_():
            return NotImplemented
        result = [PAULI_GATES[p].on(q) for p, q in zip(self.pauli_mask, qubits) if p]
        if self.coefficient != 1:
            result.append(global_phase_op.global_phase_operation(self.coefficient))
        return result

    def _is_parameterized_(self) -> bool:
        return protocols.is_parameterized(self.coefficient)

    def _parameter_names_(self) -> AbstractSet[str]:
        return protocols.parameter_names(self.coefficient)

    def _resolve_parameters_(self, resolver: qubitron.ParamResolver, recursive: bool) -> Self:
        return self.copy(
            coefficient=protocols.resolve_parameters(self.coefficient, resolver, recursive)
        )

    def __pos__(self):
        return self

    def __pow__(self, power: float) -> NotImplementedType | Self:
        concrete_class = type(self)
        if isinstance(power, int):
            i_group = [1, +1j, -1, -1j]
            coef = (
                i_group[i_group.index(cast(complex, self.coefficient)) * power % 4]
                if self.coefficient in i_group
                else self.coefficient**power
            )
            if power % 2 == 0:
                return concrete_class.eye(len(self)).__mul__(coef)
            return concrete_class(coefficient=coef, pauli_mask=self.pauli_mask)
        return NotImplemented

    @overload
    def __getitem__(self, item: int) -> qubitron.Pauli | qubitron.IdentityGate:
        pass

    @overload
    def __getitem__(self, item: slice) -> Self:
        pass

    def __getitem__(self, item):
        if isinstance(item, int):
            return PAULI_GATES[self.pauli_mask[item]]

        if isinstance(item, slice):
            return type(self)(coefficient=1, pauli_mask=self.pauli_mask[item])

        raise TypeError(f'indices must be integers or slices, not {type(item)}')

    def __iter__(self) -> Iterator[qubitron.Pauli | qubitron.IdentityGate]:
        for i in range(len(self)):
            yield self[i]

    def __len__(self) -> int:
        return len(self.pauli_mask)

    def __neg__(self):
        return type(self)(coefficient=-self.coefficient, pauli_mask=self.pauli_mask)

    def __truediv__(self, other):
        if isinstance(other, (sympy.Basic, numbers.Number)):
            return self.__mul__(1 / other)

        return NotImplemented

    def __mul__(self, other):
        concrete_class = type(self)
        if isinstance(other, BaseDensePauliString):
            if isinstance(other, MutableDensePauliString):
                concrete_class = MutableDensePauliString
            max_len = max(len(self.pauli_mask), len(other.pauli_mask))
            min_len = min(len(self.pauli_mask), len(other.pauli_mask))
            new_mask = np.zeros(max_len, dtype=np.uint8)
            new_mask[: len(self.pauli_mask)] ^= self.pauli_mask
            new_mask[: len(other.pauli_mask)] ^= other.pauli_mask
            tweak = _vectorized_pauli_mul_phase(
                self.pauli_mask[:min_len], other.pauli_mask[:min_len]
            )
            return concrete_class(
                pauli_mask=new_mask, coefficient=self.coefficient * other.coefficient * tweak
            )

        if isinstance(other, (sympy.Basic, numbers.Number)):
            new_coef = protocols.mul(self.coefficient, other, default=None)
            if new_coef is None:
                return NotImplemented
            return concrete_class(pauli_mask=self.pauli_mask, coefficient=new_coef)

        split = _attempt_value_to_pauli_index(other)
        if split is not None:
            p, i = split
            mask = np.copy(self.pauli_mask)
            mask[i] ^= p
            return concrete_class(
                pauli_mask=mask,
                coefficient=self.coefficient * _vectorized_pauli_mul_phase(self.pauli_mask[i], p),
            )

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (sympy.Basic, numbers.Number)):
            return self.__mul__(other)

        split = _attempt_value_to_pauli_index(other)
        if split is not None:
            p, i = split
            mask = np.copy(self.pauli_mask)
            mask[i] ^= p
            return type(self)(
                pauli_mask=mask,
                coefficient=self.coefficient * _vectorized_pauli_mul_phase(p, self.pauli_mask[i]),
            )

        return NotImplemented

    def tensor_product(self, other: BaseDensePauliString) -> Self:
        """Concatenates dense pauli strings and multiplies their coefficients.

        Args:
            other: The dense pauli string to place after the end of this one.

        Returns:
            A dense pauli string with the concatenation of the paulis from the
            two input pauli strings, and the product of their coefficients.
        """
        return type(self)(
            coefficient=self.coefficient * other.coefficient,
            pauli_mask=np.concatenate([self.pauli_mask, other.pauli_mask]),
        )

    def __abs__(self) -> Self:
        coef = self.coefficient
        return type(self)(
            coefficient=sympy.Abs(coef) if isinstance(coef, sympy.Expr) else abs(coef),
            pauli_mask=self.pauli_mask,
        )

    def on(self, *qubits: qubitron.Qid) -> qubitron.PauliString:
        return self.sparse(qubits)

    def sparse(self, qubits: Sequence[qubitron.Qid] | None = None) -> qubitron.PauliString:
        """A `qubitron.PauliString` version of this dense pauli string.

        Args:
            qubits: The qubits to apply the Paulis to. Defaults to
                `qubitron.LineQubit.range(len(self))`.

        Returns:
            A `qubitron.PauliString` with the non-identity operations from
            this dense pauli string applied to appropriate qubits.

        Raises:
            ValueError: If the number of qubits supplied does not match that of
                this instance.
        """
        if qubits is None:
            from qubitron import devices

            qubits = devices.LineQubit.range(len(self))

        if len(qubits) != len(self):
            raise ValueError('Wrong number of qubits.')

        return pauli_string.PauliString(
            coefficient=self.coefficient,
            qubit_pauli_map={q: PAULI_GATES[p] for q, p in zip(qubits, self.pauli_mask) if p},
        )

    def __str__(self) -> str:
        if self.coefficient == 1:
            coef = '+'
        elif self.coefficient == -1:
            coef = '-'
        elif isinstance(self.coefficient, (numbers.Complex, sympy.Symbol)):
            coef = f'{self.coefficient}*'
        else:
            coef = f'({self.coefficient})*'
        mask = ''.join(PAULI_CHARS[p] for p in self.pauli_mask)
        return coef + mask

    def __repr__(self) -> str:
        paulis = ''.join(PAULI_CHARS[p] for p in self.pauli_mask)
        return (
            f'qubitron.{type(self).__name__}({repr(paulis)}, '
            f'coefficient={proper_repr(self.coefficient)})'
        )

    def _commutes_(self, other: Any, *, atol: float = 1e-8) -> bool | NotImplementedType | None:
        if isinstance(other, BaseDensePauliString):
            n = min(len(self.pauli_mask), len(other.pauli_mask))
            phase = _vectorized_pauli_mul_phase(self.pauli_mask[:n], other.pauli_mask[:n])
            return phase == 1 or phase == -1

        # Single qubit Pauli operation.
        split = _attempt_value_to_pauli_index(other)
        if split is not None:
            p1, i = split
            p2 = self.pauli_mask[i]
            return (p1 or p2) == (p2 or p1)

        return NotImplemented

    def frozen(self) -> DensePauliString:
        """A `qubitron.DensePauliString` with the same contents."""
        return DensePauliString(coefficient=self.coefficient, pauli_mask=self.pauli_mask)

    def mutable_copy(self) -> MutableDensePauliString:
        """A `qubitron.MutableDensePauliString` with the same contents."""
        return MutableDensePauliString(
            coefficient=self.coefficient, pauli_mask=np.copy(self.pauli_mask)
        )

    @abc.abstractmethod
    def copy(
        self,
        coefficient: qubitron.TParamValComplex | None = None,
        pauli_mask: None | str | Iterable[int] | np.ndarray = None,
    ) -> Self:
        """Returns a copy with possibly modified contents.

        Args:
            coefficient: The new coefficient value. If not specified, defaults
                to the current `coefficient` value.
            pauli_mask: The new `pauli_mask` value. If not specified, defaults
                to the current pauli mask value.

        Returns:
            A copied instance.
        """


class DensePauliString(BaseDensePauliString):
    """An immutable string of Paulis, like `XIXY`, with a coefficient.

    A `DensePauliString` represents a multi-qubit pauli operator, i.e. a tensor product of single
    qubits Pauli gates (including the `qubitron.IdentityGate`), each of which would act on a
    different qubit. When applied on qubits, a `DensePauliString` results in `qubitron.PauliString`
    as an operation.

    Note that `qubitron.PauliString` only stores a tensor product of non-identity `qubitron.Pauli`
    operations whereas `qubitron.DensePauliString` also supports storing the `qubitron.IdentityGate`.

    For example,

    >>> dps = qubitron.DensePauliString('XXIY')
    >>> print(dps) # 4 qubit pauli operator with 'X' on first 2 qubits, 'I' on 3rd and 'Y' on 4th.
    +XXIY
    >>> ps = dps.on(*qubitron.LineQubit.range(4)) # When applied on qubits, we get a `qubitron.PauliString`.
    >>> print(ps) # Note that `qubitron.PauliString` only preserves non-identity operations.
    X(q(0))*X(q(1))*Y(q(3))

    This can optionally take a coefficient, for example:

    >>> dps = qubitron.DensePauliString("XX", coefficient=3)
    >>> print(dps) # Represents 3 times the operator XX acting on two qubits.
    (3+0j)*XX
    >>> print(dps.on(*qubitron.LineQubit.range(2))) # Coefficient is propagated to `qubitron.PauliString`.
    (3+0j)*X(q(0))*X(q(1))

    If the coefficient has magnitude of 1, the resulting operator is a unitary and thus is
    also a `qubitron.Gate`.

    Note that `DensePauliString` is an immutable object. If you need a mutable version of
    dense pauli strings, see `qubitron.MutableDensePauliString`.
    """

    def frozen(self) -> DensePauliString:
        return self

    def copy(
        self,
        coefficient: qubitron.TParamValComplex | None = None,
        pauli_mask: None | str | Iterable[int] | np.ndarray = None,
    ) -> DensePauliString:
        if pauli_mask is None and (coefficient is None or coefficient == self.coefficient):
            return self
        return DensePauliString(
            coefficient=self.coefficient if coefficient is None else coefficient,
            pauli_mask=self.pauli_mask if pauli_mask is None else pauli_mask,
        )


@value.value_equality(unhashable=True, approximate=True)
class MutableDensePauliString(BaseDensePauliString):
    """A mutable string of Paulis, like `XIXY`, with a coefficient.

    `qubitron.MutableDensePauliString` is a mutable version of `qubitron.DensePauliString`.
    It exists mainly to help mutate dense pauli strings efficiently, instead of always creating
    a copy, and then converting back to a frozen `qubitron.DensePauliString` representation.

    For example:

    >>> mutable_dps = qubitron.MutableDensePauliString('XXZZ')
    >>> mutable_dps[:2] = 'YY' # `qubitron.MutableDensePauliString` supports item assignment.
    >>> print(mutable_dps)
    +YYZZ (mutable)

    See docstrings of `qubitron.DensePauliString` for more details on dense pauli strings.
    """

    @overload
    def __setitem__(self, key: int, value: qubitron.PAULI_GATE_LIKE) -> Self:
        pass

    @overload
    def __setitem__(
        self, key: slice, value: Iterable[qubitron.PAULI_GATE_LIKE] | np.ndarray | BaseDensePauliString
    ) -> Self:
        pass

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.pauli_mask[key] = _pauli_index(value)
            return self

        if isinstance(key, slice):
            if isinstance(value, BaseDensePauliString):
                if value.coefficient != 1:
                    raise ValueError(
                        "Can't slice-assign from a PauliProduct whose "
                        "coefficient is not 1.\n"
                        "\nWorkaround: If you just want to ignore the "
                        "coefficient, do `= value[:]` instead of `= value`."
                    )
                self.pauli_mask[key] = value.pauli_mask
            else:
                self.pauli_mask[key] = _as_pauli_mask(value)
            return self

        raise TypeError(f'indices must be integers or slices, not {type(key)}')

    def __itruediv__(self, other):
        if isinstance(other, (sympy.Basic, numbers.Number)):
            return self.__imul__(1 / other)
        return NotImplemented

    def __imul__(self, other):
        if isinstance(other, BaseDensePauliString):
            if len(other) > len(self):
                raise ValueError(
                    "The receiving dense pauli string is smaller than "
                    "the dense pauli string being multiplied into it.\n"
                    f"self={repr(self)}\n"
                    f"other={repr(other)}"
                )
            self_mask = self.pauli_mask[: len(other.pauli_mask)]
            self._coefficient *= _vectorized_pauli_mul_phase(self_mask, other.pauli_mask)
            self._coefficient *= other.coefficient
            self_mask ^= other.pauli_mask
            return self

        if isinstance(other, (sympy.Basic, numbers.Number)):
            new_coef = protocols.mul(self.coefficient, other, default=None)
            if new_coef is None:
                return NotImplemented
            self._coefficient = new_coef if isinstance(new_coef, sympy.Basic) else complex(new_coef)
            return self

        split = _attempt_value_to_pauli_index(other)
        if split is not None:
            p, i = split
            self._coefficient *= _vectorized_pauli_mul_phase(self.pauli_mask[i], p)
            self.pauli_mask[i] ^= p
            return self

        return NotImplemented

    def copy(
        self,
        coefficient: qubitron.TParamValComplex | None = None,
        pauli_mask: None | str | Iterable[int] | np.ndarray = None,
    ) -> MutableDensePauliString:
        return MutableDensePauliString(
            coefficient=self.coefficient if coefficient is None else coefficient,
            pauli_mask=np.copy(self.pauli_mask) if pauli_mask is None else pauli_mask,
        )

    def __str__(self) -> str:
        return super().__str__() + ' (mutable)'

    def _value_equality_values_(self):
        return self.coefficient, tuple(PAULI_CHARS[p] for p in self.pauli_mask)

    @classmethod
    def inline_gaussian_elimination(cls, rows: list[MutableDensePauliString]) -> None:
        if not rows:
            return

        height = len(rows)
        width = len(rows[0])
        next_row = 0

        for col in range(width):
            for held in [DensePauliString.Z_VAL, DensePauliString.X_VAL]:
                # Locate pivot row.
                for k in range(next_row, height):
                    if (rows[k].pauli_mask[col] or held) != held:
                        pivot_row = k
                        break
                else:
                    continue

                # Eliminate column entry in other rows.
                for k in range(height):
                    if k != pivot_row:
                        if (rows[k].pauli_mask[col] or held) != held:
                            rows[k].__imul__(rows[pivot_row])

                # Keep it sorted.
                if pivot_row != next_row:
                    rows[next_row], rows[pivot_row] = (rows[pivot_row], rows[next_row])

                next_row += 1


def _pauli_index(val: qubitron.PAULI_GATE_LIKE) -> int:
    m = pauli_string.PAULI_GATE_LIKE_TO_INDEX_MAP
    if val not in m:
        raise TypeError(
            f'Expected a qubitron.PAULI_GATE_LIKE (any of qubitron.I qubitron.X, qubitron.Y, '
            f'qubitron.Z, "I", "X", "Y", "Z", "i", "x", "y", "z", 0, 1, 2, 3) but '
            f'got {repr(val)}.'
        )
    return m[val]


def _as_pauli_mask(val: Iterable[qubitron.PAULI_GATE_LIKE] | np.ndarray) -> np.ndarray:
    if isinstance(val, np.ndarray):
        return np.asarray(val, dtype=np.uint8)
    return np.array([_pauli_index(v) for v in val], dtype=np.uint8)


def _attempt_value_to_pauli_index(v: qubitron.Operation) -> tuple[int, int] | None:
    if not isinstance(v, raw_types.Operation):
        return None

    if not isinstance(v.gate, pauli_gates.Pauli):
        return None  # pragma: no cover

    q = v.qubits[0]
    from qubitron import devices

    if not isinstance(q, devices.LineQubit):
        raise ValueError(
            'Got a Pauli operation, but it was applied to a qubit type '
            'other than `qubitron.LineQubit` so its dense index is ambiguous.\n'
            f'v={repr(v)}.'
        )
    return pauli_string.PAULI_GATE_LIKE_TO_INDEX_MAP[v.gate], q.x


def _vectorized_pauli_mul_phase(lhs: int | np.ndarray, rhs: int | np.ndarray) -> complex:
    """Computes the leading coefficient of a pauli string multiplication.

    The two inputs must have the same length. They must follow the convention
    that I=0, X=1, Z=2, Y=3 and have no out-of-range values.

    Args:
        lhs: Left hand side `pauli_mask` from `DensePauliString`.
        rhs: Right hand side `pauli_mask` from `DensePauliString`.

    Returns:
        1, 1j, -1, or -1j.
    """

    # Vectorized computation of per-term phase exponents.
    t = np.array(rhs, dtype=np.int8)
    t *= lhs != 0
    t -= lhs * (rhs != 0)
    t += 1
    t %= 3
    t -= 1

    # Result is i raised to the sum of the per-term phase exponents.
    s = int(np.sum(t, dtype=np.uint8).item() & 3)
    return 1j**s
