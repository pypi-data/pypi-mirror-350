

from h5cross.utils import _group_keys



# TODO: complete tests


def test_group_keys():
    keys = ['a/b/c', 'a/b/d', 'a/e', 'f/g', 'h']

    grouped_keys = _group_keys(keys, sep='/')

    target_results = {'a': {'b': {'c': 'a/b/c', 'd': 'a/b/d'}, 'e': 'a/e'},
                      'f': {'g': 'f/g'}, 'h': 'h'}
    assert grouped_keys['a']['b']['c'] == target_results['a']['b']['c']
    assert grouped_keys['a']['b']['d'] == target_results['a']['b']['d']
    assert grouped_keys['f']['g'] == target_results['f']['g']
    assert grouped_keys['h'] == target_results['h']

    # ensure order (root)
    target_keys = ['a', 'f', 'h']
    for key, target_key in zip(grouped_keys, target_keys):
        assert key == target_key

    # ensure order (nested)
    target_keys = ['b', 'e']
    for key, target_key in zip(grouped_keys['a'], target_keys):
        assert key == target_key
