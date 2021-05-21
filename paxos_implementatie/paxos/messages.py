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
    def __init__(self, message_id: Optional[MessageId], src: Optional[Computer], dst: Computer, value: Optional[Any]):
        self.id = message_id
        self.source = src
        self.destination = dst
        self.value = value

    def __str__(self):
        return f'{self.source} -> {self.destination} '


class Propose(Message):
    name = "PROPOSE"

    def __init__(self, message_destination, message_value):
        super().__init__(None, None, message_destination, message_value)

    def __str__(self):
        return super(Propose, self).__str__() + f' {self.name} v={self.value}'


class Prepare(Message):
    name = "PREPARE"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Prepare, self).__str__() + f' {self.name} n= {Computer.id}'


class Promise(Message):
    name = "PROMISE"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Promise, self).__str__() + f' {self.name} n= {Computer.id} Prior:({None})'


class Accept(Message):
    name = "ACCEPT"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Accept, self).__str__() + f' {self.name}'


class Accepted(Message):
    name = "ACCEPTED"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Accepted, self).__str__() + f' {self.name}'


class Rejected(Message):
    name = "REJECTED"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Rejected, self).__str__() + f' {self.name}'


# voor learner nodig
class Success(Message):
    name = "SUCCESS"

    def __init__(self, message_id, message_source, message_destination, message_value):
        super().__init__(message_id, message_source, message_destination, message_value)

    def __str__(self):
        return super(Success, self).__str__() + f' {self.name}'