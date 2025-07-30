import pytest
from unittest.mock import MagicMock, patch

from agent_pilot.pe.api import generate_prompt_stream
from agent_pilot.pe.models import GeneratePromptStreamRequest
from agent_pilot.models import TaskType


class MockStreamingResponse:
    """Mock response object for streaming responses."""

    def __init__(self, chunks):
        self.chunks = chunks

    def iter_lines(self):
        """Return the lines of the stream."""
        for chunk in self.chunks:
            # Simulate the event stream format
            yield 'event: message'.encode('utf-8')
            if isinstance(chunk, dict) and 'data' in chunk:
                yield f'data: "{chunk["data"]}"'.encode('utf-8')
            else:
                yield f'data: "{chunk}"'.encode('utf-8')
            yield b''  # Empty line


def test_generate_prompt_stream():
    # Create mock chunks
    chunks = ['chunk1', 'chunk2', 'chunk3']

    # Create a mock streaming response
    mock_response = MockStreamingResponse(chunks)

    # Create mock for the HTTP client
    mock_http_client = MagicMock()
    mock_http_client.post.return_value = (mock_response, 200)

    with patch('agent_pilot.pe.api.get_http_client', return_value=mock_http_client):
        result_chunks = list(
            generate_prompt_stream(
                rule='Create a creative story',
                temperature=0.8,
                top_p=0.9,
                task_type=TaskType.DEFAULT,
                request_id='test-request',
            )
        )

    assert [chunk.data.content for chunk in result_chunks] == chunks

    # Verify the request was made with correct parameters
    mock_http_client.post.assert_called_once()
    call_args = mock_http_client.post.call_args

    assert call_args[1]['action'] == 'GeneratePromptStream'

    # Check request payload
    data = call_args[1]['data']
    assert data['Rule'] == 'Create a creative story'
    assert data['Temperature'] == 0.8
    assert data['TopP'] == 0.9
    assert data['TaskType'] == 'DEFAULT'
    assert data['RequestId'] == 'test-request'


def test_generate_prompt_stream_error():
    # Create mock for the HTTP client that raises an error
    mock_http_client = MagicMock()
    mock_http_client.post.return_value = ({'Error': 'Test error message'}, 400)

    with patch('agent_pilot.pe.api.get_http_client', return_value=mock_http_client):
        with pytest.raises(RuntimeError) as excinfo:
            list(generate_prompt_stream(rule='Test rule'))

    assert 'Error generating prompt: 400' in str(excinfo.value)


def test_complex_chunk_format():
    # Test handling of chunks that are dictionaries with 'data' field
    complex_chunks = [{'data': 'chunk1'}, 'chunk2', {'data': 'chunk3', 'extra': 'ignored'}]
    expected_chunks = ['chunk1', 'chunk2', 'chunk3']

    # Create a mock streaming response
    mock_response = MockStreamingResponse(complex_chunks)

    # Create mock for the HTTP client
    mock_http_client = MagicMock()
    mock_http_client.post.return_value = (mock_response, 200)

    with patch('agent_pilot.pe.api.get_http_client', return_value=mock_http_client):
        chunks = list(generate_prompt_stream(rule='Test rule'))

    assert [chunk.data.content for chunk in chunks] == expected_chunks


def test_request_serialization():
    """Test that request models correctly serialize with aliases."""
    request = GeneratePromptStreamRequest(rule='Test rule', temperature=0.5, task_type=TaskType.DEFAULT)

    data = request.model_dump(by_alias=True)

    assert data['Rule'] == 'Test rule'
    assert data['Temperature'] == 0.5
    assert data['TaskType'] == 'DEFAULT'
    assert data['CurrentPrompt'] is None
