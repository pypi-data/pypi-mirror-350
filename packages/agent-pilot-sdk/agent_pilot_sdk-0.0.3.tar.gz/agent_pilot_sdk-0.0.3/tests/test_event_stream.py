import pytest
from unittest.mock import MagicMock, patch

from agent_pilot.pe.api import generate_prompt_stream
from agent_pilot.pe.utils import parse_event_stream_line
from agent_pilot.pe.models import GeneratePromptChunk, GeneratePromptStreamResponseChunk


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


class TestEventStreamParser:
    def test_parse_event_line_with_event_and_data(self):
        # This function only handles event: or data: separately
        event_line = 'event: message'
        result = parse_event_stream_line(event_line)
        assert result is not None
        assert result.event == 'message'

        # Data line format must match the regex pattern
        data_line = 'data: "Hello, world!"'
        result = parse_event_stream_line(data_line, result)
        assert result is not None
        assert result.data.content == 'Hello, world!'

    def test_parse_event_line_with_only_data(self):
        # The current implementation doesn't create a new event chunk for data-only lines
        # without an existing chunk with message event
        data_line = 'data: "Hello, world!"'
        result = parse_event_stream_line(
            data_line,
            GeneratePromptStreamResponseChunk(
                event='message',
                data=GeneratePromptChunk(content='', usage=None),
            ),
        )
        assert result is not None
        assert result.event == 'message'
        assert result.data.content == 'Hello, world!'

    def test_parse_event_line_with_non_json_data(self):
        # The current implementation requires data to be in quotes
        data_line = 'data: "This is plain text"'
        result = parse_event_stream_line(
            data_line,
            GeneratePromptStreamResponseChunk(
                event='message',
                data=GeneratePromptChunk(content='', usage=None),
            ),
        )
        assert result is not None
        assert result.event == 'message'
        assert result.data.content == 'This is plain text'

    def test_parse_event_line_with_newlines(self):
        # Test that newlines in the data are properly decoded
        data_line = 'data: "Line 1\\nLine 2\\nLine 3"'
        result = parse_event_stream_line(
            data_line,
            GeneratePromptStreamResponseChunk(
                event='message',
                data=GeneratePromptChunk(content='', usage=None),
            ),
        )
        assert result is not None
        assert result.event == 'message'
        assert result.data.content == 'Line 1\nLine 2\nLine 3'
        assert len(result.data.content.split('\n')) == 3

    def test_parse_event_line_with_invalid_format(self):
        # The current implementation returns None for invalid formats
        line = 'invalid format'
        result = parse_event_stream_line(line)
        assert result is None

    def test_parse_event_line_with_empty_line(self):
        # The current implementation returns None for empty lines
        result = parse_event_stream_line('')
        assert result is None

    def test_parse_event_line_with_event(self):
        # Test that an event line is properly parsed
        line = 'event: message'
        result = parse_event_stream_line(line)
        assert result is not None
        assert result.event == 'message'
        assert result.data.content == ''

    def test_parse_event_line_with_error(self):
        # Test that an error event is properly parsed
        line = 'event: error'
        result = parse_event_stream_line(line)
        assert result is not None
        assert result.event == 'error'
        assert result.data.content == ''


class TestGeneratePromptStream:
    @patch('agent_pilot.pe.api.get_http_client')
    def test_generate_prompt_stream(self, mock_get_http_client):
        # Create mock chunks
        chunks = ['chunk1', 'chunk2', 'chunk3']

        # Create a mock streaming response
        mock_response = MockStreamingResponse(chunks)

        # Create mock for the HTTP client
        mock_client = MagicMock()
        mock_client.post.return_value = (mock_response, 200)
        mock_get_http_client.return_value = mock_client

        # Call the function
        results = list(generate_prompt_stream('Test rule'))

        # Verify HTTP client was called correctly
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args[1]
        assert call_args['action'] == 'GeneratePromptStream'
        assert call_args['stream'] is True

        # Check the results
        assert [chunk.data.content for chunk in results] == chunks

    @patch('agent_pilot.pe.api.get_http_client')
    def test_generate_prompt_stream_with_complex_chunks(self, mock_get_http_client):
        # Test handling of chunks that are dictionaries with 'data' field
        complex_chunks = [{'data': 'chunk1'}, 'chunk2', {'data': 'chunk3', 'extra': 'ignored'}]
        expected_chunks = ['chunk1', 'chunk2', 'chunk3']

        # Create a mock streaming response
        mock_response = MockStreamingResponse(complex_chunks)

        # Create mock for the HTTP client
        mock_client = MagicMock()
        mock_client.post.return_value = (mock_response, 200)
        mock_get_http_client.return_value = mock_client

        # Call the function
        results = list(generate_prompt_stream('Test rule'))

        assert [chunk.data.content for chunk in results] == expected_chunks

    @patch('agent_pilot.pe.api.get_http_client')
    def test_generate_prompt_stream_with_newlines(self, mock_get_http_client):
        # Test handling of newlines in the chunks
        chunks = ['Line 1\\nLine 2', 'Text with\\nnewlines\\nand more lines']

        # Create a mock streaming response
        mock_response = MockStreamingResponse(chunks)

        # Create mock for the HTTP client
        mock_client = MagicMock()
        mock_client.post.return_value = (mock_response, 200)
        mock_get_http_client.return_value = mock_client

        # Call the function
        results = list(generate_prompt_stream('Test rule'))

        # Check that newlines are properly decoded
        assert len(results) == 2
        assert results[0].data.content == 'Line 1\nLine 2'
        assert results[1].data.content == 'Text with\nnewlines\nand more lines'

        # Verify that the strings actually contain newlines
        assert len(results[0].data.content.split('\n')) == 2
        assert len(results[1].data.content.split('\n')) == 3

    @patch('agent_pilot.pe.api.get_http_client')
    def test_generate_prompt_stream_http_error(self, mock_get_http_client):
        # Setup mock client that returns an error
        mock_client = MagicMock()
        mock_client.post.return_value = ({'Error': 'Error message'}, 400)
        mock_get_http_client.return_value = mock_client

        # Call should raise RuntimeError
        with pytest.raises(RuntimeError) as excinfo:
            list(generate_prompt_stream('Test rule'))

        assert 'Error generating prompt: 400' in str(excinfo.value)
