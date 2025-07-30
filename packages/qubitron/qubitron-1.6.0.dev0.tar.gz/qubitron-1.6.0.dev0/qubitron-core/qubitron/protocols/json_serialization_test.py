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

import contextlib
import dataclasses
import datetime
import importlib
import io
import json
import os
import pathlib
import warnings
from unittest import mock

import attrs
import networkx as nx
import numpy as np
import pandas as pd
import pytest
import sympy

import qubitron
from qubitron._compat import proper_eq
from qubitron.protocols import json_serialization
from qubitron.testing.json import assert_json_roundtrip_works, ModuleJsonTestSpec, spec_for

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent.parent


@dataclasses.dataclass
class _ModuleDeprecation:
    old_name: str
    deprecation_assertion: contextlib.AbstractContextManager


# tested modules and their deprecation settings
TESTED_MODULES: dict[str, _ModuleDeprecation | None] = {
    'qubitron_aqt': None,
    'qubitron_ionq': None,
    'qubitron_google': None,
    'qubitron_pasqal': None,
    'qubitron_rigetti': None,
    'qubitron.protocols': None,
    'non_existent_should_be_fine': None,
}

# TODO(#6706) remove after qubitron_rigetti supports NumPy 2.0
if np.__version__.startswith("2."):  # pragma: no cover
    warnings.warn(
        "json_serialization_test - ignoring qubitron_rigetti due to incompatibility with NumPy 2.0"
    )
    del TESTED_MODULES["qubitron_rigetti"]


def _get_testspecs_for_modules() -> list[ModuleJsonTestSpec]:
    modules = []
    for m in TESTED_MODULES.keys():
        try:
            modules.append(spec_for(m))
        except ModuleNotFoundError:
            # for optional modules it is okay to skip
            pass
    return modules


MODULE_TEST_SPECS = _get_testspecs_for_modules()


def test_deprecated_qubitron_type_in_json_dict():
    class HasOldJsonDict:
        # Required for testing serialization of non-qubitron objects.
        __module__ = 'test.nonqubitron.namespace'

        def __eq__(self, other):
            return isinstance(other, HasOldJsonDict)  # pragma: no cover

        def _json_dict_(self):
            return {'qubitron_type': 'test.nonqubitron.namespace.HasOldJsonDict'}

        @classmethod
        def _from_json_dict_(cls, **kwargs):
            return cls()  # pragma: no cover

    with pytest.raises(ValueError, match='not a Qubitron type'):
        _ = qubitron.json_qubitron_type(HasOldJsonDict)

    def custom_resolver(name):
        if name == 'test.nonqubitron.namespace.HasOldJsonDict':  # pragma: no cover
            return HasOldJsonDict

    test_resolvers = [custom_resolver] + qubitron.DEFAULT_RESOLVERS
    with pytest.raises(ValueError, match="Found 'qubitron_type'"):
        assert_json_roundtrip_works(HasOldJsonDict(), resolvers=test_resolvers)


def test_line_qubit_roundtrip():
    q1 = qubitron.LineQubit(12)
    assert_json_roundtrip_works(
        q1,
        text_should_be="""{
  "qubitron_type": "LineQubit",
  "x": 12
}""",
    )


def test_gridqubit_roundtrip():
    q = qubitron.GridQubit(15, 18)
    assert_json_roundtrip_works(
        q,
        text_should_be="""{
  "qubitron_type": "GridQubit",
  "row": 15,
  "col": 18
}""",
    )


def test_op_roundtrip():
    q = qubitron.LineQubit(5)
    op1 = qubitron.rx(0.123).on(q)
    assert_json_roundtrip_works(
        op1,
        text_should_be="""{
  "qubitron_type": "GateOperation",
  "gate": {
    "qubitron_type": "Rx",
    "rads": 0.123
  },
  "qubits": [
    {
      "qubitron_type": "LineQubit",
      "x": 5
    }
  ]
}""",
    )


def test_op_roundtrip_filename(tmpdir):
    filename = f'{tmpdir}/op.json'
    q = qubitron.LineQubit(5)
    op1 = qubitron.rx(0.123).on(q)
    qubitron.to_json(op1, filename)
    assert os.path.exists(filename)
    op2 = qubitron.read_json(filename)
    assert op1 == op2

    gzip_filename = f'{tmpdir}/op.gz'
    qubitron.to_json_gzip(op1, gzip_filename)
    assert os.path.exists(gzip_filename)
    op3 = qubitron.read_json_gzip(gzip_filename)
    assert op1 == op3


def test_op_roundtrip_file_obj(tmpdir):
    filename = f'{tmpdir}/op.json'
    q = qubitron.LineQubit(5)
    op1 = qubitron.rx(0.123).on(q)
    with open(filename, 'w+') as file:
        qubitron.to_json(op1, file)
        assert os.path.exists(filename)
        file.seek(0)
        op2 = qubitron.read_json(file)
        assert op1 == op2

    gzip_filename = f'{tmpdir}/op.gz'
    with open(gzip_filename, 'w+b') as gzip_file:
        qubitron.to_json_gzip(op1, gzip_file)
        assert os.path.exists(gzip_filename)
        gzip_file.seek(0)
        op3 = qubitron.read_json_gzip(gzip_file)
        assert op1 == op3


def test_fail_to_resolve():
    buffer = io.StringIO()
    buffer.write(
        """
    {
      "qubitron_type": "MyCustomClass",
      "data": [1, 2, 3]
    }
    """
    )
    buffer.seek(0)

    with pytest.raises(ValueError) as e:
        qubitron.read_json(buffer)
    assert e.match("Could not resolve type 'MyCustomClass' during deserialization")


QUBITS = qubitron.LineQubit.range(5)
Q0, Q1, Q2, Q3, Q4 = QUBITS

### MODULE CONSISTENCY tests


@pytest.mark.parametrize('mod_spec', MODULE_TEST_SPECS, ids=repr)
# during test setup deprecated submodules are inspected and trigger the
# deprecation error in testing. It is cleaner to just turn it off than to assert
# deprecation for each submodule.
@mock.patch.dict(os.environ, clear='CIRQ_TESTING')
def test_shouldnt_be_serialized_no_superfluous(mod_spec: ModuleJsonTestSpec):
    # everything in the list should be ignored for a reason
    names = set(mod_spec.get_all_names())
    missing_names = set(mod_spec.should_not_be_serialized).difference(names)
    assert len(missing_names) == 0, (
        f"Defined as \"should't be serialized\", "
        f"but missing from {mod_spec}: \n"
        f"{missing_names}"
    )


@pytest.mark.parametrize('mod_spec', MODULE_TEST_SPECS, ids=repr)
# during test setup deprecated submodules are inspected and trigger the
# deprecation error in testing. It is cleaner to just turn it off than to assert
# deprecation for each submodule.
@mock.patch.dict(os.environ, clear='CIRQ_TESTING')
def test_not_yet_serializable_no_superfluous(mod_spec: ModuleJsonTestSpec):
    # everything in the list should be ignored for a reason
    names = set(mod_spec.get_all_names())
    missing_names = set(mod_spec.not_yet_serializable).difference(names)
    assert (
        len(missing_names) == 0
    ), f"Defined as Not yet serializable, but missing from {mod_spec}: \n{missing_names}"


@pytest.mark.parametrize('mod_spec', MODULE_TEST_SPECS, ids=repr)
def test_mutually_exclusive_not_serialize_lists(mod_spec: ModuleJsonTestSpec):
    common = set(mod_spec.should_not_be_serialized) & set(mod_spec.not_yet_serializable)
    assert len(common) == 0, (
        f"Defined in both {mod_spec.name} 'Not yet serializable' "
        f" and 'Should not be serialized' lists: {common}"
    )


@pytest.mark.parametrize('mod_spec', MODULE_TEST_SPECS, ids=repr)
def test_resolver_cache_vs_should_not_serialize(mod_spec: ModuleJsonTestSpec):
    resolver_cache_types = set([n for (n, _) in mod_spec.get_resolver_cache_types()])
    common = set(mod_spec.should_not_be_serialized) & resolver_cache_types

    assert len(common) == 0, (
        f"Defined in both {mod_spec.name} Resolver "
        f"Cache and should not be serialized:"
        f"{common}"
    )


@pytest.mark.parametrize('mod_spec', MODULE_TEST_SPECS, ids=repr)
def test_resolver_cache_vs_not_yet_serializable(mod_spec: ModuleJsonTestSpec):
    resolver_cache_types = set([n for (n, _) in mod_spec.get_resolver_cache_types()])
    common = set(mod_spec.not_yet_serializable) & resolver_cache_types

    assert len(common) == 0, (
        f"Issue with the JSON config of {mod_spec.name}.\n"
        f"Types are listed in both"
        f" {mod_spec.name}.json_resolver_cache.py and in the 'not_yet_serializable' list in"
        f" {mod_spec.test_data_path}/spec.py: "
        f"\n {common}"
    )


def test_builtins():
    assert_json_roundtrip_works(True)
    assert_json_roundtrip_works(1)
    assert_json_roundtrip_works(1 + 2j)
    assert_json_roundtrip_works({'test': [123, 5.5], 'key2': 'asdf', '3': None, '0.0': []})


def test_numpy():
    x = np.ones(1)[0]

    assert_json_roundtrip_works(np.bool_(True))
    assert_json_roundtrip_works(x.astype(np.int8))
    assert_json_roundtrip_works(x.astype(np.int16))
    assert_json_roundtrip_works(x.astype(np.int32))
    assert_json_roundtrip_works(x.astype(np.int64))
    assert_json_roundtrip_works(x.astype(np.uint8))
    assert_json_roundtrip_works(x.astype(np.uint16))
    assert_json_roundtrip_works(x.astype(np.uint32))
    assert_json_roundtrip_works(x.astype(np.uint64))
    assert_json_roundtrip_works(x.astype(np.float32))
    assert_json_roundtrip_works(x.astype(np.float64))
    assert_json_roundtrip_works(x.astype(np.complex64))
    assert_json_roundtrip_works(x.astype(np.complex128))

    assert_json_roundtrip_works(np.ones((11, 5)))
    assert_json_roundtrip_works(np.arange(3))


def test_pandas():
    assert_json_roundtrip_works(
        pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]], columns=['x', 'y', 'z'], index=[2, 5])
    )
    assert_json_roundtrip_works(pd.Index([1, 2, 3], name='test'))
    assert_json_roundtrip_works(
        pd.MultiIndex.from_tuples([(1, 2), (3, 4), (5, 6)], names=['alice', 'bob'])
    )

    assert_json_roundtrip_works(
        pd.DataFrame(
            index=pd.Index([1, 2, 3], name='test'),
            data=[[11, 21.0], [12, 22.0], [13, 23.0]],
            columns=['a', 'b'],
        )
    )
    assert_json_roundtrip_works(
        pd.DataFrame(
            index=pd.MultiIndex.from_tuples([(1, 2), (2, 3), (3, 4)], names=['x', 'y']),
            data=[[11, 21.0], [12, 22.0], [13, 23.0]],
            columns=pd.Index(['a', 'b'], name='c'),
        )
    )


def test_sympy():
    # Raw values.
    assert_json_roundtrip_works(sympy.Symbol('theta'))
    assert_json_roundtrip_works(sympy.Integer(5))
    assert_json_roundtrip_works(sympy.Rational(2, 3))
    assert_json_roundtrip_works(sympy.Float(1.1))

    # Basic operations.
    s = sympy.Symbol('s')
    t = sympy.Symbol('t')
    assert_json_roundtrip_works(t + s)
    assert_json_roundtrip_works(t * s)
    assert_json_roundtrip_works(t / s)
    assert_json_roundtrip_works(t - s)
    assert_json_roundtrip_works(t**s)

    # Linear combinations.
    assert_json_roundtrip_works(t * 2)
    assert_json_roundtrip_works(4 * t + 3 * s + 2)

    assert_json_roundtrip_works(sympy.pi)
    assert_json_roundtrip_works(sympy.E)
    assert_json_roundtrip_works(sympy.EulerGamma)


class SBKImpl(qubitron.SerializableByKey):
    """A test implementation of SerializableByKey."""

    def __init__(
        self,
        name: str,
        data_list: list | None = None,
        data_tuple: tuple | None = None,
        data_dict: dict | None = None,
    ):
        self.name = name
        self.data_list = data_list or []
        self.data_tuple = data_tuple or ()
        self.data_dict = data_dict or {}

    def __eq__(self, other):
        if not isinstance(other, SBKImpl):
            return False  # pragma: no cover
        return (
            self.name == other.name
            and self.data_list == other.data_list
            and self.data_tuple == other.data_tuple
            and self.data_dict == other.data_dict
        )

    def __hash__(self):
        return hash(
            (self.name, tuple(self.data_list), self.data_tuple, frozenset(self.data_dict.items()))
        )

    def _json_dict_(self):
        return {
            "name": self.name,
            "data_list": self.data_list,
            "data_tuple": self.data_tuple,
            "data_dict": self.data_dict,
        }

    @classmethod
    def _from_json_dict_(cls, name, data_list, data_tuple, data_dict, **kwargs):
        return cls(name, data_list, tuple(data_tuple), data_dict)


def test_serializable_by_key():
    def custom_resolver(name):
        if name == 'SBKImpl':
            return SBKImpl

    test_resolvers = [custom_resolver, *qubitron.DEFAULT_RESOLVERS]

    sbki_empty = SBKImpl('sbki_empty')
    assert_json_roundtrip_works(sbki_empty, resolvers=test_resolvers)

    sbki_list = SBKImpl('sbki_list', data_list=[sbki_empty, sbki_empty])
    assert_json_roundtrip_works(sbki_list, resolvers=test_resolvers)

    sbki_tuple = SBKImpl('sbki_tuple', data_tuple=(sbki_list, sbki_list))
    assert_json_roundtrip_works(sbki_tuple, resolvers=test_resolvers)

    sbki_dict = SBKImpl('sbki_dict', data_dict={'a': sbki_tuple, 'b': sbki_tuple})
    assert_json_roundtrip_works(sbki_dict, resolvers=test_resolvers)

    sbki_json = str(qubitron.to_json(sbki_dict))
    # There are 4 SBKImpl instances, one each for empty, list, tuple, dict.
    assert sbki_json.count('"qubitron_type": "VAL"') == 4
    # There are 3 SBKImpl refs, one each for empty, list, and tuple.
    assert sbki_json.count('"qubitron_type": "REF"') == 3

    list_sbki = [sbki_dict]
    assert_json_roundtrip_works(list_sbki, resolvers=test_resolvers)

    dict_sbki = {'a': sbki_dict}
    assert_json_roundtrip_works(dict_sbki, resolvers=test_resolvers)

    # Serialization keys have unique suffixes.
    sbki_other_list = SBKImpl('sbki_list', data_list=[sbki_list])
    assert_json_roundtrip_works(sbki_other_list, resolvers=test_resolvers)


# during test setup deprecated submodules are inspected and trigger the
# deprecation error in testing. It is cleaner to just turn it off than to assert
# deprecation for each submodule.
@mock.patch.dict(os.environ, clear='CIRQ_TESTING')
def _list_public_classes_for_tested_modules():
    # to remove DeprecationWarning noise during test collection
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return sorted(
            (
                (mod_spec, n, o)
                for mod_spec in MODULE_TEST_SPECS
                for (n, o) in mod_spec.find_classes_that_should_serialize()
            ),
            key=lambda mno: (str(mno[0]), mno[1]),
        )


@pytest.mark.parametrize('mod_spec,qubitron_obj_name,cls', _list_public_classes_for_tested_modules())
def test_json_test_data_coverage(mod_spec: ModuleJsonTestSpec, qubitron_obj_name: str, cls):
    if qubitron_obj_name in mod_spec.tested_elsewhere:
        pytest.skip("Tested elsewhere.")

    if qubitron_obj_name in mod_spec.not_yet_serializable:
        return pytest.xfail(reason="Not serializable (yet)")

    test_data_path = mod_spec.test_data_path
    rel_path = test_data_path.relative_to(REPO_ROOT)
    mod_path = mod_spec.name.replace(".", "/")
    rel_resolver_cache_path = f"{mod_path}/json_resolver_cache.py"
    json_path = test_data_path / f'{qubitron_obj_name}.json'
    json_path2 = test_data_path / f'{qubitron_obj_name}.json_inward'
    deprecation_deadline = mod_spec.deprecated.get(qubitron_obj_name)

    if not json_path.exists() and not json_path2.exists():  # pragma: no cover
        pytest.fail(
            f"Hello intrepid developer. There is a new public or "
            f"serializable object named '{qubitron_obj_name}' in the module '{mod_spec.name}' "
            f"that does not have associated test data.\n"
            f"\n"
            f"You must create the file\n"
            f"    {rel_path}/{qubitron_obj_name}.json\n"
            f"and the file\n"
            f"    {rel_path}/{qubitron_obj_name}.repr\n"
            f"in order to guarantee this public object is, and will "
            f"remain, serializable.\n"
            f"\n"
            f"The content of the .repr file should be the string returned "
            f"by `repr(obj)` where `obj` is a test {qubitron_obj_name} value "
            f"or list of such values. To get this to work you may need to "
            f"implement a __repr__ method for {qubitron_obj_name}. The repr "
            f"must be a parsable python expression that evaluates to "
            f"something equal to `obj`."
            f"\n"
            f"The content of the .json file should be the string returned "
            f"by `qubitron.to_json(obj)` where `obj` is the same object or "
            f"list of test objects.\n"
            f"To get this to work you likely need "
            f"to add {qubitron_obj_name} to the "
            f"`_class_resolver_dictionary` method in "
            f"the {rel_resolver_cache_path} source file. "
            f"You may also need to add a _json_dict_ method to "
            f"{qubitron_obj_name}. In some cases you will also need to add a "
            f"_from_json_dict_ class method to the {qubitron_obj_name} class."
            f"\n"
            f"For more information on JSON serialization, please read the "
            f"docstring for qubitron.protocols.SupportsJSON. If this object or "
            f"class is not appropriate for serialization, add its name to "
            f"the `should_not_be_serialized` list in the TestSpec defined in the "
            f"{rel_path}/spec.py source file."
        )

    repr_file = test_data_path / f'{qubitron_obj_name}.repr'
    if repr_file.exists() and cls is not None:
        objs = _eval_repr_data_file(repr_file, deprecation_deadline=deprecation_deadline)
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            assert type(obj) == cls, (
                f"Value in {test_data_path}/{qubitron_obj_name}.repr must be of "
                f"exact type {cls}, or a list of instances of that type. But "
                f"the value (or one of the list entries) had type "
                f"{type(obj)}.\n"
                f"\n"
                f"If using a value of the wrong type is intended, move the "
                f"value to {test_data_path}/{qubitron_obj_name}.repr_inward\n"
                f"\n"
                f"Value with wrong type:\n{obj!r}."
            )


@dataclasses.dataclass
class SerializableTypeObject:
    test_type: type

    def _json_dict_(self):
        return {'test_type': json_serialization.json_qubitron_type(self.test_type)}

    @classmethod
    def _from_json_dict_(cls, test_type, **kwargs):
        return cls(json_serialization.qubitron_type_from_json(test_type))


@pytest.mark.parametrize('mod_spec,qubitron_obj_name,cls', _list_public_classes_for_tested_modules())
def test_type_serialization(mod_spec: ModuleJsonTestSpec, qubitron_obj_name: str, cls):
    if qubitron_obj_name in mod_spec.tested_elsewhere:
        pytest.skip("Tested elsewhere.")

    if qubitron_obj_name in mod_spec.not_yet_serializable:
        return pytest.xfail(reason="Not serializable (yet)")

    if cls is None:
        pytest.skip(f'No serialization for None-mapped type: {qubitron_obj_name}')  # pragma: no cover

    try:
        typename = qubitron.json_qubitron_type(cls)
    except ValueError as e:
        pytest.skip(f'No serialization for non-Qubitron type: {str(e)}')

    def custom_resolver(name):
        if name == 'SerializableTypeObject':
            return SerializableTypeObject

    sto = SerializableTypeObject(cls)
    test_resolvers = [custom_resolver] + qubitron.DEFAULT_RESOLVERS
    expected_json = (
        f'{{\n  "qubitron_type": "SerializableTypeObject",\n' f'  "test_type": "{typename}"\n}}'
    )
    assert qubitron.to_json(sto) == expected_json
    assert qubitron.read_json(json_text=expected_json, resolvers=test_resolvers) == sto
    assert_json_roundtrip_works(sto, resolvers=test_resolvers)


def test_invalid_type_deserialize():
    def custom_resolver(name):
        if name == 'SerializableTypeObject':
            return SerializableTypeObject

    test_resolvers = [custom_resolver] + qubitron.DEFAULT_RESOLVERS
    invalid_json = '{\n  "qubitron_type": "SerializableTypeObject",\n  "test_type": "bad_type"\n}'
    with pytest.raises(ValueError, match='Could not resolve type'):
        _ = qubitron.read_json(json_text=invalid_json, resolvers=test_resolvers)

    factory_json = '{\n  "qubitron_type": "SerializableTypeObject",\n  "test_type": "sympy.Add"\n}'
    with pytest.raises(ValueError, match='maps to a factory method'):
        _ = qubitron.read_json(json_text=factory_json, resolvers=test_resolvers)


def test_to_from_strings():
    x_json_text = """{
  "qubitron_type": "_PauliX",
  "exponent": 1.0,
  "global_shift": 0.0
}"""
    assert qubitron.to_json(qubitron.X) == x_json_text
    assert qubitron.read_json(json_text=x_json_text) == qubitron.X

    with pytest.raises(ValueError, match='specify ONE'):
        qubitron.read_json(io.StringIO(), json_text=x_json_text)


def test_to_from_json_gzip():
    a, b = qubitron.LineQubit.range(2)
    test_circuit = qubitron.Circuit(qubitron.H(a), qubitron.CX(a, b))
    gzip_data = qubitron.to_json_gzip(test_circuit)
    unzip_circuit = qubitron.read_json_gzip(gzip_raw=gzip_data)
    assert test_circuit == unzip_circuit

    with pytest.raises(ValueError):
        _ = qubitron.read_json_gzip(io.StringIO(), gzip_raw=gzip_data)
    with pytest.raises(ValueError):
        _ = qubitron.read_json_gzip()


def _eval_repr_data_file(path: pathlib.Path, deprecation_deadline: str | None):
    content = path.read_text()
    ctx_managers: list[contextlib.AbstractContextManager] = [contextlib.suppress()]
    if deprecation_deadline:  # pragma: no cover
        # we ignore coverage here, because sometimes there are no deprecations at all in any of the
        # modules
        ctx_managers = [qubitron.testing.assert_deprecated(deadline=deprecation_deadline, count=None)]

    for deprecation in TESTED_MODULES.values():
        if deprecation is not None and deprecation.old_name in content:
            ctx_managers.append(deprecation.deprecation_assertion)  # pragma: no cover

    imports = {'qubitron': qubitron, 'pd': pd, 'sympy': sympy, 'np': np, 'datetime': datetime, 'nx': nx}

    for m in TESTED_MODULES.keys():
        try:
            imports[m] = importlib.import_module(m)
        except ImportError:
            pass

    with contextlib.ExitStack() as stack:
        for ctx_manager in ctx_managers:
            stack.enter_context(ctx_manager)
        obj = eval(content, imports, {})
        return obj


def assert_repr_and_json_test_data_agree(
    mod_spec: ModuleJsonTestSpec,
    repr_path: pathlib.Path,
    json_path: pathlib.Path,
    inward_only: bool,
    deprecation_deadline: str | None,
):
    if not repr_path.exists() and not json_path.exists():
        return

    rel_repr_path = f'{repr_path.relative_to(REPO_ROOT)}'
    rel_json_path = f'{json_path.relative_to(REPO_ROOT)}'

    try:
        json_from_file = json_path.read_text()
        ctx_manager = (
            qubitron.testing.assert_deprecated(deadline=deprecation_deadline, count=None)
            if deprecation_deadline
            else contextlib.suppress()
        )
        with ctx_manager:
            json_obj = qubitron.read_json(json_text=json_from_file)
    except ValueError as ex:  # pragma: no cover
        if "Could not resolve type" in str(ex):
            mod_path = mod_spec.name.replace(".", "/")
            rel_resolver_cache_path = f"{mod_path}/json_resolver_cache.py"
            pytest.fail(
                f"{rel_json_path} can't be parsed to JSON.\n"
                f"Maybe an entry is missing from the "
                f" `_class_resolver_dictionary` method in {rel_resolver_cache_path}?"
            )
        else:
            raise ValueError(f"deprecation: {deprecation_deadline} - got error: {ex}")
    except AssertionError as ex:  # pragma: no cover
        raise ex
    except Exception as ex:  # pragma: no cover
        raise IOError(f'Failed to parse test json data from {rel_json_path}.') from ex

    try:
        repr_obj = _eval_repr_data_file(repr_path, deprecation_deadline)
    except Exception as ex:  # pragma: no cover
        raise IOError(f'Failed to parse test repr data from {rel_repr_path}.') from ex

    assert proper_eq(json_obj, repr_obj), (
        f'The json data from {rel_json_path} did not parse '
        f'into an object equivalent to the repr data from {rel_repr_path}.\n'
        f'\n'
        f'json object: {json_obj!r}\n'
        f'repr object: {repr_obj!r}\n'
    )

    if not inward_only:
        json_from_qubitron = qubitron.to_json(repr_obj)
        json_from_qubitron_obj = json.loads(json_from_qubitron)
        json_from_file_obj = json.loads(json_from_file)

        assert json_from_qubitron_obj == json_from_file_obj, (
            f'The json produced by qubitron no longer agrees with the json in the '
            f'{rel_json_path} test data file.\n'
            f'\n'
            f'You must either fix the qubitron code to continue to produce the '
            f'same output, or you must move the old test data to '
            f'{rel_json_path}_inward and create a fresh {rel_json_path} file.\n'
            f'\n'
            f'test data json:\n'
            f'{json_from_file}\n'
            f'\n'
            f'qubitron produced json:\n'
            f'{json_from_qubitron}\n'
        )


@pytest.mark.parametrize(
    'mod_spec, abs_path',
    [(m, abs_path) for m in MODULE_TEST_SPECS for abs_path in m.all_test_data_keys()],
)
def test_json_and_repr_data(mod_spec: ModuleJsonTestSpec, abs_path: str):
    assert_repr_and_json_test_data_agree(
        mod_spec=mod_spec,
        repr_path=pathlib.Path(f'{abs_path}.repr'),
        json_path=pathlib.Path(f'{abs_path}.json'),
        inward_only=False,
        deprecation_deadline=mod_spec.deprecated.get(os.path.basename(abs_path)),
    )
    assert_repr_and_json_test_data_agree(
        mod_spec=mod_spec,
        repr_path=pathlib.Path(f'{abs_path}.repr_inward'),
        json_path=pathlib.Path(f'{abs_path}.json_inward'),
        inward_only=True,
        deprecation_deadline=mod_spec.deprecated.get(os.path.basename(abs_path)),
    )


def test_pathlib_paths(tmpdir):
    path = pathlib.Path(tmpdir) / 'op.json'
    qubitron.to_json(qubitron.X, path)
    assert qubitron.read_json(path) == qubitron.X

    gzip_path = pathlib.Path(tmpdir) / 'op.gz'
    qubitron.to_json_gzip(qubitron.X, gzip_path)
    assert qubitron.read_json_gzip(gzip_path) == qubitron.X


def test_dataclass_json_dict() -> None:
    @dataclasses.dataclass(frozen=True)
    class MyDC:
        q: qubitron.LineQubit
        desc: str

        def _json_dict_(self):
            return qubitron.dataclass_json_dict(self)

    def custom_resolver(name):
        if name == 'MyDC':
            return MyDC

    my_dc = MyDC(qubitron.LineQubit(4), 'hi mom')

    assert_json_roundtrip_works(my_dc, resolvers=[custom_resolver, *qubitron.DEFAULT_RESOLVERS])


def test_numpy_values():
    assert (
        qubitron.to_json({'value': np.array(1)})
        == """{
  "value": 1
}"""
    )


def test_basic_time_assertions():
    naive_dt = datetime.datetime.now()
    utc_dt = naive_dt.astimezone(datetime.timezone.utc)
    assert naive_dt.timestamp() == utc_dt.timestamp()

    re_utc = datetime.datetime.fromtimestamp(utc_dt.timestamp())
    re_naive = datetime.datetime.fromtimestamp(naive_dt.timestamp())

    assert re_utc == re_naive, 'roundtripping w/o tz turns to naive utc'
    assert re_utc != utc_dt, 'roundtripping loses tzinfo'
    assert naive_dt == re_naive, 'works, as long as you called fromtimestamp from the same timezone'


def test_datetime():
    naive_dt = datetime.datetime.now()

    re_naive_dt = qubitron.read_json(json_text=qubitron.to_json(naive_dt))
    assert re_naive_dt != naive_dt, 'loads in with timezone'
    assert re_naive_dt.timestamp() == naive_dt.timestamp()

    utc_dt = naive_dt.astimezone(datetime.timezone.utc)
    re_utc_dt = qubitron.read_json(json_text=qubitron.to_json(utc_dt))
    assert re_utc_dt == utc_dt
    assert re_utc_dt == re_naive_dt

    pst_dt = naive_dt.astimezone(tz=datetime.timezone(offset=datetime.timedelta(hours=-8)))
    re_pst_dt = qubitron.read_json(json_text=qubitron.to_json(pst_dt))
    assert re_pst_dt == pst_dt
    assert re_pst_dt == utc_dt
    assert re_pst_dt == re_naive_dt


@attrs.frozen
class _TestAttrsClas:
    name: str
    x: int


def test_attrs_json_dict():
    obj = _TestAttrsClas('test', x=123)
    js = json_serialization.attrs_json_dict(obj)
    assert js == {'name': 'test', 'x': 123}
