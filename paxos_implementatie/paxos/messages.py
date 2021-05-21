from __future__ import annotations
import abc
from typing import Optional, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from computer import Computer


class MessageId:
    def __init__(self, n: int, source_id: int):
        self.n = n
        self.source_id = source_id

    def __gt__(self, other):
        if self.n != other.n:
            return self.n > other.n
        else:
            return self.source_id > other.source_id


class Message(metaclass=abc.ABCMeta):
    def __init__(self, message_id: Optional[MessageId], source: Optional[Computer], destination: Computer, value: Optional[Any]):
        self.id = message_id
        self.source = source
        self.destination = destination
        self.value = value


class Propose(Message):
    def __init__(self, message_destination, message_value):
        super().__init__(None, None, message_destination, message_value)


class Prepare(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)


class Promise(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)


class Accept(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)


class Accepted(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)


class Rejected(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)


# voor learner nodig
class Success(Message):
    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)
