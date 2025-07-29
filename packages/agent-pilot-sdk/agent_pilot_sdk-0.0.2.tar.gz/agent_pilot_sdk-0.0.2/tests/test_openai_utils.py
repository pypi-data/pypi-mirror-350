from unittest.mock import MagicMock, patch
import json
import logging

from agent_pilot.openai_utils import OpenAIUtils


class TestOpenAIUtils:
    def test_parse_role_assistant(self):
        """Test that 'assistant' role is parsed to 'ai'."""
        assert OpenAIUtils.parse_role('assistant') == 'ai'

    def test_parse_role_other(self):
        """Test that other roles remain unchanged."""
        assert OpenAIUtils.parse_role('user') == 'user'
        assert OpenAIUtils.parse_role('system') == 'system'

    def test_get_property_from_dict(self):
        """Test getting property from a dictionary."""
        test_dict = {'key1': 'value1', 'key2': 'value2'}

        assert OpenAIUtils.get_property(test_dict, 'key1') == 'value1'
        assert OpenAIUtils.get_property(test_dict, 'key2') == 'value2'
        assert OpenAIUtils.get_property(test_dict, 'key3') is None

    def test_get_property_from_object(self):
        """Test getting property from an object."""

        class TestObject:
            attr1 = 'value1'
            attr2 = 'value2'

        test_obj = TestObject()

        assert OpenAIUtils.get_property(test_obj, 'attr1') == 'value1'
        assert OpenAIUtils.get_property(test_obj, 'attr2') == 'value2'
        assert OpenAIUtils.get_property(test_obj, 'attr3') is None

    def test_parse_message_dict(self):
        """Test parsing a message from dictionary."""
        test_message = {
            'role': 'user',
            'content': 'Hello, world!',
            'refusal': False,
            'tool_calls': [{'type': 'function', 'id': '123'}],
            'tool_call_id': '123',
        }

        parsed = OpenAIUtils.parse_message(test_message)

        assert parsed['role'] == 'user'
        assert parsed['content'] == 'Hello, world!'
        assert parsed['refusal'] is False
        assert parsed['tool_calls'] == [{'type': 'function', 'id': '123'}]
        assert parsed['tool_call_id'] == '123'
        assert parsed['audio'] is None

    def test_parse_message_with_audio(self):
        """Test parsing a message with audio content."""

        # Create a mock audio object that can be serialized to JSON
        class MockAudio:
            def model_dump_json(self, indent=None, exclude_unset=False):
                return json.dumps({'file_id': '123', 'duration': 10.5})

        # Create a message with audio
        test_message = {'role': 'user', 'content': 'Audio message', 'audio': MockAudio()}

        parsed = OpenAIUtils.parse_message(test_message)

        assert parsed['role'] == 'user'
        assert parsed['content'] == 'Audio message'
        assert parsed['audio'] == {'file_id': '123', 'duration': 10.5}

    def test_parse_message_object(self):
        """Test parsing a message from object."""

        class Message:
            def __init__(self):
                self.role = 'system'
                self.content = 'System message'
                self.refusal = None
                self.audio = None
                self.tool_calls = None
                self.tool_call_id = None

        test_message = Message()
        parsed = OpenAIUtils.parse_message(test_message)

        assert parsed['role'] == 'system'
        assert parsed['content'] == 'System message'
        assert parsed['refusal'] is None
        assert parsed['audio'] is None
        assert parsed['tool_calls'] is None
        assert parsed['tool_call_id'] is None

    def test_parse_input(self):
        """Test parsing input arguments."""
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello!'},
        ]

        kwargs = {
            'messages': messages,
            'model': 'test-model',
            'temperature': 0.7,
            'top_p': 1.0,
            'max_tokens': 100,
            'ignore_this': 'value',  # This should be ignored
        }

        result = OpenAIUtils.parse_input(**kwargs)

        # Check structure
        assert 'model_name' in result
        assert 'input' in result
        assert 'extra' in result

        # Check values
        assert result['model_name'] == 'test-model'
        assert len(result['input']) == 2

        # Check monitored parameters
        assert 'temperature' in result['extra']
        assert result['extra']['temperature'] == 0.7
        assert 'top_p' in result['extra']
        assert result['extra']['top_p'] == 1.0
        assert 'max_tokens' in result['extra']
        assert result['extra']['max_tokens'] == 100

        # Check that non-monitored parameters are ignored
        assert 'ignore_this' not in result['extra']

    def test_parse_input_with_engine_fallback(self):
        """Test parsing input with engine fallback for model name."""
        messages = [{'role': 'user', 'content': 'Hello'}]

        # Test with engine instead of model
        kwargs1 = {'messages': messages, 'engine': 'engine-model'}
        result1 = OpenAIUtils.parse_input(**kwargs1)
        assert result1['model_name'] == 'engine-model'

        # Test with deployment_id
        kwargs2 = {'messages': messages, 'deployment_id': 'deployment-model'}
        result2 = OpenAIUtils.parse_input(**kwargs2)
        assert result2['model_name'] == 'deployment-model'

        # Test priority (model > engine > deployment_id)
        kwargs3 = {
            'messages': messages,
            'model': 'primary-model',
            'engine': 'engine-model',
            'deployment_id': 'deployment-model',
        }
        result3 = OpenAIUtils.parse_input(**kwargs3)
        assert result3['model_name'] == 'primary-model'

    def test_parse_output(self):
        """Test parsing output."""
        # Create a mock output object
        output = MagicMock()
        output.choices = [MagicMock()]
        output.choices[0].message = {'role': 'assistant', 'content': 'Hello, how can I help you?'}
        output.usage.completion_tokens = 10
        output.usage.prompt_tokens = 20

        result = OpenAIUtils.parse_output(output)

        # Check structure
        assert 'output' in result
        assert 'tokensUsage' in result

        # Check values
        assert result['output']['role'] == 'assistant'
        assert result['output']['content'] == 'Hello, how can I help you?'
        assert result['tokensUsage']['completion'] == 10
        assert result['tokensUsage']['prompt'] == 20

    def test_parse_output_with_exception(self, caplog):
        """Test parsing output when an exception occurs."""
        with caplog.at_level(logging.INFO):
            # Create a mock output that will cause an exception
            output = MagicMock()
            # Set up to raise an exception when accessed
            type(output).choices = RuntimeError('Test exception')

            result = OpenAIUtils.parse_output(output)

            # Check that the result is None (as per implementation)
            assert result is None

            # Check that error was logged
            assert 'Error parsing output' in caplog.text

    def test_parse_output_with_complex_message(self):
        """Test parsing output with a complex message structure."""
        # Create a mock output with a more complex message
        output = MagicMock()
        output.choices = [MagicMock()]
        output.choices[0].message = {
            'role': 'assistant',
            'content': None,  # Content can be None when tool calls are present
            'tool_calls': [
                {
                    'id': 'call_123',
                    'type': 'function',
                    'function': {'name': 'get_weather', 'arguments': '{"location": "New York"}'},
                }
            ],
        }
        output.usage.completion_tokens = 15
        output.usage.prompt_tokens = 25

        result = OpenAIUtils.parse_output(output)

        # Check parsed values
        assert result['output']['role'] == 'assistant'
        assert result['output']['content'] is None
        assert len(result['output']['tool_calls']) == 1
        assert result['output']['tool_calls'][0]['id'] == 'call_123'
        assert result['tokensUsage']['completion'] == 15
        assert result['tokensUsage']['prompt'] == 25

    def test_parse_output_missing_usage(self):
        """Test parsing output when usage information is missing."""

        # Create a custom class with no usage attribute
        class OutputWithoutUsage:
            def __init__(self):
                self.choices = [MagicMock()]
                self.choices[0].message = {'role': 'assistant', 'content': 'Hello'}
                # No usage attribute

        output = OutputWithoutUsage()

        with patch('logging.info') as mock_log:
            result = OpenAIUtils.parse_output(output)

            # Should handle the missing attribute gracefully
            assert result is None
            mock_log.assert_called()

    def test_parse_output_empty_choices(self):
        """Test parsing output with empty choices array."""
        # Create a mock output with empty choices
        output = MagicMock()
        output.choices = []
        output.usage.completion_tokens = 10
        output.usage.prompt_tokens = 20

        with patch('logging.info') as mock_log:
            result = OpenAIUtils.parse_output(output)

            # Should handle the empty choices gracefully
            assert result is None
            mock_log.assert_called()

    def test_parse_output_with_stream(self):
        """Test parse_output with stream parameter."""
        # Create a mock output object
        output = MagicMock()
        output.choices = [MagicMock()]
        output.choices[0].message = {'role': 'assistant', 'content': 'Hello'}
        output.usage.completion_tokens = 10
        output.usage.prompt_tokens = 20

        # Call with stream=True
        result = OpenAIUtils.parse_output(output, stream=True)

        # Should handle stream parameter properly
        assert result is not None
        assert 'output' in result
        assert 'tokensUsage' in result
