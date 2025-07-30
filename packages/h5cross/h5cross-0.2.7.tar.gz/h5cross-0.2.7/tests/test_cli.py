
import os

from click.testing import CliRunner
import pytest


from h5cross import cli


@pytest.mark.parametrize('filenames', [['file1.h5', 'file2.h5'],
                                       ['file1.h5', 'file3.h5']])
@pytest.mark.parametrize('add_stats', [[], ['--add-stats']])
def test_compare_h5(datadir, filenames, add_stats):
    # just checks cli does not fail
    filenames = [os.path.join(datadir, filename) for filename in filenames]

    runner = CliRunner()
    result = runner.invoke(cli.diff, [*filenames, *add_stats, '--test'])

    assert result.exit_code == 0


def test_visual_h5(datadir):
    filename = os.path.join(datadir, 'file1.h5')

    runner = CliRunner()
    result = runner.invoke(cli.view, [filename, '--test'])

    assert result.exit_code == 0


@pytest.mark.parametrize('filenames', [['file1.h5', 'file2.h5'],
                                       ['file1.h5', 'file3.h5']])
@pytest.mark.parametrize('select_vars', [['--select-vars', 'temperature'],
                                         ['--select-vars', 'temperature,pressure']])
@pytest.mark.parametrize('use_seaborn', [['--use-seaborn'], []])
@pytest.mark.parametrize('add_xy', [['--add-xy'], []])
def test_compare_scatter_h5(datadir, tmpdir, filenames, select_vars, use_seaborn,
                            add_xy):
    filename = os.path.join(tmpdir, 'plot')

    filenames = [os.path.join(datadir, filename) for filename in filenames]

    runner = CliRunner()
    result = runner.invoke(cli.scatter,
                           [*filenames, *select_vars, *use_seaborn,
                            *add_xy, '--test', '--save-name', filename])

    assert result.exit_code == 0

    file_exists = False
    for cmp_filename in os.listdir(tmpdir):
        if cmp_filename.startswith('plot'):
            file_exists = True
            break

    assert file_exists is True
