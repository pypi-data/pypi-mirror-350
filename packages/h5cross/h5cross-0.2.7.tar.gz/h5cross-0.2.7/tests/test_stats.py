
import pytest

import numpy as np

from h5cross.stats import compute_dict_stats
from h5cross.prettytable import get_stats_table

from .data import TEST_DICT


ATOL = 1e-6


def test_stats():

    skip_list = ['pressure', 'O2 mass fraction']
    stats = compute_dict_stats(TEST_DICT, skip_list=skip_list)

    target_stats = {'min': 0.08493008, 'max': 0.93432919, 'mean': 0.532405342,
                    'median': 0.57242786, 'std': 0.2690518441418391}

    # ensure statistics are well computed
    h2_stats = stats['Extra']['H2 mass fraction']
    for key, target_value in target_stats.items():
        assert abs(target_value - getattr(h2_stats, key)) < ATOL

    # ensure skip list works
    assert 'pressure' not in stats
    assert stats['Extra'].get('Extra', None) is None


@pytest.mark.parametrize('full_path', [True, False])
def test_stats_table(full_path):

    stats_dict = compute_dict_stats(TEST_DICT)

    stats_table = get_stats_table(stats_dict, full_path=full_path)

    rows = stats_table._rows
    row_names = [row[0] for row in rows]
    target_row_names = ['Extra/H2 mass fraction', 'Extra/Extra/O2 mass fraction',
                        'pressure']

    assert len(rows) == 3
    assert len(rows[0]) == 6
    for row_name, target_row_name in zip(row_names, target_row_names):
        if full_path:
            assert row_name == target_row_name
        else:
            assert row_name == target_row_name.split('/')[-1]


def test_stats_array_type():

    array = np.array(['1', '2'])
    out = compute_dict_stats({'string': array})

    assert out == {}
