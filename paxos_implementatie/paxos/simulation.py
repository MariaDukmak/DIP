from typing import List, Optional
from computer import Acceptor, Proposer, Computer
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
            print(f'{t:03}:')
            return

        event = get_event_on_tick(events, t)
        if event is None:
            # There is no event on this tick, proceed normally
            message = network.extract_massage()
            network.deliver_message(message)
            print(f'{t:03}:{message.source} -> {message.destination} {message.name} n={Acceptor.update_greatest_msg_id(message.id)}')
        else:
            # Ignore the queue this tick, the event is more important
            tick, fails, repairs, message_destination, message_value = event
            for computer in fails:
                computer.failed = True
                print(f'** {computer.id} kapot **')

            for computer in repairs:
                computer.failed = False
                print(f'** {computer.id} gerepareerd **')

            if message_destination is not None and message_value is not None:
                message = messages.Propose(message_destination, message_value)
                network.deliver_message(message)
                print(f'{t:03}:    -> {message.destination} {message_value}')
    if network.__len__() == 0:
        print(f'\n P{Proposer.id} heeft wel consensus (voorgesteld: %voorgesteld%, geaccepteerd: %geaccepteerd%)')
    else:
        print(f' \n P{Proposer.id} heeft geen consensus.')


def main():
    pass


if __name__ == "__main__":
    main()
