import collections
from graphviz import Digraph  # type: ignore
import logging
from inspect import signature
from functools import wraps
from typing import Callable, TypeVar, Any, Generic, List
import typing

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


VI = TypeVar("VI", str, List[str])


class Interpreter(Generic[VI]):
    """
    This class is used to implement most of the functions of a simple eDSL interpreter
    """

    def __init__(self):
        """
        This is the constructor of an eDSL interpreter,
        most of the class attributes of the eDSL interpreter will be initialized below,
        see attribute notes for details
        """
        # This attribute is used to count the number of established states
        self.state_count = 0  # type: int
        # This ordered dictionary is used to store all states, each state will
        # correspond to an index, state is a string type value
        self.state_list = collections.OrderedDict()  # type: Any
        # This attribute is used to count the number of possible signal value
        self.input_count = 0  # type: int
        # This ordered dictionary is used to store all possible input signal ,
        # each input signal  will correspond to an index, input signal  is a
        # string type value
        self.input_list = collections.OrderedDict()  # type: Any
        # This attribute is used to save the current state during the execution
        # phase
        self.state = "NO_STATE"  # type: str
        # This list saves all termination status
        self.end_state = []  # type: List
        # This list saves all terminated input signal values
        self.end_input = []  # type: List
        # This ordered dictionary is used to record the input signal string
        # during execution
        self.input_queue = collections.OrderedDict()  # type: Any
        # This list is used to temporarily save all input state transitions
        self.trans_list = []  # type: List
        # This attribute is used to identify whether the program has reached
        # the termination state after execution
        self.final = False  # type: bool
        # Program-defined clock
        self.clock = 0  # type: int
        # Index of the executed instruction
        self.count = 0  # type: int
        # The state transition table is generated by the input state
        # transition, and the state transition is read from it during execution
        self.action_table = []  # type: List
        self.history = []  # type: List

    def typecheck(*type_args: Any, **type_kwargs: Any) -> Any:
        """
        This function is a decorator used to check the input parameter type
        :param type_args:One or more unnamed parameters passed in.
        :param type_kwargs:One or more parameters with parameter names passed in.
        :return:An example of a decorator used to check the input type.
        """

        def decorator(func) :
            sig = signature(func)
            bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_values = sig.bind(*args, **kwargs)
                for name, value in bound_values.arguments.items():
                    if name in bound_types:
                        if not isinstance(value, bound_types[name]):
                            logger.error('Argument {} must be {}'.format(
                                name, bound_types[name]))
                            raise TypeError(
                                'Argument {} must be {}'.format(
                                    name, bound_types[name]))
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @typecheck(filename=str)
    def input_from_file(self, filename: str) -> bool:
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
                if line[0] == '>':
                    self.end_input.append(line.strip("\n").strip(">"))
                elif line[0] == '<':
                    self.end_state.append(line.strip("\n").strip("<"))
                elif line[0] == '$':
                    self.add_state(line.strip("\n").strip("$"))
                elif line[0] == '%':
                    self.add_input(line.strip("\n").strip("%"))
                elif line[0] == '#' and line[len(line) - 1] == '#':
                    lt = line.strip("\n").strip("#").split(",")
                    for e in lt:
                        es = e.split(" ")
                        self.input_signal(es[0], es[1])
                else:
                    lt = line.strip("\n").split(":")
                    at = lt[0].split("-->")
                    if len(lt) != 2 or len(at) != 3:
                        logger.error("Input invalid.")
                        return False
                    else:
                        self.add_trans(at[0], at[1], at[2], int(lt[1]))
        return True

    def create_action_table(self):
        """
        This function is used to construct a state transition table for the interpreter,
        and this method needs to be explicitly called to complete the creation before execution.
        :return: None
        """
        state_num = self.state_count
        input_num = self.input_count
        logger.info("\nCreate the action table.")
        logger.info(
            "Number of states: " +
            str(state_num) +
            "\t,\t" +
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
        :return: None
        """
        logger.info("Create a viz graph.")
        g = Digraph('test_picture')
        for i in self.state_list:
            g.node(self.state_list[i], self.state_list[i])
        for t in self.trans_list:
            g.edge(str(t[0]), str(t[2]), label=str(t[1]) + " " + str(t[3]))
        g.view()

    @typecheck(state=str)
    def add_state(self, state: str):
        """
        Add a new state to the interpreter
        :param state: new state
        :return: None
        """
        self.state_list[self.state_count] = state
        self.state_count += 1

    @typecheck(object, str)
    def add_input(self, input):
        """
        Add a new input signal to the interpreter
        :param input: new input signal
        :return: None
        """
        self.input_list[self.input_count] = input
        self.input_count += 1

    @typecheck(object, str, str, str, int)
    def add_trans(self, ins: str, inc: str, outs: str, times: int):
        """
        Add a new state transition to the interpreter
        :param ins: Current state
        :param inc: input signal
        :param outs: transferred state
        :param times: Time required for state transition
        :return: None
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

    @typecheck(object, str, int)
    def input_signal(self, inc: str, time: int):
        """
        input a signal
        :param inc: input signal i.e. event
        :param time: the time when the event takes effect.
        :return: None
        """
        self.input_queue[self.count] = [inc, time]
        self.count += 1

    def execute(self) -> bool:
        """
        This function inputs the signals in the order in input_queue, executes the process,
        the state transition by matching the state in the state transition table,
        and finally checks whether the termination state is reached and the termination input signal is obtained.
        :return: true if Successfully reached the termination state and received the termination signal , otherwise false
        """
        for v in self.end_input:
            logger.info("End input:" + str(v))
        for v in self.end_state:
            logger.info("End state:" + str(v))
        self.state = self.state_list[0]
        logger.info("Execute: \nStart state= " + self.state)
        state_index = 0
        self.count = 0
        timer = 0
        max_t = 0
        next = None # type: Any
        next_clock = self.input_queue[0][1]
        while self.count < len(self.input_queue):
            if timer >= max_t and next_clock == self.clock:
                if self.state in self.end_state and self.input_queue[self.count][0] in self.end_input:
                    logger.info("Terminal: at clock " +
                                str(self.clock) +
                                "\t,\tstate: " +
                                str(self.state) +
                                "\t,\tinput : " +
                                str(self.input_queue[self.count][0]))
                    self.final = True

                    record = [self.clock, self.state, str(self.input_queue[self.count][0]), None]
                    self.history.append(record)
                    break
                if not next:
                    for s in self.input_list.keys():
                        if self.input_list[s] == self.input_queue[self.count][0]:
                            index = s
                    next_clock = self.input_queue[self.count + 1][1]
                    next = self.action_table[state_index][index]
                    if next == []:
                        logger.error("Unknown state transition.")
                        break
                    max_t = next[1]
                    timer = 0
                    logger.info("receive signal: at clock " +
                                str(self.clock) +
                                "\t,\tinput : " +
                                str(self.input_list[index]))
                else:

                    for s in self.input_list.keys():
                        if self.input_list[s] == self.input_queue[self.count][0]:
                            index = s
                    if len(self.input_queue) == self.count + 1:
                        next_clock = next_clock + 10
                    else:
                        next_clock = self.input_queue[self.count + 1][1]
                    next = self.action_table[state_index][index]
                    if next == []:
                        logger.error("Unknown state transition.")
                        break
                    logger.info("receive signal: at clock " +
                                str(self.clock) +
                                "\t,\tinput : " +
                                str(self.input_list[index]))
                    max_t = next[1]
                    timer = 0
            elif timer == max_t:
                logger.info("transition: at clock " +
                            str(self.clock) +
                            "\t,\tcurrent_state: " +
                            str(self.state) +
                            "\t,\tinput : " +
                            str(self.input_list[index]) +
                            "\t,\tnext_state : " +
                            str(self.state_list[next[0]]))
                record = [self.clock, self.state, str(self.input_list[index]), str(self.state_list[next[0]])]
                self.history.append(record)

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
