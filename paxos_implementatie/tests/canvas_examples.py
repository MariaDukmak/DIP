from unittest import TestCase, main


class CanvasExamples(TestCase):
    def test_example1(self):
        """Example 1 from the canvas page."""
        simulation_input = """
            1 3 15
            0 PROPOSE 1 42
            0 END
            """
        expected_output = """
            000:    -> P1  PROPOSE v=42
            001: P1 -> A1  PREPARE n=1
            002: P1 -> A2  PREPARE n=1
            003: P1 -> A3  PREPARE n=1
            004: A1 -> P1  PROMISE n=1 (Prior: None)
            005: A2 -> P1  PROMISE n=1 (Prior: None)
            006: A3 -> P1  PROMISE n=1 (Prior: None)
            007: P1 -> A1  ACCEPT n=1 v=42
            008: P1 -> A2  ACCEPT n=1 v=42
            009: P1 -> A3  ACCEPT n=1 v=42
            010: A1 -> P1  ACCEPTED n=1 v=42
            011: A2 -> P1  ACCEPTED n=1 v=42
            012: A3 -> P1  ACCEPTED n=1 v=42
            
            P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)
            """
        # TODO
        simulation_output = ""
        self.assertEqual(simulation_output, expected_output)

    def test_example2(self):
        """Example 2 from the canvas page."""
        simulation_input = """
            2 3 50
            0 PROPOSE 1 42
            8 FAIL PROPOSER 1
            11 PROPOSE 2 37
            26 RECOVER PROPOSER 1
            0 END
            """
        expected_output = """
            000:    -> P1  PROPOSE v=42
            001: P1 -> A1  PREPARE n=1
            002: P1 -> A2  PREPARE n=1
            003: P1 -> A3  PREPARE n=1
            004: A1 -> P1  PROMISE n=1 (Prior: None)
            005: A2 -> P1  PROMISE n=1 (Prior: None)
            006: A3 -> P1  PROMISE n=1 (Prior: None)
            007: P1 -> A1  ACCEPT n=1 v=42
            008: ** P1 kapot **
            009:
            010:
            011:    -> P2  PROPOSE v=37
            012: P2 -> A1  PREPARE n=2
            013: P2 -> A2  PREPARE n=2
            014: P2 -> A3  PREPARE n=2
            015: A1 -> P2  PROMISE n=2 (Prior: n=1, v=42)
            016: A2 -> P2  PROMISE n=2 (Prior: None)
            017: A3 -> P2  PROMISE n=2 (Prior: None)
            018: P2 -> A1  ACCEPT n=2 v=42
            019: P2 -> A2  ACCEPT n=2 v=42
            020: P2 -> A3  ACCEPT n=2 v=42
            021: A1 -> P2  ACCEPTED n=2 v=42
            022: A2 -> P2  ACCEPTED n=2 v=42
            023: A3 -> P2  ACCEPTED n=2 v=42
            024:
            025:
            026: ** P1 gerepareerd **
            026: P1 -> A2  ACCEPT n=1 v=42
            027: P1 -> A3  ACCEPT n=1 v=42
            028: A1 -> P1  ACCEPTED n=1 v=42
            029: A2 -> P1  REJECTED n=1
            030: A3 -> P1  REJECTED n=1
            031: P1 -> A1  PREPARE n=3
            032: P1 -> A2  PREPARE n=3
            033: P1 -> A3  PREPARE n=3
            034: A1 -> P1  PROMISE n=3 (Prior: n=2, v=42)
            035: A2 -> P1  PROMISE n=3 (Prior: n=2, v=42)
            036: A3 -> P1  PROMISE n=3 (Prior: n=2, v=42)
            037: P1 -> A1  ACCEPT n=3 v=42
            038: P1 -> A2  ACCEPT n=3 v=42
            039: P1 -> A3  ACCEPT n=3 v=42
            040: A1 -> P1  ACCEPTED n=3 v=42
            041: A2 -> P1  ACCEPTED n=3 v=42
            042: A3 -> P1  ACCEPTED n=3 v=42
            
            P1 heeft wel consensus (voorgesteld: 42, geaccepteerd: 42)
            P2 heeft wel consensus (voorgesteld: 37, geaccepteerd: 42)
            """
        # TODO
        simulation_output = ""
        self.assertEqual(simulation_output, expected_output)


if __name__ == '__main__':
    main()
