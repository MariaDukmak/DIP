from unittest import TestCase, main
from paxos_implementatie.paxos import simulation


class CanvasExamples(TestCase):
    def test_example1(self):
        """
        Example 1 from the canvas page.
        """

        simulation_input = "1 3 0 15\n" \
                           "0 PROPOSE 1 42\n" \
                           "0 END"

        expected_output = "00000:\t-> P1 PROPOSE v=42\n"\
                          "00001: P1 -> A1 PREPARE n=1\n"\
                          "00002: P1 -> A2 PREPARE n=1\n"\
                          "00003: P1 -> A3 PREPARE n=1\n"\
                          "00004: A1 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "00005: A2 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "00006: A3 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n"\
                          "00007: P1 -> A1 ACCEPT n=1 v=42\n"\
                          "00008: P1 -> A2 ACCEPT n=1 v=42\n"\
                          "00009: P1 -> A3 ACCEPT n=1 v=42\n"\
                          "00010: A1 -> P1 ACCEPTED n=1 v=42\n"\
                          "00011: A2 -> P1 ACCEPTED n=1 v=42\n"\
                          "00012: A3 -> P1 ACCEPTED n=1 v=42\n"\
                          "\n"\
                          "P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)\n"
        simulation_output = simulation.run_simulation(simulation_input)
        self.assertEqual(expected_output, simulation_output)

    def test_example2(self):
        """
        Example 2 from the canvas page.
        """

        simulation_input = "2 3 0 50\n" \
                           "0 PROPOSE 1 42\n" \
                           "8 FAIL PROPOSER 1\n" \
                           "11 PROPOSE 2 37\n" \
                           "26 RECOVER PROPOSER 1\n" \
                           "0 END\n"
        expected_output = "00000:\t-> P1 PROPOSE v=42\n" \
                          "00001: P1 -> A1 PREPARE n=1\n" \
                          "00002: P1 -> A2 PREPARE n=1\n" \
                          "00003: P1 -> A3 PREPARE n=1\n" \
                          "00004: A1 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "00005: A2 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "00006: A3 -> P1 PROMISE n=1 Prior:(n=None, v=None)\n" \
                          "00007: P1 -> A1 ACCEPT n=1 v=42\n" \
                          "00008: ** P1 kapot **\n" \
                          "00009:\n" \
                          "00010:\n" \
                          "00011:\t-> P2 PROPOSE v=37\n" \
                          "00012: P2 -> A1 PREPARE n=2\n" \
                          "00013: P2 -> A2 PREPARE n=2\n" \
                          "00014: P2 -> A3 PREPARE n=2\n" \
                          "00015: A1 -> P2 PROMISE n=2 Prior:(n=1, v=42)\n" \
                          "00016: A2 -> P2 PROMISE n=2 Prior:(n=None, v=None)\n" \
                          "00017: A3 -> P2 PROMISE n=2 Prior:(n=None, v=None)\n" \
                          "00018: P2 -> A1 ACCEPT n=2 v=42\n" \
                          "00019: P2 -> A2 ACCEPT n=2 v=42\n" \
                          "00020: P2 -> A3 ACCEPT n=2 v=42\n" \
                          "00021: A1 -> P2 ACCEPTED n=2 v=42\n" \
                          "00022: A2 -> P2 ACCEPTED n=2 v=42\n" \
                          "00023: A3 -> P2 ACCEPTED n=2 v=42\n" \
                          "00024:\n" \
                          "00025:\n" \
                          "00026: ** P1 gerepareerd **\n" \
                          "00027: P1 -> A2 ACCEPT n=1 v=42\n" \
                          "00028: P1 -> A3 ACCEPT n=1 v=42\n" \
                          "00029: A1 -> P1 ACCEPTED n=1 v=42\n" \
                          "00030: A2 -> P1 REJECTED n=1\n" \
                          "00031: A3 -> P1 REJECTED n=1\n" \
                          "00032: P1 -> A1 PREPARE n=3\n" \
                          "00033: P1 -> A2 PREPARE n=3\n" \
                          "00034: P1 -> A3 PREPARE n=3\n" \
                          "00035: A1 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "00036: A2 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "00037: A3 -> P1 PROMISE n=3 Prior:(n=2, v=42)\n" \
                          "00038: P1 -> A1 ACCEPT n=3 v=42\n" \
                          "00039: P1 -> A2 ACCEPT n=3 v=42\n" \
                          "00040: P1 -> A3 ACCEPT n=3 v=42\n" \
                          "00041: A1 -> P1 ACCEPTED n=3 v=42\n" \
                          "00042: A2 -> P1 ACCEPTED n=3 v=42\n" \
                          "00043: A3 -> P1 ACCEPTED n=3 v=42\n" \
                          "\n" \
                          "P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)\n" \
                          "P2 heeft wel consensus (voorgesteld: 37, geaccepteerd: 42)\n"\

        simulation_output = simulation.run_simulation(simulation_input)
        self.assertEqual(expected_output, simulation_output)


if __name__ == '__main__':
    main()
