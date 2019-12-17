import pytest
import sys

sys.path.append("src")

import numpy as np
import json
from src.library.analyzer.summary import replace_all_nans


def test_nans():
    obj = {}
    obj["firstKey"] = np.nan
    obj["secondKey"] = {}
    obj["secondKey"]["nestedKey"] = np.nan
    replace_all_nans(obj)
    assert obj["firstKey"] is None
    assert obj["secondKey"]["nestedKey"] is None


def test_for_zeros():
    obj = {}
    obj["zero"] = 0
    obj["isNan"] = np.nan
    replace_all_nans(obj)
    assert obj["zero"] == 0
    assert obj["isNan"] is None


def test_valid_json():
    obj = {}
    obj["number"] = 1
    obj["nothing"] = np.nan
    obj["zero"] = 0
    replace_all_nans(obj)
    string = json.dumps(obj)
    assert string == '{"number": 1, "nothing": null, "zero": 0}'
