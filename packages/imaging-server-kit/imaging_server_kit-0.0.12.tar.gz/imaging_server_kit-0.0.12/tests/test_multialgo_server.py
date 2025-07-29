"""
Integration tests for MultiAlgorithmServer.
"""
from fastapi.testclient import TestClient
import pytest

from imaging_server_kit import algorithm_server, MultiAlgorithmServer

# Define two simple algorithm servers
@algorithm_server(
    algorithm_name="a1",
    parameters={},
    sample_images=[],
    metadata_file=None,
)
def algo1():
    # Returns empty result
    return []

@algorithm_server(
    algorithm_name="a2",
    parameters={},
    sample_images=[],
    metadata_file=None,
)
def algo2():
    # Raises an error to test 500 handling
    raise RuntimeError("algo2 failure")

# Create the multi-algo server
multi_srv = MultiAlgorithmServer("multi", [algo1, algo2])
client = TestClient(multi_srv.app, raise_server_exceptions=False)

def test_list_services():
    resp = client.get("/services")
    assert resp.status_code == 200
    assert set(resp.json().get("services", [])) == {"a1", "a2"}

def test_version():
    resp = client.get("/version")
    assert resp.status_code == 200
    assert isinstance(resp.json(), str)

@pytest.mark.parametrize("algo", ["a1", "a2"])
def test_parameters_endpoint(algo):
    resp = client.get(f"/{algo}/parameters")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    # No properties defined
    assert body.get("properties", {}) == {}

def test_sample_images_empty():
    resp = client.get("/a1/sample_images")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"sample_images": []}

def test_unknown_algorithm_404():
    # Info
    resp = client.get("/unknown/info")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Algorithm unknown not found"
    # Process
    resp = client.post("/unknown/process", json={})
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Algorithm unknown not found"
    # Parameters
    resp = client.get("/unknown/parameters")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Algorithm unknown not found"
    # Sample images
    resp = client.get("/unknown/sample_images")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Algorithm unknown not found"

def test_validation_error_extra_field():
    # a1 expects no params, so extra field triggers 422
    resp = client.post("/a1/process", json={"foo": 123})
    assert resp.status_code == 422
    data = resp.json()
    # Validation raised as HTTPException detail list
    assert isinstance(data.get("detail"), list)

def test_runtime_error_internal():
    # algo2 always raises RuntimeError
    resp = client.post("/a2/process", json={})
    assert resp.status_code == 500
    data = resp.json()
    assert data.get("error_type") == "internal_server_error"
    assert "algo2 failure" in data.get("message", "")