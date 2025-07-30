

import os

import yaml


from h5cross.io import write_dict_to_yaml
from h5cross.io import write_h5
from h5cross.io import load_hdf_as_dict


TEST_DICT = {'a': 1,
             'b': {'c': 1.2,
                   'd': 'a string'},
             'e': None}


def _assert_dict(result_dict):
    assert result_dict['a'] == TEST_DICT['a']
    assert result_dict['b']['c'] == TEST_DICT['b']['c']

    val = result_dict['b']['d']
    if type(val) is not str:
        assert val.decode('utf-8') == TEST_DICT['b']['d']
    else:
        assert val == TEST_DICT['b']['d']
    assert result_dict['e'] == TEST_DICT['e']


def test_write_load_dict_yaml(tmpdir):

    filename = os.path.join(tmpdir, 'example')

    write_dict_to_yaml(TEST_DICT, filename)

    # load file back
    with open(f'{filename}.yml', 'r', encoding='utf-8') as file:
        data_dict = yaml.load(file, Loader=yaml.SafeLoader)

    _assert_dict(data_dict)


def test_write_load_hdf(tmpdir):

    filename = os.path.join(tmpdir, 'example')
    write_h5(TEST_DICT, filename)

    data_dict = load_hdf_as_dict(f'{filename}.h5')
    _assert_dict(data_dict)
