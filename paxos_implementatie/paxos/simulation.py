from typing import Dict
from paxos_implementatie.paxos.computer import Acceptor, Proposer
from paxos_implementatie.paxos.network import Network
from paxos_implementatie.paxos.event import Event
from paxos_implementatie.paxos.messages import *


def run_simulation(input_string: str) -> str:
    setup = setup_simulation(input_string)
    return simulate(*setup)


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
                    computer = network.proposers[int(computer_id)-1] if computer_type == 'PROPOSER' else network.acceptors[int(computer_id)-1]
                    if tick in events:
                        events[tick].fails.append(computer)
                    else:
                        events[tick] = Event(tick, [computer], [], None, None)

                elif event_type == 'RECOVER':
                    computer_type, computer_id = rest
                    computer = network.proposers[int(computer_id)-1] if computer_type == 'PROPOSER' else network.acceptors[int(computer_id)-1]
                    if tick in events:
                        events[tick].repairs.append(computer)
                    else:
                        events[tick] = Event(tick, [], [computer], None, None)

                else:
                    raise Exception(f"{event_type} not acceptable, not PROPOSE, FAIL or RECOVER")

    return network, tmax, events


def simulate(network: Network, tmax: int, events: Dict[int, Event]):
    Proposer.n = 0
    output = ""

    for t in range(tmax):
        if len(network) == 0 and len(events) == 0:
            # The simulation ends when there are no messages or events
            output += f'{t:03}:\n'
            break

        event = events.get(t)
        if event is None:
            # There is no event on this tick, proceed normally
            message = network.extract_massage()
            if message is not None:
                network.deliver_message(message)
                output += f'{t:03}: {message}\n'
            else:
                output += f'{t:03}:\n'
        else:
            events.pop(t)
            # Ignore the queue this tick, the event is more important
            for computer in event.fails:
                computer.failed = True
                output += f'{t:03}: ** {computer} kapot **\n'

            for computer in event.repairs:
                computer.failed = False
                output += f'{t:03}: ** {computer} gerepareerd **\n'

            if event.message_destination is not None and event.message_value is not None:
                message = Propose(event.message_destination, event.message_value)
                network.deliver_message(message)
                output += f'{t:03}:{message}\n'

    output += '\n'
    for p in network.proposers:
        if len(network.queue) == 0:
            output += f'{p} heeft wel consensus (voorgesteld: {p.suggested_value}, geaccepteerd: {p.accepted_value})\n'
        else:
            output += f'{p} heeft geen consensus.\n'

    print(output)

    return output


if __name__ == "__main__":
    run_simulation("1 3 15\n0 PROPOSE 1 42\n0 END")
    run_simulation("2 3 50\n0 PROPOSE 1 42\n8 FAIL PROPOSER 1\n11 PROPOSE 2 37\n26 RECOVER PROPOSER 1\n0 END")
