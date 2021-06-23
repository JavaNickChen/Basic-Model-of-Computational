import unittest

from Interpreter import Interpreter


class Lab2Test(unittest.TestCase):

    # Test inputting event/state table from file.
    def test_input_from_file(self):
        intp = Interpreter()
        intp.input_from_file("PytestExample.txt")
        lst = [['state_1', 'event_1', 'state_2', 2],
               ['state_2', 'event_2', 'state_OFF', 3]]
        self.assertEqual(intp.trans_list, lst)

    # Unit tests for input data validation in aspect-oriented style.
    def test_aspect_oriented_valid(self):

        @Interpreter.typecheck(a=int)
        def inc(a):
            return a + 1
        # Pass in a variable that meets the criteria —— The variable's type is int.
        self.assertEqual(inc(2), 3)
        # A variable that does not qualify is passed in. The variable's type is character, not int.
        self.assertRaises(TypeError, inc, 'b')

        # Test for using Traffic Light example.
    def test_interpreter(self):
        # Test the interpreter for normal function.
        # To configure the state machine.
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

    # Test for recognizing specific substring in a string.
    def test_interperter2(self):
        # To configure the state machine.
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

    # Test for words counting and words extracting of text parsing.
    def test_interpreter3(self):
        # To configure the state machine.
        intp = Interpreter()
        intp.input_from_file("WordCounting.txt")
        input_str = "Hello, world! I love object-oriented Programming! #"
        for index, element in enumerate(input_str):
            intp.input_signal(element, index)
        intp.create_action_table()
        intp.end_state.append("Word")
        intp.end_input.append("#")
        result = intp.execute()

        self.assertEqual(result, True)

        # To get the word number and the words of 'input_str'.
        word_counter = 0
        quantity_expected = 6
        list_expected = ["Hello", "world", "I", "love", "object-oriented", "Programming"]
        list_get = []

        front_pointer = 0
        front_confirmed = False
        tail_pointer= 0
        tail_confirmed = False
        for index, element in enumerate(intp.history):
            # count the number of word.
            if (element[-1] == 'Word') and (element[-1] != element[1]):
                word_counter = word_counter + 1

            # get the word.
            if (not front_confirmed) and (element[-1] == 'Character') and (element[1] == 'Word' or element[1] == 'INIT'):
                front_pointer = index
                front_confirmed = True
            if (not tail_confirmed) and (element[-1] == 'Word') and (element[1] == 'Character'):
                tail_pointer = index - 1
                tail_confirmed = True
            if tail_confirmed and front_confirmed:
                word = input_str[front_pointer: tail_pointer + 1]
                list_get.append(word)
                tail_confirmed = False
                front_confirmed = False

        self.assertEqual(word_counter, quantity_expected)
        self.assertEqual(list_get.sort(), list_expected.sort())


if __name__ == '__main__':
    unittest.main()
