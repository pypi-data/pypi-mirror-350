import pytest
from unittest.mock import patch, MagicMock
import threading
import time

from agent_pilot.event_queue import EventQueue
from agent_pilot.models import TrackingEvent


class TestEventQueue:
    @pytest.fixture
    def mock_consumer(self):
        """Fixture to mock the Consumer class."""
        with patch('agent_pilot.event_queue.Consumer') as mock_consumer_class:
            mock_consumer_instance = MagicMock()
            mock_consumer_class.return_value = mock_consumer_instance
            yield mock_consumer_instance

    @pytest.fixture
    def sample_event(self):
        """Fixture to create a sample TrackingEvent."""
        return TrackingEvent(
            run_type='test_run',
            event_name='test_event',
            run_id='test_run_123',
            task_id='test_task_456',
            prompt_version='v1',
        )

    def test_event_queue_initialization(self, mock_consumer):
        """Test that EventQueue initializes properly."""
        queue = EventQueue()

        # Verify the queue state
        assert isinstance(queue.lock, type(threading.Lock()))
        assert queue.events == []

        # Verify Consumer was created and started
        mock_consumer.start.assert_called_once()

    def test_append_single_event(self, mock_consumer, sample_event):
        """Test appending a single event to the queue."""
        queue = EventQueue()
        queue.append(sample_event)

        assert len(queue.events) == 1
        assert queue.events[0] == sample_event

    def test_append_multiple_events(self, mock_consumer, sample_event):
        """Test appending multiple events as a list."""
        queue = EventQueue()

        # Create multiple events
        events = [sample_event, sample_event, sample_event]
        queue.append(events)

        assert len(queue.events) == 3
        assert queue.events == events

    def test_get_batch_no_contention(self, mock_consumer, sample_event):
        """Test getting a batch of events with no lock contention."""
        queue = EventQueue()

        # Add some events
        queue.append(sample_event)
        queue.append(sample_event)

        # Get the batch
        batch = queue.get_batch()

        # Verify the batch contains the events and the queue is now empty
        assert len(batch) == 2
        assert batch[0] == sample_event
        assert batch[1] == sample_event
        assert queue.events == []

    def test_get_batch_with_contention(self, mock_consumer):
        """Test getting a batch when the lock is already held."""
        queue = EventQueue()

        # Acquire the lock to simulate contention
        queue.lock.acquire()

        try:
            # Try to get a batch while the lock is held
            batch = queue.get_batch()

            # Verify an empty batch is returned
            assert batch == []
        finally:
            # Release the lock
            queue.lock.release()

    def test_thread_safety(self, mock_consumer, sample_event):
        """Test thread safety of the EventQueue."""
        queue = EventQueue()

        # Number of events to add per thread
        events_per_thread = 100

        # Function to add events in a separate thread
        def add_events():
            for _ in range(events_per_thread):
                queue.append(sample_event)
                # Small sleep to increase chance of thread interleaving
                time.sleep(0.001)

        # Create and start multiple threads
        threads = []
        for _ in range(5):  # 5 threads
            thread = threading.Thread(target=add_events)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Get all events
        all_events = queue.get_batch()

        # Verify all events were added
        assert len(all_events) == events_per_thread * 5
