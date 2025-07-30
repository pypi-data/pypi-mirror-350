# Copyright 2022 The Qubitron Developers
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


def test_init_sum_of_products_raises():
    # data shouldn't be empty.
    with pytest.raises(ValueError):
        _ = qubitron.SumOfProducts([])

    # size mismatch
    with pytest.raises(ValueError):
        _ = qubitron.SumOfProducts([[1], [1, 0]])


def test_init_product_of_sums():
    eq = qubitron.testing.EqualsTester()
    # 0. Trivial case of 1 control and 1 qubit.
    eq.add_equality_group(qubitron.ProductOfSums([1]), qubitron.ProductOfSums(((1,),)))
    eq.add_equality_group(qubitron.ProductOfSums([0]), qubitron.ProductOfSums(((0,),)))
    # 1. Multiple controls for 1 qubit.
    #   - The number of different "terms" in this case is just 1; since each term corresponds
    #     to a specific qubit.
    eq.add_equality_group(qubitron.ProductOfSums([[0, 1, 2]]), qubitron.ProductOfSums(((0, 1, 2),)))
    # 2. Multiple qubits, each with 1 control.
    #   - Duplicates within qubit control values are ignored.
    #   - Supports initialization by Sequence[int] and Sequence[Collection[int]].
    #   - Duplicates and Permutation across qubit control value groups leads to different objects.
    eq.add_equality_group(
        qubitron.ProductOfSums([0, 1, 2]),
        qubitron.ProductOfSums([[0, 0], [1, 1], [2, 2]]),
        qubitron.ProductOfSums([[0], [1], [2]]),
    )
    eq.add_equality_group([0, 0, 1, 1, 2, 2])
    eq.add_equality_group([2, 0, 1])
    # 3. Multiple controls and multiple qubits.
    #   - Permutations within qubit control value groups leads to same objects.
    eq.add_equality_group(
        qubitron.ProductOfSums([(0, 1), (1, 2)]),
        qubitron.ProductOfSums([(1, 0), (2, 1)]),
        qubitron.ProductOfSums([[0, 1], (2, 1)]),
    )
    eq.add_equality_group([(1, 2), (0, 1)])


def test_init_sum_of_products():
    eq = qubitron.testing.EqualsTester()
    # 0. Trivial case of 1 control and 1 qubit
    eq.add_equality_group(qubitron.SumOfProducts([[1]]), qubitron.SumOfProducts(((1,),)))
    eq.add_equality_group(qubitron.SumOfProducts([[0]]), qubitron.SumOfProducts(((0,),)))
    # 1. Multiple controls for 1 qubit.
    #   - Duplicates and Permutation across different terms is ignored.
    eq.add_equality_group(
        qubitron.SumOfProducts([[0], [1], [2]], name="custom name"),
        qubitron.SumOfProducts([[0], [1], [2]], name="name does not matter"),
        qubitron.SumOfProducts([[2], [0], [1]]),
        qubitron.SumOfProducts([[0], [0], [2], [2], [1], [1]]),
    )
    # 2. Multiple qubits, each with 1 control.
    #   - The number of different "terms" in this case is just 1; since each term corresponds
    #     to a valid control combination.
    #   - Duplicates and Permutations within a term are not ignored, since they correspond to
    #     different control configuration.
    eq.add_equality_group(qubitron.SumOfProducts([[0, 1, 2]]), qubitron.SumOfProducts([(0, 1, 2)]))
    eq.add_equality_group(qubitron.SumOfProducts([[1, 0, 2]]))
    eq.add_equality_group(qubitron.SumOfProducts([(0, 2, 1)]))
    eq.add_equality_group(qubitron.SumOfProducts([[0, 0, 1, 1, 2, 2]]))
    # 3. Multiple qubits, multiple controls.
    eq.add_equality_group(
        qubitron.SumOfProducts([(0, 1), (0, 2), (1, 1), (1, 2)]),
        qubitron.SumOfProducts([(1, 2), (0, 2), (0, 1), (1, 1)]),
        qubitron.SumOfProducts([(1, 2), (1, 2), (0, 2), (0, 2), (1, 1), (0, 1)]),
    )
    eq.add_equality_group(qubitron.SumOfProducts([(1, 0), (2, 0), (1, 1), (2, 1)]))


def test_equality_across_types():
    eq = qubitron.testing.EqualsTester()
    # Trivial case of 1 control and 1 qubit
    eq.add_equality_group(
        qubitron.SumOfProducts([[1]]),
        qubitron.ProductOfSums([1]),
        qubitron.SumOfProducts(((1,),)),
        qubitron.ProductOfSums(((1,),)),
    )
    # Note that instances of `AbstractControlValues` will not compare equal to corresponding
    # expanded tuples used in their internal representation (i.e. `tuple(control_values)`).
    eq.add_equality_group(((1,),), tuple(qubitron.ProductOfSums([1])), tuple(qubitron.SumOfProducts([[1]])))
    # Multiple controls for 1 qubit.
    eq.add_equality_group(qubitron.SumOfProducts([[0], [1], [2]]), qubitron.ProductOfSums([[0, 1, 2]]))
    # Multiple qubits, each with 1 control
    eq.add_equality_group(qubitron.ProductOfSums([0, 1, 2]), qubitron.SumOfProducts([[0, 1, 2]]))
    # Expanded tuples of unequal `SumOfProducts` and `ProductOfSums` can be equal.
    eq.add_equality_group(
        ((0,), (1,), (2,)),
        tuple(qubitron.SumOfProducts([[0], [1], [2]])),
        tuple(qubitron.ProductOfSums([0, 1, 2])),
    )
    eq.add_equality_group(
        ((0, 1, 2),), tuple(qubitron.ProductOfSums([[0, 1, 2]])), tuple(qubitron.SumOfProducts([[0, 1, 2]]))
    )
    # Multiple qubits, multiple controls.
    eq.add_equality_group(
        qubitron.ProductOfSums([(0, 1), (1, 2), 1]),
        qubitron.SumOfProducts([(0, 1, 1), (0, 2, 1), (1, 1, 1), (1, 2, 1)]),
    )
    eq.add_equality_group(qubitron.SumOfProducts([(0, 1), (1, 0)]))  # xor control
    eq.add_equality_group(qubitron.ProductOfSums([(0, 1), (1, 0)]))  # or control


def test_and_operation():
    eq = qubitron.testing.EqualsTester()

    eq.add_equality_group(
        qubitron.ProductOfSums([0]) & qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([0]) & qubitron.SumOfProducts([[1]]),
        qubitron.SumOfProducts([[0]]) & qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([0, 1]),
        qubitron.SumOfProducts([[0, 1]]),
    )
    eq.add_equality_group(
        qubitron.ProductOfSums([1]) & qubitron.SumOfProducts([[0]]), qubitron.ProductOfSums([1, 0])
    )

    eq.add_equality_group(
        qubitron.ProductOfSums([[0, 1]]) & qubitron.ProductOfSums([1]),
        qubitron.SumOfProducts([[0], [1]]) & qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([[0, 1], [1]]),
        qubitron.SumOfProducts([[0, 1], [1, 1]]),
    )

    eq.add_equality_group(
        qubitron.ProductOfSums([0, 1]) & qubitron.ProductOfSums([0]),
        qubitron.ProductOfSums([0]) & qubitron.ProductOfSums([1, 0]),
    )

    eq.add_equality_group(
        qubitron.SumOfProducts([(0, 0), (1, 1)]) & qubitron.ProductOfSums([0, 1]),
        qubitron.SumOfProducts([(0, 0), (1, 1)]) & qubitron.ProductOfSums([0]) & qubitron.ProductOfSums([1]),
        qubitron.SumOfProducts([(0, 0, 0, 1), (1, 1, 0, 1)]),
    )

    eq.add_equality_group(
        qubitron.SumOfProducts([(0, 1), (1, 0)]) & qubitron.SumOfProducts([(0, 0), (0, 1), (1, 0)]),
        qubitron.SumOfProducts(
            [(0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0)]
        ),
    )


@pytest.mark.parametrize(
    'cv1, cv2, expected_type',
    [
        [qubitron.ProductOfSums([0, 1]), qubitron.ProductOfSums([0]), qubitron.ProductOfSums],
        [qubitron.SumOfProducts([(0, 0), (1, 1)]), qubitron.ProductOfSums([0, 1, 2]), qubitron.SumOfProducts],
    ],
)
def test_and_operation_adds_qubits(cv1, cv2, expected_type):
    assert isinstance(cv1 & cv2, expected_type)
    assert qubitron.num_qubits(cv1 & cv2) == qubitron.num_qubits(cv1) + qubitron.num_qubits(cv2)


def test_or_operation():
    eq = qubitron.testing.EqualsTester()

    eq.add_equality_group(
        qubitron.ProductOfSums([0]) | qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([1]) | qubitron.SumOfProducts([[0]]),
        qubitron.SumOfProducts([[0]]) | qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([[0, 1]]),
        qubitron.SumOfProducts([[1], [0]]),
    )

    eq.add_equality_group(
        qubitron.ProductOfSums([[0, 1]]) | qubitron.ProductOfSums([2]),
        qubitron.SumOfProducts([[0], [2]]) | qubitron.ProductOfSums([1]),
        qubitron.ProductOfSums([[0, 1, 2]]),
        qubitron.SumOfProducts([[0], [1], [2]]),
    )

    eq.add_equality_group(
        qubitron.ProductOfSums([0, 1]) | qubitron.SumOfProducts([[0, 0], [1, 1]]),
        qubitron.SumOfProducts([[0, 0], [1, 1]]) | qubitron.ProductOfSums([0, 1]),
        qubitron.SumOfProducts([[0, 0], [1, 1], [0, 1]]),
    )


@pytest.mark.parametrize(
    'cv1,cv2,expected_type',
    [
        [qubitron.ProductOfSums([0, 1, 2]), qubitron.ProductOfSums([2, 0, 1]), qubitron.ProductOfSums],
        [
            qubitron.SumOfProducts([[0, 0, 0], [1, 1, 1]]),
            qubitron.SumOfProducts([[0, 1, 0], [1, 0, 1]]),
            qubitron.SumOfProducts,
        ],
        [qubitron.ProductOfSums([0, 1]), qubitron.ProductOfSums([1]), None],
        [qubitron.SumOfProducts([[0], [1], [2]]), qubitron.SumOfProducts([[1, 0]]), None],
    ],
)
def test_or_operation_acts_on_same_qubits(cv1, cv2, expected_type):
    if qubitron.num_qubits(cv1) == qubitron.num_qubits(cv2):
        assert qubitron.num_qubits(cv1 | cv2) == qubitron.num_qubits(cv1)
        assert expected_type is not None
        assert isinstance(cv1 | cv2, expected_type)
    else:
        assert expected_type is None
        with pytest.raises(ValueError, match="must act on equal number of qubits"):
            _ = cv1 | cv2


@pytest.mark.parametrize('data', [((1,),), ((0, 1), (1,)), [(0, 1), (1, 0)]])
def test_product_of_sums_repr(data):
    qubitron.testing.assert_equivalent_repr(qubitron.ProductOfSums(data))


@pytest.mark.parametrize('data', [((1,),), ((0, 1),), ((0, 0), (0, 1), (1, 0))])
def test_sum_of_products_repr(data):
    qubitron.testing.assert_equivalent_repr(qubitron.SumOfProducts(data))
    qubitron.testing.assert_equivalent_repr(qubitron.SumOfProducts(data, name="CustomName"))


def test_sum_of_products_validate():
    control_val = qubitron.SumOfProducts(((1, 2), (0, 1)))

    _ = control_val.validate([2, 3])

    with pytest.raises(ValueError):
        _ = control_val.validate([2, 2])

    # number of qubits != number of control values.
    with pytest.raises(ValueError):
        _ = control_val.validate([2])


@pytest.mark.parametrize('data', [((1,),), ((0, 1),), ((0, 0), (0, 1), (1, 0))])
def test_sum_of_products_num_qubits(data):
    assert qubitron.num_qubits(qubitron.SumOfProducts(data)) == len(data[0])


@pytest.mark.parametrize(
    'data, is_trivial',
    [
        [((1,),), True],
        [((0, 1),), False],
        [((0, 0), (0, 1), (1, 0)), False],
        [((1, 1, 1, 1),), True],
    ],
)
def test_sum_of_products_is_trivial(data, is_trivial):
    assert qubitron.SumOfProducts(data).is_trivial == is_trivial


@pytest.mark.parametrize(
    'data, is_trivial',
    [[((1,),), True], [((0, 1),), False], [([2], [1], [2]), False], [([1], [1], [1], [1]), True]],
)
def test_product_of_sum_is_trivial(data, is_trivial):
    assert qubitron.ProductOfSums(data).is_trivial == is_trivial


def test_product_of_sums_str():
    c = qubitron.ProductOfSums([(0, 1), 1, 0, (0, 2)])
    assert str(c) == 'C01C1C0C02'


def test_sum_of_products_str():
    c = qubitron.SumOfProducts(((1, 0), (0, 1)))
    assert str(c) == 'C_01_10'

    c = qubitron.SumOfProducts(((1, 0), (0, 1)), name="xor")
    assert str(c) == 'C_xor'


def test_control_values_diagrams():
    q = qubitron.LineQubit.range(3)
    ccx = qubitron.X(q[0]).controlled_by(*q[1:])
    ccx_sop = qubitron.X(q[0]).controlled_by(*q[1:], control_values=qubitron.SumOfProducts([[1, 1]]))
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(ccx, ccx_sop),
        """
0: ───X───X───
      │   │
1: ───@───@───
      │   │
2: ───@───@───
""",
    )
    c0c1x = qubitron.X(q[0]).controlled_by(*q[1:], control_values=[0, 1])
    c0c1x_sop = qubitron.X(q[0]).controlled_by(*q[1:], control_values=qubitron.SumOfProducts([[0, 1]]))
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(c0c1x, c0c1x_sop),
        """
0: ───X─────X─────
      │     │
1: ───(0)───(0)───
      │     │
2: ───@─────@─────
""",
    )

    c01c2x = qubitron.X(q[0]).controlled_by(*q[1:], control_values=[[0, 1], 1])
    c01c2x_sop = qubitron.X(q[0]).controlled_by(
        *q[1:], control_values=qubitron.SumOfProducts([[0, 1], [1, 1]])
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(c01c2x, c01c2x_sop),
        """
0: ───X───────X───────
      │       │
1: ───(0,1)───@(01)───
      │       │
2: ───@───────@(11)───
""",
    )

    xor_sop = qubitron.X(q[0]).controlled_by(
        *q[1:], control_values=qubitron.SumOfProducts([[0, 1], [1, 0]])
    )
    xor_named_sop = qubitron.X(q[0]).controlled_by(
        *q[1:], control_values=qubitron.SumOfProducts([[0, 1], [1, 0]], name="xor")
    )
    qubitron.testing.assert_has_diagram(
        qubitron.Circuit(xor_sop, xor_named_sop),
        """
0: ───X───────X────────
      │       │
1: ───@(01)───@────────
      │       │
2: ───@(10)───@(xor)───
        """,
    )
