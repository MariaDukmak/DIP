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

    def __str__(self):
        return str(self.id + 1)


class Acceptor(Computer):
    def __init__(self, computer_id: int, network: Network):
        super(Acceptor, self).__init__(computer_id, network)
        self.greatest_msg_id = None
        self.prior_n, self.prior_v = None, None

    def receive_message(self, incoming_m: messages.Message):
        self.sleep = False

        if incoming_m.id > self.greatest_msg_id:
            if type(incoming_m) == messages.Prepare:
                self.network.queue_message(messages.Promise(incoming_m.id, self, incoming_m.source, incoming_m.value,
                                                            self.prior_n, self.prior_v))

            elif type(incoming_m) == messages.Accept:
                self.prior_n = incoming_m.id
                self.prior_v = incoming_m.value
                # for c in [incoming_m.source] + self.network.acceptors:
                #     if c is not self:
                self.network.queue_message(messages.Accepted(incoming_m.id, self, incoming_m.source, incoming_m.value))

        else:
            self.network.queue_message(messages.Rejected(incoming_m.id, self, incoming_m.source))

        # TODO: maak een count voor accepted messages, check of je dit echt wilt!

        self.sleep = True

    def update_greatest_msg_id(self, message_id: messages.MessageId):
        if message_id > self.greatest_msg_id:
            self.greatest_msg_id = message_id

    def __str__(self):
        return 'A' + super(Acceptor, self).__str__()


class Proposer(Computer):
    n = 0

    def __init__(self, computer_id: int, network: Network):
        super(Proposer, self).__init__(computer_id, network)
        self.promises = 0
        self.accepted_value = None
        self.suggested_value = None

    @staticmethod
    def _next_message_id() -> int:
        Proposer.n += 1
        return Proposer.n

    def majority_message(self):
        return self.promises > len(self.network.acceptors)/2

    def receive_message(self, incoming_m: messages.Message):
        self.sleep = False

        if type(incoming_m) == messages.Promise:
            self.promises += 1
            if self.majority_message():
                for a in self.network.acceptors:
                    self.network.queue_message(messages.Accept(incoming_m.id, self, a, incoming_m.value))
                self.promises = 0

        # TODO: fix wat met de output van dit moet gebeuren
        elif type(incoming_m) == messages.Accepted:
            self.promises += 1
            if self.majority_message():
                self.promises = 0
            self.accepted_value = incoming_m.value

        elif type(incoming_m) == messages.Propose:
            self.promises = 0
            self.suggested_value = incoming_m.value
            message_id = messages.MessageId(Proposer._next_message_id(), self.id)
            for a in self.network.acceptors:
                self.network.queue_message(messages.Prepare(message_id, self, a, incoming_m.value))

        self.sleep = True

    def __str__(self):
        return f"P{super(Proposer, self).__str__()}"

