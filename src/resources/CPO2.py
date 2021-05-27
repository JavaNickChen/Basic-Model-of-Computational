import collections
from graphviz import Digraph
import logging

# Some processing of python logging
# enables python log to be displayed in the console and saved in a file at
# the same time.
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.txt", mode='w')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.addHandler(fh)


class interpreter:
    """
    This class is used to implement most of the functions of a simple eDSL interpreter
    """

    def __init__(self):
        """
        This is the constructor of an eDSL interpreter,
        most of the class attributes of the eDSL interpreter will be initialized below,
        see attribute notes for details
        """
        self.state_count = 0  # This attribute is used to count the number of established states
        # This ordered dictionary is used to store all states, each state will
        # correspond to an index, state is a string type value
        self.state_list = collections.OrderedDict()
        self.input_count = 0  # This attribute is used to count the number of possible signal value
        # This ordered dictionary is used to store all possible input signal ,
        # each input signal  will correspond to an index, input signal  is a
        # string type value
        self.input_list = collections.OrderedDict()
        self.state = 0  # This attribute is used to save the current state during the execution phase
        self.end_state = []  # This list saves all termination status
        self.end_input = []  # This list saves all terminated input signal values
        # This ordered dictionary is used to record the input signal string
        # during execution
        self.input_queue = collections.OrderedDict()
        self.trans_list = []  # This list is used to temporarily save all input state transitions
        self.final = False  # This attribute is used to identify whether the program has reached the termination state after execution
        self.clock = 0  # Program-defined clock
        self.count = 0  # Index of the executed instruction
        self.action_table = []  # The state transition table is generated by the input state transition, and the state transition is read from it during execution

    def input_from_file(self, filename):
        """
        This function provides a way to input from a file
        :param filename: File location
        :return: false if some invalid input occur , true if successfully input
        """
        f = open(filename)
        while True:
            lines = f.readlines()
            if not lines:
                break
            for line in lines:
                if line[0] == '$':
                    lt = line.strip("\n").strip("$")
                    self.add_state(lt)
                elif line[0] == '%':
                    lt = line.strip("\n").strip("%")
                    self.add_input(lt)
                elif line[0] == '#' and line[len(line) - 1] == '#':
                    lt = line.strip("\n").strip("#").split(",")
                    for e in lt:
                        es=e.split(" ")
                        self.input_signal(es[0],es[1])
                else:
                    lt = line.strip("\n").split(":")
                    at = lt[0].split("-->")
                    if len(lt) != 2 or len(at) != 3:
                        logger.error("Input invalid.")
                        return false
                    else:
                        self.add_trans(at[0], at[1], at[2], int(lt[1]))
        return True

    def create_action_table(self):
        """
        This function is used to construct a state transition table for the interpreter,
        and this method needs to be explicitly called to complete the creation before execution.
        """
        state_num = self.state_count
        input_num = self.input_count
        logger.info("Create the action table.")
        logger.info(
            "Number of states: " +
            str(state_num) +
            " Number of input character: " +
            str(input_num))
        self.action_table = []
        for i in range(state_num):
            temp_list = []
            for j in range(input_num):
                temp_list.append([])
            self.action_table.append(temp_list)
        for t in self.trans_list:
            for s in self.state_list.keys():
                if self.state_list[s] == t[0]:
                    inct = s
                if self.state_list[s] == t[2]:
                    outt = s
            for s in self.input_list.keys():
                if self.input_list[s] == t[1]:
                    inrt = s
            self.action_table[inct][inrt] = [outt, t[3]]

    def create_graph(self):
        """
        This function creates a visual state transition diagram.
        You need to explicitly call create_action_table before use
        :return:
        """
        logger.info("Create a viz graph.")
        g = Digraph('测试图片')
        for i in self.state_list:
            g.node(self.state_list[i], self.state_list[i])
        for t in self.trans_list:
            g.edge(str(t[0]), str(t[2]), label=str(t[1]) + " " + str(t[3]))
        g.view()

    def add_state(self, state):
        """
        Add a new state to the interpreter
        :param state: new state
        :return:
        """
        self.state_list[self.state_count] = state
        self.state_count += 1

    def add_input(self, input):
        """
        Add a new input signal to the interpreter
        :param input: new input signal
        :return:
        """
        self.input_list[self.input_count] = input
        self.input_count += 1

    def add_trans(self, ins, inc, outs, times):
        """
        Add a new state transition to the interpreter
        :param ins: Current state
        :param inc: input signal
        :param outs: transferred state
        :param times: Time required for state transition
        :return:
        """
        if ins not in self.state_list.values():
            self.state_list[self.state_count] = ins
            self.state_count += 1
        if outs not in self.state_list.values():
            self.state_list[self.state_count] = outs
            self.state_count += 1
        if inc not in self.input_list.values():
            self.input_list[self.input_count] = inc
            self.input_count += 1
        self.trans_list.append([ins, inc, outs, times])

    def input_signal(self, inc,time):
        """
        input a signal
        :param inc: input signal
        :return:
        """
        self.input_queue[self.count] = [inc,time]
        self.count += 1

    def execute(self):
        """
        This function inputs the signals in the order in input_queue, executes the process,
        the state transition by matching the state in the state transition table,
        and finally checks whether the termination state is reached and the termination input signal is obtained.
        :return: true if Successfully reached the termination state and received the termination signal , otherwise false
        """
        self.state = self.state_list[0]
        logger.info("Execute: Start state= " + self.state)
        state_index = 0
        self.count = 0
        timer = 0
        max_t = 0
        next=None
        next_clock = self.input_queue[0][1]
        while self.count < len(self.input_queue):
            if timer >= max_t and next_clock==self.clock:
                if self.state in self.end_state and self.input_queue[self.count][0] in self.end_input:
                    logger.info("Terminal: at clock " +
                                str(self.clock) +
                                "\t,\tstate: " +
                                str(self.state) +
                                "\t,\tinput : " +
                                str(self.input_queue[self.count][0]))
                    self.final = True
                    break
                if not next:
                    for s in self.input_list.keys():
                        if self.input_list[s] == self.input_queue[self.count][0]:
                            index = s
                    next_clock = self.input_queue[self.count+1][1]
                    next = self.action_table[state_index][index]
                    if next == []:
                        logger.error("Unknown state transition.")
                        break
                    max_t = next[1]
                    timer = 0

                else:

                    for s in self.input_list.keys():
                        if self.input_list[s] == self.input_queue[self.count][0]:
                            index = s
                    if len(self.input_queue)==self.count+1:
                        next_clock = next_clock+10
                    else:
                        next_clock = self.input_queue[self.count + 1][1]
                    next = self.action_table[state_index][index]
                    if next == []:
                        logger.error("Unknown state transition.")
                        break
                    max_t = next[1]
                    timer = 0
            elif timer == max_t:
                logger.info("trans: at clock " +
                            str(self.clock) +
                            "\t,\tori_state: " +
                            str(self.state) +
                            "\t,\tinput : " +
                            str(self.input_list[index]) +
                            "\t,\tnext_state : " +
                            str(self.state_list[next[0]]))
                self.state = self.state_list[next[0]]
                state_index = next[0]
                timer += 1
                self.count += 1

            else:
                timer += 1
                self.clock += 1



        if self.final:
            logger.info("Reach the end state.")
            return True
        else:
            logger.info("Not reach the end state.")
            return False


if __name__ == "__main__":
    intp = interpreter()
    intp.input_from_file("test.txt")
    # intp.add_state("INIT")
    # intp.add_state("RED")
    # intp.add_state("YELLOW")
    # intp.add_state("GREEN")
    # intp.add_state("OFF")
    # intp.add_input("TURN ON")
    # intp.add_input("TURN GREEN")
    # intp.add_input("TURN YELLOW")
    # intp.add_input("TURN RED")
    # intp.add_input("TURN OFF")
    # intp.add_trans("INIT","TURN ON","RED",3)
    # intp.add_trans("RED","TURN GREEN","GREEN",2)
    # intp.add_trans("GREEN","TURN YELLOW","YELLOW",2)
    # intp.add_trans("YELLOW","TURN RED","RED",2)
    # intp.add_trans("RED", "TURN OFF", "OFF", 2)
    # intp.add_trans("GREEN", "TURN OFF", "OFF", 2)
    # intp.add_trans("YELLOW", "TURN OFF", "OFF", 2)
    intp.input_signal("TURN ON",0)
    intp.input_signal("TURN GREEN",5)
    intp.input_signal("TURN YELLOW",8)
    intp.input_signal("TURN RED",11)
    intp.input_signal("TURN OFF",15)
    intp.create_action_table()
    intp.end_state.append("RED")
    intp.end_input.append("TURN OFF")
    intp.execute()
    intp.create_graph()
