"""Parse the input into events and runs the simulation."""
from typing import Dict, Union
from paxos_implementatie.paxos.computer import Acceptor, Proposer, Learner
from paxos_implementatie.paxos.network import Network
from paxos_implementatie.paxos.event import Event
from paxos_implementatie.paxos.messages import *


def run_simulation(input_string: str) -> str:
    """
    Run the simulation with the parsed input

    :param input_string: the string input
    :return: output string of the simulation
    """
    setup = setup_simulation(input_string)
    return simulate(*setup)


def setup_simulation(simulation_input: str) -> tuple[Network, Union[int, Any], dict[int, Event]]:
    """
    Parse the input string into events that the simulation can run

    :param simulation_input: the input string
    :return: tuple of the network, max tik and events.
    """
    network = Network()
    events = {}
    tmax = 0

    input_lines = simulation_input.split('\n')
    for i, line in enumerate(input_lines):
        if i == 0:
            # First line
            n_proposers, n_acceptors, n_learners, tmax = map(int, line.split(' '))
            network.proposers = [Proposer(p, network) for p in range(n_proposers)]
            network.acceptors = [Acceptor(a, network) for a in range(n_acceptors)]
            network.learners = [Learner(l, network) for l in range(n_learners)]
        else:
            if line == '0 END':
                break
            else:
                tick, event_type, *rest = line.split(' ')
                tick = int(tick)

                if event_type == 'PROPOSE':
                    p_i, *v = rest
                    events[tick] = Event(tick, [], [], network.proposers[int(p_i)-1], ' '.join(v))

                elif event_type == 'FAIL':
                    computer_type, computer_id = rest
                    computer = network.proposers[int(computer_id)-1] if computer_type == 'PROPOSER' \
                        else network.acceptors[int(computer_id)-1]

                    if tick in events:
                        events[tick].fails.append(computer)
                    else:
                        events[tick] = Event(tick, [computer], [], None, None)

                elif event_type == 'RECOVER':
                    computer_type, computer_id = rest
                    computer = network.proposers[int(computer_id)-1] if computer_type == 'PROPOSER'\
                        else network.acceptors[int(computer_id)-1]

                    if tick in events:
                        events[tick].repairs.append(computer)
                    else:
                        events[tick] = Event(tick, [], [computer], None, None)

                else:
                    raise Exception(f"{event_type} not acceptable, not PROPOSE, FAIL or RECOVER")

    return network, tmax, events


def simulate(network: Network, tmax: int, events: Dict[int, Event]) -> str:
    """
    Run every event per tik in the simulation and prints the messages per tik.

    :param network: the network of the simulation
    :param tmax: maximum tiks of the simulation
    :param events: the parsed events of the simulation
    :return: output string
    """
    Proposer.n = 0
    output = ""

    for t in range(tmax):
        if len(network) == 0 and len(events) == 0:
            # The simulation ends when there are no messages or events
            break

        event = events.get(t)
        if event is None:
            # There is no event on this tick, proceed normally
            message = network.extract_massage()
            if message is not None:
                if type(message) != Predicted:
                    network.deliver_message(message)
                output += f'{t:05}: {message}\n'
            else:
                output += f'{t:05}:\n'
        else:
            events.pop(t)
            # Ignore the queue this tick, the event is more important
            for computer in event.fails:
                computer.failed = True
                output += f'{t:05}: ** {computer} kapot **\n'

            for computer in event.repairs:
                computer.failed = False
                output += f'{t:05}: ** {computer} gerepareerd **\n'

            if event.message_destination is not None and event.message_value is not None:
                message = Propose(event.message_destination, event.message_value)
                network.deliver_message(message)
                output += f'{t:05}:{message}\n'

    output += '\n'
    for p in network.proposers:
        if len(network.queue) == 0:
            output += f'{p} heeft wel consensus (voorgesteld: {p.suggested_value}, geaccepteerd: {p.accepted_value})\n'
        else:
            output += f'{p} heeft geen consensus.\n'

    print(output)

    return output


if __name__ == "__main__":
    # run_simulation("1 3 0 15\n0 PROPOSE 1 42\n0 END")
    run_simulation("2 3 0 50\n0 PROPOSE 1 42\n8 FAIL PROPOSER 1\n11 PROPOSE 2 37\n26 RECOVER PROPOSER 1\n0 END")
    # run_simulation("1 3 1 10000\n0 PROPOSE 1 nl: g\n100 PROPOSE 1 nl:ga\n200 PROPOSE 1 nl:af\n300 PROPOSE 1 nl:f"
    #                "\n400 PROPOSE 1 en: g\n500 PROPOSE 1 en:gr\n600 PROPOSE 1 en:re\n700 PROPOSE 1 en:ea"
    #                "\n800 PROPOSE 1 en:at\n900 PROPOSE 1 en:t \n0 END")