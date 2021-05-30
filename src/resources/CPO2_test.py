import unittest

from src.resources.CPO2 import Interpreter


class Lab2Test(unittest.TestCase):
    def test_interpreter(self):
        intp = Interpreter()
        intp.input_from_file("TrafficLight.txt")
        intp.input_signal("TURN ON", 0)
        intp.input_signal("TURN GREEN", 5)
        intp.input_signal("TURN YELLOW", 8)
        intp.input_signal("TURN RED", 11)
        intp.input_signal("TURN OFF", 15)
        intp.create_action_table()
        intp.end_state.append("RED")
        intp.end_input.append("TURN OFF")

        result = intp.execute()
        self.assertEqual(result, True)

    def test_interpreter2(self):
        intp = Interpreter()
        intp.input_from_file("TrafficLight.txt")
        intp.input_signal("TURN RED", 0)
        intp.input_signal("TURN ON", 5)
        intp.input_signal("TURN OFF", 8)
        intp.input_signal("TURN GREEN", 11)
        intp.input_signal("TURN OFF", 15)
        intp.create_action_table()
        intp.end_state.append("RED")
        intp.end_input.append("TURN OFF")

        self.assertEqual(intp.execute(), False)

    def test_input_from_file(self):
        intp = Interpreter()
        intp.input_from_file("PytestExample.txt")
        lst = [['state_1', 'event_1', 'state_2', 2], ['state_2', 'event_2', 'state_OFF', 3]]
        self.assertEqual(intp.trans_list, lst)

    def test_interperter3(self):
        intp = Interpreter()
        intp.input_from_file("StringRecognition.txt")
        input_str = "abcdabccdf"
        for index, element in enumerate(input_str):
            intp.input_signal(element, index)
        intp.create_action_table()
        intp.end_state.append("c")
        intp.end_input.append("c")
        result = intp.execute()
        self.assertEqual(result, True)






