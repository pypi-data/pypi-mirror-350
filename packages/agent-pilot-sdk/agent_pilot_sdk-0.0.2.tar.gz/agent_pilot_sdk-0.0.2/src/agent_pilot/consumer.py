import time
import atexit
import logging
from threading import Thread
from typing import Optional, Any
from .config import get_config
from .models import TrackingEvent
from .http_client import get_http_client

logger = logging.getLogger(__name__)


class Consumer(Thread):
    def __init__(self, event_queue: Any, api_key: Optional[str] = None) -> None:
        self.running = True
        self.event_queue = event_queue
        self.api_key = api_key
        self.http_client = get_http_client()

        Thread.__init__(self, daemon=True)
        atexit.register(self.stop)

    def run(self) -> None:
        while self.running:
            self.send_batch()
            time.sleep(0.5)

        self.send_batch()

    def send_batch(self) -> None:
        config = get_config()
        batch: list[TrackingEvent] = self.event_queue.get_batch()

        verbose = config.verbose
        api_url = config.api_url

        if len(batch) > 0:
            api_key = self.api_key or config.api_key
            if not config.local_debug and not api_key:
                return logger.error('API key not found. Please provide an API key.')

            if verbose:
                logger.info(f'Sending {len(batch)} events.')
                for event in batch:
                    logger.info(f'event {event.run_id}: {event.model_dump()}')

            try:
                if verbose:
                    logger.info('Sending events to ', api_url)
                task_id = batch[0].task_id
                data = {'TaskId': task_id, 'TrackingEvents': [event.model_dump() for event in batch]}

                if verbose:
                    logger.info(f'Sending data: {data}')

                action = 'TrackingEvent'
                response_data, response_status_code = self.http_client.post(
                    action=action, data=data, api_key=api_key, api_url=api_url
                )

                if verbose:
                    logger.info(
                        f'Events sent. response_data: {response_data}, response_status_code: {response_status_code}'
                    )
            except Exception as e:
                if verbose:
                    logger.exception(f'Error sending events: {e}')
                else:
                    logger.error('Error sending events')

                self.event_queue.append(batch)

    def stop(self) -> None:
        self.running = False
        if self.running and self.is_alive():
            self.join()
