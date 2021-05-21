import abc
import math
import messages
from network import Network


class Computer(metaclass=abc.ABCMeta):

    def __init__(self, computer_id, network: Network):
        self.id = computer_id
        self.network = network
        self.failed = False
        self.sleep = True

    @abc.abstractmethod
    def receive_message(self, message: messages.Message):
        """Receives a message from another machine/Network??"""
        raise NotImplementedError


class Acceptor(Computer):
    def __init__(self, computer_id, network: Network):
        super(Acceptor, self).__init__(computer_id, network)
        self.largest_n = -math.inf

    def receive_message(self, message: messages.Message):
        self.sleep = False

        if type(message) == messages.Promise:
            pass
        elif type(message) == messages.Accepted:
            pass
        elif type(message) == messages.Propose:
            # alle Aacceptors in netwerk krijgen (messages.Prepare, n)
            pass
        elif type(message) == messages.Promise:
            pass
        elif type(message) == messages.Prepare:
            pass

        self.sleep = True


class Proposer(Computer):
    n = 0

    def __init__(self, computer_id, network: Network):
        super(Proposer, self).__init__(computer_id, network)

    @staticmethod
    def _next_message_id() -> int:
        Proposer.n += 1
        return Proposer.n

    def receive_message(self, message: messages.Message):
        self.sleep = False

        if type(message) == messages.Promise:
            pass
        elif type(message) == messages.Accepted:
            pass

        self.sleep = True

