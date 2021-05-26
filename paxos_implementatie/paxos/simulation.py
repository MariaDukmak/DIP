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

def setup_simulation(simulation_input: str):
    network = Network()
    events = {}
    tmax = 0

    input_lines = simulation_input.split('\n')
    for i, line in enumerate(input_lines):
        if i == 0:
            # First line
            n_proposers, n_acceptors, tmax = map(int, line.split(' '))
            network.proposers = [Proposer(p, network) for p in range(n_proposers)]
            network.acceptors = [Acceptor(a, network) for a in range(n_acceptors)]
        else:
            if line == '0 END':
                break
            else:
                tick, event_type, *rest = line.split(' ')
                tick = int(tick)

                if event_type == 'PROPOSE':
                    p_i, v = rest
                    events[tick] = Event(tick, [], [], network.proposers[int(p_i)-1], v)

                elif event_type == 'FAIL':
                    computer_type, computer_id = rest
                    computer = network.proposers[int(computer_id)] if computer_type == 'PROPOSER' else network.acceptors[int(computer_id)]
                    if tick in events:
                        events[tick].fails.append(computer)
                    else:
                        events[tick] = Event(tick, [computer], [], None, None)

                elif event_type == 'RECOVER':
                    computer_type, computer_id = rest
                    computer = network.proposers[int(computer_id)] if computer_type == 'PROPOSER' else network.acceptors[int(computer_id)]
                    if tick in events:
                        events[tick].repairs.append(computer)
                    else:
                        events[tick] = Event(tick, [], [computer], None, None)

                else:
                    raise Exception(f"{event_type} not acceptable, not PROPOSE, FAIL or RECOVER")

    return network, tmax, events


def simulate(network: Network, tmax: int, events: Dict[int, Event]):
    output = ""
    # een hele domme oplossing maar goed :)
    propose_value = None
    accepted_value = None

    for t in range(tmax):
        if len(network) == 0 or len(events) == 0:
            # The simulation ends when there are no messages or events
            print(f'{t:03}:')
            return

        event = get_event_on_tick(events, t)
        if event is None:
            # There is no event on this tick, proceed normally
            message = network.extract_massage()
            if message is not None:
                network.deliver_message(message)
                accepted_value = message.value
                output += f'{t:03}: {message}\n'
            else:
                output += f'{t:03}:\n'
        else:
            # Ignore the queue this tick, the event is more important
            tick, fails, repairs, message_destination, message_value = event
            for computer in fails:
                computer.failed = True
                output += f'** {computer.id} kapot **\n'

            for computer in repairs:
                computer.failed = False
                output += f'** {computer.id} gerepareerd **\n'

            if message_destination is not None and message_value is not None:
                message = messages.Propose(message_destination, message_value)
                network.deliver_message(message)
                propose_value = message.value
                output += f'{t:03}:{message}\n'

    for p in network.proposers:
        if len(network.queue) == 0:
            output += f'\n{p} heeft wel consensus (voorgesteld: {propose_value} , geaccepteerd: {accepted_value})\n'
        else:
            output += f'{p} heeft geen consensus.\n'
    print(output)

    return output


if __name__ == "__main__":
    # run_simulation("1 3 15\n0 PROPOSE 1 42\n0 END")
    run_simulation("2 3 50\n0 PROPOSE 1 42\n8 FAIL PROPOSER 1\n11 PROPOSE 2 37\n26 RECOVER PROPOSER 1\n0 END")
