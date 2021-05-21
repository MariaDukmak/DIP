import abc
import messages
from network import Network


class Computer(metaclass=abc.ABCMeta):

    def __init__(self, computer_id: int, network: Network):
        self.id = computer_id
        self.network = network
        self.failed = False
        self.sleep = True

    @abc.abstractmethod
    def receive_message(self, message: messages.Message):
        """Receives a message from another machine/Network??"""
        raise NotImplementedError


class Acceptor(Computer):
    def __init__(self, computer_id: int, network: Network):
        super(Acceptor, self).__init__(computer_id, network)
        self.greatest_msg_id = None

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

    def update_greatest_msg_id(self, message_id: messages.MessageId):
        if self.greatest_msg_id is None:
            self.greatest_msg_id = message_id
        elif message_id > self.greatest_msg_id:
            self.greatest_msg_id = message_id


class Proposer(Computer):
    n = 0

    def __init__(self, computer_id: int, network: Network):
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

