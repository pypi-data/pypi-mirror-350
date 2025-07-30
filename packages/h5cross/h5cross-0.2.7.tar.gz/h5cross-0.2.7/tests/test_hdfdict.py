import os
import datetime


import pytest
import numpy as np
import h5py

from h5cross import hdfdict


def equaldt(a, b):
    d = a - b
    return d.total_seconds() < 1e-3


@pytest.mark.parametrize("lazy", [True, False])
def test_dict_to_hdf(tmpdir, lazy):

    test_dict = {
        "a": np.random.randn(10),
        "b": [1, 2, 3],
        "c": "Hallo",  # TODO: check how to go to string automatically
        "d": np.array(["a", "b"]).astype("S"),
        "e": True,
        "f": (True, False),
        "g": [datetime.datetime.now() for i in range(5)],
        "h": datetime.datetime.utcnow(),
        # "i": [("Hello", 5), (6, "No HDF but json"), {"foo": True}],
        # "j": {"test2": datetime.datetime.now(), "again": ["a", 1], (1, 2): (3, 4)},
    }

    # dump
    filename = os.path.join(tmpdir, "example.h5")
    with h5py.File(filename, "w") as h5file:
        hdfdict.dump(test_dict, h5file)

    # load
    h5file = h5py.File(filename, "r")
    res = hdfdict.load(h5file, lazy=lazy)

    assert tuple(test_dict.keys()) == tuple(res.keys())
    np.testing.assert_allclose(test_dict["a"], res["a"])
    np.testing.assert_array_equal(test_dict["b"], res["b"])
    assert test_dict["c"] == res["c"].decode("utf-8")
    np.testing.assert_array_equal(test_dict["d"], res["d"])
    np.testing.assert_array_equal(test_dict["e"], res["e"])
    np.testing.assert_array_equal(test_dict["f"], res["f"])

    for a, b in zip(test_dict["g"], res["g"]):
        assert equaldt(a, b)

    assert equaldt(test_dict["h"], res["h"])

    # assert test_dict["i"][0][0] == "Hello"
    # assert test_dict["i"][1][0] == 6

    # assert isinstance(test_dict["j"]["test2"], datetime.datetime)
    # assert test_dict["j"]["again"][0] == "a"
    # assert res["j"]["again"][1] == 1

    if lazy:
        res.unlazy()  # all lazy objects will be rolled out.

    h5file.close()
