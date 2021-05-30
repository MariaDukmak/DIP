"""Contains all messages types for the paxos also include a message id checker."""
from __future__ import annotations
from typing import Optional, Any, TYPE_CHECKING
import abc
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

    def __eq__(self, other):
        return self.n == other.n and self.source_id == other.source_id

    def __ge__(self, other):
        return self > other or self == other

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
        return f"\t-> {self.destination} {type(self).__name__.upper()} v={self.value}"


class Prepare(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Prepare, self).__str__()} {type(self).__name__.upper()} {self.id}"


class Promise(Message):

    def __init__(self, message_id, message_source, message_destination, message_value, prior_n, prior_v):
        super().__init__(message_id, message_source, message_destination, message_value)
        self.prior_n = prior_n
        self.prior_v = prior_v

    def __str__(self):
        return f"{super(Promise, self).__str__()} {type(self).__name__.upper()} {self.id} Prior:(n={self.prior_n}, v={self.prior_v})"


class Accept(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Accept, self).__str__()} {type(self).__name__.upper()} {self.id} v={self.value}"


class Accepted(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Accepted, self).__str__()} {type(self).__name__.upper()} {self.id} v={self.value}"


class Rejected(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Rejected, self).__str__()} {type(self).__name__.upper()} {self.id}"


class Success(Message):

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return f"{super(Success, self).__str__()} {type(self).__name__.upper()}"


class Predicted(Message):
    def __init__(self, message_source, learned):
        super().__init__(None, message_source, None, None)
        self.learned = learned

    def __str__(self):
        return f"{super(Predicted, self).__str__()} {type(self).__name__.upper()}" \
               f" heeft er {self.learned} letter combinatie geleerd."
