"""
Error-path tests for centralized exception handling in imaging_server_kit.
"""
from fastapi.testclient import TestClient
import pytest

from imaging_server_kit import algorithm_server


@algorithm_server(
    algorithm_name="erroralgo",
    parameters={},
    sample_images=[],
    metadata_file=None,
)
def error_algo():
    # Algorithm that raises an unexpected exception
    raise RuntimeError("oops something went wrong")

error_client = TestClient(error_algo.app, raise_server_exceptions=False)

def test_internal_server_error_response():
    # Calling process should yield a 500 with structured JSON
    resp = error_client.post("/erroralgo/process", json={})
    assert resp.status_code == 500
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("error_type") == "internal_server_error"
    # Message should include the exception text
    assert "oops something went wrong" in data.get("message", "")


@algorithm_server(
    algorithm_name="validationalgo",
    parameters={},
    sample_images=[],
    metadata_file=None,
)
def validation_algo():
    # Minimal algorithm, returns empty
    return []

validation_client = TestClient(validation_algo.app, raise_server_exceptions=False)

def test_validation_error_on_extra_field():
    # Sending an extra field should trigger a 422 validation error
    resp = validation_client.post(
        "/validationalgo/process", json={"unexpected": 123}
    )
    assert resp.status_code == 422
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("error_type") == "validation_error"
    detail = data.get("detail")
    # Detail should be a list of error entries
    assert isinstance(detail, list) and len(detail) >= 1
    err = detail[0]
    # Error type should indicate extra field
    err_type = err.get("type", "").lower()
    assert "extra" in err_type

@pytest.mark.parametrize("payload", [None, "not a dict"])
def test_validation_error_on_invalid_json(payload):
    # Missing or invalid JSON body yields 422
    if payload is None:
        resp = validation_client.post("/validationalgo/process")
    else:
        resp = validation_client.post(
            "/validationalgo/process", data=payload, headers={"Content-Type": "application/json"}
        )
    assert resp.status_code == 422
    data = resp.json()
    assert data.get("error_type") == "validation_error"
    # Detail should list the JSON parse or validation error
    assert isinstance(data.get("detail"), list)