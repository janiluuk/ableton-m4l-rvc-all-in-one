# Test Suite

This directory contains automated tests for the RVC API endpoints.

## Running Tests

To run all tests:

```bash
cd server/server
pip install -r requirements.txt
pytest test_api.py -v
```

To run specific test classes:

```bash
# Test only the /convert endpoint
pytest test_api.py::TestConvertEndpoint -v

# Test only the /uvr endpoint
pytest test_api.py::TestUVREndpoint -v

# Test integration
pytest test_api.py::TestAPIIntegration -v
```

To run a specific test:

```bash
pytest test_api.py::TestConvertEndpoint::test_convert_with_uvr_separator -v
```

## Test Coverage

The test suite covers:

### /convert Endpoint Tests (TestConvertEndpoint)
- Basic endpoint accessibility
- Request with default parameters
- Request with Demucs separator
- Request with UVR separator
- Request with all optional parameters
- Error handling

### /uvr Endpoint Tests (TestUVREndpoint)
- Basic endpoint accessibility
- UVR with Demucs (default behavior)
- UVR with UVR separator
- UVR with Demucs-specific parameters (shifts, segment)
- Error handling

### RVCConverter Tests (TestRVCConverter)
- Verify Demucs separator is called correctly
- Verify UVR separator is called correctly

### API Integration Tests (TestAPIIntegration)
- OpenAPI schema generation
- API documentation accessibility
- Endpoint schema validation

## Test Structure

Tests use:
- **pytest** as the test framework
- **FastAPI TestClient** for API endpoint testing
- **unittest.mock** for mocking external dependencies
- Mock audio files generated in-memory for testing

## Dependencies

Testing dependencies are included in `requirements.txt`:
- pytest>=7.0.0
- httpx>=0.24.0
- python-multipart>=0.0.6

Heavy dependencies (torch, librosa) are mocked in tests to keep test execution fast.

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
- name: Run API tests
  run: |
    cd server/server
    pip install pytest httpx python-multipart fastapi numpy scipy soundfile
    pytest test_api.py -v
```
