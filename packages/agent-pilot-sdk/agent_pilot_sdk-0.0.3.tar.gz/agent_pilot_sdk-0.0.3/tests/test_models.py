import pytest
from pydantic import ValidationError
import json

from agent_pilot.models import TrackingEvent, PromptVersion


class TestTrackingEvent:
    def test_tracking_event_required_fields(self):
        """Test TrackingEvent creation with only required fields."""
        event = TrackingEvent(
            run_type='test_run',
            event_name='test_event',
            run_id='test_run_123',
            task_id='test_task_456',
            prompt_version='v1',
        )

        assert event.run_type == 'test_run'
        assert event.event_name == 'test_event'
        assert event.run_id == 'test_run_123'
        assert event.task_id == 'test_task_456'
        assert event.prompt_version == 'v1'

        # Optional fields should be None
        assert event.session_id is None
        assert event.parent_run_id is None
        assert event.model_name is None
        assert event.input_messages is None
        assert event.output_message is None
        assert event.prompt_template is None
        assert event.variables is None
        assert event.error is None
        assert event.token_usage is None
        assert event.tags is None
        assert event.params is None
        assert event.properties is None
        assert event.timestamp is None

    def test_tracking_event_all_fields(self):
        """Test TrackingEvent creation with all fields."""
        input_data = [{'prompt': 'Test prompt'}]
        output_data = {'response': 'Test response'}
        error_data = {'message': 'Test error'}
        token_usage_data = {'prompt_tokens': 10, 'completion_tokens': 20, 'total_tokens': 30}

        event = TrackingEvent(
            run_type='test_run',
            event_name='test_event',
            run_id='test_run_123',
            task_id='test_task_456',
            prompt_version='v1',
            session_id='test_session_789',
            parent_run_id='parent_run_123',
            model_name='test-model',
            input_messages=input_data,
            output_message=output_data,
            prompt_template=[{'role': 'system', 'content': 'You are a test assistant'}],
            variables={'name': 'Test User'},
            error=error_data,
            token_usage=token_usage_data,
            tags=['test', 'dev'],
            params={'temperature': 0.7},
            properties={'source': 'unit_test'},
            timestamp='2023-05-01T12:00:00Z',
        )

        # Verify all fields
        assert event.run_type == 'test_run'
        assert event.event_name == 'test_event'
        assert event.run_id == 'test_run_123'
        assert event.task_id == 'test_task_456'
        assert event.prompt_version == 'v1'
        assert event.session_id == 'test_session_789'
        assert event.parent_run_id == 'parent_run_123'
        assert event.model_name == 'test-model'
        assert event.input_messages == input_data
        assert event.output_message == output_data
        assert event.prompt_template == [{'role': 'system', 'content': 'You are a test assistant'}]
        assert event.variables == {'name': 'Test User'}
        assert event.error == error_data
        assert event.token_usage == token_usage_data
        assert event.tags == ['test', 'dev']
        assert event.params == {'temperature': 0.7}
        assert event.properties == {'source': 'unit_test'}
        assert event.timestamp == '2023-05-01T12:00:00Z'

    def test_tracking_event_missing_required_fields(self):
        """Test TrackingEvent creation with missing required fields raises error."""
        with pytest.raises(ValidationError):
            TrackingEvent(
                run_type='test_run',
                # Missing event_name
                run_id='test_run_123',
                task_id='test_task_456',
                prompt_version='v1',
            )

    def test_tracking_event_json_serialization(self):
        """Test TrackingEvent can be properly serialized to JSON."""
        input_data = [{'prompt': 'Test prompt'}]
        output_data = {'response': 'Test response'}

        event = TrackingEvent(
            run_type='test_run',
            event_name='test_event',
            run_id='test_run_123',
            task_id='test_task_456',
            prompt_version='v1',
            input_messages=input_data,
            output_message=output_data,
        )

        # Convert to JSON
        event_json = event.model_dump_json()
        event_dict = json.loads(event_json)

        # Verify JSON has expected fields
        assert event_dict['run_type'] == 'test_run'
        assert event_dict['event_name'] == 'test_event'
        assert event_dict['run_id'] == 'test_run_123'
        assert event_dict['task_id'] == 'test_task_456'
        assert event_dict['prompt_version'] == 'v1'
        assert event_dict['input_messages'] == input_data
        assert event_dict['output_message'] == output_data

        # Optional fields should be None
        assert event_dict.get('session_id') is None


class TestPromptVersion:
    def test_prompt_version_creation(self):
        """Test PromptVersion creation with required fields."""
        prompt_version = PromptVersion(
            task_id='test-task-456',
            version='v1',
            model_name='test-model',
            temperature=0.7,
            top_p=1.0,
        )

        assert prompt_version.task_id == 'test-task-456'
        assert prompt_version.version == 'v1'
        assert prompt_version.model_name == 'test-model'
        assert prompt_version.temperature == 0.7
        assert prompt_version.top_p == 1.0
        assert prompt_version.messages is None
        assert prompt_version.variable_names is None

    def test_prompt_version_with_all_fields(self):
        """Test PromptVersion creation with all fields."""
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello!'},
        ]

        prompt_version = PromptVersion(
            task_id='test-task-456',
            version='v1',
            messages=messages,
            variable_names=['test_vars'],
            model_name='test-model',
            temperature=0.7,
            top_p=1.0,
        )

        assert prompt_version.task_id == 'test-task-456'
        assert prompt_version.version == 'v1'
        assert prompt_version.messages == messages
        assert prompt_version.variable_names == ['test_vars']
        assert prompt_version.model_name == 'test-model'
        assert prompt_version.temperature == 0.7
        assert prompt_version.top_p == 1.0

    def test_prompt_version_missing_required_fields(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            PromptVersion(
                prompt_version_id='test-pvid-123',
                task_id='test-task-456',
                version='v1',
                # Missing model_name, temperature, top_p
            )

    def test_prompt_version_json_serialization(self):
        """Test PromptVersion can be properly serialized to JSON."""
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello!'},
        ]

        prompt_version = PromptVersion(
            task_id='test-task-456',
            version='v1',
            messages=messages,
            variable_names=['test_vars'],
            model_name='test-model',
            temperature=0.7,
            top_p=1.0,
        )

        # Convert to JSON
        prompt_version_json = prompt_version.model_dump_json()
        prompt_version_dict = json.loads(prompt_version_json)

        # Verify JSON has expected fields
        assert prompt_version_dict['task_id'] == 'test-task-456'
        assert prompt_version_dict['version'] == 'v1'
        assert prompt_version_dict['messages'] == messages
        assert prompt_version_dict['variable_names'] == ['test_vars']
        assert prompt_version_dict['model_name'] == 'test-model'
        assert prompt_version_dict['temperature'] == 0.7
        assert prompt_version_dict['top_p'] == 1.0
