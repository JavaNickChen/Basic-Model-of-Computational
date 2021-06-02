 

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
Our program, a finite state machine interpreter, can be used to simulate a Mealy type finite state machine and can interpret and execute the corresponding input signal string. The interpreter supports file format input, defining and visulizing computational process models, and tracing the inperpreter work. Besides, if the interpreter reaches the end state during execution, it returns the corresponding pass information. When encountering illegal input and illegal state transition, the program will output an ERROR message. The specific program execution process and error messages will be output in the console and log files at the same time through python logging. 

Our code has been committed into the github https: 
      
	https://github.com/JavaNickChen/Basic-Model-of-Computational    

# Contribution Summary for Each Group Member
After reading the experimental files, Chen gave a general framework of the software, and discussed with Wang how to modify the framework and how to implement it. Later, Wang implemented the first version of the program through coding. After that, Chen tested the program and gave feedback. The tests and modifications are then iterated to get this version of the program.   

# Explanation of Taken Design Decisions and Analysis   

In our program architecture, we use ordered dictionaries and ordered lists to save the input state, input event set, and state transition rules. The state and input event set are stored in the ordered dictionary, and the dictionary key is the index. By reading the state transition, we build the state transition table in a nested dictionary. The row index and column index of the state transition table correspond to the state index and the input event index respectively. When the program is executing, we can obtain the state transition relationship of the automaton by querying the state transition table.       

In our program, the clock cycle is added to the execution phase. We can set the time required for each state transition and customize the time point when the events happen.       

Our program also supports file input(use the 'input_from_file' function), logging error information or execution information of state machine, and building a visual diagram of the state machine through graphviz(use the 'create_graph' function). 

# File Input Function Demonstration

File input：      
	State transition form ：(Current state)-->(input signal)-->(Transition state):(time)      
	Add a state: $(State name)      
	Add a input character : %(character name)      
	Add a termination state: >(state name)      
	Add a termination signal: <(signal name)      
	Add a input signal sequence: #(signal1 time1,signal2 time2,signal3 time3,...)#          

Please note that the "(" and ")" in the above representation are used to identify what should be filled in here. There are no parentheses "(" or ")" in the file input form.

# Conclusion   
The interpreter model, after testing and verification, can effectively complete the interpretation task and simulation task of the mealy finite state machine. Our model supports defining computation process model, visualization, tracing the work, and file input, which basically meets the experimental requirements. Further work may be to abstract the state as a separate class, as well as richer and detailed automata execution information and error feedback.
