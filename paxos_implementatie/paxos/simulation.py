from computer import Acceptor, Proposer
from network import Network


def simulate(n_p: int, n_a: int, tmax: int = 20):
    network = Network()
    acceptors = {Acceptor(i, network) for i in range(n_a)}
    proposers = {Proposer(i, network) for i in range(n_p)}

    # for tik in

# nP , nA, tmax
# input = 1, 3, 15
