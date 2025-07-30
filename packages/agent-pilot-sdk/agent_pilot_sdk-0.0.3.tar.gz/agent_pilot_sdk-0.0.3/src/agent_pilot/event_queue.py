import threading
from typing import List, Union, TypeVar, Any
from agent_pilot.consumer import Consumer

T = TypeVar('T')


class EventQueue:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.events: List[Any] = []
        self.consumer = Consumer(self)
        self.consumer.start()

    def append(self, event: Union[List[T], T]) -> None:
        with self.lock:
            if isinstance(event, list):
                self.events.extend(event)
            else:
                self.events.append(event)

    def get_batch(self) -> List[Any]:
        if self.lock.acquire(False):  # non-blocking
            try:
                events = self.events
                self.events = []
                return events
            finally:
                self.lock.release()
        else:
            return []
