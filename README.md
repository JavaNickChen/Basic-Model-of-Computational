 

# Title  
	Basic-Model-of-Computational for Laboratory Works of CPO Course    
	
# Group Name and List of Group Menmber      
	Group Name: PZEZ  
	Group Member:   Chen Jinhua && Wang Maoyu       
	
# Laboratory Work Number    
	2    
	
# Variant Description   
	Variant： eDSL for finite state machine
    Sub-variant: Mealy type of finite state machine    
	
# Synopsis
As a team, Chen Jinhua and Wang Maoyu completed the tasks required by CPO Lab 2. We have finished a interpreter based on finite state machine. Chen Jinhua, and Wang Maoyu is responsible for the basic code of the program.

A finite state machine interpreter can be used to simulate a Mealy type finite state machine and can interpret and execute the corresponding input signal string. The interpreter supports file format input, and if it reaches the end state during execution, it returns the corresponding pass information. When encountering illegal input and illegal state transition, the program will output an ERROR message. The specific program execution process and error messages will be output in the console and log files at the same time through python logging. 

Our code has been committed into the github https: 
      
	https://github.com/JavaNickChen/Basic-Model-of-Computational    

# Contribution Summary for Each Group Member
Chen, Jinhua has completed the mutable version of the dictionary structure. The code he has completed is under the file path 'SRC /Chen';     
 
Wang, Maoyu has implemented an immutable version of the dictionary structure, and the code he has completed is under the file path 'SRC /Wang'.    

# Explanation of Taken Design Decisions and Analysis   

In our program architecture, we use ordered dictionaries and ordered lists to save the input state, input character set, and state transitions. The state and input character set are stored in the ordered dictionary, and the dictionary key is the index. By reading the state transition, we build the state transition table in a nested dictionary. The row index and column index of the state transition table correspond to the state index and the input character index respectively. When the program is executing, we can obtain the state transition of the automaton by querying the state transition table. 
In our program, the clock cycle is added to the execution phase. We can set the time required for each state transition, or customize the time point of input signal input. 
Our program also supports file input, logging output state machine error information and execution information, and building a visual diagram of the state machine through graphviz. 

# Work Demonstration

File input：
State transition form ：(Current state)-->(input signal)-->(Transition state):(time)
Add a state: $(State name)
Add a input character : %(character name)
Add a termination state: >(state name)
Add a termination signal: <(signal name)
Add a input signal sequence: #(signal1 time1,signal2 time2,signal3 time3,...)#
Please note that the  "(" and ")" in the above representation is used to identify what should be filled in here. There are no parentheses"( "or" )"in the file input form.

# Conclusion   
According to the test results, the dictionary model After testing and verification, the program we designed can effectively complete the interpretation task and simulation task of the mealy finite state machine. Our model also supports visualization and file input, which basically meets the experimental requirements. Further work may be to abstract the state as a separate class, as well as richer and detailed automata execution information and error feedback.