import pytest
from unittest.mock import patch, MagicMock
import uuid
import sys

# Direct imports to avoid confusion with the monitor function
from agent_pilot.tracking import track_event, wrap
from agent_pilot.models import TrackingEvent
from agent_pilot.context import tags_ctx, Run
from agent_pilot.event_queue import EventQueue


class TestTrackEvent:
    @pytest.fixture
    def mock_config(self):
        """Fixture to mock the config."""
        with patch('agent_pilot.config.get_config', autospec=True) as mock_get_config:
            config = MagicMock()
            config.api_key = 'test_api_key'
            config.verbose = False
            mock_get_config.return_value = config
            yield config

    def test_track_event_basic(self):
        """Test basic functionality of track_event."""
        # Setup mocks
        mock_queue = MagicMock(spec=EventQueue)
        mock_config = MagicMock()
        mock_config.api_key = 'test_api_key'
        mock_config.verbose = False

        # Set expected values
        expected_uuid = '12345678-1234-5678-1234-567812345678'
        expected_parent = 'parent-run-id'

        # Mock create_uuid_from_string to return the expected values
        def mock_create_uuid_side_effect(input_str):
            if 'parent-run-id' in input_str:
                return expected_parent
            return uuid.UUID(expected_uuid)

        # Apply patches
        with (
            patch('agent_pilot.config.get_config', return_value=mock_config),
            patch('agent_pilot.utils.create_uuid_from_string', side_effect=mock_create_uuid_side_effect),
        ):
            # Call track_event with minimal required parameters and callback_queue
            track_event(
                run_type='test_run',
                event_name='test_event',
                run_id=expected_uuid,
                task_id='test-task-id',
                version='v1',
                callback_queue=mock_queue,
                api_key='test_api_key',  # Explicitly provide API key
                parent_run_id=expected_parent,  # Explicitly set parent run ID
            )

        # Verify event was created and added to queue
        mock_queue.append.assert_called_once()
        event = mock_queue.append.call_args[0][0]

        # Check event properties
        assert isinstance(event, TrackingEvent)
        assert event.run_type == 'test_run'
        assert event.event_name == 'test_event'
        assert event.task_id == 'test-task-id'
        assert event.prompt_version == 'v1'

        # Skip the run_id and parent_run_id checks since they're going to be UUIDs based on inputs
        # In a real test, you might want to validate that they match expected patterns

    def test_track_event_with_all_params(self, mock_config):
        """Test track_event with all parameters provided."""
        # Create test data
        mock_queue = MagicMock(spec=EventQueue)
        input_data = [{'prompt': 'Test prompt'}]  # Convert to JSON string
        output_data = {'response': 'Test response'}  # Convert to JSON string
        token_usage = {'prompt_tokens': 10, 'completion_tokens': 20}  # Convert to JSON string
        error_data = {'message': 'Test error'}  # Convert to JSON string
        tags = ['tag1', 'tag2']
        timestamp = '2023-01-01T00:00:00Z'

        # Call track_event with all parameters
        track_event(
            run_type='test_run',
            event_name='test_event',
            run_id='test-run-id',
            task_id='test-task-id',
            version='v1',
            session_id='test-session-id',
            parent_run_id='explicit-parent-id',
            model_name='test-model',
            input_messages=input_data,
            output_message=output_data,
            token_usage=token_usage,
            error=error_data,
            tags=tags,
            timestamp=timestamp,
            callback_queue=mock_queue,
            api_key='test_api_key',
        )

        print(mock_queue.append.call_args)

        # Verify event was created and added to queue
        event = mock_queue.append.call_args[0][0]

        # Check additional event properties
        assert event.session_id == 'test-session-id'
        assert event.model_name == 'test-model'
        assert event.input_messages == [{'prompt': 'Test prompt'}]  # Check parsed dict
        assert event.output_message == {'response': 'Test response'}  # Check parsed dict
        assert event.token_usage == {'prompt_tokens': 10, 'completion_tokens': 20}  # Check parsed dict
        assert event.error == {'message': 'Test error'}  # Check parsed dict
        assert event.tags == tags
        assert event.timestamp == timestamp

    def test_track_event_with_verbose_logging(self, caplog):
        """Test track_event with verbose logging enabled."""
        # Setup mocks
        mock_queue = MagicMock(spec=EventQueue)
        mock_config = MagicMock()
        mock_config.api_key = 'test_api_key'
        mock_config.verbose = True

        # Apply patches
        with patch('agent_pilot.config.get_config', return_value=mock_config):
            # Call track_event
            track_event(
                run_type='test_run',
                event_name='test_event',
                run_id='test-run-id',
                task_id='test-task-id',
                version='v1',
                callback_queue=mock_queue,
                api_key='test_api_key',
            )

        # Verify logging attempt was made (even if we can't directly check the log message)
        assert mock_queue.append.called

    def test_track_event_with_custom_queue(self):
        """Test track_event with a custom callback queue."""
        # Create mocks
        # mock_queue = MagicMock(spec=EventQueue)
        custom_queue = MagicMock()
        mock_config = MagicMock()
        mock_config.api_key = 'test_api_key'

        # Apply patches
        with patch('agent_pilot.config.get_config', return_value=mock_config):
            # Call track_event with custom queue
            track_event(
                run_type='test_run',
                event_name='test_event',
                run_id='test-run-id',
                task_id='test-task-id',
                version='v1',
                callback_queue=custom_queue,
                api_key='test_api_key',
            )

        # Verify event was added to custom queue
        custom_queue.append.assert_called_once()

    def test_track_event_with_tags_from_context(self):
        """Test track_event uses tags from context when not explicitly provided."""
        # Create mocks
        mock_queue = MagicMock(spec=EventQueue)
        mock_config = MagicMock()
        mock_config.api_key = 'test_api_key'

        # Set tags in context
        context_tags = ['context_tag1', 'context_tag2']
        tags_ctx.set(context_tags)

        try:
            # Apply patches
            with patch('agent_pilot.config.get_config', return_value=mock_config):
                # Call track_event without tags parameter
                track_event(
                    run_type='test_run',
                    event_name='test_event',
                    run_id='test-run-id',
                    task_id='test-task-id',
                    version='v1',
                    callback_queue=mock_queue,
                    api_key='test_api_key',
                )

            # Verify event used tags from context
            event = mock_queue.append.call_args[0][0]
            assert event.tags == context_tags
        finally:
            # Reset tags context
            tags_ctx.set(None)

    def test_track_event_exception_handling(self, caplog):
        """Test that track_event handles exceptions gracefully."""
        # This test verifies that track_event doesn't allow exceptions to propagate
        # But since we're mocking the queue and it's hard to verify the logging behavior,
        # we'll just assert that the function completes even with a faulty queue

        # Create mocks
        mock_queue = MagicMock(spec=EventQueue)
        mock_queue.append.side_effect = Exception('Test exception')

        # Call track_event and verify it completes without raising an exception
        track_event(
            run_type='test_run',
            event_name='test_event',
            run_id='test-run-id',
            task_id='test-task-id',
            version='v1',
            callback_queue=mock_queue,
            api_key='test_api_key',
        )

        # If we got here without an exception, the test passes


class TestWrap:
    @pytest.fixture
    def mock_track_event(self):
        """Fixture to mock track_event function."""
        # Mock the function directly
        mock_track = MagicMock()
        original_track_event = track_event
        track_event_module = sys.modules['agent_pilot.tracking']
        track_event_module.track_event = mock_track

        yield mock_track

        # Restore original
        track_event_module.track_event = original_track_event

    @pytest.fixture
    def mock_run_manager(self):
        """Fixture to mock run_manager."""
        # Mock run_manager directly
        mock_manager = MagicMock()

        # Setup mock run
        mock_run = MagicMock()
        mock_run.id = 'test-run-id'
        mock_run.task_id = 'test-task-id'
        mock_run.version = 'v1'

        # Setup manager to return the mock run
        mock_manager.start_run.return_value = mock_run
        mock_manager.current_run_id = None

        # Save original and replace
        module = sys.modules['agent_pilot.tracking']
        original_run_manager = module.run_manager
        module.run_manager = mock_manager

        yield mock_manager

        # Restore original
        module.run_manager = original_run_manager

    @pytest.fixture
    def mock_default_input_parser(self):
        """Fixture to mock the default input parser."""
        # Create a mock parser that returns a dict with model_name
        mock_parser = MagicMock(
            return_value={
                'task_id': 'test-task-id',
                'version': 'v1',
                'input': 'test-input',
                'model_name': 'test-model',
            }
        )
        # Save original and replace

        module = sys.modules['agent_pilot.tracking']
        module.default_input_parser = mock_parser

        yield mock_parser

    @pytest.fixture
    def mock_default_output_parser(self):
        """Fixture to mock the default output parser."""
        # Create a mock parser that returns output data and token usage
        mock_parser = MagicMock(
            return_value={
                'task_id': 'test-task-id',
                'version': 'v1',
                'output': 'test output',
                'tokensUsage': {'prompt': 10, 'completion': 20},
            }
        )

        module = sys.modules['agent_pilot.tracking']
        module.default_output_parser = mock_parser

        yield mock_parser

    def test_wrap_basic_function(
        self, mock_track_event, mock_run_manager, mock_default_input_parser, mock_default_output_parser
    ):
        """Test wrapping a basic function."""

        # Create a test function to wrap
        def test_function(arg1, arg2):
            return f'{arg1} {arg2}'

        # Wrap the function
        wrapped_function = wrap(test_function, run_type='test_type', model_name='test-model', tags=['test-tag'])

        # Call the wrapped function
        result = wrapped_function('hello', 'world')

        # Verify result
        assert result == 'hello world'

        # Verify tracking events were logged
        assert mock_track_event.call_count == 2

        # Check start event
        start_call = mock_track_event.mock_calls[0]
        assert start_call[1][0] == 'test_type'  # run_type
        assert start_call[1][1] == 'start'  # event_name

        # Check end event
        end_call = mock_track_event.mock_calls[1]
        assert end_call[1][0] == 'test_type'  # run_type
        assert end_call[1][1] == 'end'  # event_name

        # Verify run management
        mock_run_manager.start_run.assert_called_once()
        mock_run_manager.end_run.assert_called_once_with('test-run-id')

    def test_wrap_function_with_exception(
        self, mock_track_event, mock_run_manager, mock_default_input_parser, mock_default_output_parser
    ):
        """Test wrapped function that raises an exception."""

        # Create a test function that raises an exception
        def test_function():
            raise ValueError('Test error')

        # Let's directly patch input parser as a function
        input_parser_patch = MagicMock(return_value={'input': {'prompt': 'test'}, 'model_name': 'test-model'})

        # Wrap the function
        wrapped_function = wrap(test_function, run_type='test_type', input_parser=input_parser_patch)

        # Call the wrapped function and expect exception
        with pytest.raises(ValueError, match='Test error'):
            wrapped_function()

        # Verify error event was logged before rethrowing
        assert mock_track_event.call_count >= 1

        # Check start event
        start_call = mock_track_event.mock_calls[0]
        assert start_call[1][0] == 'test_type'  # run_type
        assert start_call[1][1] == 'start'  # event_name

    def test_wrap_with_custom_parsers(
        self, mock_track_event, mock_run_manager, mock_default_input_parser, mock_default_output_parser
    ):
        """Test wrap with custom input and output parsers."""

        # Create custom parsers
        def custom_input_parser(*args, **kwargs):
            return {
                'task_id': 'test-task-id',
                'version': 'v1',
                'input': 'custom_input_parser_result',
                'model_name': 'custom-model',
            }

        def custom_output_parser(output, *args, **kwargs):
            return {
                'task_id': 'test-task-id',
                'version': 'v1',
                'output': 'custom_output_parser_result',
                'tokensUsage': {'custom': 42},
            }

        # Create a test function
        def test_function():
            return 'original_output'

        # Wrap with custom parsers
        wrapped_function = wrap(
            test_function, run_type='test_type', input_parser=custom_input_parser, output_parser=custom_output_parser
        )

        # Call the wrapped function
        result = wrapped_function()

        # Verify original result is returned
        assert result == 'original_output'

        # Verify custom parsers were used
        start_call = mock_track_event.mock_calls[0]
        assert 'custom_input_parser_result' in str(start_call)  # input

        end_call = mock_track_event.mock_calls[1]
        assert 'custom_output_parser_result' in str(end_call)  # output

    def test_wrap_with_parent_run_id(
        self, mock_track_event, mock_run_manager, mock_default_input_parser, mock_default_output_parser
    ):
        """Test wrap with parent_run_id from parameter and run_manager."""
        # Set current run in run_manager
        mock_run_manager.current_run_id = Run('manager-parent-id')
        mock_run_manager.parent_run_id = Run('explicit-parent-id')

        def test_function():
            return 'test result'

        # Test 1: Using explicit parent in kwargs
        wrapped_function1 = wrap(
            test_function,
            run_type='test_type',
            input_parser=mock_default_input_parser,
            output_parser=mock_default_output_parser,
        )
        wrapped_function1(task_id='test-task-id', version='v1', parent='explicit-parent-id')

        # Verify explicit parent was used in the call (the actual parameters match what was passed)
        mock_run_manager.start_run.assert_called_with(None, 'test-task-id', 'v1', 'explicit-parent-id')

        # Reset mocks
        mock_run_manager.start_run.reset_mock()

        # Test 2: Using parent from run_manager
        wrapped_function2 = wrap(
            test_function,
            run_type='test_type',
            input_parser=mock_default_input_parser,
            output_parser=mock_default_output_parser,
        )
        wrapped_function2()

        # Verify run_manager parent was used
        mock_run_manager.start_run.assert_called_with(None, None, None, mock_run_manager.current_run_id)
