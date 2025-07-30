
import os

import pytest

from h5cross.visit_h5 import get_h5_structure
from h5cross.visit_h5 import _ascii2string
from h5cross.io import write_h5
from h5cross.utils import unwrap_dict

from .data import TEST_DICT


def _create_example_h5(tmpdir, as_dict=False):
    filename = os.path.join(tmpdir, 'example')
    write_h5(TEST_DICT, filename)
    return get_h5_structure(f'{filename}.h5', as_dict=as_dict)


def test_ascii2string():
    word = "testing/"
    ascii_list = []
    for letter in word:
        ascii_list.append(ord(letter))

    assert word[:-1] == _ascii2string(ascii_list)


def test_get_structure(tmpdir):

    h5_struct_unwrapped = unwrap_dict(_create_example_h5(tmpdir, as_dict=False))

    # check keys
    target_struct_keys = ['Extra/H2 mass fraction', 'Extra/Extra/O2 mass fraction', 'pressure']

    for key in target_struct_keys:
        assert key in h5_struct_unwrapped


@pytest.mark.parametrize('as_dict', [False, True])
def test_get_structure_field(tmpdir, as_dict):
    # TODO: test non float
    h5_struct = _create_example_h5(tmpdir, as_dict=as_dict)

    # on root
    pressure_field = h5_struct['pressure']
    target_value = {'dtype': 'float64', 'value': 'array of 16 elements'}
    for key, target_value_ in target_value.items():
        if as_dict:
            assert pressure_field[key] == target_value_
        else:
            assert getattr(pressure_field, key) == target_value_

    # test one nested
    h2_field = h5_struct['Extra']['H2 mass fraction']
    target_value = {'dtype': 'float64', 'value': 'array of 20 elements'}
    for key, target_value_ in target_value.items():
        if as_dict:
            assert h2_field[key] == target_value_
        else:
            assert getattr(h2_field, key) == target_value_
