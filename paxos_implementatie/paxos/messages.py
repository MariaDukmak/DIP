import abc
from collections import namedtuple


class Message(metaclass=abc.ABCMeta):
    def __init__(self, message_id, message_source, message_destination):
        self.id = message_id
        self.source = message_source
        self.destination = message_destination

    def __lt__(self, other):
        if self.id != other.id:
            return self.id < other.id
        else:
            return self.source < other.source

    def __gt__(self, other):
        if self.id != other.id:
            return self.id > other.id
        else:
            return self.source > other.source


class Propose(Message):
    def __init__(self, message_destination):
        super().__init__(None, None, message_destination)


class Prepare(Message):
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)


class Promise(Message):
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)


class Accept(Message):
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)


class Accepted(Message):
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)


class Rejected:
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)


# voor learner nodig
class Success:
    def __init__(self, message_id, message_source, message_destination):
        super().__init__(message_id, message_source, message_destination)
