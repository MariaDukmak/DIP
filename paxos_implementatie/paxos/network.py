"""Holds the proposers, acceptors and learners also ensures delivering messages within the network."""
from typing import List
from paxos_implementatie.paxos.messages import *


class Network:
    # list of messages that should be delivered
    queue: List[Message]

    def __init__(self):
        self.queue = []
        self.acceptors = []
        self.proposers = []
        self.learners = []

    def __len__(self) -> int:
        """
        Return the length of the queue in the network
        :return: length of the queue
        """
        return len(self.queue)

    def queue_message(self, m: Message) -> None:
        """
        Add a message to the queue
        :param m: message of type message
        """
        self.queue.append(m)

    def extract_massage(self) -> Message:
        """
        Delete the last successful massage from the queue and return it
        :return: message of type message
        """
        for i in range(len(self.queue)):
            message = self.queue[i]

            if isinstance(message, Predicted):
                return self.queue.pop(i)
            if not message.source.failed and not message.destination.failed:
                return self.queue.pop(i)

    @staticmethod
    def deliver_message(message: Message) -> None:
        """
        Deliver a message to the destination computer
        :param message: a massage of type message
        """
        message.destination.receive_message(message)
