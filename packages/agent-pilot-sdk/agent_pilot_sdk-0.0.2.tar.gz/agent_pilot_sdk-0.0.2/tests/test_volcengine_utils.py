from unittest.mock import MagicMock
import logging

from agent_pilot.volcengine_utils import VolcengineUtils


class TestVolcengineUtils:
    def test_parse_role_assistant(self):
        """Test that 'assistant' role is parsed to 'ai'."""
        assert VolcengineUtils.parse_role('assistant') == 'ai'

    def test_parse_role_other(self):
        """Test that other roles remain unchanged."""
        assert VolcengineUtils.parse_role('user') == 'user'
        assert VolcengineUtils.parse_role('system') == 'system'

    def test_get_property_from_dict(self):
        """Test getting property from a dictionary."""
        test_dict = {'key1': 'value1', 'key2': 'value2'}

        assert VolcengineUtils.get_property(test_dict, 'key1') == 'value1'
        assert VolcengineUtils.get_property(test_dict, 'key2') == 'value2'
        assert VolcengineUtils.get_property(test_dict, 'key3') is None

    def test_get_property_from_object(self):
        """Test getting property from an object."""

        class TestObject:
            attr1 = 'value1'
            attr2 = 'value2'

        test_obj = TestObject()

        assert VolcengineUtils.get_property(test_obj, 'attr1') == 'value1'
        assert VolcengineUtils.get_property(test_obj, 'attr2') == 'value2'
        assert VolcengineUtils.get_property(test_obj, 'attr3') is None

    def test_parse_message_dict(self):
        """Test parsing a message from dictionary."""
        test_message = {
            'role': 'user',
            'content': 'Hello, world!',
            'reasoning_content': 'Some reasoning',
            'tool_calls': [{'type': 'function', 'id': '123'}],
            'tool_call_id': '123',
        }

        parsed = VolcengineUtils.parse_message(test_message)

        assert parsed['role'] == 'user'
        assert parsed['content'] == 'Hello, world!'
        assert parsed['reasoning_content'] == 'Some reasoning'
        assert parsed['tool_calls'] == [{'type': 'function', 'id': '123'}]
        assert parsed['tool_call_id'] == '123'

    def test_parse_message_object(self):
        """Test parsing a message from object."""

        class Message:
            def __init__(self):
                self.role = 'system'
                self.content = 'System message'
                self.reasoning_content = None
                self.tool_calls = None
                self.tool_call_id = None

        test_message = Message()
        parsed = VolcengineUtils.parse_message(test_message)

        assert parsed['role'] == 'system'
        assert parsed['content'] == 'System message'
        assert parsed['reasoning_content'] is None
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

        result = VolcengineUtils.parse_input(**kwargs)

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

    def test_parse_output(self):
        """Test parsing output."""
        # Create a mock output object
        output = MagicMock()
        output.choices = [MagicMock()]
        output.choices[0].message = {'role': 'assistant', 'content': 'Hello, how can I help you?'}
        output.usage.completion_tokens = 10
        output.usage.prompt_tokens = 20

        result = VolcengineUtils.parse_output(output)

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

            result = VolcengineUtils.parse_output(output)

            # Check that default values are returned
            assert result['output'] == {}
            assert result['tokensUsage']['completion'] == 0
            assert result['tokensUsage']['prompt'] == 0

            # Check that error was logged
            assert 'Error parsing output' in caplog.text
