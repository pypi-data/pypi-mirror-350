import pytest
from unittest.mock import patch, MagicMock
from agent_pilot.models import PromptVersion
import uuid

from agent_pilot.tracking import run_manager
from agent_pilot.config import Config


@pytest.fixture
def mock_config():
    """Fixture for mocking the config object."""
    test_config = Config(
        api_key='test_api_key', api_url='http://test-api-url.com', disable_ssl_verify=False, verbose=False
    )
    test_config.local_debug = False

    with patch('agent_pilot.config.get_config', return_value=test_config):
        with patch('agent_pilot.http_client.get_config', return_value=test_config):
            yield test_config


@pytest.fixture
def mock_requests_post():
    """Fixture for mocking requests.post calls."""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def sample_prompt_version_dict():
    """Sample prompt version dictionary for testing."""
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant. {{variable}}'},
        {'role': 'user', 'content': 'Hello, {{name}}!'},
    ]

    return {
        'prompt_version_id': 'test-pvid-123',
        'task_id': 'test-task-123',
        'version': 'v1',
        'messages': messages,
        'variables_name': 'test_vars',
        'model_name': 'test-model',
        'temperature': 0.7,
        'top_p': 1.0,
    }


@pytest.fixture
def sample_prompt_version(sample_prompt_version_dict):
    """Sample PromptVersion object for testing."""
    return PromptVersion(**sample_prompt_version_dict)


@pytest.fixture
def mock_time():
    """Fixture for mocking time.time function."""
    with patch('time.time') as mock_time:
        mock_time.return_value = 1000  # Fixed timestamp in seconds
        yield mock_time


@pytest.fixture(autouse=True)
def reset_run_manager():
    """Reset the RunManager singleton before and after each test."""
    # Reset before test
    run_manager._current_run = None
    run_manager._run_stack = []
    run_manager.runs = {}
    yield
    # Reset after test
    run_manager._current_run = None
    run_manager._run_stack = []
    run_manager.runs = {}


@pytest.fixture
def mock_uuid(monkeypatch):
    """Mock uuid4 to return a deterministic value for testing."""
    value = str(uuid.uuid4())

    class MockUUID:
        @staticmethod
        def uuid4():
            return value

    monkeypatch.setattr(uuid, 'uuid4', MockUUID.uuid4)
    return value
