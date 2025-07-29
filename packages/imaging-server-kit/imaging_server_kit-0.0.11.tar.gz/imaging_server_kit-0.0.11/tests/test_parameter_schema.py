"""
Tests for parameter schema ergonomics in imaging_server_kit.
"""

from fastapi.testclient import TestClient
import pytest

from imaging_server_kit import (
    algorithm_server,
    IntSpinBoxUI,
    FloatSpinBoxUI,
    DropDownUI,
    ImageUI,
)


@algorithm_server(
    algorithm_name="paramtest",
    parameters={
        "n": IntSpinBoxUI("Number", "Number desc", min=1, max=5, step=1, default=3),
        "f": FloatSpinBoxUI(
            "Float", "Float desc", min=0.1, max=1.0, step=0.1, default=0.5
        ),
        "opt": DropDownUI("Option", "Option desc", items=["a", "b", "c"], default="b"),
    },
    sample_images=[],
    metadata_file=None,
)
def param_algo(n, f, opt):
    return []


client = TestClient(param_algo.app)


def test_parameter_schema_properties_and_metadata():
    resp = client.get("/paramtest/parameters")
    assert resp.status_code == 200
    schema = resp.json()
    # All parameters have defaults => no required key
    assert "required" not in schema
    props = schema.get("properties", {})
    # Integer param
    n_schema = props.get("n", {})
    assert n_schema.get("type") == "integer"
    assert n_schema.get("minimum") == 1
    assert n_schema.get("maximum") == 5
    assert n_schema.get("default") == 3
    assert n_schema.get("title") == "Number"
    assert n_schema.get("description") == "Number desc"
    assert n_schema.get("step") == 1
    assert n_schema.get("widget_type") == "int"
    # Float param
    f_schema = props.get("f", {})
    assert f_schema.get("type") == "number"
    assert f_schema.get("minimum") == pytest.approx(0.1)
    assert f_schema.get("maximum") == pytest.approx(1.0)
    assert f_schema.get("default") == pytest.approx(0.5)
    assert f_schema.get("title") == "Float"
    assert f_schema.get("description") == "Float desc"
    assert f_schema.get("step") == pytest.approx(0.1)
    assert f_schema.get("widget_type") == "float"
    # Dropdown param
    o_schema = props.get("opt", {})
    assert o_schema.get("type") == "string"
    # Enum from Literal[*items]
    assert o_schema.get("enum") == ["a", "b", "c"]
    assert o_schema.get("default") == "b"
    assert o_schema.get("title") == "Option"
    assert o_schema.get("description") == "Option desc"
    assert o_schema.get("widget_type") == "dropdown"


@algorithm_server(
    algorithm_name="paramreq",
    parameters={
        "img": ImageUI("Image", "Image desc", dimensionality=[2, 3]),
    },
    sample_images=[],
    metadata_file=None,
)
def param_req(img):
    return []


client_req = TestClient(param_req.app)


def test_required_parameter_in_schema():
    resp = client_req.get("/paramreq/parameters")
    assert resp.status_code == 200
    schema = resp.json()
    # 'img' has no default => required
    assert "required" in schema
    assert "img" in schema.get("required", [])
    # Check property metadata for image
    img_schema = schema.get("properties", {}).get("img", {})
    assert img_schema.get("type") == "string"
    assert img_schema.get("title") == "Image"
    assert img_schema.get("description") == "Image desc"
    assert img_schema.get("widget_type") == "image"
