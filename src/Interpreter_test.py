import unittest

from src.Interpreter import Interpreter


class Lab2Test(unittest.TestCase):
    # Using Traffic Light example for a test case.
    def test_interpreter(self):
        # Test the interpreter for normal function.
        intp1 = Interpreter()
        intp1.input_from_file("TrafficLight.txt")
        intp1.input_signal("TURN ON", 0)
        intp1.input_signal("TURN GREEN", 5)
        intp1.input_signal("TURN YELLOW", 8)
        intp1.input_signal("TURN RED", 11)
        intp1.input_signal("TURN OFF", 15)
        intp1.create_action_table()
        intp1.end_state.append("RED")
        intp1.end_input.append("TURN OFF")
        result = intp1.execute()
        self.assertEqual(result, True)

        # Test the interpreter's handling of receiving abnormal event list.
        intp2 = Interpreter()
        intp2.input_from_file("TrafficLight.txt")
        intp2.input_signal("TURN RED", 0)
        intp2.input_signal("TURN ON", 5)
        intp2.input_signal("TURN OFF", 8)
        intp2.input_signal("TURN GREEN", 11)
        intp2.input_signal("TURN OFF", 15)
        intp2.create_action_table()
        intp2.end_state.append("RED")
        intp2.end_input.append("TURN OFF")

        self.assertEqual(intp2.execute(), False)

    # Test inputing event/state table from file
    def test_input_from_file(self):
        intp = Interpreter()
        intp.input_from_file("PytestExample.txt")
        lst = [['state_1', 'event_1', 'state_2', 2], ['state_2', 'event_2', 'state_OFF', 3]]
        self.assertEqual(intp.trans_list, lst)

    # Recognize specific substring in a string for a test case.
    def test_interperter2(self):
        intp = Interpreter()
        intp.input_from_file("StringRecognition.txt")
        # In the test, "input_str" consists of three lowercase letters:a, b and c.
        input_str = "abcabccbb"
        for index, element in enumerate(input_str):
            intp.input_signal(element, index)
        intp.create_action_table()
        intp.end_state.append("c")
        intp.end_input.append("c")
        result = intp.execute()
        intp.create_graph()
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()





