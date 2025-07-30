import pytest
import requests
from unittest.mock import patch, MagicMock

from agent_pilot.optimize.optimize_client import optimize_service_start, optimize_service_get_progress
from agent_pilot.config import Config
from agent_pilot.optimize.models import (
    OptimizeServiceStartOptimizeResult,
    OptimizeServiceProgressResult,
    OptimizeJobInfoPayload,
    OptimizeProgress,
)
import agent_pilot.http_client


# --- Fixtures ---


@pytest.fixture(autouse=True)
def reset_http_client_singleton_before_each_test():
    """
    Ensure the agent_pilot.http_client.http_client singleton is reset before each test run.
    This will force get_http_client() to create a new instance for each test.
    """
    agent_pilot.http_client.http_client = None


@pytest.fixture
def mock_get_config():
    """Fixture to mock get_config."""
    with patch('agent_pilot.http_client.get_config') as mock_get:
        config = MagicMock(spec=Config)
        config.api_key = 'test_api_key_from_config'
        config.api_url = 'http://default-api-url.com'
        config.ssl_verify = True
        config.local_debug = False  # Default to False
        config.verbose = False
        mock_get.return_value = config
        yield config


@pytest.fixture
def mock_requests_post():
    """Fixture to mock requests.post."""
    with patch('agent_pilot.http_client.requests.post') as mock_post:
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.ok = True
        # Default successful response structure, can be overridden in tests
        mock_response.json.return_value = {'Result': {}}
        mock_post.return_value = mock_response
        yield mock_post


# --- Test Data ---
TEST_TASK_ID = 'test_task_123'
TEST_VERSION = 'v1.0'
TEST_OPTIMIZE_JOB_ID = 'opt_job_789'

# --- Test Cases for optimize_service_start ---


def test_start_optimize_success_production(mock_get_config, mock_requests_post):
    """Test successful start_optimize in production mode."""
    mock_get_config.local_debug = False
    expected_result_data = {
        'TaskId': TEST_TASK_ID,
        'Version': TEST_VERSION,
        'OptimizeJobId': TEST_OPTIMIZE_JOB_ID,
    }
    mock_requests_post.return_value.json.return_value = {'Result': expected_result_data}

    result = optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)

    assert isinstance(result, OptimizeServiceStartOptimizeResult)
    assert result.TaskId == TEST_TASK_ID
    assert result.Version == TEST_VERSION
    assert result.OptimizeJobId == TEST_OPTIMIZE_JOB_ID

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert call_args[0][0].startswith(f'{mock_get_config.api_url}')
    assert 'Authorization' in call_args[1]['headers']
    assert call_args[1]['headers']['Authorization'] == f'Bearer {mock_get_config.api_key}'
    assert {'TaskId': TEST_TASK_ID, 'Version': TEST_VERSION}.items() <= call_args[1]['json'].items()


def test_start_optimize_success_local_debug(mock_get_config, mock_requests_post):
    """Test successful start_optimize in local debug mode."""
    mock_get_config.local_debug = True
    expected_result_data = {
        'TaskId': TEST_TASK_ID,
        'Version': TEST_VERSION,
        'OptimizeJobId': TEST_OPTIMIZE_JOB_ID,
    }
    mock_requests_post.return_value.json.return_value = {'Result': expected_result_data}

    result = optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)

    assert isinstance(result, OptimizeServiceStartOptimizeResult)
    assert result.OptimizeJobId == TEST_OPTIMIZE_JOB_ID

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert (
        call_args[0][0] == f'{mock_get_config.api_url}/agent-pilot-optimize?'
        f'Version=2024-01-01&Action=OptimizeServiceStartOptimize'
    )
    assert 'Authorization' in call_args[1]['headers']
    assert {'TaskId': TEST_TASK_ID, 'Version': TEST_VERSION}.items() <= call_args[1]['json'].items()


def test_start_optimize_missing_api_key_production(mock_get_config, mock_requests_post):
    """Test RuntimeError when API key is missing in production for start_optimize."""
    mock_get_config.api_key = None
    mock_get_config.local_debug = False

    with pytest.raises(RuntimeError, match='No authentication api_key provided'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)
    mock_requests_post.assert_not_called()


def test_start_optimize_unauthorized_401(mock_get_config, mock_requests_post):
    """Test RuntimeError on 401 Unauthorized response for start_optimize."""
    mock_requests_post.return_value.status_code = 401
    mock_requests_post.return_value.ok = False

    with pytest.raises(RuntimeError, match='Invalid or unauthorized API credentials'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)
    mock_requests_post.assert_called_once()


def test_start_optimize_other_http_error(mock_get_config, mock_requests_post):
    """Test RuntimeError on non-200/401 HTTP error for start_optimize."""
    mock_requests_post.return_value.status_code = 500
    mock_requests_post.return_value.ok = False
    mock_requests_post.return_value.text = 'Internal Server Error'

    with pytest.raises(RuntimeError, match='500 - Internal Server Error'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)
    mock_requests_post.assert_called_once()


def test_start_optimize_network_error(mock_get_config, mock_requests_post):
    """Test RuntimeError on requests.exceptions.RequestException for start_optimize."""
    mock_requests_post.side_effect = requests.exceptions.RequestException('Connection failed')

    with pytest.raises(RuntimeError, match='Network error while starting optimization job: Connection failed'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)
    mock_requests_post.assert_called_once()


def test_start_optimize_empty_result_data(mock_get_config, mock_requests_post):
    """Test RuntimeError when API returns an empty 'Result' for start_optimize."""
    mock_requests_post.return_value.json.return_value = {'Result': None}

    with pytest.raises(RuntimeError, match='Optimization job start result not found in response'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)
    mock_requests_post.assert_called_once()

    mock_requests_post.return_value.json.return_value = {}  # No 'Result' key
    with pytest.raises(RuntimeError, match='Optimization job start result not found in response'):
        optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION)


def test_start_optimize_custom_api_key_url(mock_get_config, mock_requests_post):
    """Test start_optimize with custom api_key and api_url."""
    custom_key = 'custom_test_key'
    custom_url = 'http://custom-api-url.com'
    expected_result_data = {'TaskId': TEST_TASK_ID, 'Version': TEST_VERSION, 'OptimizeJobId': TEST_OPTIMIZE_JOB_ID}
    mock_requests_post.return_value.json.return_value = {'Result': expected_result_data}

    optimize_service_start(task_id=TEST_TASK_ID, version=TEST_VERSION, api_key=custom_key, api_url=custom_url)

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert call_args[0][0].startswith(custom_url)
    assert call_args[1]['headers']['Authorization'] == f'Bearer {custom_key}'


# --- Test Cases for optimize_service_get_progress ---


def test_get_progress_success_production(mock_get_config, mock_requests_post):
    """Test successful get_progress in production mode."""
    mock_get_config.local_debug = False
    expected_job_info = {
        'JobId': TEST_OPTIMIZE_JOB_ID,
        'Version': TEST_VERSION,
        'State': 3,
        'CreatedTime': '2024-01-01T00:00:00Z',
        'UpdatedTime': '2024-01-01T01:00:00Z',
    }
    expected_progress = {
        'ProgressPercent': 100.0,
        'TotalCnt': 10,
        'BetterCnt': 5,
        'WorseCnt': 2,
        'UnchangedCnt': 3,
        'InitFullscoreCnt': 0,
        'FullscoreCntList': [0, 1],
        'InitAverageScore': 0.5,
        'AverageScoreList': [0.5, 0.5],
        'OptimizeTokenConsumption': 10000,
        'OptimalPrompt': 'test_prompt',
    }
    mock_requests_post.return_value.json.return_value = {
        'Result': {'JobInfo': expected_job_info, 'Progress': expected_progress}
    }

    result = optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)

    assert isinstance(result, OptimizeServiceProgressResult)
    assert isinstance(result.JobInfo, OptimizeJobInfoPayload)
    assert isinstance(result.Progress, OptimizeProgress)
    assert result.JobInfo.JobId == TEST_OPTIMIZE_JOB_ID
    assert result.Progress.percent == 100.0

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert call_args[0][0].startswith(f'{mock_get_config.api_url}')
    assert 'Authorization' in call_args[1]['headers']
    assert call_args[1]['headers']['Authorization'] == f'Bearer {mock_get_config.api_key}'
    assert {'OptimizeJobId': TEST_OPTIMIZE_JOB_ID}.items() <= call_args[1]['json'].items()


def test_get_progress_success_local_debug(mock_get_config, mock_requests_post):
    """Test successful get_progress in local debug mode."""
    mock_get_config.local_debug = True
    expected_job_info = {
        'JobId': TEST_OPTIMIZE_JOB_ID,
        'Version': TEST_VERSION,
        'State': 2,
        'CreatedTime': '2024-01-01T00:00:00Z',
        'UpdatedTime': '2024-01-01T01:00:00Z',
    }
    expected_progress = {
        'ProgressPercent': 50.0,
        'TotalCnt': 10,
        'BetterCnt': 2,
        'WorseCnt': 1,
        'UnchangedCnt': 7,
        'InitFullscoreCnt': 0,
        'FullscoreCntList': [0, 1],
        'InitAverageScore': 0.5,
        'AverageScoreList': [0.5, 0.5],
        'OptimizeTokenConsumption': 10000,
        'OptimalPrompt': 'test_prompt',
    }
    mock_requests_post.return_value.json.return_value = {
        'Result': {'JobInfo': expected_job_info, 'Progress': expected_progress}
    }

    result = optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)

    assert isinstance(result, OptimizeServiceProgressResult)
    assert result.JobInfo.State == 2  # Example state
    assert result.Progress.percent == 50.0

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert call_args[0][0].startswith(f'{mock_get_config.api_url}')
    assert 'Authorization' in call_args[1]['headers']
    assert {'OptimizeJobId': TEST_OPTIMIZE_JOB_ID}.items() <= call_args[1]['json'].items()


def test_get_progress_missing_api_key_production(mock_get_config, mock_requests_post):
    """Test RuntimeError when API key is missing in production for get_progress."""
    mock_get_config.api_key = None
    mock_get_config.local_debug = False
    # Simulate config.local_debug might not exist
    with patch('agent_pilot.optimize.optimize_client.hasattr') as mock_hasattr:
        mock_hasattr.return_value = False  # Simulate local_debug absence

        with pytest.raises(RuntimeError, match='No authentication api_key provided'):
            optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)
        mock_requests_post.assert_not_called()


def test_get_progress_unauthorized_401(mock_get_config, mock_requests_post):
    """Test RuntimeError on 401 Unauthorized response for get_progress."""
    mock_requests_post.return_value.status_code = 401
    mock_requests_post.return_value.ok = False

    with pytest.raises(RuntimeError, match='Invalid or unauthorized API credentials'):
        optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)
    mock_requests_post.assert_called_once()


def test_get_progress_other_http_error(mock_get_config, mock_requests_post):
    """Test RuntimeError on non-200/401 HTTP error for get_progress."""
    mock_requests_post.return_value.status_code = 503
    mock_requests_post.return_value.ok = False
    mock_requests_post.return_value.text = 'Service Unavailable'

    with pytest.raises(RuntimeError, match='Error fetching optimization progress:'):
        optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)
    mock_requests_post.assert_called_once()


def test_get_progress_network_error(mock_get_config, mock_requests_post):
    """Test RuntimeError on requests.exceptions.RequestException for get_progress."""
    mock_requests_post.side_effect = requests.exceptions.RequestException('Connection timeout')

    with pytest.raises(RuntimeError, match='Network error while fetching optimization progress: Connection timeout'):
        optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)
    mock_requests_post.assert_called_once()


def test_get_progress_empty_result_data(mock_get_config, mock_requests_post):
    """Test RuntimeError when API returns an empty 'Result' for get_progress."""
    mock_requests_post.return_value.json.return_value = {'Result': None}

    with pytest.raises(RuntimeError, match='Optimization progress result not found in response'):
        optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)
    mock_requests_post.assert_called_once()

    mock_requests_post.reset_mock()  # Reset mock for the next call
    mock_requests_post.return_value.json.return_value = {}  # No 'Result' key
    with pytest.raises(RuntimeError, match='Optimization progress result not found in response'):
        optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID)


def test_get_progress_custom_api_key_url(mock_get_config, mock_requests_post):
    """Test get_progress with custom api_key and api_url."""
    custom_key = 'custom_progress_key'
    custom_url = 'http://custom-progress-api.com'
    expected_job_info = {
        'JobId': TEST_OPTIMIZE_JOB_ID,
        'Version': TEST_VERSION,
        'State': 2,
        'CreatedTime': '2024-01-01T00:00:00Z',
        'UpdatedTime': '2024-01-01T01:00:00Z',
    }
    expected_progress = {
        'ProgressPercent': 50.0,
        'TotalCnt': 10,
        'BetterCnt': 2,
        'WorseCnt': 1,
        'UnchangedCnt': 7,
        'InitFullscoreCnt': 0,
        'FullscoreCntList': [0, 1],
        'InitAverageScore': 0.5,
        'AverageScoreList': [0.5, 0.5],
        'OptimizeTokenConsumption': 10000,
        'OptimalPrompt': 'test_prompt',
    }
    mock_requests_post.return_value.json.return_value = {
        'Result': {'JobInfo': expected_job_info, 'Progress': expected_progress}
    }

    optimize_service_get_progress(optimize_job_id=TEST_OPTIMIZE_JOB_ID, api_key=custom_key, api_url=custom_url)

    mock_requests_post.assert_called_once()
    call_args = mock_requests_post.call_args
    assert call_args[0][0].startswith(custom_url)
    assert call_args[1]['headers']['Authorization'] == f'Bearer {custom_key}'
