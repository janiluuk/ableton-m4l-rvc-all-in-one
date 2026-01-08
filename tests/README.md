# Tests

This directory contains tests for the Ableton M4L RVC All-In-One project.

## Running Tests

### Install test dependencies

```bash
pip install -r requirements-test.txt
```

### Run all tests

```bash
pytest tests/ -v
```

### Run specific test file

```bash
pytest tests/test_applio_integration.py -v
```

## Test Coverage

### Applio Integration Tests (`test_applio_integration.py`)

Tests for the Applio voice conversion integration:

- **test_applio_server_url_from_env**: Verifies that the Applio server URL can be configured via the `APPLIO_SERVER` environment variable
- **test_convert_with_applio_disabled**: Tests that the convert method returns a tuple with `None` for the Applio output when Applio processing is disabled
- **test_convert_with_applio_auto_enables_separation**: Verifies that enabling Applio automatically enables vocal separation
- **test_applio_server_imports**: Tests that the Applio server module can be imported successfully

## Integration Testing

For integration testing with actual Docker containers:

1. Start the services:
```bash
cd server
docker compose up -d
```

2. Wait for services to be ready:
```bash
# Check RVC server
curl http://localhost:8000/health

# Check Applio server
curl http://localhost:8001/health
```

3. Test the full pipeline with a sample audio file (requires actual models to be installed)

## Notes

- Unit tests mock external dependencies to run quickly without requiring actual RVC/Applio installations
- Integration tests require Docker containers to be running
- Model files are not included in the repository and must be provided separately
