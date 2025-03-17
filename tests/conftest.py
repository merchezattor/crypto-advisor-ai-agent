"""
Pytest configuration file.

This file contains global fixtures and configuration for the test suite.
"""
import pytest

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark a test as an integration test that requires external dependencies"
    )

def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--run-integration", 
        action="store_true", 
        default=False, 
        help="run integration tests that depend on external services"
    )

def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless explicitly requested."""
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration) 