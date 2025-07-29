"""
Integration tests for a minimal algorithm server using FastAPI TestClient.
"""
from fastapi.testclient import TestClient
import pytest

from imaging_server_kit import algorithm_server


@algorithm_server(
    algorithm_name="hello",
    parameters={},
    sample_images=[],
    metadata_file=None,
)
def hello_algorithm():
    # Minimal algorithm: no parameters, returns empty result list
    return []

# Instantiate the TestClient using the generated FastAPI app
client = TestClient(hello_algorithm.app)

def test_services_endpoint():
    response = client.get("/services")
    assert response.status_code == 200
    assert response.json() == {"services": ["hello"]}

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    # Version should be a string
    assert isinstance(response.json(), str)

def test_parameters_endpoint():
    # No parameters defined, properties should be empty
    response = client.get("/hello/parameters")
    assert response.status_code == 200
    schema = response.json()
    assert isinstance(schema, dict)
    assert schema.get("properties") == {}

def test_process_endpoint_success():
    # Sending empty JSON for empty parameters
    response = client.post("/hello/process", json={})
    assert response.status_code == 201
    # Should return a serialized empty list
    assert response.json() == []

@pytest.mark.parametrize("payload, status_code", [
    (None, 422),
    ("not a dict", 422),
])
def test_process_endpoint_invalid_payload(payload, status_code):
    # Invalid payload should return a 422 error
    if payload is None:
        response = client.post("/hello/process")
    else:
        response = client.post("/hello/process", data=payload)
    assert response.status_code == status_code