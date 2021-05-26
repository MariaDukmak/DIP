from unittest import TestCase, main
from paxos_implementatie.paxos import simulation


class CanvasExamples(TestCase):
    def test_example1(self):
        """Example 1 from the canvas page."""
        simulation_input = "1 3 15\n" \
                           "0 PROPOSE 1 42\n" \
                           "0 END"

        expected_output = "000:\t-> P1 PROPOSE v=42\n"\
                          "001: P1 -> A1 PREPARE n=1\n"\
                          "002: P1 -> A2 PREPARE n=1\n"\
                          "003: P1 -> A3 PREPARE n=1\n"\
                          "004: A1 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "005: A2 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "006: A3 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "007: P1 -> A1 ACCEPT n=1 v=42\n"\
                          "008: P1 -> A2 ACCEPT n=1 v=42\n"\
                          "009: P1 -> A3 ACCEPT n=1 v=42\n"\
                          "010: A1 -> P1 ACCEPTED n=1 v=42\n"\
                          "011: A2 -> P1 ACCEPTED n=1 v=42\n"\
                          "012: A3 -> P1 ACCEPTED n=1 v=42\n"\
                          "013:\n"\
                          "\n"\
                          "P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)\n"
        simulation_output = simulation.run_simulation(simulation_input)
        self.assertEqual(expected_output, simulation_output)

    def test_example2(self):
        """Example 2 from the canvas page."""
        simulation_input = "2 3 50\n" \
                           "0 PROPOSE 1 42\n" \
                           "8 FAIL PROPOSER 1\n" \
                           "11 PROPOSE 2 37\n" \
                           "26 RECOVER PROPOSER 1\n" \
                           "0 END\n"
        expected_output = "000:\t-> P1 PROPOSE v=42\n" \
                          "001: P1 -> A1 PREPARE n=1\n" \
                          "002: P1 -> A2 PREPARE n=1\n" \
                          "003: P1 -> A3 PREPARE n=1\n" \
                          "004: A1 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "005: A2 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "006: A3 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "007: P1 -> A1 ACCEPT n=1 v=42\n" \
                          "008: ** P1 kapot **\n" \
                          "009:\n" \
                          "010:\n" \
                          "011:\t-> P2 PROPOSE v=37\n" \
                          "012: P2 -> A1 PREPARE n=2\n" \
                          "013: P2 -> A2 PREPARE n=2\n" \
                          "014: P2 -> A3 PREPARE n=2\n" \
                          "015: A1 -> P2 PROMISE n=2 Prior:(n=1, v=42)\n" \
                          "016: A2 -> P2 PROMISE n=2 Prior:(n=None, v=None)\n" \
                          "017: A3 -> P2 PROMISE n=2 Prior:(n=None, v=None)\n" \
                          "018: P2 -> A1 ACCEPT n=2 v=42\n" \
                          "019: P2 -> A2 ACCEPT n=2 v=42\n" \
                          "020: P2 -> A3 ACCEPT n=2 v=42\n" \
                          "021: A1 -> P2 ACCEPTED n=2 v=42\n" \
                          "022: A2 -> P2 ACCEPTED n=2 v=42\n" \
                          "023: A3 -> P2 ACCEPTED n=2 v=42\n" \
                          "024:\n" \
                          "025:\n" \
                          "026: ** P1 gerepareerd **\n" \
                          "027: P1 -> A2 ACCEPT n=1 v=42\n" \
                          "028: P1 -> A3 ACCEPT n=1 v=42\n" \
                          "029: A1 -> P1 ACCEPTED n=1 v=42\n" \
                          "030: A2 -> P1 REJECTED n=1\n" \
                          "031: A3 -> P1 REJECTED n=1\n" \
                          "032: P1 -> A1 PREPARE n=3\n" \
                          "033: P1 -> A2 PREPARE n=3\n" \
                          "034: P1 -> A3 PREPARE n=3\n" \
                          "035: A1 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "036: A2 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "037: A3 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "038: P1 -> A1 ACCEPT n=3 v=42\n" \
                          "039: P1 -> A2 ACCEPT n=3 v=42\n" \
                          "040: P1 -> A3 ACCEPT n=3 v=42\n" \
                          "041: A1 -> P1 ACCEPTED n=3 v=42\n" \
                          "042: A2 -> P1 ACCEPTED n=3 v=42\n" \
                          "043: A3 -> P1 ACCEPTED n=3 v=42\n" \
                          "044:\n" \
                          "\n" \
                          "P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)\n" \
                          "P2 heeft wel consensus (voorgesteld: 37, geaccepteerd: 42)\n"\

        simulation_output = simulation.run_simulation(simulation_input)
        self.assertEqual(expected_output, simulation_output)


if __name__ == '__main__':
    main()
