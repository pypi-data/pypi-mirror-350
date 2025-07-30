import pytest
from fed_rf_mk.client import FLClient

def test_set_get_params():
    client = FLClient()
    data = {"target": "y", "ignored_columns": ["x1", "x2"]}
    model = {"fl_epochs": 3}
    # setting
    assert client.set_data_params(data) == f"Data parameters set: {data}"
    assert client.set_model_params(model) == f"Model parameters set: {model}"
    # getting
    assert client.get_data_params() == data
    assert client.get_model_params() == model

def test_weight_normalization_all_none():
    client = FLClient()
    # all weights None → equal distribution
    client.weights = {"a": None, "b": None, "c": None}
    client.modelParams = {"fl_epochs": 0}  # skip any federated loop
    client.dataParams = {}
    client.datasites = {}                # no actual calls
    client.run_model()
    assert client.weights == pytest.approx({"a": 1/3, "b": 1/3, "c": 1/3})

def test_weight_normalization_partial_none():
    client = FLClient()
    # one defined, two undefined
    client.weights = {"a": 0.2, "b": None, "c": None}
    client.modelParams = {"fl_epochs": 0}
    client.dataParams = {}
    client.datasites = {}
    client.run_model()
    # leftover = 0.8, split evenly → 0.4 each
    assert client.weights["a"] == pytest.approx(0.2)
    assert client.weights["b"] == pytest.approx(0.4)
    assert client.weights["c"] == pytest.approx(0.4)
