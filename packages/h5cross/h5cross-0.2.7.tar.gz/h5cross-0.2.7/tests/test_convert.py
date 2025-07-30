
import os
import pytest
from h5cross.convert import convert


@pytest.mark.skip("External file dependent test. To change...")
def test_nek5000(meshes_dir):
    filename = os.path.join(meshes_dir, 'nek5000', 'channel3D_0.f00001')

    data_dict = convert(filename, file_format='nek5000')

    expected_keys = {'xmesh', 'ymesh', 'zmesh', 'ux', 'uy', 'uz', 'pressure',
                     'Parameters'}
    for key in data_dict:
        assert key in expected_keys


@pytest.mark.skip("External file dependent test. To change...")
def test_vtk(meshes_dir):
    filename = os.path.join(meshes_dir, 'vtk', 'triangle_mesh_linear.vtk')

    data_dict = convert(filename, file_format='vtk')

    expected_keys = {'pressure', 'velocity', 'Mesh'}
    for key in data_dict:
        assert key in expected_keys


@pytest.mark.skip("External file dependent test. To change...")
def test_vtu(meshes_dir):
    filename = os.path.join(meshes_dir, 'vtu', 'triangle_mesh_linear.vtu')

    data_dict = convert(filename, file_format='vtu')

    expected_keys = {'pressure', 'velocity', 'Mesh'}
    for key in data_dict:
        assert key in expected_keys


@pytest.mark.skip("External file dependent test. To change...")
def test_pvtu(meshes_dir):
    filename = os.path.join(meshes_dir, 'pvtu', 'example_pvtu.pvtu')

    data_dict = convert(filename, file_format='pvtu')

    expected_keys = {'node_value', 'simerr_type', 'Mesh'}
    for key in data_dict:
        assert key in expected_keys
