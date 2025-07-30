import pytest
import os
from typing import Any
from unittest.mock import patch

def pytest_configure(config: Any) -> None:
    """Configure pytest to use the asyncio plugin."""
    config.addinivalue_line("markers", "asyncio: mark test as async")

@pytest.fixture
def mock_openai_api_key():
    """Mock OpenAI API key for testing."""
    return "sk-test-openai-key"

@pytest.fixture
def mock_google_api_key():
    """Mock Google API key for testing."""
    return "test-google-key"

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "sk-test-openai-key",
        "GOOGLE_API_KEY": "test-google-key"
    }):
        yield 