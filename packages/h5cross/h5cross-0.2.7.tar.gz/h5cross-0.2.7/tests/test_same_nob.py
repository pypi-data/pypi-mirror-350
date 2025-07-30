
import pytest
import numpy as np

from h5cross.same_nob import h5_same
from h5cross.same_nob import _same_nob


def test_same_nob():
    """ unit tests for base method"""
    ok_, log_o = _same_nob({"float": 1.5}, {"float": 1.5})
    dif, log_d = _same_nob({"float": 1}, {"float": 1.5})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"int": 1}, {"int": 1})
    dif, log_d = _same_nob({"int": 3}, {"int": 1})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"string": "string"}, {"string": "string"})
    dif, log_d = _same_nob({"string": "str"}, {"string": "string"})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"bytes": b"bytes"}, {"bytes": b"bytes"})
    dif, log_d = _same_nob({"bytes": "str"}, {"bytes": b"bytes"})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"bool": False}, {"bool": False})
    dif, log_d = _same_nob({"bool": True}, {"bool": False})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"complex": 1 + 5j}, {"complex": 1 + 5j})
    dif, log_d = _same_nob({"complex": 1}, {"complex": 1 + 5j})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"tuple": (1, 2, 3)}, {"tuple": (1, 2, 3)})
    dif, log_d = _same_nob({"tuple": (1, 5)}, {"tuple": (1, 2, 3)})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"list": [1, 2, 3]}, {"list": [1, 2, 3]})
    dif, log_d = _same_nob({"list": [0, 1]}, {"list": [1, 2, 3]})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"numpy": {"int32": np.int32(1)}}, {"numpy": {"int32": np.int32(1)}})
    dif, log_d = _same_nob({"numpy": {"int32": np.int32(3)}}, {"numpy": {"int32": np.int32(1)}})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"uint64": np.uint64(1)}, {"uint64": np.uint64(1)})
    dif, log_d = _same_nob({"uint64": np.uint64(3)}, {"uint64": np.uint64(1)})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"float": np.float_(1.5)}, {"float": np.float_(1.5)})
    dif, log_d = _same_nob({"float": np.float_(5)}, {"float": np.float_(1.5)})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"string": np.string_("string")}, {"string": np.string_("string")})
    dif, log_d = _same_nob({"string": np.string_("bool")}, {"string": np.string_("string")})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"bool": np.bool_(False)}, {"bool": np.bool_(False)})
    dif, log_d = _same_nob({"bool": np.bool_(True)}, {"bool": np.bool_(False)})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"bytes": np.bytes_("bytes")}, {"bytes": np.bytes_("bytes")})
    dif, log_d = _same_nob({"bytes": np.bytes_("bit")}, {"bytes": np.bytes_("bytes")})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"complex": np.complex_(1 + 5j)}, {"complex": np.complex_(1 + 5j)})
    dif, log_d = _same_nob({"complex": np.complex_(1 + 7j)}, {"complex": np.complex_(1 + 5j)})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"list": [np.int32(1), np.int32(2), np.int32(3)]}, {"list": [np.int32(1), np.int32(2), np.int32(3)]})
    dif, log_d = _same_nob({"list": [np.int32(1), np.uint64(2)]}, {"list": [np.int32(1), np.int32(2), np.int32(3)]})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"tuple": (np.int32(1), np.int32(2), np.int32(3))}, {"tuple": (np.int32(1), np.int32(2), np.int32(3))})
    dif, log_d = _same_nob({"tuple": (np.int32(1), np.int32(2), 5)}, {"tuple": (np.int32(1), np.int32(2), np.int32(3))})
    assert ok_, log_o
    assert not dif, log_d

    ok_, log_o = _same_nob({"ndarray": np.array([1, 2, 3])}, {"ndarray": np.array([1, 2, 3])})
    dif, log_d = _same_nob({"ndarray": np.array([1, 5, 3])}, {"ndarray": np.array([1, 2, 3])})
    assert ok_, log_o
    assert not dif, log_d

    dif, log_d = _same_nob({"ndarray": np.array([1, 3])}, {"ndarray": np.array([1, 2, 3])})
    assert not dif, log_d

    ok_, log_o = _same_nob({"2darray": np.array([[1, 2, 3], [1, 2, 3]])}, {"2darray": np.array([[1, 2, 3], [1, 2, 3]])})
    dif, log_d = _same_nob({"2darray": np.array([[1, 5, 3], [1, 5, 3]])}, {"2darray": np.array([[1, 2, 3], [1, 2, 3]])})
    assert ok_, log_o
    assert not dif, log_d

    class NotImpl():
        def __init__(self):
            self._not_understood = None

    NI = NotImpl()

    with pytest.raises(NotImplementedError):
        assert _same_nob({"notimpl": NI}, {"notimpl": NI})
        assert _same_nob({"notinlist": [NI, NI]}, {"notinlist": [NI, NI]})


def test_h5same(datadir):
    """test for h5 to h5 comparisons"""
    assert h5_same(datadir.join("source.mesh.h5"), datadir.join("source.mesh.h5"))
    with pytest.raises(ValueError):
        assert h5_same(datadir.join("source.mesh.h5"), datadir.join('target.mesh.h5'))
