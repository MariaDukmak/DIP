from typing import List, Optional
from computer import Acceptor, Proposer
from network import Network
from event import Event
import messages


def get_event_on_tick(events: List[Event], tick: int) -> Optional[Event]:
    for event in events:
        if event.tick == tick:
            events.remove(event)
            return event


def simulate(tmax: int, events: List[Event]):
    network = Network()

    for t in range(tmax):
        if len(network) == 0 or len(events) == 0:
            # The simulation ends when there are no messages or events
            return

        event = get_event_on_tick(events, t)
        if event is None:
            # There is no event on this tick, proceed normally
            message = network.extract_massage()
            network.deliver_message(message)
        else:
            # Ignore the queue this tick, the event is more important
            tick, fails, repairs, message_destination, message_value = event
            for computer in fails:
                computer.failed = True
            for computer in repairs:
                computer.failed = False
            if message_destination is not None and message_value is not None:
                message = messages.Propose(message_destination, message_value)
                network.deliver_message(message)

