import glob
import os

import numpy as np

from paxos_implementatie.paxos.messages import *
from paxos_implementatie.paxos.network import Network


class Computer(metaclass=abc.ABCMeta):

    def __init__(self, computer_id: int, network: Network):
        self.id = computer_id
        self.network = network
        self.failed = False
        self.sleep = True

    @abc.abstractmethod
    def receive_message(self, message: Message) -> Exception:
        """
        Receive a message from another machine in the network
        :param message:a message in the netwerk queue
        :return Exception
        """
        raise NotImplementedError("This function does only work for the subclasses Acceptor and Proposer!")

    def __str__(self) -> str:
        """
        Prints the id of the computer, we begin at 1
        """
        return str(self.id + 1)


class Acceptor(Computer):
    def __init__(self, computer_id: int, network: Network):
        super(Acceptor, self).__init__(computer_id, network)
        self.greatest_msg_id = None
        self.prior_n = None
        self.prior_v = None

    def receive_message(self, incoming_m: Message) -> None:
        """
        Receives messages from the netwerk, based on that it reply with a new message

        :param incoming_m: a message in the netwerk queue
        """
        # Acceptor is awake
        # This doesn't do anything practical but you can think of it as a finite state machine
        self.sleep = False

        # Check the greatest id in the netwerk
        self.update_greatest_msg_id(incoming_m.id)

        # Check if this propose id greater than the previous one
        if incoming_m.id >= self.greatest_msg_id:
            # Prepare -> Promise + prior (previous accept of exist)
            if isinstance(incoming_m, Prepare):
                self.network.queue_message(Promise(incoming_m.id, self, incoming_m.source, incoming_m.value,
                                                   self.prior_n, self.prior_v))
            # Accept -> Accepted + update prior
            elif isinstance(incoming_m, Accept):
                self.prior_n, self.prior_v = incoming_m.id.n, incoming_m.value
                self.network.queue_message(Accepted(incoming_m.id, self, incoming_m.source, incoming_m.value))

        else:
            # Reject propose if id is less than the previous one
            self.network.queue_message(Rejected(incoming_m.id, self, incoming_m.source, incoming_m.value))

        # Acceptor back to sleep
        self.sleep = True

    def update_greatest_msg_id(self, message_id: MessageId) -> None:
        """
        Update the greatest message id locally using MessageId class
        :param message_id: the id of the message
        """
        if message_id > self.greatest_msg_id:
            self.greatest_msg_id = message_id

    def __str__(self) -> str:
        return f"A{super(Acceptor, self).__str__()}"


class Proposer(Computer):
    n = 0

    def __init__(self, computer_id: int, network: Network):
        super(Proposer, self).__init__(computer_id, network)
        self.promises = 0
        self.accepted_value = None
        self.suggested_value = None
        self.working_id = 0

    @staticmethod
    def _next_message_id() -> int:
        """
        Get id for the next propose
        :return: int of the next id
        """
        Proposer.n += 1
        return Proposer.n

    def majority_message(self) -> bool:
        """
        Check if the majority of the acceptors has response
        :return: boolen, true or false
        """
        return self.promises > len(self.network.acceptors) / 2

    def receive_message(self, incoming_m: Message) -> None:
        """
        Receives messages from the netwerk, based on that it reply with a new message
        :param incoming_m: a message in the netwerk queue
        """
        # Proposer is awake
        # This doesn't do anything practical but you can think of it as a finite state machine
        self.sleep = False

        # Propose -> Prepare
        if isinstance(incoming_m, Propose):
            self.promises = 0
            self.suggested_value = incoming_m.value
            self.accepted_value = incoming_m.value
            message_id = MessageId(Proposer._next_message_id(), self.id)
            self.working_id = message_id
            for a in self.network.acceptors:
                self.network.queue_message(Prepare(message_id, self, a, incoming_m.value))

        # Promise -> Accept
        elif isinstance(incoming_m, Promise):
            incoming_m: Promise
            self.promises += 1
            if incoming_m.prior_v is not None:
                self.accepted_value = incoming_m.prior_v
            if self.majority_message():
                for a in self.network.acceptors:
                    self.network.queue_message(Accept(incoming_m.id, self, a, self.accepted_value))
                self.promises = 0

        # Accepted -> Success
        elif isinstance(incoming_m, Accepted):
            self.promises += 1
            if self.majority_message():
                for c in self.network.learners:
                    self.network.queue_message(Success(incoming_m.id, self, c, incoming_m.value))
            self.promises = 0

        # Rejected -> Prepare
        elif isinstance(incoming_m, Rejected):
            if incoming_m.id == self.working_id:
                message_id = MessageId(Proposer._next_message_id(), self.id)
                self.working_id = message_id
                for a in self.network.acceptors:
                    self.network.queue_message(Prepare(message_id, self, a, incoming_m.value))

        # Proposers back to sleep
        self.sleep = True

    def __str__(self) -> str:
        return f"P{super(Proposer, self).__str__()}"


class Learner(Computer):

    def __init__(self, computer_id: int, network: Network):
        super(Learner, self).__init__(computer_id, network)
        self.matrices = {}
        self.learned_n = 0

    def receive_message(self, incoming_m: Message) -> None:
        """
        Receives messages from the netwerk, based on that it reply with a new message
        :param incoming_m: a message in the netwerk queue
        """
        # Success -> Predicted
        if isinstance(incoming_m, Success):
            self.create_matrix(incoming_m.value)
            for a in self.network.acceptors:
                a.prior_v, a.prior_n = None, None
            self.network.queue_message(Predicted(self, self.learned_n))
        # else is messages not implemented voor learner
        else:
            raise AttributeError("This type message doesn't exist for Learner")

    def create_matrix(self, value: str) -> None:
        """
        Creat a matrix of the characters, update the matrix with
        the learned letters and save it.
        :param value: the letter combination as nl:aa or en:ga
        """
        # the accepted charcters
        characters = 'abcdefghijklmnopqrstuwxyz '

        # split the language and the letter combination
        language, *letter_combi = value.split(':')
        letter_combi = [l if l in characters else '!' for l in ':'.join(letter_combi)]
        file_path = os.path.join('learned_matrices', language + '.np')

        # open or create the matrix
        if file_path in glob.glob('learned_matrices/*.np'):
            matrix = np.loadtxt(file_path)
        else:
            matrix = np.zeros([len(characters)] * 2)

        # update the matrix
        matrix[characters.index(letter_combi[0]), characters.index(letter_combi[1])] += 1
        np.savetxt(file_path, matrix)

        # update the local learning counter
        self.learned_n += 1

    def __str__(self) -> str:
        return f'L{super(Learner, self).__str__()}'
