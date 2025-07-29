import pytest
from unittest.mock import patch, MagicMock
import threading
import requests
import logging

from agent_pilot.consumer import Consumer
from agent_pilot.models import TrackingEvent


class TestConsumer:
    @pytest.fixture
    def mock_event_queue(self):
        """Fixture to create a mock event queue."""
        mock_queue = MagicMock()
        mock_queue.get_batch.return_value = []  # Default to empty batch
        return mock_queue

    @pytest.fixture
    def mock_config(self):
        """Fixture to mock the config."""
        with patch('agent_pilot.consumer.get_config') as mock_get_config:
            config = MagicMock()
            config.api_key = 'test_api_key'
            config.api_url = 'http://test-api-url.com'
            config.verbose = False
            config.ssl_verify = True
            config.local_debug = False
            mock_get_config.return_value = config
            yield config

    @pytest.fixture
    def sample_events(self):
        """Fixture to create sample events."""
        return [
            TrackingEvent(
                run_type='test_run_1',
                event_name='test_event_1',
                run_id='test_run_id_1',
                task_id='test_task_id_1',
                prompt_version='v1',
            ),
            TrackingEvent(
                run_type='test_run_2',
                event_name='test_event_2',
                run_id='test_run_id_2',
                task_id='test_task_id_2',
                prompt_version='v2',
            ),
        ]

    def test_consumer_initialization(self, mock_event_queue):
        """Test proper initialization of Consumer."""
        with patch('agent_pilot.consumer.atexit.register') as mock_register:
            consumer = Consumer(mock_event_queue, api_key='custom_api_key')

            # Verify attributes
            assert consumer.running is True
            assert consumer.event_queue is mock_event_queue
            assert consumer.api_key == 'custom_api_key'
            assert isinstance(consumer, threading.Thread)
            assert consumer.daemon is True

            # Verify atexit registration
            mock_register.assert_called_once_with(consumer.stop)

    def test_consumer_run(self, mock_event_queue):
        """Test the run method of Consumer."""
        with patch.object(Consumer, 'send_batch') as mock_send_batch, patch('time.sleep') as mock_sleep:
            consumer = Consumer(mock_event_queue)

            # Setup to run for a short time then stop
            def stop_after_calls(*args, **kwargs):
                nonlocal mock_send_batch
                if mock_send_batch.call_count >= 3:
                    consumer.running = False

            mock_send_batch.side_effect = stop_after_calls

            # Run the consumer
            consumer.run()

            # Verify send_batch was called multiple times
            assert mock_send_batch.call_count >= 3
            # Verify sleep was called between batches
            assert mock_sleep.call_count >= 2

    def test_send_batch_no_events(self, mock_event_queue, mock_config):
        """Test send_batch with no events."""
        with patch('requests.post') as mock_post:
            mock_event_queue.get_batch.return_value = []

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify no API call was made
            mock_post.assert_not_called()

    def test_send_batch_with_events(self, mock_event_queue, mock_config, sample_events):
        """Test send_batch with events."""
        with patch('requests.post') as mock_post:
            # Setup successful response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            # Return sample events from queue
            mock_event_queue.get_batch.return_value = sample_events

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify API call was made with correct data
            mock_post.assert_called_once()
            kwargs = mock_post.call_args[1]

            # Check headers
            assert kwargs['headers']['Authorization'] == f'Bearer {mock_config.api_key}'
            assert kwargs['headers']['Content-Type'] == 'application/json'

            # Check payload
            assert 'TrackingEvents' in kwargs['json']
            assert len(kwargs['json']['TrackingEvents']) == 2

    def test_send_batch_no_api_key(self, mock_event_queue, mock_config, sample_events, caplog):
        """Test send_batch behavior when no API key is available."""
        with patch('requests.post') as mock_post, caplog.at_level(logging.ERROR):
            # Set API key to None
            mock_config.api_key = None

            # Return sample events from queue
            mock_event_queue.get_batch.return_value = sample_events

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify error was logged
            assert 'API key not found' in caplog.text

            # Verify no API call was made
            mock_post.assert_not_called()

    def test_send_batch_request_error(self, mock_event_queue, mock_config, sample_events, caplog):
        """Test send_batch handling of request errors."""
        with patch('requests.post') as mock_post, caplog.at_level(logging.ERROR):
            # Setup request to raise exception
            mock_post.side_effect = requests.exceptions.RequestException('Test error')

            # Return sample events from queue
            mock_event_queue.get_batch.return_value = sample_events

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify error was logged
            assert 'Error sending events' in caplog.text

            # Verify events were put back in the queue
            mock_event_queue.append.assert_called_once_with(sample_events)

    def test_send_batch_verbose_logging(self, mock_event_queue, mock_config, sample_events, caplog):
        """Test verbose logging in send_batch."""
        with patch('requests.post') as mock_post, caplog.at_level(logging.INFO):
            # Enable verbose logging
            mock_config.verbose = True

            # Setup successful response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            # Return sample events from queue
            mock_event_queue.get_batch.return_value = sample_events

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify informational messages were logged
            assert f'Sending {len(sample_events)} events' in caplog.text

    def test_send_batch_with_local_debug(self, mock_event_queue, mock_config, sample_events):
        """Test send_batch with local_debug enabled."""
        with patch('requests.post') as mock_post:
            # Enable local_debug
            mock_config.local_debug = True

            # Setup successful response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            # Return sample events from queue
            mock_event_queue.get_batch.return_value = sample_events

            consumer = Consumer(mock_event_queue)
            consumer.send_batch()

            # Verify API call was made with correct local debug headers
            mock_post.assert_called_once()
            kwargs = mock_post.call_args[1]

            # Check headers for local debug
            assert 'Authorization' in kwargs['headers']

    def test_stop(self, mock_event_queue):
        """Test the stop method of Consumer."""
        consumer = Consumer(mock_event_queue)
        consumer.stop()

        # Verify the consumer was stopped
        assert consumer.running is False
