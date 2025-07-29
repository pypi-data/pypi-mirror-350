"""
Smoke tests for imaging_server_kit package import and basic API availability.
"""


def test_import_imaging_server_kit():
    # Basic import
    import imaging_server_kit as kit

    # __version__ should be present
    assert hasattr(kit, "__version__"), "__version__ attribute is missing"
    # Core classes and functions should import without error
    from imaging_server_kit import (
        AlgorithmServer,
        Client,
        AlgorithmHub,
        MultiAlgorithmServer,
        AuthenticatedAlgorithmServer,
        algorithm_server,
    )
    from imaging_server_kit.core import (
        encode_contents,
        decode_contents,
        serialize_result_tuple,
        deserialize_result_tuple,
    )

    # Ensure imported objects are callable or types
    assert callable(AlgorithmServer), "AlgorithmServer should be callable"
    assert callable(Client), "Client should be callable"
    assert callable(AlgorithmHub), "AlgorithmHub should be callable"
    assert callable(MultiAlgorithmServer), "MultiAlgorithmServer should be callable"
    # algorithm_server should be a decorator (callable)
    assert callable(algorithm_server), "algorithm_server should be callable"
    # serialization utilities
    assert callable(encode_contents), "encode_contents should be callable"
    assert callable(decode_contents), "decode_contents should be callable"
    assert callable(serialize_result_tuple), "serialize_result_tuple should be callable"
    assert callable(
        deserialize_result_tuple
    ), "deserialize_result_tuple should be callable"
