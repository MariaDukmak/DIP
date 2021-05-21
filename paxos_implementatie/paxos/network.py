import messages
from typing import List


class Network:
    queue: List[messages.Message]

    def __init__(self):
        self.queue = []

    def queue_message(self, m: messages.Message):
        """Add a message to the queue."""
        self.queue.append(m)

    def extract_massage(self) -> messages.Message:
        """Delete the last successful massage from the queue and return it."""
        for i in range(len(self.queue)):
            m = self.queue[i]

            if not m.source.failed and not m.destination.failed:
                return self.queue.pop(i)
