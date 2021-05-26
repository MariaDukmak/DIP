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
        if other is None:
            return True
        elif self.n != other.n:
            return self.n > other.n
        else:
            return self.source_id > other.source_id

    def __str__(self):
        return f"n={self.n}"


class Message(metaclass=abc.ABCMeta):
    def __init__(self, message_id: Optional[MessageId], src: Optional[Computer], dst: Computer, value: Optional[Any]):
        self.id = message_id
        self.source = src
        self.destination = dst
        self.value = value

    def __str__(self):
        return f'{self.source} -> {self.destination}'


class Propose(Message):

    def __init__(self, message_destination, message_value):
        super().__init__(None, None, message_destination, message_value)

    def __str__(self):
        return f"\t-> {self.destination} {type(self).__name__} v={self.value}"


class Prepare(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        # Computer.id moet aangepast worden
        return f"{super(Prepare, self).__str__()} {type(self).__name__} {self.id}"


class Promise(Message):

    def __init__(self, message_id, message_source, message_destination, message_value, prior_n, prior_v):
        super().__init__(message_id, message_source, message_destination, message_value)
        self.prior_n = prior_n
        self.prior_v = prior_v

    def __str__(self):
        # Computer.id moet aangepast worden, en de Prior list
        return f"{super(Promise, self).__str__()} {type(self).__name__} {self.id} Prior:(n={self.prior_n}, v={self.prior_v})"


class Accept(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Accept, self).__str__()} {type(self).__name__} {self.id} v={self.value}"


class Accepted(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Accepted, self).__str__()} {type(self).__name__} {self.id} v={self.value}"


class Rejected(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Rejected, self).__str__()} {type(self).__name__}"


# voor learner nodig
class Success(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Success, self).__str__()} {type(self).__name__}"
