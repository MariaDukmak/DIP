"""Parse the input into events and runs the simulation."""
from pathlib import Path
from typing import Dict, Union

import matplotlib.pyplot as plt
import seaborn as sns

from paxos_implementatie.paxos.computer import *
from paxos_implementatie.paxos.event import Event
from paxos_implementatie.paxos.messages import *
from paxos_implementatie.paxos.network import Network


def run_simulation(input_string: str) -> str:
    """
    Run the simulation with the parsed input

    :param input_string: the string input
    :return: output string of the simulation
    """
    # Clear the learned matrices a before beginning a new simulation
    for f in glob.glob('learned_matrices/*.np'):
        os.remove(f)

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

            # start a propose using the external output
            if event.message_destination is not None and event.message_value is not None:
                message = Propose(event.message_destination, event.message_value)
                network.deliver_message(message)
                output += f'{t:05}:{message}\n'

    output += '\n'
    for p in network.proposers:
        # if there is no messages moren to deliver
        if len(network.queue) == 0:
            output += f'{p} heeft wel consensus (voorgesteld: {p.suggested_value}, geaccepteerd: {p.accepted_value})\n'
        else:
            output += f'{p} heeft geen consensus.\n'

    print(output)

    return output


def plot_matrix():
    """
    Plot the matrix of the letter combination as heatmap.
    """
    CHARACTERS = 'abcdefghijklmnopqrstuwxyz '
    MATRIX_PATH = Path('learned_matrices')
    matrices = list(map(np.loadtxt, glob.glob(str(MATRIX_PATH / '*.np'))))
    languages = [os.path.basename(path)[:-3] for path in glob.glob(str(MATRIX_PATH / '*.np'))]
    for matrix, lang in zip(matrices, languages):
        ax = sns.heatmap(matrix, center=0, xticklabels=CHARACTERS, yticklabels=CHARACTERS)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=100)
        plt.title(f"{lang.upper()} MATRIX")
        plt.xlabel("Second character")
        plt.ylabel("First characters")
        plt.savefig(f"images/{lang}-matrix.png")
        plt.show()


if __name__ == "__main__":
    run_simulation("1 3 0 15\n0 PROPOSE 1 42\n0 END")
    run_simulation("2 3 0 50\n0 PROPOSE 1 42\n8 FAIL PROPOSER 1\n11 PROPOSE 2 37\n26 RECOVER PROPOSER 1\n0 END")
    simulation_output = run_simulation("1 3 1 10000\n"
                   "0 PROPOSE 1 nl: g\n"
                   "100 PROPOSE 1 nl:ga\n"
                   "200 PROPOSE 1 nl:af\n"
                   "300 PROPOSE 1 nl:aa\n"
                   "400 PROPOSE 1 nl:f \n"
                   "500 PROPOSE 1 en: g\n"
                   "600 PROPOSE 1 en:gr\n"
                   "700 PROPOSE 1 en:re\n"
                   "800 PROPOSE 1 en:ea"
                   "\n900 PROPOSE 1 en:at\n1000 PROPOSE 1 en:t \n0 END")

    plot_matrix()


