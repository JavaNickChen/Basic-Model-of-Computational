import collections
from graphviz import Digraph
import logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.txt", mode='w')
fh.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.addHandler(fh)
class interpreter:
    def __init__(self):
        self.state_count = 0
        self.state_list = collections.OrderedDict()
        self.input_count = 0
        self.input_list = collections.OrderedDict()
        self.state=0
        self.end_state=[]
        self.end_input=[]
        self.input_queue=collections.OrderedDict()
        self.trans_list=[]
        self.final = False
        self.clock=0
        self.count=0
        self.action_table=[]

    def input_from_file(self,filename):
        f = open(filename)
        while 1:
            lines = f.readlines()
            if not lines:
                break
            for line in lines:
                if line[0]=='$':
                    lt = line.strip("\n").strip("$")
                    self.add_state(lt)
                elif line[0]=='%':
                    lt = line.strip("\n").strip("%")
                    self.add_input(lt)
                elif line[0]=='#' and line[len(line)-1]=='#':
                    lt=line.strip("\n").strip("#").split(",")
                    for e in lt:
                        self.input_signal(e)
                else:
                    lt = line.strip("\n").split(":")
                    at = lt[0].split("-->")
                    if len(lt) != 2 or len(at) != 3:
                        logger.error("Input invalid.")
                    else:
                        self.add_trans(at[0], at[1], at[2], int(lt[1]))


    def create_action_table(self):
        state_num = self.state_count
        input_num = self.input_count
        logger.info("Create the action table.")
        logger.info("Number of states: "+str(state_num)+" Number of input character: "+str(input_num))
        self.action_table=[]
        for i in range(state_num):
            temp_list = []
            for j in range(input_num):
                temp_list.append([])
            self.action_table.append(temp_list)
        for t in self.trans_list:
            for s in self.state_list.keys():
                if self.state_list[s]==t[0]:
                    inct=s
                if self.state_list[s]==t[2]:
                    outt=s
            for s in self.input_list.keys():
                if self.input_list[s]==t[1]:
                    inrt=s
            self.action_table[inct][inrt]=[outt,t[3]]

    def create_graph(self):
        logger.info("Create a viz graph.")
        g = Digraph('测试图片')
        for i in self.state_list:
            g.node(self.state_list[i],self.state_list[i])
        for t in self.trans_list:
            g.edge(str(t[0]), str(t[2]),label=str(t[1])+" "+str(t[3]))
        g.view()


    def add_state(self,state):
        self.state_list[self.state_count]=state
        self.state_count+=1

    def add_input(self,input):
        self.input_list[self.input_count] =input
        self.input_count += 1

    def add_trans(self,ins,inc,outs,times):
        if ins not in self.state_list.values():
            self.state_list[self.state_count]=ins
            self.state_count+=1
        if outs not in self.state_list.values():
            self.state_list[self.state_count] = outs
            self.state_count += 1
        if inc not in self.input_list.values():
            self.input_list[self.input_count] = inc
            self.input_count += 1
        self.trans_list.append([ins,inc,outs,times])

    def input_signal(self,inc):
        self.input_queue[self.count]=inc
        self.count += 1

    def execute(self):
        self.state=self.state_list[0]
        logger.info("Execute: Start state= "+self.state)
        state_index=0
        self.count=0
        timer=0
        max_t=0
        while self.count< len(self.input_queue):
            if self.state in self.end_state and self.input_queue[self.count] in self.end_input:
                self.final=True
                break
            if timer<max_t:
                timer+=1
            else:
                for s in self.input_list.keys():
                    if self.input_list[s] == self.input_queue[self.count]:
                        index = s
                next = self.action_table[state_index][index]
                if next == []:
                    logger.error("Unknown state transition.")
                    break
                else:
                    logger.info("trans: at clock "+ str(self.clock)+" ori_state: "+str(self.state)+" input : "+ str(self.input_list[index])+" next_state : "+str(self.state_list[next[0]]))
                self.state = self.state_list[next[0]]
                state_index = next[0]
                max_t=next[1]
                timer=0
                self.count+=1
            self.clock += 1

        if self.final:
            logger.info("Reach the end state.")
        else:
            logger.info("Not reach the end state.")


if __name__ == "__main__":
    intp=interpreter()
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
    intp.input_signal("TURN ON")
    intp.input_signal("TURN GREEN")
    intp.input_signal("TURN YELLOW")
    intp.input_signal("TURN RED")
    intp.input_signal("TURN OFF")
    intp.create_action_table()
    intp.end_state.append("RED")
    intp.end_input.append("TURN OFF")
    intp.execute()
    intp.create_graph()














